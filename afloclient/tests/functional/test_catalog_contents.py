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

import ddt
import uuid

from tempest_lib.cli import output_parser
from tempest_lib import exceptions

from afloclient.tests.functional import base


@ddt.ddt
class ClientTestCatalogContents(base.BaseTestCase):
    """Test catalog contents of aflo component service."""

    @ddt.data('admin', 'user')
    def test_catalog_contents(self, role):
        """Test of 'Catalog contents commands'
        Test the operation of the List, Get, Update, Delete commands result.
        :param role: running user.
        """
        catalog_id = 'catalog0-1111-2222-3333-100000000001'
        seq_no = None

        # Add records
        seq_no, seq_no_dammy = \
            self._create_catalog_contents('admin', catalog_id)

        # Get records by list.
        self._list_catalog_contents(role, catalog_id, seq_no)

        # Get records by catalog contents get.
        self._show_catalog_contents(role, catalog_id, seq_no)

        # Update records
        if role == 'admin':
            self._update_catalog_contents(role,
                                          catalog_id,
                                          seq_no)

        # Delete records
        self.clients['admin']\
            .run_command('catalog-contents-delete',
                         params=' --catalog-id %s --seq-no %s' %
                                (catalog_id, seq_no))

        self.clients['admin']\
            .run_command('catalog-contents-delete',
                         params=' --catalog-id %s --seq-no %s' %
                                ('catalog0-1111-2222-3333-100000000002',
                                 seq_no_dammy))

        self.assertRaises(exceptions.CommandFailed,
                          self.clients['admin'].run_command,
                          'catalog-contents-delete',
                          params=' --catalog-id %s --seq-no %s' %
                          (catalog_id, seq_no))

    def _create_catalog_contents(self, role, catalog_id):
        """Create catalog contents data.
        :param role: running user.
        :param catalog_id: Catalog id.
        """
        st_create_dammy = self.clients[role].run_command(
            'catalog-contents-create',
            params=' --catalog-id {0}'
                   ' --goods-id {1}'
                   ' --goods-num {2}'
                   .format('catalog0-1111-2222-3333-100000000002',
                           'goods_id_dammy',
                           '5678'))

        st_create = self.clients[role].run_command(
            'catalog-contents-create',
            params=' --catalog-id {0}'
                   ' --goods-id {1}'
                   ' --goods-num {2}'
                   .format(catalog_id,
                           'goods_id',
                           '1234'))

        # Check got UUID
        seq_no = output_parser.tables(st_create)[0]['values'][0][1]
        self.assertTrue(seq_no is not None)
        seq_no_dammy = output_parser.tables(st_create_dammy)[0]['values'][0][1]
        self.assertTrue(seq_no is not None)

        # Check all param
        check_param = {'catalog_id': catalog_id,
                       'seq_no': seq_no,
                       'goods_id': 'goods_id',
                       'goods_num': '1234',
                       }
        self._check_return_param(
            output_parser.tables(st_create)[0]['values'][0],
            check_param)

        return seq_no, seq_no_dammy

    def _show_catalog_contents(self, role, catalog_id, seq_no):
        """Show catalog contents data.
        :param role: running user.
        :param catalog_id: Catalog id.
        :param seq_no: Seq no.
        """
        st_get = self.clients[role].run_command(
            'catalog-contents-get',
            params=' --catalog-id ' + catalog_id + ' --seq-no ' + seq_no)
        catalog_contents = output_parser.tables(st_get)[0]['values'][0]

        # Check all param
        check_param = {'catalog_id': catalog_id,
                       'seq_no': seq_no,
                       'goods_id': 'goods_id',
                       'goods_num': '1234',
                       }
        self._check_return_param(catalog_contents,
                                 check_param)

        return catalog_contents

    def _list_catalog_contents(self, role, catalog_id, seq_no):
        """List catalog contents data.
        :param role: running user.
        :param catalog_id: Catalog id.
        """
        st_list = self.clients[role].run_command(
            'catalog-contents-list',
            params=' --catalog-id {0}'
                   ' --limit {1}'
                   ' --force-show-deleted {2}'
                   .format(catalog_id,
                           '1000',
                           'true'))

        catalog_contents_list = output_parser.tables(st_list)[0]['values']
        self.assertTrue(len(catalog_contents_list) >= 1)

        # Check all param
        result = False
        for catalog_contents in catalog_contents_list:
            if catalog_contents[1] == seq_no:
                result = True
                break

        self.assertTrue(result)

        return catalog_contents_list

    def _update_catalog_contents(self,
                                 role,
                                 catalog_id,
                                 seq_no):
        """Update catalog contents data.
        :param role: running user.
        :param catalog_id: Catalog id.
        :param seq_no: Seq no.
        :param catalog contents: catalog contents.
        """
        st_update = self.clients[role].run_command(
            'catalog-contents-update',
            params=' --catalog-id {0}'
                   ' --seq-no {1}'
                   ' --goods-id {2}'
                   ' --goods-num {3}'
                   .format(catalog_id,
                           seq_no,
                           'goods_id_updated',
                           '912'))

        catalog_contents = output_parser.tables(st_update)[0]['values'][0]

        # Check all param
        check_param = {'catalog_id': catalog_id,
                       'seq_no': seq_no,
                       'goods_id': 'goods_id_updated',
                       'goods_num': '912',
                       }
        self._check_return_param(catalog_contents, check_param)

        return catalog_contents

    def _check_return_param(self, return_data, check_param):
        self.assertEqual(return_data[0], check_param['catalog_id'])
        self.assertEqual(return_data[1], check_param['seq_no'])
        self.assertEqual(return_data[2], check_param['goods_id'])
        self.assertEqual(return_data[3], check_param['goods_num'])
        self.assertIsNotNone(return_data[4])
        self.assertIsNotNone(return_data[5])
        self.assertEqual(return_data[6], 'None')
        self.assertEqual(return_data[7], 'False')
        self.assertEqual(return_data[8], 'None')
        self.assertEqual(return_data[9], 'None')
        self.assertEqual(return_data[10], 'None')
        self.assertEqual(return_data[11], 'None')
        self.assertEqual(return_data[12], 'None')
        self.assertEqual(return_data[13], 'None')

    @ddt.data('admin', 'user')
    def test_catalog_contents_invalid_show_irregular_no_data(self, role):
        """Test of 'Catalog contents commands'
        Test the operation of the Show command(Not exist seq no).
        :param role: running user.
        """
        catalog_id = 'catalog0-1111-2222-3333-000000000005'
        seq_no = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'catalog-contents-show',
                          params=' --catalog-id % --seq-no %s' %
                                 (catalog_id, seq_no))

    @ddt.data('admin', 'user')
    def test_catalog_contents_list_irregular_params(self, role):
        """Test of 'Catalog contents commands'
        Test the operation of the List command(Ignore parameters).
        :param role: running user.
        """
        catalog_id = 'catalog0-1111-2222-3333-000000000005'

        args = [' --sort-key a',
                ' --sort-dir a',
                ' --limit a',
                ' --marker a',
                ' --force-show-deleted a']

        for arg in args:
            # List data.
            self.assertRaises(exceptions.CommandFailed,
                              self.clients[role].run_command,
                              'catalog-contents-list %s %s' %
                              (catalog_id, arg))

    @ddt.data('user')
    def test_catalog_contents_invalid_create_irregular_no_auth(self, role):
        """Test of 'Catalog contents commands'
        Test the operation of the Create command(Not exist authority).
        :param role: running user.
        """
        catalog_id = 'catalog0-1111-2222-3333-000000000005'

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'catalog-contents-create',
                          params=' --catalog-id {0}'
                                 ' --goods-id {1}'
                                 ' --goods-num {2}'
                                 .format(catalog_id, 'goods_id', '1234'))

    @ddt.data('admin', 'user')
    def test_catalog_contents_invalid_update_irregular_no_data(self, role):
        """Test of 'Catalog contents commands'
        Test the operation of the Update command(Not exist seq no).
        :param role: running user.
        """
        catalog_id = 'catalog0-1111-2222-3333-000000000005'
        seq_no = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'catalog-contents-update',
                          params=' --catalog-id {0}'
                                 ' --seq-no {1}'
                                 ' --goods-id {2}'
                                 ' --goods-num {3}'
                                 .format(catalog_id,
                                         seq_no, 'a', 'a'))

    @ddt.data('admin')
    def test_catalog_contents_invalid_delete_irregular_no_data(self, role):
        """Do a test of 'Catalog contents commands'
        Test the operation of the Delete command(Not exist catalog id, seq no).
        """
        catalog_id = str(uuid.uuid4())
        seq_no = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'catalog-contents-delete',
                          params=' --catalog-id %s --seq-no %s' %
                                 (catalog_id, seq_no))

    @ddt.data('user')
    def test_catalog_contents_invalid_delete_irregular_no_authority(self,
                                                                    role):
        """Do a test of 'Catalog contents commands'
        Test the operation of the Delete command(Not exist authority).
        """
        catalog_id = str(uuid.uuid4())
        seq_no = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'catalog-contents-delete',
                          params=' --catalog-id %s --seq-no %s' %
                                 (catalog_id, seq_no))
