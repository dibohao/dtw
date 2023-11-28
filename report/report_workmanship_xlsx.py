from odoo import models

from odoo import _, fields, models
from odoo.exceptions import UserError

#下面是用pandas生成excel及json文件 import pandas as pd

    # rec=self.env['dtw.workmanship']
    # data=rec.search_read([],["id","name","target_tork","min_tork","max_tork","angle","barcode","company_id"])
    # df=pd.DataFrame(data)
    # # writer = pd.ExcelWriter("demo.xlsx")
    # df.to_excel(excel_writer="test.xlsx",sheet_name="sheet_1",index=False)
    # return df.to_json("test.json",orient="records")

class WorkmanshipXlsx(models.AbstractModel):
    _name = 'report.dtw.report_workmanship_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, workmanship):
        workmanship=self.env['dtw.workmanship'].search([('dispatch','=',True)])
        sheet = workbook.add_worksheet('sheet1')
        # bold = workbook.add_format({'bold': True})
        header = ['工艺名称','目标扭力','扭力单位','最小扭力','最大扭力','目标角度','最小角度','最大角度','公司名称','模式','公司代码','工艺代码','操作员','二维码',]
        for col in range(len(header)):
            sheet.write(0, col, header[col])
            # sheet.write(0, 0, obj.name, bold)
        for row in range(1, len(workmanship)+1):
            workmanship_id = workmanship[row-1]
            sheet.write(row, 0, workmanship_id.name)
            sheet.write(row, 1, workmanship_id.target_tork)
            sheet.write(row, 2, workmanship_id.tork_unit)
            sheet.write(row, 3, workmanship_id.min_tork)
            sheet.write(row, 4, workmanship_id.max_tork)
            sheet.write(row, 5, workmanship_id.angle)
            sheet.write(row, 6, workmanship_id.min_angle)
            sheet.write(row, 7, workmanship_id.max_angle)
            sheet.write(row, 8, workmanship_id.company_id.name)
            sheet.write(row, 9, workmanship_id.worktype_id.name)
            sheet.write(row, 10, workmanship_id.company_id.id)
            sheet.write(row, 11, workmanship_id.id)
            sheet.write(row, 12, workmanship_id.operator_id.name)
            sheet.write(row, 13, workmanship_id.barcode)