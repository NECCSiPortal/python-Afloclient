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

"""Oslo config
"""

import copy
import os

from oslo_config import cfg
import oslo_log._options as log_options

# 1. Define opts

# "auth_opts" are used by functional tests that are located in
# directory "%project_root%/afloclient/tests/functional"
auth_opts = [
    cfg.StrOpt("username",
               default=None,
               help="This should be the username of a user WITHOUT "
                    "administrative privileges."),
    cfg.StrOpt("project_id",
               help="The non-administrative user's project id "
                    "for keystone v3."),
    cfg.StrOpt("tenant_name",
               default=None,
               help="The non-administrative user's tenant name."),
    cfg.StrOpt("password",
               default=None,
               help="The non-administrative user's password."),

    cfg.StrOpt("auth_url",
               default=None,
               help="URL for where to find the OpenStack Identity admin "
                    "API endpoint."),
    cfg.StrOpt("auth_version",
               default=2,
               help="API version of the admin Identity API endpoint."),
    cfg.StrOpt("admin_username",
               default=None,
               help="This should be the username of a user WITH "
                    "administrative privileges."),
    cfg.StrOpt("admin_tenant_name",
               default=None,
               help="The administrative user's tenant name."),
    cfg.StrOpt("admin_password",
               default=None,
               help="The administrative user's password."),
    cfg.StrOpt("admin_project_id",
               help="The administrative user's project id."),

    cfg.StrOpt("admin_auth_url",
               default=None,
               help="URL for where to find the OpenStack Identity admin "
                    "API endpoint."),
    cfg.StrOpt("user_domain_id",
               default="default",
               help="Set domain_id as a non-administrative user's "
                    "for keystone v3."),
    cfg.StrOpt("admin_user_domain_id",
               default="default",
               help="Set domain_id as a administrative user's "
                    "for keystone v3."),
]

base_opts = [
    cfg.StrOpt("aflo_exec_dir",
               default=os.environ.get(
                   'OS_AFLO_EXEC_DIR',
                   os.path.join(os.path.abspath('.'), '.tox/functional/bin')),
               help="The path to afloclient to be executed."),
    cfg.BoolOpt("suppress_errors_in_cleanup",
                default=True,
                help="Whether to suppress errors with clean up operation "
                     "or not."),
]


# 2. Generate config

PROJECT_NAME = 'afloclient'

DEFAULT_CONFIG_FILE = (
    os.environ.get('OS_%s_CONFIG_FILE' % PROJECT_NAME.upper()) or
    '%s.conf' % PROJECT_NAME)
DEFAULT_CONFIG_DIR = (
    os.environ.get('OS_%s_CONFIG_DIR' % PROJECT_NAME.upper()) or
    os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
                 "etc/afloclient")
)
DEFAULT_CONFIG_PATH = os.path.join(DEFAULT_CONFIG_DIR, DEFAULT_CONFIG_FILE)
FAILOVER_CONFIG_PATH = '/etc/%(pn)s/%(cn)s' % {
    'pn': PROJECT_NAME, 'cn': DEFAULT_CONFIG_FILE}
CONFIG_FILES = []

if os.path.isfile(DEFAULT_CONFIG_PATH):
    CONFIG_FILES.append(DEFAULT_CONFIG_PATH)
if os.path.isfile(FAILOVER_CONFIG_PATH):
    CONFIG_FILES.append(FAILOVER_CONFIG_PATH)

CONF = cfg.CONF

if CONFIG_FILES:
    CONF([], project=PROJECT_NAME, default_config_files=CONFIG_FILES)
else:
    CONF([], project=PROJECT_NAME)

# 3. Register opts

CONF.register_opts(auth_opts)
CONF.register_opts(base_opts)

# 4. Define list_opts for config aflo generator


def list_opts():
    """Return a list of oslo_config options available in Afloclient."""
    opts = [
        (None, copy.deepcopy(auth_opts)),
        (None, copy.deepcopy(base_opts)),
    ]
    opts.extend(log_options.list_opts())
    return opts
