import sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,urllib2,re
import shutil
import time

addon = 'plugin.program.echotvguide'
addonPath = xbmc.translatePath(os.path.join('special://home', 'addons', addon))  
icon = xbmc.translatePath(os.path.join('special://home/addons', addon, 'icon.png'))
addonPath = xbmc.translatePath(os.path.join('special://home', 'addons', addon))
dbPath = xbmc.translatePath(xbmcaddon.Addon(addon).getAddonInfo('profile'))
dialog = xbmcgui.Dialog();dp = xbmcgui.DialogProgress()

metaFile = xbmc.translatePath(os.path.join(addonPath,'resources','maintenance','meta_players.zip'))   
destPath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'plugin.video.meta'))   
destPath2 = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'plugin.video.meta', 'players')) 



import base64
xmlURL = base64.b64decode(b'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2hhbGlrdXMvX0FuZHlSZXBvL21hc3Rlci9fdHh0Lw==') # blah blah _AndyRepo/master/_txt/  

meta_players1 = 'https://api.github.com/repos/OpenELEQ/unofficial-meta-players-verified/zipball'
meta_players2 = 'https://api.github.com/repos/OpenELEQ/unofficial-meta-players-verified/zipball'
meta_players3 = 'https://api.github.com/repos/OpenELEQ/unofficial-meta-players-verified/zipball'
meta_players4 = 'https://api.github.com/repos/OpenELEQ/unofficial-meta-players-verified/zipball'


mode='run_meta_players_Menu'

def meta_players_Menu():
        choice = dialog.select('Choose meta player to Download', ['Close',
                                                           'All meta players (Built in zip)',        
                                                           meta_players1,
                                                           meta_players2,
                                                           meta_players3,
                                                           meta_players4])
        if choice == 0: sys.exit(0)
        if choice == 1:
            meta_playersDL(meta_players1)
        if choice == 2:
            meta_playersDL(meta_players2)
        if choice == 3:
            meta_playersDL(meta_players3)
        if choice == 4:
            meta_playersDL(meta_players4)



def meta_playersDL(meta_playersfile):
    asFile = xmlURL + meta_playersfile
    asDest = xbmc.translatePath(os.path.join('special://home','userdata','meta_players.xml'))


    tmpData = downloader(asFile,asDest)
    notify('Meta players', 'Meta players Installed.',os.path.join('special://home/addons', addon, 'icon.png'))##NOTIFY##  
    sys.exit() 



#GRAB POSSIBLE CREDENTIALS
def meta():
    if os.path.exists(destPath):
        try:
            if not os.path.exists(destPath2):
                os.makedirs(destPath2)     
        except: pass
            
    if os.path.exists(destPath2):
        try:
            import zipfile                  
            zin = zipfile.ZipFile(metaFile, 'r')
            zin.extractall(destPath2)
            
            import xbmcgui
            icon=os.path.join(xbmc.translatePath('special://home'), 'addons/plugin.video.meta/icon.png')
            dialog = xbmcgui.Dialog();dp = xbmcgui.DialogProgress()
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("plugin.video.meta","Meta players added to plugin.video.meta",3000, icon))
            
        except: pass






def downloader(url, dest, dp = None):
    import xbmcgui
    import urllib
    import time

    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create("Meta players","Downloading & Installing meta players", ' ', ' ')
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

if mode=='run_meta_players_Menu' : meta_players_Menu()
