# -*- coding: utf-8 -*-

'''
    Sanctuary Add-on
    Copyright (C) 2016 Origin

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
	
    Just don't be a nob about it....

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
	
    This addon could not of became what it is without the help and generosity of everyone involved.
    Not all of the coding is my original work but i have tried my best to utilise and learn from others.
    If i have used code that you wrote i can only apologise for not thanking you personally and ensure you no offence was meant.
    Just sometimes i find it best not to rewrite what works well, mostly to a higher standard that my current understanding
'''
import xbmcplugin, xbmc, xbmcaddon, urllib, xbmcgui, traceback, requests, re, os, base64
from lib import process
import os, shutil, xbmcgui
addon_id = 'plugin.video.sanctuary'
Dialog = xbmcgui.Dialog()
addons = xbmc.translatePath('special://home/addons/')
ADDON = xbmcaddon.Addon(id=addon_id)
ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.sanctuary/')
ICON = ADDON_PATH + 'icon.png'
ADDON = xbmcaddon.Addon(id=addon_id)
FANART = ADDON_PATH + 'fanart.jpg'
Adult_Pass = ADDON.getSetting('Adult')
Adult_Default = ADDON.getSetting('Porn_Pass')
base_icons = 'http://herovision.x10host.com/freeview/'
ORIGIN_ICON = base_icons + 'origin.png'
ORIGIN_FANART = base_icons + 'origin.jpg'
PANDORA_ICON = 'https://s32.postimg.org/ov9s6ipf9/icon.png'
RAIDER_ICON = base_icons + 'pyramid.png'
FREEVIEW_ICON = base_icons + 'freeview.png'
NINJA_ICON = base_icons + 'ninja2.png'
BRETTUS_ICON = base_icons + 'brettus_anime.png'
OBLIVION_ICON = base_icons + 'oblivion.png'
TIGEN_ICON = base_icons + 'Tigen.png'
COLD_ICON = base_icons + 'Cold.png'
BAMF_ICON = base_icons + 'BAMF.png'
RENEGADES_ICON = base_icons + 'renegades.png'
QUICK_ICON = base_icons + 'quick.png'
RAY_ICON = base_icons + 'raysraver.png'
SILENT_ICON = base_icons + 'silent.png'
REAPER_ICON = base_icons + 'reaper.png'
DOJO_ICON = base_icons + 'dojo.png'
ULTRA_ICON = base_icons + 'Ultra.png'
FIDO_ICON = base_icons + 'fido.png'
INTRO_VID = base_icons + 'Intro.mp4'
INTRO_VID_TEMP = xbmc.translatePath('special://home/addons/plugin.video.sanctuary/DELETE_ME')

def Main_Menu():
    if not os.path.exists(INTRO_VID_TEMP):
        if ADDON.getSetting('Intro_Vid')=='true':
            xbmc.Player().play(INTRO_VID, xbmcgui.ListItem('You have been updated'))
            os.makedirs(INTRO_VID_TEMP)
    process.Menu('Big Bag \'O\' Tricks','',13,'',FANART,'','')
    if ADDON.getSetting('Classic_View')=='true':
        process.Menu('Big Bag \'O\' Tricks','',13,'',FANART,'','')
        classic_list()
    else:
		process.Menu('24/7','',38,'',FANART,'','')
		process.Menu('Documentaries','',39,'',FANART,'','')
		process.Menu('Kids','',33,'',FANART,'','')
		process.Menu('Live TV','',32,'',FANART,'','')
		process.Menu('Movies','',30,'',FANART,'','')
		process.Menu('Music','',34,'',FANART,'','')
		process.Menu('Sports','',40,'',FANART,'','')
		process.Menu('TV Shows','',31,'',FANART,'','')
		if Adult_Pass == Adult_Default:
			process.Menu('Adult','',37,'',FANART,'','')
		process.Menu('Add-on\'s','',35,'',FANART,'','')
		process.setView('movies', 'INFO')
		
def twenty47():
	from lib.pyramid import pyramid
	process.Menu('Origin 24/7 Cartoons','',812,ORIGIN_ICON,FANART,'','')
	pyramid.not_so_anon('Fido 24/7','[QT][LW][PD][QZ][WI][PD][AL][DE][SS][MW][FU][XU][WX][UR][YY][YZ][PD][LS][LS][XU][QZ][YO][BU][PD][OI][MW][UP][YZ][LW][YO][LS][XU][WX][PD][LS][LS][XU][QZ][YZ][XX][XW]-[XB][RJ][KW][PD][QZ][QZ][MW][JJ][UP][YZ][XX][XW][XB][RJ][KW][PD][QZ][QZ][MW][JJ][UP]Hope you enjoy the view',FIDO_ICON,FANART,'','','')
	process.Menu('Pyramid 24/7','http://tombraiderbuilds.co.uk/addon/tvseries/247shows/247shows.txt',1101,RAIDER_ICON,'','','')
	process.Menu('Supremacy 24/7','http://stephen-builds.uk/supremacy/24-7/24-7.txt',1101,'http://www.stephen-builds.co.uk/wizard/icon.png','','','')
	process.Random_play('Raiz TV - Play 10 Random Cartoons',1154,url='http://raiztv.co.uk/RaysRavers/list2/raiztv/kids/kidsrandom.txt',image=RAY_ICON,isFolder=False)
	
def docs():
	process.Menu('Raiz Documentaries','http://raiztv.co.uk/RaysRavers/list2/raiztv/doc/doc.txt',1101,RAY_ICON,'','','')
	process.Menu('Pyramid Documentaries','http://tombraiderbuilds.co.uk/addon/documentaries/documentaries.txt',1101,RAY_ICON,'','','')
	
def sports():
	process.Menu('Renegades Darts','',2150,RENEGADES_ICON,FANART,'','')
	process.Menu('Origin Football Replays','',2150,ORIGIN_ICON,FANART,'','')
	process.Menu('Today\'s Football','',1750,ICON,FANART,'','')
		
def Adult():
	process.Menu('Just For Him','',1400,NINJA_ICON,FANART,'','')
	process.Menu('Origin','',700,ORIGIN_ICON,ORIGIN_FANART,'','')
	process.Menu('Fido','http://fantazyrepo.uk/addonimages/fido.addon/Livetv/adult.xml',1101,FIDO_ICON,'','','')


def Movie_Men():
	process.Menu('Search','Movies',1501,'','','','')
	process.Menu('Recent Movies','',5,ICON,FANART,'','')
	process.Menu('4k','4k',36,'','','','')
	process.Menu('3D','3D',36,'','','','')
	process.Menu('1080p','1080p',36,'','','','')
	process.Menu('Other - Linked to add-on\'s menu as most have movies','Other',36,'','','','')

def Movie_Def(url):
	if url == '4k':
		from lib.pyramid import pyramid
		pyramid.not_so_anon('Silent Hunter 4k','[QT][UP][YO][JJ][MW][QZ][WI][UP][WI][SS][MW][PD][BU][WX][UP][SS][FA][MW][WX][YO][XU][YZ][UP][YO][JJ][MW][QZ][WI][KW][UR][QZ][WI][MW][SS][YZ][BU][PD][YO][QZ][YZ][XW][YY]Hope you enjoy the view',SILENT_ICON,FANART,'','','')
		process.Menu('Pandora 4k','http://genietvcunts.co.uk/PansBox/ORIGINS/4Kmovies.php',426,PANDORA_ICON,'','','')
		process.Menu('Pyramid 4k','http://tombraiderbuilds.co.uk/addon/movies/uhd/uhd.txt',1101,RAIDER_ICON,'','','')
	elif url == '3D':
		process.Menu('Pandora 3D','http://genietvcunts.co.uk/PansBox/ORIGINS/hey3D.php',426,PANDORA_ICON,'','','')
		process.Menu('Pyramid 3D','http://tombraiderbuilds.co.uk/addon/movies/3d/3d.txt',1101,RAIDER_ICON,'','','')
	elif url == '1080p':
		process.Menu('Pandora 1080p','http://genietvcunts.co.uk/PansBox/ORIGINS/hey1080p.php',426,PANDORA_ICON,'','','')
	elif url == 'Other':
		classic_list()


def TV_Men():
	process.Menu('Search','TV',1501,'','','','')
	process.Menu('Latest Episodes','',3,ICON,FANART,'','')
	from lib.pyramid import pyramid
	process.Menu('Pandora\'s TV','http://genietvcunts.co.uk/PansBox/ORIGINS/tvcats.php',423,PANDORA_ICON,'','','')
	process.Menu('Cerberus TV','http://hellhound.info/cerberus/tvmenu.php',2301,REAPER_ICON,'','','')
	pyramid.not_so_anon('Pyramid TV','[QT][WI][XU][BU][ID][SS][PD][YO][LS][MW][SS][ID][UR][YO][JJ][LS][UP][WX][RJ][XU][WX][UR][YY][YZ][PD][LS][LS][XU][QZ][YZ][WI][FA][UP][MW][SS][YO][MW][UP][YZ][WI][FA][AL][XU][QZ][MW][BU][PD][YO][QZ]Have a nice day now',RAIDER_ICON,FANART,'','','')
	process.Menu('Tigen\'s TV','http://kodeeresurrection.com/TigensWorldtxt/TvShows/Txts/OnDemandSub.txt',1101,TIGEN_ICON,'','','')
	process.Menu('Raiz TV','http://raiztv.co.uk/RaysRavers/list2/raiztv/tv/tv.txt',1101,RAY_ICON,'','','')
	process.Menu('Dojo TV','http://herovision.x10host.com/dojo/tvshows/tvshows.php',2300,DOJO_ICON,'','','')

def Live_Men():
	process.Menu('Search','Live TV',1501,'','','','')
	process.Menu('TV Guide','',2200,ICON,FANART,'','')
	from lib.pyramid import pyramid
	process.Menu('Oblivion IPTV','',1129,OBLIVION_ICON,FANART,'','')
	process.Menu('BAMF IPTV','',1132,BAMF_ICON,FANART,'','')
	pyramid.not_so_anon('Pyramid Live','[QT][WI][XU][BU][ID][SS][PD][YO][LS][MW][SS][ID][UR][YO][JJ][LS][UP][WX][RJ][XU][WX][UR][YY][YZ][PD][LS][LS][XU][QZ][YZ][UR][YY][MW][QZ][WI][MW][SS][WI][PD][YO][QZ][BU][MW][QZ][WI][YZ][UR][YY][MW][QZ][WI][MW][SS][WI][PD][YO][QZ][BU][MW][QZ][WI]Have a nice day now',RAIDER_ICON,FANART,'','','')
	process.Menu('Ultra Live',base64.decodestring('aHR0cDovL3VsdHJhdHYubmV0MTYubmV0L2lwdHZzZXJ2ZXIvcG9ydGFsLnhtbA=='),1101,ULTRA_ICON,'','','')
	pyramid.not_so_anon('Fido Live','[QT][LW][PD][QZ][WI][PD][AL][DE][SS][MW][FU][XU][WX][UR][YY][YZ][PD][LS][LS][XU][QZ][YO][BU][PD][OI][MW][UP][YZ][LW][YO][LS][XU][WX][PD][LS][LS][XU][QZ][YZ]L[YO][FA][MW][WI][FA][YZ][JJ][YO][FA][MW][WI][FA]Hope you enjoy the view',FIDO_ICON,FANART,'','','')
	process.Menu('FreeView - [COLORred]VPN required if you are outside UK[/COLOR]','',1200,FREEVIEW_ICON,FANART,'','')
	process.Menu('Lily Sports Live','http://kodeeresurrection.com/LILYSPORTStxts/home.txt',1101,'http://kodeeresurrection.com/LILYSPORTS/plugin.video.LILYSPORTS/icon.png','','','')
	process.Menu('Supremacy Live','http://stephen-builds.uk/supremacy/LiveTV/live.txt',1101,'http://www.stephen-builds.co.uk/wizard/icon.png','','','')

def Kids_Men():
	process.Menu('Search','cartoon',1501,'','','','')
	from lib.pyramid import pyramid
	process.Menu('Tigen\'s World','',1143,TIGEN_ICON,FANART,'','')
	process.Menu('Raiz Kids','http://raiztv.co.uk/RaysRavers/list2/raiztv/kids/kidsmain.txt',1101,RAY_ICON,'','','')
	process.Menu('Origin Kids','',800,ORIGIN_ICON,ORIGIN_FANART,'','')
	pyramid.not_so_anon('Silent Hunter Kids','[QT][UP][YO][JJ][MW][QZ][WI][UP][WI][SS][MW][PD][BU][WX][UP][SS][FA][MW][WX][YO][XU][YZ][UP][YO][JJ][MW][QZ][WI][KW][UR][QZ][WI][MW][SS][YZ][BU][PD][YO][QZ][YZ][RJ][KW][YO][JJ][LS][SS][MW][QZ]Hope you enjoy the view',SILENT_ICON,FANART,'','','')
	process.Menu('Oblivion Kids','http://pastebin.com/raw/Y8X1vCaV',1101,OBLIVION_ICON,'','','')
	pyramid.not_so_anon('Pyramid Kids','[QT][WI][XU][BU][ID][SS][PD][YO][LS][MW][SS][ID][UR][YO][JJ][LS][UP][WX][RJ][XU][WX][UR][YY][YZ][PD][LS][LS][XU][QZ][YZ][YY][YO][LS][UP][RJ][KW][PD][QZ][QZ][MW][JJ][UP][YZ][YY][YO][LS][UP][RJ][KW][PD][QZ][QZ][MW][JJ][UP]Have a nice day now',RAIDER_ICON,FANART,'','','')
	process.Menu('BAMF Kids Live','http://genietvcunts.co.uk/bamffff/kids.m3u',1101,BAMF_ICON,'','','')
	process.Menu('Supremacy Kids Live','http://stephen-builds.uk/supremacy/Kids%20Tv/Kids%20Tv.txt',1101,'http://www.stephen-builds.co.uk/wizard/icon.png','','','')
	process.Menu('Brettus Anime','',1600,BRETTUS_ICON,FANART,'','')

	

def Music_Men():
	process.Menu('Search','',1503,'','','','')
	from lib.pyramid import pyramid
	process.Menu('Quicksilver Music','',1133,QUICK_ICON,'','','')
	process.Menu('Rays Ravers','',1147,RAY_ICON,'','','')
	pyramid.not_so_anon('Fido Live Music','[QT][LW][PD][QZ][WI][PD][AL][DE][SS][MW][FU][XU][WX][UR][YY][YZ][PD][LS][LS][XU][QZ][YO][BU][PD][OI][MW][UP][YZ][LW][YO][LS][XU][WX][PD][LS][LS][XU][QZ][YZ]M[UR][UP][YO][RJ][YZ]M[UR][UP][YO][RJ]Hope you enjoy the view',FIDO_ICON,FANART,'','','')
	process.Menu('Tigen\'s World','',1143,TIGEN_ICON,FANART,'','')
	pyramid.not_so_anon('Pyramid\'s Music','[QT][WI][XU][BU][ID][SS][PD][YO][LS][MW][SS][ID][UR][YO][JJ][LS][UP][WX][RJ][XU][WX][UR][YY][YZ][PD][LS][LS][XU][QZ][YZ][BU][UR][UP][YO][RJ][YZ][BU][UR][UP][YO][RJ]Have a nice day now',RAIDER_ICON,FANART,'','','')
	process.Menu('Pandora\'s Music','http://genietvcunts.co.uk/PansBox/ORIGINS/seasonmusic.php',423,PANDORA_ICON,'','','')

def classic_list():
		if ADDON.getSetting('Origin')=='true':
			process.Menu('Origin','',4,ORIGIN_ICON,FANART,'','')
		if ADDON.getSetting('Pandoras_Box')=='true':
			process.Menu('Pandora\'s Box','',900,PANDORA_ICON,FANART,'','')
		if ADDON.getSetting('Pyramid')=='true':
			process.Menu('Pyramid','',1100,RAIDER_ICON,FANART,'','')
		if ADDON.getSetting('Freeview')=='true':
			process.Menu('FreeView - [COLORred]VPN required if you are outside UK[/COLOR]','',1200,FREEVIEW_ICON,FANART,'','')
		if ADDON.getSetting('Brettus_Anime')=='true':
			process.Menu('Brettus Anime','',1600,BRETTUS_ICON,FANART,'','')
		if ADDON.getSetting('Oblivion')=='true':
			process.Menu('Oblivion IPTV','',1129,OBLIVION_ICON,FANART,'','')
		if ADDON.getSetting("Tigen's_World")=='true':
			process.Menu('Tigen\'s World','',1143,TIGEN_ICON,FANART,'','')
		if ADDON.getSetting('Cold_As_Ice')=='true':
			process.Menu('Cold As Ice','',1800,COLD_ICON,FANART,'','')
		if ADDON.getSetting('Supremacy')=='true':
			process.Menu('Supremacy','',1131,'http://www.stephen-builds.co.uk/wizard/icon.png',FANART,'','')
		if ADDON.getSetting('Renegades')=='true':
			process.Menu('Renegades Darts','',2150,RENEGADES_ICON,FANART,'','')
		if ADDON.getSetting('Just_For_Him')=='true':
			process.Menu('Just For Him','',1400,NINJA_ICON,FANART,'','')
		if ADDON.getSetting('BAMF')=='true':
			process.Menu('BAMF IPTV','',1132,BAMF_ICON,FANART,'','')
		if ADDON.getSetting('Quicksilver')=='true':
			process.Menu('Quicksilver Music','',1133,QUICK_ICON,'','','')
		if ADDON.getSetting('Rays_Ravers')=='true':
			process.Menu('Rays Ravers','',1147,RAY_ICON,'','','')
		if ADDON.getSetting('Silent_Hunter')=='true':
			process.Menu('Silent Hunter','',1134,SILENT_ICON,'','','')
		if ADDON.getSetting('Dojo')=='true':
			process.Menu('Dojo Streams','http://herovision.x10host.com/dojo/main.php',2300,DOJO_ICON,'','','')
		if ADDON.getSetting('Cerberus')=='true':
			process.Menu('Cerberus','http://hellhound.info/cerberus/mainmenu.php',2301,REAPER_ICON,'','','')
		if ADDON.getSetting('Ultra')=='true':
			process.Menu('Ultra IPTV','',1145,ULTRA_ICON,'','','')
		if ADDON.getSetting('Fido')=='true':
			process.Menu('Fido','',1146,FIDO_ICON,'','','')
		process.setView('movies', 'MAIN')
		

def bagotricks():
    if ADDON.getSetting('TV_Guide')=='true':
        process.Menu('TV Guide','',2200,ICON,FANART,'','')
    if ADDON.getSetting("Today's_Football")=='true':
        process.Menu('Today\'s Football','',1750,ICON,FANART,'','')
    if ADDON.getSetting('Latest_Episodes')=='true':
        process.Menu('Latest Episodes','',3,ICON,FANART,'','')
    if ADDON.getSetting('Recent_Movies')=='true':
        process.Menu('Recent Movies','',5,ICON,FANART,'','')
    if ADDON.getSetting('Favourites')=='true':
        process.Menu('Favourites','',10,base_icons + 'favs.png',FANART,'','')
    if ADDON.getSetting('Search')=='true':
        process.Menu('Search','',1500,base_icons + 'search.png',FANART,'','')
	
def DOJO_MAIN(url):
    OPEN = process.OPEN_URL(url)
    Regex = re.compile('<a href="(.+?)" target="_blank"><img src="(.+?)" style="max-width:200px;" /><description = "(.+?)" /><background = "(.+?)" </background></a><br><b>(.+?)</b>').findall(OPEN)
    for url,icon,desc,fanart,name in Regex:
        if 'php' in url:
            process.Menu(name,url,2300,icon,fanart,desc,'')
        else:
            process.Play(name,url,906,icon,fanart,desc,'')

    process.setView('tvshows', 'Media Info 3')			
		
def Reaper_Loop(url):
    OPEN = process.OPEN_URL(url)
    Regex = re.compile('<NAME>(.+?)</NAME><URL>(.+?)</URL><ICON>(.+?)</ICON><FANART>(.+?)</FANART><DESC>(.+?)</DESC>').findall(OPEN)
    for name,url,icon,fanart,desc in Regex:
        if 'Favourites' in name:
            pass
        elif 'Search' in name:
            pass
        elif 'php' in url:
            process.Menu(name,url,2301,icon,fanart,desc,'')
        else:
            process.Play(name,url,906,icon,fanart,desc,'')


def Latest_Episodes():
    process.Menu('Pandora Latest Episodes','http://genietvcunts.co.uk/PansBox/ORIGINS/recenttv.php',426,ICON,FANART,'','')
    process.Menu('TV Schedule','http://www.tvmaze.com/calendar',6,ICON,FANART,'','')

def Recent_Movies():
    process.Menu('Pandora Recent Movies','http://genietvcunts.co.uk/PansBox/ORIGINS/recentmovies.php',426,PANDORA_ICON,FANART,'','')
    process.Menu('Pyramid Recent Movies','http://tombraiderbuilds.co.uk/addon/movies/New%20Releaes/newreleases.txt',1101,RAIDER_ICON,FANART,'','')
    process.Menu('Supremacy Recent Movies','https://simplekore.com/wp-content/uploads/file-manager/steboy11/New%20Releases/New%20Releases.txt',1101,'http://www.stephen-builds.co.uk/wizard/icon.png',FANART,'','')


def TV_Calender_Day(url):
	from datetime import datetime
	today = datetime.now().strftime("%d")
	this_month = datetime.now().strftime("%m")
	this_year = datetime.now().strftime("%y")
	todays_number = (int(this_year)*100)+(int(this_month)*31)+(int(today))
	HTML = process.OPEN_URL(url)
	match = re.compile('<span class="dayofmonth">.+?<span class=".+?">(.+?)</span>(.+?)</span>(.+?)</div>',re.DOTALL).findall(HTML)
	for Day_Month,Date,Block in match:
		Date = Date.replace('\n','').replace('  ','').replace('	','')
		Day_Month = Day_Month.replace('\n','').replace('  ','').replace('	','')
		Final_Name = Day_Month.replace(',',' '+Date+' ')
		split_month = Day_Month+'>'
		Month_split = re.compile(', (.+?)>').findall(str(split_month))
		for item in Month_split:
			month_one = item.replace('January','1').replace('February','2').replace('March','3').replace('April','4').replace('May','5').replace('June','6')
			month = month_one.replace('July','7').replace('August','8').replace('September','9').replace('October','10').replace('November','11').replace('December','12')
		show_day = Date.replace('st','').replace('th','').replace('nd','').replace('rd','')
		shows_number = (int(this_year)*100)+(int(month)*31)+(int(show_day))
		if shows_number>= todays_number:
			process.Menu('[COLORred]*'+'[COLORwhite]'+Final_Name+'[/COLOR]','',7,'','','',Block)
		else:
			process.Menu('[COLORgreen]*'+'[COLORwhite]'+Final_Name+'[/COLOR]','',7,'','','',Block)

def TV_Calender_Prog(extra):
	match = re.compile('<span class="show">.+?<a href=".+?">(.+?)</a>:.+?</span>.+?<a href=".+?" title=".+?">(.+?)</a>',re.DOTALL).findall(str(extra))
	for prog, ep in match:
		process.Menu(prog+' - Season '+ep.replace('x',' Episode '),'',8,'','','',prog)

def send_to_search(name,extra):
	dp =  xbmcgui.DialogProgress()
	dp.create('Checking for stream')
	from lib import search
	search.TV(name)





def Origin_Main():
#    process.Menu('Movies','',200,ORIGIN_ICON,ORIGIN_FANART,'','')
 #   process.Menu('TV Shows','',300,ORIGIN_ICON,ORIGIN_FANART,'','')
    process.Menu('Live TV','',19,ORIGIN_ICON,ORIGIN_FANART,'','')
    process.Menu('Index Google Search','',2350,ORIGIN_ICON,ORIGIN_FANART,'','')
#    process.Menu('Comedy','',100,ORIGIN_ICON,ORIGIN_FANART,'','')
    process.Menu('Sports Replays','',2100,ORIGIN_ICON,ORIGIN_FANART,'','')
    process.Menu('Cartoons','',800,ORIGIN_ICON,ORIGIN_FANART,'','')
    process.Menu('Music','',2,ORIGIN_ICON,ORIGIN_FANART,'','')
    if Adult_Pass == Adult_Default:
        process.Menu('Porn','',700,ORIGIN_ICON,ORIGIN_FANART,'','')
		
def google_index_search():
    Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
    Search_name = Search_title.lower()
    if Search_name == '':
        pass
    else:
		html = requests.get('https://www.google.co.uk/search?q=%2B(.mkv%7C.mp4%7C.avi%7C.mov%7C.mpg%7C.wmv%7C.flv)%20+'+Search_name.replace(' ','+')+'++intitle:%22index+of%22+-inurl:(jsp%7Cpl%7Cphp%7Chtml%7Caspx%7Chtm%7Ccf%7Cshtml)+-inurl:(listen77%7Cmp3raid%7Cmp3toss%7Cmp3drug%7Cindex_of%7Cwallywashis)&gws_rd=cr&ei=DCR6WOPpDYvPgAa6kp24Dg').text
		match = re.compile('<a href="(.+?)"').findall(html)
		for url in match:
			if 'google' in url:
				pass
			elif not 'http' in url:
				pass
			else:
				url_start = url.replace('/url?q=','').replace('%2520','%20')
				url_end = re.compile('(.+?)&amp;').findall(str(url_start))
				for fin_url in url_end:
					if 'http' in fin_url:
						process.Menu(fin_url,fin_url,2000,'','','','')

def Music():
#    process.Menu('Now thats what i call music','',1700,ORIGIN_ICON,ORIGIN_FANART,'','')
 #   process.Menu('Misc A-Z','http://herovision.x10host.com/Music/',2000,ORIGIN_ICON,ORIGIN_FANART,'','')
    process.Menu('Audiobooks','',600,ORIGIN_ICON,ORIGIN_FANART,'','')
    process.Menu('World Radio','',500,ORIGIN_ICON,ORIGIN_FANART,'','')
    process.Menu('Music Search','',1503,'','','','')


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

params=get_params()
url=None
name=None
iconimage=None
mode=None
description=None
extra=None
fanart=None
fav_mode=None
regexs=None
playlist=None

try:
    regexs=params["regexs"]
except:
    pass

try:
    fav_mode=int(params["fav_mode"])
except:
    pass
try:
    extra=urllib.unquote_plus(params["extra"])
except:
    pass
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
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:
    playitem=urllib.unquote_plus(params["playitem"])
except:
    pass
try:
    playlist=eval(urllib.unquote_plus(params["playlist"]).replace('||',','))
except:
    pass
try:
    regexs=params["regexs"]
except:
    pass


if mode == None: Main_Menu()
elif mode == 1 : process.queueItem()
elif mode == 2 : Music()
elif mode == 3 : Latest_Episodes()
elif mode == 4 : Origin_Main()
elif mode == 5 : Recent_Movies()
elif mode == 6 : TV_Calender_Day(url)
elif mode == 7 : TV_Calender_Prog(extra)
elif mode == 8 : send_to_search(name,extra)
elif mode == 10: from lib import process;process.getFavourites()
elif mode==11:
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    process.addFavorite(name,url,iconimage,fanart,fav_mode)
elif mode==12:
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    process.rmFavorite(name)
elif mode == 13: bagotricks()
elif mode == 19: from lib import Live;Live.Live_Menu()
elif mode == 20: from lib import Live;Live.Live_Main()
elif mode == 21: from lib import Live;Live.Get_Channel(url)
elif mode == 22: from lib import Live;Live.Get_Playlink(name,url)
elif mode == 23: from lib import Live;Live.Ultra()
elif mode == 24: from lib import Live;Live.Get_Ultra_Channel(url)
elif mode == 25: from lib import Live;Live.Search_Ultra()
elif mode == 26: from lib import Live;Live.Check_For_200_Response()
elif mode == 27: from lib import Live;Live.search_checked()
elif mode == 30: Movie_Men()
elif mode == 31: TV_Men()
elif mode == 32: Live_Men()
elif mode == 33: Kids_Men()
elif mode == 34: Music_Men()
elif mode == 35: classic_list()
elif mode == 36: Movie_Def(url)
elif mode == 37: Adult()
elif mode == 38: twenty47()
elif mode == 39: docs()
elif mode == 40: sports()
elif mode == 100: from lib import comedy;comedy.Comedy_Main()
elif mode == 101: from lib import comedy;comedy.Stand_up()
elif mode == 102: from lib import comedy;comedy.Search()
elif mode == 103: from lib import comedy;comedy.Play_Stage(url)
elif mode == 104: from lib import comedy;comedy.Regex(url)
elif mode == 105: process.Resolve(url)
elif mode == 106: from lib import comedy;comedy.Stand_up_Menu()
elif mode == 107: from lib import comedy;comedy.grab_youtube_playlist(url)
elif mode == 108: from lib import comedy;comedy.Search()
elif mode == 109: from lib import yt;yt.PlayVideo(url)
elif mode == 110: from lib import comedy;comedy.Movies_Menu()
elif mode == 111: from lib import comedy;comedy.Pubfilm_Comedy_Grab(url)
elif mode == 112: from lib import comedy;comedy.Grab_Season(iconimage,url)
elif mode == 113: from lib import comedy;comedy.Grab_Episode(url,name,fanart,iconimage)
elif mode == 114: from lib import comedy;comedy.Get_Sources(name,url,iconimage,fanart)
elif mode == 115: from lib import comedy;comedy.Get_site_link(url,name)
elif mode == 116: from lib import comedy;comedy.final(url)
elif mode == 200: from lib import Movies;Movies.Movie_Main()
elif mode == 202 : from lib import Movies;Movies.Movie_Genre(url)
elif mode == 203 : from lib import Movies;Movies.IMDB_Grab(url)
elif mode == 204 : from lib import Movies;Movies.Check_Link(name,url,image)
elif mode == 205 : from lib import Movies;Movies.Get_playlink(url)
elif mode == 206 : from lib import Movies;Movies.IMDB_Top250(url)
elif mode == 207 : from lib import Movies;Movies.search_movies()
elif mode == 208 : from lib import Movies;Movies.movie_channels()
elif mode == 209 : from lib import Movies;Movies.split_for_search(extra)
elif mode == 300 : from lib import multitv;multitv.multiv_Main_Menu()
elif mode == 301 : from lib import multitv;multitv.IMDB_TOP_100_EPS(url)
elif mode == 302 : from lib import multitv;multitv.Popular(url)
elif mode == 303 : from lib import multitv;multitv.Genres()
elif mode == 304 : from lib import multitv;multitv.Genres_Page(url)
elif mode == 305 : from lib import multitv;multitv.IMDB_Get_Season_info(url,iconimage,extra)
elif mode == 306 : from lib import multitv;multitv.IMDB_Get_Episode_info(url,extra)
elif mode == 307 : from lib import multitv;multitv.SPLIT(extra)
elif mode == 308 : from lib import multitv;multitv.Search_TV()
elif mode == 400: from lib import Football_Repeat;Football_Repeat.footy_Main_Menu()
elif mode == 401: from lib import Football_Repeat;Football_Repeat.get_All_Rows(url,iconimage)
elif mode == 402: from lib import Football_Repeat;Football_Repeat.get_PLAYlink(url)
elif mode == 403: from lib import Football_Repeat;Football_Repeat.Football_Highlights()
elif mode == 404: from lib import Football_Repeat;Football_Repeat.FootballFixturesDay()
elif mode == 405: from lib import Football_Repeat;Football_Repeat.FootballFixturesGame(url,iconimage)
elif mode == 406: from lib import Football_Repeat;Football_Repeat.Prem_Table(url)
elif mode == 407: from lib import Football_Repeat;Football_Repeat.get_Multi_Links(url,iconimage)
elif mode == 408: from lib import Football_Repeat;Football_Repeat.Get_the_rows(url,iconimage)
elif mode == 409: from lib import Football_Repeat;Football_Repeat.League_Tables(url)
elif mode == 410: from lib import Football_Repeat;Football_Repeat.Search()
elif mode == 411: from lib import Football_Repeat;Football_Repeat.Prem_Table2(url)
elif mode == 412: from lib import Football_Repeat;Football_Repeat.champ_league(url)
elif mode == 413: from lib import Football_Repeat;Football_Repeat.footytube(url)
elif mode == 414: from lib import Football_Repeat;Football_Repeat.footytube_leagues(name)
elif mode == 415: from lib import Football_Repeat;Football_Repeat.footytube_teams(url)
elif mode == 416: from lib import Football_Repeat;Football_Repeat.footytube_videos(url)
elif mode == 417: from lib import Football_Repeat;Football_Repeat.footytube_frame(name,url)
elif mode == 418: from lib import Football_Repeat;Football_Repeat.get_origin_playlink(url,iconimage,FANART)
elif mode == 419: from lib import Football_Repeat;Football_Repeat.Resolve(url)
elif mode == 420: from lib import Football_Repeat;Football_Repeat.FootballFixturesSingle(description);Football_Repeat.window.doModal();del Football_Repeat.window
elif mode == 421: from lib import Football_Repeat;Football_Repeat.METALLIQ()
elif mode == 500: from lib import radio_gaga;radio_gaga.Radio_Country()
elif mode == 501: from lib import radio_gaga;radio_gaga.Radio(url)
elif mode == 502: process.Resolve(url)
elif mode == 600: from lib import Kodible;Kodible.Kodible_Main_Menu()
elif mode == 602: process.Resolve(url)
elif mode == 603: from lib import Kodible;Kodible.Kids_Audio()
elif mode == 604: from lib import Kodible;Kodible.Kids_Play(url)
elif mode == 605: from lib import Kodible;Kodible.Kids_Play_Multi(url)
elif mode == 606: from lib import Kodible;Kodible.Kids_Menu()
elif mode == 607: from lib import Kodible;Kodible.Kids_AZ()
elif mode == 608: from lib import Kodible;Kodible.Kids_AZ_Audio(url)
elif mode == 614: from lib import Kodible;Kodible.Search_Kids()
elif mode == 700: from lib import xxx_vids;xxx_vids.X_vid_Menu()
elif mode == 701: from lib import xxx_vids;xxx_vids.XNew_Videos(url)
elif mode == 702: from lib import xxx_vids;xxx_vids.XGenres(url)
elif mode == 703: from lib import xxx_vids;xxx_vids.XPornstars(url)
elif mode == 704: from lib import xxx_vids;xxx_vids.XSearch_X()
elif mode == 705: from lib import xxx_vids;xxx_vids.Xtags(url)
elif mode == 706: from lib import xxx_vids;xxx_vids.XPlayLink(url)
elif mode == 800: from lib import Big_Kids;Big_Kids.Big_Kids_Main_Menu()
elif mode == 801: from lib import Big_Kids;Big_Kids.TESTCATS()
elif mode == 802: from lib import Big_Kids;Big_Kids.Search_cartoons()
elif mode == 803: from lib import Big_Kids;Big_Kids.LISTS(url)
elif mode == 804: from lib import Big_Kids;Big_Kids.LISTS2(url,iconimage)
elif mode == 805: process.Resolve(url)
elif mode == 806: from lib import Big_Kids;Big_Kids.watch_cartoon_menu()
elif mode == 807: from lib import Big_Kids;Big_Kids.watch_cartoon_grab_episode(url)
elif mode == 808: from lib import Big_Kids;Big_Kids.watch_cartoon_final(url)
elif mode == 809: from lib import Big_Kids;Big_Kids.watch_cartoon_grab_movies(url)
elif mode == 810: from lib import Big_Kids;Big_Kids.watch_cartoon_grab_episode_second(url)
elif mode == 811: from lib import Big_Kids;Big_Kids.Search_movies()
elif mode == 812: from lib import Big_Kids;Big_Kids.Random_Lists()
elif mode == 813: from lib import Big_Kids;Big_Kids.Random_Cartoon(url)
elif mode == 814: from lib import Big_Kids;Big_Kids.Random_Movie(url)
elif mode == 816: from lib import Big_Kids;Big_Kids.Random_Play_Cartoon(url,name)
elif mode == 817: from lib import Big_Kids;Big_Kids.twenty47_select()
elif mode == 900: from lib import Pandora;Pandora.Pandora_Main()
elif mode == 901: from lib import Pandora;Pandora.Pandoras_Box()
elif mode == 423: from lib import Pandora;Pandora.open_Menu(url)
elif mode == 426: from lib import Pandora;Pandora.Pandora_Menu(url)
elif mode == 903: from lib import Pandora;Pandora.Search_Menu()
elif mode == 904: from lib import Pandora;Pandora.Search_Pandoras_Films()
elif mode == 905: from lib import Pandora;Pandora.Search_Pandoras_TV()
elif mode == 906: process.Big_Resolve(name,url)
elif mode == 907: from lib import Pandora;Pandora.Pans_Resolve(name,url)
elif mode == 1100: from lib.pyramid import pyramid;pyramid.SKindex();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1128: from lib.pyramid import pyramid;pyramid.SKindex_Joker();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1129: from lib.pyramid import pyramid;pyramid.SKindex_Oblivion();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1131: from lib.pyramid import pyramid;pyramid.SKindex_Supremacy();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1132: from lib.pyramid import pyramid;pyramid.SKindex_BAMF();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1133: from lib.pyramid import pyramid;pyramid.SKindex_Quicksilver();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1134: from lib.pyramid import pyramid;pyramid.SKindex_Silent();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1101:from lib.pyramid import pyramid;pyramid.getData(url,fanart);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1102:from lib.pyramid import pyramid;pyramid.getChannelItems(name,url,fanart);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1103:from lib.pyramid import pyramid;pyramid.getSubChannelItems(name,url,fanart);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1104:from lib.pyramid import pyramid;pyramid.getFavorites();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1105:
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    from lib.pyramid import pyramid;pyramid.addFavorite(name,url,iconimage,fanart,fav_mode)
elif mode==1106:
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    from lib.pyramid import pyramid;pyramid.rmFavorite(name)
elif mode==1107:from lib.pyramid import pyramid;pyramid.addSource(url)
elif mode==1108:from lib.pyramid import pyramid;pyramid.rmSource(name)
elif mode==1109:from lib.pyramid import pyramid;pyramid.download_file(name, url)
elif mode==1110:from lib.pyramid import pyramid;pyramid.getCommunitySources()
elif mode==1111:from lib.pyramid import pyramid;pyramid.addSource(url)
elif mode==1112:
    from lib.pyramid import pyramid
    if 'google' in url:
        import urlresolver
        resolved = urlresolver.resolve(url)
        item = xbmcgui.ListItem(path=resolved)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    elif not url.startswith("plugin://plugin") or not any(x in url for x in pyramid.g_ignoreSetResolved):#not url.startswith("plugin://plugin.video.f4mTester") :
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    else:
        print 'Not setting setResolvedUrl'
        xbmc.executebuiltin('XBMC.RunPlugin('+url+')')
elif mode==1113:from lib.pyramid import pyramid;pyramid.play_playlist(name, playlist)
elif mode==1114:from lib.pyramid import pyramid;pyramid.get_xml_database(url);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1115:from lib.pyramid import pyramid;pyramid.get_xml_database(url, True);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1116:from lib.pyramid import pyramid;pyramid.getCommunitySources(True);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1117:
    url,setresolved = getRegexParsed(regexs, url)
    if url:
        from lib.pyramid import pyramid;pyramid.playsetresolved(url,name,iconimage,setresolved)
    else:
        xbmc.executebuiltin("XBMC.Notification(ThePyramid ,Failed to extract regex. - "+"this"+",4000,"+icon+")")
elif mode==1118:
    try:
        from lib.pyramid import youtubedl
    except Exception:
        xbmc.executebuiltin("XBMC.Notification(ThePyramid,Please [COLOR yellow]install the Youtube Addon[/COLOR] module ,10000,"")")
    stream_url=youtubedl.single_YD(url)
    from lib.pyramid import pyramid;pyramid.playsetresolved(stream_url,name,iconimage)
elif mode==1119:from lib.pyramid import pyramid;pyramid.playsetresolved (pyramid.urlsolver(url),name,iconimage,True)
elif mode==1121:from lib.pyramid import pyramid;pyramid.ytdl_download('',name,'video')
elif mode==1123:from lib.pyramid import pyramid;pyramid.ytdl_download(url,name,'video')
elif mode==1124:from lib.pyramid import pyramid;pyramid.ytdl_download(url,name,'audio')
elif mode==1125:from lib.pyramid import pyramid;pyramid.search(url);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1126:
    name = name.split(':')
    from lib.pyramid import pyramid;pyramid.search(url,search_term=name[1])
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1127:
    from lib.pyramid import pyramid;pyramid.pulsarIMDB=search(url)
    xbmc.Player().play(pulsarIMDB)
elif mode == 1130:from lib.pyramid import pyramid;pyramid.GetSublinks(name,url,iconimage,fanart)
elif mode == 1140:from lib.pyramid import pyramid;pyramid.SearchChannels();pyramid.SetViewThumbnail();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1141: from lib.pyramid import pyramid;pyramid.Search_input(url);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1142: from lib.pyramid import pyramid;pyramid.RESOLVE(url)
elif mode == 1143: from lib.pyramid import pyramid;pyramid.SKindex_TigensWorld();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1144: from lib.pyramid import pyramid;pyramid.queueItem();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1145: from lib.pyramid import pyramid;pyramid.SKindex_Ultra();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1146: from lib.pyramid import pyramid;pyramid.SKindex_Fido();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1147: from lib.pyramid import pyramid;pyramid.SKindex_Rays();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1153: from lib.pyramid import pyramid;pyramid.pluginquerybyJSON(url);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1154: from lib.pyramid import pyramid;pyramid.get_random(url);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1200: from lib.freeview import freeview;freeview.CATEGORIES()
elif mode == 1201: from lib.freeview import freeview;freeview.play(url)
elif mode == 1202: from lib.freeview import freeview;freeview.tvplayer(url)
elif mode == 1400 : from lib import ninja;ninja.CATEGORIES()
elif mode == 1401 : from lib import ninja;ninja.VIDEOLIST(url)
elif mode == 1402 : from lib import ninja;ninja.PLAYVIDEO(url)
elif mode == 1500 : from lib import search;search.Search_Menu()
elif mode == 1501 : from lib import search;search.Search_Input(name,url,extra)
elif mode == 1502 : from lib import search;search.MUSIC(Search_name,url)
elif mode == 1503 : from lib import search;search.Music_Search()
elif mode == 1504 : from lib import search;search.Clear_Search(url)
elif mode == 1600 : from lib import brettus_anime;brettus_anime.GetList()
elif mode == 1601 : from lib import brettus_anime;brettus_anime.GetContent(url,iconimage)
elif mode == 1602 : from lib import brettus_anime;brettus_anime.PLAYLINK(url,iconimage)
elif mode == 1700 : from lib import Now_thats_what_i_call_music;Now_thats_what_i_call_music.Now_Thats_What_I_Call_Music()
elif mode == 1701 : from lib import Now_thats_what_i_call_music;Now_thats_what_i_call_music.Now_Loop(url,iconimage,fanart)
elif mode == 1702 : from lib import Now_thats_what_i_call_music;Now_thats_what_i_call_music.Now_Playlinks(url,iconimage,fanart)
elif mode == 1750 : from lib import todays_football;todays_football.Todays_Football_Menu()
elif mode == 1751 : from lib import todays_football;todays_football.Todays_Football()
elif mode == 1752 : from lib import todays_football;todays_football.Search_Channels_Mainstream(url)
elif mode == 1753 : from lib import todays_football;todays_football.Live_On_Sat()
elif mode == 1800 : from lib import cold_as_ice;cold_as_ice.Cold_Menu()
elif mode == 1801 : from lib import cold_as_ice;cold_as_ice.GetContent(url,iconimage)
elif mode == 1802 : from lib import cold_as_ice;cold_as_ice.PLAYLINK(name,url,iconimage)
elif mode == 2000 : from lib import index_regex;index_regex.Main_Loop(url)
elif mode == 2100 : from lib import Sports_Replays;Sports_Replays.Sports_Repeats()
elif mode == 2101 : from lib import Sports_Replays;Sports_Replays.Motor_Replays(url)
elif mode == 2102 : from lib import Sports_Replays;Sports_Replays.motor_name(url)
elif mode == 2103 : from lib import Sports_Replays;Sports_Replays.motor_race(extra)
elif mode == 2104 : from lib import Sports_Replays;Sports_Replays.motor_single(name,extra)
elif mode == 2105 : from lib import Sports_Replays;Sports_Replays.F1_Replays(url)
elif mode == 2106 : from lib import Sports_Replays;Sports_Replays.F1_page(url)
elif mode == 2107 : from lib import Sports_Replays;Sports_Replays.F1_items(url,iconimage)
elif mode == 2108 : from lib import Sports_Replays;Sports_Replays.F1_Playlink(url)
elif mode == 2150 : from lib import renegades;renegades.run()
#elif mode == 2151 : import plugintools;plugintools.add_item(mode,name,url,iconimage,fanart)
elif mode == 2200 : from lib import tv_guide;tv_guide.TV_GUIDE_MENU()
elif mode == 2201 : from lib import tv_guide;tv_guide.whatsoncat()
elif mode == 2202 : from lib import tv_guide;tv_guide.whatson(url)
elif mode == 2203 : from lib import tv_guide;tv_guide.search_split(extra)
elif mode == 2204 : from lib import tv_guide;tv_guide.TV_GUIDE_CO_UK_CATS()
elif mode == 2205 : from lib import tv_guide;tv_guide.tvguide_co_uk(url)
elif mode == 2206 : from lib import tv_guide;tv_guide.WhatsOnCOUK(url,extra)
elif mode == 2207 : from lib import tv_guide;tv_guide.Select_Type()
elif mode == 2300 : DOJO_MAIN(url)
elif mode == 2301 : Reaper_Loop(url)
elif mode == 2350 : google_index_search()
elif mode == 10000: from lib import youtube_regex;youtube_regex.Youtube_Grab_Playlist_Page(url)
elif mode == 10001: from lib import youtube_regex;youtube_regex.Youtube_Playlist_Grab(url)
elif mode == 10002: from lib import youtube_regex;youtube_regex.Youtube_Playlist_Grab_Duration(url)
elif mode == 10003: from lib import yt;yt.PlayVideo(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
