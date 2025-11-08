# Prometheus Pandas

Python library for querying [Prometheus](https://prometheus.io/) and accessing the results as
 [Pandas](https://pandas.pydata.org/) data structures.

This is mostly intended for use in [Jupyter](https://jupyter.org/) notebooks. See [Prometheus.ipynb](Prometheus.ipynb) for an example.

## Example

Evaluate an instant query at a single point in time:

```python
>>> from prometheus_pandas import query
>>>
>>> p = query.Prometheus('http://localhost:9090')
>>> df = p.query('node_cpu_seconds_total{}', '2025-11-01T00:05:00Z')
>>> print(df)
__name__            node_cpu_seconds_total
cpu                                      0
instance                    localhost:9100
job                                   node
mode                                  idle  iowait      irq    nice softirq    steal    system      user
2025-11-01 00:05:00             3273742.09  563.24  1184.02  471.03  765.63  9935.97  22907.48  42498.63
```

Evaluates an expression query over a time range:

```python
>>> from prometheus_pandas import query
>>>
>>> p = query.Prometheus('http://localhost:9090')
>>> df = p.query_range(
        'sum(rate(node_cpu_seconds_total{mode=~"system|user"}[1m])) by (mode)',
        '2025-11-01T00:00:00Z', '2025-11-01T06:00:00Z', '1h')
>>> print(df)
mode                   system      user
2025-11-01 00:00:00  0.005333  0.009556
2025-11-01 01:00:00  0.006667  0.012222
2025-11-01 02:00:00  0.006444  0.009778
2025-11-01 03:00:00  0.006889  0.011111
2025-11-01 04:00:00  0.007111  0.010667
2025-11-01 05:00:00  0.007111  0.012889
2025-11-01 06:00:00  0.007778  0.013333
```

Use string labels instead of a [`pd.MultiIndex`](https://pandas.pydata.org/docs/reference/api/pandas.MultiIndex.html#pandas.MultiIndex):

```python
>>> from prometheus_pandas import query
>>>
>>> p = query.Prometheus('http://localhost:9090')
>>> df = p.query_range(
        'sum(rate(node_cpu_seconds_total{mode=~"system|user"}[1m])) by (mode)',
        '2025-11-01T00:00:00Z', '2025-11-01T06:00:00Z', '1h', string_labels=True)
>>> print(df)
                    {mode="system"} {mode="user"}
2025-11-01 00:00:00        0.005333      0.009556
2025-11-01 01:00:00        0.006667      0.012222
2025-11-01 02:00:00        0.006444      0.009778
2025-11-01 03:00:00        0.006889      0.011111
2025-11-01 04:00:00        0.007111      0.010667
2025-11-01 05:00:00        0.007111      0.012889
2025-11-01 06:00:00        0.007778      0.013333
```

Customizing the HTTP request:

```python
>>> import requests
>>> from prometheus_pandas import query
>>>
>>> http = requests.Session()
>>> http.auth = ('user', 'pass')  # Basic authentication
>>> http.cert = '/path/client.cert'  # X.509 client certificate authentication
>>> http.verify = '/path/to/certfile'  # Custom certificate bundle
>>>
>>> p = query.Prometheus('http://localhost:9090', http)
>>> df = p.query('node_cpu_seconds_total{mode="system"}', '2025-11-01T00:05:00Z')
>>> print(df)
__name__            node_cpu_seconds_total
cpu                                      0
instance                    localhost:9100
job                                   node
mode                                system
2025-11-01 00:05:00               22907.48
```

## Installation

Latest release via [`pip`](https://pip.pypa.io):

```bash
pip install prometheus-pandas [--user]
```

via Git:

```bash
git clone https://github.com/dcoles/prometheus-pandas.git; cd prometheus-pandas
python3 setup.py install [--user]
```

## Licence

Licenced under the [MIT License](https://choosealicense.com/licenses/mit/). See `LICENSE` for details.
