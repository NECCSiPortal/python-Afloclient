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

"""Interface of called CatalogComponent."""
from afloclient.common import utils
from afloclient.openstack.common.apiclient import base

SORT_DIR_VALUES = ('asc', 'desc')
SORT_KEY_VALUES = ('catalog_id',
                   'region_id',
                   'catalog_name',
                   'lifetime_start',
                   'lifetime_end')


class Catalog(base.Resource):
    """Represents a Catalog."""

    def __repr__(self):
        """String of Object.
        """
        return "<Catalog %s>" % self._info


class CatalogManager(base.ManagerWithFind):
    """Manager class for manipulating Aflo."""

    def list(self, kwargs=None):
        """Get a list of catalog.
        :param kwargs: Filtering row data<key=value>.
        """
        url = "/v1/catalog"
        if kwargs:
            url = url + "?" + utils.urlencode(kwargs)

        response_key = "catalog"

        resp, body = self.client.get(url)
        data = []

        for row in body[response_key]:
            catalog = Catalog(self, row, loaded=True)

            data.append(catalog)

        return data

    def create(self, fields):
        """Create a Catalog.
        :param fields: Catalog name & region id.
        """
        url = '/v1/catalog'
        response_key = 'catalog'
        request_data = {'catalog': fields}

        resp, body = self.client.post(url, data=request_data)

        return Catalog(self, body[response_key], loaded=True)

    def update(self, catalog_id, catalog):
        """Update catalog data.
        :param catalog_id: Catalog_id.
        :param catalog: Catalog data.
        """
        url = "/v1/catalog/%s" % catalog_id
        request_data = {'catalog': catalog}

        resp, body = self.client.patch(url, data=request_data)

        catalog = Catalog(self, body["catalog"], loaded=True) \
            if 'catalog' in body else None

        return catalog

    def get(self, catalog_id):
        """Get a Catalog.
        :param catalog_id: Target UUID.
        """
        url = "/v1/catalog/%s" % catalog_id

        resp, body = self.client.get(url)
        catalog = Catalog(self, body["catalog"], loaded=True) \
            if "catalog" in body and body['catalog'] else None

        return catalog

    def delete(self, catalog_id):
        """Delete a catalog.
        :param catalog_id: Catalog id.
        """
        url = "/v1/catalog/%s" % catalog_id
        self.client.delete(url)
