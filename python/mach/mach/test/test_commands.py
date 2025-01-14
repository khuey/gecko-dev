# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, unicode_literals

import os

from mozunit import main

from buildconfig import topsrcdir
import mach
from mach.test.common import TestBase


class TestCommands(TestBase):
    all_commands = [
        'cmd_bar',
        'cmd_foo',
        'cmd_foobar',
        'mach-commands',
        'mach-completion',
        'mach-debug-commands',
    ]

    def _run_mach(self, args):
        mach_dir = os.path.dirname(mach.__file__)
        providers = [
            'commands.py',
            os.path.join(mach_dir, 'commands', 'commandinfo.py'),
        ]

        def context_handler(key):
            if key == 'topdir':
                return topsrcdir

        return TestBase._run_mach(self, args, providers,
                                  context_handler=context_handler)

    def format(self, targets):
        return "\n".join(targets) + "\n"

    def test_mach_completion(self):
        result, stdout, stderr = self._run_mach(['mach-completion'])
        assert result == 0
        assert stdout == self.format(self.all_commands)

        result, stdout, stderr = self._run_mach(['mach-completion', 'cmd_f'])
        assert result == 0
        # While it seems like this should return only commands that have
        # 'cmd_f' as a prefix, the completion script will handle this case
        # properly.
        assert stdout == self.format(self.all_commands)

        result, stdout, stderr = self._run_mach(['mach-completion', 'cmd_foo'])
        assert result == 0
        assert stdout == self.format(['help', '--arg'])


if __name__ == '__main__':
    main()
