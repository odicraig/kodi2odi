import urllib,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os
import urlresolver
import requests
from addon.common.addon import Addon
from addon.common.net import Net


#We Love Soaps - By Mucky Duck (09/2015)

addon_id='plugin.video.welovesoaps'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
Addon = xbmcaddon.Addon(addon_id)
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
baseurl500 = 'http://hdsoapcity.blogspot.co.uk'
baseurl510 = 'http://uksoapshare.blogspot.co.uk'
baseurl520 = 'http://www.livehangama.com'
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'




def CAT():
        link = OPEN_URL(baseurl520)
        all_links = regex_get_all(link, 'data-toggle="dropdown">Soap Operas', '</nav>')
        match=re.compile('<li id="nav-menu-item-.*?".*?><a href="(.*?)" class="menu-link  sub-menu-link">(.*?)</a></li>').findall(str(all_links))
        for url, name in match:
                thumb = name.rstrip()
                thumb = thumb.replace(' ','-').lower()
                iconimage = art + thumb + '-LiveHangama.png'
                addDir('[COLOR white]%s[/COLOR]' %name,url,520,iconimage,fanart,'')
        addDir('[COLOR white]General Hospital[/COLOR]',url+'/category/general-hospital/',520,art+'general-hospital-LiveHangama.png',fanart,'')
        #addDir('[COLOR white]Soap City[/COLOR]',baseurl500,500,icon,fanart,'')
        #addDir('[COLOR white]UK Soap Share[/COLOR]',baseurl510,510,icon,fanart,'')
        xbmc.executebuiltin("Container.SetViewMode(500)")




def BASE500(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile("<a dir='ltr' href='(.+?)'>(.+?)</a>").findall(link)
        for url, name in match:
                if 'Days' not in name:
                        name =name.replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"')
                        iconimage = art+name+'.jpg'
                        addDir('[COLOR white]%s[/COLOR]' %name,url,501,iconimage,fanart,'')
        xbmc.executebuiltin("Container.SetViewMode(500)")



def BASE500INDEX(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, '<div style="text-align: left;">', '</h2>')
        for a in all_videos:
                name = regex_from_to(a, "<a href='.+?'>", "</a>").replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#8230;','...')
                name = name.replace('&#8211;','-').replace('&#8212;','--').replace("&#8217;","'").replace('&#8220;','"').replace('&#8221;','"')
                name = name.replace('Watch Online','').replace('HD','')
                url = regex_from_to(a, '<iframe .+?src="', '"></iframe>').replace("&amp;","&")
                iconimage = regex_from_to(a, '<img .+?src="', '"').replace("&amp;","&")
                addDir('[COLOR white]%s[/COLOR]' %name,url,1,iconimage,fanart,'')
        try:
                nextp=re.compile("<a class='blog-pager-older-link' href='(.+?)'").findall(link)[0]
                addDir('[COLOR cyan]Next Page>>>[/COLOR]',nextp,501,icon,fanart,'')
        except: pass
        xbmc.executebuiltin("Container.SetViewMode(500)")




def BASE510(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile("<a dir='ltr' href='(.+?)'>(.+?)</a>").findall(link)
        for url, name in match:
                name = name.replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"')
                try:
                        link = OPEN_URL(url)
                        icon = re.compile("<meta content=\'(.+?)\' itemprop=\'image_url\'/>\n<meta content=\'.+?\' itemprop=\'blogId\'/>").findall(link)[0] 
                        addDir('[COLOR white]%s[/COLOR]' %name,url,511,icon,fanart,'')
                except: pass




def BASE510L(url,iconimage):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore').decode('ascii')
        match=re.compile('<a href="(.+?)" target=.*?>(.+?)</a>').findall(link)
        for url, name in match:
                name = name.replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"')
                name = name.replace('.x264','').replace('-SS.mp4','')
                if  'tusfiles' in url:
                        link = OPEN_URL(url)
                        match=re.compile('\|image\|video\|(.*?)\|').findall(link)[0]
                        url = 'https://r.tusfiles.net/d/'+match+'/video.mp4'
                        addDir('[COLOR white]%s[/COLOR]' %name,url,1,iconimage,fanart,'')
                elif  'hugefiles' in url:
                        addDir('[COLOR white]%s[/COLOR]' %name,url,1,iconimage,fanart,'')
        try:
                nextp=re.compile("<a class='blog-pager-older-link' href='(.+?)'").findall(link)[0]
                addDir('[COLOR cyan]Next Page>>>[/COLOR]',nextp,511,art+'wls.png',fanart,'')
        except: pass




def BASE520(name,url):
        name = name.replace('[COLOR white]','').replace('[/COLOR]','')
        link = OPEN_URL(url)
        all_links = regex_get_all(link, 'div class="video-listing-content.*?">', '</div><div class="row"></div></div>')
        all_videos = regex_get_all(str(all_links), 'video-item post', '"clearfix"')
        for a in all_videos:
                name2 = regex_from_to(a, 'title="', '"').replace(" Full Episode","")
                url = regex_from_to(a, 'href="', '"')
                iconimage = regex_from_to(a, 'src="', '"')
                if iconimage == '':
                        thumb = name.rstrip()
                        thumb = thumb.replace(' ','-').lower()
                        iconimage = art + thumb + '-LiveHangama.png'
                addDir('[COLOR white]%s[/COLOR]' %name2,url,521,iconimage,fanart,'')
        try:
                nextp=re.compile('<a href="(.*?)" >Older posts <span class="meta-nav">&rarr;</span></a></div>').findall(link)[0]
                addDir('[COLOR cyan]GoTo Next Page>>>[/COLOR]',nextp,520,icon,fanart,'')
        except: pass
        xbmc.executebuiltin("Container.SetViewMode(500)")




def BASE520L(url,iconimage):
        link = OPEN_URL(url)
        match = re.findall(r'<ifram.*?rc="(.*?)" .*?>', str(link), re.I|re.DOTALL)[0]
        if 'http' not in match:
                match = 'http:' + match
        if 'dailymotion' in match:
                try:
                        link2 = OPEN_URL(match)
                        try:
                                url = re.compile('"video\\\/mp4","url":"(.*?)"',re.DOTALL).findall(link2)[-1]
                        except:
                                url = re.compile('"video\\\/mp4","url":"(.*?)"',re.DOTALL).findall(link2)[0]
                        url = url.replace('\/','/')
                except:
                        url = urlresolver.resolve(match)
        else:
                url = urlresolver.resolve(match)
        liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={"Title":name,"Plot":description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)





def regex_from_to(text, from_string, to_string, excluding=True):
        if excluding:
                try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
                except: r = ''
        else:
                try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
                except: r = ''
        return r




def regex_get_all(text, start_with, end_with):
        r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
        return r            




def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
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




def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
        liz.setProperty('fanart_image', fanart)
        if mode==1 or mode ==521:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok



def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok




def OPEN_URL(url):
    headers = {}
    name = ''
    headers['User-Agent'] = User_Agent
    link = requests.get(url, headers=headers).text
    link = link.encode('ascii', 'ignore').decode('ascii')
    return link



def RESOLVE(name,url):
    url1 = urlresolver.resolve(url)
    if url1:
        try:
            liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
            liz.setInfo(type='Video', infoLabels={'Title':description})
            liz.setProperty("IsPlayable","true")
            liz.setPath(url1)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        except: pass
    else:
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)




def setView(content, viewType):
        ''' Why recode whats allready written and works well,
        Thanks go to Eldrado for it '''

        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        #if addon.get_setting('auto-view') == 'true':

        #    print addon.get_setting(viewType)
        #    if addon.get_setting(viewType) == 'Info':
        #        VT = '515'
        #    elif addon.get_setting(viewType) == 'Wall':
        #        VT = '501'
        #    elif viewType == 'default-view':
        #        VT = addon.get_setting(viewType)

        #    print viewType
        #    print VT
        
        #    xbmc.executebuiltin("Container.SetViewMode(%s)" % ( int(VT) ) )

        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )

           
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
site=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass
   
        
if mode==None or url==None or len(url)<1:
        CAT()

elif mode==1:
        RESOLVE(name,url)

elif mode==500:
        BASE500(url)

elif mode==501:
        BASE500INDEX(url)

elif mode==510:
        BASE510(url)

elif mode==511:
        BASE510L(url,iconimage)

elif mode==520:
        BASE520(name,url)

elif mode==521:
        BASE520L(url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
