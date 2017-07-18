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

"""Test afloclient/v1/shell.py."""

import codecs
import copy
import exceptions
import json
import mock
import os
import testtools

from afloclient.common import utils
from afloclient import exc
from afloclient import shell as gshell
from afloclient.tests.unit.v1 import test_tickets
from afloclient.v1.catalog_contents import CatalogContents
from afloclient.v1.catalog_scope import CatalogScope
from afloclient.v1.catalogs import Catalog
from afloclient.v1.contracts import Contract
from afloclient.v1.goods import Goods
from afloclient.v1.price import Price
from afloclient.v1 import shell as v1shell
from afloclient.v1.tickets import Ticket
from afloclient.v1.valid_catalog import ValidCatalog

FILES_DIR = 'afloclient/tests/unit/v1/operation_definition_files/'

contract_return_data = {
    'contract_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
    'project_id': 'project_id_101',
    'region_id': 'region_id_101',
    'project_name': 'project_name_101',
    'catalog_id': 'catalog_id_101',
    'catalog_name': 'catalog_name_101',
    'num': 101,
    'parent_ticket_template_id': 'parent_ticket_template_id_101',
    'ticket_template_id': 'ticket_template_id_101',
    'parent_ticket_template_name': 'parent_ticket_template_name_101',
    'parent_application_kinds_name': 'parent_application_kinds_name_101',
    'application_kinds_name': 'application_kinds_name_101',
    'cancel_application_id': 'cancel_application_id_101',
    'application_id': 'application_id_101',
    'ticket_template_name': 'ticket_template_name_101',
    'application_name': 'application_name_101',
    'application_date': '2015-06-01T00:00:00.000000',
    'parent_contract_id': 'parent_contract_id_101',
    'lifetime_start': '2015-07-01T00:00:00.000000',
    'lifetime_end': '2015-08-01T00:00:00.000000',
    'created_at': '2015-06-01T00:00:00.000000',
    'updated_at': '2015-06-01T00:00:00.000000',
    'deleted_at': None,
    'deleted': False,
    'expansions': {'expansion_key1': 'expansion_key1',
                   'expansion_key2': 'expansion_key2',
                   'expansion_key3': 'expansion_key3',
                   'expansion_key4': 'expansion_key4',
                   'expansion_key5': 'expansion_key5',
                   },
    'expansions_text': {'expansion_text': 'expansion_text'}
}
contract_print_data = {
    'contract_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
    'project_id': 'project_id_101',
    'region_id': 'region_id_101',
    'project_name': 'project_name_101',
    'catalog_id': 'catalog_id_101',
    'catalog_name': 'catalog_name_101',
    'num': 101,
    'parent_ticket_template_id': 'parent_ticket_template_id_101',
    'ticket_template_id': 'ticket_template_id_101',
    'parent_ticket_template_name': 'parent_ticket_template_name_101',
    'parent_application_kinds_name': 'parent_application_kinds_name_101',
    'application_kinds_name': 'application_kinds_name_101',
    'cancel_application_id': 'cancel_application_id_101',
    'application_id': 'application_id_101',
    'ticket_template_name': 'ticket_template_name_101',
    'application_name': 'application_name_101',
    'application_date': '2015-06-01T00:00:00.000000',
    'parent_contract_id': 'parent_contract_id_101',
    'lifetime_start': '2015-07-01T00:00:00.000000',
    'lifetime_end': '2015-08-01T00:00:00.000000',
    'created_at': '2015-06-01T00:00:00.000000',
    'updated_at': '2015-06-01T00:00:00.000000',
    'deleted_at': None,
    'deleted': False,
    'expansion_key1': 'expansion_key1',
    'expansion_key2': 'expansion_key2',
    'expansion_key3': 'expansion_key3',
    'expansion_key4': 'expansion_key4',
    'expansion_key5': 'expansion_key5',
    'expansion_text': 'expansion_text'
}

goods_return_data = {
    'goods_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00201',
    'region_id': 'region_id_101',
    'goods_name': 'goods_name_101',
    'created_at': '2015-06-01T00:00:00.000000',
    'updated_at': '2015-06-01T00:00:00.000000',
    'deleted_at': None,
    'deleted': False,
    'expansions': {
        'expansion_key1': 'expansion_key1',
        'expansion_key2': 'expansion_key2',
        'expansion_key3': 'expansion_key3',
        'expansion_key4': 'expansion_key4',
        'expansion_key5': 'expansion_key5',
    },
    'expansions_text': {
        'expansion_text': 'expansion_text'
    }
}
goods_print_data = {
    'goods_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00201',
    'region_id': 'region_id_101',
    'goods_name': 'goods_name_101',
    'created_at': '2015-06-01T00:00:00.000000',
    'updated_at': '2015-06-01T00:00:00.000000',
    'deleted_at': None,
    'deleted': False,
    'expansion_key1': 'expansion_key1',
    'expansion_key2': 'expansion_key2',
    'expansion_key3': 'expansion_key3',
    'expansion_key4': 'expansion_key4',
    'expansion_key5': 'expansion_key5',
    'expansion_text': 'expansion_text'
}

catalog_return_data = {
    'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
    'region_id': 'region_id_101',
    'catalog_name': 'catalog_name_101',
    'lifetime_start': '2015-7-1T00:00:00.000000',
    'lifetime_end': '2015-8-1T00:00:00.000000',
    'created_at': '2015-06-01T00:00:00.000000',
    'updated_at': '2015-06-01T00:00:00.000000',
    'deleted_at': None,
    'deleted': False,
    'expansions': {
        'expansion_key1': 'expansion_key1',
        'expansion_key2': 'expansion_key2',
        'expansion_key3': 'expansion_key3',
        'expansion_key4': 'expansion_key4',
        'expansion_key5': 'expansion_key5',
    },
    'expansions_text': {
        'expansion_text': 'expansion_text'
    }
}
catalog_print_data = {
    'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
    'region_id': 'region_id_101',
    'catalog_name': 'catalog_name_101',
    'lifetime_start': '2015-7-1T00:00:00.000000',
    'lifetime_end': '2015-8-1T00:00:00.000000',
    'created_at': '2015-06-01T00:00:00.000000',
    'updated_at': '2015-06-01T00:00:00.000000',
    'deleted_at': None,
    'deleted': False,
    'expansion_key1': 'expansion_key1',
    'expansion_key2': 'expansion_key2',
    'expansion_key3': 'expansion_key3',
    'expansion_key4': 'expansion_key4',
    'expansion_key5': 'expansion_key5',
    'expansion_text': 'expansion_text'
}

catalog_contents_return_data = {
    'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
    'seq_no': 'ea0a4146-fd07-414b-aa5e-dedbeef00501',
    'goods_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00201',
    'goods_num': 'CPU',
    'created_at': '2015-06-01T00:00:00.000000',
    'updated_at': '2015-06-01T00:00:00.000000',
    'deleted_at': None,
    'deleted': False,
    'expansions': {
        'expansion_key1': 'expansion_key1',
        'expansion_key2': 'expansion_key2',
        'expansion_key3': 'expansion_key3',
        'expansion_key4': 'expansion_key4',
        'expansion_key5': 'expansion_key5',
    },
    'expansions_text': {
        'expansion_text': 'expansion_text'
    }
}
catalog_contents_print_data = {
    'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
    'seq_no': 'ea0a4146-fd07-414b-aa5e-dedbeef00501',
    'goods_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00201',
    'goods_num': 'CPU',
    'created_at': '2015-06-01T00:00:00.000000',
    'updated_at': '2015-06-01T00:00:00.000000',
    'deleted_at': None,
    'deleted': False,
    'expansion_key1': 'expansion_key1',
    'expansion_key2': 'expansion_key2',
    'expansion_key3': 'expansion_key3',
    'expansion_key4': 'expansion_key4',
    'expansion_key5': 'expansion_key5',
    'expansion_text': 'expansion_text'
}

catalog_scope_return_data = {
    'id': 'id0a4146-fd07-414b-aa5e-dedbeef00001',
    'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
    'scope': 'bdb8f50f82da4370813e6ea797b1fb101',
    'lifetime_start': '2015-12-31T23:59:59.999999',
    'lifetime_end': '9999-12-31T23:59:59.999999',
    'created_at': '2015-06-01T00:00:00.000000',
    'updated_at': '2015-06-01T00:00:00.000000',
    'deleted_at': None,
    'deleted': False,
    'expansions': {
        'expansion_key1': 'expansion_key1',
        'expansion_key2': 'expansion_key2',
        'expansion_key3': 'expansion_key3',
        'expansion_key4': 'expansion_key4',
        'expansion_key5': 'expansion_key5',
    },
    'expansions_text': {
        'expansion_text': 'expansion_text'
    }
}
catalog_scope_print_data = {
    'id': 'id0a4146-fd07-414b-aa5e-dedbeef00001',
    'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
    'scope': 'bdb8f50f82da4370813e6ea797b1fb101',
    'lifetime_start': '2015-12-31T23:59:59.999999',
    'lifetime_end': '9999-12-31T23:59:59.999999',
    'created_at': '2015-06-01T00:00:00.000000',
    'updated_at': '2015-06-01T00:00:00.000000',
    'deleted_at': None,
    'deleted': False,
    'expansion_key1': 'expansion_key1',
    'expansion_key2': 'expansion_key2',
    'expansion_key3': 'expansion_key3',
    'expansion_key4': 'expansion_key4',
    'expansion_key5': 'expansion_key5',
    'expansion_text': 'expansion_text'
}

valid_catalog_return_data = {
    'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
    'scope': 'Default',
    'catalog_name': 'CATALOG-A-102',
    'catalog_lifetime_start': '2015-12-31T23:59:59.999999',
    'catalog_lifetime_end': '9999-12-31T23:59:59.999999',
    'catalog_scope_id': 'id0a4146-fd07-414b-aa5e-dedbeef000016',
    'catalog_scope_lifetime_start': '2015-12-31T23:59:59.999999',
    'catalog_scope_lifetime_end': '9999-12-31T23:59:59.999999',
    'price_seq_no': 'ea0a4146-fd07-414b-aa5e-dedbeef00005',
    'price': '210.5',
    'price_lifetime_start': '2015-12-31T23:59:59.999999',
    'price_lifetime_end': '9999-12-31T23:59:59.999999'
}

price_return_data = {
    'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
    'scope': 'Default',
    'seq_no': 'ea0a4146-fd07-414b-aa5e-dedbeef00005',
    'price': '1000',
    'lifetime_start': '2015-7-1T00:00:00.000000',
    'lifetime_end': '2015-8-1T00:00:00.000000',
    'created_at': '2015-06-01T00:00:00.000000',
    'updated_at': '2015-06-01T00:00:00.000000',
    'deleted_at': None,
    'deleted': False,
    'expansions': {
        'expansion_key1': 'expansion_key1',
        'expansion_key2': 'expansion_key2',
        'expansion_key3': 'expansion_key3',
        'expansion_key4': 'expansion_key4',
        'expansion_key5': 'expansion_key5',
    },
    'expansions_text': {
        'expansion_text': 'expansion_text'
    }
}
price_print_data = {
    'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
    'scope': 'Default',
    'seq_no': 'ea0a4146-fd07-414b-aa5e-dedbeef00005',
    'price': '1000',
    'lifetime_start': '2015-7-1T00:00:00.000000',
    'lifetime_end': '2015-8-1T00:00:00.000000',
    'created_at': '2015-06-01T00:00:00.000000',
    'updated_at': '2015-06-01T00:00:00.000000',
    'deleted_at': None,
    'deleted': False,
    'expansion_key1': 'expansion_key1',
    'expansion_key2': 'expansion_key2',
    'expansion_key3': 'expansion_key3',
    'expansion_key4': 'expansion_key4',
    'expansion_key5': 'expansion_key5',
    'expansion_text': 'expansion_text'
}


class ShellTest(testtools.TestCase):
    """Test Shell."""

    def setUp(self):
        """Setup test mock."""
        super(ShellTest, self).setUp()
        self._mock_utils()
        self.gc = self._mock_client()

    def _make_args(self, args):
        """Create arguments object.
        :param args: source arguments.
        """

        class Args(object):

            def __init__(self, entries):
                self.__dict__.update(entries)

        return Args(args)

    def _mock_client(self):
        """Create client of mock."""
        my_mocked_gc = mock.Mock()
        my_mocked_gc.schemas.retun_value = 'test'
        my_mocked_gc.get.return_value = {}

        return my_mocked_gc

    def _mock_utils(self):
        """Set utility function of mock."""
        utils.print_list = mock.Mock()
        utils.print_dict = mock.Mock()

    def assert_exits_with_msg(self, func, func_args, err_msg):
        """Test function and add message to result.
        :param func: run test function.
        :param func_args: run test function arguments.
        :param err_msg: error message.
        """
        with mock.patch.object(utils, 'exit') as mocked_utils_exit:
            mocked_utils_exit.return_value = '%s' % err_msg

            func(self.gc, func_args)
            mocked_utils_exit.assert_called_once_with(err_msg)

    def test_do_tickettemplate_get(self):
        """Test ticket template get command.
        """
        input = {'id': '1'}
        args = self._make_args(input)
        with mock.patch.object(self.gc.tickettemplates, 'get') as mocked_func:
            mocked_func.return_value = {}
            columns = ['id', 'ticket_type',
                       'template_contents', 'workflow_pattern_id']

            v1shell.do_tickettemplate_get(self.gc, args)

            mocked_func.assert_called_once_with('1')
            utils.print_list.assert_called_once_with([{}], columns)

    def test_do_tickettemplate_get_empty_args(self):
        """Test ticket template get command by empty args."""
        input = {}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_tickettemplate_get,
                          self.gc,
                          args)

    def test_do_tickettemplate_list(self):
        """Test ticket template list command."""
        args = {}
        with mock.patch.object(self.gc.tickettemplates, 'list') as mocked_func:
            mocked_func.return_value = {}
            columns = ['id', 'ticket_type',
                       'template_contents', 'workflow_pattern_id']

            v1shell.do_tickettemplate_list(self.gc, args)

            mocked_func.assert_called_once_with({})
            utils.print_list.assert_called_once_with({}, columns)

    def test_do_tickettemplate_list_limit_marker(self):
        """Test ticket template list command."""

        input = {'limit': 1,
                 'marker': 'a',
                 'sort_key': 'created_at',
                 'sort_dir': 'desc',
                 'enable_expansion_filters': False,
                 'force_show_deleted': False}
        value = {'limit': 1,
                 'marker': 'a',
                 'sort_key': ['created_at'],
                 'sort_dir': ['desc'],
                 'enable_expansion_filters': False,
                 'force_show_deleted': False}

        args = self._make_args(input)
        with mock.patch.object(self.gc.tickettemplates, 'list') as mocked_func:
            mocked_func.return_value = {}
            columns = ['id', 'ticket_type',
                       'template_contents', 'workflow_pattern_id']

            v1shell.do_tickettemplate_list(self.gc, args)

            called_args, kwargs = mocked_func.call_args

            self.assertEqual(sorted(value.items()),
                             sorted(called_args[0].items()))
            utils.print_list.assert_called_once_with({}, columns)

    def test_do_tickettemplate_list_ticket_type(self):
        """Test 'List search of tickettemplate.'
        Test of if you filtering a ticket type.
        """
        input = {'ticket_type': 'New Contract,request'}
        value = {'ticket_type': 'New Contract,request'}

        args = self._make_args(input)
        with mock.patch.object(self.gc.tickettemplates, 'list') as mocked_func:
            mocked_func.return_value = {}
            columns = ['id', 'ticket_type',
                       'template_contents', 'workflow_pattern_id']

            v1shell.do_tickettemplate_list(self.gc, args)

            called_args, kwargs = mocked_func.call_args

            self.assertEqual(sorted(value.items()),
                             sorted(called_args[0].items()))
            utils.print_list.assert_called_once_with({}, columns)

    def test_do_tickettemplate_create(self):
        """Test 'Create of tickettemplate'.
        A file encode is 'utf-8'.
        """
        self._test_do_tickettemplate_create_file_encode('utf-8')

    def test_do_tickettemplate_create_s_jis(self):
        """Test 'Create of tickettemplate'.
        A file encode is 's-jis'.
        """
        self._test_do_tickettemplate_create_file_encode('s-jis')

    def _test_do_tickettemplate_create_file_encode(self, encode):
        """Test 'Create of tickettemplate'.
        :param encode: File encode.
        """
        file_path = _get_dict_contents_file_path(
            'template_contents', '20160627')
        input = {'file': file_path, 'encode': encode}

        template_contents_string = codecs.open(input['file'],
                                               'r',
                                               input['encode']).read()
        template_contents = json.loads(template_contents_string,
                                       input['encode'])

        value = {'template_contents': template_contents}
        args = self._make_args(input)
        with mock.patch.object(self.gc.tickettemplates,
                               'create') as mocked_func:
            mocked_func.return_value = None
            columns = ['id',
                       'ticket_type',
                       'template_contents', 'workflow_pattern_id']
            v1shell.do_tickettemplate_create(self.gc, args)

            mocked_func.assert_called_once_with(value)
            utils.print_list.assert_called_once_with([None], columns)

    def test_do_tickettemplate_create_invalid_file_encode_irregular(self):
        """Test 'Create of tickettemplate'.
        Test the operation of the parameter without.
        """
        input = {}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_tickettemplate_create,
                          self.gc,
                          args)

    def test_do_tickettemplate_create_no_parameter_irregular(self):
        """Test 'Create of tickettemplate'.
        Test the operation of the parameter without.
        """
        input = {}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_tickettemplate_create,
                          self.gc,
                          args)

    def test_do_tickettemplate_create_not_exists_file_irregular(self):
        """Test 'Create of tickettemplate'.
        Test the operation of the invalid file type.
        """
        input = {'file': '/home/user/aaa.json',
                 'encode': 'utf-8'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_tickettemplate_create,
                          self.gc,
                          args)

    def test_do_tickettemplate_create_invalid_file_irregular(self):
        """Test 'Create of tickettemplate'.
        Test the operation of the invalid file type.
        """
        file_path = _get_dict_contents_file_path('template_contents_invalid')
        input = {'file': file_path,
                 'encode': 'utf-8'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_tickettemplate_create,
                          self.gc,
                          args)

    def test_do_tickettemplate_delete(self):
        """Test delete command."""
        input = {'id': '1'}
        args = self._make_args(input)
        with mock.patch.object(self.gc.tickettemplates,
                               'delete') as mocked_func:
            mocked_func.return_value = {}

            v1shell.do_tickettemplate_delete(self.gc, args)

            mocked_func.assert_called_once_with('1')

    def test_do_tickettemplate_delete_empty_args(self):
        """Test delete command."""
        input = {}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_tickettemplate_delete,
                          self.gc,
                          args)

    def test_do_workflowpattern_create(self):
        """Test 'Create of workflow pattern'."""
        file_path = _get_dict_contents_file_path('workflow_pattern_contents')
        input = {'file': file_path, 'encode': 'utf-8'}

        workflow_pattern_string = codecs.open(input['file'],
                                              'r',
                                              input['encode']).read()
        wf_pattern_contents = json.loads(workflow_pattern_string,
                                         input['encode'])

        value = {'wf_pattern_contents': wf_pattern_contents}
        args = self._make_args(input)
        with mock.patch.object(self.gc.workflowpatterns,
                               'create') as mocked_func:
            mocked_func.return_value = None
            columns = ['id',
                       'code',
                       'wf_pattern_contents']
            v1shell.do_workflowpattern_create(self.gc, args)

            mocked_func.assert_called_once_with(value)
            utils.print_list.assert_called_once_with([None], columns)

    def test_do_workflowpattern_create_s_jis(self):
        """Test 'Create of workflow pattern'."""
        file_path = _get_dict_contents_file_path('workflow_pattern_contents')
        input = {'file': file_path, 'encode': 's-jis'}

        workflow_pattern_string = codecs.open(input['file'],
                                              'r',
                                              input['encode']).read()
        wf_pattern_contents = json.loads(workflow_pattern_string,
                                         input['encode'])

        value = {'wf_pattern_contents': wf_pattern_contents}
        args = self._make_args(input)
        with mock.patch.object(self.gc.workflowpatterns,
                               'create') as mocked_func:
            mocked_func.return_value = None
            columns = ['id',
                       'code',
                       'wf_pattern_contents']
            v1shell.do_workflowpattern_create(self.gc, args)

            mocked_func.assert_called_once_with(value)
            utils.print_list.assert_called_once_with([None], columns)

    def test_do_workflowpattern_create_no_parameter_irregular(self):
        """Test 'Create of workflow pattern'.
        Test the operation of the parameter without.
        """
        input = {}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_workflowpattern_create,
                          self.gc,
                          args)

    def test_do_workflowpattern_create_not_exists_file_irregular(self):
        """Test 'Create of workflow pattern'.
        Test the operation of the invalid file type.
        """
        input = {'file': '/home/user/aaa.json',
                 'encode': 'utf-8'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_workflowpattern_create,
                          self.gc,
                          args)

    def test_do_workflowpattern_create_invalid_file_irregular(self):
        """Test 'Create of workflow pattern'.
        Test the operation of the invalid file type.
        """
        file_path = _get_dict_contents_file_path(
            'workflow_pattern_contents_invalid')
        input = {'file': file_path, 'encode': 'utf-8'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_workflowpattern_create,
                          self.gc,
                          args)

    def test_do_workflowpattern_delete(self):
        """Test delete command."""
        input = {'id': '1'}
        args = self._make_args(input)
        with mock.patch.object(self.gc.workflowpatterns,
                               'delete') as mocked_func:
            mocked_func.return_value = {}

            v1shell.do_workflowpattern_delete(self.gc, args)

            mocked_func.assert_called_once_with('1')

    def test_do_workflowpattern_delete_empty_args(self):
        """Test delete command."""
        input = {}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_workflowpattern_delete,
                          self.gc,
                          args)

    def test_do_ticket_get(self):
        """Test get command."""
        input = {'id': '1'}
        args = self._make_args(input)
        with mock.patch.object(self.gc.tickets, 'get') as mocked_func:
            mocked_func.return_value = \
                copy.deepcopy(
                    test_tickets.fixtures_ticket_data_detail)["ticket"]
            # ticket_columns = v1shell._print_ticket_columns
            v1shell.do_ticket_get(self.gc, args)

            # ticket = \
            #    {
            #        'ticket': {
            #            'id': '1',
            #            'ticket_template_id': '1',
            #            'ticket_type': '1',
            #            'target_id': '1',
            #            'tenant_id': '1',
            #            'owner_id': '1',
            #            'owner_at': '1',
            #            'ticket_detail': '1',
            #            'action_detail': '1',
            #            'created_at': '2015-07-01',
            #            'updated_at': '2015-07-01',
            #            'deleted_at': '2015-07-01',
            #            'deleted': False
            #        }
            #    }
            mocked_func.assert_called_once_with('1')
            # FIXME(core) : This assert method is
            #   tox result success on local machine.
            #   But it is failed on jenkins server tox job.
            # utils.print_list.assert_called(ticket, ticket_columns)

    def test_do_ticket_get_none_ticket(self):
        """Test get command."""
        input = {'id': '1'}
        args = self._make_args(input)
        with mock.patch.object(self.gc.tickets, 'get') as mocked_func:
            mocked_func.return_value = None

            v1shell.do_ticket_get(self.gc, args)

            mocked_func.assert_called_once_with('1')

    def test_do_ticket_get_empty_args(self):
        """Test ticket get command by empty args."""
        input = {}
        args = self._make_args(input)

        self.assertRaises(exceptions.AttributeError,
                          v1shell.do_ticket_get,
                          self.gc,
                          args)

    def test_do_ticket_list(self):
        """Test list command."""
        args = {}
        with mock.patch.object(self.gc.tickets, 'list') as mocked_func:
            mocked_func.return_value = []
            columns = \
                ['id',
                 'ticket_template_id',
                 'ticket_type', 'target_id',
                 'tenant_id',
                 'owner_id', 'owner_at',
                 'ticket_detail', 'action_detail',
                 'last_workflow_id',
                 'last_status',
                 'last_status_code',
                 'last_status_detail',
                 'last_target_role',
                 'last_confirmer_id', 'last_confirmed_at',
                 'last_additional_data']

            v1shell.do_ticket_list(self.gc, args)

            mocked_func.assert_called_once_with({})
            utils.print_list.assert_called_once_with([], columns)

    def test_do_ticket_list_limit_marker_filter(self):
        """Test list command."""
        input = {'tenant_id': '1',
                 'last_status_code': '1',
                 'ticket_template_id': '1',
                 'ticket_type': '1',
                 'target_id': '1',
                 'owner_id': '1',
                 'owner_at_to': '1',
                 'owner_at_from': '1',
                 'last_confirmer_id': '1',
                 'last_confirmed_at_to': '1',
                 'last_confirmed_at_from': '1',
                 "tenant_id": '1',
                 'limit': 1,
                 'marker': 'a',
                 'sort_key': ['text', 'id'],
                 'sort_dir': ['desc', 'asc'],
                 'ticket_template_name': 'a',
                 'application_kinds_name': 'a'}

        args = self._make_args(input)
        with mock.patch.object(self.gc.tickets, 'list') as mocked_func:
            mocked_func.return_value = None
            columns = \
                ['id',
                 'ticket_template_id',
                 'ticket_type', 'target_id',
                 'tenant_id',
                 'owner_id',
                 'owner_at',
                 'ticket_detail', 'action_detail',
                 'last_workflow_id',
                 'last_status',
                 'last_status_code',
                 'last_status_detail',
                 'last_target_role',
                 'last_confirmer_id',
                 'last_confirmed_at',
                 'last_additional_data']

            v1shell.do_ticket_list(self.gc, args)

            called_args, kwargs = mocked_func.call_args

            self.assertEqual(sorted(input.items()),
                             sorted(called_args[0].items()))
            utils.print_list.assert_called_once_with([], columns)

    def test_do_ticket_delete(self):
        """Test delete command."""
        input = {'id': '1'}
        args = self._make_args(input)
        with mock.patch.object(self.gc.tickets, 'delete') as mocked_func:
            mocked_func.return_value = {}

            v1shell.do_ticket_delete(self.gc, args)

            mocked_func.assert_called_once_with('1')

    def test_do_ticket_delete_empty_args(self):
        """Test delete command."""
        input = {}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_ticket_delete,
                          self.gc,
                          args)

    def test_do_ticket_create(self):
        """Test create command."""
        input = {'status_code': 'status_code',
                 'ticket_template_id': '1',
                 'ticket_detail': '{"key": "value"}'}
        args = self._make_args(input)
        with mock.patch.object(self.gc.tickets, 'create') as mocked_func:
            mocked_func.return_value = (None, None)
            columns = v1shell._print_ticket_columns
            v1shell.do_ticket_create(self.gc, args)

            mocked_func.assert_called_once_with(input)
            utils.print_list.assert_called_once_with([None], columns)

    def test_do_ticket_create_empty_ticket_detail(self):
        """Test create command."""
        input = {'ticket_template_id': '1',
                 'status_code': 'status_code'}
        args = self._make_args(input)
        with mock.patch.object(self.gc.tickets, 'create') as mocked_func:
            mocked_func.return_value = (None, None)
            columns = v1shell._print_ticket_columns
            v1shell.do_ticket_create(self.gc, args)

            mocked_func.assert_called_once_with(input)
            utils.print_list.assert_called_once_with([None], columns)

    def test_do_ticket_create_invalid_ticket_detail(self):
        """Test create command."""
        input = {'ticket_template_id': '1',
                 'ticket_detail': '}',
                 'status_code': 'status_code'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_ticket_create,
                          self.gc,
                          args)

    def test_do_ticket_create_empty_status_code(self):
        """Test create command."""
        input = {'ticket_template_id': '1',
                 'ticket_detail': '{"key": "value"}'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_ticket_create,
                          self.gc,
                          args)

    def test_do_ticket_create_empty_args(self):
        """Test ticket get command by empty args."""
        input = {}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_ticket_create,
                          self.gc,
                          args)

    def test_do_ticket_update(self):
        """Test update command.
        """
        input = {'id': '1',
                 'last_workflow_id': '1',
                 'next_workflow_id': '1',
                 'last_status_code': '1',
                 'next_status_code': '1',
                 'additional_data': '{"json": "1"}'}

        args = self._make_args(input)
        with mock.patch.object(self.gc.tickets, 'update') as mocked_func:
            mocked_func.return_value = {}

            v1shell.do_ticket_update(self.gc, args)

            mocked_func.assert_called_once_with(
                input['id'], {'last_workflow_id': '1',
                              'next_workflow_id': '1',
                              'last_status_code': '1',
                              'next_status_code': '1',
                              'additional_data': '{"json": "1"}'})

    def test_do_ticket_update_small(self):
        """Test update command."""
        input = {'id': '1',
                 'last_workflow_id': '1',
                 'next_workflow_id': '1',
                 'last_status_code': '1',
                 'next_status_code': '1'}

        args = self._make_args(input)
        with mock.patch.object(self.gc.tickets, 'update') as mocked_func:
            mocked_func.return_value = {}

            v1shell.do_ticket_update(self.gc, args)

            mocked_func.assert_called_once_with(
                input['id'], {'last_workflow_id': '1',
                              'last_status_code': '1',
                              'next_workflow_id': '1',
                              'next_status_code': '1'})

    def test_do_ticket_update_invalid_additional_data(self):
        """Test create command."""
        input = {'id': '1',
                 'last_workflow_id': '1',
                 'next_workflow_id': '1',
                 'status_code': '1',
                 'additional_data': '{'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_ticket_update,
                          self.gc,
                          args)

    def test_do_ticket_update_empty_args(self):
        """Test update command."""
        input = {}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_ticket_update,
                          self.gc,
                          args)

    def test_join_list_data(self):
        """Test v1 shell _join_list_data method."""
        # Last workflow not exists.
        tickets = Ticket(self,
                         copy.deepcopy(test_tickets.fixtures_ticket_data_row1),
                         loaded=True)
        workflow_id = tickets.last_workflow['id']

        result = v1shell._join_list_data([tickets])

        self.assertEqual(tickets.id,
                         result[0]['id'])
        self.assertEqual(workflow_id,
                         result[0]['last_workflow_id'])

    def test_join_list_data_None(self):
        """Test v1 shell _join_list_data method by all none or ticket none."""
        result = v1shell._join_list_data(None)
        self.assertEqual(result, [])

        result = v1shell._join_list_data([])
        self.assertEqual(result, [])

    def test_join_list_data_workflow_None(self):
        """Test v1 shell _join_list_data method by workflow data none."""
        # Last workflow not exists.
        last_none_tickets = Ticket(self, copy.deepcopy(
            test_tickets.fixtures_ticket_data_row1), loaded=True)
        last_none_tickets.last_workflow = None

        result = v1shell._join_list_data([last_none_tickets])

        self.assertEqual(last_none_tickets.id,
                         result[0]['id'])
        self.assertIsNone(result[0]['last_workflow_id'])

    def test_do_workflow_get(self):
        """Test workflow get command."""
        input = {'id': '1'}
        args = self._make_args(input)
        with mock.patch.object(self.gc.tickets, 'get') as mocked_func:
            data = test_tickets.fixtures_ticket_data_detail
            mocked_func.return_value = \
                Ticket(self,
                       copy.deepcopy(data)["ticket"],
                       loaded=True)
            columns = v1shell._print_workflow_columns
            v1shell.do_workflow_get(self.gc, args)

            mocked_func.assert_called_once_with('1')
            utils.print_list.assert_called_once_with(
                test_tickets.fixtures_ticket_data_detail["ticket"]["workflow"],
                columns)

    def test_do_workflow_get_empty_args(self):
        """Test workflow get command by no args."""
        input = {}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_workflow_get,
                          self.gc,
                          args)

    def test_do_workflow_get_empty_id(self):
        """Test workflow get command by no id."""
        input = {'id': ''}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_workflow_get,
                          self.gc,
                          args)

    def test_do_contract_create(self):
        """Test create command."""
        input = {
            'project_id': 'project_id_101',
            'region_id': 'region_id_101',
            'project_name': 'project_name_101',
            'catalog_id': 'catalog_id_101',
            'catalog_name': 'catalog_name_101',
            'num': 101,
            'parent_ticket_template_id': 'parent_ticket_template_id_101',
            'ticket_template_id': 'ticket_template_id_101',
            'parent_ticket_template_name': 'parent_ticket_template_name_101',
            'parent_application_kinds_name': 'parent_app_kinds_name_101',
            'application_kinds_name': 'application_kinds_name_101',
            'cancel_application_id': 'cancel_application_id_101',
            'application_id': 'application_id_101',
            'ticket_template_name': 'ticket_template_name_101',
            'application_name': 'application_name_101',
            'application_date': '2015-6-1',
            'parent_contract_id': 'parent_contract_id_101',
            'lifetime_start': '2015-7-1',
            'lifetime_end': '2015-8-1',
            'expansion_key1': 'expansion_key1',
            'expansion_key2': 'expansion_key2',
            'expansion_key3': 'expansion_key3',
            'expansion_key4': 'expansion_key4',
            'expansion_key5': 'expansion_key5',
            'expansion_text': 'expansion_text'
        }
        requestparam = {
            'project_id': 'project_id_101',
            'region_id': 'region_id_101',
            'project_name': 'project_name_101',
            'catalog_id': 'catalog_id_101',
            'catalog_name': 'catalog_name_101',
            'num': 101,
            'parent_ticket_template_id': 'parent_ticket_template_id_101',
            'ticket_template_id': 'ticket_template_id_101',
            'parent_ticket_template_name': 'parent_ticket_template_name_101',
            'parent_application_kinds_name': 'parent_app_kinds_name_101',
            'application_kinds_name': 'application_kinds_name_101',
            'cancel_application_id': 'cancel_application_id_101',
            'application_id': 'application_id_101',
            'ticket_template_name': 'ticket_template_name_101',
            'application_name': 'application_name_101',
            'application_date': '2015-6-1',
            'parent_contract_id': 'parent_contract_id_101',
            'lifetime_start': '2015-7-1',
            'lifetime_end': '2015-8-1',
            'expansions': {
                'expansion_key1': 'expansion_key1',
                'expansion_key2': 'expansion_key2',
                'expansion_key3': 'expansion_key3',
                'expansion_key4': 'expansion_key4',
                'expansion_key5': 'expansion_key5',
            },
            'expansions_text': {
                'expansion_text': 'expansion_text'
            }
        }
        args = self._make_args(input)
        with mock.patch.object(self.gc.contracts, 'create') as mocked_func:
            mocked_func.return_value = Contract(self,
                                                contract_return_data,
                                                loaded=True)
            columns = ['contract_id',
                       'region_id',
                       'project_id',
                       'project_name',
                       'catalog_id',
                       'catalog_name',
                       'num',
                       'parent_ticket_template_id',
                       'ticket_template_id',
                       'parent_ticket_template_name',
                       'parent_application_kinds_name',
                       'application_kinds_name',
                       'cancel_application_id',
                       'application_id',
                       'ticket_template_name',
                       'application_name',
                       'application_date',
                       'parent_contract_id',
                       'lifetime_start',
                       'lifetime_end',
                       'created_at',
                       'updated_at',
                       'deleted_at',
                       'deleted',
                       'expansion_key1',
                       'expansion_key2',
                       'expansion_key3',
                       'expansion_key4',
                       'expansion_key5',
                       'expansion_text']
            v1shell.do_contract_create(self.gc, args)

            mocked_func.assert_called_once_with(requestparam)
            utils.print_list.assert_called_once_with([contract_print_data],
                                                     columns)

    def test_do_contract_create_empty_args(self):
        """Test create command by empty args."""
        args = None

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_contract_create,
                          self.gc,
                          args)

    def test_contract_update(self):
        input_dict = {
            'contract_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
            'project_id': 'project_id_101',
            'region_id': 'region_id_101',
            'project_name': 'project_name_101',
            'catalog_id': 'catalog_id_101',
            'catalog_name': 'catalog_name_101',
            'num': 101,
            'parent_ticket_template_id': 'parent_ticket_template_id_101',
            'ticket_template_id': 'ticket_template_id_101',
            'parent_ticket_template_name': 'parent_ticket_template_name_101',
            'parent_application_kinds_name': 'parent_app_kinds_name_101',
            'application_kinds_name': 'application_kinds_name_101',
            'cancel_application_id': 'cancel_application_id_101',
            'application_id': 'application_id_101',
            'ticket_template_name': 'ticket_template_name_101',
            'application_name': 'application_name_101',
            'application_date': '2015-6-1',
            'parent_contract_id': 'parent_contract_id_101',
            'lifetime_start': '2015-7-1',
            'lifetime_end': '2015-8-1',
            'expansion_key1': 'expansion_key1',
            'expansion_key2': 'expansion_key2',
            'expansion_key3': 'expansion_key3',
            'expansion_key4': 'expansion_key4',
            'expansion_key5': 'expansion_key5',
            'expansion_text': 'expansion_text'
        }
        requestparam = {
            'project_id': 'project_id_101',
            'region_id': 'region_id_101',
            'project_name': 'project_name_101',
            'catalog_id': 'catalog_id_101',
            'catalog_name': 'catalog_name_101',
            'num': 101,
            'parent_ticket_template_id': 'parent_ticket_template_id_101',
            'ticket_template_id': 'ticket_template_id_101',
            'parent_ticket_template_name': 'parent_ticket_template_name_101',
            'parent_application_kinds_name': 'parent_app_kinds_name_101',
            'application_kinds_name': 'application_kinds_name_101',
            'cancel_application_id': 'cancel_application_id_101',
            'application_id': 'application_id_101',
            'ticket_template_name': 'ticket_template_name_101',
            'application_name': 'application_name_101',
            'application_date': '2015-6-1',
            'parent_contract_id': 'parent_contract_id_101',
            'lifetime_start': '2015-7-1',
            'lifetime_end': '2015-8-1',
            'expansions': {
                'expansion_key1': 'expansion_key1',
                'expansion_key2': 'expansion_key2',
                'expansion_key3': 'expansion_key3',
                'expansion_key4': 'expansion_key4',
                'expansion_key5': 'expansion_key5',
            },
            'expansions_text': {
                'expansion_text': 'expansion_text'
            }
        }
        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.contracts, 'update') as mocked_func:
            mocked_func.return_value = Contract(self,
                                                contract_return_data,
                                                loaded=True)
            v1shell.do_contract_update(self.gc, args)
            columns = v1shell._print_contract_columns
            mocked_func.assert_called_once_with(
                'ea0a4146-fd07-414b-aa5e-dedbeef00001',
                requestparam)
            utils.print_list.assert_called_once_with([contract_print_data],
                                                     columns)

    def test_contract_update_with_contract_id_only(self):
        input_dict = {
            'contract_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00002',
        }
        requestparam = {}
        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.contracts, 'update') as mocked_func:
            v1shell.do_contract_update(self.gc, args)
            mocked_func.assert_called_once_with(
                'ea0a4146-fd07-414b-aa5e-dedbeef00002',
                requestparam)

    def test_contract_update_invalid_no_contract_id(self):
        input_dict = {
            'project_id': 'project_id_101',
            'region_id': 'region_id_101',
            'project_name': 'project_name_101',
            'catalog_id': 'catalog_id_101',
            'catalog_name': 'catalog_name_101',
            'num': 101,
            'parent_ticket_template_id': 'parent_ticket_template_id_101',
            'ticket_template_id': 'ticket_template_id_101',
            'parent_ticket_template_name': 'parent_ticket_template_name_101',
            'parent_application_kinds_name': 'parent_app_kinds_name_101',
            'application_kinds_name': 'application_kinds_name_101',
            'cancel_application_id': 'cancel_application_id_101',
            'application_id': 'application_id_101',
            'ticket_template_name': 'ticket_template_name_101',
            'application_name': 'application_name_101',
            'application_date': '2015-6-1',
            'parent_contract_id': 'parent_contract_id_101',
            'lifetime_start': '20-7-1',
            'lifetime_end': '2015-8-1',
            'expansion_key1': 'expansion_key1',
            'expansion_key2': 'expansion_key2',
            'expansion_key3': 'expansion_key3',
            'expansion_key4': 'expansion_key4',
            'expansion_key5': 'expansion_key5',
            'expansion_text': 'expansion_text'
        }

        args = self._make_args(input_dict)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_contract_update,
                          self.gc,
                          args)

    def test_contract_update_empty_args(self):
        args = None

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_contract_update,
                          self.gc,
                          args)

    def test_do_contract_get(self):
        """Test get command."""
        input = {'contract_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00101'}
        args = self._make_args(input)

        columns = \
            ['contract_id',
             'region_id',
             'project_id',
             'project_name',
             'catalog_id',
             'catalog_name',
             'num',
             'parent_ticket_template_id',
             'ticket_template_id',
             'parent_ticket_template_name',
             'parent_application_kinds_name',
             'application_kinds_name',
             'cancel_application_id',
             'application_id',
             'ticket_template_name',
             'application_name',
             'application_date',
             'parent_contract_id',
             'lifetime_start',
             'lifetime_end',
             'created_at',
             'updated_at',
             'deleted_at',
             'deleted',
             'expansion_key1',
             'expansion_key2',
             'expansion_key3',
             'expansion_key4',
             'expansion_key5',
             'expansion_text']

        with mock.patch.object(self.gc.contracts, 'get') as mocked_func:
            mocked_func.return_value = Contract(self,
                                                contract_return_data,
                                                loaded=True)

            v1shell.do_contract_get(self.gc, args)

            mocked_func.assert_called_once_with(
                'ea0a4146-fd07-414b-aa5e-dedbeef00101')
            utils.print_list([contract_print_data], columns)

    def test_contract_delete(self):
        contract_id = 'ea0a4146-fd07-414b-aa5e-dedbeef00101'
        input_dict = {'contract_id': contract_id}
        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.contracts, 'delete') as mocked_func:
            mocked_func.return_value = {}

            v1shell.do_contract_delete(self.gc, args)

            mocked_func.assert_called_once_with(contract_id)

    def test_contract_delete_none_args(self):
        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_contract_delete,
                          self.gc,
                          None)

    def test_contract_delete_empty_args(self):
        input_dict = {}
        args = self._make_args(input_dict)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_contract_delete,
                          self.gc,
                          args)

    def test_do_contract_list(self):
        """Test list command with no params."""
        args = {}
        with mock.patch.object(self.gc.contracts, 'list') as mocked_func:
            mocked_func.return_value = [Contract(self,
                                                 contract_return_data,
                                                 loaded=True)]
            columns = \
                ['contract_id',
                 'region_id',
                 'project_id',
                 'project_name',
                 'catalog_id',
                 'catalog_name',
                 'num',
                 'parent_ticket_template_id',
                 'ticket_template_id',
                 'parent_ticket_template_name',
                 'parent_application_kinds_name',
                 'application_kinds_name',
                 'cancel_application_id',
                 'application_id',
                 'ticket_template_name',
                 'application_name',
                 'application_date',
                 'parent_contract_id',
                 'lifetime_start',
                 'lifetime_end',
                 'created_at',
                 'updated_at',
                 'deleted_at',
                 'deleted',
                 'expansion_key1',
                 'expansion_key2',
                 'expansion_key3',
                 'expansion_key4',
                 'expansion_key5',
                 'expansion_text']

            v1shell.do_contract_list(self.gc, args)

            mocked_func.assert_called_once_with({})
            utils.print_list.assert_called_once_with([contract_print_data],
                                                     columns)

    def test_do_contract_list_all_params(self):
        """Test list command with all parameters."""
        input_dict = {'application_id': 'pplication_id_10',
                      'catalog_name': 'atalog_name_10',
                      'force_show_deleted': 'false',
                      'lifetime': '2015-08-05',
                      'limit': 1,
                      'marker': 'ea0a4146-fd07-414b-aa5e-dedbeef00101',
                      'project_id': 'project_id_102',
                      'project_name': 'roject_name_10',
                      'region_id': 'region_id_102',
                      'sort_dir': 'asc,desc',
                      'sort_key': 'contract_name,lifetime_strat'}

        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.contracts, 'list') as mocked_func:
            mocked_func.return_value = [Contract(self,
                                                 contract_return_data,
                                                 loaded=True)]
            columns = \
                ['contract_id',
                 'region_id',
                 'project_id',
                 'project_name',
                 'catalog_id',
                 'catalog_name',
                 'num',
                 'parent_ticket_template_id',
                 'ticket_template_id',
                 'parent_ticket_template_name',
                 'parent_application_kinds_name',
                 'application_kinds_name',
                 'cancel_application_id',
                 'application_id',
                 'ticket_template_name',
                 'application_name',
                 'application_date',
                 'parent_contract_id',
                 'lifetime_start',
                 'lifetime_end',
                 'created_at',
                 'updated_at',
                 'deleted_at',
                 'deleted',
                 'expansion_key1',
                 'expansion_key2',
                 'expansion_key3',
                 'expansion_key4',
                 'expansion_key5',
                 'expansion_text']

            v1shell.do_contract_list(self.gc, args)

            called_args, kwargs = mocked_func.call_args

            self.assertEqual(sorted(input_dict.items()),
                             sorted(called_args[0].items()))
            utils.print_list.assert_called_once_with([contract_print_data],
                                                     columns)

    def test_do_goods_create(self):
        """Test create command."""
        input = {'goods_name': 'testgoods'}
        args = self._make_args(input)
        with mock.patch.object(self.gc.goods, 'create') as mocked_func:
            mocked_func.return_value = Goods(self,
                                             goods_return_data,
                                             loaded=True)
            columns = v1shell._print_goods_columns
            v1shell.do_goods_create(self.gc, args)

            mocked_func.assert_called_once_with(input)
            utils.print_list.assert_called_once_with([goods_print_data],
                                                     columns)

    def test_goods_update(self):
        input_dict = {
            'goods_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
            'region_id': 'region_id_101',
            'goods_name': 'goods_name_101',
            'expansion_key1': 'expansion_key1',
            'expansion_key2': 'expansion_key2',
            'expansion_key3': 'expansion_key3',
            'expansion_key4': 'expansion_key4',
            'expansion_key5': 'expansion_key5',
            'expansion_text': 'expansion_text'
        }
        requestparam = {
            'region_id': 'region_id_101',
            'goods_name': 'goods_name_101',
            'expansions': {
                'expansion_key1': 'expansion_key1',
                'expansion_key2': 'expansion_key2',
                'expansion_key3': 'expansion_key3',
                'expansion_key4': 'expansion_key4',
                'expansion_key5': 'expansion_key5',
            },
            'expansions_text': {
                'expansion_text': 'expansion_text'
            }
        }
        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.goods, 'update') as mocked_func:
            mocked_func.return_value = Goods(self,
                                             goods_return_data,
                                             loaded=True)
            columns = v1shell._print_goods_columns
            v1shell.do_goods_update(self.gc, args)
            mocked_func.assert_called_once_with(
                'ea0a4146-fd07-414b-aa5e-dedbeef00001',
                requestparam)
            utils.print_list.assert_called_once_with([goods_print_data],
                                                     columns)

    def test_goods_update_with_goods_id_only(self):
        input_dict = {
            'goods_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
        }
        requestparam = {}
        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.goods, 'update') as mocked_func:
            v1shell.do_goods_update(self.gc, args)
            mocked_func.assert_called_once_with(
                'ea0a4146-fd07-414b-aa5e-dedbeef00001',
                requestparam)

    def test_goods_update_invalid_no_goods_id(self):
        input_dict = {
            'region_id': 'region_id_101',
            'goods_name': 'goods_name_101',
            'expansion_key1': 'expansion_key1',
            'expansion_key2': 'expansion_key2',
            'expansion_key3': 'expansion_key3',
            'expansion_key4': 'expansion_key4',
            'expansion_key5': 'expansion_key5',
            'expansion_text': 'expansion_text'
        }

        args = self._make_args(input_dict)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_goods_update,
                          self.gc,
                          args)

    def test_goods_update_none_args(self):
        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_goods_update,
                          self.gc,
                          None)

    def test_do_goods_list(self):
        """Test 'List Search of price'
        Test the operation of the parameter without.
        """
        args = {}
        with mock.patch.object(self.gc.goods, 'list') as mocked_func:
            mocked_func.return_value = [Goods(self,
                                              goods_return_data,
                                              loaded=True)]
            columns = \
                ['goods_id',
                 'region_id',
                 'goods_name',
                 'created_at',
                 'updated_at',
                 'deleted_at',
                 'deleted',
                 'expansion_key1',
                 'expansion_key2',
                 'expansion_key3',
                 'expansion_key4',
                 'expansion_key5',
                 'expansion_text']

            v1shell.do_goods_list(self.gc, args)

            called_args, kwargs = mocked_func.call_args

            mocked_func.assert_called_once_with({})
            utils.print_list.assert_called_once_with([goods_print_data],
                                                     columns)

    def test_do_goods_list_all_param(self):
        """Test 'List Search of goods'
        Test with all parameters.
        """
        input = {'region_id': '1',
                 'limit': 1,
                 'marker': 'a',
                 'sort_key': 'region_id,goods_id',
                 'sort_dir': 'desc,asc',
                 'force_show_deleted': 'True'}

        args = self._make_args(input)
        with mock.patch.object(self.gc.goods, 'list') as mocked_func:
            mocked_func.return_value = [Goods(self,
                                              goods_return_data,
                                              loaded=True)]
            columns = \
                ['goods_id',
                 'region_id',
                 'goods_name',
                 'created_at',
                 'updated_at',
                 'deleted_at',
                 'deleted',
                 'expansion_key1',
                 'expansion_key2',
                 'expansion_key3',
                 'expansion_key4',
                 'expansion_key5',
                 'expansion_text']

            v1shell.do_goods_list(self.gc, args)

            called_args, kwargs = mocked_func.call_args

            self.assertEqual(sorted({'region_id': '1',
                                     'limit': 1,
                                     'marker': 'a',
                                     'sort_key': 'region_id,goods_id',
                                     'sort_dir': 'desc,asc',
                                     'force_show_deleted': 'True'}.items()),
                             sorted(called_args[0].items()))
            utils.print_list.assert_called_once_with([goods_print_data],
                                                     columns)

    def test_goods_get(self):
        """Test 'Get of goods'
        Test to get the data of goods_id = 1.
        """
        input = {'goods_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00101'}
        args = self._make_args(input)

        with mock.patch.object(self.gc.goods, 'get') as mocked_func:
            mocked_func.return_value = Goods(self,
                                             goods_return_data,
                                             loaded=True)
            columns = v1shell._print_goods_columns
            v1shell.do_goods_get(self.gc, args)

            mocked_func.assert_called_once_with(input['goods_id'])
            utils.print_list.assert_called_once_with([goods_print_data],
                                                     columns)

    def test_do_goods_delete(self):
        goods_id = 'ea0a4146-fd07-414b-aa5e-dedbeef00001'
        input_dict = {'goods_id': goods_id}
        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.goods, 'delete') as mocked_func:
            mocked_func.return_value = {}

            v1shell.do_goods_delete(self.gc, args)

            mocked_func.assert_called_once_with(goods_id)

    def test_do_catalog_create(self):
        """Test create command."""
        input = {'catalog_name': 'test_catalog'}
        args = self._make_args(input)
        with mock.patch.object(self.gc.catalogs, 'create') as mocked_func:
            mocked_func.return_value = Catalog(self,
                                               catalog_return_data,
                                               loaded=True)
            columns = v1shell._print_catalog_columns
            v1shell.do_catalog_create(self.gc, args)

            mocked_func.assert_called_once_with(input)
            utils.print_list.assert_called_once_with([catalog_print_data],
                                                     columns)

    def test_catalog_update(self):
        input_dict = {
            'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
            'region_id': 'region_id_101',
            'catalog_name': 'catalog_name_101',
            'lifetime_start': '2015-7-1',
            'lifetime_end': '2015-8-1',
            'expansion_key1': 'expansion_key1',
            'expansion_key2': 'expansion_key2',
            'expansion_key3': 'expansion_key3',
            'expansion_key4': 'expansion_key4',
            'expansion_key5': 'expansion_key5',
            'expansion_text': 'expansion_text'
        }
        requestparam = {
            'region_id': 'region_id_101',
            'catalog_name': 'catalog_name_101',
            'lifetime_start': '2015-7-1',
            'lifetime_end': '2015-8-1',
            'expansions': {
                'expansion_key1': 'expansion_key1',
                'expansion_key2': 'expansion_key2',
                'expansion_key3': 'expansion_key3',
                'expansion_key4': 'expansion_key4',
                'expansion_key5': 'expansion_key5',
            },
            'expansions_text': {
                'expansion_text': 'expansion_text'
            }
        }
        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.catalogs, 'update') as mocked_func:
            mocked_func.return_value = Catalog(self,
                                               catalog_return_data,
                                               loaded=True)
            columns = v1shell._print_catalog_columns
            v1shell.do_catalog_update(self.gc, args)
            mocked_func.assert_called_once_with(
                'ea0a4146-fd07-414b-aa5e-dedbeef00001',
                requestparam)
            utils.print_list.assert_called_once_with([catalog_print_data],
                                                     columns)

    def test_catalog_update_with_catalog_id_only(self):
        input_dict = {
            'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00002',
        }
        requestparam = {}
        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.catalogs, 'update') as mocked_func:
            v1shell.do_catalog_update(self.gc, args)
            mocked_func.assert_called_once_with(
                'ea0a4146-fd07-414b-aa5e-dedbeef00002',
                requestparam)

    def test_catalog_update_invalid_no_catalog_id(self):
        input_dict = {
            'region_id': 'region_id_101',
            'catalog_name': 'catalog_name_101',
            'lifetime_start': '20-7-1',
            'lifetime_end': '2015-8-1',
            'expansion_key1': 'expansion_key1',
            'expansion_key2': 'expansion_key2',
            'expansion_key3': 'expansion_key3',
            'expansion_key4': 'expansion_key4',
            'expansion_key5': 'expansion_key5',
            'expansion_text': 'expansion_text'
        }

        args = self._make_args(input_dict)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_catalog_update,
                          self.gc,
                          args)

    def test_catalog_update_empty_args(self):
        args = None

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_catalog_update,
                          self.gc,
                          args)

    def test_do_catalog_get(self):
        """Test get command."""
        input_dict = {'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00101'}
        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.catalogs, 'get') as mocked_func:
            mocked_func.return_value = Catalog(self,
                                               catalog_return_data,
                                               loaded=True)
            columns = v1shell._print_catalog_columns
            v1shell.do_catalog_get(self.gc, args)
            mocked_func.assert_called_once_with(input_dict['catalog_id'])
            utils.print_list.assert_called_once_with([catalog_print_data],
                                                     columns)

    def test_do_catalog_get_none_data(self):
        """Test get command."""
        input_dict = {'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00103'}
        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.catalogs, 'get') as mocked_func:
            mocked_func.return_value = None

            v1shell.do_catalog_get(self.gc, args)

            mocked_func.assert_called_once_with(input_dict['catalog_id'])

    def test_do_catalog_get_empty_args(self):
        """Test catalog get command by empty args."""
        input_dict = {}
        args = self._make_args(input_dict)

        self.assertRaises(exceptions.AttributeError,
                          v1shell.do_catalog_get,
                          self.gc,
                          args)

    def test_catalog_list(self):
        """Test 'List Search of catalog'
        Test the operation of the parameter without.
        """
        input_dict = {}
        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.catalogs, 'list') as mocked_func:
            mocked_func.return_value = [Catalog(self,
                                                catalog_return_data,
                                                loaded=True)]
            columns = \
                ['catalog_id',
                 'region_id',
                 'catalog_name',
                 'lifetime_start',
                 'lifetime_end',
                 'created_at',
                 'updated_at',
                 'deleted_at',
                 'deleted',
                 'expansion_key1',
                 'expansion_key2',
                 'expansion_key3',
                 'expansion_key4',
                 'expansion_key5',
                 'expansion_text']

            v1shell.do_catalog_list(self.gc, args)

            called_args, kwargs = mocked_func.call_args

            mocked_func.assert_called_once_with({})
            utils.print_list.assert_called_once_with([catalog_print_data],
                                                     columns)

    def test_catalog_list_all_param(self):
        """Test 'List Search of catalog'
        Test with all parameters.
        """
        input_dict = {'catalog_id': '1',
                      'region_id': '1',
                      'catalog_name': 'catalog_test',
                      'lifetime': '2015-07-01',
                      'limit': 1,
                      'marker': 'a',
                      'sort_key': 'catalog_id,lifetime_start',
                      'sort_dir': 'desc,asc'}

        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.catalogs, 'list') as mocked_func:
            mocked_func.return_value = [Catalog(self,
                                                catalog_return_data,
                                                loaded=True)]
            columns = \
                ['catalog_id',
                 'region_id',
                 'catalog_name',
                 'lifetime_start',
                 'lifetime_end',
                 'created_at',
                 'updated_at',
                 'deleted_at',
                 'deleted',
                 'expansion_key1',
                 'expansion_key2',
                 'expansion_key3',
                 'expansion_key4',
                 'expansion_key5',
                 'expansion_text']

            v1shell.do_catalog_list(self.gc, args)

            called_args, kwargs = mocked_func.call_args

            self.assertEqual(sorted({'catalog_id': '1',
                                     'region_id': '1',
                                     'catalog_name': 'catalog_test',
                                     'lifetime': '2015-07-01',
                                     'limit': 1,
                                     'marker': 'a',
                                     'sort_key': 'catalog_id,lifetime_start',
                                     'sort_dir': 'desc,asc'}.items()),
                             sorted(called_args[0].items()))
            utils.print_list.assert_called_once_with([catalog_print_data],
                                                     columns)

    def test_do_catalog_delete(self):
        catalog_id = 'ea0a4146-fd07-414b-aa5e-dedbeef00101'
        input_dict = {'catalog_id': catalog_id}
        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.catalogs, 'delete') as mocked_func:
            mocked_func.return_value = {}

            v1shell.do_catalog_delete(self.gc, args)

            mocked_func.assert_called_once_with(catalog_id)

    def test_do_catalog_contents_create(self):
        """Test create command."""
        input = {'catalog_id': '1',
                 'goods_id': 'goods_001',
                 'goods_num': '2'}
        args = self._make_args(input)
        with mock.patch.object(self.gc.catalog_contents,
                               'create') as mocked_func:
            mocked_func.return_value = \
                CatalogContents(self,
                                catalog_contents_return_data,
                                loaded=True)
            columns = v1shell._print_catalog_contents_columns
            v1shell.do_catalog_contents_create(self.gc, args)

            check_input = {'goods_id': 'goods_001',
                           'goods_num': 2}

            mocked_func.assert_called_once_with('1', check_input)
            utils.print_list.assert_called_once_with(
                [catalog_contents_print_data],
                columns)

    def test_do_catalog_contents_list(self):
        """Test list command with no params."""
        input_dict = {'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00101'}
        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.catalog_contents, 'list') \
                as mocked_func:

            mocked_func.return_value = \
                [CatalogContents(self,
                                 catalog_contents_return_data,
                                 loaded=True)]
            columns = \
                ['catalog_id',
                 'seq_no',
                 'goods_id',
                 'goods_num',
                 'created_at',
                 'updated_at',
                 'deleted_at',
                 'deleted',
                 'expansion_key1',
                 'expansion_key2',
                 'expansion_key3',
                 'expansion_key4',
                 'expansion_key5',
                 'expansion_text']

            v1shell.do_catalog_contents_list(self.gc, args)

            mocked_func.assert_called_once_with(
                'ea0a4146-fd07-414b-aa5e-dedbeef00101',
                {})
            utils.print_list.assert_called_once_with(
                [catalog_contents_print_data],
                columns)

    def test_do_catalog_contents_list_all_params(self):
        """Test list command with all parameters."""
        input_dict = {'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00101',
                      'force_show_deleted': 'false',
                      'limit': 1,
                      'marker': '101',
                      'sort_dir': 'asc,desc',
                      'sort_key': 'goods_id,goods_num'}

        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.catalog_contents, 'list') \
                as mocked_func:

            mocked_func.return_value = \
                [CatalogContents(self,
                                 catalog_contents_return_data,
                                 loaded=True)]
            columns = \
                ['catalog_id',
                 'seq_no',
                 'goods_id',
                 'goods_num',
                 'created_at',
                 'updated_at',
                 'deleted_at',
                 'deleted',
                 'expansion_key1',
                 'expansion_key2',
                 'expansion_key3',
                 'expansion_key4',
                 'expansion_key5',
                 'expansion_text']

            v1shell.do_catalog_contents_list(self.gc, args)

            called_args, kwargs = mocked_func.call_args

            self.assertEqual(called_args[0], input_dict['catalog_id'])
            self.assertEqual(
                sorted({'force_show_deleted': 'false',
                        'limit': 1,
                        'marker': '101',
                        'sort_dir': 'asc,desc',
                        'sort_key': 'goods_id,goods_num'}.items()),
                sorted(called_args[1].items()))
            utils.print_list.assert_called_once_with(
                [catalog_contents_print_data],
                columns)

    def test_do_catalog_contents_get(self):
        """Test 'Get of catalog contents'
        """
        input = {'catalog_id': '1', 'seq_no': '1'}
        args = self._make_args(input)

        with mock.patch.object(self.gc.catalog_contents, 'get') as mocked_func:
            mocked_func.return_value = \
                CatalogContents(self,
                                catalog_contents_return_data,
                                loaded=True)
            columns = v1shell._print_catalog_contents_columns
            v1shell.do_catalog_contents_get(self.gc, args)

            mocked_func.assert_called_once_with('1', '1')
            utils.print_list.assert_called_once_with(
                [catalog_contents_print_data],
                columns)

    def test_catalog_contents_update(self):
        input_dict = {
            'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00101',
            'seq_no': '1',
            'goods_id': 'goods_id_100',
            'goods_num': '1',
            'expansion_key1': 'expansion_key1',
            'expansion_key2': 'expansion_key2',
            'expansion_key3': 'expansion_key3',
            'expansion_key4': 'expansion_key4',
            'expansion_key5': 'expansion_key5',
            'expansion_text': 'expansion_text'
        }
        requestparam = {
            'goods_id': 'goods_id_100',
            'goods_num': 1,
            'expansions': {
                'expansion_key1': 'expansion_key1',
                'expansion_key2': 'expansion_key2',
                'expansion_key3': 'expansion_key3',
                'expansion_key4': 'expansion_key4',
                'expansion_key5': 'expansion_key5',
            },
            'expansions_text': {
                'expansion_text': 'expansion_text'
            }
        }
        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.catalog_contents,
                               'update')as mocked_func:
            mocked_func.return_value = \
                CatalogContents(self,
                                catalog_contents_return_data,
                                loaded=True)
            columns = v1shell._print_catalog_contents_columns
            v1shell.do_catalog_contents_update(self.gc, args)
            mocked_func.assert_called_once_with(
                'ea0a4146-fd07-414b-aa5e-dedbeef00101',
                '1',
                requestparam)
            utils.print_list.assert_called_once_with(
                [catalog_contents_print_data],
                columns)

    def test_catalog_contents_update_with_catalog_id_and_seq_no(self):
        input_dict = {
            'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00101',
            'seq_no': '1',
        }
        requestparam = {}
        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.catalog_contents,
                               'update') as mocked_func:
            v1shell.do_catalog_contents_update(self.gc, args)
            mocked_func.assert_called_once_with(
                'ea0a4146-fd07-414b-aa5e-dedbeef00101',
                '1',
                requestparam)

    def test_catalog_contents_update_invalid_no_catalog_id(self):
        input_dict = {
            'seq_no': '1',
            'goods_id': 'goods_id_100',
            'goods_num': '1',
            'expansion_key1': 'expansion_key1',
            'expansion_key2': 'expansion_key2',
            'expansion_key3': 'expansion_key3',
            'expansion_key4': 'expansion_key4',
            'expansion_key5': 'expansion_key5',
            'expansion_text': 'expansion_text'
        }

        args = self._make_args(input_dict)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_catalog_contents_update,
                          self.gc,
                          args)

    def test_catalog_contents_update_invalid_no_seq_no(self):
        input_dict = {
            'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00101',
            'goods_id': 'goods_id_100',
            'goods_num': '1',
            'expansion_key1': 'expansion_key1',
            'expansion_key2': 'expansion_key2',
            'expansion_key3': 'expansion_key3',
            'expansion_key4': 'expansion_key4',
            'expansion_key5': 'expansion_key5',
            'expansion_text': 'expansion_text'
        }

        args = self._make_args(input_dict)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_catalog_contents_update,
                          self.gc,
                          args)

    def test_catalog_contents_update_none_args(self):
        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_catalog_contents_update,
                          self.gc,
                          None)

    def test_do_catalog_contents_delete(self):
        catalog_id = 'ea0a4146-fd07-414b-aa5e-dedbeef00101'
        seq_no = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'
        input_dict = {'catalog_id': catalog_id,
                      'seq_no': seq_no}
        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.catalog_contents,
                               'delete') as mocked_func:
            mocked_func.return_value = {}

            v1shell.do_catalog_contents_delete(self.gc, args)

            mocked_func.assert_called_once_with(catalog_id, seq_no)

    def test_do_catalog_contents_delete_invalid_no_catalog_id(self):
        seq_no = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'
        input_dict = {'seq_no': seq_no}
        args = self._make_args(input_dict)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_catalog_contents_delete,
                          self.gc,
                          args)

    def test_do_catalog_contents_delete_invalid_no_seq_no(self):
        catalog_id = 'ea0a4146-fd07-414b-aa5e-dedbeef00101'
        input_dict = {'catalog_id': catalog_id}
        args = self._make_args(input_dict)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_catalog_contents_delete,
                          self.gc,
                          args)

    def test_do_catalog_contents_delete_none_args(self):
        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_catalog_contents_delete,
                          self.gc,
                          None)

    def test_catalog_scope_list(self):
        input_dict = {}
        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.catalog_scope, 'list') as mocked_func:
            mocked_func.return_value = [CatalogScope(self,
                                                     catalog_scope_return_data,
                                                     loaded=True)]
            columns = v1shell._print_catalog_scope_columns
            v1shell.do_catalog_scope_list(self.gc, args)

            mocked_func.assert_called_once_with({})
            utils.print_list.assert_called_once_with(
                [catalog_scope_print_data],
                columns)

    def test_catalog_scope_list_all_param(self):
        input_dict = {'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
                      'scope': 'bdb8f50f82da4370813e6ea797b1fb101',
                      'lifetime': '2016-12-31T23:59:59.999999',
                      'limit': 1,
                      'marker': 'id0a4146-fd07-414b-aa5e-dedbeef00002',
                      'sort_key': 'catalog_id,scope',
                      'sort_dir': 'desc,asc',
                      'force_show_deleted': 'False'}

        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.catalog_scope, 'list') as mocked_func:
            mocked_func.return_value = [CatalogScope(self,
                                                     catalog_scope_return_data,
                                                     loaded=True)]
            columns = v1shell._print_catalog_scope_columns
            v1shell.do_catalog_scope_list(self.gc, args)

            called_args, kwargs = mocked_func.call_args
            self.assertEqual(
                sorted(
                    {'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
                     'scope': 'bdb8f50f82da4370813e6ea797b1fb101',
                     'lifetime': '2016-12-31T23:59:59.999999',
                     'limit': 1,
                     'marker': 'id0a4146-fd07-414b-aa5e-dedbeef00002',
                     'sort_key': 'catalog_id,scope',
                     'sort_dir': 'desc,asc',
                     'force_show_deleted': 'False'}.items()),
                sorted(called_args[0].items()))
            utils.print_list.assert_called_once_with(
                [catalog_scope_print_data],
                columns)

    def test_catalog_scope_create(self):
        input = {
            'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
            'scope': 'project_101',
            'lifetime_start': '2015-12-31T23:59:59.999999',
            'lifetime_end': '9999-12-31T23:59:59.999999',
            'expansion_key1': 'expansion_key1',
            'expansion_key2': 'expansion_key2',
            'expansion_key3': 'expansion_key3',
            'expansion_key4': 'expansion_key4',
            'expansion_key5': 'expansion_key5',
            'expansion_text': 'expansion_text'}
        args = self._make_args(input)
        with mock.patch.object(self.gc.catalog_scope, 'create') as mocked_func:
            mocked_func.return_value = CatalogScope(self,
                                                    catalog_scope_return_data,
                                                    loaded=True)
            columns = v1shell._print_catalog_scope_columns
            v1shell.do_catalog_scope_create(self.gc, args)

            check_input = {
                'lifetime_start': '2015-12-31T23:59:59.999999',
                'lifetime_end': '9999-12-31T23:59:59.999999',
                'expansions': {
                    'expansion_key1': 'expansion_key1',
                    'expansion_key2': 'expansion_key2',
                    'expansion_key3': 'expansion_key3',
                    'expansion_key4': 'expansion_key4',
                    'expansion_key5': 'expansion_key5'
                },
                'expansions_text': {
                    'expansion_text': 'expansion_text'
                }
            }
            mocked_func.assert_called_once_with(
                'ea0a4146-fd07-414b-aa5e-dedbeef00001',
                'project_101',
                check_input)
            utils.print_list.assert_called_once_with(
                [catalog_scope_print_data],
                columns)

    def test_catalog_scope_create_invalid_no_catalog_id(self):
        input = {'scope': 'project_101'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_catalog_scope_create,
                          self.gc,
                          args)

    def test_catalog_scope_create_invalid_no_scope(self):
        input = {'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_catalog_scope_create,
                          self.gc,
                          args)

    def test_catalog_scope_create_invalid_no_args(self):
        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_catalog_scope_create,
                          self.gc,
                          None)

    def test_catalog_scope_get(self):
        catalog_scope_id = 'id0a4146-fd07-414b-aa5e-dedbeef00001'
        input = {'id': catalog_scope_id}
        args = self._make_args(input)

        with mock.patch.object(self.gc.catalog_scope, 'get') as mocked_func:
            mocked_func.return_value = \
                CatalogScope(self,
                             catalog_scope_return_data,
                             loaded=True)
            columns = v1shell._print_catalog_scope_columns
            v1shell.do_catalog_scope_get(self.gc, args)

            mocked_func.assert_called_once_with(catalog_scope_id)
            utils.print_list.assert_called_once_with(
                [catalog_scope_print_data],
                columns)

    def test_catalog_scope_update(self):
        input = {
            'id': 'id0a4146-fd07-414b-aa5e-dedbeef00001',
            'lifetime_start': '2015-12-31T23:59:59.999999',
            'lifetime_end': '9999-12-31T23:59:59.999999',
            'expansion_key1': 'expansion_key1',
            'expansion_key2': 'expansion_key2',
            'expansion_key3': 'expansion_key3',
            'expansion_key4': 'expansion_key4',
            'expansion_key5': 'expansion_key5',
            'expansion_text': 'expansion_text'}
        args = self._make_args(input)
        with mock.patch.object(self.gc.catalog_scope, 'update') as mocked_func:
            mocked_func.return_value = CatalogScope(self,
                                                    catalog_scope_return_data,
                                                    loaded=True)
            columns = v1shell._print_catalog_scope_columns
            v1shell.do_catalog_scope_update(self.gc, args)

            check_input = {
                'lifetime_start': '2015-12-31T23:59:59.999999',
                'lifetime_end': '9999-12-31T23:59:59.999999',
                'expansions': {
                    'expansion_key1': 'expansion_key1',
                    'expansion_key2': 'expansion_key2',
                    'expansion_key3': 'expansion_key3',
                    'expansion_key4': 'expansion_key4',
                    'expansion_key5': 'expansion_key5'
                },
                'expansions_text': {
                    'expansion_text': 'expansion_text'
                }
            }
            mocked_func.assert_called_once_with(
                'id0a4146-fd07-414b-aa5e-dedbeef00001',
                check_input)
            utils.print_list.assert_called_once_with(
                [catalog_scope_print_data],
                columns)

    def test_catalog_scope_update_with_no_data(self):
        input = {'id': 'id0a4146-fd07-414b-aa5e-dedbeef00001'}
        args = self._make_args(input)
        with mock.patch.object(self.gc.catalog_scope, 'update') as mocked_func:
            mocked_func.return_value = CatalogScope(self,
                                                    catalog_scope_return_data,
                                                    loaded=True)
            columns = v1shell._print_catalog_scope_columns
            v1shell.do_catalog_scope_update(self.gc, args)

            mocked_func.assert_called_once_with(
                'id0a4146-fd07-414b-aa5e-dedbeef00001',
                {})
            utils.print_list.assert_called_once_with(
                [catalog_scope_print_data],
                columns)

    def test_catalog_scope_update_invalid_no_id(self):
        input = {'lifetime_start': '2015-12-31T23:59:59.999999'}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_catalog_scope_update,
                          self.gc,
                          args)

    def test_catalog_scope_update_invalid_no_args(self):
        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_catalog_scope_update,
                          self.gc,
                          None)

    def test_catalog_scope_delete(self):
        catalog_scope_id = 'id0a4146-fd07-414b-aa5e-dedbeef00001'
        input = {'id': catalog_scope_id}
        args = self._make_args(input)
        with mock.patch.object(self.gc.catalog_scope,
                               'delete') as mocked_func:
            mocked_func.return_value = {}

            v1shell.do_catalog_scope_delete(self.gc, args)

            mocked_func.assert_called_once_with(catalog_scope_id)

    def test_catalog_scope_delete_invalid_no_id(self):
        catalog_scope_id = 'id0a4146-fd07-414b-aa5e-dedbeef00001'
        input = {'catalog_id': catalog_scope_id}
        args = self._make_args(input)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_catalog_scope_delete,
                          self.gc,
                          args)

    def test_catalog_scope_delete_none_args(self):
        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_catalog_scope_delete,
                          self.gc,
                          None)

    def test_valid_catalog_list(self):
        input_dict = {'lifetime': '2016-12-31T23:59:59.999999'}
        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.valid_catalog, 'list') as mocked_func:
            mocked_func.return_value = \
                [ValidCatalog(self,
                              valid_catalog_return_data,
                              loaded=True)]
            columns = v1shell._print_valid_catalog_columns
            v1shell.do_valid_catalog_list(self.gc, args)

            mocked_func.assert_called_once_with(input_dict)
            utils.print_list.assert_called_once_with(
                [valid_catalog_return_data],
                columns)

    def test_valid_catalog_list_all_param(self):
        input_dict = {
            'lifetime': '2016-12-31T23:59:59.999999',
            'scope': 'project_101',
            'catalog_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
            'catalog_name': 'CATALOG-A-102',
            'refine_flg': 'True',
            'limit': '1',
            'catalog_marker': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
            'catalog_scope_marker': 'id0a4146-fd07-414b-aa5e-dedbeef00002',
            'price_marker': 'price-seq-no-111-222-333',
            'sort_key': 'catalog_id,scope',
            'sort_dir': 'desc,asc'}
        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.valid_catalog, 'list') as mocked_func:
            mocked_func.return_value = \
                [ValidCatalog(self,
                              valid_catalog_return_data,
                              loaded=True)]
            columns = v1shell._print_valid_catalog_columns
            v1shell.do_valid_catalog_list(self.gc, args)

            called_args, kwargs = mocked_func.call_args
            self.assertEqual(sorted(input_dict.items()),
                             sorted(called_args[0].items()))
            utils.print_list.assert_called_once_with(
                [valid_catalog_return_data],
                columns)

    def test_valid_catalog_list_invalid_no_lifetime(self):
        input_dict = {'scope': 'project_101'}
        args = self._make_args(input_dict)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_valid_catalog_list,
                          self.gc,
                          args)

    def test_valid_catalog_list_invalid_no_args(self):
        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_valid_catalog_list,
                          self.gc,
                          None)

    def test_do_price_create(self):
        """Test create command."""
        input = {'catalog_id': '1',
                 'scope': '1',
                 'price': '10000'}
        args = self._make_args(input)
        with mock.patch.object(self.gc.price, 'create') as mocked_func:
            mocked_func.return_value = Price(self,
                                             price_return_data,
                                             loaded=True)
            columns = v1shell._print_price_columns
            v1shell.do_price_create(self.gc, args)

            mocked_func.assert_called_once_with('1', '1', {'price': '10000'})
            utils.print_list.assert_called_once_with([price_print_data],
                                                     columns)

    def test_price_list(self):
        """Test 'List Search of price'
        Test the operation of the parameter without.
        """
        input = {'catalog_id': '1'}

        args = self._make_args(input)
        with mock.patch.object(self.gc.price, 'list') as mocked_func:
            mocked_func.return_value = [Price(self,
                                              price_return_data,
                                              loaded=True)]
            columns = \
                ['catalog_id',
                 'scope',
                 'seq_no',
                 'price',
                 'lifetime_start',
                 'lifetime_end',
                 'created_at',
                 'updated_at',
                 'deleted_at',
                 'deleted',
                 'expansion_key1',
                 'expansion_key2',
                 'expansion_key3',
                 'expansion_key4',
                 'expansion_key5',
                 'expansion_text']

            v1shell.do_price_list(self.gc, args)

            called_args, kwargs = mocked_func.call_args

            mocked_func.assert_called_once_with('1', {})
            utils.print_list.assert_called_once_with([price_print_data],
                                                     columns)

    def test_price_list_all_param(self):
        """Test 'List Search of price'
        Test with all parameters.
        """
        input = {'catalog_id': '1',
                 'scope': '1',
                 'lifetime': '2015-07-01',
                 'limit': 1,
                 'marker': 'a',
                 'sort_key': 'price,lifetime_start',
                 'sort_dir': 'desc,asc'}

        args = self._make_args(input)
        with mock.patch.object(self.gc.price, 'list') as mocked_func:
            mocked_func.return_value = [Price(self,
                                              price_return_data,
                                              loaded=True)]
            columns = \
                ['catalog_id',
                 'scope',
                 'seq_no',
                 'price',
                 'lifetime_start',
                 'lifetime_end',
                 'created_at',
                 'updated_at',
                 'deleted_at',
                 'deleted',
                 'expansion_key1',
                 'expansion_key2',
                 'expansion_key3',
                 'expansion_key4',
                 'expansion_key5',
                 'expansion_text']

            v1shell.do_price_list(self.gc, args)

            called_args, kwargs = mocked_func.call_args

            self.assertEqual(sorted({'scope': '1',
                                     'lifetime': '2015-07-01',
                                     'limit': 1,
                                     'marker': 'a',
                                     'sort_key': 'price,lifetime_start',
                                     'sort_dir': 'desc,asc'}.items()),
                             sorted(called_args[1].items()))
            utils.print_list.assert_called_once_with([price_print_data],
                                                     columns)

    def test_price_get(self):
        input = {'catalog_id': '1', 'scope': '1', 'seq_no': '1'}
        args = self._make_args(input)

        with mock.patch.object(self.gc.price, 'get') as mocked_func:
            mocked_func.return_value = Price(self,
                                             price_return_data,
                                             loaded=True)
            columns = v1shell._print_price_columns
            v1shell.do_price_get(self.gc, args)

            mocked_func.assert_called_once_with('1', '1', '1')
            utils.print_list.assert_called_once_with([price_print_data],
                                                     columns)

    def test_do_price_update_no_keyword(self):
        """Test create command."""
        input = {'catalog_id': '1',
                 'scope': '1',
                 'seq_no': '1'}
        args = self._make_args(input)
        with mock.patch.object(self.gc.price, 'update') as mocked_func:
            mocked_func.return_value = Price(self,
                                             price_return_data,
                                             loaded=True)
            columns = \
                ['catalog_id',
                 'scope',
                 'seq_no',
                 'price',
                 'lifetime_start',
                 'lifetime_end',
                 'created_at',
                 'updated_at',
                 'deleted_at',
                 'deleted',
                 'expansion_key1',
                 'expansion_key2',
                 'expansion_key3',
                 'expansion_key4',
                 'expansion_key5',
                 'expansion_text']

            v1shell.do_price_update(self.gc, args)

            mocked_func.assert_called_once_with('1', '1', '1', {})
            utils.print_list.assert_called_once_with([price_print_data],
                                                     columns)

    def test_do_price_update_all_param(self):
        """Test create command."""
        input = {'catalog_id': '1',
                 'scope': '1',
                 'seq_no': '1',
                 'price': '10000',
                 'lifetime_start': '2015-07-01T00:00:00',
                 'lifetime_end': '2015-08-01T00:00:00',
                 'expansion_key1': '1',
                 'expansion_key2': '2',
                 'expansion_key3': '3',
                 'expansion_key4': '4',
                 'expansion_key5': '5',
                 'expansion_text': '0'}
        args = self._make_args(input)
        with mock.patch.object(self.gc.price, 'update') as mocked_func:
            mocked_func.return_value = Price(self,
                                             price_return_data,
                                             loaded=True)
            columns = \
                ['catalog_id',
                 'scope',
                 'seq_no',
                 'price',
                 'lifetime_start',
                 'lifetime_end',
                 'created_at',
                 'updated_at',
                 'deleted_at',
                 'deleted',
                 'expansion_key1',
                 'expansion_key2',
                 'expansion_key3',
                 'expansion_key4',
                 'expansion_key5',
                 'expansion_text']

            v1shell.do_price_update(self.gc, args)

            called_args, kwargs = mocked_func.call_args

            self.assertEqual(sorted({'price': '10000',
                                     'lifetime_start': '2015-07-01T00:00:00',
                                     'lifetime_end': '2015-08-01T00:00:00',
                                     'expansions': {'expansion_key1': '1',
                                                    'expansion_key2': '2',
                                                    'expansion_key3': '3',
                                                    'expansion_key4': '4',
                                                    'expansion_key5': '5'},
                                     'expansions_text': {'expansion_text': '0'}
                                     }.items()),
                             sorted(called_args[3].items()))
            utils.print_list.assert_called_once_with([price_print_data],
                                                     columns)

    def test_do_price_delete(self):
        catalog_id = 'catalog0-1111-2222-3333-000000000001'
        scope = 'Default'
        seq_no = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'
        input_dict = {'catalog_id': catalog_id,
                      'scope': scope,
                      'seq_no': seq_no}
        args = self._make_args(input_dict)
        with mock.patch.object(self.gc.price, 'delete') as mocked_func:
            mocked_func.return_value = {}

            v1shell.do_price_delete(self.gc, args)

            mocked_func.assert_called_once_with(catalog_id, scope, seq_no)

    def test_do_price_delete_no_catalog_id(self):
        scope = 'Default'
        seq_no = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'
        input_dict = {'scope': scope,
                      'seq_no': seq_no}
        args = self._make_args(input_dict)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_price_delete,
                          self.gc,
                          args)

    def test_do_price_delete_no_scope(self):
        catalog_id = 'catalog0-1111-2222-3333-000000000001'
        seq_no = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'
        input_dict = {'catalog_id': catalog_id,
                      'seq_no': seq_no}
        args = self._make_args(input_dict)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_price_delete,
                          self.gc,
                          args)

    def test_do_price_delete_seq_no(self):
        catalog_id = 'catalog0-1111-2222-3333-000000000001'
        scope = 'Default'
        input_dict = {'catalog_id': catalog_id,
                      'scope': scope}
        args = self._make_args(input_dict)

        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_price_delete,
                          self.gc,
                          args)

    def test_do_price_delete_none_args(self):
        self.assertRaises(exceptions.SystemExit,
                          v1shell.do_price_delete,
                          self.gc,
                          None)


class ShellInvalidEndpointandParameterTest(testtools.TestCase):
    # Patch os.environ to avoid required auth info.

    def setUp(self):
        """Run before each test."""
        super(ShellInvalidEndpointandParameterTest, self).setUp()
        self.old_environment = os.environ.copy()
        os.environ = {
            'OS_USERNAME': 'username',
            'OS_PASSWORD': 'password',
            'OS_TENANT_ID': 'tenant_id',
            'OS_TOKEN_ID': 'test',
            'OS_AUTH_URL': 'http://127.0.0.1:5000/v2.0/',
            'OS_AUTH_TOKEN': 'pass',
            'OS_REGION_NAME': 'test',
            'OS_AFLO_URL': 'http://is.invalid'}

        self.shell = gshell.OpenStackClientShell()

    def tearDown(self):
        super(ShellInvalidEndpointandParameterTest, self).tearDown()
        os.environ = self.old_environment

    def run_command(self, cmd):
        self.shell.main(cmd.split())

    def assert_called(self, method, url, body=None, **kwargs):
        return self.shell.cs.assert_called(method, url, body, **kwargs)

    def assert_called_anytime(self, method, url, body=None):
        return self.shell.cs.assert_called_anytime(method, url, body)

    def test_tickettemplate_list_invalid_endpoint(self):
        """Call invalid endpoint list."""
        self.assertRaises(
            exc.CommunicationError,
            self.run_command, 'tickettemplate-list')

    def test_tickettemplate_get_invalid_endpoint(self):
        """Call invalid endpoint get."""
        self.assertRaises(
            exc.CommunicationError,
            self.run_command, 'tickettemplate-get --id 1')

    def test_tickettemplate_create_invalid_endpoint(self):
        """Call invalid endpoint create."""
        self.assertRaises(
            exc.CommunicationError,
            self.run_command,
            'tickettemplate-create --file %(file_path)s --encode utf-8' %
            {'file_path': _get_dict_contents_file_path(
                'template_contents', '20160627')}
        )

    def test_tickettemplate_delete_invalid_endpoint(self):
        """Call invalid endpoint delete."""
        self.assertRaises(
            exc.CommunicationError,
            self.run_command, 'tickettemplate-delete --id 1')

    def test_workflowpattern_create_invalid_endpoint(self):
        """Call invalid endpoint create."""
        self.assertRaises(
            exc.CommunicationError,
            self.run_command, 'workflowpattern-create --file %(file_path)s '
            '--encode utf-8' %
            {'file_path': _get_dict_contents_file_path(
                'workflow_pattern_contents')}
        )

    def test_workflowpattern_delete_invalid_endpoint(self):
        """Call invalid endpoint delete."""
        self.assertRaises(
            exc.CommunicationError,
            self.run_command, 'workflowpattern-delete --id 1')

    def test_list_invalid_endpoint(self):
        """Call invalid endpoint list."""
        self.assertRaises(
            exc.CommunicationError,
            self.run_command, 'ticket-list')

    def test_get_invalid_endpoint(self):
        """Call invalid endpoint get."""
        self.assertRaises(
            exc.CommunicationError,
            self.run_command, 'ticket-get --id 1')

    def test_create_invalid_endpoint(self):
        """Call invalid endpoint create."""
        self.assertRaises(
            exc.CommunicationError,
            self.run_command,
            'ticket-create --ticket-template-id 1 --status-code 1')

    def test_update_invalid_endpoint(self):
        """Call invalid endpoint update."""
        self.assertRaises(
            exc.CommunicationError,
            self.run_command,
            'ticket-update --id 1 --last-workflow-id 2 --next-workflow-id 3 ' +
            '--last-status-code 4 --next-status-code 5')

    def test_delete_invalid_endpoint(self):
        """Call invalid endpoint delete."""
        self.assertRaises(
            exc.CommunicationError,
            self.run_command, 'ticket-delete --id 1')

    def test_catalog_get_invalid_endpoint(self):
        """Call invalid endpoint catalog show."""
        self.assertRaises(
            exc.CommunicationError,
            self.run_command,
            'catalog-get --catalog-id ea0a4146-fd07-414b-aa5e-dedbeef00101')


def _get_dict_contents_file_path(file_prefix, version=None):
    file_name = None
    if version:
        file_name = '%(file_prefix)s_%(version)s.json' % {
            'file_prefix': file_prefix, 'version': version}
    else:
        file_name = '%(file_prefix)s.json' % {
            'file_prefix': file_prefix}

    return os.path.join(FILES_DIR, file_name)
