# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from odoo.addons import decimal_precision as dp
from odoo.exceptions import AccessError, UserError, ValidationError

class Workposition(models.Model):
    _name="dtw.workposition"
    _description="工位"
    _sql_constraints = [
    ('name_uniq',
    'UNIQUE (name)',
    '工位名称不能重复!')
    ]
    name=fields.Char('工位名称')
    remark=fields.Char('工位说明')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)

class WorkmanshipMain(models.Model):
    _name="dtw.workmanship.main"
    _description="工单"
    _rec_name="name"

    # name=fields.Char('工单名称',required="1")
    name = fields.Char(
        string="工单号",
        required=True, copy=False, readonly=True,
        index='trigram',
        default=lambda self: _('New'))
    datetime_mainship=fields.Datetime('工单日期',default=fields.Datetime.now())
    remark=fields.Text('说明')
    workmanship_ids=fields.One2many('dtw.workmanship','main_id',string='工单明细')
    company_id = fields.Many2one('res.company',  default=lambda self: self.env.user.company_id)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user.user_id)
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['company_id']=self.env.user.company_id.id    
            self = self.with_company(vals['company_id'])
            if vals.get('name', _("New")) == _("New"):
                # seq_date = fields.Datetime.context_timestamp(
                #     self, fields.Datetime.to_datetime(vals['date_order'])
                # ) if 'date_order' in vals else None
                seq=self.env['ir.sequence'].search([('code','ilike','dtw.workmanship.main'),('company_id','=',vals['company_id'])])
                if not seq:
                    seq=self.env['ir.sequence'].create({
                        'name':'Workmanship_main',
                        'code':'dtw.workmanship.main.%s' % vals['company_id'],
                        'implementation':'standard',
                        'active':True,
                        'company_id':vals['company_id'],
                        'prefix':'W',
                        'padding':6,
                        'number_increment':1,
                        'suffix':'',
                        'use_date_range':False
                    })
                vals['name'] = seq.next_by_code('dtw.workmanship.main.%s' % vals['company_id']) or _("New")
        return super().create(vals_list)

class Workmanship(models.Model):
    _name="dtw.workmanship"
    _description="工单明细"
    _rec_name="name"
    name=fields.Char('工艺号',compute="_compute_name")
    main_id=fields.Many2one('dtw.workmanship.main',string='工单号',ondelete="restrict",index=True)
    workposition_id=fields.Many2one('dtw.workposition',string='工位')
    target_tork=fields.Float(string="目标扭力值",digits='Product Unit of Measure',required="1")
    tork_unit=fields.Selection([('Nm','Nm'),('ft.lb','ft.lb'),('in.lb','in.lb'),('kg.cm','kg.cm')],default="Nm",string='扭力单位',required="1")
    min_tork=fields.Float(string='目标最低值',digits='Product Unit of Measure')
    max_tork=fields.Float(string='目标最大值',digits='Product Unit of Measure')
    allow=fields.Float(string='误差范围 %')
    remark=fields.Char("说明")
    angle=fields.Float('角度',digits='Product Unit of Measure',default=0)
    barcode = fields.Char('Barcode',compute="_compute_barcode")
    company_id = fields.Many2one('res.company', related="main_id.company_id",store=True)
    def name_get(self):
        result=[]
        for record in self:
            result.append((record.id, u"%s@%s" % (record.workposition_id.name, record.main_id.name)))
        return result

    @api.depends('main_id','workposition_id')
    def _compute_name(self):
        for r in self:
            r.name="%s@%s" % (r.workposition_id.name,r.main_id.name)    

    @api.depends('target_tork','angle')
    def _compute_barcode(self):
        for r in self:
            r.barcode="T%sU%sA%s@%s" % (str(r.target_tork),r.tork_unit,str(r.angle),str(r.id))
        
    @api.onchange('target_tork','allow')
    def _onchange_target_tork(self):
        if self.target_tork:
            self.min_tork=self.target_tork*(1-self.allow/100)
            self.max_tork=self.target_tork*(1+self.allow/100)

class Workdata(models.Model):
    _name="dtw.workdata"
    _description="工作数据"
    _order="datetime_work desc"
    workmanship_id=fields.Many2one('dtw.workmanship',string="工艺号",ondelete="restrict")
    datetime_work=fields.Datetime('操作时间')
    operator_id=fields.Many2one('dtw.operator',string="操作人员",ondelete="restrict")
    real_tork=fields.Float(string='实际值')
    real_angle=fields.Float('实际角度值')
    wrench_identity=fields.Char('扳手标识')

    main_id=fields.Many2one('dtw.workmanship.main',string="工单号",related="workmanship_id.main_id",store=True)
    workposition_id=fields.Many2one('dtw.workposition',string='工位',related="workmanship_id.workposition_id",store=True)
    target_tork=fields.Float(string="目标扭力值",related="workmanship_id.target_tork",store=True)
    tork_unit=fields.Selection([('Nm','Nm'),('ft.lb','ft.lb'),('in.lb','in.lb'),('kg.cm','kg.cm')],'扭力单位',
                               related="workmanship_id.tork_unit",store=True)
    min_tork=fields.Float(string='允许最低值',related="workmanship_id.min_tork",store=True)
    max_tork=fields.Float(string='允许最大值',related="workmanship_id.max_tork",store=True)
    flag=fields.Boolean('超差',default=False,compute='_compute_flag',store=True)
    angle=fields.Float('目标角度值',related="workmanship_id.angle",store=True)    
    company_id = fields.Many2one('res.company', ondelete="restrict")
    remark=fields.Char("说明")
    @api.depends('min_tork','max_tork','real_tork')
    def _compute_flag(self):
        for r in self:
            if r.real_tork < r.min_tork or r.real_tork > r.max_tork:
                r.flag=True
            else:
                r.flag=False
    
class Operator(models.Model):
    _name="dtw.operator"
    _description="人员信息"
    user_id=fields.Many2one('res.users',string='odoo用户')
    name=fields.Char("姓名",related='user_id.partner_id.name',store=True)
    login=fields.Char('登录名',related='user_id.login',store=True)
    password=fields.Char('密码',related='user_id.password',store=True)
    company_id = fields.Many2one('res.company', related='user_id.company_id',store=True)
    mobile=fields.Char('手机',related="user_id.partner_id.mobile",store=True)


    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         password=vals.get('password',False)
    #         if not password:
    #             vals['password']=''
    #         user_id=vals['user_id']
    #         vals['password']= self.env['res.users'].browse([user_id]).password
    #     return super().create(vals_list)





class Users(models.Model):
    _inherit="res.users"
    password = fields.Char(copy=False)        
