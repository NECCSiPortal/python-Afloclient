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

"""Test afloclient/v1/catalog_contents.py."""

import testtools

from afloclient.tests.unit import utils
from afloclient.v1 import catalog_contents
from datetime import datetime
from six.moves.urllib import parse

CATALOG_ID_101 = 'ea0a4146-fd07-414b-aa5e-dedbeef00101'
CATALOG_ID_102 = 'ea0a4146-fd07-414b-aa5e-dedbeef00102'
CATALOG_ID_103 = 'ea0a4146-fd07-414b-aa5e-dedbeef00103'

catalog_contents_list_101 = \
    {
        'catalog_id': CATALOG_ID_101,
        'seq_no': 'seq_no_101',
        'goods_id': 'goods_id_101',
        'goods_num': 101,
        'created_at': datetime.now(),
        'updated_at': None,
        'deleted_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

catalog_contents_list_102 = \
    {
        'catalog_id': CATALOG_ID_101,
        'seq_no': 'seq_no_102',
        'goods_id': 'goods_id_101',
        'goods_num': 102,
        'created_at': datetime.now(),
        'updated_at': None,
        'deleted_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

catalog_contents_list_103 = \
    {
        'catalog_id': CATALOG_ID_101,
        'seq_no': 'seq_no_103',
        'goods_id': 'goods_id_102',
        'goods_num': 101,
        'created_at': datetime.now(),
        'updated_at': None,
        'deleted_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

catalog_contents_list_104 = \
    {
        'catalog_id': CATALOG_ID_101,
        'seq_no': 'seq_no_104',
        'goods_id': 'goods_id_102',
        'goods_num': 102,
        'created_at': datetime.now(),
        'updated_at': None,
        'deleted_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }


catalog_contents_list_105 = \
    {
        'catalog_id': CATALOG_ID_101,
        'seq_no': 'seq_no_105',
        'goods_id': 'goods_id_103',
        'goods_num': 103,
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'deleted_at': datetime.now(),
        'deleted': True,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

catalog_contents_list_106 = \
    {
        'catalog_id': CATALOG_ID_102,
        'seq_no': 'seq_no_106',
        'goods_id': 'goods_id_104',
        'goods_num': 104,
        'created_at': datetime.now(),
        'updated_at': None,
        'deleted_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

catalog_contents_update_101 = \
    {
        'catalog_id': CATALOG_ID_101,
        'seq_no': 'seq_no_106',
        'goods_id': 'goods_id_104',
        'goods_num': 1,
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

# from afloclient.v1 import client
#  request fixtures
#    (request url, request header, request parameter).
fixtures = \
    {
        '/v1/catalog/1/contents': {
            'POST': (
                {},
                {'catalog_contents': {
                    'goods_id': 'goods_001',
                    'godds_num': '2'
                }},
            ),
        },
        '/v1/catalog/ea0a4146-fd07-414b-aa5e-dedbeef00101/contents': {
            'GET': (
                {},
                {'catalog_contents': [catalog_contents_list_104,
                                      catalog_contents_list_103,
                                      catalog_contents_list_102,
                                      catalog_contents_list_101]},
            )
        },
        '/v1/catalog/ea0a4146-fd07-414b-aa5e-dedbeef00101/contents?limit=3': {
            'GET': (
                {},
                {'catalog_contents': [catalog_contents_list_104,
                                      catalog_contents_list_103,
                                      catalog_contents_list_102]},
            ),
        },
        '/v1/catalog/ea0a4146-fd07-414b-aa5e-dedbeef00101/contents'
        '?marker=seq_no_105': {
            'GET': (
                {},
                {'catalog_contents': [catalog_contents_list_104,
                                      catalog_contents_list_103,
                                      catalog_contents_list_102,
                                      catalog_contents_list_101]},
            ),
        },
        '/v1/catalog/ea0a4146-fd07-414b-aa5e-dedbeef00101/contents'
        '?sort_key=goods_id': {
            'GET': (
                {},
                {'catalog_contents': [catalog_contents_list_104,
                                      catalog_contents_list_103,
                                      catalog_contents_list_102,
                                      catalog_contents_list_101]},
            ),
        },
        '/v1/catalog/ea0a4146-fd07-414b-aa5e-dedbeef00101/contents'
        '?sort_dir=asc': {
            'GET': (
                {},
                {'catalog_contents': [catalog_contents_list_101,
                                      catalog_contents_list_102,
                                      catalog_contents_list_103,
                                      catalog_contents_list_104]},
            ),
        },
        '/v1/catalog/ea0a4146-fd07-414b-aa5e-dedbeef00101/contents'
        '?sort_dir=asc%2Cdesc'
        '&sort_key=goods_id%2Cgoods_num': {
            'GET': (
                {},
                {'catalog_contents': [catalog_contents_list_102,
                                      catalog_contents_list_101,
                                      catalog_contents_list_104,
                                      catalog_contents_list_103]},
            ),
        },
        '/v1/catalog/ea0a4146-fd07-414b-aa5e-dedbeef00101/contents'
        '?sort_dir=asc%2Cdesc&sort_key=goods_id': {
            'GET': (
                {},
                {'catalog_contents': [catalog_contents_list_102,
                                      catalog_contents_list_101,
                                      catalog_contents_list_104,
                                      catalog_contents_list_103]},
            ),
        },
        '/v1/catalog/ea0a4146-fd07-414b-aa5e-dedbeef00101/contents'
        '?sort_dir=asc&sort_key=goods_id%2Cgoods_num': {
            'GET': (
                {},
                {'catalog_contents': [catalog_contents_list_102,
                                      catalog_contents_list_101,
                                      catalog_contents_list_104,
                                      catalog_contents_list_103]},
            ),
        },
        '/v1/catalog/ea0a4146-fd07-414b-aa5e-dedbeef00101/contents'
        '?force_show_deleted=true': {
            'GET': (
                {},
                {'catalog_contents': [catalog_contents_list_105,
                                      catalog_contents_list_104,
                                      catalog_contents_list_103,
                                      catalog_contents_list_102,
                                      catalog_contents_list_101]},
            ),
        },
        '/v1/catalog/ea0a4146-fd07-414b-aa5e-dedbeef00101/contents'
        '?force_show_deleted=false&limit=1'
        '&marker=seq_no_101'
        '&sort_dir=asc%2Cdesc&sort_key=goods_id%2Cgoods_num': {
            'GET': (
                {},
                {'catalog_contents': [catalog_contents_list_104]},
            ),
        },
        '/v1/catalog/ea0a4146-fd07-414b-aa5e-dedbeef00103/contents': {
            'GET': (
                {},
                {'catalog_contents': []},
            ),
        },
        '/v1/catalog/ea0a4146-fd07-414b-aa5e-dedbeef00102'
        '/contents/seq_no_106': {
            'GET': (
                {},
                {'catalog_contents': catalog_contents_list_106},
            ),
        },
        '/v1/catalog/ea0a4146-fd07-414b-aa5e-dedbeef00101/contents/seq_no_106':
        {
            'PATCH': (
                {},
                {'catalog_contents': catalog_contents_update_101},
            ),
        },
        '/v1/catalog/ea0a4146-fd07-414b-aa5e-dedbeef00101/contents'
        '/a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11':
        {
            'DELETE': (
                {},
                {},
            ),
        },
    }


class CatalogContentsManagerTest(testtools.TestCase):
    """CatalogContentsManager Test class."""

    def setUp(self):
        """Setup test class."""
        super(CatalogContentsManagerTest, self).setUp()
        self.api = utils.FakeAPI(fixtures)
        self.mgr = catalog_contents.CatalogContentsManager(self.api)

    def test_create(self):
        """Test create method."""
        kwargs = {
            'goods_id': 'goods_001',
            'goods_num': '2'
        }
        expectResponse = {
            'catalog_contents': kwargs
        }

        self.mgr.create('1', kwargs)
        expect = [('POST',
                   '/v1/catalog/1/contents',
                   {},
                   expectResponse.items())]

        self.assertEqual(expect, self.api.calls)

    def test_list_no_params(self):
        """Test list api.
        Test with no params.
        """
        res_objs = list(self.mgr.list(CATALOG_ID_101))
        url = '/v1/catalog/%s/contents' % CATALOG_ID_101
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)

        self.assertEqual(len(res_objs), 4)
        self.assertEqual(res_objs[0].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[0].seq_no, 'seq_no_104')
        self.assertEqual(res_objs[1].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[1].seq_no, 'seq_no_103')
        self.assertEqual(res_objs[2].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[2].seq_no, 'seq_no_102')
        self.assertEqual(res_objs[3].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[3].seq_no, 'seq_no_101')

    def test_list_with_limit(self):
        """Test list api.
        Test with limit.
        """
        kwargs = {'limit': 3}
        res_objs = list(self.mgr.list(CATALOG_ID_101, kwargs))
        url = '/v1/catalog/%s/contents?' % CATALOG_ID_101
        url = url + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)

        self.assertEqual(len(res_objs), 3)
        self.assertEqual(res_objs[0].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[0].seq_no, 'seq_no_104')
        self.assertEqual(res_objs[1].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[1].seq_no, 'seq_no_103')
        self.assertEqual(res_objs[2].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[2].seq_no, 'seq_no_102')

    def test_list_with_marker(self):
        """Test list api.
        Test with marker.
        """
        kwargs = {'marker': 'seq_no_105'}
        res_objs = list(self.mgr.list(CATALOG_ID_101, kwargs))
        url = '/v1/catalog/%s/contents?' % CATALOG_ID_101
        url = url + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(res_objs), 4)
        self.assertEqual(res_objs[0].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[0].seq_no, 'seq_no_104')
        self.assertEqual(res_objs[1].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[1].seq_no, 'seq_no_103')
        self.assertEqual(res_objs[2].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[2].seq_no, 'seq_no_102')
        self.assertEqual(res_objs[3].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[3].seq_no, 'seq_no_101')

    def test_list_with_sort_key(self):
        """Test list api.
        Test with sort key.
        """
        kwargs = {'sort_key': 'goods_id'}
        res_objs = list(self.mgr.list(CATALOG_ID_101, kwargs))
        url = '/v1/catalog/%s/contents?' % CATALOG_ID_101
        url = url + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(res_objs), 4)
        self.assertEqual(res_objs[0].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[0].seq_no, 'seq_no_104')
        self.assertEqual(res_objs[1].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[1].seq_no, 'seq_no_103')
        self.assertEqual(res_objs[2].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[2].seq_no, 'seq_no_102')
        self.assertEqual(res_objs[3].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[3].seq_no, 'seq_no_101')

    def test_list_with_sort_dir(self):
        """Test list api.
        Test with sort dir.
        """
        kwargs = {'sort_dir': 'asc'}
        res_objs = list(self.mgr.list(CATALOG_ID_101, kwargs))
        url = '/v1/catalog/%s/contents?' % CATALOG_ID_101
        url = url + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(res_objs), 4)
        self.assertEqual(res_objs[0].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[0].seq_no, 'seq_no_101')
        self.assertEqual(res_objs[1].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[1].seq_no, 'seq_no_102')
        self.assertEqual(res_objs[2].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[2].seq_no, 'seq_no_103')
        self.assertEqual(res_objs[3].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[3].seq_no, 'seq_no_104')

    def test_list_with_sort_key_dir(self):
        """Test list api.
        Test with sort key and sort dir.
        """
        kwargs = {'sort_dir': 'asc,desc',
                  'sort_key': 'goods_id,goods_num'}
        res_objs = list(self.mgr.list(CATALOG_ID_101, kwargs))
        url = '/v1/catalog/%s/contents?' % CATALOG_ID_101
        url = url + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(res_objs), 4)
        self.assertEqual(res_objs[0].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[0].seq_no, 'seq_no_102')
        self.assertEqual(res_objs[1].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[1].seq_no, 'seq_no_101')
        self.assertEqual(res_objs[2].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[2].seq_no, 'seq_no_104')
        self.assertEqual(res_objs[3].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[3].seq_no, 'seq_no_103')

    def test_list_with_sort_key_less_than_sort_dir(self):
        """Test list api.
        Test with sort key and sort dir, where key is less than dir.
        """
        kwargs = {'sort_dir': 'asc,desc',
                  'sort_key': 'goods_id'}

        res_objs = list(self.mgr.list(CATALOG_ID_101, kwargs))
        url = '/v1/catalog/%s/contents?' % CATALOG_ID_101
        url = url + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(res_objs), 4)
        self.assertEqual(res_objs[0].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[0].seq_no, 'seq_no_102')
        self.assertEqual(res_objs[1].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[1].seq_no, 'seq_no_101')
        self.assertEqual(res_objs[2].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[2].seq_no, 'seq_no_104')
        self.assertEqual(res_objs[3].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[3].seq_no, 'seq_no_103')

    def test_list_with_sort_key_more_than_sort_dir(self):
        """Test list api.
        Test with sort key and sort dir, where key is more than dir.
        """
        kwargs = {'sort_dir': 'asc',
                  'sort_key': 'goods_id,goods_num'}
        res_objs = list(self.mgr.list(CATALOG_ID_101, kwargs))
        url = '/v1/catalog/%s/contents?' % CATALOG_ID_101
        url = url + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(res_objs), 4)
        self.assertEqual(res_objs[0].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[0].seq_no, 'seq_no_102')
        self.assertEqual(res_objs[1].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[1].seq_no, 'seq_no_101')
        self.assertEqual(res_objs[2].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[2].seq_no, 'seq_no_104')
        self.assertEqual(res_objs[3].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[3].seq_no, 'seq_no_103')

    def test_list_with_deleted(self):
        """Test list api.
        Test with deleted.
        """
        kwargs = {'force_show_deleted': 'true'}
        res_objs = list(self.mgr.list(CATALOG_ID_101, kwargs))
        url = '/v1/catalog/%s/contents?' % CATALOG_ID_101
        url = url + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(res_objs), 5)
        self.assertEqual(res_objs[0].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[0].seq_no, 'seq_no_105')
        self.assertEqual(res_objs[1].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[1].seq_no, 'seq_no_104')
        self.assertEqual(res_objs[2].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[2].seq_no, 'seq_no_103')
        self.assertEqual(res_objs[3].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[3].seq_no, 'seq_no_102')
        self.assertEqual(res_objs[4].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[4].seq_no, 'seq_no_101')

    def test_list_with_all_params(self):
        """Test list api.
        Test with all parameters.
        """
        kwargs = {'limit': 1,
                  'marker': 'seq_no_101',
                  'sort_dir': 'asc,desc',
                  'sort_key': 'goods_id,goods_num',
                  'force_show_deleted': 'false'}

        res_objs = list(self.mgr.list(CATALOG_ID_101, kwargs))
        url = '/v1/catalog/%s/contents' \
            '?force_show_deleted=%s&limit=%s&marker=%s' \
            '&sort_dir=%s&sort_key=%s' % \
            (CATALOG_ID_101,
             'false',
             '1',
             'seq_no_101',
             'asc%2Cdesc',
             'goods_id%2Cgoods_num')
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(res_objs), 1)
        self.assertEqual(res_objs[0].catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs[0].seq_no, 'seq_no_104')

    def test_list_no_result(self):
        """Test list api.
        Test if the retrieved result is of 0.
        """
        res_objs = list(self.mgr.list(CATALOG_ID_103))
        url = '/v1/catalog/%s/contents' % CATALOG_ID_103
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(res_objs), 0)

    def test_get(self):
        res_objs = self.mgr.get(CATALOG_ID_102, 'seq_no_106')
        url = '/v1/catalog/%s/contents/%s' % (CATALOG_ID_102, 'seq_no_106')
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertIsNotNone(res_objs)
        self.assertEqual(res_objs.catalog_id, CATALOG_ID_102)
        self.assertEqual(res_objs.seq_no, 'seq_no_106')
        self.assertEqual(res_objs.goods_id, 'goods_id_104')
        self.assertEqual(res_objs.goods_num, 104)
        self.assertIsNotNone(res_objs.created_at)
        self.assertIsNone(res_objs.updated_at)
        self.assertIsNone(res_objs.deleted_at)
        self.assertEqual(res_objs.deleted, False)
        self.assertEqual(res_objs.expansions['expansion_key1'],
                         'expansion_key1')
        self.assertEqual(res_objs.expansions['expansion_key2'],
                         'expansion_key2')
        self.assertEqual(res_objs.expansions['expansion_key3'],
                         'expansion_key3')
        self.assertEqual(res_objs.expansions['expansion_key4'],
                         'expansion_key4')
        self.assertEqual(res_objs.expansions['expansion_key5'],
                         'expansion_key5')
        self.assertEqual(res_objs.expansions_text['expansion_text'],
                         'expansion_text')

    def test_update(self):
        expectResponse = {'catalog_contents': catalog_contents_update_101}

        self.mgr.update(CATALOG_ID_101,
                        'seq_no_106',
                        catalog_contents_update_101)
        expect = [('PATCH',
                   '/v1/catalog/ea0a4146-fd07-414b-aa5e-dedbeef00101' +
                   '/contents/seq_no_106',
                   {}, expectResponse.items())]
        self.assertEqual(expect, self.api.calls)

    def test_delete(self):
        """Test delete method."""
        self.mgr.delete(CATALOG_ID_101, 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11')
        expect = [('DELETE',
                   '/v1/catalog/ea0a4146-fd07-414b-aa5e-dedbeef00101' +
                   '/contents/a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
                   {}, None)]

        self.assertEqual(expect, self.api.calls)
