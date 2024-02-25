from PySide6.QtWidgets import QWidget, QFormLayout, QPushButton, QLabel, QScrollArea
from functools import partial

class FormLayoutWidget(QWidget):
    def __init__(self, mainself):
        super().__init__()

        self.form_layout = QFormLayout(self)

        for i in range(len(mainself.occasion_bt)):
            if mainself.deaddate[mainself.it[i]] < 0:
                continue
            if mainself.divide_occasion[mainself.it[i]] != None:
                mainself.occasion_bt[mainself.it[i]].setFixedSize(220, 40)
                self.form_layout.addRow("", mainself.occasion_bt[mainself.it[i]])
                mainself.occasion_bt[mainself.it[i]].clicked.connect(partial(mainself.btn_task_clicked, mainself.it[i]))
        self.finished_lb = QLabel('終了済み', self)
        self.finished_lb.setFont(mainself.font)
        self.form_layout.addRow("", self.finished_lb)
        for i in range(len(mainself.occasion_bt)):
            if mainself.deaddate[mainself.it[i]] < 0:
                mainself.occasion_bt[mainself.it[i]].setFixedSize(220, 40)
                self.form_layout.addRow("", mainself.occasion_bt[mainself.it[i]])
                mainself.occasion_bt[mainself.it[i]].clicked.connect(partial(mainself.btn_task_clicked, mainself.it[i]))
        self.setLayout(self.form_layout)

    def add_button(self, mainself):
        mainself.occasion_bt[-1].setFixedSize(220, 40)
        self.form_layout.addRow("", mainself.occasion_bt[-1])
        return self
