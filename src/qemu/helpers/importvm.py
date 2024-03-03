import json
import os.path

import xmltodict
from subprocess import check_output, DEVNULL, STDOUT

FileNotFound = Exception("File Not Found")
InvalidOSType = Exception("Invalid OS variant was passed")
CmdRunError = Exception("subprocess command execution failed")
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


class VMXmltodict(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.vmdict = xmltodict.parse(f.read())


class Import(object):
    def __init__(self, filename, diskimg, ostype):

        self.ostypes = ["centos7", "centos7.0", "ubuntubionic", "ubuntufocal", "win2k12r2", "win2k19", "win2k16"]

        for f in [filename, diskimg]:
            if not os.path.isfile(f):
                raise FileNotFound

        if ostype not in self.ostypes:
            print(f"invalid os type, msut be one of {self.ostypes}")
            raise InvalidOSType

        self.srcxml = filename
        self.disk = diskimg
        self.ostype = ostype

    def startimport(self):
        self.xd = VMXmltodict(self.srcxml)
        self.vm = Vm()
        self.vm.disk = self.disk
        self.vm.ostype = self.ostype
        self.vm.name = self.xd.vmdict['domain']['name']
        self.vm.cpus = self.xd.vmdict['domain']['vcpu']['#text']
        self.vm.memory = int(int(self.xd.vmdict['domain']['memory']['#text'])/1024)

        self.getnics()
        self.getbus()
        self.getnetworks()
        self.getgraphics()
        # create the virt-install command
        self.cmd = (f"sudo virt-install --name {self.vm.name} --ram {self.vm.memory} --vcpus {self.vm.cpus} "
                    f"--os-variant {self.vm.ostype} --disk {self.vm.disk},bus={self.vm.diskbus} {self.interfaces} "
                    f"{self.graphics} --import --noautoconsole")

    def getnics(self):
        if isinstance(self.xd.vmdict['domain']['devices']['interface'], list):
            for i in self.xd.vmdict['domain']['devices']['interface']:
                nic = Nic()
                nic.mac = i['mac']['@address']
                if i['model']['@type'] == 'virtio':
                    nic.type = 'virtio'

                nic.bridge = i['source']['@bridge']
                self.vm.nics.append(nic)
        else:
            nic = Nic()
            nic.mac = self.xd.vmdict['domain']['devices']['interface']['mac']['@address']
            if self.xd.vmdict['domain']['devices']['interface']['model']['@type'] == 'virtio':
                nic.type = 'virtio'
            nic.bridge = self.xd.vmdict['domain']['devices']['interface']['source']['@bridge']
            self.vm.nics.append(nic)

    def getbus(self):
        if isinstance(self.xd.vmdict['domain']['devices']['disk'], list):
            self.vm.diskbus = self.xd.vmdict['domain']['devices']['disk'][0]['target']['@bus']
        else:
            self.vm.diskbus = self.xd.vmdict['domain']['devices']['disk']['target']['@bus']

    def getnetworks(self):
        self.interfaces = ""
        for n in self.vm.nics:
            self.interfaces += f"--network bridge={n.bridge},model={n.type},mac={n.mac} "

    def getgraphics(self):
        if self.ostype.startswith("win"):
            self.graphics = "--graphics vnc,listen=127.0.0.1,keymap=en-us"
        else:
            self.graphics = "--graphics spice"

    def commmit(self):
        try:
            cmd_out = check_output([self.cmd], shell=True, stderr=DEVNULL).decode().strip()
            print(cmd_out)
        except Exception as e:
            print(f"error {e}")
            raise CmdRunError
