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
class ClientTestPrices(base.BaseTestCase):
    """Test price of aflo component service."""

    @ddt.data('admin', 'user')
    def test_price(self, role):
        """Test of 'Price commands'
        Test the operation of the List, Get, Update, Delete commands result.
        :param role: running user.
        """
        catalog_id = 'catalog0-1111-2222-3333-100000000001'
        scope = 'Default'

        # Add records
        seq_no, seq_no_dammy = self._create_price('admin', catalog_id, scope)

        # Get records by list.
        self._list_price(role, catalog_id, scope, seq_no)

        # Get records by price get.
        self._show_price(role, catalog_id, scope, seq_no)

        # Update records
        if role == 'admin':
            self._update_price(role, catalog_id, scope, seq_no)

        # Delete records
        self.clients['admin']\
            .run_command('price-delete',
                         params=' --catalog-id %s --scope %s --seq-no %s' %
                                (catalog_id, scope, seq_no))

        self.clients['admin']\
            .run_command('price-delete',
                         params=' --catalog-id %s --scope %s --seq-no %s' %
                                ('catalog0-1111-2222-3333-100000000001',
                                 scope,
                                 seq_no_dammy))

        self.assertRaises(exceptions.CommandFailed,
                          self.clients['admin'].run_command,
                          'price-delete',
                          params=' --catalog-id %s --scope %s --seq-no %s' %
                          (catalog_id, scope, seq_no))

    def _create_price(self, role, catalog_id, scope):
        """Create price data.
        :param role: running user.
        :param catalog_id: Catalog id.
        :param scope: scope.
        """

        st_create_dammy = self.clients[role].run_command(
            'price-create',
            params=' --catalog-id {0}'
                   ' --scope {1}'
                   ' --price {2}'
                   ' --lifetime-start {3}'
                   ' --lifetime-end {4}'
                   .format('catalog0-1111-2222-3333-100000000001',
                           scope,
                           '123.45',
                           '2015-01-01T01:02:03.123456',
                           '2015-11-12T04:05:06.234567'))

        st_create = self.clients[role].run_command(
            'price-create',
            params=' --catalog-id {0}'
                   ' --scope {1}'
                   ' --price {2}'
                   ' --lifetime-start {3}'
                   ' --lifetime-end {4}'
                   .format(catalog_id,
                           scope,
                           '123.456',
                           '2015-01-01T01:02:03.123456',
                           '2015-11-12T04:05:06.234567'))

        # Check got UUID
        seq_no = output_parser.tables(st_create)[0]['values'][0][2]
        self.assertTrue(seq_no is not None)
        seq_no_dammy = \
            output_parser.tables(st_create_dammy)[0]['values'][0][2]

        # Check all param
        check_param = {'catalog_id': catalog_id,
                       'scope': scope,
                       'seq_no': seq_no,
                       'price': '123.456',
                       'lifetime_start': '2015-01-01T01:02:03.123456',
                       'lifetime_end': '2015-11-12T04:05:06.234567',
                       }
        self._check_return_param(
            output_parser.tables(st_create)[0]['values'][0],
            check_param)

        return seq_no, seq_no_dammy

    def _show_price(self, role, catalog_id, scope, seq_no):
        """Show price data.
        :param role: running user.
        :param catalog_id: Catalog id.
        :param scope: scope.
        :pram seq_no: seq_no.
        """
        st_get = self.clients[role].run_command(
            'price-get',
            params=' --catalog-id %s --scope %s --seq-no %s' %
                   (catalog_id, scope, seq_no))
        price = output_parser.tables(st_get)[0]['values'][0]

        # Check all param
        check_param = {'catalog_id': catalog_id,
                       'scope': scope,
                       'seq_no': seq_no,
                       'price': '123.456',
                       'lifetime_start': '2015-01-01T01:02:03.000000',
                       'lifetime_end': '2015-11-12T04:05:06.000000',
                       }
        self._check_return_param(price,
                                 check_param)

        return price

    def _list_price(self, role, catalog_id, scope, seq_no):
        """List price data.
        :param role: running user.
        :param catalog_id: Catalog id.
        """
        st_list = self.clients[role].run_command(
            'price-list',
            params=' --catalog-id {0}'
                   ' --lifetime {1}'
                   ' --sort-key {2}'
                   ' --sort-dir {3}'
                   ' --limit {4}'
                   ' --force-show-deleted {5}'
                   .format(catalog_id,
                           '2015-09-28T12:13:14.123456',
                           'price',
                           'asc',
                           '1000',
                           'true'))

        price_list = output_parser.tables(st_list)[0]['values']
        self.assertTrue(len(price_list) >= 1)

        # Check all param
        result = False
        for price in price_list:
            if price[2] == seq_no:
                result = True
                break

        self.assertTrue(result)

        return price_list

    def _update_price(self, role, catalog_id, scope, seq_no):
        """Update price data.
        :param role: running user.
        :param catalog_id: Catalog id.
        :param scope: scope.
        :pram seq_no: Seq no.
        :param price: price.
        """
        st_update = self.clients[role].run_command(
            'price-update',
            params=' --catalog-id {0}'
                   ' --scope {1}'
                   ' --seq-no {2}'
                   ' --price {3}'
                   ' --lifetime-start {4}'
                   ' --lifetime-end {5}'
                   .format(catalog_id,
                           scope,
                           seq_no,
                           '678.91',
                           '2016-01-01T01:02:03.123456',
                           '2016-11-12T04:05:06.234567'))

        price = output_parser.tables(st_update)[0]['values']

        # Check all param
        check_param = {'catalog_id': catalog_id,
                       'scope': scope,
                       'seq_no': seq_no,
                       'price': '678.91',
                       'lifetime_start': '2016-01-01T01:02:03.123456',
                       'lifetime_end': '2016-11-12T04:05:06.234567',
                       }
        self._check_return_param(price[0], check_param)

        return price

    def _check_return_param(self, return_data, check_param):
        self.assertEqual(return_data[0], check_param['catalog_id'])
        self.assertEqual(return_data[1], check_param['scope'])
        self.assertEqual(return_data[2], check_param['seq_no'])
        self.assertEqual(return_data[3], check_param['price'])
        self.assertEqual(return_data[4], check_param['lifetime_start'])
        self.assertEqual(return_data[5], check_param['lifetime_end'])
        self.assertIsNotNone(return_data[6])
        self.assertIsNotNone(return_data[7])
        self.assertEqual(return_data[8], 'None')
        self.assertEqual(return_data[9], 'False')
        self.assertEqual(return_data[10], 'None')
        self.assertEqual(return_data[11], 'None')
        self.assertEqual(return_data[12], 'None')
        self.assertEqual(return_data[13], 'None')
        self.assertEqual(return_data[14], 'None')
        self.assertEqual(return_data[15], 'None')

    @ddt.data('admin', 'user')
    def test_price_invalid_show_irregular_no_data(self, role):
        """Test of 'Price commands'
        Test the operation of the Show command(Not exist seq no).
        :param role: running user.
        :param catalog_id: Catalog id.
        :param scope: scope.
        """
        catalog_id = 'catalog0-1111-2222-3333-000000000005'
        scope = 'Default'
        seq_no = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'price-show',
                          params=' --catalog-id %s --scope %s --seq-no %s' %
                                 (catalog_id, scope, seq_no))

    @ddt.data('admin', 'user')
    def test_price_list_irregular_params(self, role):
        """Test of 'Price commands'
        Test the operation of the List command(Ignore parameters).
        :param role: running user.
        """
        catalog_id = 'catalog0-1111-2222-3333-000000000005'

        args = [' --lifetime a',
                ' --sort-key a',
                ' --sort-dir a',
                ' --limit a',
                ' --marker a',
                ' --force-show-deleted a']

        for arg in args:
            # List data.
            self.assertRaises(exceptions.CommandFailed,
                              self.clients[role].run_command,
                              'price-list %s %s' % (catalog_id, arg))

    @ddt.data('user')
    def test_price_invalid_create_irregular_no_authority(self, role):
        """Test of 'Price commands'
        Test the operation of the Create command(Not exist authority).
        :param role: running user.
        :param catalog_id: Catalog id.
        :param scope: scope.
        """
        catalog_id = 'catalog0-1111-2222-3333-000000000005'
        scope = 'Default'

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'price-create',
                          params=' --catalog_id {0}'
                                 ' --scope {1}'
                                 ' --price {2}'
                                 ' --lifetime-start {3}'
                                 ' --lifetime-end {4}'
                                 .format(catalog_id,
                                         scope,
                                         '123.45',
                                         '2015-01-01T12:13:14.123456',
                                         '2015-12-13T13:14:15.234567'))

    @ddt.data('admin', 'user')
    def test_price_invalid_update_irregular_no_data(self, role):
        """Test of 'Price commands'
        Test the operation of the Update command(Not exist price id).
        :param role: running user.
        :param catalog_id: Catalog id.
        :param scope: scope.
        :param seq_no: Seq no.
        """
        catalog_id = 'catalog0-1111-2222-3333-000000000005'
        scope = 'Default'
        seq_no = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'price-update',
                          params=' --catalog-id {0}'
                                 ' --scope {1}'
                                 ' --seq-no {2}'
                                 ' --price {3}'
                                 ' --lifetime-start {4}'
                                 ' --lifetime-end {5}'
                                 .format(catalog_id,
                                         scope,
                                         seq_no,
                                         'a', 'a', 'a'))

    @ddt.data('admin')
    def test_price_invalid_delete_irregular_no_data(self, role):
        """Do a test of 'Price commands'
        Test the operation of the Delete command(Not exist
         catalog id, scope, seq no).
        """
        catalog_id = str(uuid.uuid4())
        scope = 'Default'
        seq_no = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'price-delete',
                          params=' --catalog-id %s --scope %s --seq-no %s' %
                                 (catalog_id, scope, seq_no))

    @ddt.data('user')
    def test_price_invalid_delete_irregular_no_authority(self, role):
        """Do a test of 'Price commands'
        Test the operation of the Delete command(Not exist authority).
        """
        catalog_id = str(uuid.uuid4())
        scope = 'Default'
        seq_no = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'price-delete',
                          params=' --catalog-id %s --scope %s --seq-no %s' %
                                 (catalog_id, scope, seq_no))
