import sys
import ssl
import socket
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QMetaObject, Qt, Q_ARG
from ui.ssl import Ui_MainWindow


class ClientApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ssl_socket = None

        # Kết nối sự kiện GUI với nút gửi đúng tên
        self.ui.btn_send.clicked.connect(self.send_message_from_gui)

        # Bắt đầu kết nối SSL
        self.connect_ssl()

        # Thread lắng nghe dữ liệu từ server
        threading.Thread(target=self.receive_data, daemon=True).start()

        # Thread đọc từ terminal
        threading.Thread(target=self.read_from_terminal, daemon=True).start()

    def connect_ssl(self):
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        self.ssl_socket = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname='localhost')
        self.ssl_socket.connect(('127.0.0.1', 12345))
        print("Đã kết nối đến server")

    def send_message_from_gui(self):
        message = self.ui.lineEdit_input.text()
        if message and self.ssl_socket:
            self.ssl_socket.send(message.encode('utf-8'))
            self.ui.lineEdit_input.clear()
            # Không hiển thị gì ở giao diện khi gửi

    def read_from_terminal(self):
        while True:
            try:
                message = input("Nhập tin nhắn từ terminal: ")
                if message and self.ssl_socket:
                    self.ssl_socket.send(message.encode('utf-8'))
                    # Không hiển thị gì ở giao diện khi gửi
            except Exception as e:
                print(f"Lỗi khi gửi từ terminal: {e}")
                break

    def receive_data(self):
        try:
            while True:
                data = self.ssl_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                QMetaObject.invokeMethod(
                    self.ui.plainTextEdit_chat,
                    "appendPlainText",
                    Qt.QueuedConnection,
                    Q_ARG(str, message)
                )
        except Exception as e:
            QMetaObject.invokeMethod(
                self.ui.plainTextEdit_chat,
                "appendPlainText",
                Qt.QueuedConnection,
                Q_ARG(str, f"Lỗi nhận dữ liệu: {e}")
            )
        finally:
            self.ssl_socket.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClientApp()
    window.show()
    sys.exit(app.exec_())
