from django.db import models


class UserInfo(models.Model):
    STATUS_CHOICES = (
        (False, u'停用'),
        (True, u'激活'),
    )

    user_id = models.AutoField(verbose_name=u'用户编号', primary_key=True)
    open_id = models.CharField(verbose_name=u'微信开放编号', max_length=60, blank=True, null=True)
    nickname = models.CharField(verbose_name=u'用户昵称', max_length=20, blank=True, null=True)
    last_login = models.DateTimeField(verbose_name=u'最后登入时间', blank=True, null=True)

    class Meta:
        db_table = 'user_info'
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname


class UserLoginInfo(models.Model):
    user_login_id = models.AutoField(verbose_name=u'用户登入编号', primary_key=True)
    user_id = models.ForeignKey('user_info.UserInfo', verbose_name=u'用户id', related_name='_user_id', on_delete=models.SET_NULL, blank=True, null=True)
    time = models.DateTimeField(verbose_name=u'时间')

    class Meta:
        db_table = 'user_login_info'
        verbose_name = u'用户登陆日志'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_id.nickname
