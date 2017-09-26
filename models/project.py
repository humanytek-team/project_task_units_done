# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Manuel Márquez <manuel@humanytek.com>
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
###############################################################################

from openerp import api, fields, models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    units_done = fields.Float('Units done')


class ProjectTaskWork(models.Model):
    _inherit = 'project.task.work'

    units_done = fields.Float('Units done')

    @api.model
    def _create_analytic_entries(self, vals):        

        timeline_id = super(ProjectTaskWork, self)._create_analytic_entries(
            vals)

        if timeline_id:
            HrAnalyticTimesheet = self.env['hr.analytic.timesheet']
            timeline = HrAnalyticTimesheet.browse(timeline_id)
            timeline.write({'units_done': vals['units_done']})

        return timeline_id

    @api.multi
    def write(self, vals):
        for task in self:
            line_id = task.hr_analytic_timesheet_id
            if not line_id:
                continue

            if 'units_done' in vals:
                line_id.write({'units_done': vals['units_done']})
        return super(ProjectTaskWork, self).write(vals)
