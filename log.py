import sys
import datetime
from ..utils.utils import utils

class log(object):
    def __init__(self):
        super(log, self).__init__()

        self.utils = utils(__file__)
        self.lock = self.utils.lock

        self.patterns = {
            'CC' : '\033[0m',    'BB' : '\033[1m',
            'D1' : '\033[30;1m', 'D2' : '\033[30;2m',
            'R1' : '\033[31;1m', 'R2' : '\033[31;2m',
            'G1' : '\033[32;1m', 'G2' : '\033[32;2m',
            'Y1' : '\033[33;1m', 'Y2' : '\033[33;2m',
            'B1' : '\033[34;1m', 'B2' : '\033[34;2m',
            'P1' : '\033[35;1m', 'P2' : '\033[35;2m',
            'C1' : '\033[36;1m', 'C2' : '\033[36;2m',
            'W1' : '\033[37;1m', 'W2' : '\033[37;2m',
        }

        self.type = 1
        self.spaces = ' ' * 12
        self.prefix = ''
        self.suffix = ''
        self.value_prefix = ''
        self.value_suffix = ''

    def get_value_prefix(self):
        return eval(self.value_prefix) + ' ' if self.value_prefix else ''

    def get_value_suffix(self):
        return eval(self.value_suffix) + ' ' if self.value_suffix else ''

    def log(self, value, prefix='', suffix='', color='', type=''):
        type = type if type != '' else self.type

        if self.type < type:
            return

        prefix = str(prefix if prefix else self.prefix)
        suffix = str(suffix if suffix else self.suffix)

        value = f"{color}{self.get_value_prefix().replace('{color}', color).replace('{clear}', '[CC]').replace('{prefix}', prefix)}{color}{value}{color}{self.get_value_suffix().replace('{color}', color).replace('{clear}', '[CC]').replace('{suffix}', suffix)}{self.spaces}[CC]"
        with self.lock:
            print(self.utils.colors(value, self.patterns))

    def log_replace(self, value):
        with self.lock:
            sys.stdout.write(self.utils.colors(f'{value}{self.spaces}[CC]\r', self.patterns))
            sys.stdout.flush()
