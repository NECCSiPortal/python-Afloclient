
================
Develop Note
================
CREATE 2015/06/02
UPDATE 2015/06/02 INSTALL & UNINSTALL
UPDATE 2015/06/05 COMMANDLINE TEST FOR KEYSTONE
UPDATE 2015/06/17 RUN TEMPEST CLI TEST
UPDATE 2016/02/04 for Keystone V3


================
INSTALL & UNINSTALL
================
1) install command
    $ sudo python setup.py install --record files.txt

2) call aflo command
    A RC file was created using Horizon Dashboard.
    $ source demo-openrc.sh
    $ aflo
    $ aflo ticket-create

2) uninstall command
    $ sudo cat files.txt | sudo xargs rm -rvf


================
COMMANDLINE INPUT
================
Entry your new component to keystone(use commandline).

1) Create a RC file
    Create a env-rc file from Dashboard for you run keystone command.
    http://docs.openstack.org/ja/user-guide/content/cli_openrc.html

    $ source demo-openrc.sh

2) Create user
    Create aflo service user.
    Keystone-client middleware in component service use this user authorization.
      refer : [Component]/etc/aflo-api.conf

    $ keystone user-create --name <user-name> --pass <user-password>
    $ keystone user-role-add --user <user-name> --tenant <tenant> --role <role>

    ex: <user-name>           = aflo
        <user-password>       = password
        <tenant>              = admin
        <role>                = admin

3) Create service
    Create your new component service.

    $ keystone service-create --name=<service-name> --type=<service-type> --description="<service-description>"
    ex: <service-name>        = aflo
        <service-type>        = ticket
        <service-description> = Aflo Service

4) Create endpoint
    Create your new component endpoint.

    $ keystone endpoint-create \
        --region RegionOne \
        --service_id=<service-id> \
        --publicurl=<service-public-url> \
        --internalurl=<service-internal-url> \
        --adminurl=<service-admin-url>

    ex: <service-id>           = your new service id from run "keystone service-list" command.
        <service-public-url>   = http://localhost:9293/
        <service-internal-url> = http://localhost:9293/
        <service-admin-url>    = http://localhost:9293/

5) Check access to your new component
    Using curl command or python-client.

    Install curl and openssl.

    $ yum install curl openssl

================
RUN TEMPEST CLI TEST
================

1) Create Config Aflo File
  Create a tempest config aflo file

  $ tox -e genconfig
  $ cp -p etc/afloclient/afloclient.conf.aflo etc/afloclient/afloclient.conf
  $ vi etc/afloclient/afloclient.conf
    sample:
    ----------
    [DEFAULT]
    namespace = afloclient.config

    username=demo
    tenant_name=demo
    project_id=<demo-project-id>
    password=<demo_password>

    # auth_url=http://<keystone-ip>:<keystone-port>/<version>/
    auth_url=http://127.0.0.1:5000/v2
    # auth_url=http://127.0.0.1:5000/v3

    admin_username=admin
    admin_tenant_name=admin
    admin_project_id=<admin_project_id>
    admin_password=<admin_password>

    # If you use keystone v3, add auth_version parameter.
    # auth_version = 3
    ----------

  If you have permission error on tox command, you change "./build" folder, subfolder and files permission.
  ex) $ sudo chmod 777 -R ./build

2) Install Component Service
  It is necessary for you to insatall your component servies.

3) Run Tempest CLI test
  $ tox -e functional
