# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math

from django.db import models
from django.utils.timezone import now


class Employee(models.Model):
    IDENTITY_TYPE_CHOICES = (
        (0, u'身份证'),
        (1, u'护照'),
        (2, u'驾驶证'),
    )

    STATUS_CHOICES = (
        (0, u'离职'),
        (1, u'在职'),
        (2, u'待审')
    )

    GENDER_CHOICES = (
        (0, u'男'),
        (1, u'女'),
    )

    employee_id = models.AutoField(verbose_name=u'雇员编号', primary_key=True)
    name = models.CharField(verbose_name=u'姓名', max_length=20)
    nickname = models.CharField(verbose_name=u'昵称', max_length=30)
    type_id = models.ForeignKey('employee.EmployeeType', verbose_name=u'等级', related_name='type', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.IntegerField(verbose_name=u'状态', choices=STATUS_CHOICES, default=2)
    city = models.ForeignKey('employee.EmployeeCity', verbose_name=u'城市', related_name='city', on_delete=models.SET_NULL, blank=True, null=True)
    identity_type = models.IntegerField(verbose_name=u'证件类型', choices=IDENTITY_TYPE_CHOICES, default=0)
    identity = models.CharField(verbose_name=u'证件号码', max_length=20)
    birthday = models.DateField(verbose_name=u'生日')
    gender = models.IntegerField(verbose_name=u'性别', choices=GENDER_CHOICES)
    mobile = models.CharField(verbose_name=u'联系电话', max_length=20)
    dingtalk_id = models.CharField(verbose_name=u'钉钉', max_length=30, null=True)
    wechat_id = models.CharField(verbose_name=u'微信', max_length=30)
    audio = models.CharField(verbose_name=u'音频', max_length=100)
    avatar = models.CharField(verbose_name=u'头像', max_length=100, blank=True, null=True)
    head_img1 = models.CharField(verbose_name=u'图片1', max_length=100, blank=True, null=True)
    head_img2 = models.CharField(verbose_name=u'图片2', max_length=100, blank=True, null=True)
    head_img3 = models.CharField(verbose_name=u'图片3', max_length=100, blank=True, null=True)
    join_date = models.DateField(verbose_name=u'入职日期', default=now().date())
    leave_date = models.DateField(verbose_name=u'离职日期', blank=True, null=True)
    slogan = models.CharField(verbose_name=u'标语', max_length=150, null=True)

    class Meta:
        db_table = 'employee'
        verbose_name = u'雇员信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def age(self):
        if not self.birthday:
            return 'N/A'
        return math.floor((now().date() - self.birthday).days / 365)

    age.short_description = u'年龄'

    def delete(self, using=None, keep_parents=False):
        self.status = self.STATUS_CHOICES[0]
        self.leave_date = now().date()
        self.save()


class EmployeeTag(models.Model):
    STATUS_CHOICES = (
        (False, u'停用'),
        (True, u'激活'),
    )

    tag_id = models.AutoField(verbose_name=u'标签编号', primary_key=True)
    name = models.CharField(verbose_name=u'标签', max_length=15)
    status = models.BooleanField(verbose_name=u'状态', choices=STATUS_CHOICES, default=True)

    class Meta:
        db_table = 'employee_tag'
        verbose_name = u'雇员标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        self.status = self.STATUS_CHOICES[False]
        self.save()


class EmployeeCity(models.Model):
    STATUS_CHOICES = (
        (False, u'停用'),
        (True, u'激活'),
    )

    city_id = models.AutoField(verbose_name=u'城市编号', primary_key=True)
    name = models.CharField(verbose_name=u'中文名', max_length=15)
    en_name = models.CharField(verbose_name=u'英文名', max_length=15, blank=True, null=True)
    status = models.BooleanField(verbose_name=u'状态', choices=STATUS_CHOICES, default=True)

    class Meta:
        db_table = 'employee_city'
        verbose_name = u'雇员城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        self.status = self.STATUS_CHOICES[False]
        self.save()

    @staticmethod
    def get_all_city():
        # return EmployeeCity.objects().all()
        pass


class EmployeeType(models.Model):
    STATUS_CHOICES = (
        (0, u'停用'),
        (1, u'激活'),
    )

    type_id = models.AutoField(verbose_name=u'雇员类型编号', primary_key=True)
    name = models.CharField(verbose_name=u'雇员类型', max_length=15)
    price = models.FloatField(verbose_name=u'每小时费用', default=0)
    status = models.IntegerField(verbose_name=u'状态', choices=STATUS_CHOICES, default=1)

    class Meta:
        db_table = 'employee_type'
        verbose_name = u'雇员类型信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        self.status = self.STATUS_CHOICES[0]
        self.save()


class EmployeeGroup(models.Model):
    GENDER_CHOICES = (
        (0, u'男'),
        (1, u'女'),
        (2, u'混合'),
    )
    STATUS_CHOICES = (
        (0, u'停用'),
        (1, u'激活'),
    )

    group_id = models.AutoField(verbose_name=u'雇员钉钉群编号', primary_key=True)
    name = models.CharField(verbose_name=u'群名称', max_length=20)
    dingding_id = models.CharField(verbose_name=u'钉钉id', max_length=30)
    gender = models.IntegerField(verbose_name=u'性别', choices=GENDER_CHOICES, default=2)
    status = models.IntegerField(verbose_name=u'状态', choices=STATUS_CHOICES, default=1)

    class Meta:
        db_table = 'employee_group'
        verbose_name = u'雇员群信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.dingding_id

    def delete(self, using=None, keep_parents=False):
        self.status = self.STATUS_CHOICES[0]
        self.save()
