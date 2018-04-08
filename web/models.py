from django.db import models

# Create your models here.

from rbac.models import User as RbacUser
class UserInfo(models.Model):
    nickname = models.CharField(max_length=16)
    user = models.OneToOneField(RbacUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname
class Order(models.Model):
    """
    报障单
    """
    TYPE_CHOICES = (
        (1, "租房"),
        (2, "买房"),
        (3, "卖房")
    )

    ctype = models.IntegerField(
        choices=TYPE_CHOICES,
        default=1,
        verbose_name="客户类型")

    title = models.CharField(verbose_name='标题',max_length=32)
    detail = models.TextField(verbose_name='详细')

    create_user = models.ForeignKey(UserInfo,related_name='aaa',on_delete=models.CASCADE)
    # ctime = models.DateTimeField(auto_now_add=True,default=datetime.datetime.now)
    ctime = models.DateTimeField(auto_now_add=True)
    status_choice = (
        (1,'公户'),
        (2,'私户'),
    )
    # status_choice = (
    #     (1,'公户'),
    #     (2,'私户'),
    #     (3,'已处理')
    # )
    status = models.IntegerField(choices=status_choice,default=2)
    processor = models.ForeignKey(UserInfo,related_name='bbb',null=True,blank=True,on_delete=models.CASCADE)
    solution = models.TextField(null=True,blank=True)
    ptime = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.title

class Update(models.Model):
    aa = models.ForeignKey(Order, related_name='bbb', on_delete=models.CASCADE)
    bb = models.ForeignKey(UserInfo, related_name='ccc', on_delete=models.CASCADE)
    detail = models.TextField(verbose_name='详细')
    ptime = models.DateTimeField(null=True, blank=True)
