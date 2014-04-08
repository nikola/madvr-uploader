# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2014 Nikola Klaric"

import os
import sys
from cStringIO import StringIO
from ftplib import FTP
from zipfile import ZipFile, ZIP_DEFLATED

import pefile


FTP_SERVER = 'ftp.example.com'
FTP_USERNAME = 'bob'
FTP_PASSWORD = '$ecret'
FTP_ZIP_DIR = '/home/bob/zip'
FTP_VERSION_DIR = '/home/bob/version'

MADVR_FILE_ROOT = r'C:\Users\Default\Downloads\madVR'
MADVR_FILES = [
    'activate debug mode.bat',
    'avcodec-mvr-53.dll',
    'avutil-mvr-51.dll',
    'changelog.txt',
    'dbghelp.dll',
    'install.bat',
    'InstallFilter.exe',
    'license.txt',
    'madHcCtrl.exe',
    'madHcNet32.dll',
    'madHcNet64.dll',
    'madLevelsTweaker.exe',
    'madTPG.exe',
    'madVR [debug].ax',
    'madVR.ax',
    'mvrSettings.dll',
    'readme.txt',
    'restore default settings.bat',
    'uninstall.bat',
    'unrar.dll',
    'developers/calibration demo/Delphi/SimpleDemo.dpr',
    'developers/calibration demo/Delphi/SimpleDemo.res',
    'developers/calibration demo/MSVC++/SimpleDemo.cpp',
    'developers/calibration demo/MSVC++/SimpleDemo.sln',
    'developers/calibration demo/MSVC++/SimpleDemo.vcproj',
    'developers/interfaces/madTPG.cpp',
    'developers/interfaces/madTPG.h',
    'developers/interfaces/madTPG.pas',
    'developers/interfaces/mvrInterfaces.h',
    'developers/interfaces/mvrInterfaces.pas',
    'developers/interfaces/SubRenderIntf.h',
    'developers/net-protocol.txt',
    'legal stuff/ffmpeg/compiling.txt',
    'legal stuff/ffmpeg/COPYING.LGPLv2.1',
    'legal stuff/ffmpeg/LICENSE',
    'legal stuff/ffmpeg/MAINTAINERS',
    'legal stuff/ffmpeg/mem.c',
    'legal stuff/ffmpeg/README',
    'legal stuff/nnedi3ocl/COPYING.LGPLv3',
    'legal stuff/nnedi3ocl/nnedi3ocl.cl',
]


if __name__ == '__main__':
    # Unbuffered console output.
    sys.stdout = os.fdopen(sys.stdout.fileno(), "w", 0)

    sys.stdout.write('Adding files to ZIP archive ...')
    madVrZip = StringIO()
    with ZipFile(madVrZip, 'w', ZIP_DEFLATED) as madVrZipFile:
        for arcname in MADVR_FILES:
            madVrZipFile.write(os.path.join(MADVR_FILE_ROOT, arcname), arcname)
    madVrZip.seek(0)
    sys.stdout.write(' done.\n')

    madVrVersion = pefile.PE(os.path.join(MADVR_FILE_ROOT, 'madVR.ax')).FileInfo[0].StringTable[0].entries['ProductVersion']
    sys.stdout.write('Product version: %s\n' % madVrVersion)

    ftp = FTP(FTP_SERVER)
    try:
        sys.stdout.write('Connecting to %s ...' % FTP_SERVER)
        ftp.login(FTP_USERNAME, FTP_PASSWORD)
        sys.stdout.write(' OK!\n')

        sys.stdout.write('Storing madVR.zip in %s ...' % FTP_ZIP_DIR)
        ftp.cwd(FTP_ZIP_DIR)
        ftp.storbinary('STOR madVR.zip', madVrZip)
        sys.stdout.write(' done.\n')

        sys.stdout.write('Storing version.txt in %s ...' % FTP_VERSION_DIR)
        ftp.cwd(FTP_VERSION_DIR)
        ftp.storbinary('STOR version.txt',  StringIO(madVrVersion))
        sys.stdout.write(' done.\n')
    finally:
        ftp.close()

    sys.stdout.write('No errors.')
