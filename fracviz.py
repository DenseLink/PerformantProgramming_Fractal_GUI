from matplotlib import pyplot, image
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import PySide2
from PySide2 import QtUiTools
from PySide2 import QtCore
from PySide2.QtWidgets import QPushButton, QVBoxLayout, QLabel, QLineEdit, QWidget, QMainWindow
from PySide2.QtCore import QObject, QFile
import sys
from PySide2.QtWidgets import QApplication
#addwidget
import wsl
import fractal
import time
from multiprocessing import Process
from multiprocessing.shared_memory import *
from multiprocessing.managers import *
from PySide2.QtGui import QIntValidator
import threading
from threading import Thread



#good website https://www.learnpyqt.com/courses/start/signals-slots-events/
#layout management http://zetcode.com/gui/pyqt5/layout/
#info on PySide https://srinikom.github.io/pyside-docs/PySide/QtUiTools/QUiLoader.html#PySide.QtUiTools.PySide.QtUiTools.QUiLoader.load
#QT Documentation https://wiki.qt.io/Qt_for_Python_Tutorial_HelloWorld
# QT Documentation https://doc.qt.io/qt-5/qlineedit.html
class FractalWindow(QWidget):
    #entire ui is being constructed
    #slide 7a slide 6 how to connect ui file. It is find child functionality.
    #focus on 7a and 7b and 5b and 5a
    def __init__(self, filename, app):
        super().__init__()
        self._filename = filename

        self._window = QMainWindow()

        # Load the file into a window
        #lookup custom widget classes with QT
        self.ui_file = PySide2.QtCore.QFile(self._filename)
        self.ui_file.open(PySide2.QtCore.QFile.ReadOnly)
        self.loader = PySide2.QtUiTools.QUiLoader()
        self._window = self.loader.load(self.ui_file, self)
        self.ui_file.close()

        #self._window.show()
        # Load the file into a window

        self._figure, self._axes = pyplot.subplots(1)
        self._canvas = FigureCanvas(self._figure)
        self._axes.set_axis_off()
        self._axes.set_position([0, 0, 1, 1])
        self._iterations = self._window.findChild(QLineEdit, "iterations")
        self._iterations.setValidator(QIntValidator(1, 9999, self._iterations))

        self._layout = self._window.findChild(QVBoxLayout, "layout")
        self._layout.addWidget(self._canvas)
        self._processes = self._window.findChild(QLineEdit, "processes")
        self._processes.setValidator(QIntValidator(1, 200, self._processes))

        self._resolution_x = self._window.findChild(QLineEdit, "resolution_x")
        self._resolution_x.setValidator(QIntValidator(1,9999, self._resolution_x))

        self._resolution_y = self._window.findChild(QLineEdit, "resolution_y")
        self._resolution_y.setValidator(QIntValidator(1, 9999, self._resolution_y))

        self._reset_button = self._window.findChild(QPushButton, "reset_button")
        self._status = self._window.findChild(QLabel, "status")



        #jackson = image.imread("snakes.jpg")
        #self._axes.imshow(image.imread("snakes.jpg"))

        #self.fractal1 = fractal.Mandelbrot(70, 70, 100)







        #The code below acts as signals for when text is entered on the gui or when a button is pushed
        self._iterations.returnPressed.connect(self.iteration)
        self._iterations.returnPressed.connect(app.update_plot)
        self._processes.returnPressed.connect(self.process)
        self._processes.returnPressed.connect(app.update_plot)
        self._resolution_x.returnPressed.connect(self.x_res)
        self._resolution_x.returnPressed.connect(app.update_plot)
        self._resolution_y.returnPressed.connect(self.y_res)
        self._resolution_y.returnPressed.connect(app.update_plot)
        self._reset = False
        self._reset_button.pressed.connect(self.reset)
        self._reset_button.pressed.connect(app.update_plot)




    @property
    def axes(self):
        return self._axes

    @axes.setter
    def axes(self, axes):
        self._axes = axes

    @property
    def canvas(self):
        return self._canvas

    @canvas.setter
    def canvas(self, canvas):
        self._canvas = canvas

    @property
    def figure(self):
        return self._figure

    @figure.setter
    def figure(self, figure):
        self._figure = figure

    @property
    def iterations(self):
        return self._iterations

    @iterations.setter
    def iterations(self, iterations):
        self._iterations = iterations#self._window.findChild(QLineEdit, iterations)

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, layout):
        self._layout = self._window.findChild(QVBoxLayout, layout)

    @property
    def processes(self):
        return self._processes

    @processes.setter
    def processes(self, processes):
        self._processes = processes#self._window.findChild(QLineEdit, processes)

    @property
    def resolution_x(self):
        return self._resolution_x

    @resolution_x.setter
    def resolution_x(self, resolution_x):
        self._resolution_x = resolution_x#self._window.findChild(QLineEdit, resolution_x)

    @property
    def resolution_y(self):
        return self._resolution_y

    @resolution_y.setter
    def resolution_y(self, resolution_y):
        self._resolution_y = resolution_y#self._window.findChild(QLineEdit, resolution_y)

    @property
    def reset_button(self):
        return self._reset_button

    @reset_button.setter
    def reset_button(self, reset_button):
        self._reset_button = self._window.findChild(QPushButton, reset_button)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = self._window.findChild(QLabel, status)

    def x_res(self):
        #self._resolution_x.setText(self._resolution_x.text)
        self._status.setText("Calculating set...")  # = "calculating..."
    def y_res(self):
        #self._resolution_x.setText(self._resolution_x.text)
        self._status.setText("Calculating set...")  # = "calculating..."
    def iteration(self):
        #self._resolution_x.setText(self._resolution_x.text)
        self._status.setText("Calculating set...")  # = "calculating..."
    def process(self):
        #self._resolution_x.setText(self._resolution_x.text)
        self._status.setText("Calculating set...")  # = "calculating..."
    def reset(self):
        #self._resolution_x.setText(self._resolution_x.text)
        '''self._resolution_x = "175"
        self._resolution_y = 150"
        self._iterations = 20
        self._processes = 8'''
        #self._root_widget._status.setText("Calculating set...")
        self._status.setText("Calculating set...")  # = "calculating..."
        self._reset = True

class FractalApp(QObject):
    #handles even systems and does threading. nothing is being created
    def __init__(self, filename):
        self._filename = filename
        self._root_widget = FractalWindow(self._filename, self)
        self._image = None  # flag
        self._fractal1 = None
        self._queue = []
        self._lock = threading.Lock()
        self.update_plot()


    def update_plot(self):
        p = self._root_widget.processes.text()
        x = None
        y = None
        i = None
        if self._root_widget._reset == False:
            x = int(self._root_widget.resolution_x.text())
            y = int(self._root_widget.resolution_y.text())
            i = int(self._root_widget.iterations.text())

        if self._root_widget._reset == True:
            #self._root_widget.resolution_x.setText('175')
            #self._root_widget.resolution_y.setText('150')
            #self._root_widget.iterations.setText('20')
            #self._root_widget.processes.setText('8')
            #x = 175
            #y = 150
            #i = 20
            x = int(self._root_widget.resolution_x.text())
            y = int(self._root_widget.resolution_y.text())
            i = int(self._root_widget.iterations.text())
            self._root_widget._reset = False


        #self._queue.append((self._root_widget.resolution_x.text(),self._root_widget.resolution_y.text(), self._root_widget.iterations.text(),self._root_widget.processes.text()))
        #print(self._queue)
        t = threading.Thread(target=self.custom_class, args=(x,y,i,p), daemon=True)
        t.start()
        #print(self._queue.pop(0))


    @property
    def root_widget(self):
        #return self._filename
        return self._root_widget
    @property
    def fractal(self):
        return self._fractal1
    #generate data and calculation
    @property
    def image(self):
        return self._image
    #datatoimage also in documentation imshow to display. calculations to image
    def custom_class(self,x,y,i,p):
        with SharedMemoryManager() as smm:
            # self.tasks, self.data = self.fractal1.generate_tasks(170, 20)

            self._fractal1 = fractal.Mandelbrot(x, y, i)  # self.a.resolution_x, self.a.resolution_y, self.a.iterations
            # slist = smm.ShareableList(self.fractal1)
            p = int(self._root_widget.processes.text())
            tasks, data = self._fractal1.generate_tasks(smm, p)
            # for task in tasks: task()  # Don’t do this; it’s single-threaded and just an example.
            procs = []
            for task in tasks:
                procs.append(Process(target=task))
                procs[-1].start()
            [process.join() for process in procs]

            image_matrix = self._fractal1.data_to_image_matrix(data)
        #print(i)
        #print(self._root_widget.iterations.text())
        with self._lock:
            if str(x) != self._root_widget.resolution_x.text() or str(y) != self._root_widget.resolution_y.text() or str(i) != self._root_widget.iterations.text() or str(p) != self._root_widget.processes.text():
                return



            if self._image == None:
                self._image = self._root_widget.axes.imshow(image_matrix)
            else:
                self._image.set_data(image_matrix)  # can also use set_array
            self._root_widget._status.setText("")
            self._root_widget.canvas.draw()

def main():
    wsl.set_display_to_host() #This code is connecting the Qt gui to the config launcher
    app = QApplication(sys.argv) #This code is creating the application

    #pass the file name into a class then show the image
    application = FractalApp("fracviz.ui")
    application.root_widget.show()
    sys.exit(app.exec_())
    #pass the file name into a class then show the image


if __name__ == "__main__":
    main()