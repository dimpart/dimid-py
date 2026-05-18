#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2022 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

import os
import sys

from dimsdk import ID

path = os.path.abspath(__file__)
path = os.path.dirname(path)
path = os.path.dirname(path)
path = os.path.dirname(path)
sys.path.insert(0, path)

from dimid.utils import SysArgvParser
from dimid.utils import init_logger
from dimid.utils import LogLevel
from dimid.utils import Runner

from dimid.register.shared import GlobalVariable
from dimid.register.shared import create_config, show_help
from dimid.register.shared import generate, modify


#
# show logs
#
LOG_LEVEL = LogLevel.DEVELOP


DEFAULT_CONFIG = '/etc/dim/config.ini'


async def async_main():
    #
    #  parse cmd parameters
    #
    sys_argv = SysArgvParser.parse(shortopts='hf:ld:',
                                   longopts=['help', 'config=', 'log-location', 'log-dir='])
    if sys_argv is None:
        show_help(default_config=DEFAULT_CONFIG)
        sys.exit(1)
    #
    #  init logger
    #
    show_location = sys_argv.has_opt(opt='log-location')
    init_logger(name='register', level=LOG_LEVEL, show_location=show_location)
    #
    #  create global variable
    #
    shared = GlobalVariable()
    config = await create_config(default_config=DEFAULT_CONFIG, sys_argv=sys_argv)
    await shared.prepare(config=config)
    #
    #  Check Actions
    #
    args = sys_argv.args
    if len(args) == 1 and args[0] == 'generate':
        await generate(database=shared.adb)
    elif len(args) == 2 and args[0] == 'modify':
        identifier = ID.parse(identifier=args[1])
        assert identifier is not None, 'ID error: %s' % args[1]
        await modify(identifier=identifier, database=shared.adb)
    else:
        show_help(default_config=DEFAULT_CONFIG)


def main():
    Runner.sync_run(main=async_main())


if __name__ == '__main__':
    main()
