import sys
import os

from datetime import datetime as dt
from threading import Thread
from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QObject, Signal,QUrl
from PySide6.QtGui import QIcon,QDesktopServices
from jinja2 import Environment, FileSystemLoader
from matplotlib import pyplot as plt
from logging import getLogger, DEBUG, FileHandler, StreamHandler,Formatter

from lib.model.Appsettings import AppSettings
from lib.domain.ScoreReporter import ScoreReporter
from lib.domain.FigureDrawer import SubjectDistributionDrawer


 
class App_Window():
    def __init__(self,args=None):
        super().__init__()

        self.init_from_config(args)
        self.progress_rate = 0

        # 初始化logger, 文件格式采用日期后缀
        log_file = f'app.log'  
        self.logger = self.initLogger(log_file)

        # 绑定信号槽
        self.signals = MySignals()
        self.signals.update_progress.connect(self.set_progress)
        self.signals.alert_msg.connect(self.alert_msg)

        # 初始化窗口
        self.initUI()
        pass

    def initLogger(self, log_file):
        logger = getLogger(__name__)
        logger.setLevel(DEBUG)

        # 创建一个 handler，用于写入日志文件
        file_handler = FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(DEBUG)

        # 创建一个 handler，用于输出到控制台
        console_handler = StreamHandler()
        console_handler.setLevel(DEBUG)

        formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 给 logger 添加 handler
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

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
            self.default_exam = args.exam if args.exam else appSettings.default_exam
            self.default_grade = args.grade if args.grade else appSettings.default_grade
            self.default_school = args.school if args.school else appSettings.default_school
        else:
            self.default_exam = appSettings.default_exam
            self.default_grade = appSettings.default_grade
            self.default_school = appSettings.default_school    
        pass

    def initUI(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('UI/demoui1.ui')

        self.initMenus()
        self.initComboBoxes()
        self.initTextBoxes()
        self.bindBtns()

        self.hide_progress()

    def initMenus(self):
        # 菜单点击事件绑定
        self.ui.actionReadme.triggered.connect(self.showReadme)
        self.ui.actionContact.triggered.connect(self.showContact)

    def showReadme(self):
        # 消息提示
        readme = "由Harvey Hu开发。 \r\n源码参考https://github.com/HarveyHuBJ/pyscores。"
        QMessageBox.information(None, "程序说明", readme)

        
    def showContact(self):
        # 消息提示
        readme = "QQ:10897366  \r\nEmail:tigerush80@hotmail.com"
        QMessageBox.information(None, "联系作者", readme)

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

        self.ui.cb_exam.setCurrentText(self.default_exam)
        self.ui.cb_grade.setCurrentText(self.default_grade)

        pass

    def initTextBoxes(self):
        # 初始化文本框数据 txt_school txt_output_path txt_data_file_path
        self.ui.txt_school.setText(self.default_school)
        self.ui.txt_output_path.setText(self.abspath( f'data/output/{self.get_grade()}'))
        self.ui.txt_data_file_path.setText(self.abspath( f"data/{self.get_grade()}/scores.csv"))

        # set readonly
        self.ui.txt_data_file_path.setReadOnly(True)
        self.ui.txt_output_path.setReadOnly(True)

        # set click action
        # self.ui.txt_data_file_path.mousePressEvent = lambda event: self.browseData()
        # self.ui.txt_output_path.mousePressEvent = lambda event: self.browseOutputPath()
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
        self.logger.debug("开始处理")
        
        # 创建新的线程执行计算
        thread = Thread(target=self.thread_job)
        thread.start()

        pass

    def stopJob(self):
        self.logger.debug("停止处理")
        pass

    def browseData(self):
        # 打开文件选择框, 获取文件路径
        file_path, _ = QFileDialog.getOpenFileName(None, "选择数据文件", "", "CSV Files (*.csv)")
        if not file_path:
            return
        self.ui.txt_data_file_path.setText(file_path)
        self.logger.debug("选择数据文件：", file_path)
         
        pass
 
    def browseOutputPath(self):
        # 打开文件夹选择框, 获取文件夹路径
        directory = QFileDialog.getExistingDirectory(None, "选择输出路径")
        if not directory:
            return

        self.ui.txt_output_path.setText(directory)
        self.logger.debug("选择输出路径:",directory)

        pass


    def get_grade(self):
        # 获取年级
        return self.ui.cb_grade.currentText()

    def get_levels_file_path(self):
        # 获取等级文件路径
        return self.abspath(f"config/{self.get_grade()}/levels.csv")
    
    def get_config_file_path(self):
        # 获取配置文件路径
        return self.abspath(f"config/{self.get_grade()}/config.json")

    def get_data_file_path(self):
        # 获取数据文件路径
        return self.ui.txt_data_file_path.text()
    
    def get_output_path(self):
        # 获取输出路径
        return self.ui.txt_output_path.text()

    def get_school(self):
        # 获取学校名称
        return self.ui.txt_school.text()
    
    def get_exam(self):
        # 获取考试类型
        return self.ui.cb_exam.currentText()
    

    def thread_job(self):
        # 辅助线程处理任务
        self.logger.debug("辅助线程处理任务")
        year = dt.now().strftime('%Y')
 

        try:
            reporter = ScoreReporter(self.get_data_file_path(), self.get_config_file_path(), self.get_levels_file_path())
        except Exception as e:
            self.logger.error(e)
            self.signals.alert_msg.emit("错误", "读取数据文件失败 ！\r\n "+str(e) )

            return
            
        env = Environment(loader=FileSystemLoader('templates'))

        output_path = self.get_output_path()
        # 清除output 文件夹下的所有文件
        if not os.path.exists(output_path):
            os.makedirs(output_path)


        try:

            # 渲染学生报告
            studentReportModels = reporter.calculate_students()
            if self.ui.chk_personal.isChecked():
                self.logger.info("开始处理个人成绩单任务")
                student_report_template = env.get_template('student.template.html')
                for studentReportModel in studentReportModels:
                    self.logger.debug(f"开始处理{studentReportModel.class_name}-{studentReportModel.student_name}成绩单")
                    studentReportModel.title = f'{year}-{self.get_school()}-{self.get_grade()}-{self.get_exam()}'
                    model = studentReportModel.__dict__
                    html = student_report_template.render(model)
                    with open(f'{output_path}/{studentReportModel.class_name}-{studentReportModel.student_name}.html', 'w', encoding='utf-8') as f:
                        f.write(html)


            if self.ui.chk_class.isChecked():
                self.logger.info("开始处理班级成绩单任务")

                # 渲染班级报告
                classReportModels = reporter.calculate_classes()
                
                class_report_template = env.get_template('class.template.html')
                for classReportModel in classReportModels:
                    self.logger.debug(f"开始处理{classReportModel.class_name}成绩单")
                    classReportModel.title = f'{year}-{self.get_school()}-{self.get_grade()}-{self.get_exam()}'
                    model = classReportModel.__dict__
                    html = class_report_template.render(model)
                    with open(f'{output_path}/{classReportModel.class_name}.html', 'w', encoding='utf-8') as f:
                        f.write(html)

                    # 绘图
                    
                    fiture_drawer = SubjectDistributionDrawer()
                    fiture_drawer.plot_cluster_bar_chart(classReportModel.level_distribution_data, f'{self.get_output_path()}/{classReportModel.class_name}-score-distribution.png')    

            self.logger.info("成绩单处理任务完成")

            self.signals.alert_msg.emit("完成", "成绩单处理完成! 请在输出文件夹中查看报告。")
            # 打开输出文件夹
            QDesktopServices.openUrl(QUrl.fromLocalFile(output_path))
        except Exception as e:
            self.logger.error(e)
            self.signals.alert_msg.emit("错误", "处理失败 ！\r\n 请联系维护人员。" )

            return
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