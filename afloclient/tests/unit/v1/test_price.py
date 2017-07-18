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

"""Test afloclient/v1/price.py."""

import testtools

from afloclient.tests.unit import utils
from afloclient.v1 import price
from six.moves.urllib import parse

fixtures_catalog_price_data_row1 = \
    {
        "catalog_id": "1",
        "scope": "1",
        "seq_no": "1",
        "price": 10000,
        "lifetime_start": "2015-07-01",
        "lifetime_end": "2015-07-01",
        "created_at": "2015-07-01",
        "updated_at": "2015-07-01",
        "deleted_at": None,
        "deleted": False,
        "expansions": {
            "expansion_key1": "1",
            "expansion_key2": "1",
            "expansion_key3": "1",
            "expansion_key4": "1",
            "expansion_key5": "1",
        },
        "expansions_text": {
            "expansion_text": "1",
        },
    }
fixtures_catalog_price_data_row2 = \
    {
        "catalog_id": "2",
        "scope": "1",
        "seq_no": "2",
        "price": 1000,
        "lifetime_start": "2015-07-03",
        "lifetime_end": "2015-07-03",
        "created_at": "2015-07-02",
        "updated_at": "2015-07-02",
        "deleted_at": None,
        "deleted": False,
        "expansions": {
            "expansion_key1": "1",
            "expansion_key2": "1",
            "expansion_key3": "1",
            "expansion_key4": "1",
            "expansion_key5": "1",
        },
        "expansions_text": {
            "expansion_text": "1",
        },
    }
fixtures_catalog_price_data_row3 = \
    {
        "catalog_id": "3",
        "scope": "2",
        "seq_no": "3",
        "price": 100,
        "lifetime_start": "2015-07-01",
        "lifetime_end": "2015-07-01",
        "created_at": "2015-07-03",
        "updated_at": "2015-07-03",
        "deleted_at": None,
        "deleted": False,
        "expansions": {
            "expansion_key1": "1",
            "expansion_key2": "1",
            "expansion_key3": "1",
            "expansion_key4": "1",
            "expansion_key5": "1",
        },
        "expansions_text": {
            "expansion_text": "1",
        },
    }
fixtures_catalog_price_data_row4 = \
    {
        "catalog_id": "4",
        "scope": "2",
        "seq_no": "4",
        "price": 10,
        "lifetime_start": "2015-07-03",
        "lifetime_end": "2015-07-03",
        "created_at": "2015-07-04",
        "updated_at": "2015-07-04",
        "deleted_at": "2015-07-04",
        "deleted": True,
        "expansions": {
            "expansion_key1": "1",
            "expansion_key2": "1",
            "expansion_key3": "1",
            "expansion_key4": "1",
            "expansion_key5": "1",
        },
        "expansions_text": {
            "expansion_text": "1",
        },
    }
fixtures_catalog_price_data_row5 = \
    {
        "catalog_id": "5",
        "scope": "2",
        "seq_no": "5",
        "price": 5,
        "lifetime_start": "2015-07-01",
        "lifetime_end": "2015-07-01",
        "created_at": "2015-07-05",
        "updated_at": "2015-07-05",
        "deleted_at": None,
        "deleted": False,
        "expansions": {
            "expansion_key1": "1",
            "expansion_key2": "1",
            "expansion_key3": "1",
            "expansion_key4": "1",
            "expansion_key5": "1",
        },
        "expansions_text": {
            "expansion_text": "1",
        },
    }
# from afloclient.v1 import client
#  request fixtures
#    (request url, request header, request parameter).
fixtures = \
    {
        '/v1/catalog/1/price/1': {
            'POST': (
                {},
                {'catalog_price': {
                    'price': 10000
                }},
            ),
        },
        '/v1/catalog/1/price': {
            'GET': (
                {},
                {'catalog_price': [fixtures_catalog_price_data_row5,
                                   fixtures_catalog_price_data_row3,
                                   fixtures_catalog_price_data_row2,
                                   fixtures_catalog_price_data_row1]},
            ),
        },
        # filter parameter start
        '/v1/catalog/1/price?scope=1': {
            'GET': (
                {},
                {'catalog_price': [fixtures_catalog_price_data_row2,
                                   fixtures_catalog_price_data_row1]},
            ),
        },
        '/v1/catalog/1/price?lifetime=2015-07-01': {
            'GET': (
                {},
                {'catalog_price': [fixtures_catalog_price_data_row5,
                                   fixtures_catalog_price_data_row3,
                                   fixtures_catalog_price_data_row1]},
            ),
        },
        # filter parameter end
        '/v1/catalog/1/price?limit=1': {
            'GET': (
                {},
                {'catalog_price': [fixtures_catalog_price_data_row5]},
            ),
        },
        '/v1/catalog/1/price?marker=3': {
            'GET': (
                {},
                {'catalog_price': [fixtures_catalog_price_data_row2,
                                   fixtures_catalog_price_data_row1]},
            ),
        },
        '/v1/catalog/1/price?sort_dir=desc': {
            'GET': (
                {},
                {'catalog_price': [fixtures_catalog_price_data_row5,
                                   fixtures_catalog_price_data_row1]},
            ),
        },
        '/v1/catalog/1/price?sort_key=price': {
            'GET': (
                {},
                {'catalog_price': [fixtures_catalog_price_data_row3,
                                   fixtures_catalog_price_data_row1]},
            ),
        },
        '/v1/catalog/1/price?sort_dir=desc&sort_key=price': {
            'GET': (
                {},
                {'catalog_price': [fixtures_catalog_price_data_row1,
                                   fixtures_catalog_price_data_row2,
                                   fixtures_catalog_price_data_row3,
                                   fixtures_catalog_price_data_row5]},
            ),
        },
        '/v1/catalog/1/price?sort_key=price&sort_dir=desc': {
            'GET': (
                {},
                {'catalog_price': [fixtures_catalog_price_data_row1,
                                   fixtures_catalog_price_data_row2,
                                   fixtures_catalog_price_data_row3,
                                   fixtures_catalog_price_data_row5]},
            ),
        },
        '/v1/catalog/1/price?force_show_deleted=True': {
            'GET': (
                {},
                {'catalog_price': [fixtures_catalog_price_data_row5,
                                   fixtures_catalog_price_data_row4,
                                   fixtures_catalog_price_data_row3,
                                   fixtures_catalog_price_data_row2,
                                   fixtures_catalog_price_data_row1]},
            ),
        },
        '/v1/catalog/1/price'
        '?force_show_deleted=True&lifetime=2015-07-01&limit=1&marker=3'
        '&scope=1&sort_dir=desc&sort_key=price': {
            'GET': (
                {},
                {'catalog_price': [fixtures_catalog_price_data_row1]},
            ),
        },
        '/v1/catalog/1/price/1/seq/1': {
            'GET': (
                {},
                {'catalog_price': fixtures_catalog_price_data_row1},
            ),
            'PATCH': (
                {},
                {'catalog_price': fixtures_catalog_price_data_row1}
            ),
        },
        '/v1/catalog/catalog0-1111-2222-3333-000000000001/price/Default'
        '/seq/a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11': {
            'DELETE': (
                {},
                {}
            ),
        },
    }


class PriceManagerTest(testtools.TestCase):
    """PriceManager Test class."""

    def setUp(self):
        """Setup test class."""
        super(PriceManagerTest, self).setUp()
        self.api = utils.FakeAPI(fixtures)
        self.mgr = price.PriceManager(self.api)

    def test_create(self):
        """Test create method."""
        kwargs = {
            'price': 10000
        }
        expectResponse = {
            'catalog_price': kwargs
        }

        self.mgr.create('1', '1', kwargs)
        expect = [('POST',
                   '/v1/catalog/1/price/1',
                   {},
                   expectResponse.items())]

        self.assertEqual(expect, self.api.calls)

    def test_list(self):
        """Test list method."""
        catalog_price = list(self.mgr.list('1'))
        expect = [('GET', '/v1/catalog/1/price', {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(4, len(catalog_price))
        self.assertEqual('5', catalog_price[0].catalog_id)
        self.assertEqual('2', catalog_price[0].scope)
        self.assertEqual('5', catalog_price[0].seq_no)
        self.assertEqual('3', catalog_price[1].catalog_id)
        self.assertEqual('2', catalog_price[1].scope)
        self.assertEqual('3', catalog_price[1].seq_no)

    def test_list_filter_scope(self):
        """Test list method by add filter options."""
        kwargs = {'scope': '1'}
        catalog_price = list(self.mgr.list('1', kwargs))
        url = '/v1/catalog/1/price?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(2, len(catalog_price))
        self.assertEqual('2', catalog_price[0].catalog_id)
        self.assertEqual('1', catalog_price[0].scope)
        self.assertEqual('2', catalog_price[0].seq_no)
        self.assertEqual('1', catalog_price[1].catalog_id)
        self.assertEqual('1', catalog_price[1].scope)
        self.assertEqual('1', catalog_price[1].seq_no)

    def test_list_filter_lifetime(self):
        """Test list method by add filter options."""
        kwargs = {'lifetime': '2015-07-01'}
        catalog_price = list(self.mgr.list('1', kwargs))
        url = '/v1/catalog/1/price?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(3, len(catalog_price))
        self.assertEqual('5', catalog_price[0].catalog_id)
        self.assertEqual('2', catalog_price[0].scope)
        self.assertEqual('5', catalog_price[0].seq_no)
        self.assertEqual('3', catalog_price[1].catalog_id)
        self.assertEqual('2', catalog_price[1].scope)
        self.assertEqual('3', catalog_price[1].seq_no)

    def test_list_limit(self):
        """Test list method by add limit option."""
        kwargs = {'limit': 1}
        catalog_price = list(self.mgr.list('1', kwargs))
        url = '/v1/catalog/1/price?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(catalog_price))
        self.assertEqual('5', catalog_price[0].catalog_id)
        self.assertEqual('2', catalog_price[0].scope)
        self.assertEqual('5', catalog_price[0].seq_no)

    def test_list_marker(self):
        """Test list method by add marker option."""
        kwargs = {'marker': '3'}
        catalog_price = list(self.mgr.list('1', kwargs))
        url = '/v1/catalog/1/price?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(2, len(catalog_price))
        self.assertEqual('2', catalog_price[0].catalog_id)
        self.assertEqual('1', catalog_price[0].scope)
        self.assertEqual('2', catalog_price[0].seq_no)
        self.assertEqual('1', catalog_price[1].catalog_id)
        self.assertEqual('1', catalog_price[1].scope)
        self.assertEqual('1', catalog_price[1].seq_no)

    def test_list_sort_dir(self):
        """Test list method by add sort-dir option."""
        kwargs = {'sort_dir': 'desc'}
        catalog_price = list(self.mgr.list('1', kwargs))
        url = '/v1/catalog/1/price?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(2, len(catalog_price))
        self.assertEqual('5', catalog_price[0].catalog_id)
        self.assertEqual('2', catalog_price[0].scope)
        self.assertEqual('5', catalog_price[0].seq_no)
        self.assertEqual('1', catalog_price[1].catalog_id)
        self.assertEqual('1', catalog_price[1].scope)
        self.assertEqual('1', catalog_price[1].seq_no)

    def test_list_sort_key(self):
        """Test list method by add sort-key option."""
        kwargs = {'sort_key': 'price'}
        catalog_price = list(self.mgr.list('1', kwargs))
        url = '/v1/catalog/1/price?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(2, len(catalog_price))
        self.assertEqual('3', catalog_price[0].catalog_id)
        self.assertEqual('2', catalog_price[0].scope)
        self.assertEqual('3', catalog_price[0].seq_no)
        self.assertEqual('1', catalog_price[1].catalog_id)
        self.assertEqual('1', catalog_price[1].scope)
        self.assertEqual('1', catalog_price[1].seq_no)

    def test_list_sort(self):
        """Test list method by add sort-key and sort-dir options."""
        kwargs = {'sort_dir': 'desc', 'sort_key': 'price'}
        catalog_price = list(self.mgr.list('1', kwargs))
        url = '/v1/catalog/1/price?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(4, len(catalog_price))
        self.assertEqual('1', catalog_price[0].catalog_id)
        self.assertEqual('1', catalog_price[0].scope)
        self.assertEqual('1', catalog_price[0].seq_no)
        self.assertEqual('2', catalog_price[1].catalog_id)
        self.assertEqual('1', catalog_price[1].scope)
        self.assertEqual('2', catalog_price[1].seq_no)

    def test_list_deleted(self):
        """Test list method by add force-show-deleted options."""
        kwargs = {'force_show_deleted': True}
        catalog_price = list(self.mgr.list('1', kwargs))
        url = '/v1/catalog/1/price?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(5, len(catalog_price))
        self.assertEqual('5', catalog_price[0].catalog_id)
        self.assertEqual('2', catalog_price[0].scope)
        self.assertEqual('5', catalog_price[0].seq_no)
        self.assertEqual('4', catalog_price[1].catalog_id)
        self.assertEqual('2', catalog_price[1].scope)
        self.assertEqual('4', catalog_price[1].seq_no)

    def test_list_all_param(self):
        """Test list method by add all param options."""
        kwargs = {'scope': '1',
                  'lifetime': '2015-07-01',
                  'limit': 1,
                  'marker': '3',
                  'sort_dir': 'desc',
                  'sort_key': 'price',
                  'force_show_deleted': True}
        catalog_price = list(self.mgr.list('1', kwargs))
        url = '/v1/catalog/1/price?' \
            'force_show_deleted=%s&lifetime=%s&limit=%s&' \
            'marker=%s&scope=%s&sort_dir=%s&sort_key=%s' % \
            ('True',
             '2015-07-01',
             '1',
             '3',
             '1',
             'desc',
             'price')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(catalog_price))
        self.assertEqual('1', catalog_price[0].catalog_id)
        self.assertEqual('1', catalog_price[0].scope)
        self.assertEqual('1', catalog_price[0].seq_no)

    def test_get(self):
        """Test get method."""
        price = self.mgr.get('1', '1', '1')
        url = '/v1/catalog/%s/price/%s/seq/%s' % ('1', '1', '1')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertIsNotNone(price)
        self.assertEqual(price.catalog_id, '1')
        self.assertEqual(price.scope, '1')
        self.assertEqual(price.seq_no, '1')
        self.assertEqual(price.price, 10000)
        self.assertEqual(price.lifetime_start, '2015-07-01')
        self.assertEqual(price.lifetime_end, '2015-07-01')
        self.assertIsNotNone(price.created_at)
        self.assertIsNotNone(price.updated_at)
        self.assertIsNone(price.deleted_at)
        self.assertEqual(price.deleted, False)
        self.assertEqual(price.expansions['expansion_key1'], '1')
        self.assertEqual(price.expansions['expansion_key2'], '1')
        self.assertEqual(price.expansions['expansion_key3'], '1')
        self.assertEqual(price.expansions['expansion_key4'], '1')
        self.assertEqual(price.expansions['expansion_key5'], '1')
        self.assertEqual(price.expansions_text['expansion_text'], '1')

    def test_update(self):
        kwargs = {'price': '10000',
                  'lifetime_start': '2015-07-01',
                  'lifetime_end': '2015-07-01',
                  'expansions': {'expansion_key1': '1',
                                 'expansion_key2': '1',
                                 'expansion_key3': '1',
                                 'expansion_key4': '1',
                                 'expansion_key5': '1'},
                  'expansions_text': {'expansion_text': '1'}}
        expectResponse = {
            'catalog_price': kwargs
        }
        catalog_price = self.mgr.update('1', '1', '1', kwargs)
        url = '/v1/catalog/1/price/1/seq/1'
        expect = [('PATCH', url, {}, expectResponse.items())]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual('1', catalog_price.catalog_id)
        self.assertEqual('1', catalog_price.scope)
        self.assertEqual('1', catalog_price.seq_no)

    def test_delete(self):
        """Test delete method."""
        self.mgr.delete('catalog0-1111-2222-3333-000000000001',
                        'Default',
                        'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11')
        expect = [('DELETE',
                   '/v1/catalog/catalog0-1111-2222-3333-000000000001'
                   '/price/Default/seq/a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
                   {}, None)]

        self.assertEqual(expect, self.api.calls)
