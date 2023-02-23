import sys as _sys
import time as _time

from datetime import datetime as _dt


def progress_bar(n, total, stamp, bar_length=50):
    stamp = _time.strftime('%M:%S', _time.gmtime(stamp))

    progress = float(n) / total
    bar = int(round(progress * bar_length)-1)
    arrow = '-' * bar + '>'
    empty = bar_length - len(arrow)
    spaces = ' ' * empty
    format = arrow + spaces
    percent = int(round(progress * 100))
    progress = '\rPercent: [{0}] {1}%  Time: {2}'.format(
        format, percent, stamp)

    _sys.stdout.write(progress)
    _sys.stdout.flush()


def millisecond_to_datetime(millisecond):
    second = millisecond / 1000
    stamp = _dt.fromtimestamp(second)

    return stamp
