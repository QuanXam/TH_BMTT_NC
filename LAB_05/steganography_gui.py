import sys
from PyQt5 import QtWidgets
from ui.steganography_ui import Ui_MainWindow
from img_hidden.encrypt import encode_image
from img_hidden.decrypt import decode_image

class SteganographyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối các nút với hàm xử lý
        self.ui.btn_encode.clicked.connect(self.encode)
        self.ui.btn_decode.clicked.connect(self.decode)

    def encode(self):
        image_path = self.ui.lineEdit_imagePath.text()
        message = self.ui.lineEdit_message.text()

        if not image_path or not message:
            self.ui.textEdit_decoded.setText("Vui lòng nhập đầy đủ đường dẫn ảnh và thông điệp.")
            return

        try:
            encode_image(image_path, message)
            self.ui.textEdit_decoded.setText("Mã hóa thành công. Kiểm tra tệp encoded_image.png.")
        except Exception as e:
            self.ui.textEdit_decoded.setText(f"Lỗi: {str(e)}")

    def decode(self):
        image_path = self.ui.lineEdit_imagePath.text()

        if not image_path:
            self.ui.textEdit_decoded.setText("Vui lòng nhập đường dẫn ảnh đã mã hóa.")
            return

        try:
            decoded_message = decode_image(image_path)
            self.ui.textEdit_decoded.setText(f"Thông điệp giải mã: {decoded_message}")
        except Exception as e:
            self.ui.textEdit_decoded.setText(f"Lỗi: {str(e)}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SteganographyApp()
    window.show()
    sys.exit(app.exec_())

    