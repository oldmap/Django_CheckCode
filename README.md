# Django_CheckCode

## 项目简介：
    本项目是使用最新的python3.6.1版本编写的在网站后台生成验证码图片的插件，该插件源码位于项目中app01/tools/CheckCode.py文件内，从头至尾均做了注释。为了便于展示效果，使用Django框架写了一个web（一切从简，未做任何修饰，一目了然，方便其他人引用）。
    
    本文旨在记录一下自己的学习过程，欢迎随时交流互相学习。
### 插件工作原理：
    1 随机生成的指定位数的字符串，同时将其也保存到session中，用与验证用户输入合法性；
    2 将生成的字符串绘制到图片，并将图片保存到二进制类型的的内存IO；
    3 返回 生成的字符串 和 图片的二进制流（已保存到内存IO中）；
    
### 本插件优势
    1 生成的验证码图片不落地，全部在内存中保存，调用完毕，内存即释放，减少磁盘IO以及中间一些不必要的环节，提高并发处理效率；
    2 以二进制流返回数据，前端配合js实现点击验证码图片，即可更换验证码；

------

    当我们登录或注册网站时，经常看到需要输入一张图片中的数字或是字符，验证码的作用是什么？
    1 防止对某一个特定注册用户用特定程序暴力破解方式进行不断的登陆尝试；
    2 防止防止批量注册；


#### 插件源代码
    见位于项目中 app01/tools/CheckCode.py 这个文件内

#### views视图函数
    查看app01/tools/views.py 这个文件

#### 前端html如何调用？
    参考项目内 templates/login.html文件

## Howto
1 安装python3运行环境
```
    推荐使用pyenv管理多python环境
    。。。略
```
2 clone该项目
```
git clone https://github.com/xiaotaoliu/Django_CheckCode.git
```
3 安装依赖模块
```
cd Django_CheckCode
pip3 install -r requirement.txt 
```
4 测试运行
```
cd Django_CheckCode
python manager.py runserver 192.168.11.5:80
# 将IP地址替换成你主机的IP
```
5 注意事项
    Django_CheckCode/Django_CheckCode/settins.py配置文件中
```
# django 配置
ALLOWED_HOSTS = [
    '192.168.11.5',   # 若你用IP访问django如：http://192.168.11.5:/login，需要添加IP到这里
    '.example.com',   # 你的域名或是子域名
    '.example.com.',  # Also allow FQDN and subdomains
]
```
uwsgi的方式我放到了script目录下，可以参考。
