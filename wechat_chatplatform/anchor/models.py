# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math

from django.db import models
from django.utils.timezone import now

from wechat_chatplatform.common.choices import IdentityType, AnchorStatus, Gender, Status


class Anchor(models.Model):

    anchor_id = models.AutoField(verbose_name=u'店员编号', primary_key=True)
    name = models.CharField(verbose_name=u'姓名', max_length=20)
    nickname = models.CharField(verbose_name=u'昵称', max_length=30)
    type_id = models.ForeignKey('anchor.AnchorType', verbose_name=u'等级', related_name='type', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.IntegerField(verbose_name=u'状态', choices=AnchorStatus.AnchorStatusChoice.value, default=2)
    city_id = models.ForeignKey('anchor.AnchorCity', verbose_name=u'城市', related_name='city', on_delete=models.SET_NULL, blank=True, null=True)
    identity_type = models.IntegerField(verbose_name=u'证件类型', choices=IdentityType.IdentityTypeChoice.value, default=0)
    identity = models.CharField(verbose_name=u'证件号码', max_length=20)
    birthday = models.DateField(verbose_name=u'生日')
    gender = models.IntegerField(verbose_name=u'性别', choices=Gender.GenderChoices.value)
    mobile = models.CharField(verbose_name=u'联系电话', max_length=20)
    dingtalk_id = models.CharField(verbose_name=u'钉钉', max_length=30, blank=True, null=True)
    dingtalk_robot = models.CharField(verbose_name=u'钉钉个人机器人', max_length=100, blank=True, null=True)
    wechat_id = models.CharField(verbose_name=u'微信', max_length=30)
    audio = models.CharField(verbose_name=u'音频', max_length=100, blank=True, null=True)
    avatar = models.CharField(verbose_name=u'头像', max_length=100, blank=True, null=True)
    image = models.CharField(verbose_name=u'图片', max_length=300, blank=True, null=True)
    audit_date = models.DateTimeField(verbose_name=u'审核时间', blank=True, null=True)
    auditor = models.ForeignKey('platform_admin.AdminUser', verbose_name=u'审核人', related_name='auditor', on_delete=models.SET_NULL, blank=True, null=True)
    join_date = models.DateField(verbose_name=u'入职日期', blank=True, null=True)
    leave_date = models.DateField(verbose_name=u'离职日期', blank=True, null=True)
    slogan = models.CharField(verbose_name=u'标语', max_length=150, null=True)
    tags = models.CharField(verbose_name=u'标签', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'anchor'
        verbose_name = u'店员信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def age(self):
        if not self.birthday:
            return 'N/A'
        return math.floor((now().date() - self.birthday).days / 365)

    age.short_description = u'年龄'

    def constellation(self):
        if not self.birthday:
            return 'N/A'
        birthday = self.birthday.strftime('%m-%d')
        if birthday >= '12-22' or birthday <= '01-19':
            return u'摩羯座'
        elif '01-20' <= birthday <= '02-18':
            return u'水瓶座'
        elif '02-19' <= birthday <= '03-20':
            return u'双鱼座'
        elif '03-21' <= birthday <= '04-19':
            return u'白羊座'
        elif '04-20' <= birthday <= '05-20':
            return u'金牛座'
        elif '05-21' <= birthday <= '06-21':
            return u'双子座'
        elif '06-22' <= birthday <= '07-22':
            return u'巨蟹座'
        elif '07-23' <= birthday <= '08-22':
            return u'狮子座'
        elif '08-23' <= birthday <= '09-22':
            return u'处女座'
        elif '09-23' <= birthday <= '10-23':
            return u'天秤座'
        elif '10-24' <= birthday <= '11-22':
            return u'天蝎座'
        elif '11-23' <= birthday <= '12-21':
            return u'射手座'

    constellation.short_description = u'星座'

    def delete(self, using=None, keep_parents=False):
        self.status = AnchorStatus.leave.value
        self.leave_date = now().date()
        self.save()

    def audit_pass(self):
        if self.status == AnchorStatus.unaudit.value:
            self.status = AnchorStatus.active.value
            self.join_date = now().date()
            self.save()
            return True
        return False

    def audit_reject(self):
        if self.status == AnchorStatus.unaudit.value:
            self.status = AnchorStatus.audit_fail.value
            self.save()
            return True
        return False


class AnchorTag(models.Model):

    tag_id = models.AutoField(verbose_name=u'标签编号', primary_key=True)
    name = models.CharField(verbose_name=u'标签', max_length=15)
    status = models.BooleanField(verbose_name=u'状态', choices=Status.StatusChoice.value, default=Status.active.value)

    class Meta:
        db_table = 'anchor_tag'
        verbose_name = u'店员标签信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        self.status = Status.inactive.value
        self.save()


class AnchorCity(models.Model):
    STATUS_CHOICES = (
        (Status.inactive.value, u'停用'),
        (Status.active.value, u'激活'),
    )

    city_id = models.AutoField(verbose_name=u'城市编号', primary_key=True)
    name = models.CharField(verbose_name=u'中文名', max_length=15)
    en_name = models.CharField(verbose_name=u'英文名', max_length=15, blank=True, null=True)
    status = models.BooleanField(verbose_name=u'状态', choices=Status.StatusChoice.value, default=Status.active.value)

    class Meta:
        db_table = 'anchor_city'
        verbose_name = u'店员城市信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        self.status = Status.inactive.value
        self.save()
    #
    # @staticmethod
    # def get_all_city():
    #     # return EmployeeCity.objects().all()
    #     pass


class AnchorType(models.Model):
    STATUS_CHOICES = (
        (Status.inactive.value, u'停用'),
        (Status.active.value, u'激活'),
    )

    type_id = models.AutoField(verbose_name=u'店员类型编号', primary_key=True)
    name = models.CharField(verbose_name=u'店员类型', max_length=15)
    status = models.BooleanField(verbose_name=u'状态', choices=Status.StatusChoice.value, default=Status.active.value)

    class Meta:
        db_table = 'anchor_type'
        verbose_name = u'店员类型信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        self.status = Status.inactive.value
        self.save()


class AnchorGroup(models.Model):
    GENDER_CHOICES = (
        (Gender.male.value, u'男'),
        (Gender.female.value, u'女'),
        (Gender.mix.value, u'混合'),
    )
    STATUS_CHOICES = (
        (Status.inactive.value, u'停用'),
        (Status.active.value, u'激活'),
    )

    group_id = models.AutoField(verbose_name=u'店员钉钉群编号', primary_key=True)
    name = models.CharField(verbose_name=u'群名称', max_length=20)
    dingding_id = models.CharField(verbose_name=u'钉钉id', max_length=30)
    gender = models.IntegerField(verbose_name=u'性别', choices=Gender.GenderChoices.value, default=Gender.mix.value)
    status = models.BooleanField(verbose_name=u'状态', choices=Status.StatusChoice.value, default=Status.active.value)

    class Meta:
        db_table = 'anchor_group'
        verbose_name = u'店员群信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.dingding_id

    def delete(self, using=None, keep_parents=False):
        self.status = Status.inactive.value
        self.save()