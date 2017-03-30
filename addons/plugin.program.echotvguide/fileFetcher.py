# -*- coding: utf-8 -*-
#
# FTV Guide
# Copyright (C) 2015 Thomas Geppert [bluezed]
# bluezed.apps@gmail.com
#
# This Program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
import xbmc
import xbmcvfs
import os
import urllib2
import datetime
import time
import zlib

# downloader
import xbmcgui
import urllib
import time
import sys

import base64
MAIN_URL = base64.b64decode(b'aHR0cDovL3d3dy50ZGJyZXBvLmNvbS9ndWlkZS8=')#me
#MAIN_URL = 'http://thaisatellite.tv/ftv/'#ftv

#import xbmcaddon
#AddonID     =  'plugin.program.echotvguide'
#ADDON       =  xbmcaddon.Addon(id=AddonID)
#MAIN_URL    =  ADDON.getSetting('builtin.url')

class FileFetcher(object):
    INTERVAL_ALWAYS = 0
    INTERVAL_12 = 1
    INTERVAL_24 = 2
    INTERVAL_48 = 3

    FETCH_ERROR = -1
    FETCH_NOT_NEEDED = 0
    FETCH_OK = 1

    TYPE_DEFAULT = 1
    TYPE_REMOTE = 2
    basePath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'plugin.program.echotvguide'))
    filePath = ''
    fileUrl = ''
    addon = None
    fileType = TYPE_DEFAULT

    def __init__(self, fileName, addon):
        self.addon = addon

        if fileName.startswith("http://") or fileName.startswith("sftp://") or fileName.startswith("ftp://") or \
                fileName.startswith("https://") or fileName.startswith("ftps://") or fileName.startswith("smb://") or \
                fileName.startswith("nfs://"):
            self.fileType = self.TYPE_REMOTE
            self.fileUrl = fileName
            self.filePath = os.path.join(self.basePath, fileName.split('/')[-1])
        else:
            self.fileType = self.TYPE_DEFAULT
            self.filePath = os.path.join(self.basePath, fileName)
            self.fileUrl = MAIN_URL + fileName             

        # make sure the folder is actually there already!
        if not os.path.exists(self.basePath):
            os.makedirs(self.basePath)

    def fetchFile(self):
        time.sleep(0.5)
        retVal = self.FETCH_NOT_NEEDED
        fetch = False
        if not os.path.exists(self.filePath):  # always fetch if file doesn't exist!
            fetch = True
        else:
            interval = int(self.addon.getSetting('xmltv.interval'))
            if interval != self.INTERVAL_ALWAYS:
                modTime = datetime.datetime.fromtimestamp(os.path.getmtime(self.filePath))
                td = datetime.datetime.now() - modTime
                # need to do it this way cause Android doesn't support .total_seconds() :(
                diff = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6) / 10 ** 6
                #if ((interval == self.INTERVAL_12 and diff >= 43200) or
                # 12 hours is actually 7 days
                #if ((interval == self.INTERVAL_12 and diff >= 604800) or     
                # 12 hours is actually 4 days
                if ((interval == self.INTERVAL_12 and diff >= 345600) or      
                        (interval == self.INTERVAL_24 and diff >= 86400) or
                        (interval == self.INTERVAL_48 and diff >= 172800)):
                    fetch = True
            else:
                fetch = True

        if fetch:
            tmpFile = os.path.join(self.basePath, 'tmp')
            if self.fileType == self.TYPE_REMOTE:
                xbmc.log('[plugin.program.echotvguide] file is in remote location: %s' % self.fileUrl, xbmc.LOGDEBUG)
                if not xbmcvfs.copy(self.fileUrl, tmpFile):
                    xbmc.log('[plugin.program.echotvguide] Remote file couldn\'t be copied: %s' % self.fileUrl, xbmc.LOGERROR)                 
            else:
                # Builtin               
                f = open(tmpFile, 'wb')
                xbmc.log('[plugin.program.echotvguide] file is on the internet: %s' % self.fileUrl, xbmc.LOGDEBUG)
                tmpData = urllib2.urlopen(self.fileUrl)     
                data = tmpData.read()
                if tmpData.info().get('content-encoding') == 'gzip':
                    data = zlib.decompress(data, zlib.MAX_WBITS + 16)
                f.write(data)
                f.close()

            if os.path.getsize(tmpFile) > 0:
                if os.path.exists(self.filePath):
                    os.remove(self.filePath)
                os.rename(tmpFile, self.filePath)
                retVal = self.FETCH_OK
                xbmc.log('[plugin.program.echotvguide] file %s was downloaded' % self.filePath, xbmc.LOGDEBUG)          
                #Custom  
                #tmpFile = os.path.join(self.basePath, 'guides.zip')  
                self.fileUrl2 = MAIN_URL + 'guide.zip'  
                #tmpFile = xbmc.translatePath(os.path.join('special://home', 'cache', 'guide.zip')) 
                tmpFile = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'plugin.program.echotvguide', 'guide.zip'))                
                tmpData = downloader(self.fileUrl2,tmpFile)         
                try:
                    import zipfile                  
                    zin = zipfile.ZipFile(tmpFile, 'r')
                    zin.extractall(self.basePath)
                    #from addpass import *
                    import add;add.StartCreate()
                except: pass            
            else:
                retVal = self.FETCH_ERROR 
            #import add;add.StartCreate()
        return retVal
        

def downloader(url, dest, dp = None):
    #import xbmcgui
    #import urllib
    #import time
    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create("EPG","Downloading & Installing Files", ' ', ' ')
    dp.update(0)
    start_time=time.time()
    urllib.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time))   
#     
def _pbhook(numblocks, blocksize, filesize, dp, start_time):
        try: 
            percent = min(numblocks * blocksize * 100 / filesize, 100) 
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: 
                eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: 
                eta = 0 
            kbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total) 
            e = 'Speed: %.02f Kb/s ' % kbps_speed 
            e += 'ETA: %02d:%02d' % divmod(eta, 60) 
            dp.update(percent, mbs, e)
        except: 
            percent = 100 
            dp.update(percent) 
        if dp.iscanceled(): 
            dp.close() 
