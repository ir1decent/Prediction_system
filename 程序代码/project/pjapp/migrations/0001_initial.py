# Generated by Django 4.2.1 on 2023-06-09 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('userId', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='工号')),
                ('userName', models.CharField(max_length=20, verbose_name='用户名')),
                ('passWord', models.CharField(max_length=20, verbose_name='密码')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('projectId', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True, verbose_name='项目ID')),
                ('projectName', models.CharField(max_length=255, verbose_name='项目名称')),
                ('ctime', models.DateField(verbose_name='创建时间')),
                ('Idincharge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pjapp.users')),
            ],
        ),
        migrations.CreateModel(
            name='PrimaryData',
            fields=[
                ('dataName', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True, verbose_name='数据名称')),
                ('pfilename', models.CharField(max_length=255, verbose_name='文件名1')),
                ('sfilename', models.CharField(max_length=255, verbose_name='文件名2')),
                ('filepath', models.CharField(max_length=255, verbose_name='文件路径')),
                ('projectId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pjapp.project')),
            ],
        ),
        migrations.CreateModel(
            name='PredictedData',
            fields=[
                ('dataName', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True, verbose_name='数据名称')),
                ('filename', models.CharField(max_length=255, verbose_name='文件名')),
                ('filepath', models.CharField(max_length=255, verbose_name='文件路径')),
                ('projectId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pjapp.project')),
            ],
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OperationTime', models.DateField(verbose_name='操作时间')),
                ('DorAorC', models.CharField(choices=[('delete', '删除'), ('add', '增加')], default='add', max_length=10, verbose_name='操作')),
                ('Operationdata', models.CharField(max_length=200, verbose_name='操作数据名称')),
                ('OperationUserId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pjapp.users')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imgname', models.CharField(max_length=200, verbose_name='图片名称')),
                ('imgpath', models.CharField(max_length=200, verbose_name='图片路径')),
                ('txtname', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pjapp.predicteddata')),
            ],
        ),
    ]
