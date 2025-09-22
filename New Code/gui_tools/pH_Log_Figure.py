

def PltCanvas(FigureCanvas):
    def __init__(self):
        fig = Figure(figsize = (5, 4), dpi = 100)
        # self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_ylim(bottom = 0, top = 15)
        self.ax.set_xlim(left = 0)
        self.ax.yaxis.set_major_locator(MultipleLocator(1))
        self.ax.yaxis.set_minor_locator(MultipleLocator(0.2))
        self.ax.set_title('pH v.s. Time')
        self.ax.set_ylabel('pH')
        self.ax.set_xlabel('Datapoints')