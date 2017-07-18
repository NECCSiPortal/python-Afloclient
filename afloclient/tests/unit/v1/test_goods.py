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

"""Test afloclient/v1/goods.py."""

import testtools

from afloclient.tests.unit import utils
from afloclient.v1 import goods
from datetime import datetime
from six.moves.urllib import parse

goods_101 = \
    {
        'goods_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
        'goods_name': 'goods_name_101',
        'created_at': datetime(2015, 7, 30, 1, 2, 3, 4),
        'updated_at': datetime(2015, 7, 30, 1, 2, 3, 4),
        'deleted_at': None,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5',
                       },
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

fixtures_goods_data_row1 = \
    {
        "goods_id": "1",
        "region_id": "1",
        "goods_name": "1",
        "created_at": "2015-07-03",
        "updated_at": "2015-07-03",
        "deleted_at": "2015-07-03",
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
fixtures_goods_data_row2 = \
    {
        "goods_id": "2",
        "region_id": "2",
        "goods_name": "2",
        "created_at": "2015-07-03",
        "updated_at": "2015-07-03",
        "deleted_at": "2015-07-03",
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
fixtures_goods_data_row3 = \
    {
        "goods_id": "3",
        "region_id": "1",
        "goods_name": "3",
        "created_at": "2015-07-03",
        "updated_at": "2015-07-03",
        "deleted_at": "2015-07-03",
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
fixtures_goods_data_row4 = \
    {
        "goods_id": "4",
        "region_id": "2",
        "goods_name": "4",
        "created_at": "2015-07-03",
        "updated_at": "2015-07-03",
        "deleted_at": "2015-07-03",
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
fixtures_goods_data_row5 = \
    {
        "goods_id": "5",
        "region_id": "1",
        "goods_name": "5",
        "created_at": "2015-07-03",
        "updated_at": "2015-07-03",
        "deleted_at": "2015-07-03",
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
fixtures_goods_data_row6 = \
    {
        "goods_id": "ea0a4146-fd07-414b-aa5e-dedbeef00101",
        "region_id": "1",
        "goods_name": "1",
        "created_at": "2015-07-01T00:00:00",
        "updated_at": "2015-07-02T00:00:00",
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
        '/v1/goods': {
            'POST': (
                {},
                {'goods': {
                    'goods_name': 'testgoods'
                }
                },
            ),
            'GET': (
                {},
                {'goods': [fixtures_goods_data_row4,
                           fixtures_goods_data_row3,
                           fixtures_goods_data_row2,
                           fixtures_goods_data_row1]}
            ),
        },
        '/v1/goods/ea0a4146-fd07-414b-aa5e-dedbeef00001': {
            'PATCH': (
                {},
                {'goods': goods_101},
            ),
            'DELETE': (
                {},
                {},
            ),
        },
        '/v1/goods/ea0a4146-fd07-414b-aa5e-dedbeef00101': {
            'GET': (
                {},
                {'goods': fixtures_goods_data_row6}
            ),
        },
        '/v1/goods?region_id=1': {
            'GET': (
                {},
                {'goods': [fixtures_goods_data_row3,
                           fixtures_goods_data_row1]}
            ),
        },
        '/v1/goods?limit=1': {
            'GET': (
                {},
                {'goods': [fixtures_goods_data_row4]}
            ),
        },
        '/v1/goods?marker=3': {
            'GET': (
                {},
                {'goods': [fixtures_goods_data_row2,
                           fixtures_goods_data_row1]}
            ),
        },
        '/v1/goods?sort_dir=desc': {
            'GET': (
                {},
                {'goods': [fixtures_goods_data_row3,
                           fixtures_goods_data_row1,
                           fixtures_goods_data_row4,
                           fixtures_goods_data_row2]}
            ),
        },
        '/v1/goods?sort_key=goods_id': {
            'GET': (
                {},
                {'goods': [fixtures_goods_data_row1,
                           fixtures_goods_data_row3,
                           fixtures_goods_data_row2,
                           fixtures_goods_data_row4]}
            ),
        },
        '/v1/goods?sort_dir=asc&sort_key=goods_id': {
            'GET': (
                {},
                {'goods': [fixtures_goods_data_row1,
                           fixtures_goods_data_row2,
                           fixtures_goods_data_row3,
                           fixtures_goods_data_row4]}
            ),
        },
        '/v1/goods?sort_key=goods_id&sort_dir=asc': {
            'GET': (
                {},
                {'goods': [fixtures_goods_data_row1,
                           fixtures_goods_data_row2,
                           fixtures_goods_data_row3,
                           fixtures_goods_data_row4]}
            ),
        },
        '/v1/goods?force_show_deleted=True': {
            'GET': (
                {},
                {'goods': [fixtures_goods_data_row5,
                           fixtures_goods_data_row4,
                           fixtures_goods_data_row3,
                           fixtures_goods_data_row2,
                           fixtures_goods_data_row1]}
            ),
        },
        '/v1/goods?force_show_deleted=True': {
            'GET': (
                {},
                {'goods': [fixtures_goods_data_row5,
                           fixtures_goods_data_row4,
                           fixtures_goods_data_row3,
                           fixtures_goods_data_row2,
                           fixtures_goods_data_row1]}
            ),
        },
        '/v1/goods'
        '?force_show_deleted=True&limit=2&marker=1'
        '&region_id=1&sort_dir=asc&sort_key=goods_id': {
            'GET': (
                {},
                {'goods': [fixtures_goods_data_row3,
                           fixtures_goods_data_row5]}
            ),
        },
    }


class GoodsManagerTest(testtools.TestCase):
    """GoodsManager Test class."""

    def setUp(self):
        """Setup test class."""
        super(GoodsManagerTest, self).setUp()
        self.api = utils.FakeAPI(fixtures)
        self.mgr = goods.GoodsManager(self.api)

    def test_create(self):
        """Test create method."""
        kwargs = {
            'goods_name': 'testgoods'
        }
        expectResponse = {
            'goods': kwargs
        }

        self.mgr.create(kwargs)
        expect = [('POST', '/v1/goods', {}, expectResponse.items())]

        self.assertEqual(expect, self.api.calls)

    def test_update(self):
        expectResponse = {'goods': goods_101}

        self.mgr.update('ea0a4146-fd07-414b-aa5e-dedbeef00001',
                        goods_101)
        expect = [('PATCH',
                   '/v1/goods/ea0a4146-fd07-414b-aa5e-dedbeef00001',
                   {}, expectResponse.items())]
        self.assertEqual(expect, self.api.calls)

    def test_delete(self):
        """Test delete method."""
        self.mgr.delete('ea0a4146-fd07-414b-aa5e-dedbeef00001')
        expect = [('DELETE',
                   '/v1/goods/ea0a4146-fd07-414b-aa5e-dedbeef00001',
                   {}, None)]

        self.assertEqual(expect, self.api.calls)

    def test_list_no_params(self):
        goods = list(self.mgr.list())
        expect = [('GET', '/v1/goods', {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(goods), 4)
        self.assertEqual(goods[0].goods_id, '4')
        self.assertEqual(goods[1].goods_id, '3')
        self.assertEqual(goods[2].goods_id, '2')
        self.assertEqual(goods[3].goods_id, '1')

    def test_list_with_region_id(self):
        kwargs = {'region_id': '1'}
        goods = list(self.mgr.list(kwargs))
        url = '/v1/goods?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(goods), 2)
        self.assertEqual(goods[0].goods_id, '3')
        self.assertEqual(goods[1].goods_id, '1')

    def test_list_with_limit(self):
        kwargs = {'limit': '1'}
        goods = list(self.mgr.list(kwargs))
        url = '/v1/goods?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(goods), 1)
        self.assertEqual(goods[0].goods_id, '4')

    def test_list_with_marker(self):
        kwargs = {'marker': '3'}
        goods = list(self.mgr.list(kwargs))
        url = '/v1/goods?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(goods), 2)
        self.assertEqual(goods[0].goods_id, '2')
        self.assertEqual(goods[1].goods_id, '1')

    def test_list_with_sort_key(self):
        kwargs = {'sort_key': 'goods_id'}
        goods = list(self.mgr.list(kwargs))
        url = '/v1/goods?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(goods), 4)
        self.assertEqual(goods[0].goods_id, '1')
        self.assertEqual(goods[1].goods_id, '3')
        self.assertEqual(goods[2].goods_id, '2')
        self.assertEqual(goods[3].goods_id, '4')

    def test_list_with_sort_dir(self):
        kwargs = {'sort_dir': 'desc'}
        goods = list(self.mgr.list(kwargs))
        url = '/v1/goods?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(goods), 4)
        self.assertEqual(goods[0].goods_id, '3')
        self.assertEqual(goods[1].goods_id, '1')
        self.assertEqual(goods[2].goods_id, '4')
        self.assertEqual(goods[3].goods_id, '2')

    def test_list_with_sort_key_dir(self):
        kwargs = {'sort_key': 'goods_id', 'sort_dir': 'asc'}
        goods = list(self.mgr.list(kwargs))
        url = '/v1/goods?' \
            'sort_dir=%s&sort_key=%s' % \
            ('asc',
             'goods_id')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(goods), 4)
        self.assertEqual(goods[0].goods_id, '1')
        self.assertEqual(goods[1].goods_id, '2')
        self.assertEqual(goods[2].goods_id, '3')
        self.assertEqual(goods[3].goods_id, '4')

    def test_list_with_deleted(self):
        kwargs = {'force_show_deleted': True}
        goods = list(self.mgr.list(kwargs))
        url = '/v1/goods?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(goods), 5)
        self.assertEqual(goods[0].goods_id, '5')
        self.assertEqual(goods[1].goods_id, '4')
        self.assertEqual(goods[2].goods_id, '3')
        self.assertEqual(goods[3].goods_id, '2')
        self.assertEqual(goods[4].goods_id, '1')

    def test_list_with_all_params(self):
        kwargs = {'region_id': '1',
                  'limit': '2',
                  'marker': '1',
                  'sort_key': 'goods_id',
                  'sort_dir': 'asc',
                  'force_show_deleted': True}
        goods = list(self.mgr.list(kwargs))
        url = '/v1/goods?' \
            'force_show_deleted=%s&limit=%s&marker=%s&' \
            'region_id=%s&sort_dir=%s&sort_key=%s' % \
            ('True',
             '2',
             '1',
             '1',
             'asc',
             'goods_id')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(goods), 2)
        self.assertEqual(goods[0].goods_id, '3')
        self.assertEqual(goods[1].goods_id, '5')

    def test_get(self):
        """Test get method."""
        goods = self.mgr.get('ea0a4146-fd07-414b-aa5e-dedbeef00101')
        url = '/v1/goods/%s' % ('ea0a4146-fd07-414b-aa5e-dedbeef00101')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertIsNotNone(goods)
        self.assertEqual(goods.goods_id,
                         'ea0a4146-fd07-414b-aa5e-dedbeef00101')
        self.assertEqual(goods.region_id, '1')
        self.assertEqual(goods.goods_name, '1')
        self.assertEqual(goods.created_at, '2015-07-01T00:00:00')
        self.assertEqual(goods.updated_at, '2015-07-02T00:00:00')
        self.assertIsNone(goods.deleted_at)
        self.assertEqual(goods.deleted, False)
        self.assertEqual(goods.expansions['expansion_key1'], '1')
        self.assertEqual(goods.expansions['expansion_key2'], '1')
        self.assertEqual(goods.expansions['expansion_key3'], '1')
        self.assertEqual(goods.expansions['expansion_key4'], '1')
        self.assertEqual(goods.expansions['expansion_key5'], '1')
        self.assertEqual(goods.expansions_text['expansion_text'], '1')
