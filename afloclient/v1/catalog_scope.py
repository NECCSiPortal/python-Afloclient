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

"""Interface of called catalog scope component."""
from afloclient.common import utils
from afloclient.openstack.common.apiclient import base

SORT_DIR_VALUES = ('asc', 'desc')
SORT_KEY_VALUES = ('id',
                   'catalog_id',
                   'scope',
                   'lifetime_start',
                   'lifetime_end')


class CatalogScope(base.Resource):
    """Represents a catalog scope."""

    def __repr__(self):
        """String of Object."""

        return "<Catalog Scope %s>" % self._info


class CatalogScopeManager(base.ManagerWithFind):
    """Manager class for manipulating catalog scope."""

    def list(self, kwargs=None):
        """Get a list of catalog scope.
        :param kwargs: Filtering row data<key=value>.
        """
        url = "/v1/catalogs/scope"
        if kwargs:
            url = url + "?" + utils.urlencode(kwargs)

        response_key = "catalog_scope"

        resp, body = self.client.get(url)
        data = []

        for row in body[response_key]:
            catalog_scope = CatalogScope(self, row, loaded=True)

            data.append(catalog_scope)

        return data

    def create(self, catalog_id, scope, fields):
        """Create a Catalog scope.
        :param catalog_id: The catalog id of registration to catalog scope
        :param scope: The scope of registration to catalog scope
        :param fields: entry detail data.
        """
        url = "/v1/catalogs/%s/scope/%s" % (catalog_id, scope)
        response_key = 'catalog_scope'
        request_data = {'catalog_scope': fields}

        resp, body = self.client.post(url, data=request_data)

        return CatalogScope(self, body[response_key], loaded=True)

    def get(self, catalog_scope_id):
        """Get catalog scope.
        :param catalog_scope_id: Filtering catalog scope id.
        """
        url = "/v1/catalogs/scope/%s" % catalog_scope_id

        response_key = "catalog_scope"

        resp, body = self.client.get(url)

        catalog_scope = \
            CatalogScope(self, body[response_key], loaded=True) \
            if response_key in body else None

        return catalog_scope

    def update(self, catalog_scope_id, fields):
        """Update catalog scope data.
        :param catalog_scope_id: The id of catalog scope table.
        :param fields: updata detail data.
        """
        url = "/v1/catalogs/scope/%s" % catalog_scope_id
        response_key = 'catalog_scope'
        request_data = {'catalog_scope': fields}

        resp, body = self.client.patch(url, data=request_data)

        return CatalogScope(self, body[response_key], loaded=True)

    def delete(self, catalog_scope_id):
        """Delete a catalog scope.
        :param catalog_scope_id: The id of catalog scope table.
        """
        url = "/v1/catalogs/scope/%s" % catalog_scope_id
        self.client.delete(url)
