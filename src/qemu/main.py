import argparse
import sys
import os

app_root = os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0, app_root)

from qemu.helpers import importvm


def main():
    parser = argparse.ArgumentParser(description="QEMU lib")

    sub_parser = parser.add_subparsers(dest="command")
    parse_import = sub_parser.add_parser("import", help="import and existing vm from xml")
    parse_import.add_argument("-f", "--xmlfile", help="soruce xml file to import", required=True, type=str)
    parse_import.add_argument("-d", "--diskimage", help="disk image to import", required=True, type=str)
    parse_import.add_argument("-o", "--osvariant", help="os variant of the vm", required=True, type=str)

    args = parser.parse_args()

    if args.command == "import":
        importer = importvm.Import(args.xmlfile, args.diskimage, args.osvariant)
        importer.startimport()
        importer.commmit()

if __name__ == "__main__":
    main()

