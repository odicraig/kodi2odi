import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, os, sys, time, xbmcvfs, shutil #,glob,subprocess
dialog  =  xbmcgui.Dialog();dp      =  xbmcgui.DialogProgress()
mainurl_epg  = 'https://raw.githubusercontent.com/halikus/_AndyRepo/master/_txt/'
url_EPG_ADDONINI = mainurl_epg+'addons.ini'

# Not Needed
addon1='plugin.video.stalker'
addon2='plugin.video.dnatv'
addon3='plugin.video.ufo'
addon4='plugin.video.StalkerTv'
addon5='Andy.plugin.video'
addon6='-'
addon7='-'
addon8=''
addon9='-'
addon10='-'
# Not Needed
TVGuide1="plugin.program.echotvguide"
TVGuide2="plugin.program.echotvguide.Extra"
TVGuide3="plugin.program.echotvguide.UK"
TVGuide4="plugin.program.echotvguide.Sports"    
TVGuide5="plugin.program.echotvguide.Stalker"
TVGuide6="script.tvguidetecbox"
TVGuide7="script.ivueguide"
TVGuide8='script.renegadestv'
TVGuide9="-"
TVGuide10="-"


mode='CleanCache_Silent'
#mode='CleanCache_Prompt'




addon = "plugin.program.echotvguide";icon = xbmc.translatePath(os.path.join('special://home/addons', addon, 'icon.png'))
#xbmc.executebuiltin('Notification(addonname,"Cache cleared.",icon)')
xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addon,"Cache cleared.",3000, icon))  

################################
###    Silent Main           ### 
################################
def CleanCache_Silent():
    Wipe_Cache()
    Delete_Packages()
    # Delete iptv Garbage Cache Files 
    #Go_Delete_addondata_iptv_caches()    
    # Delete EPG Files      
    #Go_Delete_addondata_EPG_Files()
    # Delete addon ini Files
    #Go_Delete_addondata_addonsini_File()  
    # Delete Thumbnails
    #Remove_Textures()
    #Destroy_Path('special://home/userdata/Thumbnails')
#



################################
###    Prompt Main           ### 
################################
def CleanCache_Prompt():
    Wipe_Cache()    
    Delete_Packages()
#
    choice = xbmcgui.Dialog().yesno('Main cache cleared.  Clear plugins Cache?', 'This will clear :', 'http_portal_iptvprivateserver_tv', 'http_mw1_iptv66_tv', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        print 'Delete iptv Garbage Cache Files'
        Go_Delete_addondata_iptv_caches()   
#        
    choice = xbmcgui.Dialog().yesno('Reset EPG?', 'This will reset your EPG and addons.ini', 'This cannot run inside TV Guide', 'ReDownloaded upon next start', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        print 'Delete EPG Files'
        Go_Delete_addondata_EPG_Files()     
#
    choice = xbmcgui.Dialog().yesno('Delete addonsini?', 'This will reset your addons.ini', 'This cannot run inside TV Guide', 'ReDownloaded upon next start', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        Go_Delete_addondata_addonsini_File()
#
    choice = xbmcgui.Dialog().yesno('Clear Cached Images?', 'This will clear your textures13.db file and remove', 'your Thumbnails folder. These will automatically be', 'repopulated after a restart.', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        print 'Delete Thumbnails'
        Remove_Textures(); Destroy_Path('special://home/userdata/Thumbnails'); dialog.ok('Done', 'Done cleaning.  Perhaps restart Kodi')
#
#
#



################################
###    Delete Cache          ###
################################
def Wipe_Cache():
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
#


################################
###    Delete Packages       ###
################################
def Delete_Packages():
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons', 'packages'))
    for root, dirs, files in os.walk(packages_cache_path):
        file_count = 0
        file_count += len(files)
    # Count files and give option to delete
        if file_count > 0:
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
#


################################
###    Start Delete IPTV Caches
################################
def Go_Delete_addondata_iptv_caches():
    # Delete iptv Garbage Cache Files
    Delete_addondata_iptv_caches(addon1)
    Delete_addondata_iptv_caches(addon2)       
    Delete_addondata_iptv_caches(addon3)
    Delete_addondata_iptv_caches(addon4)
    Delete_addondata_iptv_caches(addon5)
    Delete_addondata_iptv_caches(addon6) 
    Delete_addondata_iptv_caches(addon7) 
    Delete_addondata_iptv_caches(addon8)
    Delete_addondata_iptv_caches(addon9)   
    Delete_addondata_iptv_caches(addon10)   
#
################################
###    Delete IPTV Caches    ###
################################
def Delete_addondata_iptv_caches(addon):
    path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data',addon))
    Destroy_File(path,'http_mw1_iptv66_tv')    
    Destroy_File(path,'http_mw1_iptv66_tv-genres') 
    Destroy_File(path,'http_portal_iptvprivateserver_tv')     
    Destroy_File(path,'http_portal_iptvprivateserver_tv-genres')     
    Destroy_File(path,'http_iptv66_stalkerclone_network')     
    Destroy_File(path,'http_iptv66_stalkerclone_network-genres')     
    Destroy_File(path,'http_nfps_stalkerclone_network')  
    Destroy_File(path,'http_nfps_stalkerclone_network-genres')
    Destroy_File(path,'http_nfps_stalkerclone_network.1')  
    Destroy_File(path,'http_nfps_stalkerclone_network-genres.1')
#
#


################################
###    Start Delete userdata EPG TVGuide files
################################
def Go_Delete_addondata_EPG_Files():
    # Delete EPG Files      
    Delete_addondata_EPG_Files(TVGuide1)
    Delete_addondata_EPG_Files(TVGuide2)  
    Delete_addondata_EPG_Files(TVGuide3)
    Delete_addondata_EPG_Files(TVGuide4)         
    Delete_addondata_EPG_Files(TVGuide5)        
    Delete_addondata_EPG_Files(TVGuide6)
    Delete_addondata_EPG_Files(TVGuide7)  
    Delete_addondata_EPG_Files(TVGuide8)
    Delete_addondata_EPG_Files(TVGuide9)         
    Delete_addondata_EPG_Files(TVGuide10) 
################################
###    Delete userdata EPG TVGuide files
################################
def Delete_addondata_EPG_Files(addon):    
    path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data',addon))
    Destroy_File(path,'tmp.zip')
    Destroy_File(path,'tmp.gz')
    Destroy_File(path,'tmp')
    Destroy_File(path,'master.db')
    Destroy_File(path,'source5.db')
    Destroy_File(path,'guide.xml')
    Destroy_File(path,'master.xml')
    Destroy_File(path,'Sports.xml')
    Destroy_File(path,'Networks.xml')
    Destroy_File(path,'Stalker.xml')
    Destroy_File(path,'0.xml')
    Destroy_File(path,'1.xml')
    Destroy_File(path,'2.xml')
    Destroy_File(path,'3.xml')
    Destroy_File(path,'4.xml')
    Destroy_File(path,'5.xml')
    Destroy_File(path,'guides.ini')
    #Destroy_File(path,'settings.xml')
    #Destroy_File(path,'addons.ini')
#        
#Function to wipe file
def Destroy_File(path,file):
    lib=os.path.join(path,file)
    dp.create(lib,"Wiping...",'','Please Wait')
    try:
       os.remove(lib)
       shutil.rmtree(lib, ignore_errors=True)
    except:
       pass
    


################################
###    Function to remove textures13.db and thumbnails folder
################################         
def Remove_Textures():
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
#



################################
###    Start Delete addons.ini files
################################
def Go_Delete_addondata_addonsini_File():
    TVGuide_Delete_addonsini(TVGuide1)
    TVGuide_Delete_addonsini(TVGuide2)  
    TVGuide_Delete_addonsini(TVGuide3)
    TVGuide_Delete_addonsini(TVGuide4)         
    TVGuide_Delete_addonsini(TVGuide5)        
    TVGuide_Delete_addonsini(TVGuide6)
    TVGuide_Delete_addonsini(TVGuide7)  
    TVGuide_Delete_addonsini(TVGuide8)
    TVGuide_Delete_addonsini(TVGuide9)         
    TVGuide_Delete_addonsini(TVGuide10)    
#
def TVGuide_Delete_addonsini(addon):
    path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data',addon))
    lib=os.path.join(path, 'addons.ini')
    try:
       os.remove(lib)
    except:
       pass
       #
    path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data',addon))
    lib=os.path.join(path, 'addons.ini')
    try:
       # uncomment below to download from url
       #DownloaderClass9(url_EPG_ADDONINI,lib,addon)
       time.sleep(1)
    except:
       pass
#

def DownloaderClass9(url,dest,dlfile, useReq = False):
    dp = xbmcgui.DialogProgress()
    dp.create('Downloading',"Downloading & Copying "+dlfile,'')
    if useReq:
        import urllib2
        req = urllib2.Request(url)
        req.add_header('Referer', 'http://wallpaperswide.com/')
        f       = open(dest, mode='wb')
        resp    = urllib2.urlopen(req)
        content = int(resp.headers['Content-Length'])
        size    = content / 100
        total   = 0
        while True:
            if dp.iscanceled():
                raise Exception("Canceled")
                dp.close()
            chunk = resp.read(size)
            if not chunk:
                f.close()
                break
            f.write(chunk)
            total += len(chunk)
            percent = min(100 * total / content, 100)
            dp.update(percent)
    else:
        urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
#
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled():
        raise Exception("Canceled")
        dp.close()        






#Function to do a full wipe.
def Destroy_Path(path):
    dp.create(path,"Wiping...",path, 'Please Wait')
    shutil.rmtree(path, ignore_errors=True)
#


if mode=='CleanCache_Silent' : CleanCache_Silent()
if mode=='CleanCache_Prompt' : CleanCache_Prompt()
