import json
from urllib.parse import urljoin

import numpy as np
import pandas as pd
import requests


class Prometheus:
    def __init__(self, api_url):
        self.http = requests.Session()
        self.api_url = api_url

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.http.close()

    def query(self, query, time=None, timeout=None):
        """
        Evaluates an instant query at a single point in time.

        :param query: Prometheus expression query string.
        :param time: Evaluation timestamp. Optional.
        :param timeout: Evaluation timeout. Optional.
        :return: Pandas DataFrame or Series.
        """
        params = {'query': query}
        params.update({'time': time} if time is not None else {})
        params.update({'timeout': timeout.total_seconds()} if timeout is not None else {})

        return to_pandas(self._do_query('api/v1/query', params))

    def query_range(self, query, start, end, step, timeout=None):
        """
        Evaluates an expression query over a range of time.

        :param query: Prometheus expression query string.
        :param start: Start timestamp.
        :param end: End timestamp.
        :param step: Query resolution step width in `duration` format or float number of seconds.
        :param timeout: Evaluation timeout. Optional.
        :return: Pandas DataFrame.
        """
        params = {'query': query, 'start': start, 'end': end, 'step': step}
        params.update({'timeout': timeout} if timeout is not None else {})

        return to_pandas(self._do_query('api/v1/query_range', params))

    def _do_query(self, path, params):
        resp = self.http.get(urljoin(self.api_url, path), params=params)
        if not (resp.status_code // 100 == 200 or resp.status_code in [400, 422, 503]):
            resp.raise_for_status()

        response = resp.json()
        if response['status'] != 'success':
            raise RuntimeError('{errorType}: {error}'.format_map(response))

        return response['data']


def to_pandas(data):
    """Convert Prometheus data object to Pandas object."""
    result_type = data['resultType']
    if result_type == 'vector':
        return pd.Series((np.float64(r['value'][1]) for r in data['result']),
                         index=(metric_name(r['metric']) for r in data['result']))
    elif result_type == 'matrix':
        return pd.DataFrame({
            metric_name(r['metric']):
                pd.Series((np.float64(v[1]) for v in r['values']),
                          index=(pd.Timestamp(v[0], unit='s') for v in r['values']))
            for r in data['result']})
    elif result_type == 'scalar':
        return np.float64(data['result'])
    elif result_type == 'string':
        return data['result']
    else:
        raise ValueError('Unknown type: {}'.format(result_type))


def metric_name(metric):
    """Convert metric labels to standard form."""
    name = metric.get('__name__', '')
    labels = ','.join(('{}={}'.format(k, json.dumps(v)) for k, v in metric.items() if k != '__name__'))
    return '{0}{{{1}}}'.format(name, labels)
