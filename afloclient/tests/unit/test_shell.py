# Copyright 2013 OpenStack Foundation
# Copyright (C) 2013 Yahoo! Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import argparse
import fixtures
import mock
import os
import six
import sys

import keystoneclient
from keystoneclient import exceptions as ks_exc

from afloclient import exc
from afloclient import shell as openstack_shell
from afloclient.tests.unit import keystone_client_fixtures
from afloclient.tests.unit import utils

_old_env = None

DEFAULT_AFLO_URL = 'http://127.0.0.1:5000/'
DEFAULT_USERNAME = 'username'
DEFAULT_PASSWORD = 'password'
DEFAULT_TENANT_ID = 'tenant_id'
DEFAULT_TENANT_NAME = 'tenant_name'
DEFAULT_PROJECT_ID = '0123456789'
DEFAULT_USER_DOMAIN_NAME = 'user_domain_name'
DEFAULT_UNVERSIONED_AUTH_URL = 'http://127.0.0.1:5000/'
DEFAULT_V2_AUTH_URL = 'http://127.0.0.1:5000/v2.0/'
DEFAULT_V3_AUTH_URL = 'http://127.0.0.1:5000/v3/'
DEFAULT_AUTH_TOKEN = ' 3bcc3d3a03f44e3d8377f9247b0ad155'
TEST_SERVICE_URL = 'http://127.0.0.1:5000/'

FAKE_V2_ENV = {'OS_USERNAME': DEFAULT_USERNAME,
               'OS_PASSWORD': DEFAULT_PASSWORD,
               'OS_TENANT_NAME': DEFAULT_TENANT_NAME,
               'OS_AUTH_URL': DEFAULT_V2_AUTH_URL,
               'OS_AFLO_URL': DEFAULT_AFLO_URL}

FAKE_V3_ENV = {'OS_USERNAME': DEFAULT_USERNAME,
               'OS_PASSWORD': DEFAULT_PASSWORD,
               'OS_PROJECT_ID': DEFAULT_PROJECT_ID,
               'OS_USER_DOMAIN_NAME': DEFAULT_USER_DOMAIN_NAME,
               'OS_AUTH_URL': DEFAULT_V3_AUTH_URL,
               'OS_AFLO_URL': DEFAULT_AFLO_URL}


class ShellTest(utils.TestCase):
    # auth environment to use
    auth_env = FAKE_V2_ENV.copy()
    # expected auth plugin to invoke
    auth_plugin = 'keystoneclient.auth.identity.v2.Password'

    # Patch os.environ to avoid required auth info
    def make_env(self, exclude=None):
        env = dict((k, v) for k, v in self.auth_env.items() if k != exclude)
        self.useFixture(fixtures.MonkeyPatch('os.environ', env))

    def setUp(self):
        super(ShellTest, self).setUp()
        global _old_env
        _old_env, os.environ = os.environ, self.auth_env

        global shell, _shell, assert_called, assert_called_anytime
        _shell = openstack_shell.OpenStackClientShell()
        shell = lambda cmd: _shell.main(cmd.split())

    def tearDown(self):
        super(ShellTest, self).tearDown()
        global _old_env
        os.environ = _old_env

    def shell(self, argstr, exitcodes=(0,)):
        orig = sys.stdout
        orig_stderr = sys.stderr
        try:
            sys.stdout = six.StringIO()
            sys.stderr = six.StringIO()
            _shell = openstack_shell.OpenStackClientShell()
            _shell.main(argstr.split())
        except SystemExit:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.assertIn(exc_value.code, exitcodes)
        finally:
            stdout = sys.stdout.getvalue()
            sys.stdout.close()
            sys.stdout = orig
            stderr = sys.stderr.getvalue()
            sys.stderr.close()
            sys.stderr = orig_stderr
        return (stdout, stderr)

    def test_help_unknown_command(self):
        shell = openstack_shell.OpenStackClientShell()
        argstr = 'help foofoo'
        self.assertRaises(exc.CommandError, shell.main, argstr.split())

    def test_help(self):
        shell = openstack_shell.OpenStackClientShell()
        argstr = 'help'
        actual = shell.main(argstr.split())
        self.assertEqual(0, actual)

    def test_help_on_subcommand_error(self):
        self.assertRaises(exc.CommandError, self.shell, 'help bad')

    def test_get_base_parser(self):
        test_shell = openstack_shell.OpenStackClientShell()
        actual_parser = test_shell.get_base_parser()
        description = 'Command-line interface to the OpenStack Aflo API.'
        expected = argparse.ArgumentParser(
            prog='aflo', usage=None,
            description=description,
            conflict_handler='error',
            add_help=False,
            formatter_class=openstack_shell.HelpFormatter,)
        # NOTE(guochbo): Can't compare ArgumentParser instances directly
        # Convert ArgumentPaser to string first.
        self.assertEqual(str(expected), str(actual_parser))

    @mock.patch.object(openstack_shell.OpenStackClientShell,
                       '_get_versioned_client')
    def test_cert_and_key_args_interchangeable(self,
                                               mock_versioned_client):
        # make sure --os-cert and --os-key are passed correctly
        args = '--os-cert mycert --os-key mykey ticket-list'
        self.shell(args)
        assert mock_versioned_client.called
        ((api_version, args), kwargs) = mock_versioned_client.call_args
        self.assertEqual('mycert', args.os_cert)
        self.assertEqual('mykey', args.os_key)

        # make sure we get the same thing with --cert-file and --key-file
        args = '--cert-file mycertfile --key-file mykeyfile ticket-list'
        aflo_shell = openstack_shell.OpenStackClientShell()
        aflo_shell.main(args.split())
        assert mock_versioned_client.called
        ((api_version, args), kwargs) = mock_versioned_client.call_args
        self.assertEqual('mycertfile', args.os_cert)
        self.assertEqual('mykeyfile', args.os_key)

    @mock.patch('afloclient.v1.client.Client')
    def test_no_auth_with_token_and_ticket_url_with_v1(self, v1_client):
        # test no authentication is required if both token and endpoint url
        # are specified
        args = ('--os-auth-token mytoken --os-aflo-url '
                'https://ticket:1234/v1 '
                'ticket-list')
        aflo_shell = openstack_shell.OpenStackClientShell()
        aflo_shell.main(args.split())
        assert v1_client.called
        (args, kwargs) = v1_client.call_args
        self.assertEqual('mytoken', kwargs['token'])
        self.assertEqual('https://ticket:1234', args[0])

    def _assert_auth_plugin_args(self, mock_auth_plugin):
        # make sure our auth plugin is invoked with the correct args
        mock_auth_plugin.assert_called_once_with(
            keystone_client_fixtures.V2_URL,
            self.auth_env['OS_USERNAME'],
            self.auth_env['OS_PASSWORD'],
            tenant_name=self.auth_env['OS_TENANT_NAME'],
            tenant_id='')

    @mock.patch('afloclient.v1.client.Client')
    @mock.patch('keystoneclient.session.Session')
    @mock.patch.object(keystoneclient.discover.Discover, 'url_for',
                       side_effect=[keystone_client_fixtures.V2_URL, None])
    def test_auth_plugin_invocation_with_v1(self,
                                            v1_client,
                                            ks_session,
                                            url_for):
        with mock.patch(self.auth_plugin) as mock_auth_plugin:
            args = 'ticket-list'
            aflo_shell = openstack_shell.OpenStackClientShell()
            aflo_shell.main(args.split())
            self._assert_auth_plugin_args(mock_auth_plugin)

    @mock.patch('afloclient.v1.client.Client')
    @mock.patch('keystoneclient.session.Session')
    @mock.patch.object(keystoneclient.discover.Discover, 'url_for',
                       side_effect=[keystone_client_fixtures.V2_URL,
                                    keystone_client_fixtures.V3_URL])
    def test_auth_plugin_invocation_with_unversioned_auth_url_with_v1(
            self, v1_client, ks_session, url_for):
        with mock.patch(self.auth_plugin) as mock_auth_plugin:
            args = '--os-auth-url %s ticket-list' % (
                keystone_client_fixtures.BASE_URL)
            aflo_shell = openstack_shell.OpenStackClientShell()
            aflo_shell.main(args.split())
            self._assert_auth_plugin_args(mock_auth_plugin)

    @mock.patch.object(openstack_shell.OpenStackClientShell, 'main')
    def test_shell_keyboard_interrupt(self, mock_shell):
        # Ensure that exit code is 130 for KeyboardInterrupt
        try:
            mock_shell.side_effect = KeyboardInterrupt()
            openstack_shell.main()
        except SystemExit as ex:
            self.assertEqual(130, ex.code)

    @mock.patch('afloclient.v1.client.Client')
    def test_auth_plugin_invocation_without_username_with_v1(self, v1_client):
        self.make_env(exclude='OS_USERNAME')
        args = 'ticket-list'
        aflo_shell = openstack_shell.OpenStackClientShell()
        self.assertRaises(exc.CommandError, aflo_shell.main, args.split())

    @mock.patch('afloclient.v1.client.Client')
    def test_auth_plugin_invocation_without_auth_url_with_v1(self, v1_client):
        self.make_env(exclude='OS_AUTH_URL')
        args = 'ticket-list'
        aflo_shell = openstack_shell.OpenStackClientShell()
        self.assertRaises(exc.CommandError, aflo_shell.main, args.split())

    @mock.patch('afloclient.v1.client.Client')
    def test_auth_plugin_invocation_without_tenant_with_v1(self, v1_client):
        if 'OS_TENANT_NAME' in os.environ:
            self.make_env(exclude='OS_TENANT_NAME')
        if 'OS_PROJECT_ID' in os.environ:
            self.make_env(exclude='OS_PROJECT_ID')
        args = 'ticket-list'
        aflo_shell = openstack_shell.OpenStackClientShell()
        self.assertRaises(exc.CommandError, aflo_shell.main, args.split())

    @mock.patch('sys.stdin', side_effect=mock.MagicMock)
    @mock.patch('getpass.getpass', side_effect=EOFError)
    def test_password_prompted_ctrlD_with_v2(self, mock_getpass, mock_stdin):
        aflo_shell = openstack_shell.OpenStackClientShell()
        self.make_env(exclude='OS_PASSWORD')
        # We should get Command Error because we mock Ctl-D.
        self.assertRaises(exc.CommandError,
                          aflo_shell.main, ['ticket-list'])
        # Make sure we are actually prompted.
        mock_getpass.assert_called_with('OS Password: ')


class ShellTestWithKeystoneV3Auth(ShellTest):
    # auth environment to use
    auth_env = FAKE_V3_ENV.copy()
    # expected auth plugin to invoke
    auth_plugin = 'keystoneclient.auth.identity.v3.Password'

    def _assert_auth_plugin_args(self, mock_auth_plugin):
        mock_auth_plugin.assert_called_once_with(
            keystone_client_fixtures.V3_URL,
            user_id='',
            username=self.auth_env['OS_USERNAME'],
            password=self.auth_env['OS_PASSWORD'],
            user_domain_id='',
            user_domain_name=self.auth_env['OS_USER_DOMAIN_NAME'],
            project_id=self.auth_env['OS_PROJECT_ID'],
            project_name='',
            project_domain_id='',
            project_domain_name='')

    @mock.patch('afloclient.v1.client.Client')
    @mock.patch('keystoneclient.session.Session')
    @mock.patch.object(keystoneclient.discover.Discover, 'url_for',
                       side_effect=[None, keystone_client_fixtures.V3_URL])
    def test_auth_plugin_invocation_with_v1(self,
                                            v1_client,
                                            ks_session,
                                            url_for):
        with mock.patch(self.auth_plugin) as mock_auth_plugin:
            args = 'ticket-list'
            aflo_shell = openstack_shell.OpenStackClientShell()
            aflo_shell.main(args.split())
            self._assert_auth_plugin_args(mock_auth_plugin)

    @mock.patch('keystoneclient.session.Session')
    @mock.patch('keystoneclient.discover.Discover',
                side_effect=ks_exc.ClientException())
    def test_api_discovery_failed_with_unversioned_auth_url(self,
                                                            ks_session,
                                                            discover):
        args = '--os-auth-url %s ticket-list' % (
            keystone_client_fixtures.BASE_URL)
        aflo_shell = openstack_shell.OpenStackClientShell()
        self.assertRaises(exc.CommandError, aflo_shell.main, args.split())

    def test_bash_completion(self):
        stdout, stderr = self.shell('bash_completion')
        # just check we have some output
        required = [
            'ticket-create',
            'help']
        for r in required:
            self.assertIn(r, stdout.split())
        avoided = [
            'bash_completion',
            'bash-completion']
        for r in avoided:
            self.assertNotIn(r, stdout.split())