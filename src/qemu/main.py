import argparse
import sys
import os

app_root = os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0, app_root)

from qemu.helpers import importvm, createvm


def main():
    parser = argparse.ArgumentParser(description="QEMU lib")

    sub_parser = parser.add_subparsers(dest="command")
    parse_import = sub_parser.add_parser("import", help="import and existing vm from xml")
    parse_import.add_argument("-f", "--xmlfile", help="soruce xml file to import", required=True, type=str)
    parse_import.add_argument("-d", "--diskimage", help="disk image to import", required=True, type=str)
    parse_import.add_argument("-o", "--osvariant", help="os variant of the vm", required=True, type=str)

    parse_create = sub_parser.add_parser("create", help="create a new vm from image")
    parse_create.add_argument("-n", "--vmname", help="vm name", required=True, type=str)
    parse_create.add_argument("-i", "--winmode", help="windows server mode core or gui", default="core", required=False)

    args = parser.parse_args()

    if args.command == "import":
        importer = importvm.Import(args.xmlfile, args.diskimage, args.osvariant)
        importer.startimport()
        importer.commmit()

    if args.command == "create":
        creater = createvm.Create(args.vmname, args.winmode)
        creater.commit()

if __name__ == "__main__":
    main()

