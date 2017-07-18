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

"""Interface of called PriceComponent."""
from afloclient.common import utils
from afloclient.openstack.common.apiclient import base

SORT_DIR_VALUES = ('asc', 'desc')
SORT_KEY_VALUES = ('price', 'lifetime_start', 'lifetime_end')


class Price(base.Resource):
    """Represents a Price."""

    def __repr__(self):
        """String of Object.
        """
        return "<Price %s>" % self._info


class PriceManager(base.ManagerWithFind):
    """Manager class for manipulating Aflo."""

    def list(self, catalog_id, kwargs=None):
        """Get a list of catalog_price.
        :param catalog_id: Filterling catalog id.
        :param kwargs: Filterling row data<key=value>.
        """
        url = "/v1/catalog/%s/price" % catalog_id
        if kwargs:
            url = url + "?" + utils.urlencode(kwargs)

        response_key = "catalog_price"

        resp, body = self.client.get(url)
        data = []

        for row in body[response_key]:
            catalog_price = Price(self, row, loaded=True)

            data.append(catalog_price)

        return data

    def get(self, catalog_id, scope, seq_no):
        """Get a catalog_price.
        :param catalog_id: Filterling catalog id.
        :param scope: Filterling scope.
        :param seq_no: Filterling seq_no.
        """
        url = "/v1/catalog/%s/price/%s/seq/%s" % (catalog_id, scope, seq_no)

        response_key = "catalog_price"

        resp, body = self.client.get(url)

        catalog_price = Price(self, body[response_key], loaded=True) \
            if "catalog_price" in body else None

        return catalog_price

    def create(self, catalog_id, scope, fields):
        """Create a Price.
        :param fields: price.
        """
        url = '/v1/catalog/%s/price/%s' % (catalog_id, scope)
        response_key = 'catalog_price'
        request_data = {'catalog_price': fields}

        resp, body = self.client.post(url, data=request_data)

        return Price(self, body[response_key], loaded=True)

    def update(self, catalog_id, scope, seq_no, fields):
        """Create a Price.
        :param fields: price.
        """
        url = '/v1/catalog/%s/price/%s/seq/%s' % (catalog_id, scope, seq_no)
        response_key = 'catalog_price'
        request_data = {'catalog_price': fields}

        resp, body = self.client.patch(url, data=request_data)

        return Price(self, body[response_key], loaded=True)

    def delete(self, catalog_id, scope, seq_no):
        """Delete a catalog.
        :param catalog_id: Catalog id.
        :param scope: Scope.
        :param seq_no: Seq no.
        """
        url = "/v1/catalog/%s/price/%s/seq/%s" % (catalog_id, scope, seq_no)
        self.client.delete(url)
