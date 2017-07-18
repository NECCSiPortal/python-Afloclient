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

"""Test afloclient/v1/catalog_scope.py."""

import testtools

from afloclient.tests.unit import utils
from afloclient.v1 import catalog_scope
from datetime import datetime
from six.moves.urllib import parse

ID_101 = 'id0a4146-fd07-414b-aa5e-dedbeef00101'
ID_102 = 'id0a4146-fd07-414b-aa5e-dedbeef00102'
ID_103 = 'id0a4146-fd07-414b-aa5e-dedbeef00103'
ID_104 = 'id0a4146-fd07-414b-aa5e-dedbeef00104'
ID_105 = 'id0a4146-fd07-414b-aa5e-dedbeef00105'
ID_106 = 'id0a4146-fd07-414b-aa5e-dedbeef00106'
ID_107 = 'id0a4146-fd07-414b-aa5e-dedbeef00107'
ID_108 = 'id0a4146-fd07-414b-aa5e-dedbeef00108'

CATALOG_ID_101 = 'ea0a4146-fd07-414b-aa5e-dedbeef00101'
CATALOG_ID_102 = 'ea0a4146-fd07-414b-aa5e-dedbeef00102'

SCOPE_101 = 'bdb8f50f82da4370813e6ea797b1fb101'
SCOPE_102 = 'bdb8f50f82da4370813e6ea797b1fb102'
SCOPE_DEF = 'Default'

catalog_scope_list_101 = \
    {
        'id': ID_101,
        'catalog_id': CATALOG_ID_101,
        'scope': SCOPE_101,
        'lifetime_start': '2015-12-31T23:59:59.999999',
        'lifetime_end': '9999-12-31T23:59:59.999999',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'deleted_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

catalog_scope_list_102 = \
    {
        'id': ID_102,
        'catalog_id': CATALOG_ID_101,
        'scope': SCOPE_101,
        'lifetime_start': '2010-01-01T00:00:00.000000',
        'lifetime_end': '2010-12-31T23:59:59.999999',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'deleted_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

catalog_scope_list_103 = \
    {
        'id': ID_103,
        'catalog_id': CATALOG_ID_101,
        'scope': SCOPE_102,
        'lifetime_start': '2015-12-31T23:59:59.999999',
        'lifetime_end': '9999-12-31T23:59:59.999999',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'deleted_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

catalog_scope_list_104 = \
    {
        'id': ID_104,
        'catalog_id': CATALOG_ID_101,
        'scope': SCOPE_102,
        'lifetime_start': '2011-01-01T00:00:00.000000',
        'lifetime_end': '2011-12-31T23:59:59.999999',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'deleted_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

catalog_scope_list_105 = \
    {
        'id': ID_105,
        'catalog_id': CATALOG_ID_102,
        'scope': SCOPE_101,
        'lifetime_start': '2015-12-31T23:59:59.999999',
        'lifetime_end': '9999-12-31T23:59:59.999999',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'deleted_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

catalog_scope_list_106 = \
    {
        'id': ID_106,
        'catalog_id': CATALOG_ID_102,
        'scope': SCOPE_101,
        'lifetime_start': '2012-01-01T00:00:00.000000',
        'lifetime_end': '2012-12-31T23:59:59.999999',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'deleted_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

catalog_scope_list_107 = \
    {
        'id': ID_107,
        'catalog_id': CATALOG_ID_102,
        'scope': SCOPE_102,
        'lifetime_start': '2015-12-31T23:59:59.999999',
        'lifetime_end': '9999-12-31T23:59:59.999999',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'deleted_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

catalog_scope_list_108 = \
    {
        'id': ID_108,
        'catalog_id': CATALOG_ID_102,
        'scope': SCOPE_102,
        'lifetime_start': '2013-01-01T00:00:00.000000',
        'lifetime_end': '2013-12-31T23:59:59.999999',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'deleted_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

catalog_scope_update_101 = \
    {
        'id': ID_101,
        'catalog_id': CATALOG_ID_102,
        'scope': SCOPE_102,
        'lifetime_start': '2015-12-31T23:59:59.999999',
        'lifetime_end': '9999-12-31T23:59:59.999999',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'deleted_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1_update',
                       'expansion_key2': 'expansion_key2_update',
                       'expansion_key3': 'expansion_key3_update',
                       'expansion_key4': 'expansion_key4_update',
                       'expansion_key5': 'expansion_key5_update'},
        'expansions_text': {'expansion_text': 'expansion_text_update'}
    }

fixtures = \
    {
        '/v1/catalogs/ea0a4146-fd07-414b-aa5e-dedbeef00101'
        '/scope/bdb8f50f82da4370813e6ea797b1fb101': {
            'POST': (
                {},
                {'catalog_scope': {
                    'lifetime_start': '2015-12-31T23:59:59.999999',
                    'lifetime_end': '9999-12-31T23:59:59.999999'
                }},
            ),
        },
        '/v1/catalogs/scope/id0a4146-fd07-414b-aa5e-dedbeef00101': {
            'GET': (
                {},
                {'catalog_scope': catalog_scope_list_101},
            ),
            'PATCH': (
                {},
                {'catalog_scope': catalog_scope_update_101},
            ),
            'DELETE': (
                {},
                {},
            ),
        },
        '/v1/catalogs/scope': {
            'GET': (
                {},
                {'catalog_scope': [
                    catalog_scope_list_101,
                    catalog_scope_list_102,
                    catalog_scope_list_103,
                    catalog_scope_list_104,
                    catalog_scope_list_105,
                    catalog_scope_list_106,
                    catalog_scope_list_107,
                    catalog_scope_list_108]},
            ),
        },
        '/v1/catalogs/scope?'
        'catalog_id=ea0a4146-fd07-414b-aa5e-dedbeef00101': {
            'GET': (
                {},
                {'catalog_scope': [
                    catalog_scope_list_101,
                    catalog_scope_list_102,
                    catalog_scope_list_103,
                    catalog_scope_list_104]
                 },
            ),
        },
        '/v1/catalogs/scope?scope=bdb8f50f82da4370813e6ea797b1fb101': {
            'GET': (
                {},
                {'catalog_scope': [
                    catalog_scope_list_101,
                    catalog_scope_list_102,
                    catalog_scope_list_105,
                    catalog_scope_list_106]
                 },
            ),
        },
        '/v1/catalogs/scope?lifetime=2013-01-01T00%3A00%3A00.000000': {
            'GET': (
                {},
                {'catalog_scope': [
                    catalog_scope_list_108]
                 },
            ),
        },
        '/v1/catalogs/scope?limit=2': {
            'GET': (
                {},
                {'catalog_scope': [
                    catalog_scope_list_101,
                    catalog_scope_list_102]
                 },
            ),
        },
        '/v1/catalogs/scope?marker=id0a4146-fd07-414b-aa5e-dedbeef00106': {
            'GET': (
                {},
                {'catalog_scope': [
                    catalog_scope_list_107,
                    catalog_scope_list_108]
                 },
            ),
        },
        '/v1/catalogs/scope?sort_key=catalog_id': {
            'GET': (
                {},
                {'catalog_scope': [
                    catalog_scope_list_103]
                 },
            ),
        },
        '/v1/catalogs/scope?sort_dir=asc': {
            'GET': (
                {},
                {'catalog_scope': [
                    catalog_scope_list_104]
                 },
            ),
        },
        '/v1/catalogs/scope?sort_dir=asc&sort_key=catalog_id': {
            'GET': (
                {},
                {'catalog_scope': [
                    catalog_scope_list_105]
                 },
            ),
        },
        '/v1/catalogs/scope?force_show_deleted=True': {
            'GET': (
                {},
                {'catalog_scope': [
                    catalog_scope_list_106]
                 },
            ),
        },
        '/v1/catalogs/scope?catalog_id=ea0a4146-fd07-414b-aa5e-dedbeef00101'
        '&force_show_deleted=True&lifetime=2017-01-01T00%3A00%3A00.000000'
        '&limit=2&marker=id0a4146-fd07-414b-aa5e-dedbeef00104'
        '&scope=bdb8f50f82da4370813e6ea797b1fb101'
        '&sort_dir=desc&sort_key=catalog_id': {
            'GET': (
                {},
                {'catalog_scope': [
                    catalog_scope_list_105,
                    catalog_scope_list_106]
                 },
            ),
        },
    }


class CatalogScopeManagerTest(testtools.TestCase):
    """CatalogScopeManager Test class."""

    def setUp(self):
        """Setup test class."""
        super(CatalogScopeManagerTest, self).setUp()
        self.api = utils.FakeAPI(fixtures)
        self.mgr = catalog_scope.CatalogScopeManager(self.api)

    def test_list_no_params(self):
        catalog_scope_list = list(self.mgr.list())
        expect = [('GET', '/v1/catalogs/scope', {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(8, len(catalog_scope_list))
        self.assertEqual(ID_101, catalog_scope_list[0].id)
        self.assertEqual(ID_102, catalog_scope_list[1].id)
        self.assertEqual(ID_103, catalog_scope_list[2].id)
        self.assertEqual(ID_104, catalog_scope_list[3].id)
        self.assertEqual(ID_105, catalog_scope_list[4].id)
        self.assertEqual(ID_106, catalog_scope_list[5].id)
        self.assertEqual(ID_107, catalog_scope_list[6].id)
        self.assertEqual(ID_108, catalog_scope_list[7].id)

    def test_list_filter_catalog_id(self):
        kwargs = {'catalog_id': CATALOG_ID_101}
        catalog_scope_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs/scope?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(4, len(catalog_scope_list))
        self.assertEqual(ID_101, catalog_scope_list[0].id)
        self.assertEqual(ID_102, catalog_scope_list[1].id)
        self.assertEqual(ID_103, catalog_scope_list[2].id)
        self.assertEqual(ID_104, catalog_scope_list[3].id)

    def test_list_filter_scope(self):
        kwargs = {'scope': SCOPE_101}
        catalog_scope_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs/scope?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(4, len(catalog_scope_list))
        self.assertEqual(ID_101, catalog_scope_list[0].id)
        self.assertEqual(ID_102, catalog_scope_list[1].id)
        self.assertEqual(ID_105, catalog_scope_list[2].id)
        self.assertEqual(ID_106, catalog_scope_list[3].id)

    def test_list_filter_lifetime(self):
        kwargs = {'lifetime': '2013-01-01T00:00:00.000000'}
        catalog_scope_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs/scope?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(catalog_scope_list))
        self.assertEqual(ID_108, catalog_scope_list[0].id)

    def test_list_with_limit(self):
        kwargs = {'limit': 2}
        catalog_scope_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs/scope?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(2, len(catalog_scope_list))
        self.assertEqual(ID_101, catalog_scope_list[0].id)
        self.assertEqual(ID_102, catalog_scope_list[1].id)

    def test_list_with_marker(self):
        kwargs = {'marker': ID_106}
        catalog_scope_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs/scope?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(2, len(catalog_scope_list))
        self.assertEqual(ID_107, catalog_scope_list[0].id)
        self.assertEqual(ID_108, catalog_scope_list[1].id)

    def test_list_with_sort_key(self):
        kwargs = {'sort_key': 'catalog_id'}
        catalog_scope_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs/scope?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(catalog_scope_list))
        self.assertEqual(ID_103, catalog_scope_list[0].id)

    def test_list_with_sort_dir(self):
        kwargs = {'sort_dir': 'asc'}
        catalog_scope_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs/scope?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(catalog_scope_list))
        self.assertEqual(ID_104, catalog_scope_list[0].id)

    def test_list_with_sort_key_dir(self):
        kwargs = {'sort_dir': 'asc',
                  'sort_key': 'catalog_id'}
        catalog_scope_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs/scope?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(catalog_scope_list))
        self.assertEqual(ID_105, catalog_scope_list[0].id)

    def test_list_with_deleted(self):
        kwargs = {'force_show_deleted': True}
        catalog_scope_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs/scope?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(catalog_scope_list))
        self.assertEqual(ID_106, catalog_scope_list[0].id)

    def test_list_with_all_params(self):
        kwargs = {'catalog_id': CATALOG_ID_101,
                  'scope': SCOPE_101,
                  'lifetime': '2017-01-01T00:00:00.000000',
                  'limit': 2,
                  'marker': ID_104,
                  'sort_key': 'catalog_id',
                  'sort_dir': 'desc',
                  'force_show_deleted': True}
        catalog_scope_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs/scope?' \
            'catalog_id=%s&force_show_deleted=%s&lifetime=%s&limit=%s&' \
            'marker=%s&scope=%s&sort_dir=%s&sort_key=%s' % \
            ('ea0a4146-fd07-414b-aa5e-dedbeef00101',
             'True',
             '2017-01-01T00%3A00%3A00.000000',
             '2',
             'id0a4146-fd07-414b-aa5e-dedbeef00104',
             'bdb8f50f82da4370813e6ea797b1fb101',
             'desc',
             'catalog_id')
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(2, len(catalog_scope_list))
        self.assertEqual(ID_105, catalog_scope_list[0].id)
        self.assertEqual(ID_106, catalog_scope_list[1].id)

    def test_create(self):
        kwargs = {
            'lifetime_start': '2015-12-31T23:59:59.999999',
            'lifetime_end': '9999-12-31T23:59:59.999999'
        }
        expectResponse = {
            'catalog_scope': kwargs
        }
        self.mgr.create(CATALOG_ID_101, SCOPE_101, kwargs)

        url = '/v1/catalogs/%s/scope/%s' % (CATALOG_ID_101, SCOPE_101)
        expect = [('POST',
                   url,
                   {},
                   expectResponse.items())]

        self.assertEqual(expect, self.api.calls)

    def test_get(self):
        res_objs = self.mgr.get(ID_101)
        url = '/v1/catalogs/scope/%s' % (ID_101)
        expect = [('GET', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertIsNotNone(res_objs)
        self.assertEqual(res_objs.id, ID_101)
        self.assertEqual(res_objs.catalog_id, CATALOG_ID_101)
        self.assertEqual(res_objs.scope, SCOPE_101)
        self.assertEqual(res_objs.lifetime_start,
                         '2015-12-31T23:59:59.999999')
        self.assertEqual(res_objs.lifetime_end,
                         '9999-12-31T23:59:59.999999')
        self.assertIsNotNone(res_objs.created_at)
        self.assertIsNotNone(res_objs.updated_at)
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
        expectResponse = {'catalog_scope': catalog_scope_update_101}

        self.mgr.update(ID_101,
                        catalog_scope_update_101)
        expect = [
            ('PATCH',
             '/v1/catalogs/scope/id0a4146-fd07-414b-aa5e-dedbeef00101',
             {},
             expectResponse.items())]
        self.assertEqual(expect, self.api.calls)

    def test_delete(self):
        self. mgr.delete(ID_101)
        url = '/v1/catalogs/scope/%s' % ID_101
        expect = [('DELETE', url, {}, None)]

        self.assertEqual(expect, self.api.calls)
