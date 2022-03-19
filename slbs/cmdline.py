from argparse import ArgumentParser
from slbs._state import COMMANDS
from slbs_runtime import slbsError
from inspect import getfullargspec
from os import getcwd
from os.path import basename, splitext

import slbs
import logging
import sys

_LOG = logging.getLogger(__name__)


def main(project_dir=None):
    """
    This function is executed when you run `slbs ...` on the command line. You
    can call this function from your own build script to run slbs as if it were
    called via the above command. For an example, see:
        https://build-system.fman.io/manual/#custom-commands # TODO replace with wiki
    """
    if project_dir is None:
        project_dir = getcwd()
    try:
        slbs.init(project_dir)
        # Load built-in commands:
        from slbs import builtin_commands
        from slbs.builtin_commands import _docker
        from slbs.builtin_commands import _gpg
        from slbs.builtin_commands import _account
        from slbs.builtin_commands import _licensing
        fn, args = _parse_cmdline()
        fn(*args)
    except KeyboardInterrupt:
        print('')
        sys.exit(-1)
    except slbsError as e:
        # Don't print a stack trace for slbsErrors, just their message:
        _LOG.error(str(e))
        sys.exit(-1)


def command(f):
    """
    Use this as a decorator to define custom slbs commands. For an example, see:
        https://build-system.fman.io/manual/#custom-commands  # TODO replace with wiki
    """
    COMMANDS[f.__name__] = f
    return f


def _parse_cmdline():
    parser = _get_cmdline_parser()
    args = parser.parse_args()
    if hasattr(args, 'fn'):
        fn_args = []
        for arg in args.args[:1-len(args.defaults)]:
            fn_args.append(getattr(args, arg))
        for arg, default in zip(args.args[-len(args.defaults):], args.defaults):
            fn_args.append(getattr(args, arg, default))
        return args.fn, fn_args
    return parser.print_help, ()


def _get_cmdline_parser():
    # Were we invoked with `python -m slbs`?
    is_python_m_slbs = splitext(basename(sys.argv[0]))[0] == '__main__'
    if is_python_m_slbs:
        prog = '%s -m slbs' % basename(sys.executable)
    else:
        prog = None
    parser = ArgumentParser(prog=prog, description='slbs')
    subparsers = parser.add_subparsers()
    for cmd_name, cmd_fn in COMMANDS.items():
        cmd_parser = subparsers.add_parser(cmd_name, help=cmd_fn.__doc__)
        argspec = getfullargspec(cmd_fn)
        args = argspec.args or []
        defaults = argspec.defaults or ()
        args_without_defaults = args[:1-len(defaults)]
        args_with_defaults = args[-len(defaults):]
        for arg in args_without_defaults:
            cmd_parser.add_argument(arg)
        for arg, default in zip(args_with_defaults, defaults):
            if isinstance(default, bool):
                cmd_parser.add_argument(
                    # TODO check if requires change
                    '--' + arg, action='store_' + str(not default).lower()
                )
            else:
                type_ = None if default is None else type(default)
                cmd_parser.add_argument(arg, default=default, type=type_)
        cmd_parser.set_defaults(fn=cmd_fn, args=args, defaults=defaults)
    return parser
