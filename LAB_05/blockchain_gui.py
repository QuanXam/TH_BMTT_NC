import sys
from PyQt5 import QtWidgets
from ui.blockchain_ui import Ui_MainWindow
from blockchain.block import Block
from blockchain.blockchain import Blockchain  # Thêm import này

class BlockchainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Khởi tạo blockchain
        self.blockchain = Blockchain()

        # Kết nối các nút với hàm xử lý
        self.ui.btn_add_transaction.clicked.connect(self.add_transaction)
        self.ui.btn_mine_block.clicked.connect(self.mine_block)
        self.ui.btn_check_validity.clicked.connect(self.check_chain_validity)

        # Hiển thị chuỗi khởi tạo
        self.display_chain()

    def add_transaction(self):
        sender = self.ui.lineEdit_sender.text()
        receiver = self.ui.lineEdit_receiver.text()
        amount_text = self.ui.lineEdit_amount.text()

        if not sender or not receiver or not amount_text:
            self.ui.plainTextEdit_chain.setPlainText("Vui lòng nhập đầy đủ thông tin giao dịch.")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            self.ui.plainTextEdit_chain.setPlainText("Số tiền phải là số.")
            return

        index = self.blockchain.add_transaction(sender, receiver, amount)
        self.ui.plainTextEdit_chain.setPlainText(f"Giao dịch đã được thêm vào block #{index}.")

        # Xóa các ô nhập liệu
        self.ui.lineEdit_sender.clear()
        self.ui.lineEdit_receiver.clear()
        self.ui.lineEdit_amount.clear()

    def mine_block(self):
        previous_block = self.blockchain.get_previous_block()
        previous_proof = previous_block.proof
        new_proof = self.blockchain.proof_of_work(previous_proof)
        previous_hash = previous_block.hash

        # Thêm phần thưởng cho người đào
        self.blockchain.add_transaction("Genesis", "Miner", 1)

        new_block = self.blockchain.create_block(new_proof, previous_hash)
        self.ui.plainTextEdit_chain.setPlainText(f"Block #{new_block.index} đã được tạo thành công.")
        self.display_chain()

    def check_chain_validity(self):
        is_valid = self.blockchain.is_chain_valid(self.blockchain.chain)
        if is_valid:
            self.ui.plainTextEdit_chain.setPlainText("Chuỗi blockchain hợp lệ.")
        else:
            self.ui.plainTextEdit_chain.setPlainText("Chuỗi blockchain KHÔNG hợp lệ.")

    def display_chain(self):
        text = ""
        for block in self.blockchain.chain:
            text += f"Block #{block.index}\n"
            text += f"Timestamp: {block.timestamp}\n"
            text += f"Transactions: {block.transactions}\n"
            text += f"Proof: {block.proof}\n"
            text += f"Previous Hash: {block.previous_hash}\n"
            text += f"Hash: {block.hash}\n"
            text += "-" * 40 + "\n"
        self.ui.plainTextEdit_chain.setPlainText(text)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = BlockchainApp()
    window.show()
    sys.exit(app.exec_())