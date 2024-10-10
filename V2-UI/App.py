import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader
from lib.model.appsettings import AppSettings

class App_Window():
    def __init__(self,args=None):
        super().__init__()

        self.init_config(args)
        self.initUI()
        pass

    def init_config(self,args):
        # 初始化配置, 从命令行参数中获取或从配置文件.env中读取
        self.config = AppSettings()
        if args:
            self.config.default_exam = args.exam if args.exam else self.config.default_exam
            self.config.default_grade = args.grade if args.grade else self.config.default_grade
            self.config.default_school = args.school if args.school else self.config.default_school
        pass

    def initUI(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('V2-UI/UI/demoui1.ui')

        self.initTextBoxes()
        self.initComboBoxes()
        self.bindBtns()

    def bindBtns(self):
        # 绑定按钮事件 btn_start_job btn_browse_data btn_browse_output_path
        self.ui.btn_start_job.clicked.connect(lambda: QMessageBox.information(self.ui, "提示", "开始处理"))
        self.ui.btn_browse_data.clicked.connect(lambda: QMessageBox.information(self.ui, "提示", "选择数据"))
        self.ui.btn_browse_output_path.clicked.connect(lambda: QMessageBox.information(self.ui, "提示", "选择输出路径"))
        pass

    def initComboBoxes(self):
        # 初始化下拉框数据  cb_exam cb_grade
        self.ui.cb_exam.addItems(['请选择', '上学期期中考试', '上学期期末考试', '下学期期中考试', '下学期期末考试' ])
        self.ui.cb_grade.addItems(['请选择', '初一年级', '初二年级', '初三年级'])

        self.ui.cb_exam.setCurrentText(self.config.default_exam)
        self.ui.cb_grade.setCurrentText(self.config.default_grade)

        pass

    def initTextBoxes(self):
        # 初始化文本框数据 txt_school txt_output_path
        self.ui.txt_school.setText(self.config.default_school)
        self.ui.txt_output_path.setText("/output")
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_window = App_Window(None)
    app_window.ui.show()
    sys.exit(app.exec_())