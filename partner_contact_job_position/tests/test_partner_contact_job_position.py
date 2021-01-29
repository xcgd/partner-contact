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

import odoo

from .util.odoo_tests import TestBase
from .util.singleton import Singleton
from .util.uuidgen import genUuid


class TestMemory(object, metaclass=Singleton):
    """Keep records in memory across tests."""


@odoo.tests.common.at_install(False)
@odoo.tests.common.post_install(True)
class Test(TestBase):
    def setUp(self):
        super(Test, self).setUp()
        self.memory = TestMemory()

    def test_0001_res_partner_job_position(self):
        """Create a ob position object.
        """
        ref = genUuid()
        code = genUuid()

        # Create a job position.
        self.memory.job_position, = self.createAndTest(
            "res.partner.job_position", [{"name": ref, "code": code}]
        )

        self.assertEqual(self.memory.job_position.name, ref)
        self.assertEqual(self.memory.job_position.code, code)

    def test_0002_res_partner(self):
        """Create a partner and fill the field added in this module.
        """

        self.memory.job_position, = self.createAndTest(
            "res.partner.job_position",
            [{"name": genUuid(), "code": genUuid()}],
        )

        # Create a natural person partner and fill the field available for
        # people added in this module.
        self.memory.partner, = self.createAndTest(
            "res.partner",
            [
                {
                    "name": genUuid(),
                    "is_company": False,
                    "job_position_id": self.memory.job_position.id,
                }
            ],
        )
