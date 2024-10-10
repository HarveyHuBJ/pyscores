# Python程序在Linux下打包的说明



Ubuntu系统



## 安装Python

~~~bash
sudo apt update
sudo apt upgrade
sudo apt install python3
~~~



## 安装CX-Freeze

~~~bash
pip install cx-Freeze
~~~



## 安装patchelf工具

~~~bash
sudo apt install patchelf
~~~

检查是否安装完成

~~~bash
which patchelf
~~~





## 准备Setup文件

~~~python
from cx_Freeze import setup, Executable

setup(name="YourApp",
      version="1.0",
      description="Description of your app",
      executables=[Executable("your_script.py")]
      )
~~~

确保将 `"YourApp"`, `"1.0"`, `"Description of your app"`, 和 `your_script.py` 替换为实际的应用程序名称、版本、描述以及要转换为可执行文件的 Python 脚本文件名。



## 编译项目

~~~bash
python3 setup.py build
~~~

这将在当前目录下创建一个 `build` 文件夹，其中包含生成的可执行文件。



运行程序

~~~bash
./YourApp
~~~





# 使用Zip打包程序

并复制到本地

## 安装zip

~~~bash
sudo apt install zip
~~~



## 打包data目录

~~~bash
zip -r data.zip data
~~~



## 复制到本机

~~~bash
scp  -r vmadmin@<host>:~/pyscores/data 'C:\temp\data'
~~~

