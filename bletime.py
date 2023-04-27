import sys
import csv
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from ui_main import Ui_MainWindow

# 指令字典
COMMAND_DICT = {
    'AT+OKSCT': '+ACK:OKSCT',
    'AT+OKSCM': '+ACK:OKSCM',
    # 添加更多的指令和接收字符串
}
# MainWindow 类
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.process_file)

    # 处理日志文件
    def process_file(self):
        log_file_path = self.lineEdit.text()
        dict_file_path = self.lineEdit_2.text()
        csv_file_path = self.lineEdit_3.text()
        if not all([log_file_path, dict_file_path, csv_file_path]):
            QtWidgets.QMessageBox.critical(self, "错误", "请填写所有必填项！")
            return
        COMMAND_DICT = self.load_dict(dict_file_path)
        process_log_file(log_file_path, csv_file_path, COMMAND_DICT)
# 处理指令发送和接收时间
send_dict = {}
result_dict = {}
for line in f:
    for send_str, recv_str in COMMAND_DICT.items():
        # 如果找到了指令发送的行，记录下发送时间和指令 ID
        if send_str in line:
            send_time, send_command_id = parse_line(line)
            send_dict[send_command_id] = {'time': send_time, 'command': send_str}
        # 如果找到了指令接收的行，并且之前已经找到了对应的指令发送行
        elif recv_str in line:
            recv_time, recv_command_id = parse_line(line)
            send_info = send_dict.get(recv_command_id)
            if send_info:
                send_time = send_info['time']
                send_command = send_info['command']
                # 如果接收行的指令 ID 与发送行的指令 ID 相同，则计算时间差并写入CSV文件
                time_delta = (recv_time - send_time).total_seconds() * 1000
                writer.writerow([send_command, recv_str, time_delta])
                del send_dict[recv_command_id]
                # 记录时间差结果到结果字典
                result_dict.setdefault(send_command, []).append(time_delta)
            break

