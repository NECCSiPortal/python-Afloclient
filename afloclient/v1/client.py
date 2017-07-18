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

from afloclient.common import http
from afloclient.common import utils
from afloclient.v1.catalog_contents import CatalogContentsManager
from afloclient.v1.catalog_scope import CatalogScopeManager
from afloclient.v1.catalogs import CatalogManager
from afloclient.v1.contracts import ContractManager
from afloclient.v1.goods import GoodsManager
from afloclient.v1.price import PriceManager
from afloclient.v1.tickets import TicketManager
from afloclient.v1.tickettemplates import TickettemplateManager
from afloclient.v1.valid_catalog import ValidCatalogManager
from afloclient.v1.workflowpatterns import WorkflowpatternManager


class Client(object):
    """Client for the OpenStack Tickets v1 API.

    :param string endpoint: A user-supplied endpoint URL for the aflo
                            service.
    :param string token: Token for authentication.
    :param integer timeout: Allows customization of the timeout for client
                            http requests. (optional)
    """

    def __init__(self, endpoint, *args, **kwargs):
        """Initialize a new client for the Tickets v1 API."""
        endpoint, version = utils.strip_version(endpoint)
        self.version = version or 1.0
        self.http_client = http.HTTPClient(endpoint, *args, **kwargs)
        self.tickets = TicketManager(self.http_client)
        self.tickettemplates = TickettemplateManager(self.http_client)
        self.workflowpatterns = WorkflowpatternManager(self.http_client)
        self.contracts = ContractManager(self.http_client)
        self.goods = GoodsManager(self.http_client)
        self.catalogs = CatalogManager(self.http_client)
        self.catalog_contents = CatalogContentsManager(self.http_client)
        self.catalog_scope = CatalogScopeManager(self.http_client)
        self.price = PriceManager(self.http_client)
        self.valid_catalog = ValidCatalogManager(self.http_client)
