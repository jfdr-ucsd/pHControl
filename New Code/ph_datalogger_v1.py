import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QSlider,
    QVBoxLayout, QHBoxLayout, QSizePolicy,
    QLabel, QFileDialog, QDoubleSpinBox,
    QComboBox, QGridLayout
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator

from gui_tools.sliders import SliderWithTicks
from gui_tools.pump_choice import ChooseAcidBase
from gui_tools.graph_paper import GraphPaperWidget
from gui_tools.pH_logger import pHLogger

import numpy
import os
import random
import matplotlib
matplotlib.use("Qt5Agg")

class Log_pH_MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.started = False
        self.saving_filepath = None
        self.collecting = False
        self.time_interval = 0.1

        self.setWindowTitle("pH Data Logger")

        self.data_t = [0]
        self.data_pH = [0]

        self.setGeometry(100, 100, 900, 600)

        row0_layout = QHBoxLayout()

        self.figure = Figure(figsize = (5, 4), dpi = 100)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_ylim(bottom = 0, top = 15)
        self.ax.yaxis.set_major_locator(MultipleLocator(1))
        self.ax.yaxis.set_minor_locator(MultipleLocator(0.2))
        self.ax.set_title('pH v.s. Time')
        self.ax.set_ylabel('pH')
        self.ax.set_xlabel('Time (s)')
        self.line, = self.ax.plot([], [], 'b-o')

        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        row0_layout.addWidget(self.canvas, stretch=2) 

        self.time_interval = 0.1
        self.collector = pHLogger(interval = self.time_interval)
        self.collector.new_data.connect(self.deal_with_data)

        col0_layout = QVBoxLayout()

        # GO Button to start data collection
        self.start_button = QPushButton("▶")
        self.start_button.setStyleSheet(
            "QPushButton { " \
            "background-color: green; " \
            "color: white; " \
            "font-size: 40pt; " \
            "height: 80px; " \
            "width: 80px; } " \
            "QPushButton:disabled { " \
            "background-color: lightgray; " \
            "color: darkgray; " \
            "font-size: 40pt; " \
            "height: 80px; " \
            "width: 80px;}")
        self.start_button.setFixedSize(100, 50)
        self.start_button.clicked.connect(self.start_process)
        self.status_label = QLabel("Push the Arrow to Start pH Logging")

        # STOP Button to halt data collection
        self.BigRedButton = QPushButton("STOP")
        
        self.BigRedButton.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-size: 20pt;
                height: 60px;
            }
            QPushButton:disabled {
                background-color: lightgray;
                color: darkgray;
                font-size: 20pt;
                height: 60px;
            }
        """)
        self.BigRedButton.clicked.connect(self.stop_collecting)
        
        # pH Logging Time Interval Between Datapoints:
        self.time_interval_label = QLabel("Interval (s):")
        self.interval_choices = QDoubleSpinBox()
        self.interval_choices.setDecimals(2)
        self.interval_choices.setRange(0.1, 10.0)
        self.interval_choices.setValue(self.time_interval)
        self.interval_choices.valueChanged.connect(self.change_interval)
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(self.time_interval_label)
        interval_layout.addWidget(self.interval_choices)

        self.pump_choose = ChooseAcidBase()

        col0_layout.addWidget(self.start_button)
        col0_layout.addStretch()
        col0_layout.addLayout(interval_layout)
        col0_layout.addStretch()
        col0_layout.addWidget(self.pump_choose)
        col0_layout.addStretch()
        col0_layout.addWidget(self.BigRedButton)

        row0_layout.addLayout(col0_layout, stretch = 1)

        self.slider = SliderWithTicks(
            figure_widget = self.canvas,
            min_val = 0,
            max_val = 100,
            tick_interval = 10,
            callback = self.spinbox_changed,
        )


        main_layout = QVBoxLayout()
        graph_widget = GraphPaperWidget(grid_spacing=25)
        main_layout.addWidget(graph_widget)
        main_layout.addLayout(row0_layout)
        main_layout.addWidget(self.slider)
        
        self.setLayout(main_layout)

    def start_process(self):
        if not self.started:
            # TODO: Replace desktop_path with the Student's allowed directory on the course laptop
            desktop_path = "/Users/ericoberholtz/Desktop/pH_Data_Students"
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Select CSV File to save data",
                os.path.join(desktop_path, "data.csv"), # default name
                options = options,
            )
        
            if file_path:
                self.csv_file_path = file_path
                self.started = True
                self.collecting = True
                self.status_label.setText(f"pH Datalogging started\n\tSaving to: {file_path}")
                self.start_button.setEnabled(False)
                self.BigRedButton.setEnabled(True)
                print(f"Boolean flag set to True, CSV path: {self.csv_file_path}")
            else:
                self.status_label.setText(f"User canceled process (no file selected)")

            self.data_t.clear()
            self.data_pH.clear()
            self.line.set_data([0], [0])
            self.ax.relim()
            self.ax.set_ylim(bottom = 0, top = 15)
            self.ax.autoscale_view(scalex=True, scaley=False)
            self.canvas.draw()

            self.start_pHLog()

    def stop_collecting(self):
        """Stops data collection"""
        if self.collecting:
            self.stop_pHLog()
            self.collecting = False
            self.export_ready = True
            # TODO: export the data
            self.started = False
            self.status_label.setText("Data collection stopped. Ready to export")
            self.BigRedButton.setEnabled(False)
            self.start_button.setEnabled(True)
            print("collecting = False, export_ready = True")

    def change_interval(self, value):
        self.time_interval = value
        self.update_collector_interval(value)

    def spinbox_changed(self, value):
        # update slider without triggering its signal
        self.slider.blockSignals(True)
        self.slider.setValue(int(value))
        self.slider.blockSignals(False)
        self.applied_voltage = value / 100.0

    def start_pHLog(self):
        if not self.collector.isRunning():
            self.collector.start()

    def stop_pHLog(self):
        self.collector.stop()
    
    def update_collector_interval(self, interval):
        self.collector.set_time_interval(interval)

    def deal_with_data(self, t, pH):
        if not hasattr(self, "line"):
            return
        self.data_t.append(t)
        self.data_pH.append(pH)
        self.line.set_data(self.data_t, self.data_pH)
        self.ax.relim()
        self.ax.autoscale_view(scalex = True, scaley = False)
        self.canvas.draw_idle()
        print(f"t: {t:.2f}, pH: {pH:.2f}\t{len(self.data_t)}, {len(self.data_pH)}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Log_pH_MainWindow()
    window.show()