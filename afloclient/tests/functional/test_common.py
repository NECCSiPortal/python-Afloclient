#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

"""Test CLI Commands."""
import re

import ddt

from afloclient.tests.functional import base


@ddt.ddt
class ClientTestCommon(base.BaseTestCase):
    """Test CLI Commands."""

    @ddt.data('admin', 'user')
    def test_version(self, role):
        self.clients[role].run_command('', flags='--version')

    @ddt.data('admin', 'user')
    def test_help(self, role):
        help_text = self.clients[role].run_command('help')
        lines = help_text.split('\n')
        self.assertFirstLineStartsWith(lines, 'usage: aflo')

        commands = []
        cmds_start = lines.index('Positional arguments:')
        cmds_end = lines.index('Optional arguments:')
        command_pattern = re.compile('^ {4}([a-z0-9\-\_]+)')
        for line in lines[cmds_start:cmds_end]:
            match = command_pattern.match(line)
            if match:
                commands.append(match.group(1))
        commands = set(commands)
        wanted_commands = set((
            'help',
            'tickettemplate-list', 'tickettemplate-get',
            'ticket-get', 'ticket-list',
            'ticket-create', 'ticket-update',
            'ticket-delete',
            'contract-create',
            'contract-update',
            'contract-delete',
            'contract-get',
            'contract-list',
            'goods-create',
            'goods-update',
            'goods-get',
            'goods-list',
            'catalog-create',
            'catalog-update',
            'catalog-get',
            'catalog-list',
            'catalog-contents-create',
            'catalog-contents-update',
            'catalog-contents-get',
            'catalog-contents-list',
            'price-create',
            'price-update',
            'price-get',
            'price-list'))
        self.assertFalse(wanted_commands - commands)
