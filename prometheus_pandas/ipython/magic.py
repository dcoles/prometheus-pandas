import datetime

from IPython.core.magic import (magics_class, line_magic, cell_magic, Magics)
from IPython.core import magic_arguments

from prometheus_pandas import query
from prometheus_pandas import util


@magics_class
class PrometheusMagics(Magics):
    @magic_arguments.magic_arguments()
    @magic_arguments.argument('url', help='Prometheus host (URL)')
    @magic_arguments.argument('output', nargs='?', help='Output variable')
    @magic_arguments.argument('--time', '-t', help='Evaluation timestamp')
    @magic_arguments.argument('--timeout', '-T', help='Evaluation timeout')
    @magic_arguments.argument('--string-labels', '-S', action='store_true', help='Use string metric labels rather than a `MultiIndex`')
    @cell_magic
    def prometheus_query(self, line, cell):
        args = magic_arguments.parse_argstring(self.prometheus_query, line)

        with query.Prometheus(args.url) as p:
            result = p.query(cell, time=args.time, timeout=args.timeout, string_labels=args.string_labels)

        if args.output:
            self.shell.user_ns[args.output] = result
        else:
            return result

    @magic_arguments.magic_arguments()
    @magic_arguments.argument('url', help='Prometheus host (URL)')
    @magic_arguments.argument('start', help='Start timestamp (`rfc3339 | unix_timestamp`)')
    @magic_arguments.argument('end', help='End timestamp (`rfc3339 | unix_timestamp`)')
    @magic_arguments.argument('step', help='Query resolution step width in `duration` format or float number of seconds')
    @magic_arguments.argument('output', nargs='?', help='Output variable')
    @magic_arguments.argument('--timeout', '-T', help='Evaluation timeout')
    @magic_arguments.argument('--string-labels', '-S', action='store_true', help='Use string metric labels rather than a `MultiIndex`')
    @cell_magic
    def prometheus_query_range(self, line, cell):
        args = magic_arguments.parse_argstring(self.prometheus_query_range, line)

        with query.Prometheus(args.url) as p:
            result = p.query_range(cell, args.start, args.end, args.step, timeout=args.timeout, string_labels=args.string_labels)

        if args.output:
            self.shell.user_ns[args.output] = result
        else:
            return result

    @magic_arguments.magic_arguments()
    @magic_arguments.argument('url', help='Prometheus host (URL)')
    @magic_arguments.argument('duration', help='Query window in `duration` format or float number of seconds')
    @magic_arguments.argument('step', help='Query resolution step width in `duration` format or float number of seconds')
    @magic_arguments.argument('output', nargs='?', help='Output variable')
    @magic_arguments.argument('--timeout', '-T', help='Evaluation timeout')
    @magic_arguments.argument('--string-labels', '-S', action='store_true', help='Use string metric labels rather than a `MultiIndex`')
    @cell_magic
    def prometheus_query_range_now(self, line, cell):
        args = magic_arguments.parse_argstring(self.prometheus_query_range_now, line)
        duration = util.duration(args.duration)
        end = datetime.datetime.now(datetime.timezone.utc)
        start = end - duration

        with query.Prometheus(args.url) as p:
            result = p.query_range(cell, start, end, args.step, timeout=args.timeout, string_labels=args.string_labels)

        if args.output:
            self.shell.user_ns[args.output] = result
        else:
            return result


ip = get_ipython()
ip.register_magics(PrometheusMagics)
