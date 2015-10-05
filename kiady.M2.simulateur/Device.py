from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui
from Interface import Interface
from netaddr import IPAddress, IPNetwork
import cPickle

class Device(QtGui.QLabel):
    def __init__(self, image, name, deviceType,  parent):
        super(Device, self).__init__("<html><table><tr><td><center><strong>{0}</strong></center></td></tr><tr><td><img src='Image/{1}'></td></tr></html>".format(name, image), parent)        
        self.deviceName = name
        self.parent = parent
        self.deviceType = deviceType
        self.setGeometry(10, 10, 90, 90)
        self.setContextMenuPolicy(Qt.CustomContextMenu);
        self.connect(self,SIGNAL("customContextMenuRequested(QPoint)"),self,SLOT("contextMenuRequested(QPoint)"))
        self.interfaceList = []
        self.routageTable = {}
        
    def mouseMoveEvent(self, e):
        if e.buttons() != QtCore.Qt.LeftButton:
            return
        self.parent.moved = self
        mimeData = QtCore.QMimeData()
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        dropAction = drag.start(QtCore.Qt.MoveAction)

    def mousePressEvent(self, e):      
        super(Device, self).mousePressEvent(e)

    @pyqtSlot(QPoint)
    def contextMenuRequested(self,point):
        menu     = QMenu()    
        action1 = menu.addAction("Add Interface")
        action2 = menu.addAction("Do a Ping")
        action3 = menu.addAction("Manage Routage Table")
        action4 = menu.addAction("Delete")
        
        self.connect(action1,SIGNAL("triggered()"),self,SLOT("addInterface()"))
        self.connect(action2,SIGNAL("triggered()"),self,SLOT("doAPing()"))
        self.connect(action3,SIGNAL("triggered()"),self,SLOT("manageRoutageTable()"))
        self.connect(action4,SIGNAL("triggered()"),self,SLOT("delete()"))

        menu.exec_(self.mapToGlobal(point))
    
    def addInterfaceImage(self, interface):
        self.drawInterface()
            
    def drawInterface(self):
        i = 0
        for interface in self.interfaceList:
            if i==0:
                interface.move(self.pos().x()-30, self.pos().y())
                interface.show()

            elif i==1:
                interface.move(self.pos().x()-30, self.pos().y()+50)
                interface.show()
            
            elif i==2:
                interface.move(self.pos().x()+90, self.pos().y())
                interface.show()

            elif i==3:
                interface.move(self.pos().x()+90, self.pos().y()+50)
                interface.show()

            i = i+1

    def addRoute(self, network, route):
        added = False
        for interface in self.interfaceList:
            if route in interface.network:
                self.routageTable[network] = route
                added = True    
        return added
    
    def save(self, path):
        cPickle.dump(self, file(path,'w'))
        
            
    @pyqtSlot()
    def addInterface(self):
        name, ok = QInputDialog().getText(self, 'Add Interface', 'Interface name:')
        if ok:
            interface = Interface('point.png',name, self.parent, self)
            self.interfaceList.append(interface)
            self.addInterfaceImage(interface)

        try:
            self.parent.detailsWindow.updateDetails()
        except Exception as e:
            pass

    @pyqtSlot()
    def doAPing(self):
        ip, ok = QInputDialog().getText(self, 'Ping', 'Ip Address:')
        if ok:
            if self.parent.Ping(self, IPAddress(str(ip))):
                
                QtGui.QMessageBox.information(self, "Ping", "Ping success to {0}".format(ip))
            else:    
                QtGui.QMessageBox.critical(self, "Ping", "Failed to ping {0}".format(ip))
 
    @pyqtSlot()
    def manageRoutageTable(self):
        ip, okIp = QInputDialog().getText(self, 'Add Route', 'Network:')
        if okIp:
            mask, okMask = QInputDialog().getText(self, 'Add Route', 'Gateway:')
            if okMask:
                network = IPNetwork(str(ip))
                route = IPAddress(str(mask))                            
                self.addRoute(network, route)

        try:
            self.parent.detailsWindow.updateDetails()
        except Exception as e:
            pass

                
    @pyqtSlot()
    def delete(self):
        self.parent.deviceList.remove(self)
        self.deleteLater()