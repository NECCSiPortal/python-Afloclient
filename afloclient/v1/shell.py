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

"""Commandline subcommand  Method from."""

from __future__ import print_function

import codecs
import json
import os.path

from afloclient.common import utils
from afloclient import exc
import afloclient.v1.tickets

FILE_ENCODE = ('utf-8', 's-jis')

_print_ticket_columns = \
    ['id',
     'ticket_template_id',
     'ticket_type', 'target_id',
     'tenant_id',
     'owner_id', 'owner_at',
     'ticket_detail', 'action_detail']
_print_workflow_columns = \
    ['id',
     'ticket_id',
     'status',
     'status_code',
     'status_detail',
     'target_role',
     'confirmer_id',
     'confirmed_at',
     'additional_data']
_print_contract_columns = \
    ['contract_id',
     'region_id',
     'project_id',
     'project_name',
     'catalog_id',
     'catalog_name',
     'num',
     'parent_ticket_template_id',
     'ticket_template_id',
     'parent_ticket_template_name',
     'parent_application_kinds_name',
     'application_kinds_name',
     'cancel_application_id',
     'application_id',
     'ticket_template_name',
     'application_name',
     'application_date',
     'parent_contract_id',
     'lifetime_start',
     'lifetime_end',
     'created_at',
     'updated_at',
     'deleted_at',
     'deleted',
     'expansion_key1',
     'expansion_key2',
     'expansion_key3',
     'expansion_key4',
     'expansion_key5',
     'expansion_text']
_print_goods_columns = \
    ['goods_id',
     'region_id',
     'goods_name',
     'created_at',
     'updated_at',
     'deleted_at',
     'deleted',
     'expansion_key1',
     'expansion_key2',
     'expansion_key3',
     'expansion_key4',
     'expansion_key5',
     'expansion_text']
_print_catalog_columns = \
    ['catalog_id',
     'region_id',
     'catalog_name',
     'lifetime_start',
     'lifetime_end',
     'created_at',
     'updated_at',
     'deleted_at',
     'deleted',
     'expansion_key1',
     'expansion_key2',
     'expansion_key3',
     'expansion_key4',
     'expansion_key5',
     'expansion_text']
_print_catalog_contents_columns = \
    ['catalog_id',
     'seq_no',
     'goods_id',
     'goods_num',
     'created_at',
     'updated_at',
     'deleted_at',
     'deleted',
     'expansion_key1',
     'expansion_key2',
     'expansion_key3',
     'expansion_key4',
     'expansion_key5',
     'expansion_text']
_print_catalog_scope_columns = \
    ['id',
     'catalog_id',
     'scope',
     'lifetime_start',
     'lifetime_end',
     'created_at',
     'updated_at',
     'deleted_at',
     'deleted',
     'expansion_key1',
     'expansion_key2',
     'expansion_key3',
     'expansion_key4',
     'expansion_key5',
     'expansion_text']
_print_valid_catalog_columns = \
    ['catalog_id',
     'scope',
     'catalog_name',
     'catalog_lifetime_start',
     'catalog_lifetime_end',
     'catalog_scope_id',
     'catalog_scope_lifetime_start',
     'catalog_scope_lifetime_end',
     'price_seq_no',
     'price',
     'price_lifetime_start',
     'price_lifetime_end']
_print_price_columns = \
    ['catalog_id',
     'scope',
     'seq_no',
     'price',
     'lifetime_start',
     'lifetime_end',
     'created_at',
     'updated_at',
     'deleted_at',
     'deleted',
     'expansion_key1',
     'expansion_key2',
     'expansion_key3',
     'expansion_key4',
     'expansion_key5',
     'expansion_text']


@utils.arg('--file', metavar='<FILE>',
           help='Create workflow pattern have json file.')
@utils.arg('--encode',
           default='utf-8',
           choices=FILE_ENCODE,
           help='Json file encode. If you unset this value, it is UTF-8.')
def do_workflowpattern_create(c, args):
    """Create a new workflow pattern you can access.
    In commandline, output workflow pattern data.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}

    # Check arguments.
    if args is None or not hasattr(args, 'file') or not args.file:
        msg = "too few arguments: file is required"
        utils.exit(msg)

    # Check json file.
    if not os.path.isfile(args.file):
        msg = "invalid arguments: the file dose not exists"
        utils.exit(msg)

    workflow_pattern_string = codecs.open(args.file, 'r', args.encode).read()
    if not utils.validate_json_format(workflow_pattern_string):
        msg = "invalid arguments: the file is not json format string"
        utils.exit(msg)
    wf_pattern_contents = json.loads(workflow_pattern_string, args.encode)

    # Create row data from args.
    fields["wf_pattern_contents"] = wf_pattern_contents

    result_list = []

    # Call client.
    workflowpattern = c.workflowpatterns.create(fields)

    result_list.append(workflowpattern)

    # Show result.
    columns = ['id',
               'code',
               'wf_pattern_contents']
    utils.print_list(result_list, columns)

    return result_list


@utils.arg('--id', metavar='<ID>',
           help='Filter workflow pattern to '
                'those that have this workflow pattern id.')
def do_workflowpattern_delete(c, args):
    """Delete a workflow pattern you can access.
    Admin user only can use the action.
    :param c: call manager.
    :param args: argument options.
    """
    # Check arguments
    if args is None or not hasattr(args, 'id') or not args.id:
        msg = "too few arguments: id is required."
        utils.exit(msg)

    # Call client.
    c.workflowpatterns.delete(args.id)


@utils.arg('--id', metavar='<ID>',
           help='Filter Ticket template to those that have this id.')
def do_tickettemplate_get(c, args):
    """Get ticket template you can access.
    :param c: call manager.
    :param args: argument options.
    """
    # Check arguments
    if args is None or not hasattr(args, 'id') or not args.id:
        msg = "too few arguments: id is required"
        utils.exit(msg)

    # Call Client
    result_list = []

    try:
        result_list.append(c.tickettemplates.get(args.id))
    except exc.NotFound:
        raise exc.CommandError('No data with an ID of %s exists.' % args.id)

    # Show Result
    columns = ['id',
               'ticket_type',
               'template_contents', 'workflow_pattern_id']
    utils.print_list(result_list, columns)


@utils.arg('--limit', metavar='<LIMIT>', type=int,
           help='Maximum number of ticket template at once.')
@utils.arg('--marker', metavar='<MARKER>',
           help='Get start position of id. this value less get target.')
@utils.arg('--sort-key', default='id',
           choices=afloclient.v1.tickettemplates.SORT_KEY_VALUES,
           help='Sort Ticket template list by specified field.')
@utils.arg('--sort-dir', default='asc',
           choices=afloclient.v1.tickettemplates.SORT_DIR_VALUES,
           help='Sort Ticket template list in specified direction.')
@utils.arg('--enable-expansion-filters',
           metavar='<ENABLE_EXPANSION_FILTERS>',
           help='Whether to use the extension filter or not.')
@utils.arg('--force-show-deleted', metavar='<FORCE_SHOW_DELETED>',
           help='Get deleted Ticket template. Admin user can use this option.')
@utils.arg('--ticket-type', metavar='<TICKET_TYPE>',
           help='Filter ticket to those '
           'that have this ticket type.'
           'When a comma is contain in a value,'
           'the ticket_type condition '
           'is connected in OR.')
def do_tickettemplate_list(c, args):
    """List ticket template you can access.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}

    # Filter out None values from args.
    if args:
        fields = \
            dict(filter(lambda x: x[1] is not None
                        and x[0] in {"limit", "marker",
                                     "sort_key", "sort_dir",
                                     "enable_expansion_filters",
                                     "force_show_deleted",
                                     "ticket_type"},
                        vars(args).items()))
    if hasattr(args, "sort_key") and args.sort_key:
        fields["sort_key"] = [fields["sort_key"]]
    if hasattr(args, "sort_dir") and args.sort_dir:
        fields["sort_dir"] = [fields["sort_dir"]]

    # Call Client
    result_list = c.tickettemplates.list(fields)

    # Show Result
    columns = ['id',
               'ticket_type',
               'template_contents', 'workflow_pattern_id']
    utils.print_list(result_list, columns)


@utils.arg('--file', metavar='<FILE>',
           help='Create ticket template have json file.')
@utils.arg('--encode',
           default='utf-8',
           choices=FILE_ENCODE,
           help='Json file encode. If you unset this value, it is UTF-8.')
def do_tickettemplate_create(c, args):
    """Create a new ticket template you can access.
    In commandline, output ticket template data.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}

    # Check arguments.
    if args is None or not hasattr(args, 'file') or not args.file:
        msg = "too few arguments: file is required"
        utils.exit(msg)

    # Check json file.
    if not os.path.isfile(args.file):
        msg = "invalid arguments: the file dose not exists"
        utils.exit(msg)

    template_contents_string = codecs.open(args.file, 'r', args.encode).read()
    if not utils.validate_json_format(template_contents_string):
        msg = "invalid arguments: the file is not json format string"
        utils.exit(msg)
    template_contents = json.loads(template_contents_string, args.encode)

    # Create row data from args.
    fields["template_contents"] = template_contents

    result_list = []

    # Call client.
    tickettemplate = c.tickettemplates.create(fields)

    result_list.append(tickettemplate)

    # Show result.
    columns = ['id',
               'ticket_type',
               'template_contents', 'workflow_pattern_id']
    utils.print_list(result_list, columns)

    return result_list


@utils.arg('--id', metavar='<ID>',
           help='Filter ticket template to '
                'those that have this ticket template id.')
def do_tickettemplate_delete(c, args):
    """Delete a ticket template you can access.
    Admin user only can use the action.
    :param c: call manager.
    :param args: argument options.
    """
    # Check arguments
    if args is None or not hasattr(args, 'id') or not args.id:
        msg = "too few arguments: id is required."
        utils.exit(msg)

    # Call client.
    c.tickettemplates.delete(args.id)


@utils.arg('--id', metavar='<ID>',
           help='Filter ticket to those that have this id.')
def do_ticket_get(c, args):
    """Get ticket you can access.
    In commandline, output ticket data.
    Don't output workflow data.
    :param c: call manager.
    :param args: argument options.
    """
    # Check arguments
    if args is None or args.id is None:
        msg = "too few arguments: id is required"
        utils.exit(msg)

    result_list = []

    # Call Client
    try:
        ticket = c.tickets.get(args.id)

        result_list.append(ticket)

    except exc.NotFound:
        raise exc.CommandError('No data with an ID of %s exists.' % args.id)

    # Show Result
    utils.print_list(result_list, _print_ticket_columns)


@utils.arg('--tenant-id', metavar='<TENANT_ID>',
           help='Filter ticket to those that have this tenant id.')
@utils.arg('--last-status-code', metavar='<LAST_STATUS_CODE>',
           help='Filter ticket to those that have this last status code.')
@utils.arg('--ticket-template-id', metavar='<TICKET_TEMPLATE_ID>',
           help='Filter ticket to those that have this ticket template id.')
@utils.arg('--ticket-type', metavar='<TICKET_TYPE>',
           help='Filter ticket to those that have this ticket type.')
@utils.arg('--target-id', metavar='<TARGET_ID>',
           help='Filter ticket to those that have this target id.')
@utils.arg('--owner-at-from', metavar='<OWNER_AT_FROM>',
           help='Filter ticket to those that have this owner from date.')
@utils.arg('--owner-at-to', metavar='<OWNER_AT_TO>',
           help='Filter ticket to those that have this owner to date.')
@utils.arg('--owner-id', metavar='<OWNER_ID>',
           help='Filter ticket to those that have this owner id.')
@utils.arg('--last-confirmed-at-to', metavar='<LAST_CONFIRMED_AT_TO>',
           help='Filter ticket to those that have this to last confirmed at.')
@utils.arg('--last-confirmed-at-from', metavar='<LAST_CONFIRMED_AT_FROM>',
           help='Filter ticket to those '
           'that have this from last confirmed at.')
@utils.arg('--last-confirmer-id', metavar='<LAST_CONFIRMER_ID>',
           help='Filter ticket to those that have this last confirmer id.')
@utils.arg('--sort-key', default='tenant_id',
           choices=afloclient.v1.tickets.SORT_KEY_VALUES,
           help='Sort ticket list by specified field.')
@utils.arg('--sort-dir', default='asc',
           choices=afloclient.v1.tickets.SORT_DIR_VALUES,
           help='Sort ticket list in specified direction.')
@utils.arg('--limit', metavar='<LIMIT>', type=int,
           help='Maximum number of ticket at once.')
@utils.arg('--marker', metavar='<MARKER>',
           help='Get start position of id. this value less get target.')
@utils.arg('--ticket-template-name', metavar='<TICKET_TEMPLATE_NAME>',
           help='Filter ticket to those that have this ticket template name.')
@utils.arg('--application-kinds-name', metavar='<APPLICATION_KINDS_NAME>',
           help='Filter ticket to those '
           'that have this application kinds name.')
def do_ticket_list(c, args):
    """List ticket you can access.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}

    # Filter out None values from args.
    if args:
        fields = dict(filter(lambda x: x[1] is not None
                             and x[0] in {'tenant_id',
                                          'last_status_code',
                                          'ticket_template_id',
                                          'ticket_type', 'target_id',
                                          'owner_id',
                                          'owner_at_to', 'owner_at_from',
                                          'last_confirmer_id',
                                          'last_confirmed_at_to',
                                          'last_confirmed_at_from',
                                          "tenant_id",
                                          "sort_key", "sort_dir",
                                          "limit", "marker",
                                          "ticket_template_name",
                                          "application_kinds_name"},
                             vars(args).items()))

    # Call Client
    result_list = _join_list_data(c.tickets.list(fields))

    columns = \
        ['id',
         'ticket_template_id',
         'ticket_type', 'target_id',
         'tenant_id',
         'owner_id', 'owner_at',
         'ticket_detail', 'action_detail',
         'last_workflow_id',
         'last_status',
         'last_status_code',
         'last_status_detail',
         'last_target_role',
         'last_confirmer_id', 'last_confirmed_at',
         'last_additional_data']

    # Show Result
    utils.print_list(result_list, columns)


@utils.arg('--ticket-template-id', metavar='<TICKET_TEMPLATE_ID>',
           help='Create ticket from ticket template id.')
@utils.arg('--ticket-detail', metavar='<TICKET_DETAIL>',
           help='Create ticket have detail data<json string>.')
@utils.arg('--status-code', metavar='<STATUS_CODE>',
           help='Create ticket having status code.'
           'Status code is see workflow pattern contents.')
def do_ticket_create(c, args):
    """Create a new ticket you can access.
    In commandline, output ticket data.
    Don't output workflow data.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}

    # Check arguments
    if args is None:
        msg = "too few arguments: ticket id is required"
        utils.exit(msg)

    if not hasattr(args, 'ticket_template_id') or not args.ticket_template_id:
        msg = "too few arguments: id is required"
        utils.exit(msg)

    if hasattr(args, 'ticket_detail') and args.ticket_detail is not None:
        if not utils.validate_json_format(args.ticket_detail):
            msg = "Ticket detail is json format string."
            utils.exit(msg)

    if not hasattr(args, 'status_code') or not args.status_code:
        msg = "too few arguments: status_code is required"
        utils.exit(msg)

    # Create row data from args.
    fields["ticket_template_id"] = args.ticket_template_id
    if hasattr(args, 'ticket_detail') and args.ticket_detail is not None:
        fields["ticket_detail"] = args.ticket_detail
    fields["status_code"] = args.status_code

    result_list = []

    # Call client.
    (ticket, workflows) = c.tickets.create(fields)

    result_list.append(ticket)

    # Show result.
    utils.print_list(result_list, _print_ticket_columns)

    return result_list


@utils.arg('--id', metavar='<ID>',
           help='Filter ticket to those that have this ticket id.')
@utils.arg('--last-workflow-id', metavar='<LAST_WORKFLOW_ID>',
           help='Filter ticket to those ' +
                'that have this last update workflow id.')
@utils.arg('--next-workflow-id', metavar='<NEXT_WORKFLOW_ID>',
           help='Filter ticket to those ' +
                'that have this next update workflow id.')
@utils.arg('--last-status-code', metavar='<LAST_STATUS_CODE>',
           help='Now status value.')
@utils.arg('--next-status-code', metavar='<NEXT_STATUS_CODE>',
           help='You change to status value.')
@utils.arg('--additional-data', metavar='<ADDITIONAL_DATA>',
           help='Update ticket reason.')
def do_ticket_update(c, args):
    """Update a ticket you can access.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}

    # Check arguments
    if args is None:
        msg = "too few arguments"
        utils.exit(msg)
    if not hasattr(args, 'id'):
        msg = "too few arguments: ticket id is required"
        utils.exit(msg)
    if not hasattr(args, 'last_workflow_id'):
        msg = "too few arguments: last workflow id is required"
        utils.exit(msg)
    if not hasattr(args, 'last_status_code'):
        msg = "too few arguments: last status code is required"
        utils.exit(msg)
    if not hasattr(args, 'next_status_code'):
        msg = "too few arguments: next status code is required"
        utils.exit(msg)
    if hasattr(args, 'additional_data') and args.additional_data is not None:
        if not utils.validate_json_format(args.additional_data):
            msg = "Ticket additional data is json format string."
            utils.exit(msg)

    if hasattr(args, 'last_workflow_id'):
        fields['last_workflow_id'] = args.last_workflow_id
    if hasattr(args, 'next_workflow_id'):
        fields['next_workflow_id'] = args.next_workflow_id
    if hasattr(args, 'last_status_code'):
        fields['last_status_code'] = args.last_status_code
    if hasattr(args, 'next_status_code'):
        fields['next_status_code'] = args.next_status_code
    if hasattr(args, 'additional_data'):
        fields['additional_data'] = args.additional_data

    # Call client.
    c.tickets.update(args.id, fields)


@utils.arg('--id', metavar='<ID>',
           help='Filter ticket to those that have this ticket id.')
def do_ticket_delete(c, args):
    """Delete a ticket you can access.
    Admin user only can use the action.
    :param c: call manager.
    :param args: argument options.
    """
    # Check arguments
    if args is None:
        msg = "too few arguments."
        utils.exit(msg)
    if not hasattr(args, 'id') or not args.id:
        msg = "too few arguments: id is required."
        utils.exit(msg)

    # Call client.
    c.tickets.delete(args.id)


@utils.arg('--id', metavar='<ID>',
           help='Filter workflow of the ticket ' +
                'to those that have this ticket id.')
def do_workflow_get(c, args):
    """Get workflow of the ticket you can access.
    In commandline, output workflow data.
    :param c: call manager.
    :param args: argument options.
    """
    # Check arguments
    if args is None:
        msg = "too few arguments."
        utils.exit(msg)
    if not hasattr(args, 'id') or not args.id:
        msg = "too few arguments: id is required."
        utils.exit(msg)

    # Call Client
    try:
        ticket = c.tickets.get(args.id)

        if not ticket:
            raise exc.NotFound

        workflow = ticket.workflow

    except exc.NotFound:
        raise exc.CommandError(
            'No data with an ticket ID of %s exists.' % args.id)

    # Show Result
    utils.print_list(workflow, _print_workflow_columns)


def _join_list_data(tickets):
    """Join ticket, last_workflow, next_workflow to list.
    :param tickets: ticket data, last update workflow data of ticket,
        next confirm workflow data.
    """
    result = []

    if tickets is None or len(tickets) == 0:
        return []

    for data in tickets:
        row = {}
        row['id'] = data.id
        row['ticket_template_id'] = data.ticket_template_id
        row['ticket_type'] = data.ticket_type
        row['target_id'] = data.target_id
        row['tenant_id'] = data.tenant_id
        row['owner_id'] = data.owner_id
        row['owner_at'] = data.owner_at
        row['ticket_detail'] = data.ticket_detail
        row['action_detail'] = data.action_detail

        last = data.last_workflow
        row['last_workflow_id'] = last['id'] \
            if last is not None else None
        row['last_status'] = last['status'] \
            if last is not None else None
        row['last_status_code'] = last['status_code'] \
            if last is not None else None
        row['last_status_detail'] = last['status_detail'] \
            if last is not None else None
        row['last_target_role'] = last['target_role'] \
            if last is not None else None
        row['last_confirmer_id'] = last['confirmer_id'] \
            if last is not None else None
        row['last_confirmed_at'] = last['confirmed_at'] \
            if last is not None else None
        row['last_additional_data'] = last['additional_data'] \
            if last is not None else None

        result.append(row)

    return result


@utils.arg('--project-id',
           metavar='<PROJECT_ID>',
           help='Create project id of contract.')
@utils.arg('--region-id',
           metavar='<REGION_ID>',
           help='Create region id of contract.')
@utils.arg('--project-name',
           metavar='<PROJECT_NAME>',
           help='Create project name of contract.')
@utils.arg('--catalog-id',
           metavar='<CATALOG_ID>',
           help='Create catalog id of contract.')
@utils.arg('--catalog-name',
           metavar='<CATALOG_NAME>',
           help='Create catalog name of contract.')
@utils.arg('--num',
           metavar='<NUM>',
           help='Create num of contract.')
@utils.arg('--parent-ticket-template-id',
           metavar='<PARENT_TICKET_TEMPLATE_ID>',
           help='Create parent ticket template id of contract.')
@utils.arg('--ticket-template-id',
           metavar='<TICKET_TEMPLATE_ID>',
           help='Create ticket template id of contract.')
@utils.arg('--parent-ticket-template-name',
           metavar='<PARENT_TICKET_TEMPLATE_NAME>',
           help='Create parent ticket template name of contract.')
@utils.arg('--parent-application-kinds-name',
           metavar='<PARENT_APPLICATION_KINDS_NAME>',
           help='Create parent application kinds name of contract.')
@utils.arg('--application-kinds-name',
           metavar='<APPLICATION_KINDS_NAME>',
           help='Create application kinds name of contract.')
@utils.arg('--cancel-application-id',
           metavar='<CANCEL_APPLICATION_ID>',
           help='Create cancel application id of contract.')
@utils.arg('--application-id',
           metavar='<APPLICATION_ID>',
           help='Create application_id of contract.')
@utils.arg('--ticket-template-name',
           metavar='<TICKET_TEMPLATE_NAME>',
           help='Create ticket template name of contract.')
@utils.arg('--application-name',
           metavar='<APPLICATION_NAME>',
           help='Create application name of contract.')
@utils.arg('--application-date',
           metavar='<APPLICATION_DATE>',
           help='Create application date of contract.')
@utils.arg('--parent-contract-id',
           metavar='<PARENT_CONTRACT_ID>',
           help='Create parent contract id of contract.')
@utils.arg('--lifetime-start',
           metavar='<LIFETIME_START>',
           help='Create lifetime start of contract.')
@utils.arg('--lifetime-end',
           metavar='<LIFETIME_END>',
           help='Create lifetime end of contract.')
@utils.arg('--expansion-key1',
           metavar='<EXPANSION_KEY1>',
           help='Reserved area 1.')
@utils.arg('--expansion-key2',
           metavar='<EXPANSION_KEY2>',
           help='Reserved area 2.')
@utils.arg('--expansion-key3',
           metavar='<EXPANSION_KEY3>',
           help='Reserved area 3.')
@utils.arg('--expansion-key4',
           metavar='<EXPANSION_KEY4>',
           help='Reserved area 4.')
@utils.arg('--expansion-key5',
           metavar='<EXPANSION_KEY5>',
           help='Reserved area 5.')
@utils.arg('--expansion-text',
           metavar='<EXPANSION_TEXT>',
           help='Reserved area for big data.')
def do_contract_create(c, args):
    """Create a new contract you can access.
    :param c: call manager.
    :param args: argument options.
    """

    if args is None:
        msg = "No Inputed contract args."
        utils.exit(msg)

    contract = {}
    expansions = {}
    expansions_text = {}

    contract['project_id'] = args.project_id \
        if hasattr(args, 'project_id') and args.project_id else None
    contract['region_id'] = args.region_id \
        if hasattr(args, 'region_id') and args.region_id else None
    contract['project_name'] = args.project_name \
        if hasattr(args, 'project_name') and args.project_name else None
    contract['catalog_id'] = args.catalog_id \
        if hasattr(args, 'catalog_id') and args.catalog_id else None
    contract['catalog_name'] = args.catalog_name \
        if hasattr(args, 'catalog_name') and args.catalog_name else None
    contract['num'] = int(args.num) \
        if hasattr(args, 'num') and args.num else None
    contract['parent_ticket_template_id'] = args.parent_ticket_template_id \
        if hasattr(args, 'parent_ticket_template_id') and \
        args.parent_ticket_template_id else None
    contract['ticket_template_id'] = args.ticket_template_id \
        if hasattr(args, 'ticket_template_id') and \
        args.ticket_template_id else None
    contract['parent_ticket_template_name'] = \
        args.parent_ticket_template_name \
        if hasattr(args, 'parent_ticket_template_name') and \
        args.parent_ticket_template_name else None
    contract['parent_application_kinds_name'] = \
        args.parent_application_kinds_name \
        if hasattr(args, 'parent_application_kinds_name') and \
        args.parent_application_kinds_name else None
    contract['application_kinds_name'] = args.application_kinds_name \
        if hasattr(args, 'application_kinds_name') and \
        args.application_kinds_name else None
    contract['cancel_application_id'] = args.cancel_application_id \
        if hasattr(args, 'cancel_application_id') and \
        args.cancel_application_id else None
    contract['application_id'] = args.application_id \
        if hasattr(args, 'application_id') and args.application_id else None
    contract['ticket_template_name'] = args.ticket_template_name \
        if hasattr(args, 'ticket_template_name') and \
        args.ticket_template_name else None
    contract['application_name'] = args.application_name \
        if hasattr(args, 'application_name') and \
        args.application_name else None
    contract['application_date'] = args.application_date \
        if hasattr(args, 'application_date') and \
        args.application_date else None
    contract['parent_contract_id'] = args.parent_contract_id \
        if hasattr(args, 'parent_contract_id') and \
        args.parent_contract_id else None
    contract['lifetime_start'] = args.lifetime_start \
        if hasattr(args, 'lifetime_start') and args.lifetime_start else None
    contract['lifetime_end'] = args.lifetime_end \
        if hasattr(args, 'lifetime_end') and args.lifetime_end else None
    expansions['expansion_key1'] = args.expansion_key1 \
        if hasattr(args, 'expansion_key1') and args.expansion_key1 else None
    expansions['expansion_key2'] = args.expansion_key2 \
        if hasattr(args, 'expansion_key2') and args.expansion_key2 else None
    expansions['expansion_key3'] = args.expansion_key3 \
        if hasattr(args, 'expansion_key3') and args.expansion_key3 else None
    expansions['expansion_key4'] = args.expansion_key4 \
        if hasattr(args, 'expansion_key4') and args.expansion_key4 else None
    expansions['expansion_key5'] = args.expansion_key5 \
        if hasattr(args, 'expansion_key5') and args.expansion_key5 else None
    expansions_text['expansion_text'] = args.expansion_text \
        if hasattr(args, 'expansion_text') and args.expansion_text else None

    if expansions:
        contract['expansions'] = expansions
    if expansions_text:
        contract['expansions_text'] = expansions_text

    result_list = []

    data = c.contracts.create(contract)
    if data:
        row = {}
        row['contract_id'] = data.contract_id
        row['region_id'] = data.region_id
        row['project_id'] = data.project_id
        row['project_name'] = data.project_name
        row['catalog_id'] = data.catalog_id
        row['catalog_name'] = data.catalog_name
        row['num'] = data.num
        row['parent_ticket_template_id'] = data.parent_ticket_template_id
        row['ticket_template_id'] = data.ticket_template_id
        row['parent_ticket_template_name'] = data.parent_ticket_template_name
        row['ticket_template_name'] = data.ticket_template_name
        row['parent_application_kinds_name'] = \
            data.parent_application_kinds_name
        row['application_kinds_name'] = data.application_kinds_name
        row['cancel_application_id'] = data.cancel_application_id
        row['application_id'] = data.application_id
        row['application_name'] = data.application_name
        row['application_date'] = data.application_date
        row['parent_contract_id'] = data.parent_contract_id
        row['lifetime_start'] = data.lifetime_start
        row['lifetime_end'] = data.lifetime_end
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    utils.print_list(result_list, _print_contract_columns)

    return result_list


@utils.arg('--contract-id', metavar='<CONTRACT_ID>',
           help='Filter contract to those that have this contract id.')
@utils.arg('--project-id',
           metavar='<PROJECT_ID>',
           help='Update project id of contract.')
@utils.arg('--region-id',
           metavar='<REGION_ID>',
           help='Update region id of contract.')
@utils.arg('--project-name',
           metavar='<PROJECT_NAME>',
           help='Update project name of contract.')
@utils.arg('--catalog-id',
           metavar='<CATALOG_ID>',
           help='Update catalog id of contract.')
@utils.arg('--catalog-name',
           metavar='<CATALOG_NAME>',
           help='Update catalog name of contract.')
@utils.arg('--num',
           metavar='<NUM>',
           help='Update number of contract.')
@utils.arg('--parent-ticket-template-id',
           metavar='<PARENT_TICKET_TEMPLATE_ID>',
           help='Update parent ticket template id of contract.')
@utils.arg('--ticket-template-id',
           metavar='<TICKET_TEMPLATE_ID>',
           help='Update ticket template id of contract.')
@utils.arg('--parent-ticket-template-name',
           metavar='<PARENT_TICKET_TEMPLATE_NAME>',
           help='Update parent ticket template name of contract.')
@utils.arg('--parent-application-kinds-name',
           metavar='<PARENT_APPLICATION_KINDS_NAME>',
           help='Update parent application kinds name of contract.')
@utils.arg('--application-kinds-name',
           metavar='<APPLICATION_KINDS_NAME>',
           help='Update application kinds name of contract.')
@utils.arg('--cancel-application-id',
           metavar='<CANCEL_APPLICATION_ID>',
           help='Update cancel application id of contract.')
@utils.arg('--application-id',
           metavar='<APPLICATION_ID>',
           help='Update application id of contract.')
@utils.arg('--ticket-template-name',
           metavar='<TICKET_TEMPLATE_NAME>',
           help='Update application type of contract.')
@utils.arg('--application-name',
           metavar='<APPLICATION_NAME>',
           help='Update application name of contract.')
@utils.arg('--application-date',
           metavar='<APPLICATION_DATE>',
           help='Update application date of contract.')
@utils.arg('--parent-contract-id',
           metavar='<PARENT_CONTRACT_ID>',
           help='Update parent contract id of contract.')
@utils.arg('--lifetime-start',
           metavar='<LIFETIME_START>',
           help='Update lifetime start of contract.')
@utils.arg('--lifetime-end',
           metavar='<LIFETIME_END>',
           help='Update lifetime end of contract.')
@utils.arg('--expansion-key1',
           metavar='<EXPANSION_KEY1>',
           help='Reserved area 1.')
@utils.arg('--expansion-key2',
           metavar='<EXPANSION_KEY2>',
           help='Reserved area 2.')
@utils.arg('--expansion-key3',
           metavar='<EXPANSION_KEY3>',
           help='Reserved area 3.')
@utils.arg('--expansion-key4',
           metavar='<EXPANSION_KEY4>',
           help='Reserved area 4.')
@utils.arg('--expansion-key5',
           metavar='<EXPANSION_KEY5>',
           help='Reserved area 5.')
@utils.arg('--expansion-text',
           metavar='<EXPANSION_TEXT>',
           help='Reserved area for big data.')
def do_contract_update(c, args):
    """Update a contract you can access.
    :param c: call manager.
    :param args: argument options.
    """

    if args is None:
        msg = "No Inputed contract args."
        utils.exit(msg)
    if not hasattr(args, 'contract_id') or not args.contract_id:
        msg = "too few arguments: contract_id is required."
        utils.exit(msg)

    contract = {}
    expansions = {}
    expansions_text = {}

    if hasattr(args, 'project_id') and args.project_id is not None:
        contract['project_id'] = args.project_id
    if hasattr(args, 'region_id') and args.region_id is not None:
        contract['region_id'] = args.region_id
    if hasattr(args, 'project_name') and args.project_name is not None:
        contract['project_name'] = args.project_name
    if hasattr(args, 'catalog_id') and args.catalog_id is not None:
        contract['catalog_id'] = args.catalog_id
    if hasattr(args, 'catalog_name') and args.catalog_name is not None:
        contract['catalog_name'] = args.catalog_name
    if hasattr(args, 'num') and args.num is not None:
        contract['num'] = int(args.num)
    if hasattr(args, 'parent_ticket_template_id') and \
       args.parent_ticket_template_id is not None:
        contract['parent_ticket_template_id'] = args.parent_ticket_template_id
    if hasattr(args, 'ticket_template_id') and \
       args.ticket_template_id is not None:
        contract['ticket_template_id'] = args.ticket_template_id
    if hasattr(args, 'parent_ticket_template_name') and \
       args.parent_ticket_template_name is not None:
        contract['parent_ticket_template_name'] = \
            args.parent_ticket_template_name
    if hasattr(args, 'parent_application_kinds_name') and \
       args.parent_application_kinds_name is not None:
        contract['parent_application_kinds_name'] = \
            args.parent_application_kinds_name
    if hasattr(args, 'application_kinds_name') and \
       args.application_kinds_name is not None:
        contract['application_kinds_name'] = args.application_kinds_name
    if hasattr(args, 'cancel_application_id') and \
       args.cancel_application_id is not None:
        contract['cancel_application_id'] = args.cancel_application_id
    if hasattr(args, 'application_id') and args.application_id is not None:
        contract['application_id'] = args.application_id
    if hasattr(args, 'ticket_template_name') and \
       args.ticket_template_name is not None:
        contract['ticket_template_name'] = args.ticket_template_name
    if hasattr(args, 'application_name') and args.application_name is not None:
        contract['application_name'] = args.application_name
    if hasattr(args, 'application_date') and args.application_date is not None:
        contract['application_date'] = args.application_date
    if hasattr(args, 'parent_contract_id') and \
       args.parent_contract_id is not None:
        contract['parent_contract_id'] = args.parent_contract_id
    if hasattr(args, 'lifetime_start') and args.lifetime_start is not None:
        contract['lifetime_start'] = args.lifetime_start
    if hasattr(args, 'lifetime_end') and args.lifetime_end is not None:
        contract['lifetime_end'] = args.lifetime_end
    if hasattr(args, 'expansion_key1') and args.expansion_key1 is not None:
        expansions['expansion_key1'] = args.expansion_key1
    if hasattr(args, 'expansion_key2') and args.expansion_key2 is not None:
        expansions['expansion_key2'] = args.expansion_key2
    if hasattr(args, 'expansion_key3') and args.expansion_key3 is not None:
        expansions['expansion_key3'] = args.expansion_key3
    if hasattr(args, 'expansion_key4') and args.expansion_key4 is not None:
        expansions['expansion_key4'] = args.expansion_key4
    if hasattr(args, 'expansion_key5') and args.expansion_key5 is not None:
        expansions['expansion_key5'] = args.expansion_key5
    if hasattr(args, 'expansion_text') and args.expansion_text is not None:
        expansions_text['expansion_text'] = args.expansion_text

    if expansions:
        contract['expansions'] = expansions
    if expansions_text:
        contract['expansions_text'] = expansions_text

    result_list = []

    data = c.contracts.update(args.contract_id, contract)
    if data:
        row = {}
        row['contract_id'] = data.contract_id
        row['region_id'] = data.region_id
        row['project_id'] = data.project_id
        row['project_name'] = data.project_name
        row['catalog_id'] = data.catalog_id
        row['catalog_name'] = data.catalog_name
        row['num'] = data.num
        row['parent_ticket_template_id'] = data.parent_ticket_template_id
        row['ticket_template_id'] = data.ticket_template_id
        row['parent_ticket_template_name'] = data.parent_ticket_template_name
        row['ticket_template_name'] = data.ticket_template_name
        row['parent_application_kinds_name'] = \
            data.parent_application_kinds_name
        row['application_kinds_name'] = data.application_kinds_name
        row['cancel_application_id'] = data.cancel_application_id
        row['application_id'] = data.application_id
        row['application_name'] = data.application_name
        row['application_date'] = data.application_date
        row['parent_contract_id'] = data.parent_contract_id
        row['lifetime_start'] = data.lifetime_start
        row['lifetime_end'] = data.lifetime_end
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    utils.print_list(result_list, _print_contract_columns)

    return result_list


@utils.arg('--contract-id', metavar='<CONTRACT_ID>',
           help='Filter contract to those that have this contract id.')
def do_contract_get(c, args):
    """Get a contract you can access.
    :param c: call manager.
    :param args: argument options.
    """
    # Check arguments
    if args is None:
        msg = "too few arguments."
        utils.exit(msg)
    if not hasattr(args, 'contract_id') or not args.contract_id:
        msg = "too few arguments: contract_id is required."
        utils.exit(msg)

    result_list = []

    # Call Client
    try:
        data = c.contracts.get(args.contract_id)

    except exc.NotFound:
        raise exc.CommandError(
            'No data with an contract ID of %s exists.' % args.contract_id)

    if data:
        row = {}
        row['contract_id'] = data.contract_id
        row['region_id'] = data.region_id
        row['project_id'] = data.project_id
        row['project_name'] = data.project_name
        row['catalog_id'] = data.catalog_id
        row['catalog_name'] = data.catalog_name
        row['num'] = data.num
        row['parent_ticket_template_id'] = data.parent_ticket_template_id
        row['ticket_template_id'] = data.ticket_template_id
        row['parent_ticket_template_name'] = data.parent_ticket_template_name
        row['ticket_template_name'] = data.ticket_template_name
        row['parent_application_kinds_name'] = \
            data.parent_application_kinds_name
        row['application_kinds_name'] = data.application_kinds_name
        row['cancel_application_id'] = data.cancel_application_id
        row['application_id'] = data.application_id
        row['application_name'] = data.application_name
        row['application_date'] = data.application_date
        row['parent_contract_id'] = data.parent_contract_id
        row['lifetime_start'] = data.lifetime_start
        row['lifetime_end'] = data.lifetime_end
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    # Show Result
    utils.print_list(result_list, _print_contract_columns)


@utils.arg('--contract-id', metavar='<CONTRACT_ID>',
           help='Filter contract to those that have this contract id.')
def do_contract_delete(c, args):
    """Delete a contract you can access.
    :param c: call manager.
    :param args: argument options.
    """
    # Check arguments
    if args is None:
        msg = "too few arguments."
        utils.exit(msg)
    if not hasattr(args, 'contract_id') or not args.contract_id:
        msg = "too few arguments: contract_id is required."
        utils.exit(msg)

    c.contracts.delete(args.contract_id)


@utils.arg('--project-id',
           metavar='<PROJECT_ID>',
           help='Filter contract to those that have this project id.')
@utils.arg('--region-id',
           metavar='<REGION_ID>',
           help='Filter contract to those that have this region id.')
@utils.arg('--project-name',
           metavar='<PROJECT_NAME>',
           help='Filter contract to those that have this project name.')
@utils.arg('--catalog-name',
           metavar='<CATALOG_NAME>',
           help='Filter contract to those that have this catalog name.')
@utils.arg('--application-id',
           metavar='<APPLICATION_ID>',
           help='Filter contract to those that have this application id.')
@utils.arg('--ticket-template-name',
           metavar='<TICKET_TEMPLATE_NAME>',
           help='Filter contract to those that have this ticket template '
                'name.')
@utils.arg('--application-kinds-name',
           metavar='<APPLICATION_KINDS_NAME>',
           help='Filter contract to those that have this application kind '
                'name.')
@utils.arg('--application-name',
           metavar='<APPLICATION_NAME>',
           help='Filter contract to those that have this application name.')
@utils.arg('--parent-contract-id',
           metavar='<PARENT_CONTRACT_ID>',
           help='Filter contract to those that have this parent contract id.')
@utils.arg('--contract-id',
           metavar='<CONTRACT_ID>',
           help='Filter contract to those that have this contract id.')
@utils.arg('--application-date-from',
           metavar='<APPLICATION_DATE_FROM>',
           help='Filter contract to those that from this application date.')
@utils.arg('--application-date-to',
           metavar='<APPLICATION_DATE_TO>',
           help='Filter contract to those that to this application date.')
@utils.arg('--lifetime-start-from',
           metavar='<LIFETIME_START_FROM>',
           help='Filter contract to those that from this lifetime start.')
@utils.arg('--lifetime-start-to',
           metavar='<LIFETIME_START_TO>',
           help='Filter contract to those that to this lifetime start.')
@utils.arg('--lifetime-end-from',
           metavar='<LIFETIME_END_FROM>',
           help='Filter contract to those that from this lifetime end.')
@utils.arg('--lifetime-end-to',
           metavar='<LIFETIME_END_TO>',
           help='Filter contract to those that to this lifetime end.')
@utils.arg('--lifetime',
           metavar='<LIFETIME>',
           help='Filter contract to those '
           'that between lifetime begin and end.')
@utils.arg('--date-in-lifetime',
           metavar='<DATE_IN_LIFETIME>',
           help='Filter contract to those '
           'that between date in lifetime begin and end.')
@utils.arg('--limit',
           metavar='<LIMIT>',
           help='Maximum number of contract at once.')
@utils.arg('--marker',
           metavar='<MARKER>',
           help='Get start position of id. This value less get target.')
@utils.arg('--sort-key',
           choices=afloclient.v1.contracts.SORT_KEY_VALUES,
           help='Sort contract list by specified field.')
@utils.arg('--sort-dir',
           choices=afloclient.v1.contracts.SORT_DIR_VALUES,
           help='Sort contract list in specified direction.')
@utils.arg('--force-show-deleted',
           metavar='<FORCE_SHOW_DELETED>',
           help='Get deleted contract. Admin user can use this option.')
def do_contract_list(c, args):
    """List contract you can access.
    :param c: call manager.
    :param args: Command options.
    """
    fields = {}

    if args:
        fields = dict(filter(lambda x: x[1] and
                             x[0] in {'project_id',
                                      'region_id',
                                      'project_name',
                                      'catalog_name',
                                      'application_id',
                                      'ticket_template_name',
                                      'application_kinds_name',
                                      'application_name',
                                      'parent_contract_id',
                                      'application_date_from',
                                      'application_date_to',
                                      'lifetime_start_from',
                                      'lifetime_start_to',
                                      'lifetime_end_from',
                                      'lifetime_end_to',
                                      'lifetime',
                                      'date_in_lifetime',
                                      'limit',
                                      'marker',
                                      'sort_key',
                                      'sort_dir',
                                      'force_show_deleted'},
                             vars(args).items()))

    # Call Client
    contract_refs = c.contracts.list(fields)
    result_list = []
    for data in contract_refs:
        row = {}
        row['contract_id'] = data.contract_id
        row['region_id'] = data.region_id
        row['project_id'] = data.project_id
        row['project_name'] = data.project_name
        row['catalog_id'] = data.catalog_id
        row['catalog_name'] = data.catalog_name
        row['num'] = data.num
        row['parent_ticket_template_id'] = data.parent_ticket_template_id
        row['ticket_template_id'] = data.ticket_template_id
        row['parent_ticket_template_name'] = data.parent_ticket_template_name
        row['ticket_template_name'] = data.ticket_template_name
        row['parent_application_kinds_name'] = \
            data.parent_application_kinds_name
        row['application_kinds_name'] = data.application_kinds_name
        row['cancel_application_id'] = data.cancel_application_id
        row['application_id'] = data.application_id
        row['application_name'] = data.application_name
        row['application_date'] = data.application_date
        row['parent_contract_id'] = data.parent_contract_id
        row['lifetime_start'] = data.lifetime_start
        row['lifetime_end'] = data.lifetime_end
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    utils.print_list(result_list, _print_contract_columns)


@utils.arg('--region-id', metavar='<REGION_ID>',
           help='Create goods that can be used by the region id.')
@utils.arg('--goods-name', metavar='<GOODS_NAME>',
           help='Create goods in this name.')
@utils.arg('--expansion-key1', metavar='<EXPANSION_KEY1>',
           help='Reserved area 1.')
@utils.arg('--expansion-key2', metavar='<EXPANSION_KEY2>',
           help='Reserved area 2.')
@utils.arg('--expansion-key3', metavar='<EXPANSION_KEY3>',
           help='Reserved area 3.')
@utils.arg('--expansion-key4', metavar='<EXPANSION_KEY4>',
           help='Reserved area 4.')
@utils.arg('--expansion-key5', metavar='<EXPANSION_KEY5>',
           help='Reserved area 5.')
@utils.arg('--expansion-text', metavar='<EXPANSION_TEXT>',
           help='Reserved area for big data.')
def do_goods_create(c, args):
    """Create a new goods you can access.
    In commandline, output goods data.
    Don't output workflow data.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}
    expansions = {}
    expansions_text = {}

    # Check arguments
    if hasattr(args, 'region_id'):
        fields["region_id"] = args.region_id
    if hasattr(args, 'goods_name'):
        fields["goods_name"] = args.goods_name
    if hasattr(args, 'expansion_key1') and args.expansion_key1 is not None:
        expansions['expansion_key1'] = args.expansion_key1
    if hasattr(args, 'expansion_key2') and args.expansion_key2 is not None:
        expansions['expansion_key2'] = args.expansion_key2
    if hasattr(args, 'expansion_key3') and args.expansion_key3 is not None:
        expansions['expansion_key3'] = args.expansion_key3
    if hasattr(args, 'expansion_key4') and args.expansion_key4 is not None:
        expansions['expansion_key4'] = args.expansion_key4
    if hasattr(args, 'expansion_key5') and args.expansion_key5 is not None:
        expansions['expansion_key5'] = args.expansion_key5
    if hasattr(args, 'expansion_text') and args.expansion_text is not None:
        expansions_text['expansion_text'] = args.expansion_text

    if expansions:
        fields['expansions'] = expansions
    if expansions_text:
        fields['expansions_text'] = expansions_text

    result_list = []

    # Call client.
    data = c.goods.create(fields)

    if data:
        row = {}
        row['goods_id'] = data.goods_id
        row['region_id'] = data.region_id
        row['goods_name'] = data.goods_name
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    # Show result.
    utils.print_list(result_list, _print_goods_columns)

    return result_list


@utils.arg('--goods-id', metavar='<GOODS_ID>',
           help='Filter goods to those that have this goods id.')
@utils.arg('--region-id',
           metavar='<REGION_ID>',
           help='Update region id of goods.')
@utils.arg('--goods-name',
           metavar='<GODOS_NAME>',
           help='Update goods name of goods.')
@utils.arg('--expansion-key1',
           metavar='<EXPANSION_KEY1>',
           help='Reserved area 1.')
@utils.arg('--expansion-key2',
           metavar='<EXPANSION_KEY2>',
           help='Reserved area 2.')
@utils.arg('--expansion-key3',
           metavar='<EXPANSION_KEY3>',
           help='Reserved area 3.')
@utils.arg('--expansion-key4',
           metavar='<EXPANSION_KEY4>',
           help='Reserved area 4.')
@utils.arg('--expansion-key5',
           metavar='<EXPANSION_KEY5>',
           help='Reserved area 5.')
@utils.arg('--expansion-text',
           metavar='<EXPANSION_TEXT>',
           help='Reserved area for big data.')
def do_goods_update(c, args):
    """Update a goods you can access.
    :param c: call manager.
    :param args: argument options.
    """
    if args is None:
        msg = "No Inputed goods args."
        utils.exit(msg)
    if not hasattr(args, 'goods_id') or not args.goods_id:
        msg = "too few arguments: goods_id is required."
        utils.exit(msg)

    goods = {}
    expansions = {}
    expansions_text = {}

    if hasattr(args, 'region_id') and args.region_id is not None:
        goods['region_id'] = args.region_id
    if hasattr(args, 'goods_name') and args.goods_name is not None:
        goods['goods_name'] = args.goods_name
    if hasattr(args, 'expansion_key1') and args.expansion_key1 is not None:
        expansions['expansion_key1'] = args.expansion_key1
    if hasattr(args, 'expansion_key2') and args.expansion_key2 is not None:
        expansions['expansion_key2'] = args.expansion_key2
    if hasattr(args, 'expansion_key3') and args.expansion_key3 is not None:
        expansions['expansion_key3'] = args.expansion_key3
    if hasattr(args, 'expansion_key4') and args.expansion_key4 is not None:
        expansions['expansion_key4'] = args.expansion_key4
    if hasattr(args, 'expansion_key5') and args.expansion_key5 is not None:
        expansions['expansion_key5'] = args.expansion_key5
    if hasattr(args, 'expansion_text') and args.expansion_text is not None:
        expansions_text['expansion_text'] = args.expansion_text

    if expansions:
        goods['expansions'] = expansions
    if expansions_text:
        goods['expansions_text'] = expansions_text

    result_list = []

    data = c.goods.update(args.goods_id, goods)
    if data:
        row = {}
        row['goods_id'] = data.goods_id
        row['region_id'] = data.region_id
        row['goods_name'] = data.goods_name
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    utils.print_list(result_list, _print_goods_columns)

    return result_list


@utils.arg('--region-id',
           metavar='<REGION_ID>',
           help='Filter goods to those that have this region id.')
@utils.arg('--limit', metavar='<LIMIT>', type=int,
           help='Maximum number of goods at once.')
@utils.arg('--marker',
           metavar='<MARKER>',
           help='Get start position of id. This value less get target.')
@utils.arg('--sort-key',
           choices=afloclient.v1.goods.SORT_KEY_VALUES,
           help='Sort goods list by specified field.')
@utils.arg('--sort-dir',
           choices=afloclient.v1.goods.SORT_DIR_VALUES,
           help='Sort goods list in specified direction.')
@utils.arg('--force-show-deleted',
           metavar='<FORCE_SHOW_DELETED>',
           help='Get deleted goods. Admin user can use this option.')
def do_goods_list(c, args):
    """List goods you can access.
    :param c: call manager.
    :param args: Command options.
    """
    fields = {}

    if args:
        fields = dict(filter(lambda x: x[1] and
                             x[0] in {'region_id',
                                      'limit',
                                      'marker',
                                      'sort_key',
                                      'sort_dir',
                                      'force_show_deleted'},
                             vars(args).items()))

    # Call Client
    goods_refs = c.goods.list(fields)
    goods_list = []
    for data in goods_refs:
        row = {}
        row['goods_id'] = data.goods_id
        row['region_id'] = data.region_id
        row['goods_name'] = data.goods_name
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        goods_list.append(row)

    utils.print_list(goods_list, _print_goods_columns)


@utils.arg('--goods-id', metavar='<GOODS_ID>',
           help='Filter goods to those that have this goods id.')
def do_goods_get(c, args):
    """Get a goods you can access.
    :param c: call manager.
    :param args: argument options.
    """
    # Check arguments
    if args is None:
        msg = "too few arguments."
        utils.exit(msg)
    if not hasattr(args, 'goods_id') or not args.goods_id:
        msg = "too few arguments: goods_id is required."
        utils.exit(msg)

    result_list = []

    # Call Client
    try:
        data = c.goods.get(args.goods_id)

    except exc.NotFound:
        raise exc.CommandError(
            'No data with an goods id of %s exists.' % args.goods_id)

    if data:
        row = {}
        row['goods_id'] = data.goods_id
        row['region_id'] = data.region_id
        row['goods_name'] = data.goods_name
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    # Show Result
    utils.print_list(result_list, _print_goods_columns)


@utils.arg('--goods-id', metavar='<GOODS_ID>',
           help='Filter goods to those that have this goods id.')
def do_goods_delete(c, args):
    """Delete Goods.
    :param c: call manager.
    :param args: argument options.
    """
    # Check arguments
    if args is None:
        msg = "too few arguments: goods_id is required."
        utils.exit(msg)
    if not hasattr(args, 'goods_id') or not args.goods_id:
        msg = "too few arguments: goods_id is required."
        utils.exit(msg)

    c.goods.delete(args.goods_id)


@utils.arg('--region-id', metavar='<REGION_ID>',
           help='Create catalog that can be used by the region id.')
@utils.arg('--catalog-name', metavar='<CATALOG_NAME>',
           help='Create catalog in this name.')
@utils.arg('--lifetime-start', metavar='<LIFETIME_START>',
           help='Create lifetime start of catalog.')
@utils.arg('--lifetime-end', metavar='<LIFETIME_END>',
           help='Create lifetime end of catalog.')
@utils.arg('--expansion-key1', metavar='<EXPANSION_KEY1>',
           help='Reserved area 1.')
@utils.arg('--expansion-key2', metavar='<EXPANSION_KEY2>',
           help='Reserved area 2.')
@utils.arg('--expansion-key3', metavar='<EXPANSION_KEY3>',
           help='Reserved area 3.')
@utils.arg('--expansion-key4', metavar='<EXPANSION_KEY4>',
           help='Reserved area 4.')
@utils.arg('--expansion-key5', metavar='<EXPANSION_KEY5>',
           help='Reserved area 5.')
@utils.arg('--expansion-text', metavar='<EXPANSION_TEXT>',
           help='Reserved area for big data.')
def do_catalog_create(c, args):
    """Create a new catalog you can access.
    In commandline, output catalog data.
    Don't output workflow data.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}
    expansions = {}
    expansions_text = {}

    # Check arguments
    if hasattr(args, 'region_id'):
        fields["region_id"] = args.region_id
    if hasattr(args, 'catalog_name'):
        fields["catalog_name"] = args.catalog_name
    if hasattr(args, 'lifetime_start'):
        fields["lifetime_start"] = args.lifetime_start
    if hasattr(args, 'lifetime_end'):
        fields["lifetime_end"] = args.lifetime_end
    if hasattr(args, 'expansion_key1') and args.expansion_key1 is not None:
        expansions['expansion_key1'] = args.expansion_key1
    if hasattr(args, 'expansion_key2') and args.expansion_key2 is not None:
        expansions['expansion_key2'] = args.expansion_key2
    if hasattr(args, 'expansion_key3') and args.expansion_key3 is not None:
        expansions['expansion_key3'] = args.expansion_key3
    if hasattr(args, 'expansion_key4') and args.expansion_key4 is not None:
        expansions['expansion_key4'] = args.expansion_key4
    if hasattr(args, 'expansion_key5') and args.expansion_key5 is not None:
        expansions['expansion_key5'] = args.expansion_key5
    if hasattr(args, 'expansion_text') and args.expansion_text is not None:
        expansions_text['expansion_text'] = args.expansion_text

    if expansions:
        fields['expansions'] = expansions
    if expansions_text:
        fields['expansions_text'] = expansions_text

    result_list = []

    # Call client.
    data = c.catalogs.create(fields)

    if data:
        row = {}
        row['catalog_id'] = data.catalog_id
        row['region_id'] = data.region_id
        row['catalog_name'] = data.catalog_name
        row['lifetime_start'] = data.lifetime_start
        row['lifetime_end'] = data.lifetime_end
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    # Show result.
    utils.print_list(result_list, _print_catalog_columns)

    return result_list


@utils.arg('--catalog-id', metavar='<CATALOG_ID>',
           help='Filter catalog to those that have this catalog id.')
@utils.arg('--region-id', metavar='<REGION_ID>',
           help='Update region id of catalog.')
@utils.arg('--catalog-name',
           metavar='<CATALOG_NAME>',
           help='Update catalog name of catalog.')
@utils.arg('--lifetime-start',
           metavar='<LIFETIME_START>',
           help='Update lifetime start of catalog.')
@utils.arg('--lifetime-end',
           metavar='<LIFETIME_END>',
           help='Update lifetime end of catalog.')
@utils.arg('--expansion-key1',
           metavar='<EXPANSION_KEY1>',
           help='Reserved area 1.')
@utils.arg('--expansion-key2',
           metavar='<EXPANSION_KEY2>',
           help='Reserved area 2.')
@utils.arg('--expansion-key3',
           metavar='<EXPANSION_KEY3>',
           help='Reserved area 3.')
@utils.arg('--expansion-key4',
           metavar='<EXPANSION_KEY4>',
           help='Reserved area 4.')
@utils.arg('--expansion-key5',
           metavar='<EXPANSION_KEY5>',
           help='Reserved area 5.')
@utils.arg('--expansion-text',
           metavar='<EXPANSION_TEXT>',
           help='Reserved area for big data.')
def do_catalog_update(c, args):
    """Update a catalog you can access.
    :param c: call manager.
    :param args: argument options.
    """
    if args is None:
        msg = "No Inputed catalog args."
        utils.exit(msg)
    if not hasattr(args, 'catalog_id') or not args.catalog_id:
        msg = "too few arguments: catalog_id is required."
        utils.exit(msg)

    catalog = {}
    expansions = {}
    expansions_text = {}

    if hasattr(args, 'region_id') and args.region_id is not None:
        catalog['region_id'] = args.region_id
    if hasattr(args, 'catalog_name') and args.catalog_name is not None:
        catalog['catalog_name'] = args.catalog_name
    if hasattr(args, 'lifetime_start') and args.lifetime_start is not None:
        catalog['lifetime_start'] = args.lifetime_start
    if hasattr(args, 'lifetime_end') and args.lifetime_end is not None:
        catalog['lifetime_end'] = args.lifetime_end
    if hasattr(args, 'expansion_key1') and args.expansion_key1 is not None:
        expansions['expansion_key1'] = args.expansion_key1
    if hasattr(args, 'expansion_key2') and args.expansion_key2 is not None:
        expansions['expansion_key2'] = args.expansion_key2
    if hasattr(args, 'expansion_key3') and args.expansion_key3 is not None:
        expansions['expansion_key3'] = args.expansion_key3
    if hasattr(args, 'expansion_key4') and args.expansion_key4 is not None:
        expansions['expansion_key4'] = args.expansion_key4
    if hasattr(args, 'expansion_key5') and args.expansion_key5 is not None:
        expansions['expansion_key5'] = args.expansion_key5
    if hasattr(args, 'expansion_text') and args.expansion_text is not None:
        expansions_text['expansion_text'] = args.expansion_text

    if expansions:
        catalog['expansions'] = expansions
    if expansions_text:
        catalog['expansions_text'] = expansions_text

    result_list = []

    data = c.catalogs.update(args.catalog_id, catalog)

    if data:
        row = {}
        row['catalog_id'] = data.catalog_id
        row['region_id'] = data.region_id
        row['catalog_name'] = data.catalog_name
        row['lifetime_start'] = data.lifetime_start
        row['lifetime_end'] = data.lifetime_end
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    utils.print_list(result_list, _print_catalog_columns)

    return result_list


@utils.arg('--catalog-id', metavar='<CATALOG_ID>',
           help='Filter catalog to those that have this catalog id.')
def do_catalog_get(c, args):
    """Get a catalog you can access.
    In commandline, output catalog data.
    :param c: call manager.
    :param args: argument options.
    """
    # Check arguments
    if args is None or args.catalog_id is None:
        msg = "too few arguments: catalog_id is required"
        utils.exit(msg)

    result_list = []

    # Call Client
    try:
        data = c.catalogs.get(args.catalog_id)

    except exc.NotFound:
        raise exc.CommandError('No data with an catalog_id of %s exists.' %
                               args.catalog_id)

    if data:
        row = {}
        row['catalog_id'] = data.catalog_id
        row['region_id'] = data.region_id
        row['catalog_name'] = data.catalog_name
        row['lifetime_start'] = data.lifetime_start
        row['lifetime_end'] = data.lifetime_end
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    # Show Result
    utils.print_list(result_list, _print_catalog_columns)


@utils.arg('--catalog-id', metavar='<CATALOG_ID>',
           help='Filter catalog to those that have this catalog id.')
@utils.arg('--region-id', metavar='<REGION_ID>',
           help='Create catalog that can be used by the region id.')
@utils.arg('--catalog-name', metavar='<CATALOG_NAME>',
           help='Create catalog in this name.')
@utils.arg('--lifetime', metavar='<LIFETIME>',
           help='Filter catalog to those that have this lifetime.')
@utils.arg('--sort-key', default='catalog_id',
           choices=afloclient.v1.catalogs.SORT_KEY_VALUES,
           help='Sort catalog list by specified field.')
@utils.arg('--sort-dir', default='asc',
           choices=afloclient.v1.catalogs.SORT_DIR_VALUES,
           help='Sort catalog list in specified direction.')
@utils.arg('--limit', metavar='<LIMIT>', type=int,
           help='Maximum number of catalog at once.')
@utils.arg('--marker', metavar='<MARKER>',
           help='Get start position of id. This value less get target.')
@utils.arg('--force-show-deleted', metavar='<FORCE_SHOW_DELETED>',
           help='Get deleted catalog. Admin user can use this option.')
def do_catalog_list(c, args):
    """List catalog you can access.
    :param c: call manager.
    :param args: argument options.
    """

    fields = {}

    # Filter out None values from args.
    if args:
        fields = dict(filter(lambda x: x[1] is not None
                             and x[0] in {'catalog_id', 'region_id',
                                          'catalog_name', 'lifetime',
                                          'sort_key', 'sort_dir',
                                          'limit', 'marker',
                                          'force_show_deleted'},
                             vars(args).items()))

    # Call Client
    catalog = c.catalogs.list(fields)

    result_list = []

    for data in catalog:
        row = {}
        row['catalog_id'] = data.catalog_id
        row['region_id'] = data.region_id
        row['catalog_name'] = data.catalog_name
        row['lifetime_start'] = data.lifetime_start
        row['lifetime_end'] = data.lifetime_end
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    # Show Result
    utils.print_list(result_list, _print_catalog_columns)


@utils.arg('--catalog-id', metavar='<CATALOG_ID>',
           help='Filter catalog to those that have this catalog id.')
def do_catalog_delete(c, args):
    """Delete Catalog.
    :param c: call manager.
    :param args: argument options.
    """
    # Check arguments
    if args is None:
        msg = "too few arguments: catalog_id is required."
        utils.exit(msg)
    if not hasattr(args, 'catalog_id') or not args.catalog_id:
        msg = "too few arguments: catalog_id is required."
        utils.exit(msg)

    c.catalogs.delete(args.catalog_id)


@utils.arg('--catalog-id', metavar='<CATALOG_ID>',
           help='Create catalog id of catalog contents.')
@utils.arg('--goods-id', metavar='<GOODS_ID>',
           help='Create goods id of catalog contents.')
@utils.arg('--goods-num', metavar='<GOODS_NUM>',
           help='Create goods number of catalog contents.')
@utils.arg('--expansion-key1', metavar='<EXPANSION_KEY1>',
           help='Reserved area 1.')
@utils.arg('--expansion-key2', metavar='<EXPANSION_KEY2>',
           help='Reserved area 2.')
@utils.arg('--expansion-key3', metavar='<EXPANSION_KEY3>',
           help='Reserved area 3.')
@utils.arg('--expansion-key4', metavar='<EXPANSION_KEY4>',
           help='Reserved area 4.')
@utils.arg('--expansion-key5', metavar='<EXPANSION_KEY5>',
           help='Reserved area 5.')
@utils.arg('--expansion-text', metavar='<EXPANSION_TEXT>',
           help='Reserved area for big data.')
def do_catalog_contents_create(c, args):
    """Create a new catalog contents you can access.
    In commandline, output catalog contents data.
    Don't output workflow data.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}
    expansions = {}
    expansions_text = {}

    # Check arguments
    if args is None:
        msg = "too few arguments"
        utils.exit(msg)
    if not hasattr(args, 'catalog_id'):
        msg = "too few arguments: catalog id is required"
        utils.exit(msg)

    if hasattr(args, 'goods_id'):
        fields["goods_id"] = args.goods_id
    if hasattr(args, 'goods_num'):
        fields["goods_num"] = int(args.goods_num)
    if hasattr(args, 'expansion_key1') and args.expansion_key1 is not None:
        expansions['expansion_key1'] = args.expansion_key1
    if hasattr(args, 'expansion_key2') and args.expansion_key2 is not None:
        expansions['expansion_key2'] = args.expansion_key2
    if hasattr(args, 'expansion_key3') and args.expansion_key3 is not None:
        expansions['expansion_key3'] = args.expansion_key3
    if hasattr(args, 'expansion_key4') and args.expansion_key4 is not None:
        expansions['expansion_key4'] = args.expansion_key4
    if hasattr(args, 'expansion_key5') and args.expansion_key5 is not None:
        expansions['expansion_key5'] = args.expansion_key5
    if hasattr(args, 'expansion_text') and args.expansion_text is not None:
        expansions_text['expansion_text'] = args.expansion_text

    if expansions:
        fields['expansions'] = expansions
    if expansions_text:
        fields['expansions_text'] = expansions_text

    result_list = []

    # Call client.
    data = c.catalog_contents.create(args.catalog_id, fields)

    if data:
        row = {}
        row['catalog_id'] = data.catalog_id
        row['seq_no'] = data.seq_no
        row['goods_id'] = data.goods_id
        row['goods_num'] = data.goods_num
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    # Show result.
    utils.print_list(result_list, _print_catalog_contents_columns)

    return result_list


@utils.arg('--catalog-id',
           metavar='<CATALOG_ID>',
           help='Filter catalog contents to those that have this catalog id.')
@utils.arg('--limit',
           metavar='<LIMIT>',
           help='Maximum number of catalog contents at once.')
@utils.arg('--marker',
           metavar='<MARKER>',
           help='Get start position of seq no. This value less get target.')
@utils.arg('--sort-key',
           choices=afloclient.v1.catalog_contents.SORT_KEY_VALUES,
           help='Sort catalog contents list by specified field.')
@utils.arg('--sort-dir',
           choices=afloclient.v1.catalog_contents.SORT_DIR_VALUES,
           help='Sort catalog contents list in specified direction.')
@utils.arg('--force-show-deleted',
           metavar='<FORCE_SHOW_DELETED>',
           help='Get deleted catalog contents. Admin user can use this '
                'option.')
def do_catalog_contents_list(c, args):
    """List catalog contents you can access.
    :param c: call manager.
    :param args: Command options.
    """

    fields = {}

    if not args or not hasattr(args, 'catalog_id') or not args.catalog_id:
        msg = "too few arguments: catalog_id is required"
        utils.exit(msg)

    if args:
        fields = dict(filter(lambda x: x[1] and
                             x[0] in {'limit',
                                      'marker',
                                      'sort_key',
                                      'sort_dir',
                                      'force_show_deleted'},
                             vars(args).items()))

    # Call Client
    catalog_contents_refs = c.catalog_contents.list(args.catalog_id,
                                                    fields)
    catalog_contents = []
    for data in catalog_contents_refs:
        row = {}
        row['catalog_id'] = data.catalog_id
        row['seq_no'] = data.seq_no
        row['goods_id'] = data.goods_id
        row['goods_num'] = data.goods_num
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        catalog_contents.append(row)

    utils.print_list(catalog_contents, _print_catalog_contents_columns)


@utils.arg('--catalog-id', metavar='<CATALOG_ID>',
           help='Filter catalog contents to those that have this catalog id.')
@utils.arg('--seq-no', metavar='<SEQ_NO>',
           help='Filter catalog contents to those that have this seq no.')
def do_catalog_contents_get(c, args):
    """Get a catalog contents you can access.
    In commandline, output catalog contents data.
    :param c: call manager.
    :param args: argument options.
    """
    # Check arguments
    if args is None:
        msg = "too few arguments."
        utils.exit(msg)
    if not hasattr(args, 'catalog_id') or not args.catalog_id:
        msg = "too few arguments: catalog_id is required."
        utils.exit(msg)
    if not hasattr(args, 'seq_no') or not args.seq_no:
        msg = "too few arguments: seq_no is required."
        utils.exit(msg)

    result_list = []

    # Call client.
    try:
        data = c.catalog_contents.get(args.catalog_id, args.seq_no)

    except exc.NotFound:
        raise exc.CommandError()

    if data:
        row = {}
        row['catalog_id'] = data.catalog_id
        row['seq_no'] = data.seq_no
        row['goods_id'] = data.goods_id
        row['goods_num'] = data.goods_num
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    # Show result.
    utils.print_list(result_list, _print_catalog_contents_columns)


@utils.arg('--catalog-id', metavar='<CATALOG_ID>',
           help='Filter catalog contents to those that have' +
           ' this catalog id.')
@utils.arg('--seq-no', metavar='<SEQ_NO>',
           help='Filter catalog contents to those that have' +
           ' this sequence number.')
@utils.arg('--goods-id',
           metavar='<GOODS_ID>',
           help='Update goods id of catalog contents.')
@utils.arg('--goods-num',
           metavar='<GOODS_NUM>',
           help='Update goods number of catalog contents.')
@utils.arg('--expansion-key1',
           metavar='<EXPANSION_KEY1>',
           help='Reserved area 1.')
@utils.arg('--expansion-key2',
           metavar='<EXPANSION_KEY2>',
           help='Reserved area 2.')
@utils.arg('--expansion-key3',
           metavar='<EXPANSION_KEY3>',
           help='Reserved area 3.')
@utils.arg('--expansion-key4',
           metavar='<EXPANSION_KEY4>',
           help='Reserved area 4.')
@utils.arg('--expansion-key5',
           metavar='<EXPANSION_KEY5>',
           help='Reserved area 5.')
@utils.arg('--expansion-text',
           metavar='<EXPANSION_TEXT>',
           help='Reserved area for big data.')
def do_catalog_contents_update(c, args):
    """Update a catalog contents you can access.
    :param c: call manager.
    :param args: argument options.
    """
    if args is None:
        msg = "No Inputed catalog contets args."
        utils.exit(msg)
    if not hasattr(args, 'catalog_id') or not args.catalog_id:
        msg = "too few arguments: catalog id is required."
        utils.exit(msg)
    if not hasattr(args, 'seq_no') or not args.seq_no:
        msg = "too few arguments: sequence number is required."
        utils.exit(msg)

    catalog_contents = {}
    expansions = {}
    expansions_text = {}

    if hasattr(args, 'goods_id') and args.goods_id is not None:
        catalog_contents['goods_id'] = args.goods_id
    if hasattr(args, 'goods_num') and args.goods_num is not None:
        catalog_contents['goods_num'] = int(args.goods_num)
    if hasattr(args, 'expansion_key1') and args.expansion_key1 is not None:
        expansions['expansion_key1'] = args.expansion_key1
    if hasattr(args, 'expansion_key2') and args.expansion_key2 is not None:
        expansions['expansion_key2'] = args.expansion_key2
    if hasattr(args, 'expansion_key3') and args.expansion_key3 is not None:
        expansions['expansion_key3'] = args.expansion_key3
    if hasattr(args, 'expansion_key4') and args.expansion_key4 is not None:
        expansions['expansion_key4'] = args.expansion_key4
    if hasattr(args, 'expansion_key5') and args.expansion_key5 is not None:
        expansions['expansion_key5'] = args.expansion_key5
    if hasattr(args, 'expansion_text') and args.expansion_text is not None:
        expansions_text['expansion_text'] = args.expansion_text

    if expansions:
        catalog_contents['expansions'] = expansions
    if expansions_text:
        catalog_contents['expansions_text'] = expansions_text

    result_list = []

    data = c.catalog_contents.update(args.catalog_id,
                                     args.seq_no,
                                     catalog_contents)

    if data:
        row = {}
        row['catalog_id'] = data.catalog_id
        row['seq_no'] = data.seq_no
        row['goods_id'] = data.goods_id
        row['goods_num'] = data.goods_num
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    utils.print_list(result_list, _print_catalog_contents_columns)


@utils.arg('--catalog-id', metavar='<CATALOG_ID>',
           help='Filter catalog contents to those that have this catalog id.')
@utils.arg('--seq-no', metavar='<SEQ_NO>',
           help='Filter catalog contents to those that have this seq no.')
def do_catalog_contents_delete(c, args):
    """Delete Catalog contents.
    :param c: call manager.
    :param args: argument options.
    """
    # Check arguments
    if args is None:
        msg = "too few arguments."
        utils.exit(msg)
    if not hasattr(args, 'catalog_id') or not args.catalog_id:
        msg = "too few arguments: catalog_id is required."
        utils.exit(msg)
    if not hasattr(args, 'seq_no') or not args.seq_no:
        msg = "too few arguments: seq_no is required."
        utils.exit(msg)

    c.catalog_contents.delete(args.catalog_id, args.seq_no)


@utils.arg('--catalog-id', metavar='<CATALOG_ID>',
           help='Filter catalog scope to those that have this catalog id.')
@utils.arg('--scope', metavar='<SCOPE>',
           help='Filter catalog scope to those that have this scope.')
@utils.arg('--lifetime', metavar='<LIFETIME>',
           help='Filter catalog scope to those that have this lifetime.')
@utils.arg('--sort-key',
           choices=afloclient.v1.catalog_scope.SORT_KEY_VALUES,
           help='Sort catalog scope list by specified field.')
@utils.arg('--sort-dir',
           choices=afloclient.v1.catalog_scope.SORT_DIR_VALUES,
           help='Sort catalog scope list in specified direction.')
@utils.arg('--limit', metavar='<LIMIT>', type=int,
           help='Maximum number of catalog scope at once.')
@utils.arg('--marker', metavar='<MARKER>',
           help='Get start position of id. This value less get target.')
@utils.arg('--force-show-deleted', metavar='<FORCE_SHOW_DELETED>',
           help='Get deleted catalog scope. Admin user can use this option.')
def do_catalog_scope_list(c, args):
    """List catalog scope you can access.
    :param c: call manager.
    :pamam args: argument options.
    """

    fields = {}

    # Filter out None values from args.
    if args:
        fields = dict(filter(lambda x: x[1] is not None
                             and x[0] in {'catalog_id', 'scope', 'lifetime',
                                          'sort_key', 'sort_dir', 'limit',
                                          'marker', 'force_show_deleted'},
                             vars(args).items()))

    # Call Client
    catalog_scope = c.catalog_scope.list(fields)

    result_list = []

    for data in catalog_scope:
        row = {}
        row['id'] = data.id
        row['catalog_id'] = data.catalog_id
        row['scope'] = data.scope
        row['lifetime_start'] = data.lifetime_start
        row['lifetime_end'] = data.lifetime_end
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    # Show Result
    utils.print_list(result_list, _print_catalog_scope_columns)


@utils.arg('--catalog-id', metavar='<CATALOG_ID>',
           help='Create catalog id of catalog scope.')
@utils.arg('--scope', metavar='<SCOPE>',
           help='Create scope of catalog scope.')
@utils.arg('--lifetime-start', metavar='<LIFETIME_START>',
           help='Create lifetime start of catalog scope.')
@utils.arg('--lifetime-end', metavar='<LIFETIME_END>',
           help='Create lifetime end of catalog scope.')
@utils.arg('--expansion-key1',
           metavar='<EXPANSION_KEY1>',
           help='Reserved area 1.')
@utils.arg('--expansion-key2',
           metavar='<EXPANSION_KEY2>',
           help='Reserved area 2.')
@utils.arg('--expansion-key3',
           metavar='<EXPANSION_KEY3>',
           help='Reserved area 3.')
@utils.arg('--expansion-key4',
           metavar='<EXPANSION_KEY4>',
           help='Reserved area 4.')
@utils.arg('--expansion-key5',
           metavar='<EXPANSION_KEY5>',
           help='Reserved area 5.')
@utils.arg('--expansion-text',
           metavar='<EXPANSION_TEXT>',
           help='Reserved area for big data.')
def do_catalog_scope_create(c, args):
    """Create a new catalog scope you can access.
    In commandline, output catalog scope data.
    :param c: call manager.
    :param args: argument options.
    """
    # Check arguments
    if args is None:
        msg = "too few arguments"
        utils.exit(msg)
    if not hasattr(args, 'catalog_id') or not args.catalog_id:
        msg = "too few arguments: catalog_id is required."
        utils.exit(msg)
    if not hasattr(args, 'scope') or not args.scope:
        msg = "too few arguments: scope is required."
        utils.exit(msg)

    fields = {}
    expansions = {}
    expansions_text = {}

    if hasattr(args, 'lifetime_start') and args.lifetime_start is not None:
        fields['lifetime_start'] = args.lifetime_start
    if hasattr(args, 'lifetime_end') and args.lifetime_end is not None:
        fields['lifetime_end'] = args.lifetime_end
    if hasattr(args, 'expansion_key1') and args.expansion_key1 is not None:
        expansions['expansion_key1'] = args.expansion_key1
    if hasattr(args, 'expansion_key2') and args.expansion_key2 is not None:
        expansions['expansion_key2'] = args.expansion_key2
    if hasattr(args, 'expansion_key3') and args.expansion_key3 is not None:
        expansions['expansion_key3'] = args.expansion_key3
    if hasattr(args, 'expansion_key4') and args.expansion_key4 is not None:
        expansions['expansion_key4'] = args.expansion_key4
    if hasattr(args, 'expansion_key5') and args.expansion_key5 is not None:
        expansions['expansion_key5'] = args.expansion_key5
    if hasattr(args, 'expansion_text') and args.expansion_text is not None:
        expansions_text['expansion_text'] = args.expansion_text

    if expansions:
        fields['expansions'] = expansions
    if expansions_text:
        fields['expansions_text'] = expansions_text

    result_list = []

    # Call client.
    data = c.catalog_scope.create(args.catalog_id, args.scope, fields)

    if data:
        row = {}
        row['id'] = data.id
        row['catalog_id'] = data.catalog_id
        row['scope'] = data.scope
        row['lifetime_start'] = data.lifetime_start
        row['lifetime_end'] = data.lifetime_end
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    # Show result.
    utils.print_list(result_list, _print_catalog_scope_columns)

    return result_list


@utils.arg('--id', metavar='<ID>',
           help='Filter catalog scope to those '
                'that have this catalog scope id.')
def do_catalog_scope_get(c, args):
    """Get a catalog scope you can access.
    In commandline, output catalog scope data.
    :param c: call manager.
    :param args: argument options.
    """
    # Check arguments
    if args is None or not hasattr(args, 'id') or not args.id:
        msg = "too few arguments: id is required."
        utils.exit(msg)

    result_list = []

    # Call client.
    try:
        data = c.catalog_scope.get(args.id)
    except exc.NotFound:
        raise exc.CommandError()

    if data:
        row = {}
        row['id'] = data.id
        row['catalog_id'] = data.catalog_id
        row['scope'] = data.scope
        row['lifetime_start'] = data.lifetime_start
        row['lifetime_end'] = data.lifetime_end
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    # Show result.
    utils.print_list(result_list, _print_catalog_scope_columns)


@utils.arg('--id', metavar='<ID>',
           help='Filter catalog scope to those that have this id.')
@utils.arg('--lifetime-start',
           metavar='<LIFETIME_START>',
           help='Update lifetime start of catalog scope.')
@utils.arg('--lifetime-end',
           metavar='<LIFETIME_END>',
           help='Update lifetime end of catalog scope.')
@utils.arg('--expansion-key1',
           metavar='<EXPANSION_KEY1>',
           help='Reserved area 1.')
@utils.arg('--expansion-key2',
           metavar='<EXPANSION_KEY2>',
           help='Reserved area 2.')
@utils.arg('--expansion-key3',
           metavar='<EXPANSION_KEY3>',
           help='Reserved area 3.')
@utils.arg('--expansion-key4',
           metavar='<EXPANSION_KEY4>',
           help='Reserved area 4.')
@utils.arg('--expansion-key5',
           metavar='<EXPANSION_KEY5>',
           help='Reserved area 5.')
@utils.arg('--expansion-text',
           metavar='<EXPANSION_TEXT>',
           help='Reserved area for big data.')
def do_catalog_scope_update(c, args):
    """Update a catalog scope you can access.
    In commandline, output catalog scope data.
    :param c: call maneger.
    :param args: argument options.
    """
    # Check arguments
    if args is None or not hasattr(args, 'id') or not args.id:
        msg = "too few arguments: id is required."
        utils.exit(msg)

    fields = {}
    expansions = {}
    expansions_text = {}

    if hasattr(args, 'lifetime_start') and args.lifetime_start is not None:
        fields['lifetime_start'] = args.lifetime_start
    if hasattr(args, 'lifetime_end') and args.lifetime_end is not None:
        fields['lifetime_end'] = args.lifetime_end
    if hasattr(args, 'expansion_key1') and args.expansion_key1 is not None:
        expansions['expansion_key1'] = args.expansion_key1
    if hasattr(args, 'expansion_key2') and args.expansion_key2 is not None:
        expansions['expansion_key2'] = args.expansion_key2
    if hasattr(args, 'expansion_key3') and args.expansion_key3 is not None:
        expansions['expansion_key3'] = args.expansion_key3
    if hasattr(args, 'expansion_key4') and args.expansion_key4 is not None:
        expansions['expansion_key4'] = args.expansion_key4
    if hasattr(args, 'expansion_key5') and args.expansion_key5 is not None:
        expansions['expansion_key5'] = args.expansion_key5
    if hasattr(args, 'expansion_text') and args.expansion_text is not None:
        expansions_text['expansion_text'] = args.expansion_text

    if expansions:
        fields['expansions'] = expansions
    if expansions_text:
        fields['expansions_text'] = expansions_text

    result_list = []

    # Call client.
    data = c.catalog_scope.update(args.id, fields)

    if data:
        row = {}
        row['id'] = data.id
        row['catalog_id'] = data.catalog_id
        row['scope'] = data.scope
        row['lifetime_start'] = data.lifetime_start
        row['lifetime_end'] = data.lifetime_end
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    # Show result.
    utils.print_list(result_list, _print_catalog_scope_columns)

    return result_list


@utils.arg('--id', metavar='<ID>',
           help='Filter catalog scope to those that have this id.')
def do_catalog_scope_delete(c, args):
    """Delete catalog scope.
    :param c: call manager.
    :param args: arguments.
    """
    # Check arguments
    if args is None or not hasattr(args, 'id') or not args.id:
        msg = "too few arguments: id is required."
        utils.exit(msg)

    c.catalog_scope.delete(args.id)


@utils.arg('--catalog-id', metavar='<CATALOG_ID>',
           help='Filter valid catalog to those that have this catalog id.')
@utils.arg('--scope', metavar='<SCOPE>',
           help='Filter valid catalog to those that have this scope.')
@utils.arg('--lifetime', metavar='<LIFETIME>',
           help='Filter valid catalog to those that have this lifetime.')
@utils.arg('--catalog-name', metavar='<CATALOG_NAME>',
           help='Filter valid catalog to those that have this catalog name.')
@utils.arg('--sort-key', default='catalog_id',
           choices=afloclient.v1.catalogs.SORT_KEY_VALUES,
           help='Sort valid catalog list by specified field.')
@utils.arg('--sort-dir', default='asc',
           choices=afloclient.v1.catalogs.SORT_DIR_VALUES,
           help='Sort valid catalog list in specified direction.')
@utils.arg('--limit', metavar='<LIMIT>', type=int,
           help='Maximum number of valid catalog at once.')
@utils.arg('--catalog-marker', metavar='<CATALOG_MARKER>',
           help='Get start position of catalog id. '
                'This value less get target.')
@utils.arg('--catalog-scope-marker', metavar='<CATALOG_SCOPE_MARKER>',
           help='Get start position of catalog scope id. '
                'This value less get target.')
@utils.arg('--price-marker', metavar='<PRICE_MARKER>',
           help='Get start position of price seq no. '
                'This value less get target.')
@utils.arg('--refine-flg', metavar='<REFINE-FLG>',
           help='Whether the flag to merge the default data')
def do_valid_catalog_list(c, args):
    """List valid catalog you can access.
    :param c: call manager.
    :param args: argument options.
    """

    # Check arguments
    if args is None:
        msg = "too few arguments."
        utils.exit(msg)
    if not hasattr(args, 'lifetime') or not args.lifetime:
        msg = "too few arguments: lifetime is required."
        utils.exit(msg)

    fields = {}

    # Filter out None values from args.
    if args:
        fields = dict(filter(lambda x: x[1] is not None
                             and x[0] in {'catalog_id', 'scope', 'lifetime',
                                          'catalog_name',
                                          'sort_key', 'sort_dir',
                                          'limit', 'catalog_marker',
                                          'catalog_scope_marker',
                                          'price_marker', 'refine_flg'},
                             vars(args).items()))

    # Call Client
    valid_catalog = c.valid_catalog.list(fields)

    result_list = []

    for data in valid_catalog:
        row = {}
        row['catalog_id'] = data.catalog_id
        row['scope'] = data.scope
        row['catalog_name'] = data.catalog_name
        row['catalog_lifetime_start'] = data.catalog_lifetime_start
        row['catalog_lifetime_end'] = data.catalog_lifetime_end
        row['catalog_scope_id'] = data.catalog_scope_id
        row['catalog_scope_lifetime_start'] = data.catalog_scope_lifetime_start
        row['catalog_scope_lifetime_end'] = data.catalog_scope_lifetime_end
        row['price_seq_no'] = data.price_seq_no
        row['price'] = data.price
        row['price_lifetime_start'] = data.price_lifetime_start
        row['price_lifetime_end'] = data.price_lifetime_end

        result_list.append(row)

    # Show Result
    utils.print_list(result_list, _print_valid_catalog_columns)


@utils.arg('--catalog-id', metavar='<CATALOG_ID>',
           help='Create catalog id of catalog price.')
@utils.arg('--scope', metavar='<SCOPE>',
           help='Create scope of catalog price.')
@utils.arg('--price', metavar='<PRICE>',
           help='Create price of catalog price.')
@utils.arg('--lifetime-start', metavar='<LIFETIME_START>',
           help='Create lifetime start of catalog price.')
@utils.arg('--lifetime-end', metavar='<LIFETIME_END>',
           help='Create lifetime end of catalog price.')
@utils.arg('--expansion-key1', metavar='<EXPANSION_KEY1>',
           help='Reserved area 1.')
@utils.arg('--expansion-key2', metavar='<EXPANSION_KEY2>',
           help='Reserved area 2.')
@utils.arg('--expansion-key3', metavar='<EXPANSION_KEY3>',
           help='Reserved area 3.')
@utils.arg('--expansion-key4', metavar='<EXPANSION_KEY4>',
           help='Reserved area 4.')
@utils.arg('--expansion-key5', metavar='<EXPANSION_KEY5>',
           help='Reserved area 5.')
@utils.arg('--expansion-text', metavar='<EXPANSION_TEXT>',
           help='Reserved area for big data.')
def do_price_create(c, args):
    """Create a new price you can access.
    In commandline, output price data.
    Don't output workflow data.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}
    expansions = {}
    expansions_text = {}

    # Check arguments
    if args is None:
        msg = "too few arguments"
        utils.exit(msg)
    if not hasattr(args, 'catalog_id') or not args.catalog_id:
        msg = "too few arguments: catalog id is required"
        utils.exit(msg)
    if not hasattr(args, 'scope') or not args.scope:
        msg = "too few arguments: scope is required"
        utils.exit(msg)
    if not hasattr(args, 'price') or not args.scope:
        msg = "too few arguments: price is required"
        utils.exit(msg)

    if hasattr(args, 'price'):
        fields["price"] = args.price
    if hasattr(args, 'lifetime_start'):
        fields["lifetime_start"] = args.lifetime_start
    if hasattr(args, 'lifetime_end'):
        fields["lifetime_end"] = args.lifetime_end
    if hasattr(args, 'expansion_key1') and args.expansion_key1 is not None:
        expansions['expansion_key1'] = args.expansion_key1
    if hasattr(args, 'expansion_key2') and args.expansion_key2 is not None:
        expansions['expansion_key2'] = args.expansion_key2
    if hasattr(args, 'expansion_key3') and args.expansion_key3 is not None:
        expansions['expansion_key3'] = args.expansion_key3
    if hasattr(args, 'expansion_key4') and args.expansion_key4 is not None:
        expansions['expansion_key4'] = args.expansion_key4
    if hasattr(args, 'expansion_key5') and args.expansion_key5 is not None:
        expansions['expansion_key5'] = args.expansion_key5
    if hasattr(args, 'expansion_text') and args.expansion_text is not None:
        expansions_text['expansion_text'] = args.expansion_text

    if expansions:
        fields['expansions'] = expansions
    if expansions_text:
        fields['expansions_text'] = expansions_text

    result_list = []

    # Call client.
    data = c.price.create(args.catalog_id, args.scope, fields)

    if data:
        row = {}
        row['catalog_id'] = data.catalog_id
        row['scope'] = data.scope
        row['seq_no'] = data.seq_no
        row['price'] = data.price
        row['lifetime_start'] = data.lifetime_start
        row['lifetime_end'] = data.lifetime_end
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    # Show result.
    utils.print_list(result_list, _print_price_columns)

    return result_list


@utils.arg('--catalog-id', metavar='<CATALOG_ID>',
           help='Filter catalog price to those that have this catalog id.')
@utils.arg('--scope', metavar='<SCOPE>',
           help='Filter catalog price to those that have this scope.')
@utils.arg('--lifetime', metavar='<LIFETIME>',
           help='Filter catalog price to those that have this lifetime.')
@utils.arg('--sort-key',
           choices=afloclient.v1.price.SORT_KEY_VALUES,
           help='Sort catalog price list by specified field.')
@utils.arg('--sort-dir',
           choices=afloclient.v1.price.SORT_DIR_VALUES,
           help='Sort catalog price list in specified direction.')
@utils.arg('--limit', metavar='<LIMIT>', type=int,
           help='Maximum number of catalog price at once.')
@utils.arg('--marker', metavar='<MARKER>',
           help='Get start position of seq no. This value less get target.')
@utils.arg('--force-show-deleted', metavar='<FORCE_SHOW_DELETED>',
           help='Get deleted catalog price. Admin user can use this option.')
def do_price_list(c, args):
    """List price you can access.
    :param c: call manager.
    :param args: argument options.
    """

    # Check arguments
    if args is None:
        msg = "too few arguments."
        utils.exit(msg)
    if not hasattr(args, 'catalog_id') or not args.catalog_id:
        msg = "too few arguments: catalog_id is required."
        utils.exit(msg)

    fields = {}

    # Filter out None values from args.
    if args:
        fields = dict(filter(lambda x: x[1] is not None
                             and x[0] in {'scope', 'lifetime',
                                          'sort_key', 'sort_dir',
                                          'limit', 'marker',
                                          'force_show_deleted'},
                             vars(args).items()))

    # Call Client
    prices = c.price.list(args.catalog_id, fields)

    result_list = []

    for data in prices:
        row = {}
        row['catalog_id'] = data.catalog_id
        row['scope'] = data.scope
        row['seq_no'] = data.seq_no
        row['price'] = data.price
        row['lifetime_start'] = data.lifetime_start
        row['lifetime_end'] = data.lifetime_end
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    # Show Result
    utils.print_list(result_list, _print_price_columns)


@utils.arg('--catalog-id', metavar='<CATALOG_ID>',
           help='Filter catalog price to those that have this catalog id.')
@utils.arg('--scope', metavar='<SCOPE>',
           help='Filter catalog price to those that have this scope.')
@utils.arg('--seq-no', metavar='<SEQ_NO>',
           help='Filter catalog price to those that have this seq no.')
def do_price_get(c, args):
    """Get a price you can access.
    In commandline, output price data.
    :param c: call manager.
    :param args: argument options.
    """
    # Check arguments
    if args is None:
        msg = "too few arguments."
        utils.exit(msg)
    if not hasattr(args, 'catalog_id') or not args.catalog_id:
        msg = "too few arguments: catalog_id is required."
        utils.exit(msg)
    if not hasattr(args, 'scope') or not args.scope:
        msg = "too few arguments: scope is required."
        utils.exit(msg)
    if not hasattr(args, 'seq_no') or not args.seq_no:
        msg = "too few arguments: seq_no is required."
        utils.exit(msg)

    result_list = []

    # Call Client
    try:
        data = c.price.get(args.catalog_id, args.scope, args.seq_no)

    except exc.NotFound:
        raise exc.CommandError()

    if data:
        row = {}
        row['catalog_id'] = data.catalog_id
        row['scope'] = data.scope
        row['seq_no'] = data.seq_no
        row['price'] = data.price
        row['lifetime_start'] = data.lifetime_start
        row['lifetime_end'] = data.lifetime_end
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    # Show Result
    utils.print_list(result_list, _print_price_columns)


@utils.arg('--catalog-id', metavar='<CATALOG_ID>',
           help='Filter catalog price to those that have this catalog id.')
@utils.arg('--scope', metavar='<SCOPE>',
           help='Filter catalog price to those that have this scope.')
@utils.arg('--seq-no', metavar='<SEQ_NO>',
           help='Filter catalog price to those that have this seq no.')
@utils.arg('--price', metavar='<PRICE>',
           help='Update price of catalog price.')
@utils.arg('--lifetime-start', metavar='<LIFETIME_START>',
           help='Update lifetime start of catalog price.')
@utils.arg('--lifetime-end', metavar='<LIFETIME_END>',
           help='Update lifetime end of catalog price.')
@utils.arg('--expansion-key1', metavar='<EXPANSION_KEY1>',
           help='Reserved area 1.')
@utils.arg('--expansion-key2', metavar='<EXPANSION_KEY2>',
           help='Reserved area 2.')
@utils.arg('--expansion-key3', metavar='<EXPANSION_KEY3>',
           help='Reserved area 3.')
@utils.arg('--expansion-key4', metavar='<EXPANSION_KEY4>',
           help='Reserved area 4.')
@utils.arg('--expansion-key5', metavar='<EXPANSION_KEY5>',
           help='Reserved area 5.')
@utils.arg('--expansion-text', metavar='<EXPANSION_TEXT>',
           help='Reserved area for big data.')
def do_price_update(c, args):
    """Update a price you can access.
    :param c: call manager.
    :param args: argument options.
    """
    fields = {}
    expansions = {}

    # Check arguments
    if args is None:
        msg = "too few arguments"
        utils.exit(msg)
    if not hasattr(args, 'catalog_id') or not args.catalog_id:
        msg = "too few arguments: catalog id is required"
        utils.exit(msg)
    if not hasattr(args, 'scope') or not args.scope:
        msg = "too few arguments: scope is required"
        utils.exit(msg)
    if not hasattr(args, 'seq_no') or not args.seq_no:
        msg = "too few arguments: seq_no is required"
        utils.exit(msg)

    if hasattr(args, 'price') and args.price is not None:
        fields['price'] = args.price
    if hasattr(args, 'lifetime_start') and args.lifetime_start is not None:
        fields['lifetime_start'] = args.lifetime_start
    if hasattr(args, 'lifetime_end') and args.lifetime_end is not None:
        fields['lifetime_end'] = args.lifetime_end
    if hasattr(args, 'expansion_key1') and args.expansion_key1 is not None:
        expansions['expansion_key1'] = args.expansion_key1
    if hasattr(args, 'expansion_key2') and args.expansion_key2 is not None:
        expansions['expansion_key2'] = args.expansion_key2
    if hasattr(args, 'expansion_key3') and args.expansion_key3 is not None:
        expansions['expansion_key3'] = args.expansion_key3
    if hasattr(args, 'expansion_key4') and args.expansion_key4 is not None:
        expansions['expansion_key4'] = args.expansion_key4
    if hasattr(args, 'expansion_key5') and args.expansion_key5 is not None:
        expansions['expansion_key5'] = args.expansion_key5

    if expansions:
        fields['expansions'] = expansions
    if hasattr(args, 'expansion_text') and args.expansion_text is not None:
        fields['expansions_text'] = {}
        fields['expansions_text']['expansion_text'] = args.expansion_text

    result_list = []

    # Call client.
    data = c.price.update(args.catalog_id,
                          args.scope,
                          args.seq_no,
                          fields)

    if data:
        row = {}
        row['catalog_id'] = data.catalog_id
        row['scope'] = data.scope
        row['seq_no'] = data.seq_no
        row['price'] = data.price
        row['lifetime_start'] = data.lifetime_start
        row['lifetime_end'] = data.lifetime_end
        row['created_at'] = data.created_at
        row['updated_at'] = data.updated_at
        row['deleted_at'] = data.deleted_at
        row['deleted'] = data.deleted

        expansions = data.expansions
        row['expansion_key1'] = expansions['expansion_key1'] \
            if expansions is not None else None
        row['expansion_key2'] = expansions['expansion_key2'] \
            if expansions is not None else None
        row['expansion_key3'] = expansions['expansion_key3'] \
            if expansions is not None else None
        row['expansion_key4'] = expansions['expansion_key4'] \
            if expansions is not None else None
        row['expansion_key5'] = expansions['expansion_key5'] \
            if expansions is not None else None

        expansions_text = data.expansions_text
        row['expansion_text'] = expansions_text['expansion_text'] \
            if expansions_text is not None else None

        result_list.append(row)

    utils.print_list(result_list, _print_price_columns)


@utils.arg('--catalog-id', metavar='<CATALOG_ID>',
           help='Filter catalog price to those that have this catalog id.')
@utils.arg('--scope', metavar='<SCOPE>',
           help='Filter catalog price to those that have this scope.')
@utils.arg('--seq-no', metavar='<SEQ_NO>',
           help='Filter catalog price to those that have this seq no.')
def do_price_delete(c, args):
    """Delete Price.
    :param c: call manager.
    :param args: argument options.
    """
    # Check arguments
    if args is None:
        msg = "too few arguments."
        utils.exit(msg)
    if not hasattr(args, 'catalog_id') or not args.catalog_id:
        msg = "too few arguments: catalog_id is required."
        utils.exit(msg)
    if not hasattr(args, 'scope') or not args.scope:
        msg = "too few arguments: scope is required."
        utils.exit(msg)
    if not hasattr(args, 'seq_no') or not args.seq_no:
        msg = "too few arguments: seq_no is required."
        utils.exit(msg)

    c.price.delete(args.catalog_id, args.scope, args.seq_no)
