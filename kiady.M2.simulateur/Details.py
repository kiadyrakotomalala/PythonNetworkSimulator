from PyQt4.QtGui import *
from PyQt4.QtCore import *

class SortFilterProxyModel(QSortFilterProxyModel):
    def filterAcceptsRow(self, sourceRow, sourceParent):
        return super(SortFilterProxyModel, self).filterAcceptsRow(sourceRow, sourceParent)

class DeviceTree(QWidget):
    def __init__(self, simulator):
        self.simulator = simulator
        super(DeviceTree, self).__init__()
        self.proxyModelUser = SortFilterProxyModel()
        self.proxyModelUser.setDynamicSortFilter(True)
    
        self.proxyViewUser = QTreeView()
        self.proxyViewUser.setAlternatingRowColors(True)
        self.proxyViewUser.setModel(self.proxyModelUser)
        self.proxyViewUser.setSortingEnabled(True)        
        self.proxyViewUser.setContextMenuPolicy(Qt.CustomContextMenu)

#         self.proxyViewUser.connect(self.proxyViewUser,SIGNAL("customContextMenuRequested(QPoint)"),
#     self,SLOT("contextMenuRequested(QPoint)"))
#        
#         self.connect(self.proxyViewUser, SIGNAL("clicked()"),self,SLOT("deselect()"))
        proxyUserLayout = QGridLayout()
        proxyUserLayout.addWidget(self.proxyViewUser, 0, 0, 1, 3)
        
        self.setLayout(proxyUserLayout)
        
        self.setWindowTitle("Device")
        self.resize(350, 350)
        
        self.proxyViewUser.sortByColumn(1, Qt.AscendingOrder)
        self.setSourceUserModel(self.createUserModel(self))        
        self.proxyViewUser.clicked.connect(self.currentUserIndex)
        self.proxyViewUser.resizeColumnToContents(0)
    
    def updateDetails(self):
        self.setSourceUserModel(self.createUserModel(self)) 
        
    def createUserModel(self,parent):
        model = QStandardItemModel(0, 1, parent)
        model.setHeaderData(0, Qt.Horizontal, "Device List")
        i=0
        for device in self.simulator.deviceList: 
            model.setItem(i,0, self.interface(device))
            i = i+1
        return model

    def interface(self,device):
        item = QStandardItem(device.deviceName)
        item.setEditable(False)
        if len(device.interfaceList) != 0:
            for interface in device.interfaceList:
                item.appendRows([self.ipAddress(interface)])
        for route in device.routageTable.iteritems():
            item.appendRows([QStandardItem("Route: {0} --> {1}".format(route[0], route[1]))])
        return item
    
    def ipAddress(self, interface):
        item = QStandardItem(interface.interfaceName)
        item.setEditable(False)
        item.appendRows([QStandardItem(str(interface.ip))])
        return item
        
    def setSourceUserModel(self, model):
        self.proxyModelUser.setSourceModel(model)

    def currentUserIndex(self):
        self.dataUser=  self.proxyViewUser.currentIndex().data()
