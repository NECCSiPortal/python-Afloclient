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
class ClientTestGoods(base.BaseTestCase):
    """Test goods of aflo component service."""

    @ddt.data('admin', 'user')
    def test_goods(self, role):
        """Test of 'Goods commands'
        Test the operation of the List, Get, Update, Delete commands result.
        :param role: running user.
        """
        goods_id = None

        # Add records
        goods_id, goods_id_dammy = self._create_goods('admin')

        # Get records by list.
        self._list_goods(role, goods_id)

        # Get records by goods get.
        self._get_goods(role, goods_id)

        # Update records
        if role == 'admin':
            self._update_goods(role, goods_id)

        # Delete records
        self.clients['admin']\
            .run_command('goods-delete',
                         params=' --goods-id ' + goods_id)

        self.clients['admin']\
            .run_command('goods-delete',
                         params=' --goods-id ' + goods_id_dammy)

        self.assertRaises(exceptions.CommandFailed,
                          self.clients['admin'].run_command,
                          'goods-delete',
                          params=' --goods-id ' + goods_id)

    def _create_goods(self, role):
        """Create goods data.
        :param role: running user.
        """

        st_create_dammy = self.clients[role].run_command(
            'goods-create',
            params=' --region-id {0}'
                   ' --goods-name {1}'.format('region_id_dammy',
                                              'goods_name_dammy'))

        st_create = self.clients[role].run_command(
            'goods-create',
            params=' --region-id {0}'
                   ' --goods-name {1}'.format('region_id', 'goods_name'))

        # Check got UUID
        goods_id = output_parser.tables(st_create)[0]['values'][0][0]
        self.assertTrue(goods_id is not None)
        goods_id_dammy = \
            output_parser.tables(st_create_dammy)[0]['values'][0][0]

        # Check all param
        check_param = {'goods_id': goods_id,
                       'region_id': 'region_id',
                       'goods_name': 'goods_name',
                       }
        self._check_return_param(
            output_parser.tables(st_create)[0]['values'][0],
            check_param)

        return goods_id, goods_id_dammy

    def _get_goods(self, role, goods_id):
        """Get goods data.
        :param role: running user.
        :param goods_id: Goods id.
        """
        st_get = self.clients[role].run_command(
            'goods-get',
            params=' --goods-id ' + goods_id)
        goods = output_parser.tables(st_get)[0]['values'][0]

        # Check all param
        check_param = {'goods_id': goods_id,
                       'region_id': 'region_id',
                       'goods_name': 'goods_name',
                       }
        self._check_return_param(goods,
                                 check_param)

        return goods

    def _list_goods(self, role, goods_id):
        """List goods data.
        :param role: running user.
        """
        st_list = self.clients[role].run_command(
            'goods-list',
            params=' --region-id {0}'
                   ' --force-show-deleted {1}'
                   .format('region_id',
                           'true'))

        goods_list = output_parser.tables(st_list)[0]['values']
        self.assertTrue(len(goods_list) >= 1)

        # Check all param
        result = False
        for goods in goods_list:
            if goods[0] == goods_id:
                result = True
                break

        self.assertTrue(result)

        return goods_list

    def _update_goods(self, role, goods_id):
        """Update goods data.
        :param role: running user.
        :param goods_id: Goods id.
        :param goods: goods.
        """
        st_update = self.clients[role].run_command(
            'goods-update',
            params=' --goods-id {0}'
                   ' --region-id {1}'
                   ' --goods-name {2}'
                   .format(goods_id,
                           'region_id_updated',
                           'goods_name_updated'))

        goods = output_parser.tables(st_update)[0]['values']

        # Check all param
        check_param = {'goods_id': goods_id,
                       'region_id': 'region_id_updated',
                       'goods_name': 'goods_name_updated',
                       }
        self._check_return_param(goods[0], check_param)

        return goods

    def _check_return_param(self, return_data, check_param):
        self.assertEqual(return_data[0], check_param['goods_id'])
        self.assertEqual(return_data[1], check_param['region_id'])
        self.assertEqual(return_data[2], check_param['goods_name'])
        self.assertIsNotNone(return_data[3])
        self.assertIsNotNone(return_data[4])
        self.assertEqual(return_data[5], 'None')
        self.assertEqual(return_data[6], 'False')
        self.assertEqual(return_data[7], 'None')
        self.assertEqual(return_data[8], 'None')
        self.assertEqual(return_data[9], 'None')
        self.assertEqual(return_data[10], 'None')
        self.assertEqual(return_data[11], 'None')
        self.assertEqual(return_data[12], 'None')

    @ddt.data('admin', 'user')
    def test_goods_invalid_get_irregular_no_data(self, role):
        """Test of 'Goods commands'
        Test the operation of the Get command(Not exist goods id).
        :param role: running user.
        """
        goods_id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'goods-get',
                          params=' --good-id ' + goods_id)

    @ddt.data('admin', 'user')
    def test_goods_list_irregular_params(self, role):
        """Test of 'Goods commands'
        Test the operation of the List command(Ignore parameters).
        :param role: running user.
        """
        args = [' --marker a',
                ' --sort-key a',
                ' --sort-dir a',
                ' --force-show-deleted a']

        for arg in args:
            # List data.
            self.assertRaises(exceptions.CommandFailed,
                              self.clients[role].run_command,
                              'goods-list %s' % arg)

    @ddt.data('user')
    def test_goods_invalid_create_irregular_no_authority(self, role):
        """Test of 'Goods commands'
        Test the operation of the Create command(Not exist authority).
        :param role: running user.
        """
        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'goods-create',
                          params=' --region-id {0}'
                                 ' --goods-name {1}'
                                 .format('region_id',
                                         'goods_name'))

    @ddt.data('admin', 'user')
    def test_goods_invalid_update_irregular_no_data(self, role):
        """Test of 'Goods commands'
        Test the operation of the Update command(Not exist goods id).
        :param role: running user.
        """
        goods_id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'goods-update',
                          params=' --goods-id {0}'
                                 ' --region-id {1}'
                                 ' --goods-name {2}'
                                 .format(goods_id, 'a', 'a'))

    @ddt.data('admin')
    def test_goods_invalid_delete_irregular_no_data(self, role):
        """Do a test of 'Goods commands'
        Test the operation of the Delete command(Not exist goods id).
        """
        goods_id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'goods-delete',
                          params=' --goods-id ' + goods_id)

    @ddt.data('user')
    def test_goods_invalid_delete_irregular_no_authority(self, role):
        """Do a test of 'Goods commands'
        Test the operation of the Delete command(Not exist authority).
        """
        goods_id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'goods-delete',
                          params=' --goods-id ' + goods_id)
