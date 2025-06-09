from PyQt5.QtWidgets import QApplication, QMainWindow
from ui.base64 import Ui_MainWindow  # Đúng class tên Ui_MainWindow
import sys
import base64

class Base64App(QMainWindow):  # Phải kế thừa từ QMainWindow
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_encrypt.clicked.connect(self.encrypt_text)
        self.ui.btn_decrypt.clicked.connect(self.decrypt_text)

    def encrypt_text(self):
        text = self.ui.plainTextEdit_input.toPlainText()
        encoded = base64.b64encode(text.encode()).decode()
        self.ui.plainTextEdit_output.setPlainText(encoded)

    def decrypt_text(self):
        encoded_text = self.ui.plainTextEdit_output.toPlainText()
        try:
            decoded = base64.b64decode(encoded_text.encode()).decode()
            self.ui.plainTextEdit_input.setPlainText(decoded)
        except Exception as e:
            self.ui.plainTextEdit_input.setPlainText("Giải mã thất bại: " + str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Base64App()
    window.show()
    sys.exit(app.exec_())
