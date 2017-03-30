import sys,os,json,urllib2
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,urllib2,re
import shutil
import time

addon = 'plugin.program.echotvguide';addon_name = addon;icon = xbmc.translatePath(os.path.join('special://home/addons', addon, 'icon.png'))
addonPath = xbmc.translatePath(os.path.join('special://home', 'addons', addon))
basePath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', addon))
dbPath = xbmc.translatePath(xbmcaddon.Addon(addon).getAddonInfo('profile'))

dialog = xbmcgui.Dialog();dp = xbmcgui.DialogProgress()

mode='run_maintenance_system'


def maintenance_system():
        choice = dialog.select('Perform general maintenance', ['Close',
                                                               'Clean cache',
                                                               'Delete packages folder (old zips)',
                                                               'Delete Thumbnails',
                                                               'Delete textures (Database Textures13.db)'])
        if choice == 0:  sys.exit(0)
        #
        # Clean cache
        if choice == 1:
            xbmc_cache_path = xbmc.translatePath(os.path.join('special://home', 'cache'))
            if os.path.exists(xbmc_cache_path)==True:    
                for root, dirs, files in os.walk(xbmc_cache_path):
                    file_count = 0
                    file_count += len(files)       
                    # Count files and give option to delete
                    if file_count > 0:            
                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except:
                                pass
                        for d in dirs:
                            try:
                                shutil.rmtree(os.path.join(root, d))
                            except:
                                pass
            #xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("TV Guide","Cache cleared.",3000, icon))
            notify('Clean cache','Cache successfully cleaned.',os.path.join('special://home/addons', addon, 'icon.png'))##NOTIFY##                  
            sys.exit()
        #
        # Delete packages folder (old zips)
        if choice == 2:
            packages_cache_path = xbmc.translatePath(os.path.join('special://home/userdata', 'Thumbnails'))
            for root, dirs, files in os.walk(packages_cache_path):
               file_count = 0
               file_count += len(files)
               # Count files and give option to delete
               if file_count > 0:
                   for f in files:
                       os.unlink(os.path.join(root, f))
                   for d in dirs:
                       shutil.rmtree(os.path.join(root, d))
            #xbmc.executebuiltin('Notification(%s, %s, %s)'%("TV Guide","Packages cleared.", icon))
            notify('Delete packages folder','Packages successfully cleaned.',os.path.join('special://home/addons', addon, 'icon.png'))##NOTIFY##  
            sys.exit()
        #
        # Delete Thumbnails
        if choice == 3:
            path = xbmc.translatePath(os.path.join('special://home/userdata', 'Thumbnails'))
            dp.create(path,"Wiping...",path, 'Please Wait')
            shutil.rmtree(path, ignore_errors=True)
            #xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("TV Guide","Thumbnails cleared.",3000, icon))
            notify('Delete Thumbnails','Thumbnails successfully cleaned. (Restart Kodi)',os.path.join('special://home/addons', addon, 'icon.png'))##NOTIFY##  
            sys.exit()
        #
        # Delete textures (Database Textures13.db)
        if choice == 4:
            textures = xbmc.translatePath(os.path.join('special://home/userdata/Database', 'Textures13.db'))
            try:
                dbcon = database.connect(textures)
                dbcur = dbcon.cursor()
                dbcur.execute("DROP TABLE IF EXISTS path")
                dbcur.execute("VACUUM")
                dbcon.commit()
                dbcur.execute("DROP TABLE IF EXISTS sizes")
                dbcur.execute("VACUUM")
                dbcon.commit()
                dbcur.execute("DROP TABLE IF EXISTS texture")
                dbcur.execute("VACUUM")
                dbcon.commit()
                dbcur.execute("""CREATE TABLE path (id integer, url text, type text, texture text, primary key(id))""")
                dbcon.commit()
                dbcur.execute("""CREATE TABLE sizes (idtexture integer,size integer, width integer, height integer, usecount integer, lastusetime text)""")
                dbcon.commit()
                dbcur.execute("""CREATE TABLE texture (id integer, url text, cachedurl text, imagehash text, lasthashcheck text, PRIMARY KEY(id))""")
                dbcon.commit()
            except:
                pass
            notify('Delete textures','Textures (Textures13.db) cleaned. (Restart Kodi)',os.path.join('special://home/addons', addon, 'icon.png'))##NOTIFY##  
            sys.exit()
        #

################################################# 
# Notification #
#################################################
def notify(header,msg,icon_path):
    duration=1500
    #xbmc.executebuiltin("XBMC.Notification(%s,%s, %s, %s)" % (header, msg, duration, icon_path))
    xbmcgui.Dialog().notification(header, msg, icon=icon_path, time=duration, sound=False)
#


if mode=='run_maintenance_system' : maintenance_system()
