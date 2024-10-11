import sys
import os
from threading import Thread
from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QIcon
from jinja2 import Environment, FileSystemLoader


from lib.model.Appsettings import AppSettings
from lib.domain.ScoreReporter import ScoreReporter
 
class App_Window():
    def __init__(self,args=None):
        super().__init__()

        self.init_from_config(args)
        self.progress_rate = 0
        self.data_file_path = self.abspath( f"data/{self.grade}/scores.csv")
        self.output_path =  self.abspath("data/output")
        self.levels_file_path =self.abspath(f"config/{self.grade}/levels.csv")
        self.config_file_path =self.abspath(f"config/{self.grade}/config.json")

        # 绑定信号槽
        self.signals = MySignals()
        self.signals.update_progress.connect(self.set_progress)
        self.signals.alert_msg.connect(self.alert_msg)

        # 初始化窗口
        self.initUI()
        pass

    def alert_msg(self, msgType, msg):
        QMessageBox.warning(None, msgType, msg)
    def abspath(self, path):
        if not os.path.isabs(path):
            path = os.path.join(os.getcwd(), path)

        return os.path.abspath(path)    
    def init_from_config(self,args):
        # 初始化配置, 从命令行参数中获取或从配置文件.env中读取
        appSettings = AppSettings()
        
        if args:
            self.exam = args.exam if args.exam else appSettings.default_exam
            self.grade = args.grade if args.grade else appSettings.default_grade
            self.school = args.school if args.school else appSettings.default_school
        else:
            self.exam = appSettings.default_exam
            self.grade = appSettings.default_grade
            self.school = appSettings.default_school    
        pass

    def initUI(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('UI/demoui1.ui')

        self.initTextBoxes()
        self.initComboBoxes()
        self.bindBtns()

        self.hide_progress()

    def bindBtns(self):
        # 绑定按钮事件 btn_start_job btn_browse_data btn_browse_output_path
        self.ui.btn_start_job.clicked.connect(self.startJob)
        self.ui.btn_browse_data.clicked.connect(self.browseData)
        # self.ui.txt_data_file_path.clicked.connect(self.browseData)
         
        self.ui.btn_browse_output_path.clicked.connect(self.browseOutputPath)


        pass

    def initComboBoxes(self):
        # 初始化下拉框数据  cb_exam cb_grade
        self.ui.cb_exam.addItems([ '上学期期中考试', '上学期期末考试', '下学期期中考试', '下学期期末考试' ])
        self.ui.cb_grade.addItems([ '初一年级', '初二年级', '初三年级'])

        self.ui.cb_exam.setCurrentText(self.exam)
        self.ui.cb_grade.setCurrentText(self.grade)

        pass

    def initTextBoxes(self):
        # 初始化文本框数据 txt_school txt_output_path
        self.ui.txt_school.setText(self.school)
        self.ui.txt_output_path.setText(self.output_path)
        self.ui.txt_data_file_path.setText(self.data_file_path)

        # set readonly
        self.ui.txt_data_file_path.setReadOnly(True)
        self.ui.txt_output_path.setReadOnly(True)
        pass

    def hide_progress(self):
        # 隐藏进度条
        self.ui.progressBar_job.setVisible(False)    

    def show_progress(self):
        # 显示进度条
        self.ui.progressBar_job.setVisible(True)

    def set_progress(self, rate):
        # 设置进度条
        self.ui.progressBar_job.setValue(rate)
        
        
    def startJob(self):
        # 开启辅助线程处理任务， 并通过信号更新进度条
        print("开始处理")
        
        # 创建新的线程执行计算
        thread = Thread(target=self.thread_job)
        thread.start()

        pass

    def stopJob(self):
        print("停止处理")
        pass

    def browseData(self):
        # 打开文件选择框, 获取文件路径
        file_path, _ = QFileDialog.getOpenFileName(None, "选择数据文件", "", "CSV Files (*.csv)")
        if not file_path:
            return
        self.data_file_path = file_path
        print("选择数据", file_path)
        self.initTextBoxes()
        pass
 
    def browseOutputPath(self):
        # 打开文件夹选择框, 获取文件夹路径
        directory = QFileDialog.getExistingDirectory(None, "选择输出路径", self.output_path)
        if not directory:
            return
        self.output_path = directory

        print("选择输出路径",directory)
        self.initTextBoxes()

        pass

    def thread_job(self):
        # 辅助线程处理任务
        print("辅助线程处理任务")

        self.grade = self.ui.cb_grade.currentText()
        self.levels_file_path = self.abspath(f"config/{self.grade}/levels.csv")
        self.config_file_path =self.abspath(f"config/{self.grade}/config.json")

        try:
            reporter = ScoreReporter(self.data_file_path, self.config_file_path, self.levels_file_path)
        except Exception as e:
            print(e)
            self.signals.alert_msg.emit("错误", "读取配置文件失败 ！\r\n "+str(e) )

            return
            
        env = Environment(loader=FileSystemLoader('templates'))

        # 清除output 文件夹下的所有文件
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        if self.ui.chk_personal.isChecked():
        # 渲染学生报告
            studentReportModels = reporter.calculate_students()
            student_report_template = env.get_template('student.template.html')
            for studentReportModel in studentReportModels:
                studentReportModel.title = f'{self.school}-{self.grade}-{self.exam}'
                model = studentReportModel.__dict__
                html = student_report_template.render(model)
                with open(f'{self.output_path}/{studentReportModel.class_name}-{studentReportModel.student_name}.html', 'w', encoding='utf-8') as f:
                    f.write(html)


        if self.ui.chk_class.isChecked():
        # 渲染班级报告
            classReportModels = reporter.calculate_classes()
            class_report_template = env.get_template('class.template.html')
            for classReportModel in classReportModels:
                model = classReportModel.__dict__
                html = class_report_template.render(model)
                with open(f'{self.output_path}/{classReportModel.class_name}.html', 'w', encoding='utf-8') as f:
                    f.write(html)

        print("辅助线程处理任务完成")

        self.signals.alert_msg.emit("完成", "处理完成! 请在输出文件夹中查看报告。")
        pass

class MySignals(QObject):
    update_progress = Signal(int)
    alert_msg = Signal(str,str)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 设置logo
    app.setWindowIcon(QIcon('logo.png'))
    app_window = App_Window(None)
    app_window.ui.show()
    sys.exit(app.exec_())