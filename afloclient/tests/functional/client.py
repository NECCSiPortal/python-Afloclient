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

from oslo_config import cfg

from tempest_lib.cli import base

CONF = cfg.CONF

_COMMAND = 'aflo'
_COMMAND_KEY = 'keystone'


class CLIClient(base.CLIClient):

    def run_command(self, action, flags='', params='', fail_ok=False,
                    endpoint_type='publicURL', merge_stderr=False):
        """Executes aflo command for the given action.

        :param action: the cli command to run using client
        :type action: string
        :param flags: any optional cli flags to use
        :type flags: string
        :param params: any optional positional args to use
        :type params: string
        :param fail_ok: if True an exception is not raised when the
                        cli return code is non-zero
        :type fail_ok: boolean
        :param endpoint_type: the type of endpoint for the service
        :type endpoint_type: string
        :param merge_stderr: if True the stderr buffer is merged into stdout
        :type merge_stderr: boolean
        """
        flags += ' --os-endpoint-type %s' % endpoint_type

        # Add the required settings for keystone V3
        # since the ClientBase of Tempest-lib does not cope
        # with the keystone V3 certification.
        if int(CONF.auth_version) == 3:
            if self.username == CONF.username:
                flags += ' --os-project-id %s' % CONF.project_id
                flags += ' --os-user-domain-id %s' % CONF.user_domain_id
            else:
                flags += ' --os-project-id %s' % CONF.admin_project_id
                flags += ' --os-user-domain-id %s' % CONF.admin_user_domain_id

        return self.cmd_with_auth(
            _COMMAND, action, flags, params, fail_ok, merge_stderr)
