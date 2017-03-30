#import argparse
import sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,urllib2,re
import shutil
import time

addon         = 'plugin.program.echotvguide'
ADDONID       = addon
addon_name    = addon
icon = xbmc.translatePath(os.path.join('special://home/addons', addon, 'icon.png'))
addonPath = xbmc.translatePath(os.path.join('special://home', 'addons', addon))
basePath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', addon))
dbPath = xbmc.translatePath(xbmcaddon.Addon(addon).getAddonInfo('profile'))
dialog = xbmcgui.Dialog();dp = xbmcgui.DialogProgress()

import base64
xmlURL = base64.b64decode(b'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2hhbGlrdXMvX0FuZHlSZXBvL21hc3Rlci9fdHh0Lw==') # blah blah _AndyRepo/master/_txt/  

advancedsettings1 = 'advancedsettings.xml'
advancedsettings2 = 'advancedsettings_0_cache.xml'
advancedsettings3 = 'advancedsettings_1Gig_Mem.xml'
advancedsettings4 = 'advancedsettings_2Gig_Mem.xml'
advancedsettings5 = 'advancedsettings_4Gig_Mem.xml'
advancedsettings6 = 'advancedsettings_8Gig_Mem.xml'
advancedsettings7 = 'advancedsettings.xml'

mode='run_advancedsettings_Menu'

def advancedsettings_Menu():
        choice = dialog.select('Choose advancedsettings.xml to Download', ['Close',
                                                           advancedsettings1,
                                                           advancedsettings2,
                                                           advancedsettings3,
                                                           advancedsettings4,
                                                           advancedsettings5,
                                                           advancedsettings6,
                                                           advancedsettings7])
        if choice == 0: sys.exit(0)
        if choice == 1:
            advancedsettingsDL(advancedsettings1)
        if choice == 2:
            advancedsettingsDL(advancedsettings2)
        if choice == 3:
            advancedsettingsDL(advancedsettings3)
        if choice == 4:
            advancedsettingsDL(advancedsettings4)
        if choice == 5:
            advancedsettingsDL(advancedsettings5)
        if choice == 6:
            advancedsettingsDL(advancedsettings6)
        if choice == 7:
            advancedsettingsDL(advancedsettings7)


def advancedsettingsDL(advancedsettingsfile):
    asFile = xmlURL + advancedsettingsfile
    asDest = xbmc.translatePath(os.path.join('special://home','userdata','advancedsettings.xml'))


    tmpData = downloader(asFile,asDest)
    notify('advancedsettings.xml', 'advancedsettings.xml Installed.',os.path.join('special://home/addons', addon, 'icon.png'))##NOTIFY##  
    sys.exit() 










def downloader(url, dest, dp = None):
    import xbmcgui
    import urllib
    import time

    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create("advancedsettings.xml","Downloading & Installing advancedsettings.xml", ' ', ' ')
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
#
def notify(header,msg,icon_path):
    duration=1500
    #xbmc.executebuiltin("XBMC.Notification(%s,%s, %s, %s)" % (header, msg, duration, icon_path))
    xbmcgui.Dialog().notification(header, msg, icon=icon_path, time=duration, sound=False)
#




'''
import time
import os
import xbmc
import xbmcgui
import xbmcaddon

Source_advancedsettings = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.program.echotvguide', 'resources', 'advancedsettings', 'advancedsettings.xml'))
#basePath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'plugin.program.echotvguide'))
profilePath = xbmc.translatePath(os.path.join('special://home', 'userdata'))
DestFile = os.path.join(profilePath, 'advancedsettings.xml')

if not os.path.exists(DestFile): 
    from shutil import copyfile;copyfile(Source_advancedsettings, DestFile)
    
    if os.path.exists(DestFile):   
          d = xbmcgui.Dialog()
          d.ok('TV Guide', 'Copy successfully completed.', 'It will be used next time you start Kodi')  
'''    
    



if mode=='run_advancedsettings_Menu' : advancedsettings_Menu()
