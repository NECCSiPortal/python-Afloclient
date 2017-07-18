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

"""Interface of called valid catalog component."""
from afloclient.common import utils
from afloclient.openstack.common.apiclient import base

SORT_DIR_VALUES = ('asc', 'desc')
SORT_KEY_VALUES = ('catalog_id',
                   'scope',
                   'catalog_name',
                   'price',
                   'catalog_lifetime_start',
                   'catalog_lifetime_end',
                   'catalog_scope_lifetime_start',
                   'catalog_scope_lifetime_end',
                   'price_lifetime_start',
                   'price_lifetime_end')


class ValidCatalog(base.Resource):
    """Represents a valid catalog."""

    def __repr__(self):
        """String of Object.
        """
        return "<Valid Catalog %s>" % self._info


class ValidCatalogManager(base.ManagerWithFind):
    """Manager class for manipulating valid catalog."""

    def list(self, kwargs=None):
        """Get a list of valid catalog.
        :param kwargs: Filtering row data<key=value>.
        """
        url = "/v1/catalogs"
        if kwargs:
            url = url + "?" + utils.urlencode(kwargs)

        response_key = "valid_catalog"

        resp, body = self.client.get(url)
        data = []

        for row in body[response_key]:
            valid_list = ValidCatalog(self, row, loaded=True)

            data.append(valid_list)

        return data
