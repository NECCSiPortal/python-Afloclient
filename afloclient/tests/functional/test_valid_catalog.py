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
#
#

import ddt

from tempest_lib.cli import output_parser

from afloclient import config
from afloclient.tests.functional import base

CONF = config.CONF


@ddt.ddt
class ClientTestValidCatalog(base.BaseTestCase):
    """Test valid catalog of aflo component service."""

    @ddt.data('admin', 'user')
    def test_valid_catalog(self, role):
        """Test of 'Valid catalog commands'
        Test the operation of the List commands result.
        :param role:running user.
        """

        # Get users project_id.
        if role == 'user':
            scope = CONF.project_id
        else:
            scope = CONF.admin_project_id

        # To perform a 'valid-catalog-list' command,
        # it is necessary to prepare a test data in the following table.
        # - catalog
        # - catalog_scope
        # - price
        catalog_id, catalog_id_dammy = self._create_catalog('admin')

        seq_no, seq_no_dammy = self._create_price('admin', catalog_id,
                                                  catalog_id_dammy, scope)

        catalog_scope_id, catalog_scope_id_dammy = \
            self._create_catalog_scope('admin', catalog_id,
                                       catalog_id_dammy, scope)

        # Get records by valid catalog list.
        self._list_valid_catalog(role, catalog_id, catalog_scope_id,
                                 seq_no, scope)

        # The test data it will clean up.
        self.clients['admin'].run_command(
            'catalog-delete', params=' --catalog-id ' + catalog_id)
        self.clients['admin'].run_command(
            'catalog-delete', params=' --catalog-id ' + catalog_id_dammy)

        self.clients['admin'].run_command(
            'price-delete', params=' --catalog-id %s --scope %s --seq-no %s' %
                                   (catalog_id, scope, seq_no))
        self.clients['admin'].run_command(
            'price-delete', params=' --catalog-id %s --scope %s --seq-no %s' %
                                   (catalog_id_dammy, scope, seq_no_dammy))

        self.clients['admin'].run_command(
            'catalog-scope-delete', params=' --id ' + catalog_scope_id)
        self.clients['admin'].run_command(
            'catalog-scope-delete', params=' --id ' + catalog_scope_id_dammy)

    def _create_catalog(self, role):
        """Create catalog data.
        :param role: running user.
        """

        st_create = self.clients[role].run_command(
            'catalog-create',
            params=' --region-id {0}'
                   ' --catalog-name {1}'
                   ' --lifetime-start {2}'
                   ' --lifetime-end {3}'
                   .format('region_id',
                           'catalog_name',
                           '2015-01-01T01:02:03.123456',
                           '2018-11-12T04:05:06.234567'))

        st_create_dammy = self.clients[role].run_command(
            'catalog-create',
            params=' --region-id {0}'
                   ' --catalog-name {1}'
                   ' --lifetime-start {2}'
                   ' --lifetime-end {3}'
                   .format('region_id_dammy',
                           'catalog_name_dammy',
                           '2015-01-01T01:02:03.123456',
                           '2018-11-12T04:05:06.234567'))

        # Check got UUID.
        catalog_id = output_parser.tables(st_create)[0]['values'][0][0]
        self.assertTrue(catalog_id is not None)
        catalog_id_dammy = \
            output_parser.tables(st_create_dammy)[0]['values'][0][0]

        return catalog_id, catalog_id_dammy

    def _create_price(self, role, catalog_id, catalog_id_dammy, scope):
        """Create price data.
        :param role: running user.
        :param catalog_id: Catalog id.
        :param scope: scope.
        """

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
                           '2018-11-12T04:05:06.234567'))

        st_create_dammy = self.clients[role].run_command(
            'price-create',
            params=' --catalog-id {0}'
                   ' --scope {1}'
                   ' --price {2}'
                   ' --lifetime-start {3}'
                   ' --lifetime-end {4}'
                   .format(catalog_id_dammy,
                           scope,
                           '123.45',
                           '2015-01-01T01:02:03.123456',
                           '2018-11-12T04:05:06.234567'))

        # Check got UUID.
        seq_no = output_parser.tables(st_create)[0]['values'][0][2]
        self.assertTrue(seq_no is not None)
        seq_no_dammy = \
            output_parser.tables(st_create_dammy)[0]['values'][0][2]

        return seq_no, seq_no_dammy

    def _create_catalog_scope(self, role, catalog_id, catalog_id_dammy, scope):
        """Create catalog data.
        :param role: running user.
        """
        st_create = self.clients[role].run_command(
            'catalog-scope-create',
            params=' --catalog-id {0}'
                   ' --scope {1}'
                   ' --lifetime-start {2}'
                   ' --lifetime-end {3}'
                   .format(catalog_id,
                           scope,
                           '2015-01-01T01:02:03.123456',
                           '2020-11-12T04:05:06.234567'))

        st_create_dammy = self.clients[role].run_command(
            'catalog-scope-create',
            params=' --catalog-id {0}'
                   ' --scope {1}'
                   ' --lifetime-start {2}'
                   ' --lifetime-end {3}'
                   .format(catalog_id_dammy,
                           scope,
                           '2015-01-01T01:02:03.123456',
                           '2020-11-12T04:05:06.234567'))

        # Check got UUID.
        catalog_scope_id = output_parser.tables(st_create)[0]['values'][0][0]
        catalog_scope_id_dammy = \
            output_parser.tables(st_create_dammy)[0]['values'][0][0]
        self.assertTrue(catalog_id is not None)

        return catalog_scope_id, catalog_scope_id_dammy

    def _list_valid_catalog(self, role, catalog_id, catalog_scope_id,
                            seq_no, scope):
        """List valid catalog data.
        :param role: running user.
        :param catalog_id: catalog id for check list result.
        :param catalog_scope_id: catalog scope id for check list result.
        :param seq_no: price seq no for check list result.
        :param scope: project id.
        """

        st_list = self.clients[role].run_command(
            'valid-catalog-list',
            params=' --scope {0}'
                   ' --lifetime {1}'
                   .format(scope,
                           '2017-01-01T01:02:03.123456'))

        valid_catalog_list = output_parser.tables(st_list)[0]['values']
        self.assertTrue(len(valid_catalog_list) >= 1)

        # Check all param.
        result = False
        for valid_catalog_info in valid_catalog_list:
            if valid_catalog_info[0] == catalog_id and \
                    valid_catalog_info[5] == catalog_scope_id and \
                    valid_catalog_info[8] == seq_no:
                result = True
                break

        self.assertTrue(result)
