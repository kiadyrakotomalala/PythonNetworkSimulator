from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
from PyQt4 import QtCore, QtGui
from Device import Device
import os
from Saving import DeviceForSave, InterfaceForSave
import pickle
from Interface import Interface
import gc

class SimulatorWindow(QtGui.QWidget):
    def __init__(self, name):
        super(SimulatorWindow, self).__init__()
        self.simulatorName = name
        self.moved= None
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        self.initUI()
        self.deviceList = []
        self.linkList= []
        self.detailsWindow = ""
        
    def initUI(self):
        self.setAcceptDrops(True)
        self.setWindowTitle('Simulator Window')
        self.setGeometry(300, 300, 280, 150)

    def dragEnterEvent(self, e):      
        e.accept()

    def dropEvent(self, e):
        position = e.pos()        
        self.moved.move(position)
        try:
            self.moved.drawInterface()
        except:
            pass
        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()
        self.repaint()
    
    def addComputer(self, name):
        device = Device('computer.jpg', name, 'computer',  self)
        device.move(100, 65)
        device.show()
        self.deviceList.append(device)
        try:
            self.detailsWindow.updateDetails()
        except Exception as e:
            pass
        
    def addRouter(self, name):
        device = Device('router.jpg', name, 'router',  self)
        device.move(100, 65)
        device.show()
        self.deviceList.append(device)
        try:
            self.detailsWindow.updateDetails()
        except Exception as e:
            print e
            pass
    
    def getAllInterface(self):
        interfaceList = []
        for device in self.deviceList:
            for interface in device.interfaceList:
                interfaceList.append(interface)
        return interfaceList
    
    def addLink(self, interface1, interface2):
        if interface1.connectWith(interface2) and interface2.connectWith(interface2):
            self.linkList.append((interface1, interface2))
            self.repaint()
        
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        pen = QPen(QtCore.Qt.black, 3, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        for link in self.linkList:
            painter.drawLine(link[0].pos().x()+20,link[0].pos().y()+30,link[1].pos().x()+20,link[1].pos().y()+30)        
        painter.end()


       
    def addDeviceRoutageTable(self, device, network, gateway):
        device.addRoute(network, gateway)

    def GetDeviceByIp(self, ip):
        for device in self.deviceList:
            for interface in device.interfaceList:
                if interface.ip == ip:
                    return device

    def GetInterfaceByIp(self, ip):
        for device in self.deviceList:
            for interface in device.interfaceList:
                if interface.ip == ip:
                    return interface

    def Ping(self, device, ip):
        try:
            if self.GetInterfaceByIp(ip) == None:
                return False
        except:
            return False
        
        for interface in device.interfaceList:
            if not interface.connectedWith == None:
                if ip in interface.network and (interface.connectedWith.interfaceName == self.GetInterfaceByIp(ip).interfaceName or interface.ip == ip):
                    return True
            
        for route in device.routageTable.iteritems():
            if ip in route[0]:
                return self.Ping(self.GetDeviceByIp(route[1]), ip)

    def save(self, folder):
        try:
            os.makedirs('{0}/Device'.format(folder))
        except:
            pass
        path='{0}/Device'.format(folder)
        
        for device in self.deviceList:
            deviceSave = DeviceForSave(device)
            deviceSave.store(path)
        
        linkSave = []
        for link in self.linkList:
            linkSave.append((InterfaceForSave(link[0]), InterfaceForSave(link[1])))
        
        pickle.dump(linkSave, file(str(folder+'/Link'),'w'))

    def addLoadedDevice(self, deviceLoad):
        if deviceLoad.deviceType== 'router':
            device = Device('router.jpg', deviceLoad.deviceName, 'router',  self)
        else:
            device = Device('computer.jpg', deviceLoad.deviceName, 'computer',  self)
        device.move(deviceLoad.position)
        device.show()
        device.deviceType = deviceLoad.deviceType
        device.routageTable = deviceLoad.routageTable
        device.interfaceList = []
        for interfaceLoad in deviceLoad.interfaceList:
            interface = Interface('point.png',interfaceLoad.interfaceName, self, device)
            interface.ip = interfaceLoad.ip
            interface.network = interfaceLoad.network
            device.interfaceList.append(interface)
        device.drawInterface()
        self.deviceList.append(device)

        try:
            self.detailsWindow.updateDetails()
        except Exception as e:
            pass
    
    def getInterface(self, interface):
        for inst in gc.get_objects():
            if isinstance(inst, Interface):
                if inst.interfaceName == interface.interfaceName and inst.device.deviceName == interface.device:
                    return inst
    
    def loadAllLink(self, linkList):
        for link in linkList:
            self.addLink(self.getInterface(link[0]), self.getInterface(link[1]))
    
    def load(self, path):
        inDir = path+'/Device'
        liste = []
        
        for (dirpath, dirnames, fnames,) in os.walk(inDir):
            liste.extend([ os.path.join(inDir, fname) for fname in fnames ])
            break
        
        for l in liste:
            self.addLoadedDevice(pickle.load(file(l)))
        
        self.loadAllLink(pickle.load(file(path+'/Link')))
        
def main():
    app = QtGui.QApplication([])
    ex = SimulatorWindow()
    ex.show()    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()