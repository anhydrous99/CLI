import inspect
import argparse


def cli(func):
    module = inspect.getmodule(func)

    if module.__name__ == '__main__':
        argspec = inspect.getfullargspec(func)
        args = argspec.args
        defaults = argspec.defaults
        annotations = argspec.annotations

        n_args = len(args)
        n_defaults = len(defaults) if defaults is not None else 0

        parser = argparse.ArgumentParser(description=func.__doc__)

        for index, arg in enumerate(args):
            d_index = index - (n_args - n_defaults)

            type = str
            if arg in annotations:
                type = annotations[arg]

            default = None
            if d_index >= 0:
                arg = '--' + arg
                default = defaults[d_index]

            parser.add_argument(arg, default=default, type=type)

        args = parser.parse_args()
        args = vars(args)
        func(**args)
