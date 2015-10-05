from PyQt4.QtGui import *
from PyQt4.QtCore import *
from NewLink import SelectDialog
from netaddr import IPAddress, IPNetwork

class Interface(QLabel):
    def __init__(self, image, name,  parent, device):
        super(Interface, self).__init__("<html><table><tr><td><center><strong>{0}</strong></center></td></tr><tr><td><img src='Image/{1}'></td></tr></html>".format(name, image), parent)        
        self.interfaceName = name
        self.parent = parent
        self.device = device
        self.setGeometry(10, 10, 30, 50)
        self.setContextMenuPolicy(Qt.CustomContextMenu);
        self.connect(self,SIGNAL("customContextMenuRequested(QPoint)"),self,SLOT("contextMenuRequested(QPoint)"))
        self.connectedWith = None
        self.ip = 'No ip address'
        self.network = ''
   
    def __repr__(self):
        return '{0}-{1}'.format(self.device.deviceName, self.interfaceName)
    
    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return
        self.parent.moved = self
        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        dropAction = drag.start(Qt.MoveAction)

    def mousePressEvent(self, e):      
        super(Interface, self).mousePressEvent(e)
    
    @pyqtSlot(QPoint)
    def contextMenuRequested(self,point):
        menu     = QMenu()    
        action1 = menu.addAction("Set Ip")
        action2 = menu.addAction("Link to")
        action3 = menu.addAction("Unlink")
        action4 = menu.addAction("Delete")
        
        self.connect(action1,SIGNAL("triggered()"),self,SLOT("setIp()"))
        self.connect(action2,SIGNAL("triggered()"),self,SLOT("linkTo()"))
        self.connect(action3,SIGNAL("triggered()"),self,SLOT("unlink()"))
        self.connect(action4,SIGNAL("triggered()"),self,SLOT("delete()"))
        menu.exec_(self.mapToGlobal(point))

    def connectWith(self, interface):
        if self.connectedWith== None:
            self.connectedWith = interface
            return True
        else:
            return False

    @pyqtSlot()
    def setIp(self):
        ip, okIp = QInputDialog().getText(self, 'Set Ip Address', 'Ip Address:')
        if okIp:
            mask, okMask = QInputDialog().getText(self, 'Set Ip Address', 'Netmask bits:')
            if okMask:
                try:
                    self.ip = IPAddress(str(ip))
                    self.network = IPNetwork('{0}/{1}'.format(str(ip), str(mask)))

                    try:
                        self.parent.detailsWindow.updateDetails()
                    except Exception as e:
                        pass

                except:
                    QMessageBox.critical(self, "Set Ip", "invalid Ip or Netmask bits")

    @pyqtSlot()
    def linkTo(self):
        SelectDialog(self, self.parent.getAllInterface(), parent = self.parent)
        
        
    @pyqtSlot()
    def unlink(self):
        if self.connectedWith != None:  
            self.parent.linkList.remove((self,self.connectedWith))
            self.connectedWith.connectedWith = None
            self.connectedWith = None
            self.parent.repaint()
        else:
            QMessageBox.critical(self, "Unlink Interface", "Impossible to unlink non-connected interface")
        
    @pyqtSlot()
    def delete(self):
        if self.connectedWith != None:
            QMessageBox.critical(self, "Delete Interface", "Impossible to delete connected interface")
        else:
            self.device.interfaceList.remove(self)
            self.deleteLater()
            self.device.drawInterface()
        