# coding: utf-8
"""
"""
__author__ = "Nikola Klaric (nikola@klaric.org)"
__copyright__ = "Copyright (c) 2014 Nikola Klaric"

import sys
from cStringIO import StringIO
from ftplib import FTP
from zipfile import ZipFile

import pefile

MADVR_ZIP_PATH = r'C:\Users\Default\Downloads\madVR.zip'
FTP_SERVER = 'ftp.example.com'
FTP_USERNAME = 'bob'
FTP_PASSWORD = '$ecret'
FTP_VERSION_DIR = '/home/bob/version'

if __name__ == '__main__':
    with ZipFile(MADVR_ZIP_PATH) as madVrZipFile:
        madVrVersion = pefile.PE(data=madVrZipFile.open('madVR.ax').read()).FileInfo[0].StringTable[0].entries['ProductVersion']

    sys.stdout.write('Version: %s\n' % madVrVersion)

    ftp = FTP(FTP_SERVER)
    try:
        ftp.login(FTP_USERNAME, FTP_PASSWORD)
        ftp.cwd(FTP_VERSION_DIR)

        ftp.storbinary('STOR version.txt',  StringIO(madVrVersion))
    finally:
        ftp.close()
