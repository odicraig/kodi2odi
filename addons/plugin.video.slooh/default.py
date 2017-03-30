# -*- coding: utf-8 -*-
# GQ XBMC Addon

import sys
import httplib

import urllib, urllib2, cookielib, datetime, time, re, os, string
import xbmcplugin, xbmcgui, xbmcaddon, xbmcvfs, xbmc
import cgi, gzip
from StringIO import StringIO


USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'
GENRE_TV  = "TV"
UTF8          = 'utf-8'
MAX_PER_PAGE  = 25
SLOOHBASE = 'http://events.slooh.com/'

addon         = xbmcaddon.Addon('plugin.video.slooh')
__addonname__ = addon.getAddonInfo('name')
__language__  = addon.getLocalizedString


home          = addon.getAddonInfo('path').decode(UTF8)
icon          = xbmc.translatePath(os.path.join(home, 'icon.png'))
addonfanart   = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))


def log(txt):
    message = '%s: %s' % (__addonname__, txt.encode('ascii', 'ignore'))
    xbmc.log(msg=message, level=xbmc.LOGDEBUG)

def cleanfilename(name):    
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in name if c in valid_chars)

def demunge(munge):
        try:
            munge = urllib.unquote_plus(munge).decode(UTF8)
        except:
            pass
        return munge

def dexml(stuff):
    return str(stuff).replace('&amp;','&').replace('&#39;',"'").replace('&quot;','"')

def getRequest(url):
              log("getRequest URL:"+str(url))
              headers = {'User-Agent':USER_AGENT, 'Accept':"text/html", 'Accept-Encoding':'gzip,deflate,sdch', 'Accept-Language':'en-US,en;q=0.8'} 
              req = urllib2.Request(url.encode(UTF8), None, headers)

              try:
                 response = urllib2.urlopen(req)
                 if response.info().getheader('Content-Encoding') == 'gzip':
                    log("Content Encoding == gzip")
                    buf = StringIO( response.read())
                    f = gzip.GzipFile(fileobj=buf)
                    link1 = f.read()
                 else:
                    link1=response.read()
              except:
                 link1 = ""

              link1 = str(link1).replace('\n','')
              return(link1)


def getSources(fanart):
              urlbase = SLOOHBASE
              pg      = getRequest(urlbase)
              cats    = re.compile('<div class="eventInfo">.+?src="(.+?)".+?"title">(.+?)<.+?<p>(.+?)</p>.+?class="ts">(.+?)<.+?href="(.+?)"').findall(pg)
              for caticon, catname, catdesc, timeband, caturl in cats:
                 caturl = 'plugin://plugin.video.slooh/?mode=GC&url=%s##%s' % (caturl, urllib.quote_plus(timeband))
                 addLink(caturl.encode(UTF8), catname, icon, caticon, catdesc, GENRE_TV, '')

              cats    = re.compile('<div class="item-list">      <h3>(.+?)</h3>').findall(pg)
              for caturl in cats:
                 addDir(caturl.encode(UTF8), caturl, 'GA', icon, addonfanart, caturl, GENRE_TV, '', False)


def getCategories(url):
              urlbase = SLOOHBASE
              pg      = getRequest(urlbase)
              blob    = re.compile('<h3>%s</h3>(.+?)</ul></div>' % (url)).findall(pg)[0]
              cats    = re.compile('class="ytImage">.+?href="(.+?)".+?src="(.+?)".+?class="ytTitle">(.+?)<.+?class="ytDesc">(.+?)<').findall(blob)
              for caturl, catimage, catname, catdesc in cats:
                  caturl = 'plugin://plugin.video.slooh/?mode=GC&url=%s' % (caturl)
                  addLink(caturl,catname,catimage,addonfanart,catdesc,GENRE_TV,'',False)

def getCats(cat_url):
           if '##' in cat_url:
                (cat_url, timeband) = cat_url.split('##',1)
                timeband = urllib.unquote_plus(timeband)
                (starttime, endtime) = timeband.split(' to ',1)
                starttime = float(starttime)+15*60
                if float(time.time()) < float(starttime):
                   dialog = xbmcgui.Dialog()
                   timestr = __language__(30001)+time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime(float(starttime)))
                   dialog.ok(__language__(30000), '',timestr)
                   return

           urlbase   = SLOOHBASE+cat_url
           pg = getRequest(urlbase)
           videoid = re.compile('www.youtube-nocookie.com/embed/(.+?)\?wmode').findall(pg)[0]
           url = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=%s' % (videoid)
           xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=url))
             

def play_playlist(name, list):
        playlist = xbmc.PlayList(1)
        playlist.clear()
        item = 0
        for i in list:
            item += 1
            info = xbmcgui.ListItem('%s) %s' %(str(item),name))
            playlist.add(i, info)
        xbmc.executebuiltin('playlist.playoffset(video,0)')


def addDir(name,url,mode,iconimage,fanart,description,genre,date,showcontext=True,playlist=None,autoplay=False):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+mode
        dir_playable = False
        cm = []

        if mode != 'SR':
            u += "&name="+urllib.quote_plus(name)
            if (fanart is None) or fanart == '': fanart = addonfanart
            u += "&fanart="+urllib.quote_plus(fanart)
            dir_image = "DefaultFolder.png"
            dir_folder = True
        else:
            dir_image = "DefaultVideo.png"
            dir_folder = False
            dir_playable = True

        ok=True
        liz=xbmcgui.ListItem(name, iconImage=dir_image, thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description, "Genre": genre, "Year": date } )
        liz.setProperty( "Fanart_Image", fanart )

        if dir_playable == True:
         liz.setProperty('IsPlayable', 'true')
        if not playlist is None:
            playlist_name = name.split(') ')[1]
            cm.append(('Play '+playlist_name+' PlayList','XBMC.RunPlugin(%s?mode=PP&name=%s&playlist=%s)' %(sys.argv[0], playlist_name, urllib.quote_plus(str(playlist).replace(',','|')))))
        liz.addContextMenuItems(cm)
        return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=dir_folder)

def addLink(url,name,iconimage,fanart,description,genre,date,showcontext=True,playlist=None, autoplay=False):
        return addDir(name,url,'SR',iconimage,fanart,description,genre,date,showcontext,playlist,autoplay)



# MAIN EVENT PROCESSING STARTS HERE

xbmcplugin.setContent(int(sys.argv[1]), 'movies')

parms = {}
try:
    parms = dict( arg.split( "=" ) for arg in ((sys.argv[2][1:]).split( "&" )) )
    for key in parms:  parms[key] = demunge(parms[key])
except:
    parms = {}

p = parms.get

mode = p('mode',None)

if mode==  None:  getSources(p('fanart'))
elif mode=='SR':  xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=p('url')))
elif mode=='PP':  play_playlist(p('name'), p('playlist'))
elif mode=='GA':  getCategories(p('url'))
elif mode=='GC':  getCats(p('url'))

xbmcplugin.endOfDirectory(int(sys.argv[1]))

