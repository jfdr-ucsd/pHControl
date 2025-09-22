from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout,
    QComboBox, QLabel
)

class ChooseAcidBase(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.pump_choose = QComboBox()
        self.pump_choose.addItems(
            [
                "Acid",
                "Base"
            ]
        )
        layout.addWidget(self.pump_choose)

        self.pump_choose.currentTextChanged.connect(self.pump_changed)

        self.pump = None

    def pump_changed(self, text):
        """text: 'Acid' or 'Base'"""
        self.pump = text
        print(f"Pump changed! Current pump = {self.pump}")
