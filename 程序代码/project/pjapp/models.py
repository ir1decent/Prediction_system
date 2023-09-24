from django.db import models

# Create your models here.
class Users(models.Model):
    """用户表"""
    userId = models.CharField(verbose_name="工号", max_length=20, unique=True, primary_key=True)
    userName = models.CharField(verbose_name="用户名", max_length=20)
    passWord = models.CharField(verbose_name="密码", max_length=20)
class Project(models.Model):
    """项目表"""
    projectId = models.CharField(verbose_name="项目ID", max_length=200, unique=True, primary_key=True)
    projectName = models.CharField(verbose_name="项目名称", max_length=255)
    ctime = models.DateField(verbose_name="创建时间")
    Idincharge = models.ForeignKey("Users", to_field="userId", null=True,blank=True, on_delete=models.SET_NULL)
class PrimaryData(models.Model):
    """原始数据表"""
    projectId = models.ForeignKey("Project", to_field="projectId", null=True,blank=True, on_delete=models.SET_NULL)
    dataName = models.CharField(verbose_name="数据名称", max_length=255, unique=True, primary_key=True)
    pfilename = models.CharField(verbose_name="文件名1",max_length=255)
    sfilename = models.CharField(verbose_name="文件名2", max_length=255)
    filepath = models.CharField(verbose_name="文件路径",max_length=1000)
class PredictedData(models.Model):
    """预测数据表"""
    projectId = models.ForeignKey("Project", to_field="projectId", null=True, blank=True, on_delete=models.SET_NULL)
    dataName = models.CharField(verbose_name="数据名称", max_length=255, unique=True, primary_key=True)
    filename = models.CharField(verbose_name="文件名", max_length=255)
    filepath = models.CharField(verbose_name="文件路径", max_length=1000)
class Operation(models.Model):
    """操作记录表"""
    OperationUserId = models.ForeignKey("Users", to_field="userId", null=True,blank=True, on_delete=models.SET_NULL)
    OperationTime = models.DateField(verbose_name="操作时间")
    DorAorC = models.CharField(verbose_name="操作", max_length=10, choices=(('delete', '删除'), ('add', '增加')), default = 'add')
    Operationdata = models.CharField(verbose_name="操作数据名称", max_length=200)
class Image(models.Model):
    imgname = models.CharField(verbose_name="图片名称", max_length=200)
    imgpath = models.CharField(verbose_name="图片路径", max_length=200)
    txtname = models.ForeignKey("PredictedData", to_field="dataName", null=True,blank=True, on_delete=models.SET_NULL)