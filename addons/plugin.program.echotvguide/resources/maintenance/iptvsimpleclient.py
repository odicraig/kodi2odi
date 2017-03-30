import xbmcplugin,xbmcaddon,xbmcgui
import time
import datetime
import xbmc
import os

addon = 'plugin.program.echotvguide'
basePath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', addon))
dialog = xbmcgui.Dialog();dp = xbmcgui.DialogProgress()


pvr1 = xbmc.translatePath(os.path.join(basePath, 'playlist.m3u'))
pvr2 = xbmc.translatePath(os.path.join(basePath, 'resources', 'm3u', 'ccloud.m3u'))
pvr3 = xbmc.translatePath(os.path.join(basePath, 'resources', 'm3u', 'plugin.video.iptvsubs.m3u'))
pvr4 = xbmc.translatePath(os.path.join(basePath, 'resources', 'm3u', 'plugin.video.dex.m3u'))


mode = "pvrmain"



def pvr_main():
    choice = dialog.select('Add to pvr simple client settings', ['Close',
                                                                 'playlist.m3u (Default)',
                                                                 'ccloud.m3u',
                                                                 'plugin.video.iptvsubs.m3u (If applicable)',
                                                                 'plugin.video.dex.m3u      (If applicable)'])
    if choice == 0:  sys.exit(0)
    if choice == 1:  epg_updater = pvrUpdater(pvr1)
    if choice == 2:  epg_updater = pvrUpdater(pvr2)
    if choice == 3:  epg_updater = pvrUpdater(pvr3)
    if choice == 4:  epg_updater = pvrUpdater(pvr4)





def pvrUpdater(updater_path):
    #updater_path = os.path.join(xbmc.translatePath('special://userdata'), 'addon_data/plugin.program.echotvguide')
    #if not os.path.isdir(updater_path):
    #  try:
    #    os.mkdir(updater_path)
    #  except:
    #    pass
    #try:
    #  pvr_addon = xbmcaddon.Addon('plugin.video.iptvsubs')
    #except:
    #  pvr_addon = None
    try:
      pvriptvsimple_addon = xbmcaddon.Addon('pvr.iptvsimple')
    except:
      pvriptvsimple_addon = None
      
    checkAndUpdatePVRIPTVSetting(pvriptvsimple_addon,"epgCache", "false")
    checkAndUpdatePVRIPTVSetting(pvriptvsimple_addon,"epgPathType", "0")
    checkAndUpdatePVRIPTVSetting(pvriptvsimple_addon,"epgPath", basePath + '/guide.xml')
    checkAndUpdatePVRIPTVSetting(pvriptvsimple_addon,"m3uPathType", "0")
    checkAndUpdatePVRIPTVSetting(pvriptvsimple_addon,"m3uPath", "{0}".format(updater_path))
    
    import xbmcgui
    icon=os.path.join(xbmc.translatePath('special://home'), 'addons/plugin.program.echotvguide/icon.png')
    dialog = xbmcgui.Dialog();dp = xbmcgui.DialogProgress()
    #xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("pvr.iptvsimple","M3U and xml added to settings.xml.",3000, icon))
    notify('pvr.iptvsimple','M3U and xml added to settings.xml',os.path.join('special://home/addons', 'plugin.program.echotvguide', 'icon.png'))##NOTIFY## 




def checkAndUpdatePVRIPTVSetting(pvriptvsimple_addon, setting, value):
  if pvriptvsimple_addon.getSetting(setting) != value:
    pvriptvsimple_addon.setSetting(setting, value)          
      
def getSetting(name):
    return __addon__.getSetting(name)          



################################################# 
# Notification #
#################################################
def notify(header,msg,icon_path):
    duration=1500
    #xbmc.executebuiltin("XBMC.Notification(%s,%s, %s, %s)" % (header, msg, duration, icon_path))
    xbmcgui.Dialog().notification(header, msg, icon=icon_path, time=duration, sound=False)
#

if mode == "pvrmain":
  epg_updater = pvr_main()
  
