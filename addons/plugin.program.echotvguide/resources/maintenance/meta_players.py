# extracts meta players to plugin.video.meta
import sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,re

addon = 'plugin.program.echotvguide'
addonPath = xbmc.translatePath(os.path.join('special://home', 'addons', addon))  
metaFile = xbmc.translatePath(os.path.join(addonPath,'resources','maintenance','meta_players.zip'))   
destPath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'plugin.video.meta'))   
destPath2 = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'plugin.video.meta', 'players')) 

mode = 'meta'

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


if mode=='meta' : meta()
