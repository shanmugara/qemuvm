class Vm(object):
    def __init__(self):
        self.name = ""
        self.nics = []
        self.memory = 0
        self.cpus = 0
        self.ostype = ""
        self.diskbus = ""
        self.nicbus = ""
        self.disk = ""


class Nic(object):
    def __init__(self):
        self.bridge = ""
        self.type = "e1000e"
        self.mac = ""