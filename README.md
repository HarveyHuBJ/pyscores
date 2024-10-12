# pyscores

# 1. 功能
根据提供的班级学生成绩

- 输出每个学生的成绩及排名
- 输出班级的成绩分布



# 2. 使用说明

参考[使用说明](./pyscore使用说明.md)



# 3. 依赖

- numpy
- pandas
- pyinstaller



# 4. 制作成Exe

~~~sh
pyinstaller -F App.py --hidden-import PySide6.QtXml --icon="logo.png" --exclude-module PyQt5
pyinstaller -F App.py --noconsole --hidden-import PySide6.QtXml --icon="logo.png" --exclude-module PyQt5
xcopy /Y templates dist\templates
xcopy /Y /S data dist\data
xcopy /Y ui dist\ui
xcopy /Y /S config dist\config
copy .env dist\.env
copy C:\Windows\Fonts\simhei.ttf dist\simhei.ttf
~~~

