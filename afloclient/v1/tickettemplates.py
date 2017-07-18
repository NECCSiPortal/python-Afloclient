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

"""Interface of called Aflo Component ticket template."""
from afloclient.common import utils
from afloclient import exc
from afloclient.openstack.common.apiclient import base

SORT_DIR_VALUES = ('asc', 'desc')
SORT_KEY_VALUES = ('id', 'created_at', 'updated_at')


class Tickettemplate(base.Resource):
    """Represents a ticket template."""

    def __repr__(self):
        """String of Object."""
        return "<Tickettemplate %s>" % self._info


class TickettemplateManager(base.ManagerWithFind):
    """Manager class for manipulating Aflo tieckt template."""
    resource_class = Tickettemplate

    def get(self, id):
        """Get a ticket template.
        :param id: Target UUID.
        """
        url = "/v1/tickettemplates/%s" % id
        response_key = "tickettemplate"

        resp, body = self.client.get(url)
        return self.resource_class(self, body[response_key], loaded=True)

    def list(self, kwargs=None):
        """Get a list of ticket tempates.
        :param kwargs: Filterling row data<key=value>.
        """
        url = "/v1/tickettemplates"

        if kwargs:
            url = url + "?"

        sort_key = kwargs.pop('sort_key', []) \
            if kwargs and 'sort_key' in kwargs \
            else []
        sort_dir = kwargs.pop('sort_dir', []) \
            if kwargs and 'sort_dir' in kwargs \
            else []

        if len(sort_key) != len(sort_dir):
            raise exc.HTTPBadRequest(
                "Unexpected number of sort directions: "
                "either provide a single sort direction or an equal "
                "number of sort keys and sort directions.")
        for key in sort_key:
            url = '%s&sort_key=%s' % (url, key)
        for dir in sort_dir:
            url = '%s&sort_dir=%s' % (url, dir)

        if kwargs:
            url = url + "&" + utils.urlencode(kwargs)

        response_key = "tickettemplates"

        resp, body = self.client.get(url)
        data = body[response_key]

        return [self.resource_class(self, row, loaded=True)
                for row in data if row]

    def create(self, fields):
        """Create a ticket template.
        :param fields: entry detail data.
        """
        url = '/v1/tickettemplates'
        response_key = 'tickettemplate'
        request_data = {'tickettemplate': fields}

        resp, body = self.client.post(url, data=request_data)

        return Tickettemplate(self, body[response_key], loaded=True)

    def delete(self, id):
        """Delete a ticket template.
        :param id: Target UUID.
        """
        url = "/v1/tickettemplates/%s" % id
        self._delete(url)
