import os
import shutil

from subprocess import check_output, DEVNULL, STDOUT
from common_cls import Vm, Nic

class Create(object):
    def __init__(self,
                 vmname,
                 winmode="core",
                 cpus=2,
                 memory=4096,
                 winver="2022",
                 ostype="win2k19",
                 img_dir="/kvm/nas",
                 img_src="wind2k22-gui.qcow2",
                 diskbus="virtio"
                 ):
        self.vm = Vm()
        self.vm.name = vmname
        self.vm.cpus = cpus
        self.vm.memory = memory
        self.vm.ostype = ostype
        self.vm.diskbus = diskbus
        self.winmode = winmode
        self.winver = winver
        self.img_dir = img_dir
        self.src_img = os.path.join(self.img_dir, img_src)
        self.dst_img = os.path.join(self.img_dir, f"{self.vm.name}.qcpow2")

        if not os.path.isfile(self.src_img):
            raise FileNotFoundError(f"File:{self.src_img}")
    def setnetwork(self):
        nic = Nic()
        nic.type = "virtio"
        nic.bridge = "br0"
        self.vm.nics.append(nic)
    def setgraphics(self):
        self.graphics = self.graphics = "--graphics vnc,listen=127.0.0.1,keymap=en-us"

    def clone_img(self):
        try:
            shutil.copyfile(self.src_img, self.dst_img)
        except Exception as e:
            raise IOError

    def commit(self):
        self.setnetwork()
        self.setgraphics()
        self.clone_img()

        network = ""
        for n in self.vm.nics:
            network += f"--network bridge={n.bridge},model={n.type} "

        self.cmd = (f"virt-install --name {self.vm.name} --ram {self.vm.memory} --vcpus {self.vm.cpus} "
                    f"--os-variant {self.vm.ostype} --disk {self.dst_img},bus={self.vm.diskbus} "
                    f"{network} {self.graphics} --import --noautoconsole")

        try:
            cmd_out = check_output([self.cmd], shell=True, stderr=DEVNULL).decode().strip()
            print(cmd_out)
        except Exception as e:
            raise OSError

