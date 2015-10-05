from PyQt4 import QtGui
from Complete.select import Select_Dialog

class SelectDialog(QtGui.QMainWindow,Select_Dialog):
    def __init__(self, interf, interfaceList,  parent=None):
        super(SelectDialog, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.interfaceList = interfaceList
        for interface in interfaceList:
            if interf != interface:
                self.comboBox.addItem(str(interface))
        self.interface1 = interf
        self.main()
        
    def accept(self):
        for interface in self.interfaceList:
            if str(interface) == self.comboBox.currentText():
                interface2= interface
        self.parent.addLink(self.interface1, interface2)
        self.setVisible(False)

        
    def reject(self):
        self.setVisible(False)
    
    def main(self):
        self.show()
 
if __name__=='__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    imageViewer = SelectDialog(['kiady', 'ravahatr'])
    imageViewer.main()
    app.exec_()