from prometheus_pd import query

from IPython.core.magic import (magics_class, line_magic, cell_magic, Magics)
from IPython.core import magic_arguments


@magics_class
class PrometheusMagics(Magics):
    @magic_arguments.magic_arguments()
    @magic_arguments.argument('url', help='Prometheus host (URL)')
    @magic_arguments.argument('output', nargs='?', help='Output variable')
    @magic_arguments.argument('--time', '-t', help='Evaluation timestamp')
    @magic_arguments.argument('--timeout', '-T', help='Evaluation timeout')
    @cell_magic
    def query(self, line, cell):
        args = magic_arguments.parse_argstring(self.query, line)
        result = query.Prometheus(args.url).query(cell, time=args.time, timeout=args.timeout)

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
    @cell_magic
    def query_range(self, line, cell):
        args = magic_arguments.parse_argstring(self.query_range, line)
        result = query.Prometheus(args.url).query_range(
            cell, args.start, args.end, args.step, timeout=args.timeout)

        if args.output:
            self.shell.user_ns[args.output] = result
        else:
            return result


ip = get_ipython()
ip.register_magics(PrometheusMagics)
