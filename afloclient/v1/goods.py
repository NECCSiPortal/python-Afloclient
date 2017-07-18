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

"""Interface of called GoodsComponent."""
from afloclient.common import utils
from afloclient.openstack.common.apiclient import base

SORT_DIR_VALUES = ('asc', 'desc')
SORT_KEY_VALUES = ('goods_id', 'region_id', 'goods_name')


class Goods(base.Resource):
    """Represents a Ticket."""

    def __repr__(self):
        """String of Object.
        """
        return "<Goods %s>" % self._info


class GoodsManager(base.ManagerWithFind):
    """Manager class for manipulating Aflo."""

    def list(self, kwargs=None):
        """Get a list of goods.
        :param kwargs: Filterling row data<key=value>.
        """
        url = "/v1/goods"
        if kwargs:
            url = url + "?" + utils.urlencode(kwargs)

        response_key = "goods"

        resp, body = self.client.get(url)
        data = []

        for row in body[response_key]:
            goods = Goods(self, row, loaded=True)

            data.append(goods)

        return data

    def create(self, fields):
        """Create a Goods.
        :param fields: goods name & region id.
        """
        url = '/v1/goods'
        response_key = 'goods'
        request_data = {'goods': fields}

        resp, body = self.client.post(url, data=request_data)

        return Goods(self, body[response_key], loaded=True)

    def update(self, goods_id, goods):
        """Update goods data.
        :param goods_id: Goods_id.
        :param goods: Goods data.
        """
        url = "/v1/goods/%s" % goods_id
        request_data = {'goods': goods}

        resp, body = self.client.patch(url, data=request_data)

        goods = Goods(self, body["goods"], loaded=True) \
            if 'goods' in body else None

        return goods

    def get(self, goods_id):
        """Get a Goods.
        :param goods_id: Filtering data.
        """
        url = '/v1/goods/%s' % (goods_id)

        response_key = 'goods'

        resp, body = self.client.get(url)

        goods = Goods(self, body[response_key], loaded=True) \
            if 'goods' in body else None

        return goods

    def delete(self, goods_id):
        """Delete a goods.
        :param goods_id: Goods id.
        """
        url = "/v1/goods/%s" % goods_id
        self.client.delete(url)
