import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QApplication, QPushButton, QLineEdit, QLabel, QHBoxLayout, QMessageBox
from PySide2.QtGui import QFont

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas

import re
import numpy as np



allowed_words = [
    'x',
    '/',
    '+',
    '*',
    '^',
    '-'
]
replacements = {
    '^': '**'
}

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        # Intializing the figure and its toolbar
        self.view = FigureCanvas(Figure(figsize=(8, 8)))
        self.axes = self.view.figure.subplots()
        self.toolbar = NavigationToolbar(self.view, self)
        
        # Function label and text edit bar
        self.functionTextEdit = QLineEdit(self)
        self.functionTextEdit.setFont(QFont('Sanserif', 10))
        self.functionTextEdit.setMaximumHeight(30)
        self.functionLabel=QLabel('Function:',self)
        
        # Lower x label and text edit bar
        self.minBoundaryLabel=QLabel('X min:',self)
        self.lowerBoundaryTextEdit = QLineEdit(self)
        self.lowerBoundaryTextEdit.setFont(QFont('Sanserif', 10))
        self.lowerBoundaryTextEdit.setMaximumHeight(30)
        
        # Higher x label and text edit bar
        self.maxBoundaryLabel=QLabel('X max:',self)
        self.higherBoundaryTextEdit = QLineEdit(self)
        self.higherBoundaryTextEdit.setFont(QFont('Sanserif', 10))
        self.higherBoundaryTextEdit.setMaximumHeight(30)

        # Intializing the layouts
        layout = QVBoxLayout()
        horizontalLayout = QHBoxLayout()
        horizontalBoudariesLayout = QHBoxLayout()
        
        # Adding the labels and test edits of x in a horizontal layout
        horizontalBoudariesLayout.addWidget(self.minBoundaryLabel)
        horizontalBoudariesLayout.addWidget(self.lowerBoundaryTextEdit)
        horizontalBoudariesLayout.addWidget(self.maxBoundaryLabel)
        horizontalBoudariesLayout.addWidget(self.higherBoundaryTextEdit)
        
        # Adding the function label and text edit bar in another horizontal layout
        horizontalLayout.addWidget(self.functionLabel)
        horizontalLayout.addWidget(self.functionTextEdit)
        
        # Creating the plot button
        self.plotButton = QPushButton('Plot')
        self.plotButton.clicked.connect(self.plotting)
        horizontalLayout.addWidget(self.plotButton)
        
        # Adding the graph and its tool bar in the main vertical layout
        layout.addWidget(self.toolbar)
        layout.addWidget(self.view)
        
        # Adding the other horizontal layouts to the main vertical layout
        layout.addLayout(horizontalBoudariesLayout)
        layout.addLayout(horizontalLayout)
        
        # Initializing the warning box
        self.warning = QMessageBox()

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()
        
        
    # A function to validate the input by the user and utilizes the warning box
    def inputValidation(self):
        self.lower = self.lowerBoundaryTextEdit.text()
        self.higher = self.higherBoundaryTextEdit.text()
        self.function = self.functionTextEdit.text()
        if self.lower.isalpha() or self.higher.isalpha():
            self.warning.setWindowTitle('Error')
            self.warning.setText('The limits values should be numbers')
            self.warning.exec_()
        elif self.lower == '' or self.higher == '' or self.function == '':
            self.warning.setWindowTitle('Error')
            self.warning.setText('You cannot enter empty values')
            self.warning.exec_()
        elif float(self.lower) >= float(self.higher):
            self.warning.setWindowTitle('Limit error')
            self.warning.setText('X min cannot be higher than X max or equal to it, if x min is higher, the x values will be swapped')
            self.warning.exec_()
        else: 
            pass
    
    # A function for converting the string entered by the user to a function of x    
    def string2func(self,string):
    # find all words and check if all are allowed:
        for word in re.findall('[a-zA-Z_]+', string):
            if word not in allowed_words:
                raise ValueError(
                    f"'{word}' is forbidden to use in math expression.\nOnly functions of 'x' are allowed.\nList of allowed words: {', '.join(allowed_words)}"
                )

        for old, new in replacements.items():
            string = string.replace(old, new)

        # to deal with constant functions e.g., y = 1
        if "x" not in string:
            string = f"{string}+0*x"

        def func(x):
            return eval(string)

        return func
    
    # Plotting the function of x on the graph
    def plotting(self):
        self.inputValidation()
        self.lower=int(self.lower)
        self.higher=int(self.higher)
        self.xPoints = np.linspace(self.lower, self.higher)
        equation = str(self.functionTextEdit.text())
        try:
            y = self.string2func(equation)(self.xPoints)
        except ValueError as e:
            self.warning.setWindowTitle("Function Error!")
            self.warning.setText(str(e))
            self.warning.exec_()
        self.axes.clear()
        self.axes.plot(self.xPoints, y)
        self.view.draw()
        self.view.show()
        
        

app = QApplication(sys.argv)
w = MainWindow()
app.exec_()