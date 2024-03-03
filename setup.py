from setuptools import setup
import os
import sys

sys.path.insert(0, "src")

req_lst = ['xmltodict']
if os.name == 'nt':
    req_lst.append('colorama')

setup(name='azuregraph',
      version="0.0.1",
      description='QEMU Utils.',
      url='https://none.none',
      author='RP',
      author_email='psraj@outlook.com',
      license='GPL',
      install_requires=req_lst,
      package_dir={"": "src"},
      packages=['qemu', 'qemu.helpers'],
      entry_points={
          'console_scripts':
              ['qemuutil = qemu.main:main'],
      },
      include_package_data=True,
      zip_safe=False,
      )