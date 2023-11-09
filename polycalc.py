from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_context('poster')

from polynomial import Polynomial as P

class PolyCalc(QMainWindow):

    super_scr = {1:'\u00b1'  }
    
    def __init__(self):
        
        '''Build new GUI window'''
        
        super().__init__()
        self.setFixedSize(QSize(800, 400))
        self.setWindowTitle('PolyCalc')
        self.initUI()


    def initUI(self):
        
        
        # Setup master layout    
        self.master_layout  = QGridLayout(self)

        # Nest layouts
        self.menu_layout    = QHBoxLayout(self)
        self.message_layout = QVBoxLayout(self)
        self.input_layout   = QVBoxLayout(self)

        self.master_layout.addLayout(self.menu_layout, 0, 0, 1, 5)
        self.master_layout.addLayout(self.message_layout, 1, 0, 4, 2)
        self.master_layout.addLayout(self.input_layout, 1, 2, 4, 3)

        # Add textboxes and buttons
        self.create_textboxes()
        self.setup_dropdown_menu()
        self.result_button = QPushButton('Get_result')
        self.add_to_input_layout(self.result_button)      

        # Set connections
        self.set_connections()
        self.set_default_states()
        self.init_operators()
        
        # Add everything to window to be displayed
        self.widget = QWidget(self)
        self.widget.setLayout(self.master_layout)
        self.setCentralWidget(self.widget)


    def set_connections(self):
        
        # Setup QT connections for textbox and combo box
        self.p1_textbox.returnPressed.connect(self.parsetext_p1)
        self.p1_textbox.textChanged.connect(self.check_when_typing_p1)

        self.p2_textbox.returnPressed.connect(self.parsetext_p2)
        self.p2_textbox.textChanged.connect(self.check_when_typing_p2)

        self.combo_box.currentIndexChanged.connect(self.combo_box_update)
        self.result_button.clicked.connect(self.get_result)
        
        self.exit = QAction("Exit Application",shortcut=QKeySequence("Ctrl+q"),triggered=lambda:self.exit_app)
        self.addAction(self.exit)
        
        
        
    def set_default_states(self):
    
        # Set up default states for labels and textboxes
        self.p1_label.setText("Enter coefficients of polynomial I  : ")
        self.p2_label.setText("Enter coefficients of polynomial II : ")

        self.p1_textbox.clear()
        self.p2_textbox.clear()
        
    def create_textboxes(self):

        # Build text boxes for the GUI
        
        for i in range(2):
        
            textbox       = QLineEdit(self)
            label         = QLabel(self)

            label.resize(100,10)
        
            #self.p1_textbox.setFixedWidth(40)
            textbox.setAlignment(Qt.AlignRight)
            textbox.setLayout(self.input_layout)

            textbox.setMaxLength(24)
            
            self.add_to_input_layout(textbox)
            self.add_to_message_layout(label)

            if i == 0:
                self.p1_textbox, self.p1_label = textbox, label       
            else:
                self.p2_textbox, self.p2_label = textbox, label       
                               
        self.p2_textbox.setEnabled(False)
        self.result_label = QLabel(self)
        self.result_label.resize(100,10)
        self.result_label.setText('Result')
        self.add_to_message_layout(self.result_label)

    def setup_dropdown_menu(self):

        # Add the combo box to the GUI
        
        self.combo_label = QLabel(self)
        self.combo_label.setText('What would you like to do ?')
        
        self.combo_box = QComboBox(self)
        self.combo_box.addItem('Pick an option')
        self.combo_box.addItem('Add polynomials')
        self.combo_box.addItem('Subtract polynomials')
        self.combo_box.addItem('Multiply polynomials')
        self.combo_box.addItem('Compose polynomials')
        self.combo_box.addItem('Derivative of a polynomial')
        self.combo_box.addItem('Plot polynomial')

        self.add_to_menu_layout(self.combo_label)
        self.add_to_menu_layout(self.combo_box)

        

    # Add layouts to widgets
    def add_to_input_layout(self, w):
        self.input_layout.addWidget(w)
        
    def add_to_message_layout(self, w):
        self.message_layout.addWidget(w)

    def add_to_menu_layout(self, w):
        self.menu_layout.addWidget(w)

    def combo_box_update(self):
        
        # Code up actions that need to happen when combo box is updated
        
        if self.combo_box.currentIndex() == 0:
          
            self.p2_textbox.setEnabled(False)
            
        elif self.combo_box.currentIndex() == 5:
            
            self.p2_textbox.setEnabled(True)
            self.p1_label.setText("Enter coefficients of polynomial I  : ")
            self.p2_label.setText("Enter order of derivative           : ")
            self.p2_textbox.setText('1')
            
        elif self.combo_box.currentIndex() == 6:
            
            self.p2_textbox.setEnabled(False)
            
        else:
            
            self.p2_textbox.setEnabled(True)
            self.p1_label.setText("Enter coefficients of polynomial I  : ")
            self.p2_label.setText("Enter coefficients of polynomial II : ")

    def init_operators(self):
        
        # Initialize some function objects to carry out polynomial operations
        
        self.add  = lambda p1, p2: p1+p2
        self.sub  = lambda p1, p2: p1-p2
        self.mul  = lambda p1, p2: p1*p2
        self.comp = lambda p1, p2: p1|p2

        self.operators = {1:self.add, 2:self.sub, 3:self.mul, 4: self.comp}
    
    def get_str_coeffs(self, text):
        
        # Convert text into a list of coefficients

        str_coeffs = text.split(' ')
        coeffs     = []

        for c in str_coeffs:
            if c == '':
                continue
            
            number = c[1] if c[0] == '+' else c
            coeffs.append(number)

        return coeffs

    def get_coeffs(self, text):
        
        # Turn text into a list of integer coefficients

        str_coeffs = self.get_str_coeffs(text)
        return [int(c) for c in str_coeffs]
        


    
    def get_parsed_polynomial(self, raw):
        
        # Prase the text entered by the user
        coeffs     = self.strip_zeros(self.get_str_coeffs(raw))
        degree     = len(coeffs) - 1
        eqn        = ''
        
        for i in range(len(coeffs)):

            c   = coeffs[i]
            alg = 'x^'+str(degree-i) if (degree-i > 0) else ''
            eqn = eqn + ' +'+c+alg if c[0] != '-' else eqn + ' '+c+alg
            
        return eqn[2:] if eqn[0:2]==' +' else eqn
        

    
    def check_text(self, text, valid = ' +-0123456789'):
       
        # Check text for unnecessary characters
        for l in text:
            if l not in valid:
                return False
        return True


    def check_when_typing(self, textbox):

        # Check text as user types
        text = textbox.text()
        
        if not self.check_text(text):
            self.raise_alert('Enter only numbers and spaces')
            textbox.backspace()
                
    
    def raise_alert(self, text):
        
        # Setup an alerts dialog box

        dlg = QMessageBox(self)
        dlg.setText(text)
        button = dlg.exec()


    #A few lambda methods to setup connections
    
    parsetext_p1 = lambda self: self.parsetext(self.p1_textbox, self.p1_label)
    parsetext_p2 = lambda self: self.parsetext(self.p2_textbox, self.p2_label)

    check_when_typing_p1 = lambda self: self.check_when_typing(self.p1_textbox)
    check_when_typing_p2 = lambda self: self.check_when_typing(self.p2_textbox)

    def make_plot(self, p):

        # Code to make plot of a polynomial        

        x = np.linspace(-10, 10, 1001)
        f = [p.at(i) for i in x]
        
        fig, ax = plt.subplots(figsize = (7,5))
        ax.plot(x, f)
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        plt.tight_layout()
        plt.show(block=False)

        
    def strip_zeros(self, c):

        for i, el in enumerate(c):
            if el != '0':
                break
        
        if i == 0:
            return c.copy()
        elif i == len(c) - 1:
            return [c[-1]]
        else:
            return c[i:]
            
    def parsetext(self, txt, label):
        
        # Parse text found in the textboxes

        inp    = txt.text()

        if self.check_text(inp):
            text   = self.get_parsed_polynomial(inp)
            label.setText("You entered: " + text)
        else:
            self.raise_alert('Input can contain only numbers and spaces')
            label.clear()
            

            
    def get_result(self):
        
        # What should happen when the get result button in pressed

        # Get index of combo box
        index = self.combo_box.currentIndex()

        if index > 0 and index < 5:
            
            # Binary operations
            
            c1 = self.get_coeffs(self.p1_textbox.text())
            c2 = self.get_coeffs(self.p2_textbox.text())

            print(c1, c2)
            print(P(c1), P(c2))
            
            if c1 == [] or c2 == []:
                self.raise_alert('Enter valid coefficients for two  polynomials in the textboxes')
            else:
                r = self.operators[index](P(c1), P(c2))
                self.parsetext_p1()
                self.parsetext_p2()
                self.result_label.setText('Result: '+r.__str__())

        elif index==5:
            
            # Derivative operation
            
            c1 = self.get_coeffs(self.p1_textbox.text())
            self.parsetext_p1()

            if self.check_text(self.p2_textbox.text(), '0123456789'):
                order = int(self.p2_textbox.text())
            else:
                self.raise_alert('Input can only contain numbers - setting order to 1')
                self.p2_textbox.setText('1')
                order = 1
                
            r  = P(c1).derivative(order)
            self.result_label.setText('Result: '+r.__str__())

        elif index==6:
            
            # Plot operation
            
            c1 = self.get_coeffs(self.p1_textbox.text())

            if c1 == []:
                self.raise_alert('Enter valid coefficients for a  polynomial in the first textbox')
            else:
                self.parsetext_p1()
                self.make_plot(P(c1))
        
    def exit_app(self):
        
        # Wxit the app

        self.close()


if __name__=='__main__':
    
    app    = QApplication(sys.argv)
    window = PolyCalc()
    window.show()
    sys.exit(app.exec_())
 
