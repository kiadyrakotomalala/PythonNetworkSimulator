from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Simulator import SimulatorWindow
from Details import DeviceTree

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.dockList = []
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createDockWindows()
        self.setWindowTitle("New Simulator")
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.resize(1000,800)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        
    def createActions(self):
        self.newComputer = QtGui.QAction(QtGui.QIcon('Image/computer.jpg'),
                "&Add computer", self, shortcut='Ctrl + Alt + C',
                statusTip="Add computer",
                triggered=self.addComputer)

        self.newRouter = QtGui.QAction(QtGui.QIcon('Image/router.jpg'),
                "&Add router", self, shortcut='Ctrl + Alt + R',
                statusTip="Add router",
                triggered=self.addRouter)

        self.new = QtGui.QAction(QtGui.QIcon('Image/new.jpg'),
                "&New", self, shortcut='Ctrl + N',
                statusTip="New",
                triggered=self.newSimulator)

        self.open = QtGui.QAction(QtGui.QIcon('Image/open.jpg'),
                "&Open", self, shortcut='Ctrl + O',
                statusTip="Open",
                triggered=self.openSimulator)

        self.save = QtGui.QAction(QtGui.QIcon('Image/save.jpg'),
                "&Save", self, shortcut='CTRL + S',
                statusTip="Save",
                triggered=self.saveSimulator)

        self.saveas = QtGui.QAction(QtGui.QIcon('Image/save as.jpg'),
                "&Saveas", self, shortcut='CTRl +ALT + S',
                statusTip="Save",
                triggered=self.saveasSimulator)

        self.quit = QtGui.QAction(QtGui.QIcon('Image/quit.png'),
                "&Quit", self, shortcut='CTRL + X',
                statusTip="Quit",
                triggered=self.quitSimulator)

    def createMenus(self):
        self.fileMenu1 = self.menuBar().addMenu("&File")
        self.fileMenu1.addAction(self.new)
        self.fileMenu1.addAction(self.open)
        self.fileMenu1.addAction(self.save)
        self.fileMenu1.addAction(self.saveas)
        self.fileMenu1.addAction(self.quit)
        
        self.fileMenu = self.menuBar().addMenu("&New")
        self.fileMenu.addAction(self.newComputer)
        self.fileMenu.addAction(self.newRouter)
        self.fileMenu.addSeparator()
        self.fileMenu2 = self.menuBar().addMenu("&Vue")

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("New")
        self.fileToolBar.addAction(self.newComputer)
        self.fileToolBar.addAction(self.newRouter)        
        self.fileToolBar.addSeparator()
                
    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createDockWindows(self):
        dock = QtGui.QDockWidget("Simulator Window", self)
        dock.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.simulator = SimulatorWindow('New Simulator')
        dock.setWidget( self.simulator)
        self.dockList.append(dock)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
        action = dock.toggleViewAction()
        action.setIcon(QtGui.QIcon('Image/simulator.jpg'))
        self.fileMenu2.addAction(action)
        self.fileToolBar.addAction(action)

        dock = QtGui.QDockWidget("Details Window", self)
        dock.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.detailsWindow = DeviceTree(self.simulator)
        dock.setWidget( self.detailsWindow)
        self.simulator.detailsWindow = self.detailsWindow
        self.dockList.append(dock)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
        action = dock.toggleViewAction()
        action.setIcon(QtGui.QIcon('Image/simulator.jpg'))
        self.fileMenu2.addAction(action)
        self.fileToolBar.addAction(action)

            
    def addComputer(self):
        name, ok =QInputDialog().getText(self, 'Add new computer', 'Computer name:')
        if ok:
            self.simulator.addComputer(name)

    def addRouter(self):
        name, ok =QInputDialog().getText(self, 'Add new router', 'Router name:')
        if ok:
            self.simulator.addRouter(name)
    
    def newSimulator(self):
        self.createDockWindows()
        
    def openSimulator(self):
        loadFile = QFileDialog().getExistingDirectory(parent=self, caption='Open existing project')
        self.simulator.load(str(loadFile))

    def saveSimulator(self):
        try:
            self.simulator.save(str(self.saveFile))
        except:    
            self.saveFile = QFileDialog().getExistingDirectory(parent=self, caption='Save project')
            self.simulator.save(str(self.saveFile))
            
    def saveasSimulator(self):
        self.saveFile = QFileDialog().getExistingDirectory(parent=self, caption='Save project')
        self.simulator.save(str(self.saveFile))
    
    def quitSimulator(self):
        try:
            self.saveFile
            sys.exit()
        except:
            QMessageBox.critical(self, "Not saved project", "Please save your project")

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("mac"))
    QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())