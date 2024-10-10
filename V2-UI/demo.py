import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QLabel, QPushButton, QVBoxLayout, QWidget, QComboBox, QFileDialog, QCheckBox
from PyQt5.QtCore import Qt

class App2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('App主窗口')
        self.setGeometry(100, 100, 600, 400)

        # 创建菜单栏
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('菜单')

        # 创建【开始】菜单项
        startAction = QAction('开始', self)
        startAction.triggered.connect(self.show_main)
        fileMenu.addAction(startAction)

        # 创建【说明】菜单项
        explainAction = QAction('说明', self)
        explainAction.triggered.connect(self.show_explain)
        fileMenu.addAction(explainAction)

        # 主窗口内容
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout()

        # 文字Label
        self.title_label = QLabel("{标题位置}", self)
        self.title_label.setStyleSheet("font-size: 20pt;")

        # 下拉框
        self.grade_combobox = QComboBox(self)
        self.grade_combobox.addItems(['请选择', '初一', '初二', '初三'])

        # 按钮
        self.next_button = QPushButton('下一步', self)
        self.next_button.clicked.connect(self.show_step_window)

        layout.addWidget(self.title_label)
        layout.addWidget(self.grade_combobox)
        layout.addWidget(self.next_button)
        self.main_widget.setLayout(layout)

        # 步骤窗口内容
        self.step_widget = QWidget(self)
        self.step_layout = QVBoxLayout()

        # 步骤标题Label
        self.step_title_label = QLabel('步骤标题', self)

        # 文件选择框
        self.file_button = QPushButton('选择数据文件', self)
        self.file_button.clicked.connect(self.select_file)

        # 输出目录选择框
        self.output_button = QPushButton('选择结果文件保存目录', self)
        self.output_button.clicked.connect(self.select_output)

        # 复选框
        self.checkbox_a = QCheckBox('A', self)
        self.checkbox_b = QCheckBox('B', self)
        self.checkbox_c = QCheckBox('C', self)
        self.checkbox_d = QCheckBox('D', self)

        # 按钮：开始处理
        self.process_button = QPushButton('开始处理', self)
        self.process_button.clicked.connect(self.process_data)

        # 按钮：返回
        self.back_button = QPushButton('返回', self)
        self.back_button.clicked.connect(self.show_main)

        self.step_layout.addWidget(self.step_title_label)
        self.step_layout.addWidget(self.file_button)
        self.step_layout.addWidget(self.output_button)
        self.step_layout.addWidget(self.checkbox_a)
        self.step_layout.addWidget(self.checkbox_b)
        self.step_layout.addWidget(self.checkbox_c)
        self.step_layout.addWidget(self.checkbox_d)
        self.step_layout.addWidget(self.process_button)
        self.step_layout.addWidget(self.back_button)

        self.step_widget.setLayout(self.step_layout)
        self.step_widget.hide()

        # 默认显示主窗口
        self.show_main()

    def show_main(self):
        self.main_widget.show()
        self.step_widget.hide()

    def show_explain(self):
        # 这里可以添加显示说明内容的代码
        print("显示App说明内容")

    def show_step_window(self):
        self.main_widget.hide()
        self.step_widget.show()

    def select_file(self):
        # 这里可以添加文件选择的代码
        filename, _ = QFileDialog.getOpenFileName(self, "选择数据文件")
        print(f"选择的文件：{filename}")

    def select_output(self):
        # 这里可以添加输出目录选择的代码
        directory = QFileDialog.getExistingDirectory(self, "选择结果文件保存目录")
        print(f"选择的目录：{directory}")

    def process_data(self):
        # 这里可以添加处理数据的代码
        print("开始处理数据")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App2()
    ex.show()
    sys.exit(app.exec_())