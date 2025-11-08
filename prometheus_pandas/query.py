import datetime
import json
from typing import Optional, Union
from urllib.parse import urljoin

import numpy as np
import pandas as pd
import requests

Timestamp = Union[str, float, datetime.datetime]  # RFC-3339 string or as a Unix timestamp in seconds
Duration = Union[str, datetime.timedelta]  # Prometheus duration string

class Prometheus:
    def __init__(self, api_url: str, http: Optional[requests.Session] = None):
        """
        Create Prometheus client.

        :param api_url: URL of Prometheus server.
        :param http: Requests Session to use for requests. Optional.
        """
        self.http = http or requests.Session()
        self.api_url = api_url + '/' if not api_url.endswith('/') else api_url

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.http.close()

    def query(self, query: str, time: Optional[Timestamp] = None, timeout: Optional[Duration] = None, string_labels: bool = False) -> Union[pd.Series, pd.DataFrame]:
        """
        Evaluates an instant query at a single point in time.

        :param query: Prometheus expression query string.
        :param time: Evaluation timestamp. Optional.
        :param timeout: Evaluation timeout. Optional.
        :param string_labels: Flatten metric labels to string.
        :return: Pandas DataFrame or Series.
        """
        params = {'query': query}

        if time is not None:
            params['time'] = _json_timestamp(time)

        if timeout is not None:
            params['timeout'] = _json_duration(timeout)

        return to_pandas(self._do_query('api/v1/query', params), string_labels=string_labels)

    def query_range(self, query: str, start: Timestamp, end: Timestamp, step: Union[Duration, float], timeout: Optional[Duration] = None, string_labels: bool = False) -> pd.DataFrame:
        """
        Evaluates an expression query over a range of time.

        :param query: Prometheus expression query string.
        :param start: Start timestamp.
        :param end: End timestamp.
        :param step: Query resolution step width in `duration` format or float number of seconds.
        :param timeout: Evaluation timeout. Optional.
        :param string_labels: Flatten metric labels to string.
        :return: Pandas DataFrame.
        """
        params = {
            'query': query,
            'start': _json_timestamp(start),
            'end': _json_timestamp(end),
            'step': _json_duration(step),
        }

        if timeout is not None:
            params['timeout'] = _json_duration(timeout)

        return to_pandas(self._do_query('api/v1/query_range', params), string_labels=string_labels)

    def _do_query(self, path: str, params: dict) -> dict:
        resp = self.http.get(urljoin(self.api_url, path), params=params)
        if resp.status_code not in [400, 422, 503]:
            resp.raise_for_status()

        response = resp.json()
        if response['status'] != 'success':
            raise RuntimeError('{errorType}: {error}'.format_map(response))

        return response['data']


def to_pandas(data: dict, string_labels: bool = False) -> Union[pd.Series, pd.DataFrame]:
    """Convert Prometheus data object to Pandas data series."""
    if string_labels:
        metric = lambda m: {None: metric_name(m)}
    else:
        metric = lambda m: m

    result_type = data['resultType']

    if result_type == 'vector':
        return pd.DataFrame(
            data=[pd.Series(
                data=[r['value'][1]],
                index=[_timestamp(r['value'][0])],
                dtype=np.float64) for r in data['result']],
            index=pd.MultiIndex.from_frame(pd.DataFrame(metric(r['metric']) for r in data['result']))
        ).T if data['result'] else pd.DataFrame()

    elif result_type == 'matrix':
        return pd.DataFrame(
            data=(pd.Series(
                data=(v[1] for v in r['values']),
                index=(_timestamp(v[0]) for v in r['values']),
                dtype=np.float64) for r in data['result']),
            index=pd.MultiIndex.from_frame(pd.DataFrame(metric(r['metric']) for r in data['result']))
        ).T if data['result'] else pd.DataFrame()

    elif result_type == 'scalar':
        return pd.Series(
            data=[data['result'][1]],
            index=[_timestamp(data['result'][0])],
            dtype=np.float64) if data['result'] else pd.Series()

    elif result_type == 'string':
        return pd.Series(
            data=[data['result'][1]],
            index=[_timestamp(data['result'][0])],
            dtype=str) if data['result'] else pd.Series()

    else:
        raise ValueError('Unknown type: {}'.format(result_type))


def metric_name(metric: dict) -> str:
    """Convert metric labels to standard form."""
    name = metric.get('__name__', '')
    labels = ','.join(('{}={}'.format(k, json.dumps(v)) for k, v in metric.items() if k != '__name__'))
    return '{0}{{{1}}}'.format(name, labels)


def _json_timestamp(value) -> float:
    """Convert to JSON friendly Unix timestamp (seconds)."""
    if isinstance(value, datetime.datetime):
        return value.timestamp()
    else:
        return value


def _json_duration(value) -> float:
    """Convert to JSON friendly duration (seconds)."""
    if isinstance(value, datetime.timedelta):
        return value.total_seconds()
    else:
        return value


def _timestamp(ts_sec: float) -> pd.Timestamp:
    return pd.Timestamp(ts_sec, unit='s')
