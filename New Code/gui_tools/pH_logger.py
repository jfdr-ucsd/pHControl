import time
from PyQt5.QtCore import QThread, pyqtSignal
import random
class pHLogger(QThread):
    new_data = pyqtSignal(float, float)

    def __init__(self, interval=1.0, parent = None):
        super().__init__(parent)
        self.time_interval = interval
        self.running = False
        # self.t0 = time.time()
    
    def run(self):
        self.running = True
        self.t0 = time.time()
        while self.running:
            time.sleep(self.time_interval)
            new_pH = self.get_pH_value()

            t = time.time() - self.t0
            self.new_data.emit(t, new_pH)
            print('sent new data')

    def stop(self):
        self.running = False

    def get_pH_value(self):
        # Communicate to pH probe via USB port
        return random.uniform(0, 15)
    
    def set_time_interval(self, interval):
        self.time_interval = interval