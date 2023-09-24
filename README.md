
克里金工程数值预测系统
欢迎使用克里金工程数值预测系统！本系统是基于克里金插值方法开发的工具，用于进行空间数据插值和数值预测。通过该系统，您可以输入一组已知的空间数据点和一组想要得到的位置，并使用克里金插值方法生成预测模型，从而在规定位置进行数值预测。

系统要求
Python 3 或更高版本

安装
确保您的系统已安装 Python 3 或更高版本，推荐使用pycharm。
确保您的系统有浏览器如Edge,Chrome,Firefox等。
下载克里金工程数值预测系统的源代码。
解压缩源代码文件到您希望存放的目录。

配置环境
打开命令行终端。
进入克里金工程数值预测系统源代码所在的目录。
运行以下命令安装所需的依赖模块：
pip install -r requirements.txt

创建数据库
打开终端，运行以下命令以启动MySQL服务：
sudo mysql
若要利用工具创建你的数据库，执行以下命令：
create database your_name DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
若要展示数据库，执行：
show databases;

设置数据库连接：
在project/settings.py的DATABASE中进行设置，参照设置：
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',# 数据库类型
        'NAME': 'pjdatabase',# 数据库名字
        'USER': 'debian-sys-maint',# 用户名
        'PASSWORD': 'yP3Wy9jFtzg670Av',# 密码
        'HOST': '127.0.0.1',# 安装mysql的位置
        'PORT': 3306
    }
}

使用方法
在数据库设置好后,在项目目录中：
运行以下命令以迁移数据库设置：
python manage.py makemigrations
python manage.py migrate
若要运行系统，在项目目录下执行命令：
python manage.py runserver 8000(本地端口号）

重要文件：
function.so C++源码，实现克里金预测插值的部分
img 图片文件本地存储位置
manage.py 可执行文件
outfile 输出数据文件本地存储位置
predict_data.txt 输入数据1缓冲区
souce_data.txt 输入数据2缓冲区
out.txt 输出数据缓冲区
pjapp django框架源码
project django配置目录
pjapp/templates&statics 渲染文件
