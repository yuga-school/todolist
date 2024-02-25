import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QFormLayout, QGroupBox, QLabel, QScrollArea
from PySide6.QtGui import QFont
from datetime import datetime, timedelta
from functools import partial
from form_layout import FormLayoutWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('MainWindow')
        self.setGeometry(455, 200, 700, 540)

        current_script_path = os.path.realpath(__file__)
        self.parent_directory = os.path.dirname(current_script_path)
        self.occasion_textfile_directory = os.path.join(self.parent_directory, 'data.txt')

        self.divide_occasion = []
        self.divide_occasion = self.read_datatext(self.occasion_textfile_directory)

        for i in range(len(self.divide_occasion)):
            if os.path.isfile(os.path.join(self.parent_directory, f'{self.divide_occasion[i]}.txt')) != True:
                self.divide_occasion[i] = None

        self.occasion_bt = []
        self.deaddate = []
        self.task_detail = []
        self.it = []

        self.font = QFont()
        self.font2 = QFont()
        self.font.setPointSize(20)
        self.font2.setPointSize(15)

        for i in range(len(self.divide_occasion)):
            self.it.append(i)

        current_time = datetime.now()
        for i in range(len(self.divide_occasion)):
            self.task_detail.append(self.read_datatext(os.path.join(self.parent_directory, f'{self.divide_occasion[i]}.txt')))

        for i in range(len(self.divide_occasion)):
            if self.task_detail[i][0] == 'None':
                self.task_detail.append(0)
                continue

            time_list = [int(x) for x in self.task_detail[i][0].split(':')]
            dt1 = datetime(year=time_list[0], month=time_list[1], day=time_list[2], hour=time_list[3], minute=time_list[4])
            ct = datetime(year=current_time.year, month=current_time.month, day=current_time.day, hour=current_time.hour, minute=current_time.minute)
            td = dt1 - ct
            total_minutes = (td).total_seconds() // 60
            self.deaddate.append(total_minutes)

        datesort = {name: age for name, age in zip(self.it, self.deaddate)}
        datesort = sorted(datesort.items(), key=lambda x: x[1])
        self.it = [name for name, _ in datesort]

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setGeometry(440, 65, 250, 465)

        for i in range(len(self.divide_occasion)):
            self.occasion_bt.append(QPushButton(self.divide_occasion[i], self))

        self.form_layout_widget = FormLayoutWidget(self)
        self.scroll_area.setWidget(self.form_layout_widget)

        self.save_btn = QPushButton('追加', self)
        self.save_btn.setGeometry(520, 505, 100, 30)
        self.save_btn.setFixedSize(330, 20)
        self.save_btn.clicked.connect(self.btn_save_clicked)

        self.init_navi_msg = 'Todoリスト'
        self.todolistlabel = QLabel(self.init_navi_msg, self)
        self.detail = QLabel('詳細', self)
        self.todolistlabel.setGeometry(510, 15, 620, 50)
        self.detail.setGeometry(180, 15, 600, 50)
        self.todolistlabel.setFont(self.font)
        self.detail.setFont(self.font)

        self.name_tb = QTextEdit('', self)
        self.deadline_tb = QTextEdit('', self)
        self.explain_tb = QTextEdit('', self)
        self.detaildeadline_lb = QLabel('期限', self)
        self.detailexplain_lb = QLabel('説明', self)
        self.detaildeadline_tb = QTextEdit('', self)
        self.detailexplain_tb = QTextEdit('', self)
        self.detaildeadline_tb.setReadOnly(True)
        self.detailexplain_tb.setReadOnly(True)
        self.name_tb.setFixedSize(330, 30)
        self.detaildeadline_lb.setFont(self.font2)
        self.detailexplain_lb.setFont(self.font2)
        self.detaildeadline_tb.setFixedSize(400, 50)
        self.detailexplain_tb.setFixedSize(400, 100)
        self.deadline_tb.setFixedSize(330, 30)
        self.explain_tb.setFixedSize(330, 30)
        self.detaildeadline_tb.setFont(self.font)
        self.detailexplain_tb.setFont(self.font2)
        self.lb_navi = QLabel('', self)
        self.lb_navi.setGeometry(15, 35, 620, 30)

        self.form_layout1 = QFormLayout(self)
        self.form_layout1.addRow("名前:", self.name_tb)
        self.form_layout1.addRow("期限:", self.deadline_tb)
        self.form_layout1.addRow(QLabel('Y:M:d:h:mの形で入力してください．例:(2024年3月1日9時0分)->2024:3:1:9:0', self))
        self.form_layout1.addRow("説明:", self.explain_tb)
        self.form_layout1.addRow("", self.save_btn)

        self.group_box = QGroupBox("Todoリストにタスクを追加する", self)
        self.group_box.setLayout(self.form_layout1)

        self.main_layout1 = QScrollArea(self)
        self.main_layout1.setGeometry(10, 330, 410, 200)
        self.main_layout1.setWidget(self.group_box)

        self.form_layout2 = QFormLayout(self)
        self.form_layout2.addRow("", self.detaildeadline_lb)
        self.form_layout2.addRow("", self.detaildeadline_tb)
        self.form_layout2.addRow("", self.detailexplain_lb)
        self.form_layout2.addRow("", self.detailexplain_tb)

        self.group_box2 = QGroupBox("", self)
        self.group_box2.setLayout(self.form_layout2)

        self.main_layout2 = QScrollArea(self)
        self.main_layout2.setGeometry(10, 65, 410, 250)
        self.main_layout2.setWidget(self.group_box2)

    def btn_save_clicked(self):
        self.divide_occasion.append(self.name_tb.toPlainText())
        self.occasion_bt.append(QPushButton(self.divide_occasion[-1], self))
        dead_txt = self.deadline_tb.toPlainText()
        explain_txt = self.explain_tb.toPlainText()

        if dead_txt == '':
            dead_txt = 'None'
        if explain_txt == '':
            explain_txt = 'None'

        arr = [dead_txt, explain_txt]
        self.task_detail.append(arr)
        it = len(self.occasion_bt)
        self.occasion_bt[it - 1].clicked.connect(partial(self.btn_task_clicked, it - 1))
        self.form_layout_widget.add_button(self)
        self.save_text(self.occasion_textfile_directory)

    def btn_task_clicked(self, i):
        self.detaildeadline_tb.setText(self.task_detail[i][0])
        self.detailexplain_tb.setText(self.task_detail[i][1])

    def save_text(self, path):
        with open(path, mode='w', encoding='utf_8') as file:
            file.write(' '.join(self.divide_occasion))
        file_path = os.path.join(self.parent_directory, f'{self.divide_occasion[-1]}.txt')
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f'{self.task_detail[-1][0]} ')
            file.write(f'{self.task_detail[-1][1]}\n')

    def read_datatext(self, path):
        if os.path.isfile(path):
            with open(path, encoding='utf_8') as file:
                text = file.read()
            return text.split()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
