#!/usr/bin/env python3

from __future__ import print_function as _pf
import argparse as _argparse
import datetime
import sys

import aniso8601
from dateutil import parser as _dateutil_parser
import pytz
import tzlocal


def printf(pformat, *args, **kwargs):
    print_kwargs = {}
    for arg in ('sep', 'end', 'file', 'flush'):
        if arg in kwargs:
            print_kwargs[arg] = kwargs.pop(arg)

    print(pformat.format(*args, **kwargs), **print_kwargs)


def parse_as_iso(string):
    try:
        return aniso8601.parse_datetime(string)
    except Exception:
        try:
            return aniso8601.parse_date(string)
        except Exception as err:
            printf(
                'Can\'t interpret "{}" as an ISO-8601 time: {}',
                string, err,
                file=sys.stderr,
            )
            sys.exit(1)


def now():
    tz = tzlocal.get_localzone()
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    return tz.normalize(now.astimezone(tz))


def parse_now_or_iso(input_string):
    if input_string == 'now':
        return 'now', now()
    else:
        return 'iso-8601', parse_as_iso(input_string)


def best_guess(input_string):
    try:
        return parse_now_or_iso(input_string)
    except:
        pass
    else:
        return 'iso-8601', parsed

    return 'guess', _dateutil_parser.parse(input_string)


def show_input(input_format, input_time):
    if input_format == 'now':
        parenthetical = ' \x1b[1;36m(the current time)\x1b[0m'
    elif input_format == 'guess':
        parenthetical = ' \x1b[1;33m(guessing)\x1b[0m'
    else:
        parenthetical = ''

    printf('\x1b[1mYour input:\x1b[0m {}{}', input_time, parenthetical)


def show_delta(input_time):
    if input_time.tzinfo is None:
        print('Don\'t know the duration to a naive time.')
        #print('{} in UTC, {} in your local time ({})', .format(
        datetime.datetime.utcnow()


def show_in_tz(dt, tz):
    if dt.tzinfo is None:
        return  # can't covert due to being a naïve datetime.

    if tz.zone == getattr(dt.tzinfo, 'zone', None):
        return  # already in the user's TZ!

    tzd_dt = tz.normalize(dt.astimezone(tz))
    printf(
        '\x1b[1mIn \x1b[36m{}\x1b[0;1m:\x1b[0m {}', tz, tzd_dt,
    )


def show_in_your_tz(dt):
    your_tz = tzlocal.get_localzone()
    show_in_tz(dt, your_tz)


def show_in_utc(dt):
    show_in_tz(dt, pytz.UTC)


def show_as_posix_timestamp(dt):
    if dt.tzinfo is None:
        return
    dt = pytz.UTC.normalize(dt.astimezone(pytz.UTC))
    epoch = pytz.UTC.localize(datetime.datetime(1970, 1, 1))
    seconds = (dt - epoch).total_seconds()
    printf(
        '\x1b[1mAs a \x1b[36mPOSIX timestamp\x1b[0;1m:\x1b[0m {}', seconds,
    )


def main():
    def tz_type(value):
        return pytz.timezone(value)

    parser = _argparse.ArgumentParser()
    parser.add_argument(
        'input_time', nargs='?', default='now')
    parser.add_argument(
        '--guess', dest='method', action='store_const', const='guess')
    parser.add_argument('--tz', type=tz_type)
    parser.add_argument('--output-tz', type=tz_type)

    pargs = parser.parse_args()

    if pargs.method is None:
        input_format, input_time = parse_now_or_iso(pargs.input_time)
    if pargs.method == 'guess':
        input_format, input_time = best_guess(pargs.input_time)

    if pargs.tz:
        if input_time.tzinfo is not None:
            print(
                'The input time already has timezone information associated'
                ' with it. (It was either determined automatically, or it was'
                ' specified in the input string.) --tz isn\'t needed. If you'
                ' want to set the timezone on the \x1b[4moutput\x1b[0m'
                ' timezone, then use \x1b[1;36m--output-tz\x1b[0m.',
                file=sys.stderr,
            )
            sys.exit(1)
        input_time = pargs.tz.localize(input_time)

    show_input(input_format, input_time)
    #if input_format != 'now':
    #    show_delta(input_format, input_time)

    show_in_your_tz(input_time)
    show_in_utc(input_time)
    show_as_posix_timestamp(input_time)


if __name__ == '__main__':
    main()
