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

"""Test afloclient/v1/valid_catalog.py."""

import testtools

from afloclient.tests.unit import utils
from afloclient.v1 import valid_catalog
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
CATALOG_ID_103 = 'ea0a4146-fd07-414b-aa5e-dedbeef00103'
CATALOG_ID_104 = 'ea0a4146-fd07-414b-aa5e-dedbeef00104'

SCOPE_101 = 'bdb8f50f82da4370813e6ea797b1fb101'
SCOPE_102 = 'a0d58ee41a364026a1031aca2548fd102'
SCOPE_DEF = 'Default'

valid_catalog_list_101 = \
    {
        'catalog_id': CATALOG_ID_101,
        'scope': SCOPE_101,
        'catalog_name': 'CATALOG-A-101',
        'catalog_lifetime_start': '2015-12-31T23:59:59.999999',
        'catalog_lifetime_end': '9999-12-31T23:59:59.999999',
        'catalog_scope_id': ID_101,
        'catalog_scope_lifetime_start': '2015-12-31T23:59:59.999999',
        'catalog_scope_lifetime_end': '9999-12-31T23:59:59.999999',
        'price_seq_no': 'price-seq-no-111-222-333-1',
        'price': '101',
        'price_lifetime_start': '2015-12-31T23:59:59.999999',
        'price_lifetime_end': '9999-12-31T23:59:59.999999'
    }
valid_catalog_list_102 = \
    {
        'catalog_id': CATALOG_ID_102,
        'scope': SCOPE_101,
        'catalog_name': 'CATALOG-A-102',
        'catalog_lifetime_start': '2012-12-31T23:59:59.999999',
        'catalog_lifetime_end': '2014-12-31T23:59:59.999999',
        'catalog_scope_id': ID_102,
        'catalog_scope_lifetime_start': '2015-12-31T23:59:59.999999',
        'catalog_scope_lifetime_end': '9999-12-31T23:59:59.999999',
        'price_seq_no': 'price-seq-no-111-222-333-2',
        'price': '102',
        'price_lifetime_start': '2015-12-31T23:59:59.999999',
        'price_lifetime_end': '9999-12-31T23:59:59.999999'
    }
valid_catalog_list_103 = \
    {
        'catalog_id': CATALOG_ID_103,
        'scope': SCOPE_101,
        'catalog_name': 'CATALOG-A-103',
        'catalog_lifetime_start': '2015-12-31T23:59:59.999999',
        'catalog_lifetime_end': '9999-12-31T23:59:59.999999',
        'catalog_scope_id': ID_103,
        'catalog_scope_lifetime_start': '2015-12-31T23:59:59.999999',
        'catalog_scope_lifetime_end': '9999-12-31T23:59:59.999999',
        'price_seq_no': 'price-seq-no-111-222-333-3',
        'price': '103',
        'price_lifetime_start': '2015-12-31T23:59:59.999999',
        'price_lifetime_end': '9999-12-31T23:59:59.999999'
    }
valid_catalog_list_104 = \
    {
        'catalog_id': CATALOG_ID_104,
        'scope': SCOPE_101,
        'catalog_name': 'CATALOG-A-104',
        'catalog_lifetime_start': '2012-12-31T23:59:59.999999',
        'catalog_lifetime_end': '2014-12-31T23:59:59.999999',
        'catalog_scope_id': ID_104,
        'catalog_scope_lifetime_start': '2015-12-31T23:59:59.999999',
        'catalog_scope_lifetime_end': '9999-12-31T23:59:59.999999',
        'price_seq_no': 'price-seq-no-111-222-333-4',
        'price': '104',
        'price_lifetime_start': '2015-12-31T23:59:59.999999',
        'price_lifetime_end': '9999-12-31T23:59:59.999999'
    }
valid_catalog_list_105 = \
    {
        'catalog_id': CATALOG_ID_101,
        'scope': SCOPE_DEF,
        'catalog_name': 'CATALOG-A-101',
        'catalog_lifetime_start': '2015-12-31T23:59:59.999999',
        'catalog_lifetime_end': '9999-12-31T23:59:59.999999',
        'catalog_scope_id': ID_105,
        'catalog_scope_lifetime_start': '2015-12-31T23:59:59.999999',
        'catalog_scope_lifetime_end': '9999-12-31T23:59:59.999999',
        'price_seq_no': 'price-seq-no-111-222-333-5',
        'price': '105',
        'price_lifetime_start': '2015-12-31T23:59:59.999999',
        'price_lifetime_end': '9999-12-31T23:59:59.999999'
    }
valid_catalog_list_106 = \
    {
        'catalog_id': CATALOG_ID_101,
        'scope': SCOPE_DEF,
        'catalog_name': 'CATALOG-A-102',
        'catalog_lifetime_start': '2015-12-31T23:59:59.999999',
        'catalog_lifetime_end': '9999-12-31T23:59:59.999999',
        'catalog_scope_id': ID_106,
        'catalog_scope_lifetime_start': '2015-12-31T23:59:59.999999',
        'catalog_scope_lifetime_end': '9999-12-31T23:59:59.999999',
        'price_seq_no': 'price-seq-no-111-222-333-6',
        'price': '106',
        'price_lifetime_start': '2015-12-31T23:59:59.999999',
        'price_lifetime_end': '9999-12-31T23:59:59.999999'
    }
valid_catalog_list_107 = \
    {
        'catalog_id': CATALOG_ID_101,
        'scope': SCOPE_DEF,
        'catalog_name': 'CATALOG-A-103',
        'catalog_lifetime_start': '2015-12-31T23:59:59.999999',
        'catalog_lifetime_end': '9999-12-31T23:59:59.999999',
        'catalog_scope_id': ID_107,
        'catalog_scope_lifetime_start': '2015-12-31T23:59:59.999999',
        'catalog_scope_lifetime_end': '9999-12-31T23:59:59.999999',
        'price_seq_no': 'price-seq-no-111-222-333-7',
        'price': '107',
        'price_lifetime_start': '2015-12-31T23:59:59.999999',
        'price_lifetime_end': '9999-12-31T23:59:59.999999'
    }
valid_catalog_list_108 = \
    {
        'catalog_id': CATALOG_ID_101,
        'scope': SCOPE_DEF,
        'catalog_name': 'CATALOG-A-104',
        'catalog_lifetime_start': '2015-12-31T23:59:59.999999',
        'catalog_lifetime_end': '9999-12-31T23:59:59.999999',
        'catalog_scope_id': ID_108,
        'catalog_scope_lifetime_start': '2015-12-31T23:59:59.999999',
        'catalog_scope_lifetime_end': '9999-12-31T23:59:59.999999',
        'price_seq_no': 'price-seq-no-111-222-333-8',
        'price': '108',
        'price_lifetime_start': '2015-12-31T23:59:59.999999',
        'price_lifetime_end': '9999-12-31T23:59:59.999999'
    }

fixtures = \
    {
        '/v1/catalogs': {
            'GET': (
                {},
                {'valid_catalog': [
                    valid_catalog_list_101,
                    valid_catalog_list_102,
                    valid_catalog_list_103,
                    valid_catalog_list_104,
                    valid_catalog_list_105,
                    valid_catalog_list_106,
                    valid_catalog_list_107,
                    valid_catalog_list_108]
                 },
            ),
        },
        '/v1/catalogs?lifetime=2016-12-10T23%3A59%3A59.999999': {
            'GET': (
                {},
                {'valid_catalog': [
                    valid_catalog_list_101,
                    valid_catalog_list_103,
                    valid_catalog_list_105,
                    valid_catalog_list_106,
                    valid_catalog_list_107,
                    valid_catalog_list_108]
                 },
            ),
        },
        '/v1/catalogs?scope=bdb8f50f82da4370813e6ea797b1fb101': {
            'GET': (
                {},
                {'valid_catalog': [
                    valid_catalog_list_101,
                    valid_catalog_list_102,
                    valid_catalog_list_103,
                    valid_catalog_list_104]
                 },
            ),
        },
        '/v1/catalogs?catalog_id=ea0a4146-fd07-414b-aa5e-dedbeef00101': {
            'GET': (
                {},
                {'valid_catalog': [
                    valid_catalog_list_101,
                    valid_catalog_list_105]
                 },
            ),
        },
        '/v1/catalogs?catalog_name=CATALOG-A-104': {
            'GET': (
                {},
                {'valid_catalog': [
                    valid_catalog_list_104,
                    valid_catalog_list_108]
                 },
            ),
        },
        '/v1/catalogs?refine_flg=True': {
            'GET': (
                {},
                {'valid_catalog': [
                    valid_catalog_list_101,
                    valid_catalog_list_103]
                 },
            ),
        },
        '/v1/catalogs?limit=2': {
            'GET': (
                {},
                {'valid_catalog': [
                    valid_catalog_list_101,
                    valid_catalog_list_102]
                 },
            ),
        },
        '/v1/catalogs?catalog_marker='
        'ea0a4146-fd07-414b-aa5e-dedbeef00102': {
            'GET': (
                {},
                {'valid_catalog': [
                    valid_catalog_list_105]
                 },
            ),
        },
        '/v1/catalogs?catalog_scope_marker='
        'id0a4146-fd07-414b-aa5e-dedbeef00106': {
            'GET': (
                {},
                {'valid_catalog': [
                    valid_catalog_list_106]
                 },
            ),
        },
        '/v1/catalogs?price_marker=price-seq-no-111-222-333': {
            'GET': (
                {},
                {'valid_catalog': [
                    valid_catalog_list_107]
                 },
            ),
        },
        '/v1/catalogs?catalog_marker=ea0a4146-fd07-414b-aa5e-dedbeef00102'
        '&catalog_scope_marker=id0a4146-fd07-414b-aa5e-dedbeef00106'
        '&price_marker=price-seq-no-111-222-333': {
            'GET': (
                {},
                {'valid_catalog': [
                    valid_catalog_list_108]
                 },
            ),
        },
        '/v1/catalogs?sort_key=catalog_id': {
            'GET': (
                {},
                {'valid_catalog': [
                    valid_catalog_list_102]
                 },
            ),
        },
        '/v1/catalogs?sort_dir=asc': {
            'GET': (
                {},
                {'valid_catalog': [
                    valid_catalog_list_103]
                 },
            ),
        },
        '/v1/catalogs?sort_dir=asc&sort_key=catalog_id': {
            'GET': (
                {},
                {'valid_catalog': [
                    valid_catalog_list_104]
                 },
            ),
        },
        '/v1/catalogs?catalog_id=ea0a4146-fd07-414b-aa5e-dedbeef00101'
        '&catalog_marker=ea0a4146-fd07-414b-aa5e-dedbeef00101'
        '&catalog_scope_marker=id0a4146-fd07-414b-aa5e-dedbeef00102'
        '&lifetime=2017-01-01T00%3A00%3A00.000000&limit=3'
        '&price_marker=price-seq-no-111-222-333&refine_flg=False'
        '&scope=bdb8f50f82da4370813e6ea797b1fb101&sort_dir=desc'
        '&sort_key=catalog_id': {
            'GET': (
                {},
                {'valid_catalog': [
                    valid_catalog_list_103,
                    valid_catalog_list_104,
                    valid_catalog_list_105]
                 },
            ),
        },
    }


class ValidCatalogManagerTest(testtools.TestCase):
    """Test class of ValidCatalogManager."""

    def setUp(self):
        """Setup test class."""
        super(ValidCatalogManagerTest, self).setUp()
        self.api = utils.FakeAPI(fixtures)
        self.mgr = valid_catalog.ValidCatalogManager(self.api)

    def test_list_no_params(self):
        valid_catalog_list = list(self.mgr.list())
        expect = [('GET', '/v1/catalogs', {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(8, len(valid_catalog_list))
        self.assertEqual('101', valid_catalog_list[0].price)
        self.assertEqual('102', valid_catalog_list[1].price)
        self.assertEqual('103', valid_catalog_list[2].price)
        self.assertEqual('104', valid_catalog_list[3].price)
        self.assertEqual('105', valid_catalog_list[4].price)
        self.assertEqual('106', valid_catalog_list[5].price)
        self.assertEqual('107', valid_catalog_list[6].price)
        self.assertEqual('108', valid_catalog_list[7].price)

    def test_list_filter_lifetime(self):
        kwargs = {'lifetime': '2016-12-10T23:59:59.999999'}
        valid_catalog_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(6, len(valid_catalog_list))
        self.assertEqual('101', valid_catalog_list[0].price)
        self.assertEqual('103', valid_catalog_list[1].price)
        self.assertEqual('105', valid_catalog_list[2].price)
        self.assertEqual('106', valid_catalog_list[3].price)
        self.assertEqual('107', valid_catalog_list[4].price)
        self.assertEqual('108', valid_catalog_list[5].price)

    def test_list_filter_scope(self):
        kwargs = {'scope': SCOPE_101}
        valid_catalog_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(4, len(valid_catalog_list))
        self.assertEqual('101', valid_catalog_list[0].price)
        self.assertEqual('102', valid_catalog_list[1].price)
        self.assertEqual('103', valid_catalog_list[2].price)
        self.assertEqual('104', valid_catalog_list[3].price)

    def test_list_filter_catalog_id(self):
        kwargs = {'catalog_id': CATALOG_ID_101}
        valid_catalog_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(2, len(valid_catalog_list))
        self.assertEqual('101', valid_catalog_list[0].price)
        self.assertEqual('105', valid_catalog_list[1].price)

    def test_list_filter_catalog_name(self):
        kwargs = {'catalog_name': 'CATALOG-A-104'}
        valid_catalog_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(2, len(valid_catalog_list))
        self.assertEqual('104', valid_catalog_list[0].price)
        self.assertEqual('108', valid_catalog_list[1].price)

    def test_list_filter_refine_flg(self):
        kwargs = {'refine_flg': True}
        valid_catalog_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(2, len(valid_catalog_list))
        self.assertEqual('101', valid_catalog_list[0].price)
        self.assertEqual('103', valid_catalog_list[1].price)

    def test_list_with_limit(self):
        kwargs = {'limit': 2}
        valid_catalog_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(2, len(valid_catalog_list))
        self.assertEqual('101', valid_catalog_list[0].price)
        self.assertEqual('102', valid_catalog_list[1].price)

    def test_list_with_catalog_marker(self):
        kwargs = {'catalog_marker': CATALOG_ID_102}
        valid_catalog_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(valid_catalog_list))
        self.assertEqual('105', valid_catalog_list[0].price)

    def test_list_with_catalog_scope_marker(self):
        kwargs = {'catalog_scope_marker':
                  'id0a4146-fd07-414b-aa5e-dedbeef00106'}
        valid_catalog_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(valid_catalog_list))
        self.assertEqual('106', valid_catalog_list[0].price)

    def test_list_with_price_marker(self):
        kwargs = {'price_marker': 'price-seq-no-111-222-333'}
        valid_catalog_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(valid_catalog_list))
        self.assertEqual('107', valid_catalog_list[0].price)

    def test_list_with_markers(self):
        kwargs = {'catalog_marker': CATALOG_ID_102,
                  'catalog_scope_marker':
                  'id0a4146-fd07-414b-aa5e-dedbeef00106',
                  'price_marker': 'price-seq-no-111-222-333'}
        valid_catalog_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs?' \
            'catalog_marker=%s&catalog_scope_marker=%s' \
            '&price_marker=%s' % \
            (CATALOG_ID_102,
             'id0a4146-fd07-414b-aa5e-dedbeef00106',
             'price-seq-no-111-222-333')
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(valid_catalog_list))
        self.assertEqual('108', valid_catalog_list[0].price)

    def test_list_with_sort_key(self):
        kwargs = {'sort_key': 'catalog_id'}
        valid_catalog_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(valid_catalog_list))
        self.assertEqual('102', valid_catalog_list[0].price)

    def test_list_with_sort_dir(self):
        kwargs = {'sort_dir': 'asc'}
        valid_catalog_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(valid_catalog_list))
        self.assertEqual('103', valid_catalog_list[0].price)

    def test_list_with_sort_key_dir(self):
        kwargs = {'sort_dir': 'asc',
                  'sort_key': 'catalog_id'}
        valid_catalog_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(valid_catalog_list))
        self.assertEqual('104', valid_catalog_list[0].price)

    def test_list_with_all_params(self):
        kwargs = {'lifetime': '2017-01-01T00:00:00.000000',
                  'scope': SCOPE_101,
                  'catalog_id': CATALOG_ID_101,
                  'refine_flg': False,
                  'limit': 3,
                  'catalog_marker': CATALOG_ID_101,
                  'catalog_scope_marker': ID_102,
                  'price_marker': 'price-seq-no-111-222-333',
                  'sort_key': 'catalog_id',
                  'sort_dir': 'desc'}
        valid_catalog_list = list(self.mgr.list(kwargs))
        url = '/v1/catalogs?' \
              'catalog_id=%s&catalog_marker=%s&catalog_scope_marker=%s' \
              '&lifetime=%s&limit=%s&price_marker=%s&refine_flg=%s' \
              '&scope=%s&sort_dir=%s&sort_key=%s' % \
              (CATALOG_ID_101,
               CATALOG_ID_101,
               ID_102,
               '2017-01-01T00%3A00%3A00.000000',
               '3',
               'price-seq-no-111-222-333',
               'False',
               SCOPE_101,
               'desc',
               'catalog_id')
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(3, len(valid_catalog_list))
        self.assertEqual('103', valid_catalog_list[0].price)
        self.assertEqual('104', valid_catalog_list[1].price)
        self.assertEqual('105', valid_catalog_list[2].price)
