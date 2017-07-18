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

"""Interface of called CatalogContentsComponent."""
from afloclient.common import utils
from afloclient.openstack.common.apiclient import base

SORT_DIR_VALUES = ('asc', 'desc')
SORT_KEY_VALUES = ('goods_id', 'goods_num')


class CatalogContents(base.Resource):
    """Represents a Catalog Contents."""

    def __repr__(self):
        """String of Object.
        """
        return "<Catalog Contents %s>" % self._info


class CatalogContentsManager(base.ManagerWithFind):
    """Manager class for manipulating catalog_contents."""

    def list(self, catalog_id, kwargs=None):
        """Get catalog_contents list.
            :param kwargs: Request parameters.
        """
        url = "/v1/catalog/%s/contents" % catalog_id
        if kwargs:
            url = url + "?" + utils.urlencode(kwargs)

        response_key = "catalog_contents"

        resp, body = self.client.get(url)
        data = []

        for row in body[response_key]:
            catalog_contents = CatalogContents(self, row, loaded=True)

            data.append(catalog_contents)

        return data

    def create(self, catalog_id, fields):
        """Create a Catalog Contents.
        :param fields: goods id & goods num.
        """
        url = '/v1/catalog/%s/contents' % catalog_id
        response_key = 'catalog_contents'
        request_data = {'catalog_contents': fields}

        resp, body = self.client.post(url, data=request_data)

        return CatalogContents(self, body[response_key], loaded=True)

    def get(self, catalog_id, seq_no):
        """Get catalog contents.
        :param catalog_id: Filterling catalog id.
        :param seq_no: Filterling seq_no.
        """
        url = "/v1/catalog/%s/contents/%s" % (catalog_id, seq_no)

        response_key = "catalog_contents"

        resp, body = self.client.get(url)

        catalog_contents = \
            CatalogContents(self, body[response_key], loaded=True) \
            if response_key in body else None

        return catalog_contents

    def update(self, catalog_id, seq_no, catalog_contents):
        """Update catalog contents data.
        :param catalog_id: Catalog Id.
        :param seq_no: Serial number of the contents.
        :param catalog_contents: Catalog contents data.
        """
        url = "/v1/catalog/%s/contents/%s" % (catalog_id, seq_no)
        request_data = {'catalog_contents': catalog_contents}

        resp, body = self.client.patch(url, data=request_data)

        catalog_contents = CatalogContents(self,
                                           body["catalog_contents"],
                                           loaded=True) \
            if 'catalog_contents' in body else None

        return catalog_contents

    def delete(self, catalog_id, seq_no):
        """Delete a catalog.
        :param catalog_id: Catalog id.
        :param seq_no: Seq no.
        """
        url = "/v1/catalog/%s/contents/%s" % (catalog_id, seq_no)
        self.client.delete(url)
