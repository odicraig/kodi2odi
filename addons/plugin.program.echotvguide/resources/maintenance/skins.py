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
externaliniURL = base64.b64decode(b'aHR0cDovL3d3dy50ZGJyZXBvLmNvbS9ndWlkZS8=') # blah blah _AndyRepo/master/_epg/  
skinURL = externaliniURL + 'skins/'

skin1 = 'Default'
skin2 = 'SKY_Fanriffic'
skin3 = 'SKY_MartyMan'
skin4 = 'Silver_MartyMan'
skin5 = 'Red_MartyMan'
skin6 = 'FTV_Eminence'
skin7 = 'FTV_Touch'

mode='run_skinsDL_Menu'

def skinsDL_Menu():
    choice = dialog.select('Choose skin to Download', ['Close',
                                                       skin1,
                                                       skin2,
                                                       skin3,
                                                       skin4,
                                                       skin5])
#                                                           skin6,
#                                                           skin7])
    if choice == 0: sys.exit(0)
    if choice == 1:
        skinDL(skin1)
    if choice == 2:
        skinDL(skin2)
    if choice == 3:
        skinDL(skin3)
    if choice == 4:
        skinDL(skin4)
    if choice == 5:
        skinDL(skin5)
#        if choice == 6:
#            skinDL(skin6)
#        if choice == 7:
#            skinDL(skin7)

def skinDL(skinfile):
    # make sure the folder is actually there already!
    if not os.path.exists(basePath):
        os.makedirs(basePath)
    if not os.path.exists(os.path.join(basePath, 'resources')):
        os.makedirs(os.path.join(basePath, 'resources'))
    if not os.path.exists(os.path.join(basePath, 'resources', 'skins')):
        os.makedirs(os.path.join(basePath, 'resources', 'skins'))
 
    fileUrl = skinURL+skinfile+'.zip'  
    #tmpFile = xbmc.translatePath(os.path.join('special://home', 'addons', 'packages','skin.zip')) 
    tmpFile = xbmc.translatePath(os.path.join(basePath,'tmp'))
    tmpData = downloader(fileUrl,tmpFile)         
    import zipfile                  
    zin = zipfile.ZipFile(tmpFile, 'r')
    zin.extractall(os.path.join(basePath, 'resources', 'skins'))
    
    #
    #addon.setSetting('skin', skinfile)
    SetSetting('skin', skinfile)
    notify('Skins',skinfile + ' successfully Installed.',os.path.join('special://home/addons', addon, 'icon.png'))##NOTIFY##  
    sys.exit()  
#

def SetSetting(param, value):
    value = str(value)
    if GetSetting(param) == value:
        return
    xbmcaddon.Addon(ADDONID).setSetting(param, value)

def GetSetting(param):
    return xbmcaddon.Addon(ADDONID).getSetting(param)


def downloader(url, dest, dp = None):
    import xbmcgui
    import urllib
    import time

    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create("Skins","Downloading & Installing Skin", ' ', ' ')
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

if mode=='run_skinsDL_Menu' : skinsDL_Menu()