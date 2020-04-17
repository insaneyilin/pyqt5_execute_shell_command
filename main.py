#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QComboBox,
    QMessageBox,
    QApplication
)
from PyQt5.QtCore import QCoreApplication


# get pid list by process name
def get_pid(process):
    cmd = "ps aux| grep '%s'|grep -v grep " % process
    out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    infos = out.stdout.read().splitlines()
    pidlist = []
    if len(infos) >= 1:
        for i in infos:
            pid = i.split()[1]
            if pid not in pidlist:
                pidlist.append(int(pid))
        return pidlist
    else:
        return []


class SimpleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        btn_say_hello = QPushButton('Open', self)
        btn_say_hello.clicked.connect(self.execute_say_hello)
        btn_say_hello.move(50, 50)

        btn_close_say_hello = QPushButton('Close', self)
        btn_close_say_hello.clicked.connect(self.close_say_hello)
        btn_close_say_hello.move(50, 100)

        self.resize(200, 200)
        self.move(300, 300)
        self.setWindowTitle('PyQt5 Demo')
        self.show()


    def execute_say_hello(self):
        print('Execute say_hello.sh')
        cmd = 'bash say_hello.sh &'
        print('cmd: {}'.format(cmd))
        subprocess.call(cmd, shell=True)


    def close_say_hello(self):
        for process in ['bash say_hello.sh']:
            for pid in get_pid(process):
                print("kill process {}".format(pid))
                subprocess.Popen("kill -9 {}".format(pid), shell=True)


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?",
                                     QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close_say_hello()
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = SimpleWidget()

    sys.exit(app.exec_())
