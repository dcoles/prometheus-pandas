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
>>> p.query('node_cpu_seconds_total{mode="system"}', '2020-05-10T00:00:00Z')
node_cpu_seconds_total{cpu="0",instance="localhost:9100",job="node",mode="system"}    15706.47
node_cpu_seconds_total{cpu="1",instance="localhost:9100",job="node",mode="system"}    15133.25
node_cpu_seconds_total{cpu="2",instance="localhost:9100",job="node",mode="system"}    15095.59
node_cpu_seconds_total{cpu="3",instance="localhost:9100",job="node",mode="system"}    14649.20
dtype: float64
```

Evaluates an expression query over a time range:

```python
>>> from prometheus_pandas import query
>>>
>>> p = query.Prometheus('http://localhost:9090')
>>> print(p.query_range(
        'sum(rate(node_cpu_seconds_total{mode=~"system|user"}[1m])) by (mode)',
        '2020-10-05T00:00:00Z', '2020-10-05T06:00:00Z', '1h'))
dtype: float64
---
                     {mode="system"}  {mode="user"}
2020-10-05 00:00:00         0.022667       0.038222
2020-10-05 01:00:00         0.015333       0.036667
2020-10-05 02:00:00         0.028000       0.040667
2020-10-05 03:00:00         0.015111       0.034889
2020-10-05 04:00:00         0.015556       0.038000
2020-10-05 05:00:00         0.018444       0.040222
2020-10-05 06:00:00         0.018222       0.035111
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
