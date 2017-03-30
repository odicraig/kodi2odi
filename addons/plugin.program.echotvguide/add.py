# -*- coding: utf-8 -*-

# Deleting this file cripples the entire addon

#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
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
# http://kodi.wiki/view/How-to:Write_Python_Scripts
################################################
'''
 mettaliq redo and work
 look into database
 scrape common plugins
 other m3us from www
 add stuff to settings
 imdb info
 skin color
 reyua
'''

from __future__ import unicode_literals
from collections import namedtuple
import codecs
import sys,os,json,urllib2
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,re
import shutil
import base64
import xbmcvfs
import urllib
import random
import hashlib
import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import cookielib
import pickle
import time
import datetime


addon         = 'plugin.program.echotvguide'
ADDONID       = addon
addon_name    = addon
addonPath     = xbmc.translatePath(os.path.join('special://home/addons', addon))
basePath      = xbmc.translatePath(os.path.join('special://profile', 'addon_data', addon))
tmp_File      = os.path.join(basePath, 'tmp.ini')
icon          = xbmc.translatePath(os.path.join('special://home/addons', addon, 'icon.png'))
dbPath        = xbmc.translatePath(xbmcaddon.Addon(addon).getAddonInfo('profile'))
dialog        = xbmcgui.Dialog();dp = xbmcgui.DialogProgress()

inipath       = xbmc.translatePath(os.path.join(basePath, 'resources', 'ini'))
skinpath      = xbmc.translatePath(os.path.join(basePath, 'resources', 'skins'))
m3upath       = xbmc.translatePath(os.path.join(basePath, 'resources', 'm3u'))

uktvfrance    = 'plugin.video.uktvfrance'
xtream        = 'plugin.video.xtream-codes'
iptvsubs      = 'plugin.video.iptvsubs'# this will overwrite the other one with json version.
dex           = 'plugin.video.evolutioniptv'
livemix       = 'plugin.video.livemix' 
ntv           = 'plugin.video.ntv'
ukt           = 'plugin.video.ukturk'
spinz 		  = 'plugin.video.spinz'

externaliniURL = base64.b64decode(b'aHR0cDovL3d3dy50ZGJyZXBvLmNvbS9ndWlkZS8=')

# make sure the folder is actually there already!
if not os.path.exists(basePath):
    os.makedirs(basePath)
    
# Create Resources dir        
if not os.path.exists(os.path.join(basePath, 'resources')):
    os.makedirs(os.path.join(basePath, 'resources'))

################################################# 
# Run #
#################################################
def StartCreate():
        
    external_addon_ini(externaliniURL + 'addons.ini', os.path.join(basePath, 'addons.ini'), 'wt') # Grab addons.ini
    external_addon_ini(externaliniURL + 'addons2.ini', os.path.join(basePath, 'addons2.ini'), 'wt') # Grab addons.ini
    external_addon_ini(externaliniURL + 'addons_unstable.ini', os.path.join(basePath, 'addons_unstable.ini'), 'wt') # Grab addons.ini
    external_addon_ini(externaliniURL + 'addons_paid.ini', os.path.join(basePath, 'addons_paid.ini'), 'wt') # Grab addons.ini

    add_DexTXT()        # Parse and create Dexter ini -- mayfair
    Copy_SupFavs_ini(xbmc.translatePath('special://profile/addon_data/plugin.program.super.favourites/Super Favourites/TV Guide/favourites.xml'),os.path.join(inipath,'plugin.program.super.favourites.ini'),'w')# Add Super Favorites to ini

    return
################################################# 
# Run END #
#################################################



################################################# 
# Default skin in settings dir -  run in gui.py
#################################################
def skinDL():
    '''
    # make sure the folder is actually there already!
    if not os.path.exists(basePath):
        os.makedirs(basePath)
    if not os.path.exists(os.path.join(basePath, 'resources')):
        os.makedirs(os.path.join(basePath, 'resources'))
    if not os.path.exists(skinpath):
        os.makedirs(skinpath)
    '''    
    if not os.path.exists(os.path.join(skinpath)):
        os.makedirs(skinpath)
        
    if not os.path.exists(os.path.join(skinpath, 'Default')):       
        #Default skin  
        fileUrl = externaliniURL + 'skins/Default.zip'  
        #tmpFile = xbmc.translatePath(os.path.join('special://home', 'addons', 'packages','skin.zip')) 
        tmpFile = xbmc.translatePath(os.path.join(basePath,'tmp'))
        tmpData = downloader(fileUrl,tmpFile)         
        try:
            import zipfile                  
            zin = zipfile.ZipFile(tmpFile, 'r')
            zin.extractall(skinpath)
        except: pass 
#
# skin
def downloader(url, dest, dp = None):
    #import xbmcgui
    #import urllib
    #import time
    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create("Skin","Downloading & Installing Default Skin", ' ', ' ')
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
################################################# 
# Default skin in settings dir -  END
#################################################




################################################# 
# Notification #
#################################################
def notify(header,msg,icon_path):
    duration=2000
    #xbmc.executebuiltin("XBMC.Notification(%s,%s, %s, %s)" % (header, msg, duration, icon_path))
    xbmcgui.Dialog().notification(header, msg, icon=icon_path, time=duration, sound=False)
#
################################################# 
# Get Proper time in regards to device interpolation #
#################################################
def validTime(setting, maxAge):
    previousTime = getPreviousTime(setting)
    now          = datetime.datetime.today()
    delta        = now - previousTime
    nSeconds     = (delta.days * 86400) + delta.seconds
    return nSeconds <= maxAge
#
#################################################
# Set addon Setting
#################################################     
def SetSetting(param, value):
    value = str(value)
    if GetSetting(param) == value:
        return
    xbmcaddon.Addon(addon).setSetting(param, value)
#
#################################################
# This is a pop up box notification
#################################################
def DialogOK(line1, line2='', line3=''):
    d = xbmcgui.Dialog()
    d.ok('Subscriptions', line1, line2 , line3)     
#
#################################################
# LOG
#################################################
def log(text):
    try:
        output = '%s V%s : %s' % ("Log", 'Error?', str(text))
        if DEBUG:
            xbmc.log(output)
        else:
            xbmc.log(output, xbmc.LOGDEBUG)
    except: pass     
#
#################################################
# m3u8 to TS new file
#################################################
def M3U8_TS_New(Clean_Name,tmpFile):
    try:
        s=open(Clean_Name).read()
        s=s.replace('m3u8','ts')
        f=open(tmpFile,'w')
        f.write(s)
        f.close()
    except: pass        
# 
#################################################
# m3u8 to TS replace source file
#################################################
def M3U8_TS_Replace(Clean_Name,tmpFile):
    if os.path.exists(tmpFile):
        os.remove(tmpFile)
    os.rename(Clean_Name, tmpFile)
    s=open(tmpFile).read()
    #
    s=s.replace('m3u8','ts')
    #s=s.replace('.ts','.m3u8')
    #
    f=open(Clean_Name,'w')
    f.write(s)
    f.close()
    os.remove(tmpFile)   
#
#################################################
# Append source text to file
#################################################   
def AppendText(SourceFile, DestFile):
    try:
        s=open(SourceFile).read()
        f=open(DestFile,'a')
        f.write(s)
        f.close()
    except: pass
#
#################################################
# Replace Text in file
################################################# 
def ReplaceText(SourceFile, tmpFile, old1, new1, old2, new2, old3, new3, old4, new4):
    if os.path.exists(tmpFile):
        os.remove(tmpFile)
    os.rename(SourceFile, tmpFile)
    try:
        s=open(tmpFile).read()
        s=s.replace(old1, new1)
        s=s.replace(old2, new2)
        s=s.replace(old3, new3)
        s=s.replace(old4, new4)
        f=open(SourceFile,'a')
        f.write(s)
        f.close()
        os.remove(tmpFile)
    except: pass
#
#################################################
# Copy favs and superfavs to addon ini
#################################################
def Copy_Favs_ini(favourites,Dest_File,write_style):
    #favourites=xbmc.translatePath('special://profile/favourites.xml')
    if os.path.exists(favourites):
        s=open(favourites).read()
        s=s.replace('[/COLOR]', '')        
        s=s.replace('[COLOR yellow]', '')  
        s=s.replace('[COLOR white]', '') 
        s=s.replace('[COLOR red]', '') 
        s=s.replace('[COLOR green]', '') 
        s=s.replace('[COLOR blue]', '') 
        s=s.replace('[COLOR gold]', '')
        # Canada and UK English
        s=s.replace('<favourites>', '')
        s=s.replace('</favourites>', '')
        s=s.replace('    <favourite name="', '')
        s=s.replace(')</favourite>', '')  
        # USA English
        s=s.replace('<favorites>"', '')
        s=s.replace('</favorites>', '')
        s=s.replace('    <favorite name="', '')
        s=s.replace(')</favorite>', '')
        s=s.replace('quot;', '')      
        s=s.replace('amp;', '')  
        s=s.replace('&plugin', 'plugin')     
        #s=s.replace('" thumb="', '=')
        s=s.replace('	<favourite name="', '')  
        #
        for line in s:
          sp_line = line.rstrip(os.linesep).split("\n")
          s=re.sub('thumb.*PlayMedia','=',s)
          s=s.replace('" =(', '=')
        #
        a=open(Dest_File,write_style)
        a.write('[plugin.program.super.favourites]') 
        a.write(s)
        a.close()
        #AppendText(Dest_File, xbmc.translatePath(os.path.join(basePath, 'addons.ini')))
#
#################################################
# Copy Super favs and superfavs to addon ini
#################################################
def Copy_SupFavs_ini(favourites,Dest_File,write_style):
    if os.path.exists(favourites):
        s=open(favourites).read()        
        s=s.replace('[/COLOR]', '')        
        s=s.replace('[COLOR yellow]', '')  
        s=s.replace('[COLOR white]', '') 
        s=s.replace('[COLOR red]', '') 
        s=s.replace('[COLOR green]', '') 
        s=s.replace('[COLOR blue]', '') 
        s=s.replace('[COLOR gold]', '')
        s=s.replace('[COLORornage]', '')
        s=s.replace('[COLOR whitee]', '')
        
        s=s.replace('[I]', '')
        s=s.replace('[/I]', '')   

        s=s.replace('quot;', '')      
        s=s.replace('amp;', '')
        s=s.replace('&plugin', 'plugin')     
        # Canada and UK English        
        s=s.replace('<favourites>', '')
        s=s.replace('</favourites>', '')        
        s=s.replace('	<favourite name="', '')
        s=s.replace('<favourite name="', '')            
        #s=s.replace(')</favourites>', '')         
        s=s.replace(')</favourite>', '')
        # USA English
        s=s.replace('<favorites>"', '')
        s=s.replace('</favorites>', '')
        s=s.replace('	<favorite name="', '')
        s=s.replace('<favorite name="', '') 
        #s=s.replace(')</favorites>', '')
        s=s.replace(')</favorites>', '')
        s=s.replace(')</favorite>', '')
        #
        for line in s:
          sp_line = line.rstrip(os.linesep).split("\n")
          s=re.sub('thumb.*PlayMedia','=',s)
          s=s.replace('" =(', '=')         
        #
        a=open(Dest_File,write_style)
        a.write('[plugin.program.super.favourites]\n') 
        a.write(s)
        a.close()
        #AppendText(Dest_File, xbmc.translatePath(os.path.join(basePath, 'addons.ini')))
#
#################################################
# External addon.ini # 
#################################################
def external_addon_ini(externalini, externaliniTemp, write_style):
    try:
        #notify('addons.ini','addons.ini',icon)##NOTIFY##
        req = urllib2.Request(externalini)
        res = urllib2.urlopen(req)
        www_url = res.geturl()    
        #
        response = urllib2.urlopen(www_url)
        wwwm3uFile = response.read()         
        www = open(externaliniTemp, write_style)
        www.write(wwwm3uFile)
        www.close()
    except: pass     
 



#   WIP
#################################################
# Add stalker .ini #
#################################################
def getURL(url):
    StalkerPATH    = os.path.join(basePath, 'iptv_channels')#####################################FIX
    StalkerLogon = 'LOGIN_IPTV'
    if validTime(StalkerLogon, 60 * 60 * 24): 
        StalkerJSONCommandToRun = json.load(open(StalkerPATH))
    else:
        StalkerJSONCommandToRun = add_Stalker()
        GetStalkerDate(StalkerLogon)
    stream = url.split('result', 1)[-1].lower()    
    try:
        result = StalkerJSONCommandToRun['result']
        stalkerFileResult  = result['files']
    except Exception as e:
        #StalkerErrorMessages(e)
        print 'Stalker Not Found'
        return None
    for file in stalkerFileResult:
        stalkerLabel = file['label']
        if stream == stalkerLabel.lower():
            return file['file']
    return None
#
def add_Stalker():
    StalkerPATH    = os.path.join(basePath, 'iptv_channels')####################################FIX
    try:
        Addon   =  xbmcaddon.Addon('plugin.video.stalker')
        GetMacFromSettings   =  Addon.getSetting('portal_mac_1')
        root  = 'plugin://plugin.video.stalker/?genre_name=All&portal='
        query = ('{"name": "NFPS", "parental": "false", "url": "http://portal.iptvprivateserver.tv", "mac": "%s", "serial": {"custom": false}, "password": "0000"}' % GetMacFromSettings)
        url   =  urllib.quote_plus(query)
        stalkerurl =  root + url + '&mode=channels&genre_id=*'
        stalkerJSONplugin    = ('{"jsonrpc":"2.0", "method":"Files.GetDirectory", "params":{"directory":"plugin://plugin.video.stalker"}, "id": 1}')
        stalkerJSONdirectory  = ('{"jsonrpc":"2.0", "method":"Files.GetDirectory", "params":{"directory":"%s"}, "id": 1}' % stalkerurl)
        notify('Stalker','Trying to Log into Stalker server.',os.path.join('special://home/addons', Addon, 'icon.png'))##NOTIFY##
        xbmc.executebuiltin('ActivateWindow(busydialog)')
        xbmc.executeJSONRPC(stalkerJSONplugin)
        StalkerJSONCommandToRun = xbmc.executeJSONRPC(stalkerJSONdirectory)
        xbmc.executebuiltin('Dialog.Close(busydialog)')
        content = json.loads(StalkerJSONCommandToRun.decode('utf-8', 'ignore'))
        json.dump(content, open(StalkerPATH,'w'))
        return content
    except Exception as e:
        print 'Stalker Not Found'
        return {'Error' : 'Plugin Error'}
#
def GetStalkerDate(DateSetting):
    now = datetime.datetime.today()
    SetSetting(DateSetting, str(now))
# 
# Add stalker .ini END #   WIP








###################################################################################################
################################################################################################### Subscriptions
###################################################################################################


#################################################
# IPTVsubs .ini and m3u                  Method 1
#################################################
def add_IPTVsubs():
    tempaddonPath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', iptvsubs))
    addonDirPath = xbmc.translatePath(os.path.join('special://home', 'addons', iptvsubs))
    addonDestFile = os.path.join(tempaddonPath, 'settings.xml')
    if os.path.exists(addonDirPath):    
        if os.path.exists(addonDestFile):
            try:  
                notify('ini and m3u',iptvsubs,os.path.join('special://home/addons', iptvsubs, 'icon.png'))##NOTIFY##
                Name="iptvsubs";addon_name=iptvsubs;addon=xbmcaddon.Addon(addon_name)
                urlpath='http://2.welcm.tv:8000'
                username=addon.getSetting('kasutajanimi');password=addon.getSetting('salasona')
                groups = 'ENGLISH,SPORTS,FOR ADULTS'
                #write_style = 'w'
                Run_scraper(urlpath,addon_name,username,password,Name,groups)
            except: pass
#
# Not Needed - Replace Text Method
#################################################
# Get iptvsubs Pass and replace text in addon.ini #Not Needed
#################################################
def add_IPTVsubsTXT():
    addonSettingsFile = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'plugin.video.iptvsubs','settings.xml'))
    icon = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.video.iptvsubs','icon.png'))
    if os.path.exists(addonSettingsFile):
        Source_File = os.path.join(basePath, 'addons.ini')
        #tmp_File = os.path.join(basePath, '_backup.ini')
        if os.path.exists(Source_File):
            notify('ini',iptvsubs,os.path.join('special://home/addons', iptvsubs, 'icon.png'))##NOTIFY##
            addon=xbmcaddon.Addon('plugin.video.iptvsubs');user_name=addon.getSetting('kasutajanimi');pass_word=addon.getSetting('salasona')         
            user_name_old='iptvsubsemail@gmail.com'       
            pass_word_old='iptvsubspass' 
            ReplaceText(Source_File, tmp_File, user_name_old, user_name, pass_word_old, pass_word, '','', '','')####ReplaceTXT

#

#################################################
# Add IPTVsubs beta .ini #               Method 1
#################################################
def add_IPTVsubsBeta():
    # Grab iptvsubs Beta Files    wip
    # 88888.se:8000/panel_api.php?username=thankyouall&password=kodibeta
    # urlpath+"/panel_api.php?username=thankyouall&password=kodibeta
    tempaddonPath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'plugin.video.ruyaiptv'))
    addonDirPath = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.video.ruyaiptv'))
    addonDestFile = os.path.join(tempaddonPath, 'settings.xml')
    if os.path.exists(addonDirPath):    
        if os.path.exists(addonDestFile):
            try:    
                notify('ini and m3u',iptvsubs,os.path.join('special://home/addons', iptvsubs, 'icon.png'))##NOTIFY##
                Name="IPTVSUBS Beta";addon_name='plugin.video.ruyaiptv';addon=xbmcaddon.Addon(addon_name)
                urlpath='http://bullsiptv.se:9850'
                #urlpath='http://88888.se:8000'
                #urlpath2 = addon.getSetting('server');urlpath=urlpath2   #  server  is   88888.se:8000
                username=addon.getSetting('username');password=addon.getSetting('password')
                groups = 'All channels'
                Run_scraper(urlpath,addon_name,username,password,Name,groups)
            except: pass
#
# Not Needed - Replace Text Method
#################################################
# Get iptvsubs beta Pass and replace text in addon.ini #Not Needed
#################################################
def add_IPTVsubsBetaTXT():
    addonSettingsFile = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'plugin.video.ruyaiptv','settings.xml'))
    icon = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.video.ruyaiptv','icon.png'))
    if os.path.exists(addonSettingsFile):
        Source_File = os.path.join(basePath, 'addons.ini')
        #tmp_File = os.path.join(basePath, '_backup.ini')
        if os.path.exists(Source_File):
            notify('ini','plugin.video.ruyaiptv',os.path.join('special://home/addons', 'plugin.video.ruyaiptv', 'icon.png'))##NOTIFY## 
            user_name_old='iptvsubsemail@gmail.com'       
            pass_word_old='iptvsubspass' 
            addon=xbmcaddon.Addon('plugin.video.ruyaiptv');user_name=addon.getSetting('kasutajanimi');pass_word=addon.getSetting('salasona') 
            ReplaceText(Source_File, tmp_File, user_name_old, user_name, pass_word_old, pass_word, '','', '','')####ReplaceTXT    
#

#################################################
# Add Dex .ini #                         Method 1
#################################################
def add_Dex():
    tempaddonPath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', dex))
    addonDirPath = xbmc.translatePath(os.path.join('special://home', 'addons', dex))
    addonDestFile = os.path.join(tempaddonPath, 'settings.xml')
    if os.path.exists(addonDirPath):    
        if os.path.exists(addonDestFile):
            try:
                notify('ini and m3u',dex,os.path.join('special://home/addons', dex, 'icon.png'))##NOTIFY##
                Name="dex";addon_name=dex;addon=xbmcaddon.Addon(addon_name)
                urlpath2 = addon.getSetting('lehekylg');urlpath=urlpath2+':8000'
                username=addon.getSetting('kasutajanimi');password=addon.getSetting('salasona')
                groups = '[COLOR oldlace][B]-- [COLOR deepskyblue]CANADA [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR deepskyblue]USA [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR deepskyblue]UK [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR mediumpurple]KIDS [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR mediumpurple]NEWS [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR mediumpurple]SPORTS [COLOR oldlace]--[/B][/COLOR]'
                #write_style = 'a'
                Run_scraper(urlpath,addon_name,username,password,Name,groups)
            except: pass    
 #  
# Not Needed - Replace Text Method 
################################################
# Get Dex Pass and replace text in addon2.ini #Mayfair changed to make dexter fully working!
#################################################
def add_DexTXT():
   icon = xbmc.translatePath(os.path.join('special://home', 'addons', dex,'icon.png'))#Mayfair: icon location
   addonSettingsFile = xbmc.translatePath(os.path.join('special://profile', 'addon_data', dex,'settings.xml'))#Mayfair: dexter settings location where user/pass is stored
   user_name=xbmcaddon.Addon(dex).getSetting('kasutajanimi')#Mayfair: grab username from dexter
   pass_word=xbmcaddon.Addon(dex).getSetting('salasona')#Mayfair: grab password from dexter
   Source_File = xbmc.translatePath(os.path.join('special://profile', 'addon_data', addon,'addons_paid.ini'))#Mayfair: addons2.ini location with dexter channels all correct
   pass_word_old='EVOLPASS'#Mayfair: default password in addons2.ini to replace
   user_name_old='EVOLUSER'#Mayfair: default username in addons2.ini to replace
   ReplaceText(Source_File, tmp_File, user_name_old, user_name, pass_word_old, pass_word, '','', '','')#Mayfair: replace default user/pass with correct info from dexter settings
#################################################
# Add Spinz .ini #                         Method 1
#################################################
def add_Spinz():
    tempaddonPath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', spinz))
    addonDirPath = xbmc.translatePath(os.path.join('special://home', 'addons', spinz))
    addonDestFile = os.path.join(tempaddonPath, 'settings.xml')
    if os.path.exists(addonDirPath):    
        if os.path.exists(addonDestFile):
            try:
                notify('ini and m3u',spinz,os.path.join('special://home/addons', spinz, 'icon.png'))##NOTIFY##
                Name="dex";addon_name=spinz;addon=xbmcaddon.Addon(addon_name)
                urlpath2 = addon.getSetting('lehekylg');urlpath=urlpath2+':8000'
                username=addon.getSetting('kasutajanimi');password=addon.getSetting('salasona')
                groups = 'Sports,Kids,Cinema,Spanish,English,Adult'
                #write_style = 'a'
                Run_scraper(urlpath,addon_name,username,password,Name,groups)
            except: pass    
 #  
# Not Needed - Replace Text Method 
#################################################
# Get Spinz Pass and replace text in addon.ini #Not Needed
#################################################
def add_SpinzTXT():
    addonSettingsFile = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'plugin.video.spinz','settings.xml'))
    icon = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.video.spinz','icon.png'))
    addon_name2='plugin.video.spinz';addon=xbmcaddon.Addon(addon_name2);user_name=addon.getSetting('kasutajanimi');pass_word=addon.getSetting('salasona') 
    if os.path.exists(addonSettingsFile):
        username=addon.getSetting('kasutajanimi');password=addon.getSetting('salasona')       
        Source_File = os.path.join(basePath, 'addons.ini')
        #tmp_File = os.path.join(basePath, '_backup.ini')
        if os.path.exists(Source_File):
            user_name_old='SPINZUSER'
            pass_word_old='SPINZPASS'      
            addon_name2='plugin.video.spinz';addon=xbmcaddon.Addon(addon_name2);user_name=addon.getSetting('kasutajanimi');pass_word=addon.getSetting('salasona') 
            ReplaceText(Source_File, tmp_File, user_name_old, user_name, pass_word_old, pass_word, '','', '','')####ReplaceTXT
#
#################################################
# parse dex to .ini -- Mayfair
#################################################
def add_dexini():
    TheseAddons   =  [dex]#Mayfair: only run for dexter!!
    for FoundAddon in TheseAddons:
        if CheckHasThisAddon(FoundAddon):
            notify('generating channels',FoundAddon,os.path.join('special://home/addons', FoundAddon, 'icon.png'))##NOTIFY##
            ParseDexData(FoundAddon)
def CheckHasThisAddon(FoundAddon):
    if xbmc.getCondVisibility('System.HasAddon(%s)' % FoundAddon) == 1:
        # This is a failsafe fix as this will error out if there is no pass set.  Should add check for pass is non existant in settings.xml too
        settingsFileCheck = xbmc.translatePath(os.path.join('special://home/userdata/addon_data',FoundAddon,'settings.xml'))
        if os.path.exists(settingsFileCheck):
            return True
    else:
        return False 
#              
def ParseDexData(FoundAddon):
    AddonININame = FoundAddon  + '.ini'   
    Addoninipath  = os.path.join(inipath, AddonININame)
    response = GrabSettingsFromDex(FoundAddon)
    result   = response['result'] 
    ChannelsResult = result['files']    
    ExtrasFileToWrite  = file(Addoninipath, 'w')  
    ExtrasFileToWrite.write('[')
    ExtrasFileToWrite.write(FoundAddon)
    ExtrasFileToWrite.write(']')
    ExtrasFileToWrite.write('\n')   
    TheAddonURL = []   
    for channel in ChannelsResult:
        ParsedChannels = channel['label']
        stream  = channel['file']
        ChannelURL  = GetDexStuff(FoundAddon, ParsedChannels)
        channel = RemoveDexChanCrap(FoundAddon, ChannelURL)
        FinalChannelString = channel + '\t\t=' + stream#Mayfair: make correct formating for channel names
        TheAddonURL.append(FinalChannelString)
        TheAddonURL.sort()
    for item in TheAddonURL:
      ExtrasFileToWrite.write("%s\n" % item)
    ExtrasFileToWrite.close()
    Clean_Names_dex(Addoninipath,tmp_File)
#
def GrabSettingsFromDex(FoundAddon):
    Addon    =  xbmcaddon.Addon(FoundAddon)
    username =  Addon.getSetting('kasutajanimi')
    password =  Addon.getSetting('salasona')
    BeginningOfPluginString   = 'plugin://' + FoundAddon    
    urlBody     = '/?action=stream_video&extra&page&plot&thumbnail=&title=All&url='
    endOfString    =  GetDexVariables(FoundAddon)
    startOfString  =  BeginningOfPluginString + urlBody + endOfString
    GrabThisUrl = 'username=' + username + '&password=' + password + '&type=get_live_streams&cat_id=0'
    queryURL = BeginningOfPluginString  + '/?action=security_check&extra&page&plot&thumbnail&title=Live%20TV&url'
    query = startOfString +  urllib.quote_plus(GrabThisUrl)
    checkthisurl = ('{"jsonrpc":"2.0", "method":"Files.GetDirectory", "params":{"directory":"%s"}, "id": 1}' % queryURL)
    checkthisurltoo = ('{"jsonrpc":"2.0", "method":"Files.GetDirectory", "params":{"directory":"%s"}, "id": 1}' % query)   
    try:
        xbmc.executeJSONRPC(checkthisurl)
        response = xbmc.executeJSONRPC(checkthisurltoo)
        content = json.loads(response.decode('utf-8', 'ignore'))
        return content
    except Exception as e:
        #RunSetSetting(e)
        print e
        return {'Error' : 'Plugin Error'}
#    
def GetDexStuff(FoundAddon, RemoveURLGarbage):
    RemoveURLGarbage = RemoveURLGarbage.replace('  ', ' ').replace(' [/B]', '[/B]').replace('[COLOR white]', '').replace('[/COLOR]', '').replace('[COLOR gold]', '')        
    return RemoveURLGarbage
#    
def RemoveDexChanCrap(FoundAddon, FoundChannels):
    channel = FoundChannels.rsplit('[/B]', 1)[0].split('[B]', 1)[-1]        
    return channel
#       
def GetDexVariables(FoundAddon):
    Addon    =  xbmcaddon.Addon(FoundAddon) #Mayfair: set addon name
    addre_ss =  Addon.getSetting('lehekylg') #Mayfair: grab host url from dexter settings
    po_rt =  Addon.getSetting('pordinumber') #Mayfair: grab port from dexter settings
    correct_address = addre_ss + ':' + po_rt + '/enigma2.php?' #Mayfair: combine host+port+php that was grabbed from dexter
    return correct_address #Mayfair: return correct address+port/enigma2.php
#

# parse dex to ini END #


#################################################
# Add subscriptions .ini #iptvsubs, dex, xtream mayfair: DO NOT RUN THIS FUNCTION UNTIL YOU STOP IT FROM WRITING FOR DEX OR YOU WILL OVERWRITE THE WORKING DEXTER ABOVE!!!
#################################################
def add_subscriptions():
    #TheseAddons   =  [uktvfrance, xtream, iptvsubs, dex]
    TheseAddons   =  [iptvsubs, dex, xtream]
    for FoundAddon in TheseAddons:
        if SystemHasThisAddon(FoundAddon):
            notify('Subscriptions',FoundAddon,os.path.join('special://home/addons', FoundAddon, 'icon.png'))##NOTIFY##
            RunExtras(FoundAddon)
def SystemHasThisAddon(FoundAddon):
    if xbmc.getCondVisibility('System.HasAddon(%s)' % FoundAddon) == 1:
        # This is a failsafe fix as this will error out if there is no pass set.  Should add check for pass is non existant in settings.xml too
        settingsFileCheck = xbmc.translatePath(os.path.join('special://home/userdata/addon_data',FoundAddon,'settings.xml'))
        if os.path.exists(settingsFileCheck):
            return True
    else:
        return False 
#              
def RunExtras(FoundAddon):
    AddonININame = SaveTheseIniNames(FoundAddon)  + '.sub.ini'   
    Addoninipath  = os.path.join(inipath, AddonININame)
    response = GrabFromAddon(FoundAddon)
    result   = response['result'] 
    ChannelsResult = result['files']    
    ExtrasFileToWrite  = file(Addoninipath, 'w')  
    ExtrasFileToWrite.write('[')
    ExtrasFileToWrite.write(FoundAddon)
    ExtrasFileToWrite.write(']')
    ExtrasFileToWrite.write('\n')   
    TheAddonURL = []   
    for channel in ChannelsResult:
        ParsedChannels = channel['label']
        if 'plugin.video.dex' in channel['file']:
            stream = channel['file'].replace('.ts', '.m3u8')
        else:
            stream  = channel['file']              
        ChannelURL  = GetStuff(FoundAddon, ParsedChannels)
        channel = RemoveChannelCrap(FoundAddon, ChannelURL)
        FinalChannelString = channel + '=' + stream
        TheAddonURL.append(FinalChannelString)
        TheAddonURL.sort()
    for item in TheAddonURL:
      ExtrasFileToWrite.write("%s\n" % item)
    ExtrasFileToWrite.close()
    #AppendText(Addoninipath, xbmc.translatePath(os.path.join(basePath, 'addons.ini')))
    #notify('Subscriptions',FoundAddon+ ' ini Done',os.path.join('special://home/addons', FoundAddon, 'icon.png'))##NOTIFY##
    Clean_Names(Addoninipath,tmp_File)
#
def SaveTheseIniNames(FoundAddon):
    if FoundAddon == uktvfrance:
        return 'plugin.video.uktvfrance'
    if FoundAddon == xtream:
        return 'plugin.video.xtream-codes'
    if FoundAddon == iptvsubs:
        return 'plugin.video.iptvsubs'
    if FoundAddon == dex:
        return 'plugin.video.dex'
    if FoundAddon == spinz:
        return 'plugin.video.spinz'
#
def GrabFromAddon(FoundAddon):
    Addon    =  xbmcaddon.Addon(FoundAddon)
    username =  Addon.getSetting('kasutajanimi')
    password =  Addon.getSetting('salasona')
    BeginningOfPluginString   = 'plugin://' + FoundAddon    
    urlBody     = '/?action=stream_video&extra&page&plot&thumbnail=&title=All&url='
    endOfString    =  GetAddonVariables(FoundAddon)
    startOfString  =  BeginningOfPluginString + urlBody + endOfString
    GrabThisUrl = 'username=' + username + '&password=' + password + '&type=get_live_streams&cat_id=0'
    queryURL = BeginningOfPluginString  + '/?action=security_check&extra&page&plot&thumbnail&title=Live%20TV&url'
    query = startOfString +  urllib.quote_plus(GrabThisUrl)
    checkthisurl = ('{"jsonrpc":"2.0", "method":"Files.GetDirectory", "params":{"directory":"%s"}, "id": 1}' % queryURL)
    checkthisurltoo = ('{"jsonrpc":"2.0", "method":"Files.GetDirectory", "params":{"directory":"%s"}, "id": 1}' % query)   
    try:
        xbmc.executeJSONRPC(checkthisurl)
        response = xbmc.executeJSONRPC(checkthisurltoo)
        content = json.loads(response.decode('utf-8', 'ignore'))
        return content
    except Exception as e:
        #RunSetSetting(e)
        print e
        return {'Error' : 'Plugin Error'}
#    
def GetStuff(FoundAddon, RemoveURLGarbage):
    if (FoundAddon == uktvfrance) or (FoundAddon == xtream) or (FoundAddon == iptvsubs):      
        RemoveURLGarbage = RemoveURLGarbage.replace('  ', ' ').replace(' [/COLOR]', '[/COLOR]').replace(' - NEW', '')  
        return RemoveURLGarbage
        
    if FoundAddon == dex:
        RemoveURLGarbage = RemoveURLGarbage.replace('  ', ' ').replace(' [/B]', '[/B]')        
        return RemoveURLGarbage
#    
def RemoveChannelCrap(FoundAddon, FoundChannels):
    if (FoundAddon == uktvfrance) or (FoundAddon == xtream) or (FoundAddon == iptvsubs):
        channel = FoundChannels.rsplit('[/COLOR]', 1)[0].split('[COLOR white]', 1)[-1]
        return channel
    if FoundAddon == dex:
        channel = FoundChannels.rsplit('[/B]', 1)[0].split('[B]', 1)[-1]        
        return channel
#       
def GetAddonVariables(FoundAddon):
    if (FoundAddon == uktvfrance) or (FoundAddon == xtream):
        return 'http://37.187.139.155:8000/enigma2.php?'
    if FoundAddon == iptvsubs:
        return 'http://2.welcm.tv:8000/enigma2.php?'
    if FoundAddon == dex:
        return 'http://158.69.54.54:8000/enigma2.php?' 
#
'''        
def RunSetSetting(e):
    errorSorry = 'Sorry, an error occured: JSON Error: %s' %e
    errorPlease = 'Please contact us on the forum.'
    errorUpload = 'Upload a log via the addon settings and post the link.'
    log(e)
    #DialogOK(errorSorry, errorPlease, errorUpload)
    print errorSorry
    SetSetting(SETTING, '')
'''
# Add subscriptions .ini END #



###################################################################################################
################################################################################################### M3U
###################################################################################################


# Play Playlist #
#def playDSF(url, windowed):
def playPlaylist(url, windowed):
    try:
        DSFID   =  ttTTtt(0,[112,13,108,120,117],[115,103,45,105,212,110,32,46,233,118,53,105,75,100,34,101,38,111,148,46,218,103,216,118,30,97,110,120])
        DSF     =  xbmcaddon.Addon(DSFID)
        DSFVER  =  DSF.getAddonInfo('version')
    except: pass     
    try:
        import urllib
        channel = urllib.quote_plus(url.split(':', 1)[-1])
        url = 'plugin://%s/?channel=%s' % (DSFID, channel)
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        playlist.add(url, xbmcgui.ListItem(''))
        xbmc.Player().play(playlist, windowed=windowed)
    except:
        return False
# Playlist End # 


#################################################
# CCloud #
#################################################
def add_ccloudm3u(): 
    www_fn = xbmc.translatePath(os.path.join(m3upath, 'ccloud.m3u'))   
    panel_url = "http://ccloudtv.org/lists/kodi.txt"
    req = urllib2.Request(panel_url)
    res = urllib2.urlopen(req)
    www_url = res.geturl()    
    response = urllib2.urlopen(www_url)
    wwwm3uFile = response.read()         
    www = open(www_fn, "wb")
    www.write(wwwm3uFile)
    www.close()
# CCloud End #


#################################################
# Playlist # ccloud
#################################################
def add_playlistm3u():
    # Create playlist.m3u
    import base64
    URL1 = base64.b64decode(b'aHR0cDovL2dvMmwuaW5rL2tvZGk=')#go2l
    URL2 = base64.b64decode(b'aHR0cDovL3guY28vZGJjaDAx')#x.co    
    URL3 = base64.b64decode(b'aHR0cDovL2Fpby5jY2xvdWR0di5vcmcva29kaQ==')#aio
    URL4 = base64.b64decode(b'aHR0cDovL2tvZGkuY2NsZC5pbw==')#ccld
    GrabUrls = [URL1, URL2, URL3, URL4]    
    CheckIfM3u =  '#EXTM3U'
    for url in GrabUrls:
        request  = requests.get(url)
        M3uContents = request.text
        if CheckIfM3u in M3uContents:
            path = os.path.join(dbPath, 'playlist.m3u')
            with open(path, 'a') as f:
                f.write(M3uContents)
                break

###################################################################################################
################################################################################################### INI
###################################################################################################


#################################################
# Livemix ini
#################################################
def add_livemix():    
    if CheckIfLivemix(livemix):
        notify('Livemix','Livemix ini',os.path.join('special://home/addons', livemix, 'icon.png'))##NOTIFY##
        try:
            livemix_Run(livemix)  
        except: pass      
def CheckIfLivemix(livemix):
    if xbmc.getCondVisibility('System.HasAddon(%s)' % livemix) == 1:
        return True
    return False
#
def livemix_Run(livemix):
    iniFileName = "plugin.video.livemix.ini"
    LMini  = os.path.join(inipath, iniFileName)
    write_style = "w" 
    TrytogetChannels = getLivemixChannels()
    livemixini  = file(LMini, write_style)
    livemixini.write('[')
    livemixini.write(livemix)
    livemixini.write(']')
    livemixini.write('\n')
    for tempchan in TrytogetChannels:
        LivemixChanIDs   = tempchan['label']
        stream  = tempchan['url']
        livemixini.write('%s' % LivemixChanIDs)
        livemixini.write('=')
        livemixini.write('LIVETV:')
        livemixini.write('%s' % LivemixChanIDs)
        livemixini.write('\n')   
    livemixini.write('\n')
    livemixini.close()
    #
    ReplaceText(LMini, tmp_File, 'E=LIVETV:E','E!=LIVETV:E', 'Comedy Central=LIVETV:Comedy Central','Comedy Central UK=LIVETV:Comedy Central', 'Comedy Central.=LIVETV:Comedy Central.','Comedy Central=LIVETV:Comedy Central.', 'wwe HD=LIVETV:wwe HD','WWE Network=LIVETV:wwe HD')####ReplaceTXT
    #AppendText(LMini, xbmc.translatePath(os.path.join(basePath, 'addons.ini')))
#
# Below here needed for player
#
def getLivemixChannels():
    DecodeLivemixHex   =  getINIhex('https://app.uktvnow.net/v1/get_all_channels','goat')       
    headers =  {'User-Agent':'USER-AGENT-UKTVNOW-APP-V1', 
                'User-Agent':'application/x-www-form-urlencoded; charset=UTF-8',
                'gzip':'Accept-Encoding',
                'app-token':DecodeLivemixHex,
                'Keep-Alive':'Connection',                
                'app.uktvnow.net':'Host'}
    LMData = {'username':'goat'}
    requestthelivemixchannels = requests.post('https://app.uktvnow.net/v1/get_all_channels', data=LMData, headers=headers)   
    requestLMcontent =  requestthelivemixchannels.content
    requestLMcontent =  requestLMcontent.replace('\/','/')    
    decryptitems = '"channel_name":"(.+?)","img":"(.+?)","http_stream":"(.+?)","rtmp_stream":"(.+?)","cat_id":"(.+?)"'   
    items    = re.compile(decryptitems).findall(requestLMcontent)
    LMItems = []
    for item in items:
        link = {'label': item[0], 'url': item[2]}
        LMItems.append(link)
    return LMItems
#
def getINIhex(url, uktvnowUser):
    thetime   =  FigureOutTheTime()
    st   = "uktvnow-token-" + thetime + "-" + "_|_-" + url + "-" + uktvnowUser + "-" + "_|_" + "-" + base64.b64decode("MTIzNDU2IUAjJCVedWt0dm5vd14lJCNAITY1NDMyMQ==")
    return hashlib.md5(st).hexdigest()
#
def FigureOutTheTime():
    from datetime import datetime, timedelta
    rightnowtime = datetime.now() + timedelta(hours=5)
    return rightnowtime.strftime('%B-%d-%Y')
#
# Only needed for playing - used in gui.py #   
#def getLIVETV(url):
def playlivemix(url):
    TrytogetChannels = getLivemixChannels()
    stream   = url.split(':', 1)[-1].lower()
    for tempchan in TrytogetChannels:
        LivemixChanIDs = tempchan['label']
        url   = tempchan['url']
        if stream == LivemixChanIDs.lower():
            return url
    return None
#    
# Livemix ini End #




#################################################
# Add Extra addons .ini # ntv ukt
#################################################
def add_ntv_ukt():
    TryPlugins = [ntv, ukt]
    for FoundPlugins in TryPlugins:
        if CheckThesePlugins(FoundPlugins):
            try: run_ntv_ukt(FoundPlugins)
            except: pass
#            
def CheckThesePlugins(FoundPlugins):
    if xbmc.getCondVisibility('System.HasAddon(%s)' % FoundPlugins) == 1:
        notify(FoundPlugins,FoundPlugins,os.path.join('special://home/addons', FoundPlugins, 'icon.png'))##NOTIFY##
        return True
    return False
#    
def run_ntv_ukt(FoundPlugins):
    GetFinalini = GetPlugininipath(FoundPlugins) + '.ini'
    FinalIni  = os.path.join(inipath, GetFinalini)
    ThePluginsPath = GetPluginPathString(FoundPlugins)
    PluginToWrite  = file(FinalIni, 'w')
    PluginToWrite.write('[')
    PluginToWrite.write(FoundPlugins)
    PluginToWrite.write(']')
    PluginToWrite.write('\n')
    for channel in ThePluginsPath:
        ActualChannelName   = channel['label']
        ActualChannelName = ActualChannelName.replace(' [', '[').replace(' (Shows Premier League & Various Sports)', '').replace(' U.S (Shows Various Football & Sports)', '').replace('] ', ']').replace('[COLOR aqua]', '').replace('[COLOR limegreen]', '').replace('[COLOR yellow]', '').replace('[COLOR blue]', '').replace('[COLOR orange]', '').replace('[COLOR red]', '').replace('[COLOR white]', '').replace('[/COLOR]', '').replace('[COLOR green]', '')
        stream  = channel['file']
        PluginToWrite.write('%s' % ActualChannelName)
        PluginToWrite.write('=')
        PluginToWrite.write('%s' % stream)
        PluginToWrite.write('\n')   
    PluginToWrite.write('\n')
    PluginToWrite.close()
    #AppendText(FinalIni, xbmc.translatePath(os.path.join(basePath, 'addons.ini')))
#    
def GetPlugininipath(FoundPlugins):
    if FoundPlugins == ntv:
        return 'plugin.video.ntv'
    if FoundPlugins == ukt:
        return 'plugin.video.ukturk'
#        
def GetPluginPathString(FoundPlugins):
    if FoundPlugins == ukt:
        return PrepareUKTPath(FoundPlugins)
    if FoundPlugins == ntv:
        xbmcaddon.addon(ntv).setSetting('genre', 'false')
        xbmcaddon.addon(ntv).setSetting('tvguide', 'false')
    PluginPathBeginningurl  = 'plugin://' + FoundPlugins    
    NTVPathCheck =  PrepareNTVPath(FoundPlugins)
    query   =  PluginPathBeginningurl + NTVPathCheck
    return sendJSONplugins(query, FoundPlugins)
#   
def PrepareUKTPath(FoundPlugins):
    PluginPathBeginningurl = 'plugin://' + FoundPlugins
    TryUKTPath1 = '/?description&iconimage=&mode=1&name=Live%20TV&url=http%3a%2f%2fmetalkettle.co%2fUKTurk18022016%2fLive%2520TV.txt'
    TryUKTPath2 = '/?description&iconimage=&mode=1&name=Sports&url=http%3a%2f%2fmetalkettle.co%2fUKTurk18022016%2fSportsList.txt'    
    UKTPathCommand  = []
    UKTPathCommand += sendJSONplugins(PluginPathBeginningurl + TryUKTPath1, FoundPlugins)
    UKTPathCommand += sendJSONplugins(PluginPathBeginningurl + TryUKTPath2, FoundPlugins)
    return UKTPathCommand
#    
def PrepareNTVPath(FoundPlugins):
    if FoundPlugins == ntv:
        return '/?cat=-2&mode=2&name=My%20Channels&url=url'
#
def sendJSONplugins(query, FoundPlugins):
    try:
        JsonStringToExecute     = '{"jsonrpc":"2.0", "method":"Files.GetDirectory", "params":{"directory":"%s"}, "id": 1}' % query
        ExecuteThisJsonCommand  = xbmc.executeJSONRPC(JsonStringToExecute)
        response = json.loads(ExecuteThisJsonCommand)
        result   = response['result']
        return result['files']
    except Exception as e:
        #notify('NTV and UKTurks','Sorry, an error occured: JSON Error',os.path.join('special://home/addons', FoundPlugins, 'icon.png'))##NOTIFY##
        return {'Error' : 'Plugin Error'}
#

# Not used and not needed.  inside gui.py
'''
def getPluginInfo(streamurl):
    if streamurl.isdigit():
        IsKodiPVRChannel   = 'Kodi PVR Channel'
        IsKodiPVRChannelIcon = os.path.join(RESOURCES, 'kodi-pvr.png')
        return IsKodiPVRChannel, IsKodiPVRChannelIcon
    if streamurl.startswith('plugin://'):
        name = streamurl.split('//', 1)[-1].split('/', 1)[0]
    #if streamurl.startswith('HDTV:'):
    #    name = 'plugin.video.hdtv'
    if streamurl.startswith('HDTV2:'):
        name = 'plugin.video.ruyaiptv'
    if streamurl.startswith('HDTV3:'):
        name = 'plugin.video.ruyatv'
    #if streamurl.startswith('HDTV4:'):
    #    name = 'plugin.video.xl'
    #if streamurl.startswith('IPLAY:'):
    #    name = 'plugin.video.bbciplayer'
    #if streamurl.startswith('IPLAY2:'):
    #    name = 'plugin.video.iplayerwww'
    #if streamurl.startswith('IPLAYR:'):
    #    name = 'plugin.video.iplayerwww'
    #if streamurl.startswith('IPLAYITV:'):
    #    name = 'plugin.video.itv'
    if streamurl.startswith('LIVETV:'):
        name = 'plugin.video.livemix'
    if streamurl.startswith('upnp:'):
        name = 'script.hdhomerun.view'
    try:
        IsKodiPVRChannel   = xbmcaddon.Addon(name).getAddonInfo('name')
        IsKodiPVRChannelIcon = xbmcaddon.Addon(name).getAddonInfo('icon')
    except:
        IsKodiPVRChannel   = 'Unknown stream or add-on'
        IsKodiPVRChannelIcon =  ICON
    return IsKodiPVRChannel, IsKodiPVRChannelIcon
#
'''  
# Add Extra addons .ini END  # ntv ukt  




#################################################
# PVR Start #
#################################################
def add_pvr():
    iniFle = 'pvr.ini';writestyle = 'w'
    iniPvrAddonName = 'plugin.program.tdbtvguide'
    #iniPvrAddonName = 'pvr.iptvsimple'
    #
    PVRACTIVE   = (xbmc.getCondVisibility('Pvr.HasTVChannels')) or (xbmc.getCondVisibility('Pvr.HasRadioChannels')) == True    
    if not PVRACTIVE:
        return       
    pvrinipath  = os.path.join(inipath, iniFle)
    notify('PVR',iniFle,os.path.join(addonPath, 'resources', 'png', 'pvr.png'))##NOTIFY##
    # tv
    try:
        tryTvChannels  = _getPVRChannels('"tv"')
        tryTvChannelsCommand = tryTvChannels['result']          
    except: pass   
    # radio
    try:
        tryRadio  = _getPVRChannels('"radio"')
        tryRadioCommand = tryRadio['result']
    except: pass
    # Execute
    try:
        foundTvChannels  = tryTvChannelsCommand['channels']      
        foundRadioChannels  = tryRadioCommand['channels']
    except: pass    
    ThePVRini  = file(pvrinipath, writestyle)    
    ThePVRini.write('['+iniPvrAddonName+']\n')       
    try:
        for TryToFindStreams in foundTvChannels:
            WhatsTheGroupID  = TryToFindStreams['label']  
            stream = ('%s') % TryToFindStreams['channelid']
            ThePVRini.write('%s' % WhatsTheGroupID)
            ThePVRini.write("=")
            ThePVRini.write(('%s') % stream)            
            ThePVRini.write("\n")
    except: pass    
    try:
        for TryToFindStreams in foundRadioChannels:          
            WhatsTheGroupID  = TryToFindStreams['label']  
            stream = ('%s') % TryToFindStreams['channelid']
            ThePVRini.write('%s' % WhatsTheGroupID)
            ThePVRini.write("=")
            ThePVRini.write('%s' % stream)            
            ThePVRini.write("\n")
    except: pass   
    ThePVRini.write("\n")
    ThePVRini.close()
    #AppendText(pvrinipath, xbmc.translatePath(os.path.join(basePath, 'addons.ini')))
#
def _getPVRChannels(group):   
    method   = 'PVR.GetChannels'
    params   = 'channelgroupid'
    WhatAreGroupIDs  =  getGroupID(group)
    checkPVR =  sendJSONpvr(method, params, WhatAreGroupIDs)   
    return checkPVR
#
def getGroupID(group):
    method   = 'PVR.GetChannelGroups'
    params   = 'channeltype'   
    checkPVR = sendJSONpvr(method, params, group)
    result   = checkPVR['result']
    groups   = result['channelgroups']
    #
    for group in groups:
        WhatsTheGroupID = group['label']
        if WhatsTheGroupID == 'All channels':
            return group['channelgroupid']
#
def sendJSONpvr(method, params, value):
    JSONPVR  = ('{"jsonrpc":"2.0","method":"%s","params":{"%s":%s}, "id":"1"}' % (method, params, value))    
    checkPVR = xbmc.executeJSONRPC(JSONPVR)
    return json.loads(checkPVR.decode("utf-8"),"ignore")
# PVR End #




#################################################
#Testing Files#
#################################################
def Testing_Files():
    nonpublicFile = xbmc.translatePath(os.path.join('special://home','nonpublic.zip'))
    if os.path.exists(nonpublicFile):
        try:
            notify('Test','Test Files',icon)##NOTIFY##
            import zipfile                  
            zin = zipfile.ZipFile(nonpublicFile, 'r')
            zin.extractall(addonPath)
            #os.remove(nonpublicFile)
        except: pass
    ####Testing Files####
    testFile = xbmc.translatePath(os.path.join(addonPath,'test.py'))
    if os.path.exists(testFile):
        try:
            import test                  
        except: pass
####Testing Files END ####


#################################################
# Delete my own db as a failsafe.
#################################################
def NukeDB(poopooheadPath):
    try:
        notify('Database','Reset Database',icon)##NOTIFY##
        print 'meh'
        dirtypoopooheads  = "os.remove(os.path.join(xbmc.translatePath('special://profile/'),poopooheadPath))"
        dirtypoopooheads  = "os.remove(os.path.join(xbmc.translatePath('special://profile/'),poopooheadPath))"
        eval(dirtypoopooheads)
    except: pass


#################################################
# Delete people being unsavory.  
#################################################
def dickheads(uninstall=False):
    #import hashlib
    #import xbmcvfs
    #import xbmc
    bad_md5s = [
    ('special://home/media/-splash.png', '926dc482183da52644e08658f4bf80e8'),
    ('special://home/media/-splash.png', '084e2bc2ce2bf099ce273aabe331b02e'),
    ('special://home/addons/-skin.hybrid.dev/backgrounds/kevin-hart-screw-face.jpg', '0fa8f320016798adef160bb8880479bc')]
    bad_addons = ['-plugin.program.targetin1080pwizard', '-plugin.video.targetin1080pwizard']
    found_md5 = False
    for path, bad_md5 in bad_md5s:
        f = xbmcvfs.File(path)
        md5 = hashlib.md5(f.read()).hexdigest()
        if md5 == bad_md5:
            found_md5 = True
            break
    #
    has_bad_addon = any(xbmc.getCondVisibility('System.HasAddon(%s)' % (addon)) for addon in bad_addons)
    if has_bad_addon or found_md5:
        import xbmcgui
        import sys
        line2 = 'Press OK to uninstall this addon' if uninstall else 'Press OK to exit this addon'
        xbmcgui.Dialog().ok('An Addon is blacklisted', 'This addon will not work with the addon you have installed', line2)
        if uninstall:
            import xbmcaddon
            import shutil
            addon_path = xbmcaddon.addon().getAddonInfo('path').decode('utf-8')
            shutil.rmtree(addon_path)
        return False
    return False




#################################################
# Create m3u and ini files #
#################################################
def Run_scraper(urlpath,addon_name,username,password,Name,groups):
    panel_url = urlpath+"/panel_api.php?username={}&password={}".format(username, password)  
    u = urllib2.urlopen(panel_url)
    j = json.loads(u.read())
    #
    # Channel ID Map
    my_map = {}    
    '''
    my_map = {"TREEHOUSE HD (NA)":"I80173.labs.zap2it.com",
              "FAMILY HD (NA)":"I70520.labs.zap2it.com",
              }
    '''          
    map_file =''
    if map_file:
      with open(map_file) as f:
        for line in f:
          sp_line = line.rstrip(os.linesep).split("\t")
          my_map[sp_line[0]] = sp_line[1]
    #
    # Renames channels as they are downloaded
    channelname_map = {"5*":"5Star", 
                       #"3E HD":"3e",
                       "5STAR MAX HD - NEW":"5StarMax",
                       "A+E HD":"A&E",
                       "5 Star":"5Star",
                       "ABC HD EAST":"ABC HD",                       
                       "ABC HD WEST - NEW":"ABC West",                      
                       "ABC NEWS":"ABC News",                       
                       "ACTION HD":"ACTION",
                       "ACTION MAX HD - NEW":"ActionMax",                       
                       "ALJAZEERA ENGLISH":"Aljazeera",                      
                       "AMAZING DISCOVERIES":"Amazing Discoveries",                       
                       "AMAZING FACTS":"Amazing Facts",    
                       "ANIMAL PLANET HD":"Animal Planet", 
                       "BBC AMERICA HD":"BBC America",
                       "BBC NEWS":"BBC News", 
                       "BBC One HD":"BBC1",
                       "BBC Two HD":"BBC2",
                       "BBC Three HD":"BBC3",
                       "BBC Four HD":"BBC4", 
                       "BC1 HD - NEW":"BC1", 
                       "BET HD":"BET",
                       "BLOOMBERG":"Bloomberg", 
                       "BNN HD - NEW":"BNN", 
                       "BOUNCE HD":"Bounce",
                       "BRAVO HD":"Bravo",
                       "CARTOON NETWORK HD (NA)":"Cartoon Network", 
                       "CBC EAST HD":"CBC", 
                       "CBC NEWS HD":"CBC News",
                       "CBC VANCOUVER HD- NEW":"CBC Vancouver", 
                       "CBS HD EAST":"CBS HD", 
                       "CBS HD WEST - NEW":"CBS West",
                       "CBS NEWS HD":"CBS News",
                       "CHCH HD":"CHCH",
                       "CINEMAX EAST HD - NEW":"Cinemax", 
                       "CITY TV HD":"City TV Toronto",
                       "CITY VANCOUVER HD - NEW":"City TV Vancouver", 
                       "CNBC HD":"CNBC", 
                       "CNN HD":"CNN",
                       #"COMEDY NETWORK HD":"Comedy Network",
                       "COMEDY NETWORK HD":"Comedy Central",
                       "CP24 HD":"CP24",
                       "CTV EAST HD":"CTV Toronto", 
                       "CTV NORTH":"CTV North",
                       "CTV VANCOUVER HD - NEW":"CTV Vancouver", 
                       "CW11 HD":"CW", 
                       "DISCOVERY HD":"Discovery",
                       "DISCOVERY SCIENCE HD":"Discovery Science",
                       "DISNEY HD EAST":"Disney",
                       "DISNEY XD HD (NA)":"Disney XD", 
                       "E! HD":"E!",
                       "ENCORE WESTERN HD - NEW":"Encore Western", 
                       "FAMILY HD (NA)":"FAMILY", 
                       "FOOD HD":"Food Network",
                       "FOX HD EAST":"FOX HD",
                       "FOX HD WEST - NEW":"FOX West",    
                       "FOX NEWS HD":"FOX News", 
                       "FX HD":"FX",
                       "FXX HD":"FXX", 
                       "GLOBAL BC HD - NEW":"Global Vancouver", 
                       "GLOBAL EAST HD":"Global Toronto",
                       "HALLMARK HD":"Hallmark",
                       "HBO COMEDY HD":"HBO Comedy", 
                       "HBO EAST HD":"HBO HD", 
                       "HBO SIGNATURE HD":"HBO Signature",
                       "HGTV HD":"HGTV", 
                       "HISTORY HD":"History", 
                       "HLN HD":"HLN",
                       "HSN 2":"HSN2",                       
                       "ID HD":"Discovery Investigation",
                       "IFC HD":"IFC",    
                       "LIFE HD":"Lifetime", 
                       "LIFETIME MOVIES HD":"LMN",
                       "MOREMAX HD - NEW":"MoreMax", 
                       "MOVIE TIME HD":"MovieTime", 
                       "MSNBC HD":"MSNBC",
                       "MTV HD":"MTV",
                       "NAT GEO HD":"National Geographic", 
                       "NAT GEO WILD HD":"Nat Geo Wild", 
                       "NBC HD EAST":"NBC HD",
                       "NBC HD WEST - NEW":"NBC West", 
                       "NICKELODEON HD (NA)":"Nickelodeon", 
                       "OMNI 1 HD":"OMNI 1",
                       "OMNI 2 HD":"OMNI 2",
                       "OWN HD":"OWN",    
                       "PBS HD":"PBS", 
                       "REV'N USA HD":"Rev USA",
                       "RT DOCUMENTARY HD":"RT Documentary", 
                       "RT NEWS HD":"RT News", 
                       "SHOWCASE HD":"SHOWCASE",
                       "SHOWTIME EAST":"Showtime HD",
                       "SHOWTIME SHOWCASE HD":"Showtime Showcase", 
                       "SKY CBBC HD":"CBBC", 
                       "SKY DISNEY JR (UK)":"Disney Jr UK",
                       "SKY DISNEY XD (UK)":"Disney XD UK", 
                       "SKY NEWS HD":"Sky News", 
                       "SKY NICK (UK)":"Nickelodeon UK",
                       "SKY NICK TOONS (UK)":"Nick Toons UK",
                       "SLICE HD":"SLICE",    
                       "SPIKE HD":"Spike", 
                       "STARZ BLACK HD":"Starz In Black",
                       "STARZ COMEDY HD - NEW":"Starz Comedy", 
                       "STARZ EDGE HD":"Starz Edge", 
                       "STARZ HD":"Starz",
                       "STARZ KIDZ HD - NEW":"Starz Kids",
                       "Sky 3E":"3E", 
                       "Sky Alibi":"Alibi", 
                       "Sky Animal Planet":"Animal Planet UK",
                       "Sky Channel 4":"Channel 4", 
                       "Sky Channel 5":"Channel 5", 
                       "Sky Comedy Network":"Comedy Central UK",
                       "Sky Crime and Investigation":"Crime and Investigation",
                       "Sky Dave":"Dave",    
                       "Sky Discovery":"Discovery UK", 
                       "Sky Discovery History":"Discovery History",
                       "Sky Discovery Science":"Discovery Science UK", 
                       "Sky Discovery Shed":"Discovery Shed", 
                       "Sky Discovery Turbo":"Discovery Turbo",
                       "Sky Discovery investigation":"Discovery Investigation UK",
                       "Sky Eden":"Eden", 
                       "Sky Film 4":"Film4", 
                       "Sky Food":"Food UK",
                       "Sky Gold":"Gold", 
                       "Sky Home":"Home", 
                       "Sky Movie Romance":"Sky Movies Drama",
                       "Sky Movies Atlantic":"Sky Atlantic",    
                       "Sky Movies Sci-Fi":"Sky Movies Scifi", 
                       "Sky Natgeo":"National Geographic UK",
                       "SKY News":"Sky News",
                       "Sky One":"Sky1", 
                       "Sky Quest":"Quest", 
                       "Sky RTE 1":"RTE1",
                       "Sky RTE 2":"RTE2",
                       "Sky Watch":"Watch",  
                       "Sky Yesterday":"Yesterday", 
                       "Sky itv1":"ITV1",
                       "Sky itv2":"ITV2", 
                       "Sky itv3":"ITV3",
                       "Sky itv4":"ITV4",
                       "SyFy HD":"Syfy",
                       "TBS HD":"TBS",    
                       "TCM EAST HD":"TCM", 
                       "TCM HD":"TCM",
                       "THRILLER MAX HD - NEW":"ThrillerMax", 
                       "TLC HD":"TLC", 
                       "TNT HD":"TNT",
                       "TRAVEL HD":"Travel",
                       "TREEHOUSE HD (NA)":"TREEHOUSE", 
                       "TRU TV HD":"truTV", 
                       "TV LAND HD":"TV Land",
                       "TVO HD (NA)":"TVO", 
                       "USA NETWORK HD":"USA Network", 
                       "VELOCITY HD":"VELOCITY",
                       "VEVO 1 HD":"VEVO1",
                       "VEVO 2 HD":"VEVO2",    
                       "VH1 HD":"VH1",    
                       "VICELAND HD":"Viceland", 
                       "W MOVIES HD":"W MOVIES",
                       "W NETWORK HD":"W NETWORK", 
                       "WE TV HD":"WE TV", 
                       "WEATHER CANADA HD":"Weather Canada",
                       "WEATHER USA HD":"Weather USA",
                       "WIN TV HD":"WIN TV",
                       "YTV HD (NA)":"YTV",
                       "Astro Supersports 1 HD":"Astro SuperSport 1", 
                       "Astro Supersports 2 HD":"Astro SuperSport 2", 
                       "Astro Supersports 3 HD":"Astro SuperSport 3",                        
                       "Astro Supersports 4 HD":"Astro SuperSport 4",                         
                       #"Astro Supersports 1 HD":"Astro Supersports 1", 
                       #"Astro Supersports 2 HD":"Astro Supersports 2", 
                       #"Astro Supersports 3 HD":"Astro Supersports 3",                        
                       #"Astro Supersports 4 HD":"Astro Supersports 4",                    
                       "BEIN HD":"BEINS1", 
                       "CBS SPORTS HD":"CBS Sports",
                       "ESPN HD":"ESPN",
                       "ESPN 2 HD":"ESPN2",    
                       "FOX SPORTS 1 HD":"Fox Sports 1 HD", 
                       "FOX SPORTS 2 HD":"Fox Sports 2 HD",
                       "GOLF HD":"Golf Channel", 
                       "MLB HD 01":"MLB1", 
                       "MLB HD 02":"MLB2", 
                       "MLB HD 03":"MLB3",                       
                       "MLB HD 04":"MLB4",                        
                       "MLB HD 05":"MLB5", 
                       "MLB HD 06":"MLB6",                        
                       "MLB HD 07":"MLB7",                        
                       "MLB HD 08":"MLB8",                       
                       "MLB HD 09":"MLB9",                        
                       "MLB HD 10":"MLB10",                       
                       "MLB HD 11":"MLB11",                       
                       "MLB HD 12":"MLB12",                      
                       "MLB NETWORK":"MLB Network",
                       "NBA HD":"NBA TV",
                       "NBC SPORTS":"NBCSN", 
                       "NFL NOW HD":"NFL NOW",
                       "NHL NETWORK HD":"NHL Network", 
                       "NHL ON VERSUS HD":"VERSUS", 
                       "SKY BOX NATION":"BoxNation",
                       "SKY BT 1":"BT Sport 1",
                       "SKY BT 2":"BT Sport 2",    
                       "SKY BT 1 HD":"BT Sport 1 HD",
                       "SKY BT 2 HD":"BT Sport 2 HD",
                       "Sky Sports News HD":"Sky Sports News", 
                       "SKY SPORTS 1":"Sky Sports 1 HD", 
                       "SKY SPORTS 2":"Sky Sports 2 HD", 
                       "SKY SPORTS 3":"Sky Sports 3 HD",                        
                       "SKY SPORTS 4":"Sky Sports 4 HD",                       
                       "SKY SPORTS 5":"Sky Sports 5 HD",                       
                       "SONY ESPN HD - LIVE EVENTS":"PPV",
                       #"SPORT TIME TV 1HD":"SPORT TIME TV 1HD", 
                       "SPORTSNET 360":"Sportsnet 360", 
                       "SPORTSNET ONE HD":"Sportsnet One",
                       "SPORTSNET ONT":"Sportsnet Ontario",
                       "SPORTSNET WORLD HD":"Sportsnet World", 
                       "Sky Sports News HD":"Sky Sports News HD",
                       "Sony Six HD":"Sony Six", 
                       "TEN CRICKET HD":"TEN Cricket", 
                       "TENNIS HD":"Tennis Channel",
                       "TSN 1 HD":"TSN1",
                       "TSN 2 HD":"TSN2",
                       "TSN 3 HD":"TSN3",                       
                       "TSN 4 HD":"TSN4",                       
                       "TSN 5 HD":"TSN5",                      
                       "WILLOW CRICKET HD":"WILLOW CRICKET",    
                       "WWE HD":"WWE Network", 
                       "W NETWORK":"W Network", 
                       "YANKEES HD - NEW":"YANKEES",
                       "HUSTLER HD":"HUSTLER", 
                       "PLAYBOY TV HD - NEW":"PLAYBOY", 
                       "VIVID TV - NEW":"VIVID"
                      }                      
    #channelname_map = {} 
    namemap_file = ''
    if namemap_file:
      with open(namemap_file) as f:
        for line in f:
          sp_line = line.rstrip(os.linesep).split("\t")
          channelname_map[sp_line[0]] = sp_line[1]
          
    #fuck
    #inv_map = {v: k for k, v in my_map.items()}
    
    Channel = namedtuple('Channel', ['tvg_id', 'tvg_name', 'tvg_logo', 'group_title', 'channel_url'])
    channels = []
    online_groups = set()

    #
    # Grab Channels
    for ts_id, info in j["available_channels"].iteritems():
      #channel_url = "http://2.welcm.tv:8000/live/{}/{}/{}.m3u8".format(username, password, ts_id)
      #channel_url = urlpath+":8000/live/{}/{}/{}.m3u8".format(username, password, ts_id)
      channel_url = urlpath+"/live/{}/{}/{}.m3u8".format(username, password, ts_id)
      tvg_id = ""
      tvg_name = info['name']
      if info['epg_channel_id'] and info['epg_channel_id'].endswith(".com"):
        tvg_id = info['epg_channel_id']
      if tvg_name in my_map:
        tvg_id = my_map[tvg_name]
      tvg_logo = ""
      #if info['stream_icon']:
      #  tvg_logo = info['stream_icon']
      group_title = info['category_name']
      online_groups.add(group_title)
      if tvg_name in channelname_map:
        tvg_name = channelname_map[tvg_name]
      channels.append(Channel(tvg_id, tvg_name, tvg_logo, group_title, channel_url))
    #
    # Grab Groups
    wanted_groups = sorted(online_groups)
    if groups:
      wanted_groups = groups.split(',')
      
      
    #fuck
    #group_idx = {group:idx for idx,group in enumerate(wanted_groups)}
    #  maybe
    group_idx = {}
    for idx,group in enumerate(wanted_groups):
        group_idx[group] = idx


    # Has error if channel listings is different 
    #sys.stderr.write("Channel groups: {}\n".format(",".join(wanted_groups)))
    wanted_channels = [c for c in channels if c.group_title in wanted_groups]
    wanted_channels.sort(key=lambda c: "{}-{}".format(group_idx[c.group_title], c.tvg_name))
    #
    # Sort Channels
    channel_fn = ''
    if channel_fn:
      #with open(channel_fn, 'w') as channel_f:
      with open(channel_fn, write_style) as channel_f:
        for c in wanted_channels:
          if c.tvg_id.endswith(".com"):
            if c.tvg_name in inv_map:
              channel_f.write("{}\n".format(inv_map[c.tvg_name]))
            else:
              channel_f.write("{}\n".format(c.tvg_id))
    #
    # Create m3u
    notify('m3u',addon_name + '.m3u',os.path.join('special://home/addons', addon_name, 'icon.png'))##NOTIFY##
    output_fn = addon_name + '.m3u'
    write_style = 'w'
    with codecs.open(m3upath + '/' + output_fn, write_style, 'utf-8') as f:     
      f.write('#EXTM3U\n#http://'+Name+'\n')
      for c in wanted_channels:
        #f.write('#EXTINF:-1 tvg-id="{0}" tvg-name="{1}" tvg-logo="{1}.png" group-title="{3}",{1}\n{4}\n'.format(c.tvg_id, c.tvg_name, c.tvg_logo, c.group_title, c.channel_url))
        #f.write('#EXTINF:-1 tvg-logo="{1}.png",{1}\n{4}\n'.format(c.tvg_id, c.tvg_name, c.tvg_logo, c.group_title, c.channel_url))
        f.write('#EXTINF:-1 tvg-id="{1}" tvg-name="{1}" tvg-logo="{1}.png" group-title="{3}",{1}\n{4}\n'.format(c.tvg_id, c.tvg_name, c.tvg_logo, c.group_title, c.channel_url))
    #
    Clean_Names(m3upath + '/' + output_fn, basePath+'/_iptvsubs.m3u') 
    #AppendText(m3upath + '/' + output_fn, dbPath + '/playlist.m3u')
    
      
    #
    # Create ini  
    #ini_file = addon_name + '.m3u.ini'
    ini_file = addon_name + '.ini'
    
    #notify('ini',ini_file,os.path.join('special://home/addons', addon_name, 'icon.png'))##NOTIFY##
    write_style = 'w'
    with open(inipath + '/' + ini_file, write_style) as f:
        f.write('['+addon_name+'] \n;'+Name+'\n')
        for c in wanted_channels:
            f.write('{1}={4}\n'.format(c.tvg_id, c.tvg_name, c.tvg_logo, c.group_title, c.channel_url))
    #
     
    # This will overwrite the json subscription method.  Its for the naming and ordering.              
    M3U8_TS_Replace(inipath + '/' + ini_file, tmp_File)
    #M3U8_TS_New( + '/' + , basePath+'/' + addon_name + '.ini') 
    #AppendText(inipath + '/' + ini_file, xbmc.translatePath(os.path.join(basePath, 'addons.ini')))



###################################################################################################
################################################################################################### CLEAN
###################################################################################################


#################################################
# Clean dex ini channel names # -- mayfair
#################################################
def Clean_Names_dex(Clean_Name,tmpFile):
    if os.path.exists(tmpFile):
        os.remove(tmpFile)
    os.rename(Clean_Name, tmpFile)
    s=open(tmpFile).read()
    # Clean these names in addons.ini #

    ##### -- 24/7 SHOWS Section -- ####

    s=s.replace('247 - American Dad','American Dad')
    s=s.replace('247 - Big Bang Theory','Big Bang Theory')
    s=s.replace('247 - Family Guy','Family Guy')
    s=s.replace('247 - Friends','Friends')                       
    s=s.replace('247 - Game of Thrones','Game of Thrones')                      
    s=s.replace('247 - Gravity Falls','Gravity Falls')#channel missing from database                       
    s=s.replace('247 - How I Met Your Mother','How I Met Your Mother')#channel missing from database
    s=s.replace('247 - King of Queens','King of Queens')                       
    s=s.replace('247 - My Little Pony: Friendship is Magic','My Little Pony: Friendship is Magic')#channel missing from database                      
    s=s.replace('247 - Scrubs','Scrubs')                       
    s=s.replace('247 - Seinfeld','Seinfeld')    
    s=s.replace('247 - Simpsons','The Simpsons') 
    s=s.replace('247 - Smallville','Smallville')#channel missing from database
    s=s.replace('247 - Star Trek: The Next Generation','Star Trek TNG') 
    s=s.replace('247 - Supernatural','Supernatural')#channel missing from database
    s=s.replace('247 - Two and a Half Men','Two and a Half Men')#channel missing from database
    s=s.replace('247 - Walking Dead','Walking Dead')

    ##### -- BEIN SPORTS section -- #####

    s=s.replace('beIN 1 HD','bein 1HD')
    s=s.replace('beIN 8 HD','bein 8HD')
    s=s.replace('beIN 9 HD','bein 9HD')
    s=s.replace('beIN 10 HD','bein 10HD')
    s=s.replace('beIN 11 HD','bein 11HD')
    s=s.replace('beIN 12 HD','bein 12HD')
    s=s.replace('beIN 15 HD','bein 15HD')
    s=s.replace('beIN 16 HD','bein 16HD')
    s=s.replace('beIN','bein') 
    
    #### -- News section -- ####

    #### -- USA section -- ####

    s=s.replace('A&E HD','AE HD')
    #BET HD missing from database
    s=s.replace('Boomerang HD','Boomerang US HD')
    #Bounce missing from database
    s=s.replace('Cartoon Network HD','Cartoon Net US HD')
    #CCTV USA missing from database
    s=s.replace('Cinemax HD','CineMAX East HD')
    #Cinemax MoreMax HD missing from database
    #Cinemax ThrillerMax HD missing from database
    s=s.replace('CNN HD','CNN US HD')
    s=s.replace('Comedy Central HD','Comedy Central US HD')
    s=s.replace('Comedy Central SD','Comedy Central US SD')
    #COZI TV HD missing from database
    #Destination America HD missing from database
    #Discovery Family missing from database
    s=s.replace('Discovery HD','Discovery US HD')
    #Discovery Science (US) HD missing from database
    s=s.replace('Disney HD','Disney US HD')
    s=s.replace('Disney Jr. HD','Disney Jr US HD')
    s=s.replace('Disney XD HD','Disney XD US HD')
    #DIY missing from database
    s=s.replace('E! HD','E! HD')
    #El Rey Network HD missing from database
    s=s.replace('Fox Business Network HD','Fox Business HD')
    #FOX US missing from database
    s=s.replace('Fox News HD','FOX News HD')
    #FreeForm missing from database
    s=s.replace('Golf HD','Golf Channel HD')
    #GSN missing from database
    s=s.replace('HBO','HBO East')
    #HGTV missing from database
    s=s.replace('History HD','History US HD')
    s=s.replace('ID HD','ID US HD')
    s=s.replace('LIFE HD','Lifetime HD')
    #LMN missing from database
    #ME TV missing from database
    s=s.replace('MTV HD','MTV US HD')
    s=s.replace('NBA','NBA TV')
    s=s.replace('NBA HD','NBA TV HD')
    #NHL Network missing from database
    s=s.replace('Nick HD','Nickelodeon US HD')
    #OWN missing from database
    s=s.replace('PAC-12 Los Angeles HD','PAC-12 LA HD')
    s=s.replace('PAC 12 Arizona HD','PAC-12 Arizona HD')
    s=s.replace('PAC 12 Bay Area HD','PAC-12 Bay Area HD')
    s=s.replace('PAC 12 Los Angeles HD','PAC-12 LA HD')
    s=s.replace('PAC 12 Mountain HD','PAC-12 Mountain HD')
    #PAC 12 National missing from database
    s=s.replace('PAC 12 Washington HD','PAC-12 Washington HD')
    #QVC missing from database
    #SEC Netowkr missing from database
    s=s.replace('Showtime HD','Showtime East HD')
    #Spike US missing from database
    #Sprout missing from database
    s=s.replace('Starz HD','Starz East HD')
    s=s.replace('SyFy HD','Syfy HD')
    #Telemundo missing from database
    s=s.replace('Tennis HD','Tennis Channel HD')
    #TruTV missing from database
    #TV Land missing from database
    s=s.replace('TV One','TV One NZ')
    #Unimas missing from database
    s=s.replace('Universal HD','Universal US HD')
    #Univision missing from database
    #Velocity missing from database
    #Willow missing from database
    s=s.replace('WWE Network','WWE')

    #### -- UK section -- ####

    s=s.replace('5*','5STAR')
    #AAJ TAK missing from database
    s=s.replace('AAAAAA','')
    #ABP News missing from database
    s=s.replace('Abu Dhabi TV','Dubai One')
    s=s.replace('Animal Planet','Animal Planet UK')
    s=s.replace('Animal Planet HD UK','Animal Planet UK HD')
    s=s.replace('Animal Planet UK HD UK','Animal Planet UK HD')
    #B4u Music missing from database
    s=s.replace('BabyTV UK','Baby TV')
    s=s.replace('BBC Four','BBC4')
    s=s.replace('BBC HD 2','BBC2 HD')
    s=s.replace('BBC HD 3 / CBBC HD','CBBC HD')
    s=s.replace('BBC HD 4 / CBEEBIES HD','BBC4 HD')
    s=s.replace('BBC News Channel','BBC News')
    s=s.replace('BBC NEWS HD','BBC News HD')
    s=s.replace('BBC One','BBC1')
    s=s.replace('BBC One HD','BBC1 HD')
    s=s.replace('BBC One Scotland','BBC1 Scotland')
    #BBC Red Button 1 missing from database
    s=s.replace('BBC Two England','BBC2')
    s=s.replace('BBC Two Scotland','BBC2 Scotland')
    #BET missing from database
    #Bike Channel missing from database
    s=s.replace('Bloomberg HD','Bloomberg UK HD')
    s=s.replace('BOX Hits','Box Hits')
    s=s.replace('BT ESPN HD','BT Sport ESPN')
    #BT Sports Extra missing from database
    s=s.replace('Cartoon Network HD UK','Cartoon Network UK HD')
    s=s.replace('Cartoon Net US HD UK','Cartoon Network UK HD')
    s=s.replace('CBS Action UK','CBS Action')
    s=s.replace('CBS Drama UK','CBS Drama Backup')
    s=s.replace('CBS Reality UK','CBS Reality')
    s=s.replace('CCTV NEWS','CCTV News')
    #Challange missing from database
    #Chart Show Dance missing from database
    s=s.replace('Chealsa TV','Chelsea TV')
    s=s.replace('CNN','CNN US')
    s=s.replace('CNN EU US HD','CNN EU HD')
    s=s.replace('CNN US EU HD','CNN EU HD')
    s=s.replace('CNN US US HD','CNN US HD')
    s=s.replace('CNN US US HD Canada','CNN Canada HD')
    s=s.replace('CNN US US HD USA','CNN US HD Backup')
    s=s.replace('CNN US HD Canada','CNN Canada HD')
    s=s.replace('CNN US HD USA','CNN US HD Backup')
    s=s.replace('CNN EU US HD','CNN EU HD')
    #Colors missing from database
    #Comedy Central Extra missing from database
    s=s.replace('Comedy Central HD UK','Comedy Central UK HD')
    s=s.replace('Comedy Central uk','Comedy Central UK')
    s=s.replace('Comedy Central US HD UK','Comedy Central UK HD')
    #Community missing from database
    s=s.replace('Crime & Investigation','CI UK')
    s=s.replace('Crime Investigation +1','CI UK +1')
    #CS Summer missing
    #Daystar missing
    #Daystar UK missing
    s=s.replace('Discovery Home & Health','Discovery Home UK')
    s=s.replace('Discovery Investigation','Investigation Discovery UK')
    s=s.replace('Discovery Shed.','Discovery Shed UK')
    s=s.replace('Discovery Turbo','Discovery Turbo UK')
    s=s.replace('Discovery Science HD','Discovery Science UK HD')
    s=s.replace('Disney Jr. UK','Disney Junior UK')
    s=s.replace('Disney UK','Disney Channel UK')
    s=s.replace('ES: Disney US HD','ES: Disney HD')
    #Dmax missing
    s=s.replace('Euro Sport HD','Eurosport 1 HD')
    s=s.replace('Fashion One HD','Fashion TV HD')    
    s=s.replace('Film 4','Film4')    
    s=s.replace('Food Network UK','Food Network')    
    #Forces TV missing
    s=s.replace('FOX HD UK','FOX UK HD')    
    s=s.replace('Fox UK','FOX UK')    
    s=s.replace('Fox UK HD','FOX UK HD backup')    
    s=s.replace('France24','FRANCE 24')    
    s=s.replace('Gold','GOLD')    
    #Good Food missing
    #HeartTV missing
    s=s.replace('History 2 HD UK','H2 UK HD')    
    s=s.replace('History 2','H2 UK')    
    s=s.replace('History UK','HISTORY UK')    
    #home missing
    #ID Xtra missing
    #ID Europe missing
    #Inside missing
    #Insight missing
    #Inspiration missing
    s=s.replace('ITV','ITV1')    
    s=s.replace('ITV +1','ITV +1')    
    s=s.replace('ITV Encore HD','ITV Encore HD')    
    s=s.replace('ITV HD','ITV1 HD')    
    s=s.replace('ITV4 HD','ITV4+1 HD')
    s=s.replace('ITVBE','ITVBe')    
    s=s.replace('ITVBE HD','ITVBe HD')    
    s=s.replace('ITV1 +1','ITV +1')    
    s=s.replace('ITV1 Encore HD','ITV Encore HD')    
    s=s.replace('ITV1 HD','ITV1 HD')    
    s=s.replace('ITV14 HD','ITV4+1 HD')
    s=s.replace('ITV1BE','ITVBe')    
    s=s.replace('ITV1BE HD','ITVBe HD')    
    s=s.replace('ITV12','ITV2')    
    s=s.replace('ITV12 HD','ITV2 HD')    
    s=s.replace('ITV13','ITV3')    
    s=s.replace('ITV13 HD','ITV3 HD')    
    s=s.replace('ITV14','ITV4')    
    s=s.replace('ITV14 +1','ITV4 +1')    
    #Kerrang missing
    s=s.replace('Liverpool FC','LFC TV')    
    s=s.replace('M.U.T.V','MUTV')    
    s=s.replace('Motors Tv','Motors TV')    
    s=s.replace('Movies 4 Men','Movies4Men')    
    #Movies4Men +1 missing
    #MTV 90s missing
    s=s.replace('MTV Base','MTV BASE')    
    s=s.replace('MTV HD Uk','MTV UK HD')    
    s=s.replace('MTV US HD Uk','MTV UK HD')    
    s=s.replace('MTV MUSIC UK','MTV MUSIC')    
    s=s.replace('MTV ROCKS','MTV Rocks')    
    s=s.replace('Nat Geo UK','National Geographic UK')    
    s=s.replace('Nat Geo Wild','Nat Geo Wild UK')    
    s=s.replace('Nat Geo Wild UK UK HD','Nat Geo Wild UK HD')    
    s=s.replace('National Geographic HD','National Geographic UK HD')    
    s=s.replace('Nick Jr.','Nick Jr UK')    
    s=s.replace('NickToon UK','Nicktoons UK')    
    #Now Music missing
    s=s.replace('POP','Pop')    
    s=s.replace('Quest','QUEST')    
    #QVC +1 missing
    #QVC Beauty missing
    #QVC Extra missing
    #QVC Style missing
    #QVC UK missing
    #Rishtey TV missing
    s=s.replace('RTE Junior','RTE Jr')    
    s=s.replace('RTE News','RTE News Now')    
    #S Channel missing
    #Scuzz missing
    #Setanta missing
    s=s.replace('Sky Movies Action & Adventure','Sky Action')
    s=s.replace('Sky Movies Comedy','Sky Comedy')
    s=s.replace('Sky Movies Crime & Thriller','Sky Thriller')
    s=s.replace('Sky Movies Disney','Sky Disney')
    s=s.replace('Sky Disney US HD','Sky Disney HD')
    s=s.replace('Sky Movies Drama & Romance','Sky DramaRom')
    s=s.replace('Sky Movies Family','Sky Family')
    s=s.replace('Sky Movies Greats','Sky Greats')
    s=s.replace('Sky Movies Premiere','Sky Premiere')
    s=s.replace('Sky Movies Premier HD','Sky Premiere HD')
    s=s.replace('Sky Movies Scifi & Horror','Sky ScFi Horror')
    s=s.replace('Sky Movies Select','Sky Select')
    s=s.replace('Sky Movies Showcase','Sky Showcase')
    #Sky Real Lives missing
    #Sony Movies missing
    #Sony Sab missing
    #STAR JALSHA missing
    #STAR LIFE OK missing
    #STAR PLUS missing
    s=s.replace('STARZ TV','Starz East')
    s=s.replace('SyFy UK HD','Syfy UK HD')
    #TBN missing
    s=s.replace('TCM UK','TCM')
    #THE VAULT missing
    s=s.replace('TLC UK','TLC')
    s=s.replace('Travel Channel UK','Travel Channel')
    s=s.replace('TruTV Uk','tru TV UK')
    #Universal channel UK missing
    #UTV missing
    s=s.replace('VH1 Classics','VH1 Classic')
    #Vintage TV missing
    s=s.replace('Viva','VIVA')
    s=s.replace('W HD UK','W HD')
    s=s.replace('Watch','W')
    s=s.replace('Yesterday','YESTERDAY')
    #ZEE CINEMA missing
    #ZEE PUNJABI missing
    #ZEE TV missing
    #ZING missing
    
    #### -- CANADA/USA TESTING AREA section -- ####
    
    #### -- INTERNATIONAL TESTING AREA section -- ####
    
    #### -- CANADA section -- ####
    
    #### -- FRENCH section -- ####

    f=open(Clean_Name,'a')
    f.write(s)
    f.close()
    os.remove(tmpFile)
    return
#################################################
# Clean m3u and ini channel names #
#################################################
def Clean_Names(Clean_Name,tmpFile):
    #tmpFile = os.path.join(basePath, '_backup.ini')
    if os.path.exists(tmpFile):
        os.remove(tmpFile)
    os.rename(Clean_Name, tmpFile)
    s=open(tmpFile).read()
    # Clean these names in addons.ini #
    s=s.replace('ABC HD.png','ABC_HD.png')
    s=s.replace('ABC West.png','ABC_West.png')
    s=s.replace('ABC News.png','ABC_News.png')
    s=s.replace('AMC HD.png','AMC_HD.png')
    s=s.replace('Animal Planet.png','Animal_Planet.png')
    s=s.replace('BBC America.png','BBC_America.png')
    s=s.replace('BBC News.png','BBC_News.png')
    s=s.replace('CBC News.png','CBC_News.png')
    s=s.replace('CBC Vancouver.png','CBC_Vancouver.png')
    s=s.replace('CBS HD.png','CBS_HD.png')
    s=s.replace('CBS West.png','CBS_West.png')
    s=s.replace('CBS News.png','CBS_News.png')
    s=s.replace('CCTV News.png','CCTV_News.png')     
    s=s.replace('CEEN TV.png','CEEN_TV.png')      
    s=s.replace('City TV Vancouver.png','City_TV_Vancouver.png')
    s=s.replace('CTV Regina.png','CTV_Regina.png')
    s=s.replace('CTV Toronto.png','CTV_Toronto.png')
    s=s.replace('CTV Vancouver.png','CTV_Vancouver.png')
    s=s.replace('CTV North.png','CTV_North.png')
    s=s.replace('Cartoon Network.png','Cartoon_Network.png')
    s=s.replace('City TV Toronto.png','City_TV_Toronto.png')
    s=s.replace('Comedy Central.png','Comedy_Central.png')
    s=s.replace('Comedy Central UK.png','Comedy_Central_UK.png')
    s=s.replace('Crime and Investigation.png','Crime_and_Investigation.png')
    s=s.replace('Discovery Science.png','Discovery_Science.png')
    s=s.replace('Discovery Science UK.png','Discovery_Science_UK.png')
    s=s.replace('Discovery History.png','Discovery_History.png')
    s=s.replace('Discovery Investigation.png','Discovery_Investigation.png')
    s=s.replace('Discovery Investigation UK.png','Discovery_Investigation_UK.png')
    s=s.replace('Discovery Shed.png','Discovery_Shed.png')
    s=s.replace('Discovery Turbo.png','Discovery_Turbo.png')
    s=s.replace('Discovery UK.png','Discovery_UK.png')
    s=s.replace('Disney XD.png','Disney_XD.png')
    s=s.replace('Disney XD UK.png','Disney_XD_UK.png')
    s=s.replace('Disney Jr UK.png','Disney_Jr_UK.png')
    s=s.replace('Encore Western.png','Encore_Western.png')
    s=s.replace('FOX HD.png','FOX_HD.png')
    s=s.replace('FEVA TV.png','FEVA_TV.png')
    s=s.replace('FOX West.png','FOX_West.png')
    s=s.replace('FOX News.png','FOX_News.png')
    s=s.replace('Food Network.png','Food_Network.png')
    s=s.replace('Food UK.png','Food_UK.png')
    s=s.replace('Fox News.png','Fox_News.png')
    s=s.replace('Global Vancouver.png','Global_Vancouver.png')
    s=s.replace('Global Toronto.png','Global_Toronto.png')
    s=s.replace('HBO Comedy.png','HBO_Comedy.png')
    s=s.replace('HBO HD.png','HBO_HD.png')
    s=s.replace('HBO Signature.png','HBO_Signature.png')
    s=s.replace('Movie Time.png','Movie_Time.png')
    s=s.replace('NBC HD.png','NBC_HD.png')
    s=s.replace('NBC West.png','NBC_West.png')
    s=s.replace('Nat Geo Wild.png','Nat_Geo_Wild.png')
    s=s.replace('National Geographic.png','National_Geographic.png')
    s=s.replace('Nick Toons UK.png','Nick_Toons_UK.png')       
    s=s.replace('OMNI 1.png','OMNI_1.png')      
    s=s.replace('OMNI 2.png','OMNI_1.png')   
    s=s.replace('RT Documentary.png','RT_Documentary.png')     
    s=s.replace('RT News.png','RT_News.png')  
    s=s.replace('Rev USA.png','Rev_USA.png')
    s=s.replace('Sky News.png','Sky_News.png')
    s=s.replace('Starz In Black.png','Starz_In_Black.png')
    s=s.replace('Starz Comedy.png','Starz_Comedy.png')
    s=s.replace('Starz Edge.png','Starz_Edge.png')
    s=s.replace('Starz Kids & Family.png','Starz_Kids_&_Family.png')
    s=s.replace('Showtime HD.png','Showtime_HD.png')
    s=s.replace('Showtime Showcase.png','Showtime_Showcase.png')
    s=s.replace('Animal Planet UK.png','Animal_Planet_UK.png')
    s=s.replace('Channel 4.png','Channel_4.png')
    s=s.replace('Channel 5.png','Channel_5.png')
    s=s.replace('Discovery History UK.png','Discovery_History_UK.png')
    s=s.replace('Discovery Science.png','Discovery_Science.png')
    s=s.replace('Discovery Investigation.png','Discovery_Investigation.png')
    s=s.replace('Sky Atlantic.png','Sky_Atlantic.png')
    s=s.replace('Sky Movies Drama.png','Sky_Movies_Drama.png')
    s=s.replace('Sky Movies Action.png','Sky_Movies_Action.png')
    s=s.replace('Sky Movies Comedy.png','Sky_Movies_Comedy.png')
    s=s.replace('Sky Movies Disney.png','Sky_Movies_Disney.png')
    s=s.replace('Sky Movies Family.png','Sky_Movies_Family.png')
    s=s.replace('Sky Movies Premiere.png','Sky_Movies_Premiere.png')
    s=s.replace('Sky Movies Scifi.png','Sky_Movies_Scifi.png')
    s=s.replace('Sky Movies Select.png','Sky_Movies_Select.png')
    s=s.replace('Sky Movies Showcase.png','Sky_Movies_Showcase.png')
    s=s.replace('Starz Kids.png','Starz_Kids.png')
    s=s.replace('National Geographic UK.png','National_Geographic_UK.png')
    s=s.replace('TV Land.png','TV_Land.png')
    s=s.replace('TV JAMAICA.png','TV_JAMAICA.png')
    s=s.replace('Travel XP.png','Travel_XP.png')
    s=s.replace('USA Network.png','USA_Network.png')
    s=s.replace('W MOVIES.png','W_MOVIES.png')
    s=s.replace('WE TV.png','WE_TV.png')
    s=s.replace('WE NETWORK.png','WE_NETWORK.png')
    s=s.replace('Weather Canada.png','Weather_Canada.png')
    s=s.replace('Weather USA.png','Weather_USA.png')
    s=s.replace('WIN TV.png','WIN_TV.png')
    s=s.replace('ASTRO CRICKET HD.png','ASTRO_CRICKET_HD.png')
    s=s.replace('Arena Sports 1 HD.png','Arena_Sports_1_HD.png')     
    s=s.replace('Arena Sports 2 HD.png','Arena_Sports_2_HD.png')      
    s=s.replace('Arena Sports 3 HD.png','Arena_Sports_3_HD.png') 
    s=s.replace('Arena Sports 4 HD.png','Arena_Sports_4_HD.png')    
    s=s.replace('Astro SuperSport 1.png','Astro_SuperSport_1.png')
    s=s.replace('Astro SuperSport 2.png','Astro_SuperSport_2.png')
    s=s.replace('Astro SuperSport 3.png','Astro_SuperSport_3.png')
    s=s.replace('Astro SuperSport 4.png','Astro_SuperSport_4.png')
    s=s.replace('Fox Sports 1 HD.png','Fox_Sports_1_HD.png')
    s=s.replace('Fox Sports 2 HD.png','Fox_Sports_2_HD.png')
    s=s.replace('Golf Channel.png','Golf_Channel.png')
    s=s.replace('MLB Network.png','MLB_Network.png')
    s=s.replace('NBA TV.png','NBA_TV.png')
    s=s.replace('NFL Network.png','NFL_Network.png')
    s=s.replace('NHL Network.png','NHL_Network.png')
    s=s.replace('BT Sport 1.png','BT_Sport_1.png')
    s=s.replace('BT Sport 2.png','BT_Sport_2.png')
    s=s.replace('BT Sport 1 HD.png','BT_Sport_1_HD.png')
    s=s.replace('BT Sport 2 HD.png','BT_Sport_2_HD.png')
    s=s.replace('BT SPORTS ESPN.png','BT_SPORTS_ESPN.png')
    s=s.replace('BT SPORTS EUROPE.png','BT_SPORTS_EUROPE.png')
    s=s.replace('CBS Sports.png','CBS_Sports.png')
    s=s.replace('CTH 1 HD.png','CTH_1_HD.png') 
    s=s.replace('CTH 2 HD.png','CTH_2_HD.png')  
    s=s.replace('CTH 3 HD.png','CTH_3_HD.png')  
    s=s.replace('CTH 4 HD.png','CTH_4_HD.png') 
    s=s.replace('CTH 5 HD.png','CTH_5_HD.png')      
    s=s.replace('CTH XD HD.png','CTH_XD_HD.png')
    s=s.replace('FOX SPORTS 1 ASIA.png','FOX_SPORTS_1_ASIA.png')   
    s=s.replace('FOX SPORTS 2 ASIA.png','FOX_SPORTS_2_ASIA.png')
    s=s.replace('FOX SPORTS 3 ASIA.png','FOX_SPORTS_3_ASIA.png')
    s=s.replace('MOTO GP.png','MOTO_GP.png') 
    s=s.replace('NFL NOW.png','NFL_NOW.png') 
    s=s.replace('PREMIER SPORTS.png','PREMIER_SPORTS.png')                     
    s=s.replace('Setanta Asia HD.png','Setanta_Asia_HD.png')
    s=s.replace('Sky Sports News.png','Sky_Sports_News.png')
    s=s.replace('Sky Sports 1 HD.png','Sky_Sports_1_HD.png')
    s=s.replace('Sky Sports 2 HD.png','Sky_Sports_2_HD.png')
    s=s.replace('Sky Sports 2 HD.png','Sky_Sports_2_HD.png')
    s=s.replace('Sky Sports 3 HD.png','Sky_Sports_3_HD.png')
    s=s.replace('Sky Sports 4 HD.png','Sky_Sports_4_HD.png')
    s=s.replace('Sky Sports 5 HD.png','Sky_Sports_5_HD.png')
    s=s.replace('Sky Sports F1.png','Sky_Sports_F1.png')
    s=s.replace('Sky Sports News.png','Sky_Sports_News.png')
    s=s.replace('Sony Six.png','Sony_Six.png')
    s=s.replace('Sportsnet 360.png','Sportsnet_360.png')
    s=s.replace('Sportsnet One.png','Sportsnet_One.png')
    s=s.replace('Sportsnet Ontario.png','Sportsnet_Ontario.png')
    s=s.replace('Sportsnet World.png','Sportsnet_World.png')
    s=s.replace('Tennis Channel.png','Tennis_Channel.png')
    s=s.replace('TEN Cricket.png','TEN_Cricket.png')
    s=s.replace('WWE Network.png','WWE_Network.png')
    s=s.replace('WILLOW CRICKET.png','WILLOW_CRICKET.png')
    #
    
    
    
    s=s.replace('3E HD','3e')
    s=s.replace('5STAR MAX HD - NEW','5StarMax')
    s=s.replace('A+E HD','AE')
    s=s.replace('5 Star','5STAR')
    s=s.replace('ABC HD EAST','ABC HD')                       
    s=s.replace('ABC HD WEST - NEW','ABC West')                      
    s=s.replace('ABC NEWS','ABC News')                       
    s=s.replace('ACTION HD','ACTION')
    s=s.replace('ACTION MAX HD - NEW','ActionMax')                       
    s=s.replace('ALJAZEERA ENGLISH','Aljazeera')                      
    s=s.replace('AMAZING DISCOVERIES','Amazing Discoveries')                       
    s=s.replace('AMAZING FACTS','Amazing Facts')    
    s=s.replace('ANIMAL PLANET HD','Animal Planet') 
    s=s.replace('BBC AMERICA HD','BBC America')
    s=s.replace('BBC NEWS','BBC News') 
    s=s.replace('BBC One HD','BBC1')
    s=s.replace('BBC Two HD','BBC2')
    s=s.replace('BBC Three HD','BBC3')
    s=s.replace('BBC Four HD','BBC4') 
    s=s.replace('BC1 HD - NEW','BC1') 
    s=s.replace('BET HD','BET')
    s=s.replace('BLOOMBERG','Bloomberg') 
    s=s.replace('BNN HD - NEW','BNN') 
    s=s.replace('BOUNCE HD','Bounce')
    s=s.replace('BRAVO HD','Bravo')
    s=s.replace('CARTOON NETWORK HD (NA)','Cartoon Network') 
    s=s.replace('CBC EAST HD','CBC') 
    s=s.replace('CBC NEWS HD','CBC News')
    s=s.replace('CBC VANCOUVER HD- NEW','CBC Vancouver') 
    s=s.replace('CBS HD EAST','CBS HD') 
    s=s.replace('CBS HD WEST - NEW','CBS West')
    s=s.replace('CBS NEWS HD','CBS News')
    s=s.replace('CHCH HD','CHCH')
    s=s.replace('CINEMAX EAST HD - NEW','Cinemax') 
    s=s.replace('CITY TV HD','City TV Toronto')
    s=s.replace('CITY VANCOUVER HD - NEW','City TV Vancouver') 
    s=s.replace('CNBC HD','CNBC') 
    s=s.replace('CNN HD','CNN')
    #s=s.replace('COMEDY NETWORK HD','Comedy Network')
    s=s.replace('COMEDY NETWORK HD','Comedy Central')
    s=s.replace('CP24 HD','CP24')
    s=s.replace('CTV EAST HD','CTV Toronto') 
    s=s.replace('CTV NORTH','CTV North')
    s=s.replace('CTV VANCOUVER HD - NEW','CTV Vancouver') 
    s=s.replace('CW11 HD','CW') 
    s=s.replace('DISCOVERY HD','Discovery')
    s=s.replace('DISCOVERY SCIENCE HD','Discovery Science')
    s=s.replace('DISNEY HD EAST','Disney')
    s=s.replace('DISNEY XD HD (NA)','Disney XD') 
    s=s.replace('E! HD','E!')
    s=s.replace('ENCORE WESTERN HD - NEW','Encore Western') 
    s=s.replace('FAMILY HD (NA)','FAMILY') 
    s=s.replace('FOOD HD','Food Network')
    s=s.replace('FOX HD EAST','FOX HD')
    s=s.replace('FOX HD WEST - NEW','FOX West')    
    s=s.replace('FOX NEWS HD','FOX News') 
    s=s.replace('FX HD','FX')
    s=s.replace('FXX HD','FXX') 
    s=s.replace('GLOBAL BC HD - NEW','Global Vancouver') 
    s=s.replace('GLOBAL EAST HD','Global Toronto')
    s=s.replace('HALLMARK HD','Hallmark')
    s=s.replace('HBO COMEDY HD','HBO Comedy') 
    s=s.replace('HBO EAST HD','HBO HD') 
    s=s.replace('HBO SIGNATURE HD','HBO Signature')
    s=s.replace('HGTV HD','HGTV') 
    s=s.replace('HISTORY HD','History') 
    s=s.replace('HLN HD','HLN')
    s=s.replace('HSN 2','HSN2')                       
    s=s.replace('ID HD','Discovery Investigation')
    s=s.replace('IFC HD','IFC')    
    s=s.replace('LIFE HD','Lifetime') 
    s=s.replace('LIFETIME MOVIES HD','LMN')
    s=s.replace('MOREMAX HD - NEW','MoreMax') 
    s=s.replace('MOVIE TIME HD','MovieTime') 
    s=s.replace('MSNBC HD','MSNBC')
    s=s.replace('MTV HD','MTV')
    s=s.replace('NAT GEO HD','National Geographic') 
    s=s.replace('NAT GEO WILD HD','Nat Geo Wild') 
    s=s.replace('NBC HD EAST','NBC HD')
    s=s.replace('NBC HD WEST - NEW','NBC West') 
    s=s.replace('NICKELODEON HD (NA)','Nickelodeon') 
    s=s.replace('OMNI 1 HD','OMNI 1')
    s=s.replace('OMNI 2 HD','OMNI 2')
    s=s.replace('OWN HD','OWN')    
    s=s.replace('PBS HD','PBS') 
    #s=s.replace("REV'N USA HD",'Rev USA')
    s=s.replace('RT DOCUMENTARY HD','RT Documentary') 
    s=s.replace('RT NEWS HD','RT News') 
    s=s.replace('SHOWCASE HD','SHOWCASE')
    s=s.replace('SHOWTIME EAST','Showtime HD')
    s=s.replace('SHOWTIME SHOWCASE HD','Showtime Showcase') 
    s=s.replace('SKY CBBC HD','CBBC') 
    s=s.replace('SKY DISNEY JR (UK)','Disney Jr UK')
    s=s.replace('SKY DISNEY XD (UK)','Disney XD UK') 
    s=s.replace('SKY NEWS HD','Sky News') 
    s=s.replace('SKY NICK (UK)','Nickelodeon UK')
    s=s.replace('SKY NICK TOONS (UK)','Nick Toons UK')
    s=s.replace('SLICE HD','SLICE')    
    s=s.replace('SPIKE HD','Spike') 
    s=s.replace('STARZ BLACK HD','Starz In Black')
    s=s.replace('STARZ COMEDY HD - NEW','Starz Comedy') 
    s=s.replace('STARZ EDGE HD','Starz Edge') 
    s=s.replace('STARZ HD','Starz')
    s=s.replace('STARZ KIDZ HD - NEW','Starz Kids')
    s=s.replace('Sky 3E','3e') 
    s=s.replace('Sky Alibi','Alibi') 
    s=s.replace('Sky Animal Planet','Animal Planet UK')
    s=s.replace('Sky Channel 4','Channel 4') 
    s=s.replace('Sky Channel 5','Channel 5') 
    s=s.replace('Sky Comedy Network','Comedy Central UK')
    s=s.replace('Sky Crime and Investigation','Crime and Investigation')
    s=s.replace('Sky Dave','Dave')    
    s=s.replace('Sky Discovery','Discovery UK') 
    s=s.replace('Sky Discovery History','Discovery History')
    s=s.replace('Sky Discovery Science','Discovery Science UK') 
    s=s.replace('Sky Discovery Shed','Discovery Shed') 
    s=s.replace('Sky Discovery Turbo','Discovery Turbo')
    s=s.replace('Sky Discovery investigation','Discovery Investigation UK')
    s=s.replace('Sky Eden','Eden') 
    s=s.replace('Sky Film 4','Film4') 
    s=s.replace('Sky Food','Food UK')
    s=s.replace('Sky Gold','Gold') 
    s=s.replace('Sky Home','Home') 
    s=s.replace('Sky Movie Romance','Sky Movies Drama')
    s=s.replace('Sky Movies Atlantic','Sky Atlantic')    
    s=s.replace('Sky Movies Sci-Fi','Sky Movies Scifi') 
    s=s.replace('Sky Natgeo','National Geographic UK')
    s=s.replace('SKY News','Sky News')
    s=s.replace('Sky One','Sky1') 
    s=s.replace('Sky Quest','Quest') 
    s=s.replace('Sky RTE 1','RTE1')
    s=s.replace('Sky RTE 2','RTE2')
    s=s.replace('Sky Watch','Watch')  
    s=s.replace('Sky Yesterday','Yesterday') 
    s=s.replace('Sky itv1','ITV1')
    s=s.replace('Sky itv2','ITV2') 
    s=s.replace('Sky itv3','ITV3')
    s=s.replace('Sky itv4','ITV4')
    s=s.replace('SyFy HD','Syfy')
    s=s.replace('TBS HD','TBS')    
    s=s.replace('TCM EAST HD','TCM') 
    s=s.replace('TCM HD','TCM')
    s=s.replace('THRILLER MAX HD - NEW','ThrillerMax') 
    s=s.replace('TLC HD','TLC') 
    s=s.replace('TNT HD','TNT')
    s=s.replace('TRAVEL HD','Travel')
    s=s.replace('TREEHOUSE HD (NA)','TREEHOUSE') 
    s=s.replace('TRU TV HD','truTV') 
    s=s.replace('TV LAND HD','TV Land')
    s=s.replace('TVO HD (NA)','TVO') 
    s=s.replace('USA NETWORK HD','USA Network') 
    s=s.replace('VELOCITY HD','VELOCITY')
    s=s.replace('VEVO 1 HD','VEVO1')
    s=s.replace('VEVO 2 HD','VEVO2')    
    s=s.replace('VH1 HD','VH1')    
    s=s.replace('VICELAND HD','Viceland') 
    s=s.replace('W MOVIES HD','W MOVIES')
    s=s.replace('W NETWORK HD','W NETWORK') 
    s=s.replace('WE TV HD','WE TV') 
    s=s.replace('WEATHER CANADA HD','Weather Canada')
    s=s.replace('WEATHER USA HD','Weather USA')
    s=s.replace('WIN TV HD','WIN TV')
    s=s.replace('YTV HD (NA)','YTV')
    s=s.replace('Astro Supersports 1 HD','Astro SuperSport 1') 
    s=s.replace('Astro Supersports 2 HD','Astro SuperSport 2') 
    s=s.replace('Astro Supersports 3 HD','Astro SuperSport 3')                        
    s=s.replace('Astro Supersports 4 HD','Astro SuperSport 4')                         
    s=s.replace('Astro Supersports 1 HD','Astro Supersports 1') 
    s=s.replace('Astro Supersports 2 HD','Astro Supersports 2') 
    s=s.replace('Astro Supersports 3 HD','Astro Supersports 3')                        
    s=s.replace('Astro Supersports 4 HD','Astro Supersports 4')                    
    s=s.replace('BEIN HD','BEINS1') 
    s=s.replace('CBS SPORTS HD','CBS Sports')
    s=s.replace('ESPN HD','ESPN')
    s=s.replace('ESPN 2 HD','ESPN2')    
    s=s.replace('FOX SPORTS 1 HD','Fox Sports 1 HD') 
    s=s.replace('FOX SPORTS 2 HD','Fox Sports 2 HD')
    s=s.replace('GOLF HD','Golf Channel') 
    s=s.replace('MLB HD 01','MLB1') 
    s=s.replace('MLB HD 02','MLB2') 
    s=s.replace('MLB HD 03','MLB3')                       
    s=s.replace('MLB HD 04','MLB4')                        
    s=s.replace('MLB HD 05','MLB5') 
    s=s.replace('MLB HD 06','MLB6')                        
    s=s.replace('MLB HD 07','MLB7')                        
    s=s.replace('MLB HD 08','MLB8')                       
    s=s.replace('MLB HD 09','MLB9')                        
    s=s.replace('MLB HD 10','MLB10')                       
    s=s.replace('MLB HD 11','MLB11')                       
    s=s.replace('MLB HD 12','MLB12')                      
    s=s.replace('MLB NETWORK','MLB Network')
    s=s.replace('NBA HD','NBA TV')
    s=s.replace('NBC SPORTS','NBCSN') 
    s=s.replace('NFL NOW HD','NFL NOW')
    s=s.replace('NHL NETWORK HD','NHL Network') 
    s=s.replace('NHL ON VERSUS HD','VERSUS') 
    s=s.replace('SKY BOX NATION','BoxNation')
    s=s.replace('SKY BT 1','BT Sport 1')
    s=s.replace('SKY BT 2','BT Sport 2')    
    s=s.replace('SKY BT 1 HD','BT Sport 1 HD')
    s=s.replace('SKY BT 2 HD','BT Sport 2 HD')
    s=s.replace('Sky Sports News HD','Sky Sports News') 
    s=s.replace('SKY SPORTS 1','Sky Sports 1 HD') 
    s=s.replace('SKY SPORTS 2','Sky Sports 2 HD') 
    s=s.replace('SKY SPORTS 3','Sky Sports 3 HD')                        
    s=s.replace('SKY SPORTS 4','Sky Sports 4 HD')                       
    s=s.replace('SKY SPORTS 5','Sky Sports 5 HD')                       
    s=s.replace('SONY ESPN HD - LIVE EVENTS','PPV')
    #s=s.replace('SPORT TIME TV 1HD','SPORT TIME TV 1HD') 
    s=s.replace('SPORTSNET 360','Sportsnet 360') 
    s=s.replace('SPORTSNET ONE HD','Sportsnet One')
    s=s.replace('SPORTSNET ONT','Sportsnet Ontario')
    s=s.replace('SPORTSNET WORLD HD','Sportsnet World') 
    s=s.replace('Sky Sports News HD','Sky Sports News HD')
    s=s.replace('Sony Six HD','Sony Six') 
    s=s.replace('TEN CRICKET HD','TEN Cricket') 
    s=s.replace('TENNIS HD','Tennis Channel')
    s=s.replace('TSN 1 HD','TSN1')
    s=s.replace('TSN 2 HD','TSN2')
    s=s.replace('TSN 3 HD','TSN3')                       
    s=s.replace('TSN 4 HD','TSN4')                       
    s=s.replace('TSN 5 HD','TSN5')                      
    s=s.replace('WILLOW CRICKET HD','WILLOW CRICKET')    
    s=s.replace('WWE HD','WWE Network') 
    s=s.replace('W NETWORK','W Network') 
    s=s.replace('YANKEES HD - NEW','YANKEES')
    s=s.replace('HUSTLER HD','HUSTLER') 
    s=s.replace('PLAYBOY TV HD - NEW','PLAYBOY') 
    s=s.replace('VIVID TV - NEW','VIVID')    

    s=s.replace('东方财经浦东 ','') 
    s=s.replace('凤凰卫视 ','') 
    s=s.replace('凤凰美洲台 ','') 
    s=s.replace('凤凰香港台 ','')     
    s=s.replace('华夏电视 ','')     
    s=s.replace('厦门卫视 ','') 
    s=s.replace('台视美洲','(bonus)')     
    s=s.replace('四川国际 ','')         
    s=s.replace('国际频道 ','') 
    s=s.replace('天津卫视 ','')     
    s=s.replace('天津卫视 HD ','') 
    s=s.replace('央视 ','') 
    s=s.replace('安徽卫视 ','') 
    s=s.replace('山东卫视 HD ','')     
    s=s.replace('广东南方 ','')     
    s=s.replace('广东南方卫视 ','') 
    s=s.replace('旅游卫视 ','')     
    s=s.replace('时尚生活 ','')         
    s=s.replace('昆仑 HD ','') 
    s=s.replace('東森','(bonus)')    
    s=s.replace('河南卫视 ','')         
    s=s.replace('浙江卫视 HD ','') 
    s=s.replace('澳亞衛視','(bonus)') 



    #if args.ini_file:
    #    s=s.replace('m3u8','ts')
    f=open(Clean_Name,'a')
    f.write(s)
    f.close()
    os.remove(tmpFile)
    return


# Run #
if __name__ == '__main__':
    if StartCreate():
        StartCreate()
        print 'Subscriptions1'
    else:
        #StartCreate()
        print 'Subscriptions2'
