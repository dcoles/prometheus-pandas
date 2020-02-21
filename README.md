# Prometheus Pandas

Python library for querying [Prometheus](https://prometheus.io/) and accessing the results as
 [Pandas](https://pandas.pydata.org/) data structures.

This is mostly intended for use in [Jupyter](https://jupyter.org/) notebooks. See [Prometheus.ipynb](Prometheus.ipynb) for an example.

## Example

```
>>> from prometheus_pandas import query
>>>
>>> p = query.Prometheus('http://raspberrypi.lan:9090')
>>> p.query('node_cpu{mode="system"}', '2018-11-23T00:00:00Z')
node_cpu{cpu="cpu2",instance="localhost:9100",job="node",mode="system"}    1041.01
node_cpu{cpu="cpu1",instance="localhost:9100",job="node",mode="system"}    1017.41
node_cpu{cpu="cpu3",instance="localhost:9100",job="node",mode="system"}    1002.68
node_cpu{cpu="cpu0",instance="localhost:9100",job="node",mode="system"}    1121.87
dtype: float64
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
