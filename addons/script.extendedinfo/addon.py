# -*- coding: utf-8 -*-

import json
import os
import re
import requests
import urllib
import urllib2
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
from resources.lib.Utils import *

def AlternateAddonMovie():
    option = ADDON.getSetting('AlternateAddonMovie')
    if option == '1Channel':
        return "plugin.video.1channel"
    elif option == 'Exodus':
        return "plugin.video.exodus"
#    elif option == 'Genesis':
#        return "plugin.video.genesis"
    elif option == 'iSearch':
        return "plugin.program.super.favourites"
    elif option == 'iSTREAM':
        return "script.icechannel"
    elif option == 'Online Movies Pro':
        return "video.onlinemovies"
    elif option == 'Phoenix':
        return "plugin.video.phstreams"
    elif option == 'Pulsar':
        return "plugin.video.pulsar"
    elif option == 'Quasar':
        return "plugin.video.quasar"
    elif option == 'SALTS':
        return "plugin.video.salts"
    elif option == 'Salts HD Lite':
        return "plugin.video.saltshd.lite"
    elif option == 'Salts RD Lite':
        return "plugin.video.saltsrd.lite"
    elif option == 'Specto':
        return "plugin.video.specto"
    elif option == 'The Royal We':
        return "plugin.video.theroyalwe"
    elif option == 'UMP':
        return "plugin.program.ump"
    elif option == 'What the Furk':
        return "plugin.video.whatthefurk"
    elif option == 'Yify Movies HD':
        return "plugin.video.yifymovies.hd"
    elif option == 'Trailer':
        return "script.extendedinfo"
    else:
        return "plugin.program.super.favourites"

def AlternateAddonTVShow():
    option = ADDON.getSetting('AlternateAddonTVShow')
    if option == '1Channel':
        return "plugin.video.1channel"
    elif option == 'Exodus':
        return "plugin.video.exodus"
#    elif option == 'Genesis':
#        return "plugin.video.genesis"
    elif option == 'iSearch':
        return "plugin.program.super.favourites"
    elif option == 'iSTREAM':
        return "script.icechannel"
    elif option == 'Phoenix':
        return "plugin.video.phstreams"
    elif option == 'Pulsar':
        return "plugin.video.pulsar"
    elif option == 'Quasar':
        return "plugin.video.quasar"
    elif option == 'SALTS':
        return "plugin.video.salts"
    elif option == 'Salts HD Lite':
        return "plugin.video.saltshd.lite"
    elif option == 'Salts RD Lite':
        return "plugin.video.saltsrd.lite"
    elif option == 'Specto':
        return "plugin.video.specto"
    elif option == 'The Royal We':
        return "plugin.video.theroyalwe"
    elif option == 'TV4ME':
        return "plugin.video.tv4me"
    elif option == 'UMP':
        return "plugin.program.ump"
    elif option == 'What the Furk':
        return "plugin.video.whatthefurk"
    elif option == 'Trailer':
        return "script.extendedinfo"
    else:
        return "plugin.program.super.favourites"

def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def create_file(dir_path, file_name=None):
    if file_name:
        file_path = os.path.join(dir_path, file_name)
    file_path = file_path.strip()
    if not os.path.exists(file_path):
        f = open(file_path, 'w')
        f.write('')
        f.close()
    return file_path

ADDON = xbmcaddon.Addon(id='script.extendedinfo')
DATA_PATH = create_directory(os.path.join(xbmc.translatePath('special://profile/addon_data'), ''),'script.extendedinfo')
TRAKT_ID_PATH = create_file(DATA_PATH, "trakt_ids.list")
ONECH_URL_PATH = create_file(DATA_PATH, "1channel_urls.list")
TV4ME_URL_PATH = create_file(DATA_PATH, "tv4me_urls.list")
YIFY_URL_PATH = create_file(DATA_PATH, "yify_urls.list")
OMP_URL_PATH = create_file(DATA_PATH, "omp_urls.list")
AUTO_ALTERNATE_MOVIE=ADDON.getSetting('AutoPlayAlternateMovie')
ALTERNATE_MOVIE_ADDON=AlternateAddonMovie()
AUTO_ALTERNATE_TVSHOW=ADDON.getSetting('AutoPlayAlternateTVShow')
ALTERNATE_TVSHOW_ADDON=AlternateAddonTVShow()
xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
dialog = xbmcgui.Dialog()

traktapi='e9a7fba3fa1b527c08c073770869c258804124c5d7c984ce77206e695fbaddd5'
def get_trakt(query,db_type):
    traktid="na"
    if os.path.isfile(TRAKT_ID_PATH):
        s = read_from_file(TRAKT_ID_PATH)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                type = list1[0]
                name = list1[1]
                trakt = list1[4]
                if name==query and type==db_type:
                    traktid=trakt
    if traktid=="na": 
        header_dict = {}
        header_dict['Content-Type'] = 'application/json'
        header_dict['trakt-api-key'] = traktapi
        header_dict['trakt-api-version'] = '2'
        if query.startswith('tt'):
            url = 'http://api-v2launch.trakt.tv/search?id_type=imdb&id=%s' % (query)
        else:
            if db_type=='episode':
                url = 'http://api-v2launch.trakt.tv/search?query=%s&type=show' % (query)
            else:
                url = 'http://api-v2launch.trakt.tv/search?query=%s&type=movie' % (query)
        req=requests.get(url,headers=header_dict).content
        data=json.loads(req)
        traktid=[]
        for i in data:
            try:
                traktname = i['show']['title']
                title = traktname.encode('utf-8')
                year = i['show']['year']
                tmdb_id = i['show']['ids']['tmdb']
                tvdb_id = i['show']['ids']['tvdb']
                trakt_id = i['show']['ids']['trakt']
                if query.startswith('tt'):
                    imdb_id = query
                else:
                    imdb_id = i['show']['ids']['imdb']
                tvrage_id = i['show']['ids']['tvrage']
                slug = i['show']['ids']['slug']
            except:
                traktname = i['movie']['title']
                title = traktname.encode('utf-8')
                year = i['movie']['year']
                tmdb_id = i['movie']['ids']['tmdb']
                if query.startswith('tt'):
                    imdb_id = query
                else:
                    imdb_id = i['movie']['ids']['imdb']
                tvdb_id = "na"
                slug = i['movie']['ids']['slug']
                trakt_id = i['movie']['ids']['trakt']
                tvrage_id = "na"
        text="%s<>%s<>%s<>%s<>%s<>%s<>%s<>%s" % (db_type, title, imdb_id, year, trakt_id, tmdb_id, tvdb_id, tvrage_id)
        add_to_list(text,TRAKT_ID_PATH)
    return trakt_id

def get_tmdb(query,db_type):
    tmdbid="na"
    if os.path.isfile(TRAKT_ID_PATH):
        s = read_from_file(TRAKT_ID_PATH)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                type = list1[0]
                name = list1[1]
                tmdb = list1[5]
                if name==query and type==db_type:
                    tmdbid=tmdb
    if tmdbid=="na": 
        header_dict = {}
        header_dict['Content-Type'] = 'application/json'
        header_dict['trakt-api-key'] = traktapi
        header_dict['trakt-api-version'] = '2'
        if query.startswith('tt'):
            url = 'http://api-v2launch.trakt.tv/search?id_type=imdb&id=%s' % (query)
        else:
            if db_type=='episode':
                url = 'http://api-v2launch.trakt.tv/search?query=%s&type=show' % (query)
            else:
                url = 'http://api-v2launch.trakt.tv/search?query=%s&type=movie' % (query)
        req=requests.get(url,headers=header_dict).content
        data=json.loads(req)
        tmdbid=[]
        for i in data:
            try:
                traktname = i['show']['title']
                title = traktname.encode('utf-8')
                year = i['show']['year']
                tmdb_id = i['show']['ids']['tmdb']
                tvdb_id = i['show']['ids']['tvdb']
                trakt_id = i['show']['ids']['trakt']
                if query.startswith('tt'):
                    imdb_id = query
                else:
                    imdb_id = i['show']['ids']['imdb']                
                tvrage_id = i['show']['ids']['tvrage']
                slug = i['show']['ids']['slug']
            except:
                traktname = i['movie']['title']
                title = traktname.encode('utf-8')
                year = i['movie']['year']
                tmdb_id = i['movie']['ids']['tmdb']
                if query.startswith('tt'):
                    imdb_id = query
                else:
                    imdb_id = i['movie']['ids']['imdb']    
                tvdb_id = "na"
                slug = i['movie']['ids']['slug']
                trakt_id = i['movie']['ids']['trakt']            
                tvrage_id = "na"
        text="%s<>%s<>%s<>%s<>%s<>%s<>%s<>%s" % (db_type, title, imdb_id, year, trakt_id, tmdb_id, tvdb_id, tvrage_id)
        add_to_list(text,TRAKT_ID_PATH)
    return tmdb_id

def get_1channel_url(title):
    urlreturn="na"
    if os.path.isfile(ONECH_URL_PATH):
        s = read_from_file(ONECH_URL_PATH)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                name = list1[0]
                url = list1[1]
                if name==title:
                    urlreturn=url
    if urlreturn=="na":
        url='http://www.primewire.ag/'
        link = requests.get(url).content
        key=regex_from_to(link,'"hidden" name="key" value="', '"')
        url='http://www.primewire.ag/index.php?search_keywords=%s&key=%s&search_section=1' % (title,key)
        link = requests.get(url).content
        if db_type=='episode':
            urlreturn=regex_from_to(link,'index_item index_item_ie"><a href="','"').replace('-online-free','').replace('watch-','tv-')
        elif db_type=='movie':
            urlreturn=regex_from_to(link,'index_item index_item_ie"><a href="','"').replace('-online-free','')
        text="%s<>%s<>%s" % (title,urlreturn,db_type)
        add_to_list(text,ONECH_URL_PATH)
    return urlreturn

def get_tv4me_url(query,season,episode):
    urlreturn="na"
    if os.path.isfile(TV4ME_URL_PATH):
        s = read_from_file(TV4ME_URL_PATH)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                name = list1[0]
                url = list1[1]
                if name==query:
                    showurl=url
    if urlreturn=="na":
        url='http://www.watch-tvseries.net/play/menulist'
        link = requests.get(url).content
        match = re.compile("<li><a href='(.+?)'>(.+?)</a></li>").findall(link)
        for url, title in match:
            if query.lower() in title.lower():
                if not 'http://www.watch-tvseries.net' in url:
                    showurl='http://www.watch-tvseries.net' + url
                    text="%s<>%s" % (query,showurl)
                    add_to_list(text,TV4ME_URL_PATH)
    link = requests.get(showurl).content
    episodes = re.compile('<a title="(.+?)" href="(.+?)"> <div class="(.+?)data-original="(.+?)"(.+?)nseasnumep"> (.+?) <br(.+?)>(.+?) </div> </div> </a>').findall(link)
    for epname, url, a, thumb, b, snum, c, epnum in episodes:
        epnum = int(epnum.replace('episode ', ''))
        snum = int(snum.replace('season ', ''))
        if str(snum)==str(season) and str(epnum)==str(episode):
            urlreturn = 'http://www.watch-tvseries.net' + url
    return urlreturn

def get_yify_url(title,year):
    urlreturn="na"
    if os.path.isfile(YIFY_URL_PATH):
        s = read_from_file(YIFY_URL_PATH)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                name = list1[0]
                yr = list1[1]
                url = list1[2]
                if name==title and yr==year:
                    urlreturn=url
    if urlreturn=="na":
        url='http://yify.tv/?s=%s' % title
        link = requests.get(url).content
        data=regex_from_to(link,'<h1>Watch Movies Online</h1>','<div class')
        match=re.compile('<a href="(.+?)">Watch (.+?) Online</a>').findall(data)
        for u,qt in match:
            t=qt[:-5]
            y=qt[-4:]
            if t.lower()==title.lower() and y==year:
                urlreturn=u
                text="%s<>%s<>%s" % (title,year,urlreturn)
                add_to_list(text,YIFY_URL_PATH)
    return urlreturn

def get_omp_url(title,year):
    import urlresolver
    urlreturn="na"
    if os.path.isfile(OMP_URL_PATH):
        s = read_from_file(OMP_URL_PATH)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                name = list1[0]
                yr = list1[1]
                url = list1[2]
                if name==title and yr==year:
                    urlresolve=url
                    link = requests.get(urlresolve).content.replace("'",'"')
                    data=regex_from_to(link,'<div class="video-embed">','</div>')
                    url=regex_from_to(data,'src="','" allowFullScreen></iframe>')
                    urlreturn=urlresolver.resolve(url)
    if urlreturn=="na":
        url='http://onlinemovies.pro/?s=%s' % title
        link = requests.get(url).content
        data=regex_from_to(link,'<ul class="listing-videos listing-tube">','</ul>')
        match=re.compile('<a href="(.+?)" title="(.+?)"><span>(.+?)</span></a>').findall(data)
        for u,qt,qt1 in match:
            if ' (' in qt:
                t=qt.split(' (')[0]
                y=qt.split(' (')[1].replace(')','')
            else:
                t=qt
                y='na'
                year='na'
            if title.lower() in t.lower() and y==year:
                urlresolve=u
                text="%s<>%s<>%s" % (title,year,urlresolve)
                link = requests.get(urlresolve).content.replace("'",'"')
                data=regex_from_to(link,'<div class="video-embed">','</div>')
                url=regex_from_to(data,'src="','" allowFullScreen></iframe>')
                urlreturn=urlresolver.resolve(url) 
                add_to_list(text,OMP_URL_PATH)
    return urlreturn

def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
        r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
    else:
        r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
    return r

def regex_get_all(text, start_with, end_with):
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r

def find_list(query, search_file):
    try:
        content = read_from_file(search_file) 
        lines = content.split('\n')
        index = lines.index(query)
        return index
    except:
        return -1

def add_to_list(list, file):
    if find_list(list, file) >= 0:
        return

    if os.path.isfile(file):
        content = read_from_file(file)
    else:
        content = ""

    lines = content.split('\n')
    s = '%s\n' % list
    for line in lines:
        if len(line) > 0:
            s = s + line + '\n'
    write_to_file(file, s)

def write_to_file(path, content, append=False, silent=False):
    try:
        if append:
            f = open(path, 'a')
        else:
            f = open(path, 'w')
        f.write(content)
        f.close()
        return True
    except:
        if not silent:
            print(LANG(32192) + path)
        return False

def read_from_file(path, silent=False):
    try:
        f = open(path, 'r')
        r = f.read()
        f.close()
        return str(r)
    except:
        if not silent:
            print(LANG(32193) + path)
        return None

def alt_play(select_addon, db_type, iconimage, stream_file,viddetail):
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    #Open stream_file
    f = xbmcvfs.File(stream_file, 'r')
    r = f.read()
    f.close()
    currentaddon=regex_from_to(r,'','/')
    try:currenttvdb=regex_from_to(r,'tvdb=','&')
    except:currenttvdb=""
    try:currentimdb=regex_from_to(r,'imdb=','&')
    except:currentimdb=""
    try:currenttmdb=regex_from_to(r,'tmdb=','&')
    except:currenttmdb=""
    try:currenttvrage=regex_from_to(r,'tvrage=','&')
    except:currenttvrage=""
    alter='0'
    date=''
    vsplit=viddetail.split('<>')
    title=vsplit[0]
    if db_type=='episode':
        SE = "S%.2dE%.2d" % (int(vsplit[1]), int(vsplit[2]))
    if currentaddon==select_addon:
        xbmcPlayer.play(stream_file)
    elif db_type == 'episode' and select_addon == 'plugin.program.super.favourites' and ADDON.getSetting("CustomIsearchShow") == "true":
        xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.program.super.favourites/?label=ShowSearch&mode=400&path=special://home/addons/script.extendedinfo/resources/extras/tv/",return)')
    elif db_type == 'episode' and select_addon == 'plugin.program.super.favourites' and ADDON.getSetting("CustomIsearchShow") == "false":
        xbmc.executebuiltin('ActivateWindow(%d,"plugin://%s/?mode=%d&keyword=%s",return)' % (10025,'plugin.program.super.favourites', 0, urllib.quote_plus(title)))
    elif db_type == 'movie' and select_addon == 'plugin.program.super.favourites' and ADDON.getSetting("CustomIsearchMovie") == "true":
        xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.program.super.favourites/?label=MovieSearch&mode=400&path=special://home/addons/script.extendedinfo/resources/extras/movie/",return)')
    elif db_type == 'movie' and select_addon == 'plugin.program.super.favourites' and ADDON.getSetting("CustomIsearchMovie") == "false":
        xbmc.executebuiltin('ActivateWindow(%d,"plugin://%s/?mode=%d&keyword=%s",return)' % (10025,'plugin.program.super.favourites', 0, urllib.quote_plus(title)))
    elif select_addon == 'plugin.video.phstreams':
        if db_type == 'movie':
            xbmc.executebuiltin('ActivateWindow(%s,"plugin://%s/?action=addSearch&url=%s",return)' % (10025, 'plugin.video.phstreams',  urllib.quote_plus(title))
    else:
        data = "%s<>%s<>%s<>%s<>%s<>%s<>%s" % (viddetail,currenttvdb,currentimdb,currenttvrage,currenttmdb,alter,date)
        url=get_url(select_addon,db_type,data,iconimage)
        if url == ' not found':
            dialog.ok(LANG(32194), LANG(32195) % (title, select_addon), LANG(32196))
            return
        elif select_addon == 'plugin.program.ump':
            xbmc.executebuiltin('RunPlugin('+url+')')
        else:
            playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
            playlist.clear()
            listitem = xbmcgui.ListItem(title, iconImage=iconimage, thumbnailImage=iconimage,path=url)
            playlist.add(url,listitem)
            xbmcPlayer.play(playlist)

def get_url(select_addon,db_type,data,iconimage):
    dsplit=data.split('<>')
    if db_type=='episode':
        SE = "S%.2dE%.2d" % (int(dsplit[1]), int(dsplit[2]))
    rootname=urllib.quote(dsplit[0] + ' ' + dsplit[5])
    if db_type == 'movie':
        if select_addon=='plugin.video.1channel':
            try:
                u=get_1channel_url(dsplit[0])
                url='plugin://plugin.video.1channel/?img=%s&title=%s&url=%s&imdbnum=&video_type=movie&mode=GetSources&dialog=1&year=%s' % (urllib.quote(iconimage),dsplit[0],urllib.quote(u),dsplit[5])
            except:
                url='not found'
        if select_addon == 'plugin.video.exodus':
            url='plugin://plugin.video.exodus/?action=play&title=%s&year=%s&imdb=%s&tmdb=%s&meta=' % (urllib.quote_plus(title), year, imdb, tmdb)
#        if select_addon == 'plugin.video.genesis':
#            url='plugin://plugin.video.genesis/?action=play&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s' % (urllib.quote_plus(dsplit[0] + ' ' + dsplit[5]), urllib.quote_plus(title), year, imdb, tmdb)
        if select_addon == 'script.icechannel':
            url='plugin://script.icechannel/?&name=%s&title=%s&item_title=%s&video_type=movie&indexer=movies&imdb_id=%s&mode=file_hosts&url=%s&year=%s&item_mode=file_hosts&type=movies&library=true' % (urllib.quote_plus(dsplit[0] + " "), urllib.quote_plus(dsplit[0] + " (" + year + ")"), urllib.quote_plus(dsplit[0] + " (" + year + ")"), imdb, urllib.quote_plus("http://imdb.com/title/" + imdb), year)
        if select_addon=='plugin.video.onlinemovies':
            url=get_omp_url(dsplit[0],dsplit[5])
            print url
        if select_addon == 'plugin.video.pulsar':
            url = "plugin://plugin.video.pulsar/movie/%s/%s" % (urllib.quote(imdb), ADDON.getSetting("PulsarModeMovie"))
        if select_addon == 'plugin.video.quasar':
            url = "plugin://plugin.video.quasar/movie/%s/%s" % (tmdb, ADDON.getSetting("PulsarModeMovie"))
        if select_addon == 'plugin.video.salts':
            url='plugin://plugin.video.salts/?title=%s&video_type=Movie&trakt_id=%s&mode=get_sources&dialog=True&year=%s' % (urllib.quote_plus(dsplit[0]), trakt, year)
        if select_addon == 'plugin.video.saltshd.lite':
            url='plugin://plugin.video.saltshd.lite/?title=%s&video_type=Movie&trakt_id=%s&mode=get_sources&dialog=True&year=%s' % (urllib.quote_plus(dsplit[0]), trakt, year)
        if select_addon == 'plugin.video.saltsrd.lite':
            url='plugin://plugin.video.saltsrd.lite/?title=%s&video_type=Movie&trakt_id=%s&mode=get_sources&dialog=True&year=%s' % (urllib.quote_plus(dsplit[0]), trakt, year)
        if select_addon == 'plugin.video.specto':
            url='plugin://plugin.video.specto/?action=play&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s' % (urllib.quote_plus(dsplit[0] + ' ' + dsplit[5]), urllib.quote_plus(title), year, imdb, tmdb)
        if select_addon == 'plugin.video.theroyalwe':
            url = "plugin://plugin.video.theroyalwe/?title=%s&year=%s&mode=play_movie&tmdb_id=%s&imdb_id=%s" % (urllib.quote_plus(title), year, tmdb, imdb)
        if select_addon == 'plugin.program.ump':
            url='plugin://plugin.program.ump/?info=%%7B%%22status%%22%%3A+%%22%%22%%2C+%%22rating%%22%%3A+%%22%%22%%2C+%%22plotoutline%%22%%3A+%%22%%22%%2C+%%22code%%22%%3A+%%22%s%%22%%2C+%%22tagline%%22%%3A+%%22%%22%%2C+%%22season%%22%%3A+-1%%2C+%%22tvshowtitle%%22%%3A+%%22%%22%%2C+%%22artist%%22%%3A+%%5B%%5D%%2C+%%22aired%%22%%3A+%%22%%22%%2C+%%22tvshowalias%%22%%3A+%%22%%22%%2C+%%22director%%22%%3A+%%22%%22%%2C+%%22duration%%22%%3A+%%22%%22%%2C+%%22localtitle%%22%%3A+%%22%s%%22%%2C+%%22studio%%22%%3A+%%22%%22%%2C+%%22year%%22%%3A+%s%%2C+%%22genre%%22%%3A+%%22%%22%%2C+%%22tracknumber%%22%%3A+-1%%2C+%%22lastplayed%%22%%3A+%%22%%22%%2C+%%22album%%22%%3A+%%22%%22%%2C+%%22alternates%%22%%3A+%%5B%%22%%22%%5D%%2C+%%22count%%22%%3A+1%%2C+%%22plot%%22%%3A+%%22%%22%%2C+%%22votes%%22%%3A+%%22%%22%%2C+%%22castandrole%%22%%3A+%%5B%%22%%22%%5D%%2C+%%22episode%%22%%3A+-1%%2C+%%22overlay%%22%%3A+0%%2C+%%22credits%%22%%3A+%%22%%22%%2C+%%22mpaa%%22%%3A+%%22%%22%%2C+%%22title%%22%%3A+%%22%s%%22%%2C+%%22premiered%%22%%3A+%%22%%22%%2C+%%22originaltitle%%22%%3A+%%22%s%%22%%2C+%%22cast%%22%%3A+%%5B%%22%%22%%5D%%2C+%%22write%%22%%3A+%%22%%22%%2C+%%22sorttitle%%22%%3A+%%22%%22%%2C+%%22playcount%%22%%3A+-1%%2C+%%22size%%22%%3A+0%%2C+%%22top250%%22%%3A+-1%%2C+%%22trailer%%22%%3A+%%22%%22%%2C+%%22dateadded%%22%%3A+%%22%%22%%7D&art=%%7B%%22thumb%%22%%3A+%%22%%22%%2C+%%22fanart%%22%%3A+%%22%%22%%2C+%%22poster%%22%%3A+%%22%%22%%2C+%%22clearlogo%%22%%3A+%%22%%22%%2C+%%22landscape%%22%%3A+%%22%%22%%2C+%%22banner%%22%%3A+%%22%%22%%2C+%%22clearart%%22%%3A+%%22%%22%%7D&args=%%7B%%7D&module=imdb&content_type=video&page=urlselect' % (imdb, dsplit[0], int(year), dsplit[0], dsplit[0])
        if select_addon == 'plugin.video.whatthefurk':
            url='plugin://plugin.video.whatthefurk/?name=%s&url=imdb&mode=1100&iconimage=%s&rootname=%s&imdb=%s&videotype=movies' % (rootname,urllib.quote(iconimage),rootname,imdb)
        if select_addon=='plugin.video.yifymovies.hd':
            try:
                u=get_yify_url(dsplit[0],dsplit[5])
                url='plugin://plugin.video.yifymovies.hd/?action=play&name=%s&url=%s' % (urllib.quote_plus(dsplit[0] + ' (' + dsplit[5] + ')'),urllib.quote(u))
            except:
                url='not found'
        if select_addon == 'script.extendedinfo':
            url='plugin://script.extendedinfo/?info=playtrailer&&id=%s' % tmdb
    elif db_type == 'episode':
        if select_addon=='plugin.video.1channel':
            try:
                u=get_1channel_url(dsplit[0])
                url='plugin://plugin.video.1channel/?img=&imdbnum=&url=%s/season-%s-episode-%s&title=%s&video_type=episode&mode=GetSources&dialog=1' % (urllib.quote(u),dsplit[1],dsplit[2],urllib.quote(dsplit[0]))
            except:
                url='not found'
        if select_addon == 'plugin.video.exodus':
            url='plugin://plugin.video.exodus/?action=play&title=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&tvshowtitle=%s&premiered=&meta=' % (urllib.quote_plus(epname), year, imdb, tvdb, dsplit[1], dsplit[2], urllib.quote_plus(title)) 
#        if select_addon == 'plugin.video.genesis':
#            gtitle="%s %s" % (dsplit[0],SE)
#            url='plugin://plugin.video.exodus/?action=play&title=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&tvshowtitle=%s&premiered=&meta=' % (urllib.quote_plus(epname), year, imdb, tvdb, dsplit[1], dsplit[2], urllib.quote_plus(title)) 
        if select_addon == 'script.icechannel':
            url = "plugin://script.icechannel/?episode=%s&name=%s&title&season=%s&section=&indexer=tv_shows&library=true&imdb_id=%s&video_type=episode&url=%s&year=%s&type=tv_episodes&mode=file_hosts" % (dsplit[2], urllib.quote_plus(dsplit[0]), dsplit[2], urllib.quote(imdb), urllib.quote_plus("http://imdb.com/title/" + imdb), urllib.quote(year))
        if select_addon == "plugin.video.pulsar":
            url = "plugin://plugin.video.pulsar/show/%s/season/%s/episode/%s/%s" % (tmdb, dsplit[1], dsplit[2], ADDON.getSetting("PulsarModeTVShow"))
        if select_addon == "plugin.video.quasar":
            url = "plugin://plugin.video.quasar/show/%s/season/%s/episode/%s/%s" % (tmdb, dsplit[1], dsplit[2], ADDON.getSetting("PulsarModeTVShow"))
        if select_addon == 'plugin.video.salts':
            url='plugin://plugin.video.salts/?ep_airdate=1980-02-23&trakt_id=%s&episode=%s&mode=get_sources&dialog=True&title=%s&ep_title=%s&season=%s&year=%s&video_type=Episode' % (trakt,dsplit[2],urllib.quote_plus(dsplit[0]),urllib.quote_plus(dsplit[3]),dsplit[1],year)
        if select_addon == 'plugin.video.saltshd.lite':
            url='plugin://plugin.video.saltshd.lite/?ep_airdate=1980-02-23&trakt_id=%s&episode=%s&mode=get_sources&dialog=True&title=%s&ep_title=%s&season=%s&year=%s&video_type=Episode' % (trakt,dsplit[2],urllib.quote_plus(dsplit[0]),urllib.quote_plus(dsplit[3]),dsplit[1],year)
        if select_addon == 'plugin.video.saltsrd.lite':
            url='plugin://plugin.video.saltsrd.lite/?ep_airdate=1980-02-23&trakt_id=%s&episode=%s&mode=get_sources&dialog=True&title=%s&ep_title=%s&season=%s&year=%s&video_type=Episode' % (trakt,dsplit[2],urllib.quote_plus(dsplit[0]),urllib.quote_plus(dsplit[3]),dsplit[1],year)
        if select_addon == 'plugin.video.specto':
            gtitle="%s %s" % (dsplit[0],SE)
            url='plugin://plugin.video.specto/?action=play&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s&tvdb=%s&tvrage=%s&season=%s&episode=%s&tvshowtitle=%s&alter=0&date=' % (urllib.quote_plus(gtitle),urllib.quote_plus(epname), year, imdb, tmdb, tvdb, tvrage, dsplit[1], dsplit[2], urllib.quote_plus(dsplit[0]))
        if select_addon == 'plugin.video.theroyalwe':
            url = "plugin://plugin.video.theroyalwe/?trakt_id=%s&episode=%s&mode=play_episode&tmdb_id=%s&year=%s&season=%s&display=%s&showtitle=%s&imdb_id=%s" % (trakt, dsplit[2], tmdb, year, dsplit[1], urllib.quote_plus(dsplit[2] + '. ' + urllib.quote_plus(epname)), urllib.quote_plus(dsplit[0]), imdb)
        if select_addon == 'plugin.video.tv4me':
            gtitle="%s %s" % (dsplit[0],SE)#
            tv4meurl=get_tv4me_url(dsplit[0],int(dsplit[1]),int(dsplit[2]))
            url='plugin://plugin.video.tv4me/?name=%s&url=%s&mode=5&iconimage=%s&showname=%s' % (urllib.quote(gtitle),urllib.quote(tv4meurl),urllib.quote(iconimage),urllib.quote(dsplit[0]))
        if select_addon == 'plugin.program.ump':
            url='plugin://plugin.program.ump/?info=%%7B%%22rating%%22%%3A+%%22%%22%%2C+%%22aired%%22%%3A+%%22%%22%%2C+%%22code%%22%%3A+%%22%s%%22%%2C+%%22Language%%22%%3A+%%22%s%%22%%2C+%%22EpisodeNumber%%22%%3A+%s%%2C+%%22season%%22%%3A+%s%%2C+%%22tvshowtitle%%22%%3A+%%22%s%%22%%2C+%%22code2%%22%%3A+%%22%s%%22%%2C+%%22director%%22%%3A+%%22%%22%%2C+%%22localtitle%%22%%3A+%%22%s%%22%%2C+%%22studio%%22%%3A+%%22%%22%%2C+%%22year%%22%%3A+%s%%2C+%%22genre%%22%%3A+%%22%%22%%2C+%%22episode%%22%%3A+%s%%2C+%%22code10%%22%%3A+%%22%%22%%2C+%%22alternates%%22%%3A+%%5B%%22%%22%%5D%%2C+%%22GuestStars%%22%%3A+%%22%%22%%2C+%%22plot%%22%%3A+%%22%%22%%2C+%%22votes%%22%%3A+%%22%%22%%2C+%%22dateadded%%22%%3A+%%22%%22%%2C+%%22SeasonNumber%%22%%3A+%s%%2C+%%22title%%22%%3A+%%22%s%%22%%2C+%%22mpaa%%22%%3A+%%22%%22%%2C+%%22writer%%22%%3A+%%22%%7C%%7C%%22%%2C+%%22originaltitle%%22%%3A+%%22%s%%22%%2C+%%22cast%%22%%3A+%%5B%%22%%22%%5D%%2C+%%22absolute_number%%22%%3A+%%22%%22%%2C+%%22EpImgFlag%%22%%3A+2%%7D&art=%%7B%%22thumb%%22%%3A+%%22%%22%%2C+%%22fanart%%22%%3A+%%22%%22%%2C+%%22poster%%22%%3A+%%22%%22%%2C+%%22clearlogo%%22%%3A+%%22%%22%%2C+%%22landscape%%22%%3A+%%22%%22%%2C+%%22banner%%22%%3A+%%22%%22%%2C+%%22clearart%%22%%3A+%%22%%22%%7D&args=%%7B%%7D&module=tvdb&content_type=video&page=urlselect' % (imdb, SETTING("LanguageID"), dsplit[2], dsplit[1], dsplit[0], tvdb, dsplit[0], int(year), dsplit[2], dsplit[1], dsplit[3], dsplit[0])
        if select_addon == 'plugin.video.whatthefurk':#(
            data = '%s<|>%s<|>%s<|>%s' % (dsplit[0], dsplit[3], dsplit[1], dsplit[2])
            url='plugin://plugin.video.whatthefurk/?name=%s&url=%s&mode=1100&iconimage=%s&rootname=%s&imdb=%s&videotype=tvshows' % (urllib.quote(SE + ' ' + dsplit[3]),urllib.quote(data),urllib.quote(dsplit[0] + ' (' + dsplit[5] + ')'),urllib.quote(dsplit[0]),dsplit[7])
        if select_addon == 'script.extendedinfo':
            url='plugin://script.extendedinfo/?info=playtvtrailer&&id=%s' % tmdb
    return url

def get_file_age(file_path):
    try:    
        stat = os.stat(file_path)
        fileage = datetime.fromtimestamp(stat.st_mtime)
        now = datetime.now()
        delta = now - fileage
        return delta.seconds
    except:
        return -1

if __name__ == '__main__':
    db_type = xbmc.getInfoLabel('ListItem.DBTYPE')
    addon_list_return=[]
    addon_list=[]
    count=-1
    if db_type=='movie':
        al = ["1Channel", "Exodus", "iSearch", "iSTREAM", "Online Movies Pro", "Phoenix", "Pulsar", "Quasar", "SALTS", "Salts HD Lite", "Salts RD Lite", "Specto", "The Royal We", "UMP", "What the Furk", "Yify Movies HD", "Trailer"]
        alr = ["plugin.video.1channel", "plugin.video.exodus", "plugin.program.super.favourites", "script.icechannel", "plugin.video.onlinemovies", "plugin.video.phstreams", "plugin.video.pulsar", "plugin.video.quasar", "plugin.video.salts", "plugin.video.saltshd.lite", "plugin.video.saltsrd.lite", "plugin.video.specto", "plugin.video.theroyalwe", "plugin.program.ump", "plugin.video.whatthefurk", "plugin.video.yifymovies.hd", "script.extendedinfo"]
        title = xbmc.getInfoLabel('ListItem.Title')
        season = "na"
        epnumber = "na"
        epname = "na"
        imdb = xbmc.getInfoLabel('ListItem.IMDBNumber')
        year = xbmc.getInfoLabel('ListItem.Year')
        iconimage = xbmc.getInfoLabel('ListItem.Art(poster)')
        fanart = xbmc.getInfoLabel('ListItem.Art(fanart)')
        dbid = xbmc.getInfoLabel('ListItem.DBID')
        from resources.lib.TheMovieDB import get_movie_tmdb_id
        from resources.lib.Trakt import get_movie_info
        tmdb = get_movie_tmdb_id(imdb)
        traktids = get_movie_info(imdb)
        trakt = traktids['ids']['trakt']
        tvdb = "na"
        tvrage = "na"
    else:
        al = ["1Channel", "Exodus", "iSearch", "iSTREAM", "Pulsar", "Quasar", "SALTS", "Salts HD Lite", "Salts RD Lite", "Specto", "The Royal We", "TV4ME", "UMP", "What the Furk", "Trailer"]
        alr = ["plugin.video.1channel", "plugin.video.exodus", "plugin.program.super.favourites", "script.icechannel", "plugin.video.pulsar", "plugin.video.quasar", "plugin.video.salts", "plugin.video.saltshd.lite", "plugin.video.saltsrd.lite", "plugin.video.specto", "plugin.video.theroyalwe", "plugin.video.tv4me", "plugin.program.ump", "plugin.video.whatthefurk", "script.extendedinfo"]
        title = xbmc.getInfoLabel('ListItem.TVShowTitle')
        season = xbmc.getInfoLabel('ListItem.Season')
        epnumber = xbmc.getInfoLabel('ListItem.Episode')
        epname = xbmc.getInfoLabel('ListItem.Title')
        year = xbmc.getInfoLabel('ListItem.Year')
        iconimage = xbmc.getInfoLabel('ListItem.Art(tvshow.poster)')
        fanart = xbmc.getInfoLabel('ListItem.Art(fanart)')
        dbid = xbmc.getInfoLabel('ListItem.DBID')
        from resources.lib.local_db import get_tvshow_id_from_db_by_episode
        from resources.lib.TheMovieDB import get_show_tmdb_id, get_tvshow_ids
        from resources.lib.Trakt import get_tshow_info_max
        tvdb = get_tvshow_id_from_db_by_episode(dbid)
        tmdb = get_show_tmdb_id(tvdb)
        tmdbids = get_tvshow_ids(tmdb)
        imdb = tmdbids['imdb_id']
        tvrage = tmdbids['tvrage_id']
        traktids = get_tshow_info_max(imdb)
        trakt = traktids['ids']['trakt']
    viddetail="%s<>%s<>%s<>%s<>%s<>%s<>%s<>%s<>%s<>%s<>%s" % (title,season,epnumber,epname,imdb,year,dbid,tmdb,trakt,tvdb,tvrage)
    stream_file = xbmc.getInfoLabel('ListItem.FileNameAndPath')
    for a in alr:
        count+=1
        if xbmc.getCondVisibility("system.hasaddon(%s)" % a):
            addon_list_return.append(a)
            addon_list.append(al[count])
    if db_type=='movie' and AUTO_ALTERNATE_MOVIE=='true':
        if ALTERNATE_MOVIE_ADDON in addon_list_return:
            addon_id=1
            select_addon = ALTERNATE_MOVIE_ADDON
        else:
            addon_id = dialog.select(LANG(32186), addon_list)
            select_addon = addon_list_return[addon_id]
    elif db_type=='episode' and AUTO_ALTERNATE_TVSHOW=='true':
        if ALTERNATE_TVSHOW_ADDON in addon_list_return:
            addon_id=1
            select_addon = ALTERNATE_TVSHOW_ADDON
        else:
            addon_id = dialog.select(LANG(32186), addon_list)
            select_addon = addon_list_return[addon_id]
        print select_addon
    else:
        addon_id = dialog.select(LANG(32186), addon_list)
        select_addon = addon_list_return[addon_id]
    if addon_id > -1:
        alt_play(select_addon, db_type, iconimage, stream_file,viddetail)