# -*- coding: utf-8 -*-
# Vortex 2016

import os,re,sys,urllib,urllib2,xbmcplugin,xbmcgui,xbmcaddon,xbmc,urlparse,cookielib,base64
from resources.lib.modules import client
from resources.lib.modules import cloudflare
from resources.lib.modules import control
from resources.lib.modules import cache
from resources.lib.modules.net import Net as net
import requests
thisPlugin = int(sys.argv[1])
base_url = sys.argv[0]
args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', None)
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
ADDON = xbmcaddon.Addon(id='plugin.video.Vortex')
path = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.Vortex/'))
usdata=xbmc.translatePath(os.path.join('special://userdata/addon_data/plugin.video.Vortex/'))
mediaPath = path +"resources/media/"
fanart = 'https://s5.postimg.org/y8p45nmrr/fanart.png'
icon = (path + 'icon.png')
pager = '1'
plot = None
cj = cookielib.LWPCookieJar()
cookiepath = (usdata+'cookies.lwp')
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1')]

def TEST():
    return 

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)
        
def choose():

    try:
        onetime = OPEN_URL(english('Vm10V1UxUXhVblJWYmxKVVlrZJsV20aN1G9UMVl3V21GVU1WcHhVVzVLYkZadGVEQlViR2hyVkcxS1NHVkdjRlpXYkVwUVdWUkdTbVF5UlhwYVJsWlRVbFp3TWxaclpEUlZNVXB6VjI1T2FWSnRVbFJaVkU1RFVrWmFSbGw2Um1sTmJFcEpWVEowVjFWR1pFaGxSMFpYVFVkU1QxUnNXbmRTYlVaR1pFVTFWMkpyU2xSV1ZWcFNaREZDVWxCVU1EMD0vVm0wd2QyUXlWa2hWV0doVlYwZDRWMVl3Wkc5V2JHeDBaRWhrVmxKc2NEQlVWbU0xVmpBeFdHVkVRbHBOTTBKSVdWZDRZV014WkhWalJtaG9UVlZ3VlZkV1ZtRlRNazE0V2toV2FWSnRVbkJWYlhSM1UxWmtWMWt6YUZSTlZUVllWVzAxVDJGR1NuUlZiR2hWVmtWd2RscFdXbXRXTVd0NllVWlNUbFpVVmtwV2JHUXdWakZaZVZOclpGaGlSMmhZV1d4b1UwMHhXWGhYYlhSWFRWWmFlVlV5TVRSVk1rcFhVMnR3VjJKVVJYZFdha1pYWkVaT2NscEdhR2hsYlhoWlYxZDRiMVV3TUhoWGJrNVlZbFZhY1ZsclpGTk5SbkJHVjJ4T1ZXSkdjREZWVjNCWFZqRkplbUZIYUZkaGExcG9WVEJhVDJOdFNrZFRiV3hvVFVoQ1dWWXhaREJaVjFGNFYxaG9WbUpIVWxsWmJGWmhWMFpzY2xwR1RteFdiR3cxV2xWV1QxWXdNWEpXYWs1YVRVWndWRlpxUm1GV01rNUhWRzFHVTFKV2NFVldiR1EwVVRGYVZrMVZWazVTUkVFNQ=='))
        NEWWINDOW(onetime)
    except:
        NEWWINDOW(onetime)
    xbmcplugin.endOfDirectory(thisPlugin)
    
def NEWWINDOW(onetime):
    
    stuff = re.compile('<window>(.+?)</window><base>(.+?)</base><thumbnail>(.+?)</thumbnail>').findall(str(onetime))
    for name, base, thumb in stuff:
        try:
            test = english(base)
            if str(test) != "None":
                base = str(test)
            else:
                pass
        except:
            pass
        
        if not ('http') in base and not base == " ":
            url = build_url({'mode': str(base), 'icon': thumb})
        else:
            url =build_url({'mode': 'XML', 'name':name, 'base': str(base)})        
        li = xbmcgui.ListItem('[B]'+name+'[/B]',iconImage=thumb)
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=thisPlugin,url=url,
                                   listitem=li, isFolder=True)
    return
def english(final):
    try:
        x = "MlVPdKNBjIuHvGtF1ocXdEasWZaSeFbNyRtHmJ"
        y =":/."
        fget = x[-1]+x[-11].lower()+x[2]
        rget = x[-12]+x[6]+x[16] 
        this = fget+'.+?'+rget
        getter = re.findall(this,final)[0]
        stage = int(final.index(getter))/5
        work = base64.b64decode(str(final.replace(getter,''))).split('/')
        Solve = True
        S = 1
        while Solve is True:        
            if S<= stage*2:first = base64.b64decode(work[1])
            if S<= stage:sec = base64.b64decode(work[0])
            S = S + 1
            if not S<= stage*2 and not S<= stage: Solve = False
            work =[sec,first]
        answ = work[1]+work[0]
        if answ.startswith (x[-5].lower()+x[-10]):
            begin = (x[-3].lower()+(x[-4]*2)+x[3].lower()+y[0:2]+y[1]+x[7].lower())
            ender = (x[-10]+x[-5].lower())
            killit = (x[-5].lower()+x[-10]+x[-4]+x[-12].lower()+x[-5].lower()+x[4]+x[-11].lower()+x[-3].lower())
            mid = y[2]+x[1]+x[-6]
            url = answ.replace(killit,begin).replace(ender,mid)
        elif answ.startswith ('rtmp') or answ.startswith ('rtsp') or answ.startswith ('plugin'):url = answ
        elif answ.startswith (x[-3].lower()+(x[-4]*2)):url = answ
        elif answ.startswith (x[13].lower()+(x[17]*2)+x[4]):
            killit = (x[13].lower()+(x[17]*2)+x[4])
            begin = (x[-3].lower()+(x[-4]*2)+x[3].lower()+x[-15]+y[0:2]+y[1])
            url = answ.replace(killit,begin)
        else:
            pass
        url = url.replace('/{3,}','//').replace('  ',' ').encode('utf-8')
        return url
        
    except:
        return None

    
def OPEN_URL(url,headers=False):
    req = urllib2.Request(url)
    if headers:            
        req.add_header('User-Agent',headers['User-Agent'])
        req.add_header('Referer', headers['Referer'])
        req.add_header('Accept', headers['Accept'])
    else:
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    onetime=response.read()
    response.close()
    onetime = onetime.replace('\n','').replace('\r','')  
    return onetime

def addDirItem(title,icon,fanart,url):
    listitem =xbmcgui.ListItem (title,'','',thumbnailImage=icon)
    listitem.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url,
                                listitem=listitem)
def endDir():
    xbmcplugin.endOfDirectory(thisPlugin)
    
def TIMESHIFT():
    from datetime import datetime
    sitetime = int(datetime.utcnow().time().hour)+2
    localt = int(datetime.now().time().hour)
    diff = sitetime - localt
    return diff

if mode is None:
    choose()

elif mode[0] == "XML":
    name = args['name'][0]   
    base = args['base'][0]
    onetime = OPEN_URL(base)
    try:
        fanart = re.findall('<fanart>(.+?)</fanart>',str(onetime))[0]
    except:
        pass
    if ('<window>') in str(onetime):NEWWINDOW(onetime)
    stuff = re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(str(onetime))
    
    for title, url, icon in stuff:
        if not ('http') in url and not ('plugin') in url and not ('rtmp') in url and not ('rstp') in url and not ('base64') in url and len(url) > 2:
            url = english(url)
        if ('base64') in url:
            url = base64.b64decode(url[8:-1])    
        if ('youtube') in url and not 'plugin' in url:
            url = build_url({'mode': 'YouTube', 'name':title, 'icon':icon, 'url':url})
        if ('p2pcast') in url:
            url = build_url({'mode': 'P2P', 'name':title, 'icon':icon, 'url':url})
        if ('t-tv.org') in url:
            url = build_url({'mode': 'acestream', 'name':title, 'icon':icon, 'url':url})
        if ('mail.ru') in url:
            url = build_url({'mode': 'MAILRU', 'name':title, 'icon':icon, 'url':url})
        if ('thechive.com') in url:
            url = build_url({'mode': 'THECHIVE', 'name':title, 'icon':icon, 'url':url})
        if ('redbull.com') in url:
            url = build_url({'mode': 'REDBULL', 'name':title, 'icon':icon, 'url':url})
        if ('sublink') in url:
            links = re.findall('<sublink>(.+?)</sublink>',str(url))
            for item in links:
                url = item
                addDirItem(title,icon,fanart,url)        
        else:
            try:
                url = urlresolver.HostedMediaFile(url).resolve()
                addDirItem(title,icon,fanart,url)
            except:
                pass
        addDirItem(title,icon,fanart,url)    
    endDir()
    
elif mode[0] =="YouTube":
    url = args['url'][0]
    name = args['name'][0]
    thumbnailImage = args['icon'][0]
    try:
        try:
            url = 'plugin://plugin.video.youtube/play/?video_id=' + str(url.split('v=')[1])
        except:
            url = xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id='+ url.split('v=')[1]+')')
            pass
    except:
        pass
    listitem =xbmcgui.ListItem(name, '','',thumbnailImage)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(url, listitem)

elif mode[0] == "REDBULL":
    url = args['url'][0]
    Name = args['name'][0]
    thumbnailImage = args['icon'][0]
    link=OPEN_URL(url)
    vid_id= re.findall("data-video-id='([^']+)'",link)
    if vid_id:
        vid_id= vid_id[0]
        account= re.findall("data-account='([^']+)'",link)[0]
        url2='https://edge.api.brightcove.com/playback/v1/accounts/'+account+'/videos/'+vid_id
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36','Referer':url,'Accept':'application/json;pk=BCpkADawqM04GwfHVvRSv5kMqi1EoG_1z5mEyoDfMLer8s8rVN7jmoshU1T2q6oix3bMPtZBvpZeXjx6nPXxU5YsbnPRo9ghJKq7sIdVzHdxwMXJJUFgwsZXZBZPv0yle1JS341r7VHAEFL_'}
        link=OPEN_URL(url2,headers=headers)
        import json
        data=json.loads(link)
        data=data["id"]
        stream='http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId='+data
        listitem =xbmcgui.ListItem (Name,'','',thumbnailImage)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(stream,listitem)
    vid_you=re.findall("""href='(http://www.youtube.com.+?)'""",link)
    if vid_you:
        match=re.findall('''http://www.youtube.com/v/(.+?)\?''',vid_you[0])[0]
        xbmc.log('chekit1 '+str(match))
        try:
            stream = 'plugin://plugin.video.youtube/play/?video_id=' + str(match)
        except:
            stream = xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id='+ match.split('?feature')[1]+')')
            pass
        listitem =xbmcgui.ListItem (Name,'','',thumbnailImage)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(stream,listitem)
    
elif mode[0] == "MAILRU":
    url = args['url'][0]
    Name = args['name'][0]
    thumbnailImage = args['icon'][0]
    from resources.lib.resolvers import mailru
    stream = mailru.resolve(url)
    listitem =xbmcgui.ListItem (Name,'','',thumbnailImage)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(stream,listitem)

elif mode[0] == "THECHIVE":
    url = args['url'][0]
    Name = args['name'][0]
    thumbnailImage = args['icon'][0]
    link=OPEN_URL(url)
    match=re.search('''<meta name="twitter:player" content="https://cdnapi.kaltura.com/p/(.+?)/sp/(.+?)/embedIframeJs/uiconf_id/.+?/partner_id/.+?iframeembed=true&amp;playerId=kaltura_player_.+?&amp;entry_id=(.+?)" />''',link)
    if match:
        p=match.group(1)
        sp=match.group(2)
        entryId=match.group(3)
        stream = 'http://cdnapi.kaltura.com/p/'+p+'/sp/'+sp+'/playManifest/entryId/'+entryId+'/format/applehttp/protocol/http/a.m3u8'
    else:
        match=re.findall('''src="https://www.youtube.com/embed/(.+?)"''',link)[0]
        try:
            stream = 'plugin://plugin.video.youtube/play/?video_id=' + str(match.split('?feature')[0])
        except:
            stream = xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id='+ match.split('?feature')[1]+')')
            pass
    xbmc.log('HDH '+str(match))
    listitem =xbmcgui.ListItem (Name,'','',thumbnailImage)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(stream,listitem)

elif mode[0] == "P2P":
    url = args['url'][0]
    Name = args['name'][0]
    thumbnailImage = args['icon'][0]
    from resources.lib.resolvers import p2pcast
    stream = p2pcast.resolve(url)
    listitem =xbmcgui.ListItem (Name,'','',thumbnailImage)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(stream,listitem) 
    
elif mode[0]=="acestream":
    url = args['url'][0]
    name = args['name'][0].upper()
    thumbnailImage = args['icon'][0]
    req = client.request(url)
    url = re.findall("var id = '(acestream://.+?)'",str(req))[0]
    url = str(url)+'&name='+str(name).replace(' ','+').encode('utf-8')
    url = xbmc.executebuiltin('PlayMedia(plugin://program.plexus/?mode=1&url='+str(url)+')')
