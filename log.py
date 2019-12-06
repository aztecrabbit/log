import sys
import time
import datetime
import colorama
from ..utils.utils import utils

colorama.init()

class log(object):
    def __init__(self):
        super(log, self).__init__()

        self.libutils = utils(__file__)
        self.lock = self.libutils.lock

        self.patterns = [
            ('CC', '\033[0m'),    ('BB', '\033[1m'),
            ('D1', '\033[30;1m'), ('D2', '\033[30;2m'),
            ('R1', '\033[31;1m'), ('R2', '\033[31;2m'),
            ('G1', '\033[32;1m'), ('G2', '\033[32;2m'),
            ('Y1', '\033[33;1m'), ('Y2', '\033[33;2m'),
            ('B1', '\033[34;1m'), ('B2', '\033[34;2m'),
            ('P1', '\033[35;1m'), ('P2', '\033[35;2m'),
            ('C1', '\033[36;1m'), ('C2', '\033[36;2m'),
            ('W1', '\033[37;1m'), ('W2', '\033[37;2m'),
        ]

        self.type = 1
        self.prefix = ''
        self.suffix = ''
        self.value_prefix = ''
        self.value_suffix = ''

    def eval(self, value, color):
        return eval(value).replace('{color}', color).replace('{clear}', '[CC]') + ' ' if value else ''

    def get_value_prefix(self, value_prefix, color):
        return self.eval(self.value_prefix if value_prefix is not None else '', color)

    def get_value_suffix(self, value_suffix, color):
        return self.eval(self.value_suffix if value_suffix is not None else '', color)

    def log(self, value, prefix='', suffix='', value_prefix='', value_suffix='', color='', type=''):
        type = type if type != '' else self.type

        if self.type < type:
            return

        prefix = str(prefix if prefix else self.prefix)
        suffix = str(suffix if suffix else self.suffix)

        value = f"{color}{self.get_value_prefix(value_prefix, color).replace('{prefix}', prefix)}{color}{value}{color}{self.get_value_suffix(value_suffix, color).replace('{suffix}', suffix)}[CC]"
        value = self.libutils.colors(value, self.patterns)
        with self.lock:
            sys.stdout.write('\033[K' + value + '\033[0m' + '\n')
            sys.stdout.flush()

    def log_tab(self, value, value_tab, tab='|   ', prefix='', suffix='', value_prefix='', value_suffix='', color='', type=''):
        value += '\n\n'

        for i in range(len(value_tab)):
            value += tab + str(value_tab[i]) + '\n'

        value += tab.rstrip() + '\n'

        self.log(value, prefix=prefix, suffix=suffix, value_prefix=value_prefix, value_suffix=value_suffix, color=color, type=type)

    def log_replace(self, value, color='[G1]'):
        terminal_columns = self.libutils.get_terminal_size()['columns']
        value = value[:terminal_columns-3] + '...' if len(value) > terminal_columns else value
        value = self.libutils.colors(f'{color}{value}', self.patterns)
        with self.lock:
            sys.stdout.write('\033[K' + value + '\033[0m' + '\r')
            sys.stdout.flush()

    def sleep(self, interval=10, value='Resumming in {interval} seconds', value_resumming='Resumming...', color='[R1]', color_resumming='[G1]'):
        while interval > 0:
            if not value:
                interval = interval - 1
                time.sleep(1)
                continue

            self.log_replace(value.replace('{interval}', str(interval)), color=color)
            interval = interval - 1
            time.sleep(1)

        if not value_resumming:
            return

        self.log(value_resumming, color=color_resumming)

    def keyboard_interrupt(self):
        with self.lock:
            sys.stdout.write('\r')
            sys.stdout.flush()
            self.log_tab('Keyboard interrupted', ['Ctrl-C again if not exiting automaticly','Please wait...'], color='[R1]', type=0)
