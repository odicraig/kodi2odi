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
externaliniURL = base64.b64decode(b'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2hhbGlrdXMvX0FuZHlSZXBvL21hc3Rlci9fZXBnLw==') # _AndyRepo/master/_epg/  
reposURL = externaliniURL + 'repos/'





repos1 = 'Default'
repos2 = 'FTV_Blue'
repos3 = 'FTV_Dark'
repos4 = 'FTV_Default'
repos5 = 'FTV_MOD'
repos6 = 'FTV_Eminence'
repos7 = 'FTV_Touch'

mode='run_reposDL_Menu'

def reposDL_Menu():
        choice = dialog.select('Choose zip to Download', ['Close',
                                                           repos1,
                                                           repos2,
                                                           repos3,
                                                           repos4,
                                                           repos5,
                                                           repos6,
                                                           repos7])
        if choice == 0: sys.exit(0)
        if choice == 1:
            reposDL(repos1)
        if choice == 2:
            reposDL(repos2)
        if choice == 3:
            reposDL(repos3)
        if choice == 4:
            reposDL(repos4)
        if choice == 5:
            reposDL(repos5)
        if choice == 6:
            reposDL(repos6)
        if choice == 7:
            reposDL(repos7)


def reposDL(reposfile):
    fileUrl = reposURL+reposfile+'.zip'  
    tmpFile = xbmc.translatePath(os.path.join('special://home', 'cache', 'repos.zip')) 
    tmpData = downloader(fileUrl,tmpFile)
    
            
    try:
        import zipfile                  
        zin = zipfile.ZipFile(tmpFile, 'r')
        zin.extractall(os.path.join(basePath, 'resources', 'repos'))
    except: pass
    #
    #addon.setSetting('repos', reposfile)
    SetSetting('repos', reposfile)
    notify('repos',reposfile + ' successfully Installed.',os.path.join('special://home/addons', addon, 'icon.png'))##NOTIFY##  
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
        dp.create("repos","Downloading & Installing repos", ' ', ' ')
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

if mode=='run_reposDL_Menu' : reposDL_Menu()
