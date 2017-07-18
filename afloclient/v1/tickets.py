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

"""Interface of called TicketComponent."""
from six.moves.urllib import parse

from afloclient.common import utils
from afloclient.openstack.common.apiclient import base

UPDATE_PARAMS = ('text')

CREATE_PARAMS = UPDATE_PARAMS + ('id')

SORT_DIR_VALUES = ('asc', 'desc')
SORT_KEY_VALUES = ('id',
                   'ticket_type', 'target_id',
                   'tenant_id',
                   'owner_id', 'owner_at',
                   'last_status',
                   'last_status_code',
                   'last_confirmer_id',
                   'last_confirmed_at',
                   'created_at', 'updated_at')


class Ticket(base.Resource):
    """Represents a Ticket."""

    def __repr__(self):
        """String of Object.
        """
        return "<Ticket %s>" % self._info

    def update(self, id, **kwargs):
        """Update Object.
        :param id: Target UUID.
        :param **kwargs: Update row data<key=value>.
        """
        return self.manager.update(self, id, **kwargs)

    def delete(self, id):
        """Delete Object.
        :param id: Target UUID.
        """
        self.manager.delete(self, id)


class Workflow(base.Resource):
    """Represents a Workflow."""

    def __repr__(self):
        """String of Object."""
        return "<Workflow %s>" % self._info


class TicketManager(base.ManagerWithFind):
    """Manager class for manipulating Aflo."""

    def get(self, id):
        """Get a ticket.
        :param id: Target UUID.
        """
        url = "/v1/tickets/%s" % id

        resp, body = self.client.get(url)

        ticket = Ticket(self, body["ticket"], loaded=True) \
            if "ticket" in body else None

        return ticket

    def list(self, kwargs=None):
        """Get a list of ticket.
        :param kwargs: Filterling row data<key=value>.
        """
        url = "/v1/tickets"
        eixsts_ticket_type = False

        if kwargs:
            url = url + "?"

        # If user set catalog filter, it change to list parameter.
        # This process is necessary for 'AND' search condition.
        if kwargs and 'ticket_type' in kwargs:
            eixsts_ticket_type = True
            ticket_type = kwargs.pop('ticket_type', [])
            ticket_type_url = ''

            if not isinstance(ticket_type, list):
                ticket_type = [ticket_type]

            for i in range(0, len(ticket_type)):
                value = ticket_type[i]
                if i != 0:
                    ticket_type_url = ticket_type_url + '&'
                ticket_type_url = ticket_type_url + \
                    parse.urlencode({'ticket_type': value})

            url = url + ticket_type_url

        if kwargs:
            url = url + ('&' if eixsts_ticket_type else '') \
                + utils.urlencode(kwargs)

        response_key = "tickets"

        resp, body = self.client.get(url)
        data = []

        for row in body[response_key]:
            ticket = Ticket(self, row, loaded=True)

            data.append(ticket)

        return data

    def create(self, fields):
        """Create a ticket.
        :param fields: ticket template id & entry detail data.
        """
        url = '/v1/tickets'
        request_data = {'ticket': fields}

        resp, body = self.client.post(url, data=request_data)

        ticket = Ticket(self, body["ticket"], loaded=True) \
            if "ticket" in body else None
        workflows_data = body["workflows"] \
            if "workflows" in body else None

        workflows = []
        if workflows_data:
            for workflow in workflows_data:
                workflows.append(Workflow(self, workflow, loaded=True))

        return (ticket, workflows)

    def update(self, id, fields):
        """Update ticket data.
        :param id: Target UUID.
        :param fields: Update row data.
        """
        url = "/v1/tickets/%s" % id
        request_data = {'ticket': fields}

        self.client.put(url, data=request_data)

    def delete(self, id):
        """Delete a ticket.
        :param id: Target UUID.
        """
        url = "/v1/tickets/%s" % id
        self._delete(url)
