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

from afloclient.common import utils
from afloclient.openstack.common.apiclient import base

SORT_DIR_VALUES = ('asc', 'desc')
SORT_KEY_VALUES = ('contract_id',
                   'project_name',
                   'catalog_name',
                   'application_id',
                   'ticket_template_name',
                   'application_name',
                   'application_date',
                   'lifetime_start',
                   'lifetime_end')


class Contract(base.Resource):
    """Contract resource."""

    def __repr__(self):
        """String of contract object.
        """
        return "<Contract %s>" % self._info

    def update(self, contract_id, **kwargs):
        """Update Object.
        :param contract_id: Contract UUID.
        :param **kwargs: Update row data<key=value>.
        """
        return self.manager.update(self, contract_id, **kwargs)


class ContractManager(base.ManagerWithFind):
    """Contract manager class."""
    resource_class = Contract

    def create(self, contract):
        """Create a Contract.
        :param contract: Contract data.
        """
        url = '/v1/contract'
        data = {'contract': contract}

        resp, body = self.client.post(url, data=data)

        contract = Contract(self, body["contract"], loaded=True) \
            if 'contract' in body else None

        return contract

    def update(self, contract_id, contract):
        """Update contract data.
        :param contract: Contract id.
        :param contract: Contract data.
        """
        url = "/v1/contract/%s" % contract_id
        request_data = {'contract': contract}

        resp, body = self.client.patch(url, data=request_data)

        contract = Contract(self, body["contract"], loaded=True) \
            if 'contract' in body else None

        return contract

    def get(self, contract_id):
        """Get contract data.
        :param contract_id: Contract UUID.
        :param fields: Update row data.
        """
        url = "/v1/contract/%s" % contract_id
        response_key = 'contract'

        resp, body = self.client.get(url)

        return Contract(self, body[response_key], loaded=True)

    def delete(self, contract_id):
        """Delete a contract.
        :param contract_id: Contract id.
        """
        url = "/v1/contract/%s" % contract_id
        self.client.delete(url)

    def list(self, kwargs=None):
        """Get contract list.
            :param kwargs: Request parameters.
        """
        url = "/v1/contract"
        if kwargs:
            url = url + "?" + utils.urlencode(kwargs)

        response_key = "contract"

        resp, body = self.client.get(url)
        data = []

        for row in body[response_key]:
            contract = Contract(self, row, loaded=True)

            data.append(contract)

        return data
