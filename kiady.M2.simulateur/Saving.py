import pickle

class DeviceForSave():
    def __init__(self, device):
        self.deviceName = device.deviceName
        self.interfaceList = []
        for interface in device.interfaceList:    
            self.interfaceList.append(InterfaceForSave(interface))
        self.deviceType = device.deviceType
        self.routageTable = device.routageTable
        self.position = device.pos()

    def store(self, path):
        path = path+'/'+self.deviceName
        pickle.dump(self, file(str(path),'w'))

class InterfaceForSave():
    def __init__(self, interface):
        self.interfaceName = interface.interfaceName
        self.device = interface.device.deviceName
        try:
            self.ip = interface.ip
            self.network = interface.network
        except:
            pass   
        