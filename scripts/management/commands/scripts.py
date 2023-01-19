import importlib
import traceback
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            dest='module',
            type=str,
            help='模块名'
        )
        parser.add_argument(
            dest='func',
            type=str,
            help='方法名'
        )
        parser.add_argument(
            dest='func_args',
            nargs='*',
            type=str,
            help='方法名'
        )

    def handle(self, *args, **options):
        try:
            mod = importlib.import_module(options["module"])
            method = getattr(mod, options.get('func'))
        except Exception as e:
            print(f'load module func error:{traceback.format_exc()}')
            return
        print(f'run {options["func"]} begin')
        method(*options.get('func_args'))
        print(f'run {options["func"]} end')
