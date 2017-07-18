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

"""Test afloclient/v1/catalogs.py."""

import testtools

from afloclient.tests.unit import utils
from afloclient.v1 import catalogs
from datetime import datetime
from six.moves.urllib import parse


def get_datetime(str_date):
    """Get datetime.
        :param str_date: String of date.
    """
    return datetime.strptime(str_date + 'T00:00:00.000000',
                             '%Y-%m-%dT%H:%M:%S.%f')

CATALOG_ID_101 = 'ea0a4146-fd07-414b-aa5e-dedbeef00101'
CATALOG_ID_102 = 'ea0a4146-fd07-414b-aa5e-dedbeef00102'
CATALOG_ID_103 = 'ea0a4146-fd07-414b-aa5e-dedbeef00103'
CATALOG_ID_104 = 'ea0a4146-fd07-414b-aa5e-dedbeef00104'

fixtures_catalog_data_detail_101 = \
    {'catalog_id': CATALOG_ID_101,
     'region_id': 'region_id_101',
     'catalog_name': 'catalog_name_101',
     'lifetime_start': get_datetime('2015-07-01'),
     'lifetime_end': get_datetime('2015-08-01'),
     'created_at': datetime.utcnow(),
     'updated_at': None,
     'deleted_at': None,
     'deleted': False,
     'expansions': {'expansion_key1': 'expansion_key1',
                    'expansion_key2': 'expansion_key2',
                    'expansion_key3': 'expansion_key3',
                    'expansion_key4': 'expansion_key4',
                    'expansion_key5': 'expansion_key5'},
     'expansions_text': {'expansion_text': 'expansion_text'}}

fixtures_catalog_data_detail_102 = \
    {'catalog_id': CATALOG_ID_102,
     'region_id': 'region_id_102',
     'catalog_name': 'catalog_name_102',
     'lifetime_start': get_datetime('2015-07-02'),
     'lifetime_end': get_datetime('2015-08-02'),
     'created_at': datetime.utcnow(),
     'updated_at': datetime.utcnow(),
     'deleted_at': datetime.utcnow(),
     'deleted': True,
     'expansions': {'expansion_key1': 'expansion_key1',
                    'expansion_key2': 'expansion_key2',
                    'expansion_key3': 'expansion_key3',
                    'expansion_key4': 'expansion_key4',
                    'expansion_key5': 'expansion_key5'},
     'expansions_text': {'expansion_text': 'expansion_text'}}

fixtures_catalog_data_detail_103 = \
    {'catalog_id': CATALOG_ID_103,
     'region_id': 'region_id_103',
     'catalog_name': 'catalog_name_103',
     'lifetime_start': get_datetime('2015-07-03'),
     'lifetime_end': get_datetime('2015-08-03'),
     'created_at': datetime.utcnow(),
     'updated_at': datetime.utcnow(),
     'deleted_at': datetime.utcnow(),
     'deleted': True,
     'expansions': {'expansion_key1': 'expansion_key1',
                    'expansion_key2': 'expansion_key2',
                    'expansion_key3': 'expansion_key3',
                    'expansion_key4': 'expansion_key4',
                    'expansion_key5': 'expansion_key5'},
     'expansions_text': {'expansion_text': 'expansion_text'}}

fixtures_catalog_data_detail_104 = \
    {'catalog_id': CATALOG_ID_104,
     'region_id': None,
     'catalog_name': None,
     'lifetime_start': None,
     'lifetime_end': None,
     'created_at': datetime.utcnow(),
     'updated_at': None,
     'deleted_at': None,
     'deleted': False,
     'expansions': {'expansion_key1': None,
                    'expansion_key2': None,
                    'expansion_key3': None,
                    'expansion_key4': None,
                    'expansion_key5': None},
     'expansions_text': {'expansion_text': None}}


# from afloclient.v1 import client
#  request fixtures
#    (request url, request header, request parameter).
fixtures = \
    {
        '/v1/catalog': {
            'POST': (
                {},
                {'catalog': {
                    'catalog_name': 'test_catalog'
                }},
            ),
            'GET': (
                {},
                {'catalog': [fixtures_catalog_data_detail_104,
                             fixtures_catalog_data_detail_103,
                             fixtures_catalog_data_detail_102,
                             fixtures_catalog_data_detail_101]},
            ),
        },
        '/v1/catalog/%s' % CATALOG_ID_101: {
            'GET': (
                {},
                {'catalog': fixtures_catalog_data_detail_101},
            ),
            'PATCH': (
                {},
                {'catalog': fixtures_catalog_data_detail_101},
            ),
            'DELETE': (
                {},
                {},
            ),
        },
        '/v1/catalog/%s' % CATALOG_ID_102: {
            'GET': (
                {},
                {'catalog': fixtures_catalog_data_detail_102},
            ),
        },
        '/v1/catalog/%s' % CATALOG_ID_103: {
            'GET': (
                {},
                {'catalog': None},
            ),
        },
        '/v1/catalog/%s' % CATALOG_ID_104: {
            'GET': (
                {},
                {'catalog': fixtures_catalog_data_detail_104},
            ),
        },
        '/v1/catalog?catalog_id=1': {
            'GET': (
                {},
                {'catalog': [fixtures_catalog_data_detail_101]},
            ),
        },
        '/v1/catalog?region_id=1': {
            'GET': (
                {},
                {'catalog': [fixtures_catalog_data_detail_102]},
            ),
        },
        '/v1/catalog?catalog_name=catalog_name1': {
            'GET': (
                {},
                {'catalog': [fixtures_catalog_data_detail_103]},
            ),
        },
        '/v1/catalog?lifetime=2015-07-01': {
            'GET': (
                {},
                {'catalog': [fixtures_catalog_data_detail_104,
                             fixtures_catalog_data_detail_103,
                             fixtures_catalog_data_detail_101]},
            ),
        },
        '/v1/catalog?limit=1': {
            'GET': (
                {},
                {'catalog': [fixtures_catalog_data_detail_104]},
            ),
        },
        '/v1/catalog?marker=3': {
            'GET': (
                {},
                {'catalog': [fixtures_catalog_data_detail_102,
                             fixtures_catalog_data_detail_101]},
            ),
        },
        '/v1/catalog?sort_dir=desc': {
            'GET': (
                {},
                {'catalog': [fixtures_catalog_data_detail_104,
                             fixtures_catalog_data_detail_101]},
            ),
        },
        '/v1/catalog?sort_key=catalog_id': {
            'GET': (
                {},
                {'catalog': [fixtures_catalog_data_detail_103,
                             fixtures_catalog_data_detail_101]},
            ),
        },
        '/v1/catalog?sort_dir=desc&sort_key=catalog_id': {
            'GET': (
                {},
                {'catalog': [fixtures_catalog_data_detail_102,
                             fixtures_catalog_data_detail_101,
                             fixtures_catalog_data_detail_103,
                             fixtures_catalog_data_detail_104]},
            ),
        },
        '/v1/catalog?sort_key=catalog_id&sort_dir=desc': {
            'GET': (
                {},
                {'catalog': [fixtures_catalog_data_detail_102,
                             fixtures_catalog_data_detail_101,
                             fixtures_catalog_data_detail_103,
                             fixtures_catalog_data_detail_104]},
            ),
        },
        '/v1/catalog?force_show_deleted=True': {
            'GET': (
                {},
                {'catalog': [fixtures_catalog_data_detail_101,
                             fixtures_catalog_data_detail_102,
                             fixtures_catalog_data_detail_103,
                             fixtures_catalog_data_detail_104]},
            ),
        },
        '/v1/catalog'
        '?force_show_deleted=True&lifetime=2015-07-01&limit=1'
        '&marker=ea0a4146-fd07-414b-aa5e-dedbeef00103'
        '&sort_dir=desc&sort_key=catalog_id': {
            'GET': (
                {},
                {'catalog': [fixtures_catalog_data_detail_104]},
            ),
        },
    }


class CatalogManagerTest(testtools.TestCase):
    """CatalogManager Test class."""

    def setUp(self):
        """Setup test class."""
        super(CatalogManagerTest, self).setUp()
        self.api = utils.FakeAPI(fixtures)
        self.mgr = catalogs.CatalogManager(self.api)

    def test_create(self):
        """Test create method."""
        kwargs = {
            'catalog_name': 'test_catalog'
        }
        expectResponse = {
            'catalog': kwargs
        }

        self.mgr.create(kwargs)
        expect = [('POST', '/v1/catalog', {}, expectResponse.items())]

        self.assertEqual(expect, self.api.calls)

    def test_update(self):
        expectResponse = {'catalog': fixtures_catalog_data_detail_101}

        self.mgr.update('ea0a4146-fd07-414b-aa5e-dedbeef00101',
                        fixtures_catalog_data_detail_101)
        expect = [('PATCH',
                   '/v1/catalog/ea0a4146-fd07-414b-aa5e-dedbeef00101',
                   {}, expectResponse.items())]
        self.assertEqual(expect, self.api.calls)

    def test_get(self):
        """Test get method."""
        catalog = self.mgr.get(CATALOG_ID_101)
        url = '/v1/catalog/%s' % CATALOG_ID_101
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertIsNotNone(catalog)
        self.assertEqual(catalog.catalog_id, CATALOG_ID_101)
        self.assertEqual(catalog.region_id, 'region_id_101')
        self.assertEqual(catalog.catalog_name, 'catalog_name_101')
        self.assertEqual(catalog.lifetime_start, get_datetime('2015-07-01'))
        self.assertEqual(catalog.lifetime_end, get_datetime('2015-08-01'))
        self.assertIsNotNone(catalog.created_at)
        self.assertIsNone(catalog.updated_at)
        self.assertIsNone(catalog.deleted_at)
        self.assertEqual(catalog.deleted, False)
        self.assertEqual(catalog.expansions['expansion_key1'],
                         'expansion_key1')
        self.assertEqual(catalog.expansions['expansion_key2'],
                         'expansion_key2')
        self.assertEqual(catalog.expansions['expansion_key3'],
                         'expansion_key3')
        self.assertEqual(catalog.expansions['expansion_key4'],
                         'expansion_key4')
        self.assertEqual(catalog.expansions['expansion_key5'],
                         'expansion_key5')
        self.assertEqual(catalog.expansions_text['expansion_text'],
                         'expansion_text')

    def test_get_deleted_data(self):
        """Test get method."""
        catalog = self.mgr.get(CATALOG_ID_102)
        url = '/v1/catalog/%s' % CATALOG_ID_102
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertIsNotNone(catalog)
        self.assertEqual(catalog.catalog_id, CATALOG_ID_102)
        self.assertEqual(catalog.region_id, 'region_id_102')
        self.assertEqual(catalog.catalog_name, 'catalog_name_102')
        self.assertEqual(catalog.lifetime_start, get_datetime('2015-07-02'))
        self.assertEqual(catalog.lifetime_end, get_datetime('2015-08-02'))
        self.assertIsNotNone(catalog.created_at)
        self.assertIsNotNone(catalog.updated_at)
        self.assertIsNotNone(catalog.deleted_at)
        self.assertEqual(catalog.deleted, True)
        self.assertEqual(catalog.expansions['expansion_key1'],
                         'expansion_key1')
        self.assertEqual(catalog.expansions['expansion_key2'],
                         'expansion_key2')
        self.assertEqual(catalog.expansions['expansion_key3'],
                         'expansion_key3')
        self.assertEqual(catalog.expansions['expansion_key4'],
                         'expansion_key4')
        self.assertEqual(catalog.expansions['expansion_key5'],
                         'expansion_key5')
        self.assertEqual(catalog.expansions_text['expansion_text'],
                         'expansion_text')

    def test_get_no_data(self):
        """Test get method."""
        catalog = self.mgr.get(CATALOG_ID_103)
        url = '/v1/catalog/%s' % CATALOG_ID_103
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertIsNone(catalog)

    def test_get_min_data(self):
        """Test get method."""
        catalog = self.mgr.get(CATALOG_ID_104)
        url = '/v1/catalog/%s' % CATALOG_ID_104
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertIsNotNone(catalog)
        self.assertEqual(catalog.catalog_id, CATALOG_ID_104)
        self.assertIsNone(catalog.region_id)
        self.assertIsNone(catalog.catalog_name)
        self.assertIsNone(catalog.lifetime_start)
        self.assertIsNone(catalog.lifetime_end)
        self.assertIsNotNone(catalog.created_at)
        self.assertIsNone(catalog.updated_at)
        self.assertIsNone(catalog.deleted_at)
        self.assertEqual(catalog.deleted, False)
        self.assertIsNone(catalog.expansions['expansion_key1'])
        self.assertIsNone(catalog.expansions['expansion_key2'])
        self.assertIsNone(catalog.expansions['expansion_key3'])
        self.assertIsNone(catalog.expansions['expansion_key4'])
        self.assertIsNone(catalog.expansions['expansion_key5'])
        self.assertIsNone(catalog.expansions_text['expansion_text'])

    def test_delete(self):
        """Test delete method."""
        self.mgr.delete('ea0a4146-fd07-414b-aa5e-dedbeef00101')
        expect = [('DELETE',
                   '/v1/catalog/ea0a4146-fd07-414b-aa5e-dedbeef00101',
                   {}, None)]

        self.assertEqual(expect, self.api.calls)

    def test_list(self):
        """Test list method."""
        catalog = list(self.mgr.list())
        expect = [('GET', '/v1/catalog', {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(4, len(catalog))
        self.assertEqual(CATALOG_ID_104, catalog[0].catalog_id)
        self.assertEqual(CATALOG_ID_103, catalog[1].catalog_id)

    def test_list_filter_catalg_id(self):
        """Test list method by add filter options."""
        kwargs = {'catalog_id': '1'}
        catalog = list(self.mgr.list(kwargs))
        url = '/v1/catalog?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(catalog))
        self.assertEqual(CATALOG_ID_101, catalog[0].catalog_id)

    def test_list_filter_region_id(self):
        """Test list method by add filter options."""
        kwargs = {'region_id': '1'}
        catalog = list(self.mgr.list(kwargs))
        url = '/v1/catalog?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(catalog))
        self.assertEqual(CATALOG_ID_102, catalog[0].catalog_id)

    def test_list_filter_catalog_name(self):
        """Test list method by add filter options."""
        kwargs = {'catalog_name': 'catalog_name1'}
        catalog = list(self.mgr.list(kwargs))
        url = '/v1/catalog?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(catalog))
        self.assertEqual(CATALOG_ID_103, catalog[0].catalog_id)

    def test_list_filter_lifetime(self):
        """Test list method by add filter options."""
        kwargs = {'lifetime': '2015-07-01'}
        catalog = list(self.mgr.list(kwargs))
        url = '/v1/catalog?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(3, len(catalog))
        self.assertEqual(CATALOG_ID_104, catalog[0].catalog_id)
        self.assertEqual(CATALOG_ID_103, catalog[1].catalog_id)
        self.assertEqual(CATALOG_ID_101, catalog[2].catalog_id)

    def test_list_limit(self):
        """Test list method by add limit option."""
        kwargs = {'limit': 1}
        catalog = list(self.mgr.list(kwargs))
        url = '/v1/catalog?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(catalog))
        self.assertEqual(CATALOG_ID_104, catalog[0].catalog_id)

    def test_list_marker(self):
        """Test list method by add marker option."""
        kwargs = {'marker': 3}
        catalog = list(self.mgr.list(kwargs))
        url = '/v1/catalog?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(2, len(catalog))
        self.assertEqual(CATALOG_ID_102, catalog[0].catalog_id)
        self.assertEqual(CATALOG_ID_101, catalog[1].catalog_id)

    def test_list_sort_dir(self):
        """Test list method by add sort-dir option."""
        kwargs = {'sort_dir': 'desc'}
        catalog = list(self.mgr.list(kwargs))
        url = '/v1/catalog?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(2, len(catalog))
        self.assertEqual(CATALOG_ID_104, catalog[0].catalog_id)
        self.assertEqual(CATALOG_ID_101, catalog[1].catalog_id)

    def test_list_sort_key(self):
        """Test list method by add sort-key option."""
        kwargs = {'sort_key': 'catalog_id'}
        catalog = list(self.mgr.list(kwargs))
        url = '/v1/catalog?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(2, len(catalog))
        self.assertEqual(CATALOG_ID_103, catalog[0].catalog_id)
        self.assertEqual(CATALOG_ID_101, catalog[1].catalog_id)

    def test_list_sort(self):
        """Test list method by add sort-key and sort-dir options."""
        kwargs = {'sort_dir': 'desc', 'sort_key': 'catalog_id'}
        catalog = list(self.mgr.list(kwargs))
        url = '/v1/catalog?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(4, len(catalog))
        self.assertEqual(CATALOG_ID_102, catalog[0].catalog_id)
        self.assertEqual(CATALOG_ID_101, catalog[1].catalog_id)
        self.assertEqual(CATALOG_ID_103, catalog[2].catalog_id)
        self.assertEqual(CATALOG_ID_104, catalog[3].catalog_id)

    def test_list_deleted(self):
        """Test list method by add force-show-deleted options."""
        kwargs = {'force_show_deleted': True}
        catalog = list(self.mgr.list(kwargs))
        url = '/v1/catalog?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(4, len(catalog))
        self.assertEqual(CATALOG_ID_101, catalog[0].catalog_id)
        self.assertEqual(CATALOG_ID_102, catalog[1].catalog_id)
        self.assertEqual(CATALOG_ID_103, catalog[2].catalog_id)
        self.assertEqual(CATALOG_ID_104, catalog[3].catalog_id)

    def test_list_all_param(self):
        """Test list method by add all param options."""
        kwargs = {'lifetime': '2015-07-01',
                  'limit': 1,
                  'marker': CATALOG_ID_103,
                  'sort_dir': 'desc',
                  'sort_key': 'catalog_id',
                  'force_show_deleted': True}
        catalog = list(self.mgr.list(kwargs))
        url = '/v1/catalog?' \
            'force_show_deleted=%s&lifetime=%s&limit=%s&' \
            'marker=%s&sort_dir=%s&sort_key=%s' % \
            ('True',
             '2015-07-01',
             '1',
             CATALOG_ID_103,
             'desc',
             'catalog_id')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(catalog))
        self.assertEqual(CATALOG_ID_104, catalog[0].catalog_id)
