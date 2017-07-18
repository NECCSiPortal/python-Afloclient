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

"""Interface of called Aflo Component workflow pattern."""

from afloclient.openstack.common.apiclient import base


class Workflowpattern(base.Resource):
    """Represents a workflow pattern."""

    def __repr__(self):
        """String of Object."""
        return "<Workflowpattern %s>" % self._info


class WorkflowpatternManager(base.ManagerWithFind):
    """Manager class for manipulating Aflo workflow pattern."""
    resource_class = Workflowpattern

    def list(self, kwargs=None):
        # TODO(hiramatsu) : create list method.
        pass

    def create(self, fields):
        """Create a workflow pattern.
        :param fields: entry detail data.
        """
        url = '/v1/workflowpatterns'
        response_key = 'workflowpattern'
        request_data = {'workflowpattern': fields}

        resp, body = self.client.post(url, data=request_data)

        return Workflowpattern(self, body[response_key], loaded=True)

    def delete(self, id):
        """Delete a workflow pattern.
        :param id: Target UUID.
        """
        url = "/v1/workflowpatterns/%s" % id
        self._delete(url)
