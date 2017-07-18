# Copyright 2012 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import sys

import six
# NOTE(jokke): simplified transition to py3, behaves like py2 xrange
from six.moves import range
import testtools

from afloclient.common import utils


class TestUtils(testtools.TestCase):

    def test_prettytable(self):
        class Struct(object):
            def __init__(self, **entries):
                self.__dict__.update(entries)

        # test that the prettytable output is wellformatted (left-aligned)
        columns = ['ID', 'Name']
        val = ['Name1', 'another', 'veeeery long']
        tickets = [Struct(**{'id': i ** 16, 'name': val[i]})
                   for i in range(len(val))]

        saved_stdout = sys.stdout
        try:
            sys.stdout = output_list = six.StringIO()
            utils.print_list(tickets, columns)

            sys.stdout = output_dict = six.StringIO()
            utils.print_dict({'K': 'k', 'Key': 'veeeeeeeeeeeeeeeeeeeeeeee'
                              'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
                              'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
                              'eeeeeeeeeeeery long value'},
                             max_column_width=60)

        finally:
            sys.stdout = saved_stdout

        self.assertEqual('''\
+-------+--------------+
| ID    | Name         |
+-------+--------------+
|       | Name1        |
| 1     | another      |
| 65536 | veeeery long |
+-------+--------------+
''',
                         output_list.getvalue())

        self.assertEqual('''\
+----------+--------------------------------------------------------------+
| Property | Value                                                        |
+----------+--------------------------------------------------------------+
| K        | k                                                            |
| Key      | veeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee |
|          | eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee |
|          | ery long value                                               |
+----------+--------------------------------------------------------------+
''',
                         output_dict.getvalue())

    def test_exception_to_str(self):
        class FakeException(Exception):
            def __str__(self):
                raise UnicodeError()

        ret = utils.exception_to_str(Exception('error message'))
        self.assertEqual('error message', ret)

        ret = utils.exception_to_str(Exception('\xa5 error message'))
        if six.PY2:
            self.assertEqual(' error message', ret)
        else:
            self.assertEqual('\xa5 error message', ret)

        ret = utils.exception_to_str(FakeException('\xa5 error message'))
        self.assertEqual("Caught '%(exception)s' exception." %
                         {'exception': 'FakeException'}, ret)

    def test_validate_json_format(self):
        """Test validation json format method.
        """
        # Not json string
        self.assertEqual(utils.validate_json_format(''), False)
        self.assertEqual(utils.validate_json_format('}'), False)
        self.assertEqual(utils.validate_json_format('"'), False)
        self.assertEqual(utils.validate_json_format('aaa'), False)

        # json string
        self.assertEqual(utils.validate_json_format('{}'), True)

    def test_urlencode(self):
        self.assertEqual('1=1', utils.urlencode({1: 1}))
        self.assertEqual('1=1', utils.urlencode({"1": "1"}))
        self.assertEqual('1=%2F1', utils.urlencode({"1": u"/1"}))
