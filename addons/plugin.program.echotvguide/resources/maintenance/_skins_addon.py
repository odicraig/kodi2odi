# -*- coding: utf-8 -*-

import zipfile
import time
import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui
import urllib
import os
import re
import requests
import base64

TITLE   = 'Skins'
ADDONID = 'plugin.program.echotvguide'
ADDON   =  xbmcaddon.Addon(ADDONID)
HOME    =  ADDON.getAddonInfo('path')
PROFILE =  ADDON.getAddonInfo('profile')
VERSION = ADDON.getAddonInfo('version')
ICON    = os.path.join(HOME, 'icon.png')
FANART  = os.path.join(HOME, 'fanart.jpg')
basePath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'plugin.program.echotvguide'))
BASEURL = base64.b64decode(b'aHR0cDovL3d3dy50ZGJyZXBvLmNvbS9ndWlkZS8=') # blah blah _AndyRepo/master/_epg/  
#baseurl = 'https://raw.githubusercontent.com/halikus/_AndyRepo/master/_epg/'

import sys
path    = HOME
sys.path.insert(0, path)


_OTT            = 0
_MAIN           = 100
_ADDSKINSLIST  = 2000
_ADDLOGOSLIST  = 2100
_ADDLINEUPLIST = 2200
_GETSKINS      = 2300


def main():
    #utils.CheckVersion()
    #addDir('Back-up + Restore',   _BACKUPRESTORE,  thumbnail=ICON, fanart=FANART, isFolder=True)
    addDir('Add Skins',           _ADDSKINSLIST,   thumbnail=ICON, fanart=FANART, isFolder=True)
    #addDir('Add Logo Packs',      _ADDLOGOSLIST,   thumbnail=ICON, fanart=FANART, isFolder=True)
    

def getSkinList(id):
    regex = 'skin name="(.+?)" url="(.+?)" icon="(.+?)" fanart="(.+?)" description="(.+?)"'
    url   =  BASEURL + 'skins/'
    skins = url + 'skins.xml'
    req   = requests.get(skins)
    html  = req.content
    items = re.compile(regex).findall(html)
    for item in items:
        label  = item[0]
        id     = url + item[1]
        icon   = url + item[2]
        fanart = url + item[3]
        desc   = item[4]       
        addDir(label, _GETSKINS, id, desc=desc, thumbnail=icon, fanart=fanart, isFolder=False)
                                                                  
def getSkin(label, url):
    path    = os.path.join(basePath, 'resources', 'skins')
    zipfile = xbmc.translatePath(os.path.join('special://home', 'cache', 'skins.zip')) 
    if DialogYesNo('Would you like to install ' + label, 'and make it your active skin?', 'It will be downloaded and installed into your system.'):
        download(path, zipfile)
        DialogOK(label + ' skin has been installed successfully.', 'It is now set as your active EPG skin.', 'Please restart EPG. Thank you.')
        ADDON.setSetting('skin', label)


def download(path, zipfile):
    downloader(url, zipfile)
    extract_all(zipfile, path)
    #sfile.remove(zipfile)

def downloader(url, dest, dp = None):
    if not dp:
        dp = Progress('Downloading & Installing Files')
    dp.update(0)
    start_time=time.time()
    urllib.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time))
     
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


def extract_all(_in, _out, dp=None):
    if dp:
        return allWithProgress(_in, _out, dp)
    return allNoProgress(_in, _out)
def allNoProgress(_in, _out):
    try:
        zin = zipfile.ZipFile(_in, 'r')
        zin.extractall(_out)
    except Exception, e:
        print str(e)
        return False
    return True
def allWithProgress(_in, _out, dp):
    zin = zipfile.ZipFile(_in,  'r')
    nFiles = float(len(zin.infolist()))
    count  = 0
    try:
        for item in zin.infolist():
            count += 1
            update = count / nFiles * 100
            dp.update(int(update))
            zin.extract(item, _out)
    except Exception, e:
        print str(e)
        return False
    return True



def DialogOK(line1, line2='', line3=''):
    d = xbmcgui.Dialog()
    d.ok(TITLE + ' - ' + VERSION, line1, line2 , line3)
def DialogKB(value = '', heading = ''):
    kb = xbmc.Keyboard('', '')
    kb.setHeading(heading)
    kb.doModal()
    if (kb.isConfirmed()):
        value = kb.getText()
    return value
def DialogYesNo(line1, line2='', line3='', noLabel=None, yesLabel=None):
    d = xbmcgui.Dialog()
    if noLabel == None or yesLabel == None:
        return d.yesno(TITLE + ' - ' + VERSION, line1, line2 , line3) == True
    else:
        return d.yesno(TITLE + ' - ' + VERSION, line1, line2 , line3, noLabel, yesLabel) == True
def Progress(line1 = '', line2 = '', line3 = '', hide = False):
    dp = xbmcgui.DialogProgress()
    dp.create(TITLE, line1, line2, line3)
    dp.update(0)
    if hide:
        try:
            xbmc.sleep(250)
            WINDOW_PROGRESS = xbmcgui.Window(10101)
            CANCEL_BUTTON   = WINDOW_PROGRESS.getControl(10)
            CANCEL_BUTTON.setVisible(False)
        except:
            pass
    return dp


def SetSetting(param, value):
    value = str(value)
    if GetSetting(param) == value:
        return
    xbmcaddon.Addon(ADDONID).setSetting(param, value)


    
def addDir(label, mode, id = '', weight = -1, desc='', thumbnail='', fanart=FANART, isFolder=True, menu=None, infolabels={}, totalItems=0):
    u  = sys.argv[0]

    u += '?label=' + urllib.quote_plus(label)
    u += '&mode='  + str(mode)

    if len(id) > 0:
        u += '&id=' + urllib.quote_plus(id)

    if weight > 0:
        u += '&weight=' + urllib.quote_plus(str(weight))

    if len(thumbnail) > 0:
        u += '&image=' + urllib.quote_plus(thumbnail)

    if len(fanart) > 0:
        u += '&fanart=' + urllib.quote_plus(fanart)

    liz = xbmcgui.ListItem(label, iconImage=thumbnail, thumbnailImage=thumbnail)

    if desc:
        infolabels['plot'] = desc

    if len(infolabels) > 0:
        liz.setInfo(type='Video', infoLabels=infolabels)
   
    liz.setProperty('Fanart_Image', fanart)

    if menu:
        liz.addContextMenuItems(menu, replaceItems=True)

    #xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder, totalItems=totalItems)

'''
def get_params(p):
    param=[]
    paramstring=p
    if len(paramstring)>=2:
        params=p
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
           params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param


params = get_params(sys.argv[2])
'''

doRefresh   = False
cacheToDisc = True


try:    mode = int(params['mode'])
except: mode = _MAIN

try:    id = urllib.unquote_plus(params['id'])
except: id = ''


if mode == _MAIN:
    #main()
    getSkinList(id)

if mode == _ADDSKINSLIST:
    getSkinList(id)

if mode == _GETSKINS:
    label = urllib.unquote_plus(params['label'])
    url   = urllib.unquote_plus(params['id'])
    getSkin(label, url)

'''
if mode == _ADDLOGOSLIST:
    getLogosList(id)


if mode == _GETLOGOS:
    label = urllib.unquote_plus(params['label'])
    url   = urllib.unquote_plus(params['id'])

    getLogos(label, url)
'''

'''
if doRefresh:
    refresh()
'''
xbmcplugin.setContent(int(sys.argv[1]), 'movies')
xbmc.executebuiltin('Container.SetViewMode(%d)' % 515)
xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=cacheToDisc)


