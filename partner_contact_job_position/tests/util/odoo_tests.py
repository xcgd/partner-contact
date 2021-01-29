##############################################################################
#
#    Partner work detail for Odoo
#    Copyright (C) 2021 XCG Consulting <http://odoo.consulting>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

"""Utilities useful to Odoo tests.
"""

import odoo.models
import odoo.tests


class TestBase(odoo.tests.SingleTransactionCase):
    """Provide some test helpers.
    """

    def createAndTest(self, model, value_list, custom_testers=None):
        """Create records of the specified Odoo model using the specified
        values, and ensure afterwards that records have been succesfully
        created and that their values are the same as expected.

        :param custom_testers: Mapping of testing functions to use when
        comparing the recorded value to the one asked for by the test.
        :type custom_testers: {
            'field': f(test_instance, asked_value, recorded_value),
        }.

        :return: The created records.
        :rtype: List of odoo.models.BaseModel instances.
        """

        if custom_testers is None:
            custom_testers = {}

        records = []

        for values in value_list:

            # Maintain a local copy as Odoo calls might modify it...
            local_values = values.copy()

            record = self.env[model].create(values)
            records.append(record)

            self.assertIsInstance(record, odoo.models.BaseModel)

            for field, value in local_values.items():

                tester = (
                    custom_testers.get(field) or TestBase.defaultValueTester
                )
                tester(self, value, getattr(record, field))

        return records

    @staticmethod
    def defaultValueTester(test_instance, asked_value, recorded_value):
        """Ensure what has been recorded is the same as what has been asked
        for.
        """

        # Handle relational fields (Odoo record-sets).
        if isinstance(recorded_value, odoo.models.BaseModel):
            if isinstance(recorded_value, (tuple, list)):
                test_instance.assertEqual(recorded_value.ids, asked_value)
            else:
                test_instance.assertEqual(recorded_value.id, asked_value)

        else:
            test_instance.assertEqual(recorded_value, asked_value)
