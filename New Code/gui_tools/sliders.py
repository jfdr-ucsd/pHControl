from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QSlider, QSizePolicy,
    QHBoxLayout, QLabel, QDoubleSpinBox
)
from PyQt5.QtCore import Qt

class SliderWithTicks(QWidget):
    """ Slider widget with numeric tick labels aligned with major ticks"""
    def __init__(self, figure_widget, label_text = "Voltage Input:", min_val = 0, max_val = 100, tick_interval = 10, callback = None, parent = None):
        super().__init__(parent)
        self.callback = callback
        self.figure_widget = figure_widget 
        self.min_val = min_val
        self.max_val = max_val
        self.tick_interval = tick_interval

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        slider_row = QHBoxLayout()
        slider_row.setContentsMargins(0, 0, 0, 0)
        slider_row.setSpacing(5)
        self.left_label = QLabel(label_text)
        self.left_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        slider_row.addWidget(self.left_label)

        self.slider_container = QWidget()
        slider_layout = QVBoxLayout(self.slider_container)
        slider_layout.setContentsMargins(0, 0, 0, 0)
        slider_layout.setSpacing(0)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(min_val)
        self.slider.setMaximum(max_val)
        self.slider.setTickPosition(QSlider.NoTicks)
        self.slider.setTickInterval(tick_interval)
        self.slider.setSingleStep(1)
        slider_layout.addWidget(self.slider)
        
        self.ticks_layout = QHBoxLayout()
        self.ticks_layout.setContentsMargins(0,0,0,0)
        self.ticks_layout.setSpacing(0)

        self.tick_labels = []
        num_ticks = (max_val - min_val)//tick_interval + 1
        for i in range(num_ticks):
            lbl = QLabel(str(min_val + i*tick_interval))
            lbl.setAlignment(Qt.AlignCenter)
            self.tick_labels.append(lbl)
            self.ticks_layout.addWidget(lbl)
        
        slider_layout.addLayout(self.ticks_layout)

        slider_row.addWidget(self.slider_container)

        self.slider_input = QDoubleSpinBox()
        self.slider_input.setDecimals(2)
        self.slider_input.setRange(0, 100)
        self.slider_input.setValue(10)
        slider_row.addWidget(self.slider_input)
        
        slider_row.setStretch(0, 0)
        slider_row.setStretch(1, 2)
        slider_row.setStretch(2, 0)
        layout.addLayout(slider_row)
        self.setLayout(layout)
        
        self.slider.valueChanged.connect(self.value_changed)
        self.slider_input.valueChanged.connect(self.value_changed)

        self.update_tick_labels()

    def resizeEvent(self, event):
        """Distribute labels evenly under slider"""
        super().resizeEvent(event)
        self.update_tick_labels()

    def update_tick_labels(self):
        slider_width = self.slider.width()
        num_labels = len(self.tick_labels)
        if num_labels > 1:
            label_width = slider_width / (num_labels - 1)
            for label in self.tick_labels:
                label.setFixedWidth(label_width)

    def _slider_changed(self, value):
        if self.callback:
            self.callback(value)

    def setValue(self, value):
        self.slider.setValue(value)

    def value(self):
        return self.slider.value()
    
    def blockSignals(self, bool):
        self.slider.blockSignals(bool)

    def value_changed(self, value):
        sender = self.sender()

        if sender == self.slider:
            self.slider_input.blockSignals(True)
            self.slider_input.setValue(value)
            self.slider_input.blockSignals(False)
        elif sender == self.slider_input:
            self.slider.blockSignals(True)
            self.slider.setValue(value)
            self.slider.blockSignals(False)
