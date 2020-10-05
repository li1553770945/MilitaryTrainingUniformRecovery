from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save


class RecordModel(models.Model):
    class Meta:
        ordering = ["-time"]
        db_table = 'record'
        verbose_name = "记录"
        verbose_name_plural = verbose_name

    time = models.DateTimeField(verbose_name='时间',auto_now_add=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    manager_name = models.CharField(null=False, default="", verbose_name="管理员姓名", max_length=100)
    name = models.CharField(null=False, default="", max_length=100, verbose_name="姓名")
    stu_id = models.CharField(null=False, default="", max_length=20, verbose_name="学号")


def create_manager_name(sender, instance, **kwargs):
    instance.manager_name = instance.manager.first_name


pre_save.connect(create_manager_name, sender=RecordModel)
