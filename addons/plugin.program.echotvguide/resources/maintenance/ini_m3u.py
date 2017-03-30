#example to run -  RunScript($CWD/iptv_maintenance.py)
from __future__ import unicode_literals
from collections import namedtuple
import codecs
import sys,os,json,urllib2
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,urllib2,re
import shutil
import time
import argparse

addon = 'plugin.program.echotvguide';addon_name = addon;icon = xbmc.translatePath(os.path.join('special://home/addons', addon, 'icon.png'))
addonPath = xbmc.translatePath(os.path.join('special://home', 'addons', addon))
basePath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', addon))
dbPath = xbmc.translatePath(xbmcaddon.Addon(addon).getAddonInfo('profile'))
dialog = xbmcgui.Dialog();dp = xbmcgui.DialogProgress()
# Switch arguments  -  Bypassed later
parser = argparse.ArgumentParser(description='Generate IPTVSubs m3u file.')
parser.add_argument('-c', dest='channel_fn', type=str, help='Output file of channel guide ids.')
parser.add_argument('-u', dest='username', type=str)
parser.add_argument('-p', dest='password', type=str)
parser.add_argument('-o', dest='output_file', type=str, help="m3u output file")
parser.add_argument('-g', dest='groups', type=str, help='Groups to include in m3u file, for example (-g ENGLISH,SPORTS). Includes all by default. m3u will have groups in same order specified.')
parser.add_argument('-s', dest='guide_sort', action='store_true', default=False, help="Put all channels with guide ids at the top")
parser.add_argument('-m', dest='map_file', type=str, help="Tab separated file containing map of channel names to guide id, for example \"TREEHOUSE HD (NA)	I80173.lab.zap2it.com\"")
parser.add_argument('--ini', dest='ini_file', type=str, help="ini output file")
parser.add_argument('--name-map', dest='namemap_file', type=str, help="Tab-separated file mapping channel names")
args = parser.parse_args(sys.argv[1:])
username = args.username
password = args.password
output_fn = args.output_file
args.map_file =''
#args.groups = ''





# How to get from settings
#Name1="iptvsubs";addon_name1='plugin.video.iptvsubs';addon=xbmcaddon.Addon(addon_name1);urlpath1='http://2.welcm.tv:8000';username1=addon.getSetting('kasutajanimi');password1=addon.getSetting('salasona');groups1 = 'ENGLISH,SPORTS,FOR ADULTS'
#Name2="DexterTV";addon_name2='plugin.video.dex';addon=xbmcaddon.Addon(addon_name2);urlpath22 = addon.getSetting('lehekylg');urlpath2=urlpath22+':8000';username2=addon.getSetting('kasutajanimi');password2=addon.getSetting('salasona');groups2 = 'ENTERTAINMENT,MOVIES,UK,KIDS,NEWS,SPORTS'
# DUMMY TEMPLATE
Name1="-";urlpath1='http://2.welcm.tv:8000';username1='-';password1='-';groups1 = 'ENGLISH,SPORTS,FOR ADULTS';addon_name1=addon_name;addon=xbmcaddon.Addon(addon_name1)
Name2="-";urlpath2='http://158.69.54.54:8000';username2='-';password2='-';groups2 = 'ENTERTAINMENT,MOVIES,UK,KIDS,NEWS,SPORTS';addon_name2=addon_name;addon=xbmcaddon.Addon(addon_name2)      
Name3="-";urlpath3='http://.com:8000';username3='-';password3='-';groups3 = 'British Package,Sports Package';addon_name3=addon_name;addon=xbmcaddon.Addon(addon_name3)
Name4="-";urlpath4='http://.tv:8080';username4='-';password4='-';groups4 = 'USA,United kingdom,Sport,Porn';addon_name4=addon_name;addon=xbmcaddon.Addon(addon_name4)           
Name5="-";urlpath5='http://.us:9998';username5='-';password5='-';groups5 = 'USA,UK';addon_name5=addon_name;addon=xbmcaddon.Addon(addon_name5)
Name6="-";urlpath6='http://.co:8000';username6='-';password6='-';groups6 = 'U.S.A,U.K,XXX';addon_name6=addon_name;addon=xbmcaddon.Addon(addon_name6) 
Name7="-";urlpath7='http://.com:8000';username7='-';password7='-';groups7 = 'USA CHANNELS,UK channels';addon_name7=addon_name;addon=xbmcaddon.Addon(addon_name7) 
Name8="-";urlpath8='http://.com:8000';username8='-';password8='-';groups8 = 'English';addon_name8=addon_name;addon=xbmcaddon.Addon(addon_name8)
Name9="-";urlpath9='http://.tv:8000';username9='-';password9='-';groups9 = 'Sky UK,Radio TV';addon_name9=addon_name;addon=xbmcaddon.Addon(addon_name9) 



#GRAB POSSIBLE CREDENTIALS

#Get iptvsubs Pass
addonPath1 = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'plugin.video.iptvsubs'))
addonDestFile1 = os.path.join(addonPath1, 'settings.xml')
if os.path.exists(addonDestFile1):
    if os.path.exists(addonPath1):
        try:    
            #Name2="DexterTV";addon_name2='plugin.video.dex';addon=xbmcaddon.Addon(addon_name2);urlpath22 = addon.getSetting('lehekylg');urlpath2=urlpath22+':8000';username2=addon.getSetting('kasutajanimi');password2=addon.getSetting('salasona');groups2 = 'ENTERTAINMENT,MOVIES,UK,KIDS,NEWS,SPORTS'
            #Name2="DexterTV";addon_name2='plugin.video.dex';addon=xbmcaddon.Addon(addon_name2);urlpath22 = addon.getSetting('lehekylg');urlpath2=urlpath22+':8000';username2=addon.getSetting('kasutajanimi');password2=addon.getSetting('salasona');groups2 = [COLOR oldlace][B]-- [COLOR deepskyblue]CANADA [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR deepskyblue]USA [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR deepskyblue]UK [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR mediumpurple]KIDS [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR mediumpurple]NEWS [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR mediumpurple]SPORTS [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR tomato]TESTING AREA [COLOR oldlace]--[/B][/COLOR]'
            Name1="iptvsubs";addon_name1='plugin.video.iptvsubs';addon=xbmcaddon.Addon(addon_name1);urlpath1='http://2.welcm.tv:8000';username1=addon.getSetting('kasutajanimi');password1=addon.getSetting('salasona');groups1 = 'ENGLISH,SPORTS,FOR ADULTS'    
        except: pass


#Get DexterTV Pass
addonPath2 = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'plugin.video.dex'))
addonDestFile2 = os.path.join(addonPath2, 'settings.xml')
if os.path.exists(addonDestFile2):
    if os.path.exists(addonPath2):
        try:    
            #Name2="DexterTV";addon_name2='plugin.video.dex';addon=xbmcaddon.Addon(addon_name2);urlpath22 = addon.getSetting('lehekylg');urlpath2=urlpath22+':8000';username2=addon.getSetting('kasutajanimi');password2=addon.getSetting('salasona');groups2 = 'ENTERTAINMENT,MOVIES,UK,KIDS,NEWS,SPORTS'
            #Name2="DexterTV";addon_name2='plugin.video.dex';addon=xbmcaddon.Addon(addon_name2);urlpath22 = addon.getSetting('lehekylg');urlpath2=urlpath22+':8000';username2=addon.getSetting('kasutajanimi');password2=addon.getSetting('salasona');groups2 = [COLOR oldlace][B]-- [COLOR deepskyblue]CANADA [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR deepskyblue]USA [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR deepskyblue]UK [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR mediumpurple]KIDS [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR mediumpurple]NEWS [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR mediumpurple]SPORTS [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR tomato]TESTING AREA [COLOR oldlace]--[/B][/COLOR]'
            Name2="DexterTV";addon_name2='plugin.video.dex';addon=xbmcaddon.Addon(addon_name2);urlpath22 = addon.getSetting('lehekylg');urlpath2=urlpath22+':8000';username2=addon.getSetting('kasutajanimi');password2=addon.getSetting('salasona');groups2 = '[COLOR oldlace][B]-- [COLOR deepskyblue]CANADA [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR deepskyblue]USA [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR deepskyblue]UK [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR mediumpurple]KIDS [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR mediumpurple]NEWS [COLOR oldlace]--[/B][/COLOR],[COLOR oldlace][B]-- [COLOR mediumpurple]SPORTS [COLOR oldlace]--[/B][/COLOR]'
        except: pass


mode='run_maintenance_ini'


def maintenance_ini():
    #######################################
    # ini and m3u Maintenance
    #######################################
    
    choice = dialog.select('Choose file to edit.  Irreversible.', ['Close',
                                                                   'Copy  addons.ini to addons2.ini (Create)',
                                                                   'Clean addons2.ini channel names',
                                                                   'Clean addons.ini channel names',
                                                                   'Clean playlist.m3u channel names',
                                                                   'Clean iptv.m3u channel names',
                                                                   'Clean favorites.xml channel names',                                                                   
                                                                   'Copy  favorites.xml to addons2.ini',
                                                                   'Copy  favorites.xml to iptv.m3u',
                                                                   'Copy  iptv.m3u to addons2.ini',
                                                                   'View  addon2.ini',
                                                                   'View  addons.ini',
                                                                   'View  playlist.m3u',
                                                                   'View  iptv.m3u',
                                                                   'Delete addons2.ini',
                                                                   'Delete addons.ini',
                                                                   'Delete iptv.m3u',
                                                                   'Delete playlist.m3u',
                                                                   'Delete source.db  (Deletes linked channels)',
                                                                   'Delete guide.cfg  (Guide selection)',
                                                                   'Delete guide.xml  (Guide)',
                                                                   '',
                                                                   '* Subscription*  '+Name1,                                                                                     
                                                                   '* Subscription*  '+Name2,
                                                                   '* Subscription*  '+Name3,
                                                                   '* Subscription*  '+Name4,                                                 
                                                                   '* Subscription*  '+Name5,  
                                                                   '* Subscription*  '+Name6, 
                                                                   '* Subscription*  '+Name7,                                                 
                                                                   '* Subscription*  '+Name8,                                                                                                                                                                                                                                                                                                 
                                                                   '* Subscription*  '+Name9]) 
    if choice == 0:  sys.exit(0)
    #
    # Copy addons.ini to addons2.ini
    if choice == 1:
        SourceFile = os.path.join(basePath, 'addons.ini'); DestFile = os.path.join(basePath, 'addons2.ini') ; from shutil import copyfile; copyfile(SourceFile, DestFile);sys.exit()
    #
    # Clean addons2.ini
    if choice == 2:
        Clean_File=xbmc.translatePath(basePath+'/addons2.ini');Clean_Names(Clean_File,basePath+'/_addons2.ini')

    # Clean addons.ini
    if choice == 3:
        Clean_File=xbmc.translatePath(basePath+'/addons.ini');Clean_Names(Clean_File,basePath+'/_addons.ini')
        
    # Clean playlist.m3u          
    if choice == 4: 
        Clean_File=xbmc.translatePath(basePath+'/playlist.m3u');Clean_Names(Clean_File,basePath+'/_playlist.m3u')                        
        
    # Clean iptv.m3u           
    if choice == 5: 
        Clean_File=xbmc.translatePath(basePath+'/iptv.m3u');Clean_Names(Clean_File,basePath+'/_iptv.m3u')

    # Clean favorites.xml
    if choice == 6:
        favourites=xbmc.translatePath('special://profile/favourites.xml');Clean_Names(favourites,favourites+'.xml')

    # Copy favorites.xml to addons2.ini
    if choice == 7:
        Dest_File=xbmc.translatePath(basePath+'/addons2.ini');Copy_Favs_ini(Dest_File);Clean_Names(Dest_File,basePath+'/_addons2.ini')

    # Copy favorites.xml to iptv.m3u
    if choice == 8:
        Dest_File=xbmc.translatePath(basePath+'/iptv.m3u');Copy_Favs_m3u(Dest_File);Clean_Names(Dest_File,basePath+'/_iptv.m3u')

    # Copy iptv.m3u to addons2.ini
    if choice == 9:
        Dest_File=xbmc.translatePath(basePath+'/addons2.ini');Copy_m3u_to_addon(Dest_File);Clean_Names(Dest_File,basePath+'/_addons2.ini')

   #
    # View files
    if choice == 10:
        filePath = os.path.join(basePath, 'addons2.ini')
        class TextBox():
         WINDOW=10147 ; CONTROL_LABEL=1 ; CONTROL_TEXTBOX=5
         def __init__(self,*args,**kwargs):  xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) ; self.win=xbmcgui.Window(self.WINDOW); xbmc.sleep(500) ; self.setControls()
         def setControls(self):
             self.win.getControl(self.CONTROL_LABEL).setLabel('View File')
             try: f=open(filePath); text=f.read()
             except: text=filePath
             self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
             return
        TextBox()
        sys.exit(0)
    #
    # View addons2.ini
    if choice == 11:
        filePath = os.path.join(basePath, 'addons.ini')
        class TextBox():
         WINDOW=10147 ; CONTROL_LABEL=1 ; CONTROL_TEXTBOX=5
         def __init__(self,*args,**kwargs):  xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) ; self.win=xbmcgui.Window(self.WINDOW); xbmc.sleep(500) ; self.setControls()
         def setControls(self):
             self.win.getControl(self.CONTROL_LABEL).setLabel('View File')
             try: f=open(filePath); text=f.read()
             except: text=filePath
             self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
             return
        TextBox()
        sys.exit(0)
    #
    # View playlist.m3u
    if choice == 12:   
        filePath = os.path.join(basePath, 'playlist.m3u')
        class TextBox():
         WINDOW=10147 ; CONTROL_LABEL=1 ; CONTROL_TEXTBOX=5
         def __init__(self,*args,**kwargs):  xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) ; self.win=xbmcgui.Window(self.WINDOW); xbmc.sleep(500) ; self.setControls()
         def setControls(self):
             self.win.getControl(self.CONTROL_LABEL).setLabel('View File')
             try: f=open(filePath); text=f.read()
             except: text=filePath
             self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
             return
        TextBox()
        sys.exit(0)
    #
    # View iptv.m3u
    if choice == 13:   
        filePath = os.path.join(basePath, 'iptv.m3u')
        class TextBox():
         WINDOW=10147 ; CONTROL_LABEL=1 ; CONTROL_TEXTBOX=5
         def __init__(self,*args,**kwargs):  xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) ; self.win=xbmcgui.Window(self.WINDOW); xbmc.sleep(500) ; self.setControls()
         def setControls(self):
             self.win.getControl(self.CONTROL_LABEL).setLabel('View File')
             try: f=open(filePath); text=f.read()
             except: text=filePath
             self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
             return
        TextBox()
        sys.exit(0)

    # Delete .ini
    if choice == 14:
        filePath = os.path.join(dbPath, 'addons2.ini')
        if os.path.exists(filePath):  os.remove(filePath); sys.exit()
        else: sys.exit(0)
    #
    if choice == 15:
        filePath = os.path.join(dbPath, 'addons.ini')
        if os.path.exists(filePath):  os.remove(filePath); sys.exit()
        else: sys.exit(0)
    #
    if choice == 16:
        filePath = os.path.join(dbPath, 'iptv.m3u')
        if os.path.exists(filePath):  os.remove(filePath); sys.exit()
        else: sys.exit(0)
    #
    if choice == 17:
        filePath = os.path.join(dbPath, 'playlist.m3u')
        if os.path.exists(filePath):  os.remove(filePath); sys.exit()
        else: sys.exit(0)
    #
    if choice == 18:
        filePath = os.path.join(dbPath, 'source.db')
        if os.path.exists(filePath):  os.remove(filePath); sys.exit()
        else: sys.exit(0)
    #
    if choice == 19:
        filePath = os.path.join(dbPath, 'guide.cfg')
        if os.path.exists(filePath):  os.remove(filePath); sys.exit()
        else: sys.exit(0)
    #
    if choice == 20:
        filePath = os.path.join(dbPath, 'guide.xml')
        if os.path.exists(filePath):  os.remove(filePath); sys.exit()
        else: sys.exit(0)
    #
    if choice == 21:
        filePath = os.path.join(dbPath, 'guide.xml')
        if os.path.exists(filePath):  os.remove(filePath); sys.exit()
        else: sys.exit(0)



    #######################################
    # Custom Providers
    #######################################
    if choice == 22: Custom_Provider(Name1,addon_name1,urlpath1,username1,password1,groups1) 
    if choice == 23: Custom_Provider(Name2,addon_name2,urlpath2,username2,password2,groups2) 
    if choice == 24: Custom_Provider(Name3,addon_name3,urlpath3,username3,password3,groups3) 
    if choice == 25: Custom_Provider(Name4,addon_name4,urlpath4,username4,password4,groups4) 
    if choice == 26: Custom_Provider(Name5,addon_name5,urlpath5,username5,password5,groups5) 
    if choice == 27: Custom_Provider(Name6,addon_name6,urlpath6,username6,password6,groups6) 
    if choice == 28: Custom_Provider(Name7,addon_name7,urlpath7,username7,password7,groups7) 
    if choice == 29: Custom_Provider(Name8,addon_name8,urlpath8,username8,password8,groups8) 
    if choice == 30: Custom_Provider(Name9,addon_name9,urlpath9,username9,password9,groups9)
    # 








def Custom_Provider(provider,addon,urlpath,username,password,groups):
#######################################
# Custom Provider
#######################################
    addon_name=addon
    args.groups = groups
    choice = dialog.select(addon + '  User: '+username+'  Pass: '+password, ['Close',
                                                                              addon+'  -->  addons.ini',
                                                                              addon+'  -->  addon2.ini',
                                                                              addon+'  -->  '+provider+'.ini',
                                                                              addon+'  -->  playlist.m3u',
                                                                              addon+'  -->  iptv.m3u',
                                                                              addon+'  -->  '+provider+'.m3u',
                                                                              'Copy addons.ini to addons2.ini (Create)'])                                      
    if choice == 0: sys.exit()
    if choice == 1: args.output_file='';args.ini_file='addons.ini';Run_scraper(urlpath,addon_name,username,password,provider)
    if choice == 2: args.output_file='';args.ini_file='addons2.ini';Run_scraper(urlpath,addon_name,username,password,provider)
    if choice == 3: args.output_file='';args.ini_file=provider+'.ini' ;Run_scraper(urlpath,addon_name,username,password,provider) 
    if choice == 4: args.output_fn='playlist.m3u';args.ini_file='';Run_scraper(urlpath,addon_name,username,password,provider)
    if choice == 5: args.output_fn='iptv.m3u';args.ini_file='';Run_scraper(urlpath,addon_name,username,password,provider)
    if choice == 6: args.output_fn=provider+'.m3u';args.ini_file='';Run_scraper(urlpath,addon_name,username,password,provider) 
    if choice == 7: SourceFile = os.path.join(basePath, 'addons.ini'); DestFile = os.path.join(basePath, 'addons2.ini') ; from shutil import copyfile; copyfile(SourceFile, DestFile);sys.exit()
#



def Run_scraper(urlpath,addon_name,username,password,provider):
    #######################################
    # Run scraper
    #######################################
    # Last change message with credentials
    choice = xbmcgui.Dialog().yesno("TV Guide  " + addon_name, "Your Username  :" + username,"Your Password  :" + password, "Cancel or OK?",  yeslabel='Yes',nolabel='No')
    if choice == 0:  sys.exit(0)
    # Append or write
    if choice == 1:
        choice = xbmcgui.Dialog().yesno("TV Guide  " + addon_name, "Yes to Append to file, No to overwrite","Append adds to existing file." ,"No overwrites all data", yeslabel='Yes',nolabel='No')
        if choice == 1:  write_style = 'a'
        else:  write_style = 'w'
    #
    # Final settings before run
    #panel_url = urlpath+":8000/panel_api.php?username={}&password={}".format(username, password)
    panel_url = urlpath+"/panel_api.php?username={}&password={}".format(username, password)
  
    u = urllib2.urlopen(panel_url)
    j = json.loads(u.read())

    # Channel ID Map
    my_map = {"TREEHOUSE HD (NA)":"I80173.labs.zap2it.com",
              "YTV HD (NA)":"I70827.labs.zap2it.com",
              "FAMILY HD (NA)":"I70520.labs.zap2it.com",
              }

    if args.map_file:
      with open(args.map_file) as f:
        for line in f:
          sp_line = line.rstrip(os.linesep).split("\t")
          my_map[sp_line[0]] = sp_line[1]

    #Renames channels as they are downloaded
    channelname_map = {"5*":"5Star", 
                       "welcm":"welcmm",
                       "5 Star":"5Star",
                       "A+E HD":"A&E",
                       "A&E HD":"A&E",
                       "5 Star":"5Star",
                       "ACTION HD":"ACTION",                   
                       "Alibi SD":"Alibi",      
                       "AMC HD from BT":"AMC UK",                   
                       "ANIMAL PLANET HD - NEW":"Animal Planet",             
                       "Animal Planet HD":"Animal Planet",    
                       "BBC AMERICA HD":"BBC America",  
                       "BBC One HD":"BBC1",        
                       "BBC One=":"BBC1=",                   
                       "BBC Two HD":"BBC2",      
                       "BBC Two":"BBC2", 
                       "BBC Three HD":"BBC3",              
                       "BBC Three":"BBC3",                                 
                       "BBC Four HD":"BBC4",
                       "BBC Four":"BBC4",
                       "BBC News Channel":"BBC News",                
                       "BBC NEWS":"BBC News",       
                       "BEIN Sports 1":"BEINS1",  
                       "BEIN HD":"BEINS1",   
                       "BET HD":"BET",        
                       "Big Ten Network HD":"Big Ten Network",   
                       "BRAVO HD":"Bravo",                    
                       "BT Sport 1HD":"BT Sport 1 HD",
                       "BT Sport 2HD":"BT Sport 2 HD",
                       "BT SPort 1":"BT Sport 1", 
                       "BT SPort 2":"BT Sport 2",                        
                       "CARTOON NETWORK HD (NA)":"Cartoon Network",        
                       "Cartoon Network HD":"Cartoon Network",                   
                       "CARTOON NETWORK":"Cartoon Network",      
                       "CBC EAST HD":"CBC",                    
                       "CBC NEWS HD":"CBC News",              
                       "CBS NEWS HD":"CBS News",        
                       "CBS SPORTS HD":"CBS Sports",                   
                       "CBS Sports Network=":"CBS Sports=",      
                       "CHCH HD":"CHCH",                    
                       "CITY TV HD":"City TV Toronto",              
                       "CNBC HD":"CNBC",        
                       "CNBC uk":"CNBC UK",                   
                       "CNN HD":"CNN",
                       "Comedy Central HD":"Comedy Central",      
                       "Comedy Central uk":"Comedy Central UK",                    
                       "COMEDY NETWORK HD":"Comedy Central",              
                       "Cooking Channel HD":"Cooking Channel",        
                       "CP24 HD":"CP24",                   
                       "Crime & Investigation":"Crime Investigation",      
                       "CTV EAST HD":"CTV Toronto",                    
                       #"CTV=":"CTV Toronto=",              
                       "CW HD":"CW",        
                       "CW11 HD":"CW",                   
                       "DISCOVERY HD":"Discovery",      
                       "Discovery uk":"Discovery UK",
                       "Discovery investigation":"Discovery Investigation",          
                       "Disney HD East - NEW":"Disney",              
                       "Disney Jr. UK":"Disney Jr UK",        
                       "DISNEY XD HD (NA)":"Disney XD",                   
                       "DIY HD":"DIY",                      
                       "E! HD":"E!",      
                       "ESPN 2 HD":"ESPN2",                    
                       "ESPN HD":"ESPN",              
                       "Esquire Network HD":"Esquire",        
                       "FAMILY HD (NA)":"FAMILY",                   
                       "FOOD HD":"Food Network",      
                       "Food Network HD":"Food Network",                    
                       "FOX NEWS HD":"Fox News",
                       "FOX SPORTS 1 HD":"Fox Sports 1 HD",        
                       "FOX SPORTS 2 HD":"Fox Sports 2 HD",   
                       #"Fox Sports 1 HD":"Fox Sports 1 HD",        
                       #"Fox Sports 2 HD":"Fox Sports 2 HD",                   
                       "Fox UK":"FOX UK",      
                       "FX HD":"FX",                
                       "FXX HD":"FXX",              
                       "GLOBAL EAST HD":"Global Toronto",        
                       "GLOBAL TV":"Global Toronto",            
                       "GOLF HD":"Golf Channel",                       
                       "GSN HD":"GSN",                   
                       "Hallmark HD":"Hallmark",      
                       "HBO COMEDY HD":"HBO Comedy",                    
                       "HBO EAST HD":"HBO HD",              
                       "HBO SIGNATURE HD":"HBO Signature",        
                       "HGTV HD":"HGTV",                   
                       "History 2":"H2",      
                       "HISTORY HD":"History",                    
                       "HUSTLER HD":"HUSTLER",
                       "ID HD":"Discovery Investigation",
                       #"ID=":"Discovery Investigation=",
                       "IFC HD":"IFC",
                       "ITV 1":"ITV1",  
                       "ITV 2":"ITV2",                   
                       "LIFE HD":"Lifetime",                       
                       "LIFETIME MOVIES HD":"LMN",                  
                       "MSNBC HD - NEW":"MSNBC",      
                       "MTV HD":"MTV",                    
                       "MTV1 UK":"MTV UK",              
                       "NAT GEO HD":"National Geographic",        
                       "NAT GEO WILD HD":"Nat Geo Wild",                   
                       "NBA HD":"NBA TV",      
                       "NBC SPORTS":"NBCSN",                    
                       "NBCSN HD":"NBCSN",              
                       "NFL NOW HD":"NFL Network",        
                       "NHL NETWORK HD":"NHL Network",                   
                       "Nick HD":"Nickelodeon",                       
                       "Nick Jr.":"Nick Jr",        
                       "NICKELODEON HD (NA)":"Nickelodeon",                   
                       "OMNI 1 HD":"OMNI 1",                       
                       "OMNI 2 HD":"OMNI 2",                   
                       "OWN HD":"OWN",      
                       "PBS HD":"PBS",                    
                       "PLAYBOY TV HD - NEW":"PLAYBOY",              
                       "Poker Central HD":"Poker Central",        
                       "PREMIER HD":"Premiere",                   
                       "PREMIER SPORTS":"Premiere Sports",      
                       "SHOWCASE HD - NEW":"SHOWCASE",                    
                       "SHOWTIME EAST":"Showtime HD",              
                       "SHOWTIME SHOWCASE HD":"Showtime Showcase",  
                       "Sky Movies Drama & Romance":"Sky Movies Drama",                                     
                       "Sky Movies Sci-Fi":"Sky Movies Scifi",     
                       "Sky Movies Superheroes":"Sky Superheroes",                                              
                       "SKY SPORTS 1 HD":"Sky Sports 1 HD", 
                       "SKY SPORTS 2":"Sky Sports 2",    
                       "SKY SPORTS 2 HD":"Sky Sports 2 HD",  
                       "SKY SPORTS 3 HD":"Sky Sports 3 HD",                       
                       "SKY SPORTS 4 HD":"Sky Sports 4 HD",                       
                       "SKY SPORTS 5 HD":"Sky Sports 5 HD",
                       "Sky Sports News HD":"Sky Sports News",
                       "SLICE HD":"SLICE",                               
                       "SONY ESPN HD - LIVE EVENTS":"PPV",        
                       "Sony Six HD":"Sony Six",                   
                       "Spike HD":"Spike",
                       "SPIKE HD":"Spike",           
                       "SPORTSNET 360":"Sportsnet 360",                   
                       "SPORTSNET ONE HD":"Sportsnet One",      
                       "SPORTSNET ONT":"Sportsnet Ontario",
                       "Sportsnet Ontarioario":"Sportsnet Ontario",     
                       "SPORTSNET WORLD HD":"Sportsnet World",              
                       "Starz Black HD - NEW":"Starz In Black",        
                       "Starz Edge HD - NEW":"Starz Edge",                   
                       "Starz HD - NEW":"Starz",      
                       "SUNDANCE HD":"Sundance",                    
                       "SyFy HD":"Syfy",              
                       "TBS HD":"TBS",        
                       "TCM EAST HD":"TCM",                   
                       "TCM HD - NEW":"TCM",                    
                       "Ten Sports HD":"Ten Sports Network",                   
                       "TENNIS HD":"Tennis Channel",      
                       "The Weather Channel USA":"The Weather Channel",                    
                       "TLC HD":"TLC",              
                       "TNT HD":"TNT",        
                       "TRAVEL HD":"Travel",   
                       "Travel Channel":"Travel",              
                       "TRAVEL XP HD":"Travel XP",      
                       "TREEHOUSE HD (NA)":"TREEHOUSE",                    
                       "TRU TV HD":"truTV",              
                       "TruTV HD":"truTV",        
                       "TSN 1 HD":"TSN1",                   
                       "TSN 2 HD":"TSN2",                                     
                       "TSN 3 HD":"TSN3",                    
                       "TSN 4 HD":"TSN4",   
                       "TSN 5 HD":"TSN5",                     
                       "TSN 1":"TSN1",                   
                       "TSN 2":"TSN2",                                     
                       "TSN 3":"TSN3",                    
                       "TSN 4":"TSN4",   
                       "TSN5":"TSN 5",
                       "TV LAND HD":"TV Land",        
                       "TVO HD (NA)":"TVO",                   
                       "USA HD":"USA Network",      
                       "USA Network HD":"USA Network",                    
                       "Velocity HD - NEW":"Velocity",              
                       "VEVO 1 HD":"Vevo 1",        
                       "VEVO 2 HD":"Vevo 2",                   
                       "VEVO 3 HD":"Vevo 3",                    
                       "VH1 Classics":"VH1 Classic",                                   
                       "VH1 HD":"VH1",                   
                       "VICELAND HD":"Viceland",      
                       "VIVID TV - NEW":"VIVID",                    
                       "W MOVIES HD - NEW":"W MOVIES",              
                       "W NETWORK HD - NEW":"W Network",        
                       "WE TV HD":"WE TV",                   
                       "WEATHER CANADA HD":"WEATHER CANADA",      
                       "WWE HD":"WWE Network",                    
                       "WWE NETWORK HD":"WWE Network",              
                       "YANKEES HD - NEW":"YANKEES",                      
                       "YTV HD (NA)":"YTV"
                      }
    #channelname_map = {}
    if args.namemap_file:
      with open(args.namemap_file) as f:
        for line in f:
          sp_line = line.rstrip(os.linesep).split("\t")
          channelname_map[sp_line[0]] = sp_line[1]
    inv_map = {v: k for k, v in my_map.items()}
    Channel = namedtuple('Channel', ['tvg_id', 'tvg_name', 'tvg_logo', 'group_title', 'channel_url'])
    channels = []
    online_groups = set()


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

    wanted_groups = sorted(online_groups)
    if args.groups:
      wanted_groups = args.groups.split(',')
    group_idx = {group:idx for idx,group in enumerate(wanted_groups)}
    # Has error if channel listings is different 
    #sys.stderr.write("Channel groups: {}\n".format(",".join(wanted_groups)))
    wanted_channels = [c for c in channels if c.group_title in wanted_groups]

    if args.guide_sort:
      wanted_channels.sort(key=lambda c: "{}-{}-{}".format(0 if c.tvg_id.endswith(".com") else 1, group_idx[c.group_title], c.tvg_name))
    else:
      wanted_channels.sort(key=lambda c: "{}-{}".format(group_idx[c.group_title], c.tvg_name))


    if args.channel_fn:
      #with open(args.channel_fn, 'w') as channel_f:
      with open(args.channel_fn, write_style) as channel_f:
        for c in wanted_channels:
          if c.tvg_id.endswith(".com"):
            if c.tvg_name in inv_map:
              channel_f.write("{}\n".format(inv_map[c.tvg_name]))
            else:
              channel_f.write("{}\n".format(c.tvg_id))

    #  append to addon.ini
    if args.ini_file:
      #args.ini_file = output_fn
      #with open(args.ini_file, "w") as f:
      #with open(dbPath + args.ini_file, "a") as f:
      with open(dbPath + args.ini_file, write_style) as f:
      #with open(dbPath + output_fn, write_style) as f:
        f.write('['+addon_name+'] \n;'+provider+'\n')
        for c in wanted_channels:
          f.write('{1}={4}.ts\n'.format(c.tvg_id, c.tvg_name, c.tvg_logo, c.group_title, c.channel_url))
      Clean_Names(dbPath + args.ini_file, basePath+'/_backup.ini')
      xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("TV Guide",args.ini_file+" done.",3000, icon))
      sys.exit()


    #else:
    # append to playlist.m3u
    #with codecs.open(output_fn, "w", 'utf-8') as f:
    #with codecs.open(dbPath + output_fn, "a", 'utf-8') as f:
    
    #with codecs.open(dbPath + output_fn, write_style, 'utf-8') as f:
    with codecs.open(dbPath + args.output_fn, write_style, 'utf-8') as f:    
      f.write('#EXTM3U\n#http://'+provider+'\n')
      for c in wanted_channels:
        #f.write('#EXTINF:-1 tvg-id="{0}" tvg-name="{1}" tvg-logo="{1}.png" group-title="{3}",{1}\n{4}\n'.format(c.tvg_id, c.tvg_name, c.tvg_logo, c.group_title, c.channel_url))
        f.write('#EXTINF:-1 tvg-logo="{1}.png",{1}\n{4}\n'.format(c.tvg_id, c.tvg_name, c.tvg_logo, c.group_title, c.channel_url))
  
    Clean_Names(dbPath + args.output_fn, basePath+'/_iptv.m3u') 
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("TV Guide",args.output_fn+" done.",3000, icon))
    sys.exit()
    #
    # append to addon.ini
    #with codecs.open(dbPath + 'addons2.ini', write_style, 'utf-8') as f:
    #  f.write("["+addon_name+"]\n")
    #  for c in wanted_channels:
    #    f.write('{1}={4}\n'.format(c.tvg_id, c.tvg_name, c.tvg_logo, c.group_title, c.channel_url)) 









def Copy_Favs_ini(Dest_File):
    favourites=xbmc.translatePath('special://profile/favourites.xml')
    s=open(favourites).read()
    s=s.replace('<favourites>', '')
    s=s.replace('</favourites>', '')
    s=s.replace('    <favourite name="', '')
    s=s.replace(')</favourite>', '')   
    s=s.replace('<favorites>"', '')
    s=s.replace('</favorites>', '')
    s=s.replace('    <favorite name="', '')
    s=s.replace(')</favorite>', '')    
    s=s.replace('quot;', '')      
    s=s.replace('amp;', '')    
    s=s.replace('[/COLOR]', '')   
    s=s.replace('&plugin', 'plugin')     
    #s=s.replace('" thumb="', '=')
    
    s=s.replace('	<favourite name="', '')  
    s=s.replace('	<favourite name="', '')
    #
    for line in s:
      sp_line = line.rstrip(os.linesep).split("\n")
      s=re.sub('thumb.*PlayMedia','=',s)
      s=s.replace('" =(', '=')
    #
    a=open(Dest_File,"a")
    #a.write('[plugin.program.echotvguide] \n')
    #a.write('['+addon_name+'] \n;'+provider+'\n')
    a.write('[plugin.program.echotvguide]') 
    a.write(s)
    a.close()  
    Clean_Names(Dest_File,basePath+'/_backup.ini') 



def Copy_Favs_m3u(Dest_File):
    favourites=xbmc.translatePath('special://profile/favourites.xml')
    s=open(favourites).read()
    s=s.replace('<favourites>', '')
    s=s.replace('</favourites>', '')
    #s=s.replace('    <favourite name="', '')
    s=s.replace('    <favourite name="', '#EXTINF:-1,')
    s=s.replace(')</favourite>', '')   
    s=s.replace('<favorites>"', '')
    s=s.replace('</favorites>', '')
    #s=s.replace('    <favorite name="', '')
    s=s.replace('    <favorite name="', '#EXTINF:-1,')
    s=s.replace(')</favorite>', '')    
    s=s.replace('quot;', '')      
    s=s.replace('amp;', '')   
    s=s.replace('[/COLOR]', '')
    s=s.replace('&plugin', 'plugin')   
    #
    for line in s:
      sp_line = line.rstrip(os.linesep).split("\n")
      s=re.sub('thumb.*PlayMedia','=',s)
      #s=s.replace('" =(', '=')
      s=s.replace('" =(', '\n')
    #      
    a=open(Dest_File,"a")
    a.write('#EXTM3U \n')
    #a.write('#EXTM3U\n#http://'+provider+'\n')
    a.write(s)
    a.close()  
    Clean_Names(Dest_File,basePath+'/_iptv.m3u') 
 
 
 
#  Copy_m3u_to_addon(addons2.ini) 
def Copy_m3u_to_addon(Dest_File):
    copytostuff=xbmc.translatePath(basePath+'/iptv.m3u')
    s=open(copytostuff).read()
    s=s.replace('#EXTM3U', '')
    s=s.replace('\n', '=')
    s=s.replace('#EXTINF: 1,', '\n')
    s=s.replace('  ==', '')
    #
    a=open(Dest_File,"a")
    #a.write('['+addon_name+'] \n;'+provider+'\n')
    a.write('[plugin.program.echotvguide] \n')
    a.write(s)
    a.close()  
    Clean_Names(Dest_File,basePath+'/_backup.ini')  
 


 

def Clean_Names(Clean_Name,tmpFile):
     #tmpFile = os.path.join(basePath, '_backup.ini')
     if os.path.exists(tmpFile):
         os.remove(tmpFile)
     os.rename(Clean_Name, tmpFile)
     s=open(tmpFile).read()

     #s=open(Clean_Name).read()
     #s=s.replace('Discovery SCIence','Discovery Science')
     #s=s.replace('Disney ','Disney Channel', 1)
     #s=s.replace('UK : FILM 4','Film4')
     #s=s.replace('UK : Film 4','Film4')
     #s=s.replace('UK : TCM','TCM')
     #s=s.replace('UK : TLC HD','TLC')
     #s=s.replace('*', '')
     #s=s.replace('- ', '')
     #s=s.replace('-', ' ')  
     #s=s.replace('USA: ', '')
     #s=s.replace(' : US', '') 
     #s=s.replace('UK : ', '')  
     #s=s.replace('UK: ', '')
     #s=s.replace(' : UK', '')
     #s=s.replace('SPORT: ', '') 
     #s=s.replace('XXX: ', '')      
     #s=s.replace('UK |  ', '')       
     #s=s.replace('-UK', '')
     #s=s.replace('USA  ', '')
     #s=s.replace('USA ', '')      
     #s=s.replace('|', '')      
     #s=s.replace(': ', '')    
     #s=s.replace('<favourites>', '')
     #s=s.replace('</favourites>', '')
     #s=s.replace(')</favourite>', '')   
     #s=s.replace('<favorites>"', '')
     #s=s.replace('</favorites>', '')
     
     s=s.replace('If you see this in log file doesnt exist','')

     #s=s.replace('=http://2.welcm.tv','=plugin://plugin.video.iptvsubs/?action=run_cronjob&url=http://2.welcm.tv')
     #s=s.replace('=http://2.welcm.tv','=plugin://plugin.video.iptvsubs/?action=run_cronjob&url=http://2.welcm.tv')
        
     #s=s.replace('%2c%22plugin%3a%2f%2f',',plugin://')        
        
     #s=re.sub('thumb.*PlayMedia','=',s)        
 
     s=s.replace('HD EAST - NEW','HD') 
     s=s.replace('HD EAST','HD')  
 
     s=s.replace('HD WEST - NEW','West') 
     s=s.replace('HD WEST','West')         
        
     s=s.replace('HD1','HD 1')
     s=s.replace('HD2','HD 2')     
     s=s.replace('HD3','HD 3')    
     s=s.replace('HD4','HD 4')
     s=s.replace('HD5','HD 5')         
     s=s.replace('USA: ', '')
     s=s.replace('USA:', '')
     s=s.replace('US: ', '')
     s=s.replace('US:', '')
     s=s.replace('USA  ', '')
     s=s.replace('UK |  ', '')
     s=s.replace('UK: ', '')
     s=s.replace('UK:', '')     
     s=s.replace('Usa: ', '')
     s=s.replace('Usa:', '')
     s=s.replace('Us: ', '')
     s=s.replace('Us:', '')
     s=s.replace('Usa  ', '')
     s=s.replace('Uk |  ', '')
     s=s.replace('Uk: ', '')
     s=s.replace('Uk:', '')     
     s=s.replace(' UK HD', 'UK')    
     s=s.replace('Usa: ', '')          
     s=s.replace(" : INT", '')     
     s=s.replace('SPORT: ', '') 
     s=s.replace('CANADA: ', '') 
     s=s.replace('CANADA:', '') 
     s=s.replace('XXX: ', '')     
     s=s.replace('XXX:', '') 
     s=s.replace('Test : ', '')
     s=s.replace('Test: ', '')   
     
     s=s.replace('UK - ', '')
     s=s.replace("INT - ", '')          
     s=s.replace(" - Chazza", '') 
     #s=s.replace('UK ', '')
     s=s.replace(' (US)', '')  
     s=s.replace(' (UK)', '')
     s=s.replace(' uk', 'UK')
     #s=s.replace('.UKtv', '') 
     s=s.replace('UKtv=', '=')  
 
     #s=s.replace(' HD ', '')
     #s=s.replace(' HD', '') 
     s=s.replace(' HD+', 'HD')
     s=s.replace(' [HD]', 'HD')
     s=s.replace(' SD', '')
     s=s.replace(' HDS', '')
     s=s.replace(' HQ', '') 
     s=s.replace(' TEST', '')                
     s=s.replace(' (AR)', '')
     s=s.replace(' (Arabic)', '')
     s=s.replace(' (Documentary)', '')
     s=s.replace(' (English)', '')
     s=s.replace(' (Entertainment)', '')
     s=s.replace(' (Family)', '')
     s=s.replace(' (FR)', '')
     s=s.replace(' (French)', '')
     s=s.replace(' (IN)', '')
     s=s.replace(' (JH)', '')
     s=s.replace(' (JU)', '')
     s=s.replace(' (Maybe Geo-Blocked)', '') 
     s=s.replace(' (MO)', '')
     s=s.replace(' (Movie Channels)', '')
     s=s.replace(' (Music)', '')
     s=s.replace(' (News)', '')
     s=s.replace(' (QA)', '')
     s=s.replace(' (RS)', '')
     s=s.replace(' (RU)', '')
     s=s.replace(' (SA)', '')
     s=s.replace(' (Serbian)', '')
     s=s.replace(' (Spanish)', '')
     s=s.replace(' (Sports)', '')
     s=s.replace(' (Top10)', '')
     s=s.replace('(1080p)', '')
     s=s.replace('(720p)', '')
     s=s.replace(' 1080p', '')
     s=s.replace(' 1080i', '')
     s=s.replace(' 720p', '')
     s=s.replace(' ( 1080i )', '')     
     s=s.replace(' ( )', '')     

     s=s.replace(' Duel Audio', '') 

     s=s.replace('[/B]', '')
     s=s.replace('[/COLOR]', '')
     s=s.replace('[B]', '')
     s=s.replace('[COLOR blue]', '')
     s=s.replace('[COLOR green]', '')
     s=s.replace('[COLOR limegreen]', '')
     s=s.replace('[COLOR red]', '')
     s=s.replace('[COLOR white]', '')
     s=s.replace('[COLOR yellow]', '')
     s=s.replace('[COLORlime]', '')
     s=s.replace('[COLOR lime]', '')
     s=s.replace('[COLOR white]Sky Sports News[/COLOR]','Sky Sports News')        
     s=s.replace('=====UNITED KINGDOM LIVE CHANNELS======','UK=')         

     s=s.replace('3 e','3e')
     s=s.replace('3E','3e')
     s=s.replace('Sky 3e','3e')         
         
     s=s.replace('4 seven','4Seven')
     s=s.replace('4 SEVEN','4Seven')    
     
     s=s.replace('4MUSIC','4Music')
     s=s.replace('4music','4Music')
     s=s.replace('4SEVEN','4Seven')
     s=s.replace('4seven','4Seven')
     
     s=s.replace('5*','5Star')     
     s=s.replace('5 STAR','5Star')
     s=s.replace('5 star','5Star')
     s=s.replace('5 Star','5Star')
     s=s.replace('5STAR','5Star')
     s=s.replace('Sky 5Star','5Star')
     
     s=s.replace('5Star MAX HD - NEW','5StarMax')
     s=s.replace('5Star MAX HD','5StarMax')
     s=s.replace('Cinemax 5StarMax','5StarMax')
          
     s=s.replace('5 USA','5USA')
     s=s.replace('5 usa','5USA')
     s=s.replace('5usa','5USA')
     s=s.replace('Sky 5USA','5USA')
     
     s=s.replace('A+E HD','A&E')     
     s=s.replace('A&E HD','A&E') 
     s=s.replace('A and E', 'A&E')
     s=s.replace('A AND E','A&E')
     s=s.replace('A&amp;E','A&E') 
     s=s.replace('A&E  test','A&E')      
     
          
     s=s.replace('ACTION HD','ACTION')          

     s=s.replace('Abc=','ABC=')
     s=s.replace('ABC 7 New York','ABC HD')
     s=s.replace('ABC New York','ABC HD')
     s=s.replace('Abc HD','ABC HD') 
     s=s.replace('ABC  HD','ABC HD') 
          
     s=s.replace('ABC Miami','ABC West')


     s=s.replace('USA ABC News','ABC News')
     s=s.replace('ABCNEWS','ABC News')
     s=s.replace('ABC NEWS HD','ABC News')
     s=s.replace('ABC NEWS','ABC News')     
          
     s=s.replace('ActionMAX','ActionMax')
     s=s.replace('ACTIONMAX','ActionMax')
     s=s.replace('actionmax','ActionMax')
     s=s.replace('ActnMAX','ActionMax')
     s=s.replace('ActnMAXHD','ActionMax')
     s=s.replace('ACTION MAX HD - NEW','ActionMax')
     s=s.replace('ACTION MAX HD','ActionMax')
          
     s=s.replace('Alibi SD','Alibi')     
     s=s.replace('ALIBI','Alibi')
     s=s.replace('alibi','Alibi')
     s=s.replace('Sky Alibi','Alibi')
          
     s=s.replace('ALJAZEERA ENGLISH','Aljazeera')          
         

     s=s.replace('AMC East HD','AMC HD')
     
     s=s.replace('AMC East','AMC')
     s=s.replace('AMC US','AMC')
     s=s.replace('Amc','AMC')
     
     s=s.replace('USA AMC','AMC HD')
     
          
     s=s.replace('AMC HD from BT','AMC UK')
     s=s.replace('AMC HD - EU LINK','AMC UK')
     
     s=s.replace('ANIMAL PLANET HD - NEW','Animal Planet')
     s=s.replace('Animal Planet HD','Animal Planet')
     s=s.replace('ANIMAL PLANET','Animal Planet')
     s=s.replace('animal planet','Animal Planet')
     s=s.replace('USA Animal Planet','Animal Planet')

     s=s.replace('Sky Animal Planet','Animal Planet UK')
     
     s=s.replace('Arena Sport 1','Arenasport 1')
     s=s.replace('Arena Sport 2','Arenasport 2')
     s=s.replace('Arena Sport 3','Arenasport 3')
     s=s.replace('Arena Sport 4','Arenasport 4')
     s=s.replace('ARENA SPORTS 1','Arenasport 1')
     s=s.replace('ARENA SPORTS 2','Arenasport 2')
     s=s.replace('ARENA SPORTS 3','Arenasport 3')
     s=s.replace('ARENA SPORTS 4','Arenasport 4')
     
     s=s.replace('Astro super Sport 1','Astro SuperSport 1')
     s=s.replace('Astro super Sport 2','Astro SuperSport 2')
     s=s.replace('Astro super Sport 3','Astro SuperSport 3')
     s=s.replace('ASTRO SUPERSPORT 1','Astro SuperSport 1')
     s=s.replace('ASTRO SUPERSPORT 2','Astro SuperSport 2')
     s=s.replace('ASTRO SUPERSPORT 3','Astro SuperSport 3')
     s=s.replace('Astro Supersports 1 HD','Astro SuperSport 1')
     s=s.replace('Astro Supersports 2 HD','Astro SuperSport 2')
     s=s.replace('Astro Supersports 3 HD','Astro SuperSport 3')

     s=s.replace('Astro Supersports 4 HD','Astro SuperSport 4')

     s=s.replace('AT THE RACES HD','At The Races')
     s=s.replace('AT THE RACES','At The Races')
     s=s.replace('at the races','At The Races')
     s=s.replace('At The RacesS',' At The Races')

     s=s.replace('BABY TV','Baby TV')
     s=s.replace('baby tv','Baby TV')
     
     s=s.replace('Bbc America','BBC America')     
     s=s.replace('BBC AMERICA HD','BBC America') 

     s=s.replace('BBC One HD','BBC1')         
     s=s.replace('bbc 1','BBC1')
     s=s.replace('BBC 1','BBC1')
     s=s.replace('BBC One London ','BBC1')
     s=s.replace('bbc one','BBC1')
     s=s.replace('BBC ONE','BBC1')
     s=s.replace('bbc1','BBC1')          
     s=s.replace('BBC One','BBC1')
     s=s.replace('BBC HD 1','BBC1')
          
     s=s.replace('BBC Two HD','BBC2')          
     s=s.replace('bbc 2','BBC2')
     s=s.replace('BBC 2','BBC2')
     s=s.replace('BBC Two England ','BBC2')
     s=s.replace('BBC TWO','BBC2')   
     s=s.replace('bbc2','BBC2')
     s=s.replace('BBCTWO','BBC2')     
     s=s.replace('BBC Two','BBC2')
     s=s.replace('BBC HD 2','BBC2')
          
     s=s.replace('BBC Three HD','BBC3')
     s=s.replace('BBC 3','BBC3')
     s=s.replace('Bbc 3','BBC3')
     s=s.replace('bbc three','BBC3')
     s=s.replace('BBC3','BBC3')
     s=s.replace('Bbc3','BBC3')
     s=s.replace('bbc3','BBC3')     
     s=s.replace('BBCTHREE','BBC3')     
     s=s.replace('BBC THREE','BBC3')  
     s=s.replace('BBC Three','BBC3')  
     s=s.replace('BBC HD 3 / CBBC HD','BBC3') 
               
     s=s.replace('BBC Four HD','BBC4')     
     s=s.replace('BBC 4','BBC4')
     s=s.replace('Bbc 4','BBC4')
     s=s.replace('bbc four','BBC4')
     s=s.replace('BBC4','BBC4')
     s=s.replace('Bbc4','BBC4')
     s=s.replace('bbc4','BBC4')
     s=s.replace('BBCFOUR','BBC4')     
     s=s.replace('BBC FOUR','BBC4')
     s=s.replace('BBC Four','BBC4')
     s=s.replace('BBC HD 4 / CBeebies HD','BBC4')
               
     s=s.replace('BBC NEWS','BBC News')
     s=s.replace('BBC News Channel','BBC News')
         
     s=s.replace('BBC WORLD NEWS','BBC World News')

     s=s.replace('BC1 HD - NEW','BC1')
     s=s.replace('BC1 HD','BC1')
         
     
     
     s=s.replace('BEIN SPORTS 1 HD','bein-sports-1hd')
     s=s.replace('BEIN SPORTS 1','bein-sports-1hd')
     s=s.replace('Bein Sports 1','bein-sports-1hd')
     
     s=s.replace('BEIN SPORTS 10 HD','bein-sports-10hd')
     s=s.replace('BEIN SPORTS 10','bein-sports-10hd')
     s=s.replace('Bein Sports 10','bein-sports-10hd')

     s=s.replace('BEIN SPORTS 11 HD','bein-sports-11hd')
     s=s.replace('BEIN SPORTS 11','bein-sports-11hd')
     s=s.replace('Bein Sports 11','bein-sports-11hd')

     s=s.replace('BEIN SPORTS 12 HD','bein-sports-12hd')
     s=s.replace('BEIN SPORTS 12','bein-sports-12hd')
     s=s.replace('Bein Sports 12','bein-sports-12hd')

     s=s.replace('BEIN SPORTS 14 HD','bein-sports-14hd')
     s=s.replace('BEIN SPORTS 13 HD','bein-sports-13hd')
     s=s.replace('BEIN SPORTS 13','bein-sports-13hd')

     s=s.replace('BEIN SPORTS 15 HD','bein-sports-15hd')

     s=s.replace('BEIN SPORTS 16 HD','bein-sports-16hd')

     s=s.replace('BEIN SPORTS 2 HD','bein-sports-2hd')
     s=s.replace('BEIN SPORTS 2','bein-sports-2hd')
     s=s.replace('Bein Sports 2','bein-sports-2hd')
     s=s.replace('Bein Sports 2','bein-sports-2hd')

     s=s.replace('BEIN SPORTS 3 HD','bein-sports-3hd')
     s=s.replace('BEIN SPORTS 3','bein-sports-3hd')

     s=s.replace('BEIN SPORTS 4 HD','bein-sports-4hd')
     s=s.replace('BEIN SPORTS 4','bein-sports-4hd')
     s=s.replace('Bein Sports 4','bein-sports-4hd')

     s=s.replace('BEIN SPORTS 5 HD','bein-sports-5hd')
     s=s.replace('BEIN SPORTS 5','bein-sports-5hd')
     s=s.replace('Bein Sports 5','bein-sports-6hd')

     s=s.replace('BEIN SPORTS 6 HD','bein-sports-6hd')
     s=s.replace('BEIN SPORTS 6','bein-sports-6hd')
     s=s.replace('Bein Sports 6','bein-sports-6hd')

     s=s.replace('BEIN SPORTS 7 HD','bein-sports-7hd')
     s=s.replace('BEIN SPORTS 7','bein-sports-7hd')
     s=s.replace('Bein Sports 7','bein-sports-7hd')

     s=s.replace('BEIN SPORTS 8 HD','bein-sports-8hd')
     s=s.replace('BEIN SPORTS 8','bein-sports-8hd')
     s=s.replace('Bein Sports 8','bein-sports-8hd')

     s=s.replace('BEIN SPORTS 9 HD','bein-sports-9hd')
     s=s.replace('BEIN SPORTS 9','bein-sports-9hd')
     s=s.replace('Bein Sports 9','bein-sports-9hd')

     s=s.replace('BEIN HD','BEINS1')
     s=s.replace('BEIN SPORTS HD','BEINS1')
     s=s.replace('BEIN SPORTS HD','BEINS1')
     s=s.replace('USA Bein USA','BEINS1')
     s=s.replace('BEIN Sports 1','BEINS1')
                         
     s=s.replace('BEIN SPORTS NEWS HD','bein-sports-news')
     s=s.replace('BEIN SPORTS NEWS','bein-sports-news')

     s=s.replace('BIEN SPORTS 1 HD','Bein-sports-1hd') 
     s=s.replace('BeinSports 1','bein-sports-1hd')
     s=s.replace('BeinSports 10','bein-sports-10hd')
     s=s.replace('BeinSports 11','bein-sports-11hd')
     s=s.replace('BeinSports 12','bein-sports-12hd')
     s=s.replace('BeinSports 13','bein-sports-13hd')
     s=s.replace('BeinSports 14','bein-sports-14hd')
     s=s.replace('BeinSports 15','bein-sports-15hd')
     s=s.replace('BeinSports 16','bein-sports-16hd')
     s=s.replace('BeinSports 2','bein-sports-2hd')
     s=s.replace('BeinSports 2','bein-sports-2hd')
     s=s.replace('BeinSports 4','bein-sports-4hd')
     s=s.replace('BeinSports 5','bein-sports-6hd')
     s=s.replace('BeinSports 6','bein-sports-6hd')
     s=s.replace('BeinSports 7','bein-sports-7hd')
     s=s.replace('BeinSports 8','bein-sports-8hd')
     s=s.replace('BeinSports 9','bein-sports-9hd')
     
     s=s.replace('BET HD','BET') 
          
     s=s.replace('BIG TEN NETWORK','Big Ten Network')
     s=s.replace('big ten network','Big Ten Network')
     s=s.replace('Big Ten Network HD','Big Ten Network')
          
     s=s.replace('BLOOMBERG TV','Bloomberg')
     s=s.replace('BLOOMBERG HD','Bloomberg')
     s=s.replace('BLOOMBERG','Bloomberg')     
     s=s.replace('Bloomberg HD','Bloomberg')  

     s=s.replace('BNN HD - NEW','BNN') 
     s=s.replace('BNN HD','BNN') 
         
     s=s.replace('BOOMERANG','Boomerang')
     s=s.replace('boomerang','Boomerang')

     s=s.replace('BOUNCE HD - NEW','Bounce')
     s=s.replace('BOUNCE HD','Bounce')

     s=s.replace('SKY Box Nation','BoxNation')
     s=s.replace('BOXNATION','BoxNation')
     s=s.replace('BOX NATION','BoxNation')
     s=s.replace('Boxnation','BoxNation')
     s=s.replace('BOX_NATION','BoxNation')
     s=s.replace('SKY BoxNation','BoxNation')
               
     s=s.replace('BRAVO HD','Bravo')
     s=s.replace('BRAVO','Bravo')

     s=s.replace('BRITISH EUROPORT 1','EuroSport 1')
     s=s.replace('BRITISH EUROSPORT 1 HD','Eurosport 1')
     s=s.replace('British Eurosport 1','Eurosport 1')
     
     s=s.replace('BRITISH EUROPORT 2','EuroSport 2')
     s=s.replace('BRITISH EUROSPORT 2 HD','Eurosport 2')
     s=s.replace('British Eurosport 2','Eurosport 2')

     s=s.replace('BT Sport 1HD','BT Sport 1 HD')
     s=s.replace('BT SPort 1 HD','BT Sport 1 HD')
     s=s.replace('UK BT Sport 1 HD','BT Sport 1 HD')
     s=s.replace('Sky BT Sport 1 HD','BT Sport 1 HD')
     s=s.replace('BT Sports 1 HD','BT Sport 1 HD')
     s=s.replace('BT_SPORTS_1HD','BT Sport 1 HD')
                    
     s=s.replace('SKY BT 1','BT Sport 1')
     s=s.replace('BT SPORT 1','BT Sport 1')
     s=s.replace('BT sport 1','BT Sport 1')
     s=s.replace('BT Sport 1UK','BT Sport 1')     
     s=s.replace('Sky BT Sport 1','BT Sport 1')
     
     s=s.replace('BT sport 2 HD','BT Sport 2 HD')
     s=s.replace('UK BT Sport 2 HD','BT Sport 2 HD')
     s=s.replace('Sky BT Sport 2 HD','BT Sport 2 HD')
     s=s.replace('BT Sports 2 HD','BT Sport 2 HD')
     s=s.replace('BT_SPORTS_2HD','BT Sport 2 HD')
                    
     s=s.replace('BT SPort 2','BT Sport 2')
     s=s.replace('SKY BT 2','BT Sport 2')
     s=s.replace('BT SPORT 2','BT Sport 2')
     s=s.replace('bt sport 2','BT Sport 2')
     s=s.replace('BT Sport 2UK','BT Sport 2')  
     s=s.replace('Sky BT Sport 2','BT Sport 2')
     
     s=s.replace('BT Sport EUROPE HD','BT Sport Europe')
     s=s.replace('BT Sport Europe HD','BT Sport Europe')
     s=s.replace('BT sport europe HD','BT Sport Europe')
     s=s.replace('BT Sport EUROPE','BT Sport Europe')
     s=s.replace('BT SPORT EUROPE','BT Sport Europe')

     s=s.replace('CARTOON NETWORK HD (NA)','Cartoon Network') 
     s=s.replace('CARTOON NETWORK HD','Cartoon Network')
     s=s.replace('CARTOON NETWORK US','Cartoon Network')
     s=s.replace('cartoon network','Cartoon Network')
     s=s.replace('CARTOON NETWORK UK','Cartoon Network UK')
     s=s.replace('CARTOON NETWORK','Cartoon Network')
     s=s.replace('Cartoon N.','Cartoon Network')
     s=s.replace('CARTOONNETWORK','Cartoon Network')
     s=s.replace('CARTOON_NETWORK','Cartoon Network')
                         
     s=s.replace('CARTOONIO','Cartoonio')
     s=s.replace('cartoonio','Cartoonio')

     s=s.replace('SKY CBBC HD','CBBC') 
               
     s=s.replace('CBEEBIES','CBeebies')
     s=s.replace('cbeebies','CBeebies')
     
     #s=s.replace('Cbc','CBC')       
     s=s.replace('CBC EAST HD','CBC') 

     s=s.replace('CBC VANCOUVER HD- NEW','CBC Vancouver') 
     s=s.replace('CBC VANCOUVER HD','CBC Vancouver')
              
     s=s.replace('CBC NEWS HD','CBC News')   
     s=s.replace('CBC NEWS','CBC News')         
  
     s=s.replace('CBS NEWS HD','CBS News')   
     s=s.replace('CBS NEWS','CBS News')     

     s=s.replace('CBS East HD','CBS HD')   
     s=s.replace('CBS East','CBS HD')  
     s=s.replace('Cbs HD','CBS HD')
     s=s.replace('CBS New York','CBS HD')     

     s=s.replace('CBS Miami','CBS')     
     s=s.replace('Cbs=','CBS=')

     s=s.replace('CBS ACTION','CBS Action')
     s=s.replace('cbs action','CBS Action')
     s=s.replace('CBS ACTION','CBS Action')
     s=s.replace('cbs action','CBS Action')

     s=s.replace('CBS DRAMA','CBS Drama')
     s=s.replace('cbs DRAMA','CBS Drama')
     s=s.replace('CBS_Drama','CBS Drama')
     
     s=s.replace('CBS REALITY','CBS Reality')
     s=s.replace('cbs reality','CBS Reality')
     
     s=s.replace('CBS REALITY+1','CBS Reality +1')    
     
     s=s.replace('CBS SPORTS HD','CBS Sports Network')
     s=s.replace('CBS SPORTS','CBS Sports Network')
          
     s=s.replace('CHALLENGE','Challenge')

     s=s.replace('Sky Channel 4','Channel 4')     
     s=s.replace('CHANNEL 4','Channel 4')
     s=s.replace('channel 4','Channel 4')
     s=s.replace('CHANNEL4','Channel 4')
     s=s.replace('channel4','Channel 4')
     s=s.replace('Channel4','Channel 4')
     
     s=s.replace('Sky Channel 5','Channel 5')
     s=s.replace('CHANNEL 5','Channel 5')
     s=s.replace('channel 5','Channel 5')
     s=s.replace('CHANNEL5','Channel 5')
     s=s.replace('channel5','Channel 5')

     s=s.replace('SKY CHELSEA TV','Chelsea TV')
     s=s.replace('CHELSEA TV','Chelsea TV')
     s=s.replace('CHELSEA','Chelsea TV')
     s=s.replace('Chelsea tv','Chelsea TV')
     
     #s=s.replace('CI','CI')
     #s=s.replace('ci','CI')
     #s=s.replace('Crime & Investigation','CI')     
     s=s.replace('Crime and Investigatic','Crime and Investigation')  
               
     s=s.replace('CHCH HD','CHCH')     

     s=s.replace('CineMAX','Cinemax')
     s=s.replace('cinemax','Cinemax')
     s=s.replace('CINEMAX','Cinemax')
     s=s.replace('Cinemax EAST HD - NEW','Cinemax')     
     s=s.replace('Cinemax EAST HD','Cinemax')
     s=s.replace('Cinemax HD','Cinemax')
          
     s=s.replace('CineMAX (pacific)','Cinemax West')
     s=s.replace('CINEMAX PACIFIC','Cinemax West')
     s=s.replace('CINEMAX WEST','Cinemax West')
     s=s.replace('cinimax west','Cinimax West')

     s=s.replace('Cinemax MoreMax HD','Cinemax MoreMax')

     #s=s.replace('citv','CITV')

     s=s.replace('CITY TV HD','City TV Toronto')
     s=s.replace('CityTV','City TV Toronto')

     s=s.replace('CITY VANCOUVER HD - NEW','City TV Vancouver')
     s=s.replace('CITY VANCOUVER HD','City TV Vancouver')

          
     s=s.replace('CNN HD','CNN')
     s=s.replace('Cnn','CNN')
     s=s.replace('CNN US','CNN') 
     s=s.replace('CNNUS','CNN') 
     s=s.replace('CNN_LIVE','CNN') 
     s=s.replace('CNN_NEWS','CNN')
                            
     s=s.replace('CNN INTERNATIONAL','CNN International')
     
     s=s.replace('CNBC HD','CNBC') 
     s=s.replace('USA CNBC','CNBC') 
          
     s=s.replace('CNBC uk','CNBC UK')      

     s=s.replace('COMADY CENTRAL','Comedy Central')
     s=s.replace('comady central','Comedy Central')
     s=s.replace('Comedy Central US','Comedy Central')
     s=s.replace('COMEDY CENTRAL HD','Comedy Central')
     s=s.replace('COMEDY CENTRAL','Comedy Central')
     s=s.replace('comedy central','Comedy Central')
     s=s.replace('Comedy central','Comedy Central')
          
     s=s.replace('COMEDY CENTRAL UK','Comedy Central UK')
     s=s.replace('Comedy Central uk','Comedy Central UK')
     
     s=s.replace('COMEDY CENTRAL EXTRA','Comedy Central Extra')
     s=s.replace('Comedy Central EXTRA','Comedy Central Extra')
     s=s.replace('Comedy Central Ex=','Comedy Central Extra=')
           
     s=s.replace('COMEDY NETWORK HD','Comedy Network') 

     s=s.replace('Cooking Channel HD','Cooking Channel') 
 
     s=s.replace('CP 24','CP24')
     s=s.replace('CP24 HD','CP24')     
          
     s=s.replace('CTV Edmonton','CTV Edmonton')     
     s=s.replace('CFRN CTV Edmonton','CTV Edmonton')
          
     s=s.replace('CTV Regina','CTV Regina')     
     s=s.replace('CKCK CTV Regina','CTV Regina')
     
     s=s.replace('CICC CTV Yorkton','CTV Yorkton')

     s=s.replace('CTV VANCOUVER HD - NEW','CTV Vancouver')
     s=s.replace('CTV VANCOUVER HD','CTV Vancouver')
     
     s=s.replace('CTV NORTH','CTV North')
               
     s=s.replace('CTV EAST HD','CTV Toronto')
     s=s.replace('CTV=','CTV Toronto=')
                    
     s=s.replace('CTH STADIUM 1 HD','CTH Stadium 1')
     s=s.replace('CTH STADIUM 1','CTH Stadium 1')

     s=s.replace('CTH STADIUM 2 HD','CTH Stadium 2')
     s=s.replace('CTH STADIUM 2','CTH Stadium 2')

     s=s.replace('CTH STADIUM 3 HD','CTH Stadium 3')
     s=s.replace('CTH STADIUM 3','CTH Stadium 3')

     s=s.replace('CTH STADIUM 4 HD','CTH Stadium 4')
     s=s.replace('CTH STADIUM 4','CTH Stadium 4')

     s=s.replace('CTH STADIUM 5 HD','CTH Stadium 5')
     s=s.replace('CTH STADIUM 5','CTH Stadium 5')

     s=s.replace('CTH STADIUM 6 HD','CTH Stadium 6')
     s=s.replace('CTH STADIUM 6','CTH Stadium 6')

     s=s.replace('CTH STADIUM X HD','CTH Stadium X')
     s=s.replace('CTH STADIUM X','CTH Stadium X')

     s=s.replace('Cw','CW')
     s=s.replace('CW HD','CW')
     s=s.replace('CW11 HD','CW')
     s=s.replace('CW (PIX)','CW')
     s=s.replace('The CW Network','CW')
          
     s=s.replace('Sky Dave','Dave')              
     s=s.replace('DAVE','Dave')
     s=s.replace('dave','Dave')
     s=s.replace('Dave HD','Dave')
     
     s=s.replace('DISCOVERY HD','Discovery')
     s=s.replace('DISCOVERYHD','Discovery')
     s=s.replace('DISCOVERY CHANNEL HD','Discovery')
     s=s.replace('DISCOVERY CHANNEL','Discovery')
     s=s.replace('discovery channel','Discovery')
     s=s.replace('DISCOVERYHD','Discovery')
     s=s.replace('DISCOVERY','Discovery')
     s=s.replace('DiscoveryHD','Discovery')
     s=s.replace('Discovery HD','Discovery')
               
     s=s.replace('Discovery uk','Discovery UK')
     #s=s.replace('Sky Discovery','Discovery UK')
     
     s=s.replace('DISCOVERY HISTORY','Discovery History')
     s=s.replace('discovery history','Discovery History')

     s=s.replace('Sky Discovery History','Discovery History UK')
     
     s=s.replace('DISCOVERY HOME AND HEALTH','Discovery Home And Health')
 
     s=s.replace('Sky Discovery Science','Discovery Science')    
     s=s.replace('DISCOVERY SCIENCE ','Discovery Science')
     s=s.replace('DISCOVERY SCIENCE','Discovery Science')
     s=s.replace('discovery science','Discovery Science')
     s=s.replace('Discovery SCIence UK','Discovery Science')
     s=s.replace('Discovery SCIence','Discovery Science')
     s=s.replace('Discovery SCIENCE','Discovery Science')
     s=s.replace('Discovery UK SCIence','Discovery Science')
     s=s.replace('SCIence','Science')
     s=s.replace('Discovery Science HD','Discovery Science')
     s=s.replace('Discovery Sci=','Discovery Science=')
                                   
     s=s.replace('Sky Discovery Shed','Discovery Shed')
     s=s.replace('DISCOVERY SHED','Discovery Shed')
     s=s.replace('discovery shed','Discovery Shed')
     s=s.replace('Discovery UK Shed','Discovery Shed')
     
     s=s.replace('DISCOVERY TURBO','Discovery Turbo')
     s=s.replace('discovery turbo','Discovery Turbo')
     
     s=s.replace('DISCOVERY INVESTIGATION','Discovery Investigation')
     s=s.replace('discovery investigation','Discovery Investigation')
     s=s.replace('Discovery investigation','Discovery Investigation')
     s=s.replace('Sky Discovery Investigation','Discovery Investigation')
     s=s.replace('Discovery ID','Discovery Investigation')
     s=s.replace('Discovery UK investigation','Discovery Investigation')
           
     s=s.replace('Disney HD East - NEW','Disney')
     s=s.replace('Disney HD East','Disney')
     s=s.replace('DISNEY CHANNEL HD','Disney')
     s=s.replace('DISNEY CHANNEL','Disney')
     s=s.replace('disney channel','Disney')
     s=s.replace('DisneyChnl','Disney')       
     s=s.replace('Disney Channel','Disney')  
     s=s.replace('DISNEY_CHANNEL','Disney')  
     s=s.replace('DISNEY HD EAST','Disney')
     s=s.replace('DISNEY HD','Disney')
                                   
     s=s.replace('Disney Channel UK','Disney UK')                   
     s=s.replace('Sky Disney Chaneel HD','Disney UK')
                    
     s=s.replace('Disney Jr .','Disney Jr')
     s=s.replace('DISNEY JUNIOR ','Disney Jr')
     s=s.replace('DISNEY JUNIOR','Disney Jr')
     s=s.replace('disney junior','Disney Jr')
     s=s.replace('Disney Junior','Disney Jr')
     
     s=s.replace('SKY DISNEY JR (UK)','Disney Jr UK')
     s=s.replace('Disney Jr. UK','Disney Jr UK')
     s=s.replace('Disney JrUK','Disney Jr UK')
     s=s.replace('Sky Disney Jr HD','Disney Jr UK')
     s=s.replace('Sky Movies Disney JR','Disney Jr UK')
               
     s=s.replace('DISNEY XD','Disney XD')
     s=s.replace('disney XD','Disney XD')
     s=s.replace('DISNEY XD HD (NA)','Disney XD')
     s=s.replace('DISNEY XD HD','Disney XD')
     s=s.replace('DISNEY_XD','Disney XD')
     s=s.replace('DISNEY_XD','Disney XD')
               
     s=s.replace('SKY DISNEY XD HD (UK)','Disney XD UK')
     s=s.replace('SKY Disney XD','Disney XD UK')
               
     s=s.replace('DIY HD','DIY')
     
     s=s.replace('dmax','DMAX')
     s=s.replace('Dmax','DMAX')
     
     s=s.replace('DRAMA','Drama')
     s=s.replace('drama','Drama')

     s=s.replace('E! HD','E!') 
     s=s.replace('E! entertainment','E!')  
     s=s.replace('E! Entertainment','E!') 
     s=s.replace('e! entertainment','E!')     
     s=s.replace('e!','E!')
     s=s.replace('E! (CA)','E!')
     
     s=s.replace('E4','E4')
     #s=s.replace('e4','E4')
     
     s=s.replace('EDEN','Eden')
     s=s.replace('eden','Eden')

     s=s.replace('ENCORE','Encore')
     s=s.replace('encore','Encore')

     s=s.replace('Encore WESTERN HD - NEW','Encore Western')

     s=s.replace('ENCORE ACTION','Encore Action')

     s=s.replace('ESPN 2 HD','ESPN2') 
     s=s.replace('espn 2','ESPN2')
     s=s.replace('ESPN 2','ESPN2')
     s=s.replace('ESPN 2 LA','ESPN2')     
     s=s.replace('USA ESPN2','ESPN2') 
     
     s=s.replace('ESPN HD','ESPN')          
     s=s.replace('ESPN US','ESPN')
     s=s.replace('ESPN LA','ESPN')
     s=s.replace('espn','ESPN')
     s=s.replace('USA ESPNA','ESPN')
     s=s.replace('ESPN_HD','ESPN')
               
     s=s.replace('ESPN uk','ESPN UK')

     s=s.replace('ESPNEWS','ESPNews')     
     s=s.replace('ESPN NEWS HD','ESPNews')
     
     s=s.replace('ESPN U','ESPNU')  
     s=s.replace('ESPNU HD','ESPNU') 
     
     s=s.replace('Esquire Network HD','Esquire')  
     
     s=s.replace('EURO NEWS','Euro News')
     
     s=s.replace('EUROSPORT HD','Eurosport')
     s=s.replace('EUROSPORT','Eurosport')
     s=s.replace('EurosportS 1','Eurosport')
     s=s.replace('Eurosport UK','Eurosport')
     s=s.replace('Eurosport 1','Eurosport')
          
     s=s.replace('EUROSPORT 2 HD','Eurosport 2')
     s=s.replace('EUROSPORT 2','Eurosport 2')
     s=s.replace('EurosportS 2','Eurosport 2')
     s=s.replace('Eurosport 2 UK','Eurosport 2')
     s=s.replace('Eurosport 2 HD','Eurosport 2')
               
     s=s.replace('FAMILY HD (NA)','FAMILY')     

     s=s.replace('Sky Film4','Film4')     
     s=s.replace('FILM 4','Film4')
     s=s.replace('film4','Film4')
     s=s.replace('FILM 4','Film4')
     s=s.replace('Film 4','Film4')
     s=s.replace('Film4 UK','Film4')
     s=s.replace('Film4 HD','Film4')
     s=s.replace('FILM4','Film4')
                         
     s=s.replace('flava','Flava')
     s=s.replace('FLAVA','Flava')
 
     s=s.replace('FOOD HD','Food Network')
     s=s.replace('Food Network HD','Food Network')
     s=s.replace('FOOD NETWORK','Food Network')
     s=s.replace('food network','Food Network')
     s=s.replace('FOOD Network','Food Network')
     s=s.replace('FOOD=','Food Network=')
         
     s=s.replace('FOOD NETWORK UK','Food Network UK')
   
     s=s.replace('fox','FOX')
     s=s.replace('Fox HD','FOX HD')
     s=s.replace('Fox East','FOX HD')  
     s=s.replace('FOX43 HD','FOX HD')      
     
        
     s=s.replace('Fox=','FOX=') 
     s=s.replace('fox','FOX')
     s=s.replace('Fox Miami','FOX')
     s=s.replace('FOX5 HD','FOX') 
               
     s=s.replace('Fox UK','FOX UK')    
     
     s=s.replace('FOX AMERICA','Fox News')
     s=s.replace('FOX NEWS HD','Fox News')
     s=s.replace('FOX NEWS','Fox News')
     s=s.replace(' Fox News','Fox News')
         
     s=s.replace('FOX SPORTS 1 HD','Fox Sports 1 HD')
     s=s.replace('Fox Sports HD','Fox Sports 1 HD')
          
     s=s.replace('fox SPORTS 1','Fox Sports 1')
     s=s.replace('fox sports 1','Fox Sports 1')
     s=s.replace('FOX Sports 1','Fox Sports 1')
     s=s.replace('Fox Sport 1','Fox Sports 1')
     
               
     s=s.replace('FOX SPORTS 2 HD','Fox Sports 2 HD')
     
     s=s.replace('fox SPORTS 2','Fox Sports 2')
     s=s.replace('fox sports 2','Fox Sports 2')
     s=s.replace(' FOX Sports 2','Fox Sports 2')
     s=s.replace('FOX Sports 2','Fox Sports 2')
          
     s=s.replace('FXX HD','FXX') 
     s=s.replace('Fxx','FXX') 
     s=s.replace('FXX WEST','FXX') 
     
     s=s.replace('FX HD','FX') 
     s=s.replace('Fx','FX') 

     s=s.replace('Global Halifax','Global Maritimes')
     
     s=s.replace('GLOBAL EAST HD','Global Toronto')     
     s=s.replace('GLOBAL TV','Global Toronto') 
     s=s.replace('Global tv (CA)','Global Toronto') 
     s=s.replace('Global tv','Global Toronto') 
     
     s=s.replace('GLOBAL BC HD - NEW','Global Vancouver')
     s=s.replace('GLOBAL BC HD','Global Vancouver') 
     s=s.replace('Global Vancouver','Global Vancouver')     
     s=s.replace('GLOBALTV','Global Vancouver')  
     
     s=s.replace('Sky Gold','Gold')
     s=s.replace('GOLD','Gold')
     s=s.replace('gold','Gold')

     s=s.replace('GOLF','Golf Channel')
     s=s.replace('golf','Golf Channel')
     s=s.replace('The Golf Channel','Golf Channel')     
     s=s.replace('THE GOLF CHANNEL','Golf Channel')
     s=s.replace('GOLF HD','Golf Channel')
          
     s=s.replace('GOOD FOOD','Good Food UK')
     s=s.replace('good food','Good Food UK')

     s=s.replace('Game Show Network','GSN')
     s=s.replace('GSN HD','GSN')
     
     s=s.replace('Hallmark HD','Hallmark')
     s=s.replace('HALLMARK','Hallmark')
     s=s.replace('Hallmark','Hallmark')


     s=s.replace('Hbo','HBO')

     s=s.replace('HBO EAST HD','HBO HD')
     s=s.replace('HBO EAST1','HBO HD')     
     s=s.replace('HBO EAST ','HBO HD')
     s=s.replace('HBO 1','HBO HD')

     s=s.replace('Hbo West','HBO West')

     s=s.replace('HBO 2 ','HBO2')
     s=s.replace('HBO EAST2','HBO2')

     s=s.replace('HBO COMEDY HD','HBO Comedy')
     s=s.replace('HBO COMEDY','HBO Comedy')
     s=s.replace('HBOCmdy HD','HBO Comedy')
     s=s.replace('HBOCmdy','HBO Comedy')

     s=s.replace('Hbo Family','HBO Family')

     s=s.replace('HBO EastSignature','HBO Signature')
     s=s.replace('HBO SIGNATURE HD','HBO Signature')
     s=s.replace('HBO SIGNATURE','HBO Signature')
          
     s=s.replace('HBO ZONE ','HBO Zone')
     s=s.replace('HBOZone HD','HBO Zone')
     s=s.replace('HBOZone','HBO Zone')

     s=s.replace('HGTV HD','HGTV') 
     s=s.replace('Hgtv','HGTV')     
     
     s=s.replace('HISTORY HD','History')
     s=s.replace('HISTORY','History')
     s=s.replace('History_CHANNEL','History')
     s=s.replace('History HD','History')
                   
     s=s.replace('History 2','H2')     
     s=s.replace('HISTORY2 (H2)','H2')
     s=s.replace('H2 USA','H2')
     s=s.replace('H2USA','H2')
     s=s.replace('h2','H2')
     
     s=s.replace('HISTORY CANADA','History Canada')     
 
     s=s.replace('HLN HD - NEW','HLN')
     s=s.replace('HLN HD','HLN')     
    
     s=s.replace('Sky Home','Home')

     s=s.replace('HORROR CHANNEL','Horror Channel')
     s=s.replace('horror channel','Horror Channel')
     
     s=s.replace('HUSTLER HD','HUSTLER')

     s=s.replace('Information Discovery','ID')
     s=s.replace('ID HD','ID')

     s=s.replace('IFC HD','IFC')     
     s=s.replace('Ifc','IFC')

     s=s.replace('IRISH TV','Irish TV')
     s=s.replace('irish tv','Irish TV')

     s=s.replace('itv ENCORE','ITV Encore')
     s=s.replace('Itv encore','ITV Encore')
     s=s.replace('itv encore','ITV Encore')
     s=s.replace('ITVENCORE','ITV Encore')

     s=s.replace('Sky itv1','ITV1')         
     s=s.replace('itv1','ITV1')    
     s=s.replace('itv 1','ITV1')
     s=s.replace('ITV 1','ITV1')
     s=s.replace('Itv 1','ITV1')
     s=s.replace('ITV London','ITV1')
     s=s.replace('Itv1','ITV1')
     s=s.replace('ITV1 HD','ITV1')
     s=s.replace('Sky ITV1','ITV1')
     s=s.replace('UK_ITV1','ITV1')
     s=s.replace('ITV HD 1','ITV1')
                        
     s=s.replace('itv1+1','ITV1+1')
     s=s.replace('ITV1+1','ITV1+1')
     s=s.replace('Itv1+1','ITV1+1')
     s=s.replace('Itv1+1','ITV1+1')     
     
     s=s.replace('Sky itv2','ITV2')      
     s=s.replace('itv2','ITV2')   
     s=s.replace('itv 2','ITV2')
     s=s.replace('ITV 2','ITV2')
     s=s.replace('Itv 2','ITV2')
     s=s.replace('Itv2','ITV2')
     s=s.replace('ITV2 HD','ITV2')
     s=s.replace('Sky ITV2','ITV2')
     s=s.replace('UK_ITV2','ITV2')
     s=s.replace('ITV HD 2','ITV2')
                    
     s=s.replace('itv2+1','ITV2+1')
     s=s.replace('ITV2+1','ITV2+1')
     s=s.replace('Itv2+1','ITV2+1')
     s=s.replace('Itv2+1','ITV2+1')

     s=s.replace('Sky itv3','ITV3')
     s=s.replace('itv3','ITV3') 
     s=s.replace('itv 3','ITV3')
     s=s.replace('ITV 3','ITV3')
     s=s.replace('Itv 3','ITV3')
     s=s.replace('Itv3','ITV3')
     s=s.replace('ITV3 HD','ITV3')
     s=s.replace('Sky ITV3','ITV3')
     s=s.replace('UK_ITV3','ITV3')
     s=s.replace('ITV HD 3','ITV3')
                        
     s=s.replace('itv3+1','ITV3+1')
     s=s.replace('ITV3+1','ITV3+1')
     s=s.replace('Itv3+1','ITV3+1')
     s=s.replace('Itv3+1','ITV3+1')

     s=s.replace('Sky itv4','ITV4')
     s=s.replace('itv4','ITV4')     
     s=s.replace('itv 4','ITV4')
     s=s.replace('ITV 4','ITV4')
     s=s.replace('Itv 4','ITV4')
     s=s.replace('Itv4','ITV4')
     s=s.replace('ITV4 HD','ITV4')
     s=s.replace('Sky ITV4','ITV4')
     s=s.replace('UK_ITV4','ITV4')
     s=s.replace('ITV HD 4','ITV4')
                         
     s=s.replace('itv4+1','ITV4+1')
     s=s.replace('ITV4+1','ITV4+1')
     s=s.replace('Itv4+1','ITV4+1')
     s=s.replace('Itv4+1','ITV4+1')

     s=s.replace('itvbe','ITVBe')
     s=s.replace('ITVBE','ITVBe')
     
     s=s.replace('KERRANG! TV','Kerrang')
     s=s.replace('kerrang! tv','Kerrang')
     s=s.replace('kerrang','Kerrang')
     
     s=s.replace('KISS TV','Kiss')
     s=s.replace('kiss tv','Kiss')
     s=s.replace('KISS','Kiss')
     s=s.replace('kiss','Kiss')
     
     s=s.replace('KIX','Kix')
     s=s.replace('kix','Kix')

     s=s.replace('KTLA 5','KTLA')
     s=s.replace('Ktla','KTLA')

     s=s.replace('LIFTIME','Lifetime')
     s=s.replace('LIFE HD','Lifetime')
     
     s=s.replace('Lifetime Movie Network','LMN')
     s=s.replace('LIFETIME MOVIES HD','LMN') 
                    
     s=s.replace('LFCTV ','Lfctv')
     s=s.replace('Liverpool FC TV','Lfctv')
     s=s.replace('liverpool TV','Lfctv')

     s=s.replace('london live','London Live')
     s=s.replace('LONDON LIVE','London Live')
     
     s=s.replace('MLB NETWORK','MLB Network')

     s=s.replace('MORE 4','More4')
     s=s.replace('more 4','More4')
     s=s.replace('More 4','More4')
     s=s.replace('MORE_4','More4')
     
     s=s.replace('MOREMAX HD - NEW','MoreMax')
     s=s.replace('MOREMAX HD','MoreMax')
     s=s.replace('Cinemax MoreMax','MoreMax')
               
     s=s.replace('MOTORS TV','Motors TV')
     s=s.replace('motors tv','Motots TV')

     s=s.replace('MOVIES 24','Movies 24')
     s=s.replace('movies 24','Movies 24')

     s=s.replace('MOVIE TIME HD','MovieTime')
     
     s=s.replace('MOVIES4MEN','Movies4Men')
     s=s.replace('movies4men','Movies4Men')
     s=s.replace('Movies 4 Men','Movies4Men')
          
     s=s.replace('MSNBC HD - NEW','MSNBC')
     s=s.replace('MSNBC HD','MSNBC')
              
     s=s.replace('MTV MUSIC','MTV')
     s=s.replace('MTV HD','MTV')
     
     s=s.replace('MTV uk','MTV UK')
     s=s.replace('MTV1 UK','MTV UK')
     
     s=s.replace('mutv','MUTV')
     s=s.replace('SKY MUTV','MUTV')
     
     s=s.replace('MYTV','MY9')

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

     s=s.replace('NAT GEO WILD HD','Nat Geo Wild')     
     s=s.replace('NAT GEO WILD','Nat Geo Wild')
     s=s.replace('nat geo wild','Nat Geo Wild')
     s=s.replace('National Geographic Channel WILD','Nat Geo Wild')
     s=s.replace('NatGeoWild','Nat Geo Wild')
     s=s.replace('Nat geo wild','Nat Geo Wild')
     s=s.replace('NATIONAL_GEOWILD','Nat Geo Wild')
          
     s=s.replace('Nat Geo WildUK','Nat Geo Wild UK')
     s=s.replace('Sky Nat Geo Wild HD','Nat Geo Wild UK')
     
     s=s.replace('NAT GEO HD','National Geographic')  
     s=s.replace('NAT GEO','National Geographic')
     s=s.replace('NatGeo','National Geographic')
     s=s.replace('NATIONAL GEOGRAPHIC CHANNEL','National Geographic')
     s=s.replace('NATIONAL GEOGRAPHIC','National Geographic')
     s=s.replace('national geographic','National Geographic')
     s=s.replace('National Geographic Channel','National Geographic')
     s=s.replace('NATIONAL_GEOGRAPHIC','National Geographic')
     s=s.replace('NATIONAL_GEOGRAPHY','National Geographic')
     s=s.replace('Nat Geo=','National Geographic=')
                    
     s=s.replace('Sky Natgeo','National Geographic UK')
     s=s.replace('Nat Geo UK','National Geographic UK')
     s=s.replace('Sky National Geographic HD','National Geographic UK')
          
     s=s.replace('Nbc=','NBC=')
     s=s.replace('NBC Miami','NBC')
     
     s=s.replace('NBC East','NBC HD')    
     s=s.replace('NBC hd','NBC HD')
     s=s.replace('NBC New York','NBC HD')   
          
     s=s.replace('NBC SPORTS NETWORK','NBCSN')
     s=s.replace('Nbc Sports Network','NBCSN')
     s=s.replace('NBC SPORTS','NBCSN')
     s=s.replace('nbcsn','NBCSN')
     s=s.replace('NBCSN HD','NBCSN')
     s=s.replace('NBCSPORTSHD','NBCSN')
               
     s=s.replace('NBATV','NBA TV')
     s=s.replace('NBA HD','NBA TV')
     s=s.replace('USA NBA','NBA TV')
               
     s=s.replace('NFL NETWORK','NFL Network')
     s=s.replace('NFL NOW HD','NFL Network')
     
     s=s.replace('NHL NETWORK HD','NHL Network')
     s=s.replace('NHL NETWORK','NHL Network')

     s=s.replace('NICKELODEON HD (NA)','Nickleodeon')
     s=s.replace('NICKELODEON HD','Nickleodeon')     
     s=s.replace('NICKELODEON','Nickleodeon')
     s=s.replace('nickleodeon','Nickleodeon')
     s=s.replace('Nick HD','Nickleodeon')
     s=s.replace('NICKLEODON','Nickleodeon')
     
     s=s.replace('SKY NICK (UK)','Nickleodeon UK')
     s=s.replace('SKY NICK=','Nickleodeon UK=')
               
     s=s.replace('NICK JR','Nick Jr')
     s=s.replace('nick jr','Nick Jr')     
     s=s.replace('NickJr','Nick Jr')
     s=s.replace('NickJr TOO','Nick Jr')
     s=s.replace('Nick Jr.','Nick Jr')
     s=s.replace('Nick JR','Nick Jr')
     s=s.replace('NICK JUNIOR','Nick Jr')
                    
     s=s.replace('SKY NICK TOONS (UK)','Nick Toons UK')          
     s=s.replace('SKY NICK TOONS','Nick Toons UK')  
     s=s.replace('NICKTOONS','Nick Toons UK')  
                    
     s=s.replace('OMNI 1 HD','OMNI 1')          
          
     s=s.replace('OMNI 2 HD','OMNI 2') 
               
     s=s.replace('OWN HD','OWN')
     s=s.replace('Oprah Winfrey Network','OWN')
          
     s=s.replace('OXYGEN','Oxygen')
          
     s=s.replace('PAC-12 Arizona HD','PAC-12 Arizona')
     s=s.replace('PAC-12 Arizona','PAC-12 Arizona')
     s=s.replace('PAC-12 Bay Area HD','PAC-12 Bay Area')
     s=s.replace('PAC-12 Bay Area','PAC-12 Bay Area')
     s=s.replace('PAC-12 Los Angeles','PAC-12 Los Angeles')
     s=s.replace('PAC-12 Mountain HD','PAC-12 Mountain')
     s=s.replace('PAC-12 National','PAC-12 National')
     s=s.replace('PAC-12 Oregon HD','PAC-12 Oregon')
     
     s=s.replace('PBS HD','PBS')
     s=s.replace('Pbs','PBS')
          
     s=s.replace('pick','Pick')
     s=s.replace('PICK','Pick')
     
     s=s.replace('PLAYBOY TV HD - NEW','PLAYBOY')
     s=s.replace('PLAYBOY TV HD','PLAYBOY')
          
     s=s.replace('Poker Central HD','Poker Central')

     s=s.replace('PREMIER SPORTS','Premier Sports')
     s=s.replace('PREMIER HD','Premier Sports')
     s=s.replace('SKY-PREMIERE SPORT','Premier Sports')   
     
       
     s=s.replace('Ppv1','PPV')
     s=s.replace('Sky Box Office 1','PPV')  
     s=s.replace('Sky Sports Box Office PPV live during events','PPV')  
     s=s.replace('Sky Sports Box Office b','PPV')  
     s=s.replace('PPV 2 (1.4k Bitrate)','PPV')
               
     s=s.replace('Ppv2','PPV')
     s=s.replace('SONY ESPN HD - LIVE EVENTS','PPV')
     s=s.replace('PPV 3 (2k Bitrate)','PPV')


     s=s.replace('QUEST','Quest')
     s=s.replace('Quest','Quest')
     s=s.replace('quest','Quest')
     
     s=s.replace('RACING HD','Racing UK')
     s=s.replace('RACING UK','Racing UK')
     s=s.replace('racing uk','Racing UK')
     s=s.replace('RaCIng UK','Racing UK')
     
     s=s.replace('REALLY','Really')
     s=s.replace('really','Really')

     s=s.replace('RTE NEWS NOW',' RTE News Now')
     s=s.replace('rte news now','RTE News Now')
     s=s.replace('RTE NEWS','RTE News Now')
     s=s.replace('Rte news','RTE News Now')
     s=s.replace('rte news','RTE News Now')
     s=s.replace('RT NEWS HD','RTE News Now')
     
     s=s.replace('RT DOCUMENTARY HD','RT Documentary')     
     
     s=s.replace('Sky RTE 1','RTE1')
     s=s.replace('rte one','RTE1')
     s=s.replace('Rte one','RTE1')
     s=s.replace('rte1','RTE1')
     s=s.replace('RTEONE','RTE1')
     s=s.replace('rteone','RTE1')
     s=s.replace('rte 1','RTE1')
     s=s.replace('RTE One','RTE1')
     s=s.replace('RTE ONE HD','RTE1')
     s=s.replace('Sky RTE ONE','RTE1')  
     s=s.replace('RTE1HD','RTE1') 
     s=s.replace('RTE 1','RTE1') 
                       
     s=s.replace('Sky RTE 2','RTE2')          
     s=s.replace('RTE TWO','RTE2')
     s=s.replace('rte two','RTE2')
     s=s.replace('Rte two','RTE2')
     s=s.replace('rte2','RTE2')
     s=s.replace('RTETWO','RTE2')
     s=s.replace('rtetwo','RTE2')
     s=s.replace('rte 2','RTE2')
     s=s.replace('RTE Two','RTE2')
     s=s.replace('RTE 2 HD','RTE2')
     s=s.replace('Sky RTE TWO','RTE2')
     s=s.replace('RTE TWO HD','RTE2')
     s=s.replace('RTE TWOHD','RTE2')
     s=s.replace('RTE 2','RTE2')  
                                
     s=s.replace('SETANTA IRELAND HD','Setanta Ireland')
     s=s.replace('Setanta Ireland HD','Setanta Ireland')
     s=s.replace('SETANTA IRELAND HD','Setanta Ireland')
     s=s.replace('Setanta Ireland HD','Setanta Ireland')
     s=s.replace('SETANTA IRELAND HD','Setanta Ireland')
     s=s.replace('setanta ireland','Setanta Ireland')
     s=s.replace('SETANTA IRELAND','Setanta Ireland')
     s=s.replace('setanta ireland','Setanta Ireland')
     s=s.replace('SETANTA IRELAND','Setanta Ireland')
     s=s.replace('setanta ireland','Setanta Ireland')
     
     s=s.replace('SETANTA SPORTS 1 HD','Setanta Sports 1')
     s=s.replace('Setanta Sports 1 HD','Setanta Sports 1')
     s=s.replace('SETANTA SPORTS 1','Setanta Sports 1')
     s=s.replace('setanta sports 1','Setanta Sports 1')
     s=s.replace('Setanta Sports Ireland','Setanta Ireland')
     s=s.replace('setanta sports','Setanta Sports 1')

     s=s.replace('SHOWCASE HD - NEW','SHOWCASE')
     s=s.replace('SHOWCASE HD','SHOWCASE')
          
     s=s.replace('ShowTime HD','Showtime HD')
     s=s.replace('SHOWTIME EAST','Showtime HD')
     s=s.replace('SHOWTIME','Showtime HD')

     s=s.replace('SHOWTIME (PACIFIC)','Showtime West')
     s=s.replace('SHOWTIME WEST','Showtime West')
     s=s.replace('showtime west','Showtime West')     
               
     s=s.replace('SHOWTIME BEYOND','Showtime Beyond')
     s=s.replace('showtime beyond','Showtime Beyond')
     
     s=s.replace('SHOWTIME EXTREME','Showtime Extreme')
     s=s.replace('showtime extreme','Showtime Extreme')
     
     s=s.replace('SHOWTIME NEXT','Showtime Next')
     s=s.replace('showtime next','Showtime Next')

     s=s.replace('SHOWTIME SHOWCASE HD','Showtime Showcase')
     s=s.replace('SHOWTIME SHOWCASE','Showtime Showcase')
     s=s.replace('showtime showcase','Showtime Showcase')
     
     s=s.replace('SKY1','Sky1')
     s=s.replace('sky1','Sky1')
     s=s.replace('SKY 1','Sky1')
     s=s.replace('sky 1','Sky1')
     s=s.replace('Sky 1','Sky1')
     s=s.replace('SKY ONE','Sky1')
     s=s.replace('sky one','Sky1')
     s=s.replace('Sky One HD','Sky1')
     s=s.replace('Sky Uno HD','Sky1')
     s=s.replace('SKY_ONE','Sky1')
     s=s.replace('Sky One','Sky1')
                              
     s=s.replace('SKY2','Sky2')
     s=s.replace('sky2','Sky2')    
     s=s.replace('SKY 2','Sky2')
     s=s.replace('sky 2','Sky2')
     s=s.replace('SKY TWO','Sky2')
     s=s.replace('sky two','Sky2')
     s=s.replace('SKY_TWO','Sky2')
     s=s.replace('SKY TWO','Sky2')      
     s=s.replace('Sky 2','Sky2')
     
     s=s.replace('SKY ARTS 1','Sky Arts 1')
     s=s.replace('sky arts 1','Sky Arts 1')
     s=s.replace('sky arts one','Sky Arts 1')
     s=s.replace('Sky Arts One','Sky Arts 1')
     s=s.replace('SKY ARTS ONE','Sky Arts 1')
     s=s.replace('Sky Arts1','Sky Arts 1')
     s=s.replace('Sky Arts 1 HD','Sky Arts 1')
          
     s=s.replace('sky atlanic','Sky Alantic')
     s=s.replace('SKY ATLANTIC','Sky Alantic')
     s=s.replace('Sky Atlanic UK','Sky Alantic')
     s=s.replace('Sky Atlantic UK','Sky Alantic')
     s=s.replace('Sky Atlantic HD','Sky Alantic')
     s=s.replace('SKY_ATLANTIC_HD','Sky Alantic')
                    
     s=s.replace('Sky Action Movies','Sky Movies Action')
     s=s.replace('SKY ACTION','Sky Movies Action')
     s=s.replace('sky action','Sky Movies Action')
     s=s.replace('Sky Movies Action & Adventure','Sky Movies Action')
     s=s.replace('Sky Movies Action','Sky Movies Action')
     s=s.replace('SKY MOVIES ACTION','Sky Movies Action')
     s=s.replace('Sky ActionUK','Sky Movies Action')
     s=s.replace('Sky action','Sky Movies Action')
     s=s.replace('Sky Movies Action HD','Sky Movies Action')
     s=s.replace('Sky Movies Action & ADVENTURE','Sky Movies Action')
     s=s.replace('SKY_MOVIES_ACTION','Sky Movies Action')
                         
     s=s.replace('Sky Comedy Movies','Sky Movies Comedy')
     s=s.replace('SKY COMEDY','Sky Movies Comedy')
     s=s.replace('sky comedy','Sky Movies Comedy')
     s=s.replace('SKY MOVIES COMEDY','Sky Movies Comedy')
     s=s.replace('Sky Comedy UK','Sky Movies Comedy')
     s=s.replace('Sky Movies ComedyUK','Sky Movies Comedy')
     s=s.replace('Sky Movies Comedy HD','Sky Movies Comedy')
     s=s.replace('SKY_MOVIES_COMEDY','Sky Movies Comedy')
                    
     s=s.replace('SKY MOVIES CRIME','Sky Movies Crime')
     s=s.replace('SKY THRILLER','Sky Movies Crime')
     s=s.replace('sky thriller','Sky Movies Crime')
     #s=s.replace('Sky Movies Crime & T','Sky Movies Crime')
     s=s.replace('Sky Movies Thriller','Sky Movies Crime')
     s=s.replace('SKY MOVIES THRILLER','Sky Movies Crime')
     s=s.replace('Sky ThrillerUK','Sky Movies Crime')
     s=s.replace('Sky Movies Crime HD','Sky Movies Crime')
     s=s.replace('Sky Movies CrimeHRILLER','Sky Movies Crime')
     s=s.replace('SKY_MOVIES_THRILLER','Sky Movies Crime')
     s=s.replace('Sky Movies Crime & THRILLER','Sky Movies Crime')
     s=s.replace('Sky Movies Crime & Thriller','Sky Movies Crime')
                              
     s=s.replace('SKY DISNEY','Sky Movies Disney')
     s=s.replace('sky disney','Sky Movies Disney')
     s=s.replace('Sky Movies Disney','Sky Movies Disney')
     s=s.replace('SKY MOVIES DISNEY','Sky Movies Disney')
     s=s.replace('Sky Movies DisneyUK','Sky Movies Disney')
     s=s.replace('Sky Movies Disney JR','Sky Movies Disney')
          
     s=s.replace('SKY DRAMA AND ROMANCE','Sky Movies Drama')
     s=s.replace('SKY Drama AND ROMANCE','Sky Movies Drama')
     s=s.replace('Sky DramaRom Movies','Sky Movies Drama')
     s=s.replace('Sky Movies Drama & Romance','Sky Movies Drama')
     s=s.replace('Sky Movies Drama','Sky Movies Drama')
     s=s.replace('SKY MOVIES DRAMA','Sky Movies Drama')
     s=s.replace('Sky Movie Romance','Sky Movies Drama')
     s=s.replace('Sky DramaUK','Sky Movies Drama')
     s=s.replace('Sky Movies Drama HD','Sky Movies Drama')
     s=s.replace('SKY MOVIES Drama & ROMANCE','Sky Movies Drama')
     s=s.replace('SKY_MOVIES_Drama_ROMANCE','Sky Movies Drama')
     s=s.replace('SKY MOVIES Drama&ROMANCE HD','Sky Movies Drama')
                              
     s=s.replace('Sky Family Movies','Sky Movies Family') 
     s=s.replace('SKY FAMILY','Sky Movies Family')
     s=s.replace('Sky FamilyUK','Sky Movies Family')
     s=s.replace('Sky Movies Family HD','Sky Movies Family') 
     s=s.replace('SKY MOVIES FAMILY','Sky Movies Family')
     s=s.replace('SKY_MOVIES_FAMILY','Sky Movies Family')
     s=s.replace('Sky Movies Family HD','Sky Movies Family')
                         
     s=s.replace('Sky Greats Movies','Sky Movies Greats')
     s=s.replace('SKY GREATS','Sky Movies Greats')
     s=s.replace('Sky Modern Great','Sky Movies Greats')
     s=s.replace('SKY MOVIES MODERN GREATS','Sky Movies Greats')
     s=s.replace('SKY_MOVIES_MODERN_GREAT','Sky Movies Greats')
     s=s.replace('Sky Movies Modern HD','Sky Movies Greats')
                      
     s=s.replace('SKY LIVING','Sky Living')
     s=s.replace('sky living','Sky Living')
 
     s=s.replace('sky permiere','Sky Movies Premiere')
     s=s.replace('Sky Premiere Movies','Sky Movies Premiere')
     s=s.replace('SKY PREMIERE','Sky Movies Premiere')
     s=s.replace('Sky Movies Premier','Sky Movies Premiere')
     s=s.replace('SKY MOVIES PREMIERE','Sky Movies Premiere')
     s=s.replace('Sky Movie PremierUK','Sky Movies Premiere')
     s=s.replace('Sky Movie PremiereUK','Sky Movies Premiere')
     s=s.replace('Sky Movies PremiereeeeeeeeUK','Sky Movies Premiere')
     s=s.replace('Sky Movies Premiereeeeeeeeeeeeeeeeeeee','Sky Movies Premiere')                        
     s=s.replace('Sky premier','Sky Movies Premiere')  
     s=s.replace('Sky Movies Premieree','Sky Movies Premiere') 
     s=s.replace('SKY MOVIES PREMIER','Sky Movies Premiere') 
     s=s.replace('SKY_MOVIES_PREMIERE','Sky Movies Premiere') 
     s=s.replace('Sky Movies Premiere HD','Sky Movies Premiere') 
                                                 
     s=s.replace('Sky ScFiHorror Movies','Sky Movies Scifi') 
     s=s.replace('sky sci-fi & horror','Sky Movies Scifi')
     s=s.replace('SKY SCI-FI HORROR','Sky Movies Scifi')
     s=s.replace('Sky Movies Scifi','Sky Movies Scifi')
     s=s.replace('SKY MOVIES SCIFI','Sky Movies Scifi')
     s=s.replace('Sky Movies Sci-Fi','Sky Movies Scifi')  
     s=s.replace('Sky Movies SCIfi HD','Sky Movies Scifi') 
     s=s.replace('Sky SCIFi','Sky Movies Scifi') 
     s=s.replace('Sky Movie SCI-Fi & horror','Sky Movies Scifi') 
     s=s.replace('SKY MOVIES SCI-FI & HORROR','Sky Movies Scifi') 
     s=s.replace('Sky Movies SCIfi','Sky Movies Scifi')
     s=s.replace('Sky Movies SCI-Fi','Sky Movies Scifi')
     s=s.replace('Sky Movies Scifi & Horror','Sky Movies Scifi')
     s=s.replace('SCIfi','Scifi')
                                              
     s=s.replace('Sky Movies Select','Sky Movies Select')
     s=s.replace('SKY MOVIES SELECT','Sky Movies Select')
     s=s.replace('Sky Select Movies','Sky Movies Select')
     s=s.replace('SKY SELECT','Sky Movies Select')
     s=s.replace('sky select','Sky Movies Select')
     s=s.replace('Sky Select','Sky Movies Select')
     s=s.replace('Sky Movies Select HD','Sky Movies Select')
     s=s.replace('SKY_MOVIES_SELECT','Sky Movies Select')
                              
     s=s.replace('Sky Movies Showcase','Sky Movies Showcase')
     s=s.replace('SKY MOVIES SHOWCASE','Sky Movies Showcase')
     s=s.replace('SKY SHOWCASE','Sky Movies Showcase')
     s=s.replace('sky showcase','Sky Movies Showcase') 
     s=s.replace('Sky Showcase HD','Sky Movies Showcase') 
     s=s.replace('Sky Movies ShowCase','Sky Movies Showcase') 
                   
     s=s.replace('Sky Movies Superheroes','Sky Movies Superheroes')


     
     s=s.replace('SKYSPORTS 1','Sky Sports 1')
     s=s.replace('SKYSPORTS 2','Sky Sports 2')
     s=s.replace('SKYSPORTS 3','Sky Sports 3')
     s=s.replace('SKYSPORTS 4','Sky Sports 4')
     s=s.replace('SKYSPORTS 5','Sky Sports 5')

     s=s.replace('SKY SPORTS 1 HD','Sky Sports 1 HD')
     s=s.replace('Sky Sports 1 HD+','Sky Sports 1 HD')
     s=s.replace('SKY_SPORTS_1HD','Sky Sports 1 HD')
     s=s.replace('SKY SPORTS  1 HD','Sky Sports 1 HD')
               
     s=s.replace('SKY SPORTS 1','Sky Sports 1')
     s=s.replace('sky sports 1s','Sky Sports 1')
     s=s.replace('Sky Sport 1UK','Sky Sports 1')
     
     s=s.replace('SKY SPORTS 2 HD','Sky Sports 2 HD')
     s=s.replace('Sky Sports 2 HD+','Sky Sports 2 HD')
     s=s.replace('Sky Sport 2 Uk HD','Sky Sports 2 HD')
     s=s.replace('SKY_SPORTS_2HD','Sky Sports 2 HD')
     s=s.replace('SKY SPORTS  2 HD','Sky Sports 2 HD')
                    
     s=s.replace('SKY SPORTS 2','Sky Sports 2')
     s=s.replace('sky sports 2s','Sky Sports 2')
     s=s.replace('Sky sport 2UK','Sky Sports 2')
     
     s=s.replace('SKY SPORTS 3 HD','Sky Sports 3 HD')
     s=s.replace('Sky Sports 3 HD+','Sky Sports 3 HD')
     s=s.replace('Sky Sports 3 HD3','Sky Sports 3 HD')
     s=s.replace('Sky Sports 3 HD UK','Sky Sports 3 HD')     
     s=s.replace('SKY_SPORTS_3HD','Sky Sports 3 HD')
     s=s.replace('SKY SPORTS  3 HD','Sky Sports 3 HD')
               
     s=s.replace('SKY SPORTS 3','Sky Sports 3')
     s=s.replace('sky sports 3s','Sky Sports 3')
     s=s.replace('Sky sport 3UK','Sky Sports 3')
     
     s=s.replace('SKY SPORTS 4 HD','Sky Sports 4 HD')
     s=s.replace('Sky Sports 4 HD+','Sky Sports 4 HD')
     s=s.replace('Sky sport 4 HDUK','Sky Sports 4 HD')     
     s=s.replace('SKY_SPORTS_4HD','Sky Sports 4 HD')
     s=s.replace('SKY SPORTS  4 HD','Sky Sports 4 HD')
               
     s=s.replace('SKY SPORTS 4','Sky Sports 4')
     s=s.replace('sky sports 4s','Sky Sports 4')
     s=s.replace('Sky sport 4UK','Sky Sports 4')
     
     s=s.replace('SKY SPORTS 5 HD','Sky Sports 5 HD')
     s=s.replace('Sky Sports 5 HD+','Sky Sports 5 HD')
     s=s.replace('SKY_SPORTS_5HD','Sky Sports 5 HD')     
     s=s.replace('SKY SPORTS  5 HD','Sky Sports 5 HD')
          
     s=s.replace('SKY SPORTS 5','Sky Sports 5')
     s=s.replace('sky sports 5s','Sky Sports 5')
     s=s.replace('Sky Sport 5UK','Sky Sports 5')
     s=s.replace('Sky sport 5UK','Sky Sports 5')
     
          
     s=s.replace('SKY SPORTS F1 HD','Sky Sports F1')
     s=s.replace('sky sports F1 HD','Sky Sports F1')
     s=s.replace('Sky Sports F1 HD+','Sky Sports F1')
     s=s.replace('SKY SPORTS F1','Sky Sports F1')
     s=s.replace('Sky Sports F1/DARTS','Sky Sports F1')
     s=s.replace('Sky Spts F1','Sky Sports F1')     
     s=s.replace('Sky sports F1 HD UK','Sky Sports F1')  
     s=s.replace('SKY_SPORTS_F1HD','Sky Sports F1') 
     s=s.replace('SKY Sports F1 New','Sky Sports F1')
                    
     s=s.replace('Sky Sports News HD','Sky Sports News')
     s=s.replace('SKY SPORTS NEWS','Sky Sports News')
     s=s.replace('sky sports news','Sky Sports News')
     s=s.replace('Sky Sport News','Sky Sports News')
     s=s.replace('Sky Sport newsUK','Sky Sports News')
     s=s.replace('SKY SPORT NEWS','Sky Sports News')
     s=s.replace('SKY_SPORTS_NEWS','Sky Sports News')
          
     s=s.replace('Sky Sport ','Sky Sports ')
          
     s=s.replace('SKY NEWS HD','Sky News')
     s=s.replace('SKY NEWS','Sky News')
     s=s.replace('Sky News UK','Sky News')
     
     s=s.replace('SLICE HD','SLICE')

     s=s.replace('SONY MOVIE CHANNEL','Sony Movie Channel')
     s=s.replace('sony movie channel','Sony Movie Channel')

     s=s.replace('Sony Six HD','Sony Six')

     s=s.replace('SPIKE HD','Spike')
     s=s.replace('Spike HD','Spike')
     s=s.replace('SPIKE','Spike')
     s=s.replace('spike','Spike')

     s=s.replace('SPORT TIME TV3HD','SPORT TIME TV 3HD')

     s=s.replace('THE SCORE','Sportsnet 360')
     s=s.replace('SPORTSNET 360','Sportsnet 360')
     
     s=s.replace('SPORTSNET ONE HD','Sportsnet One')
     s=s.replace('SPORTSNET ONE','Sportsnet One')
     s=s.replace('SportsNet ONE','Sportsnet One')
          
     s=s.replace('SPORTS NET Ontario','Sportsnet Ontario')
     s=s.replace('SPORTSNET ONT','Sportsnet Ontario')   
     s=s.replace('Sportsnet Ontarioario','Sportsnet Ontario')  
     s=s.replace('SportsNet Ontario','Sportsnet Ontario')
                     
     s=s.replace('SPORTSNET WORLD HD','Sportsnet World')
     s=s.replace('SPORTS NET WORLD','Sportsnet World')
     s=s.replace('SportsNet World - scribe','Sportsnet World')
     s=s.replace('SPORTSNETWORLD','Sportsnet World')
 
     s=s.replace('SPORT TIME TV3HD','SPORT TIME TV3 HD')
          
     s=s.replace('STARZ (pacific)','Starz')
     s=s.replace('Starz HD - NEW','Starz')
     s=s.replace('Starz HD','Starz')
     s=s.replace('STARZ HD','Starz')
     s=s.replace('Starz HD','Starz')     
     s=s.replace('STARZ','Starz')
     s=s.replace('starz','Starz')
     s=s.replace('STARZ','Starz')
     s=s.replace('starz','Starz')
     
     s=s.replace('STARZ WEST','Starz West')
     s=s.replace('starz west','Starz West')

     s=s.replace('STARZ CINEMA','Starz Cinema')
     s=s.replace('starz cinema','Starz Cinema')
     s=s.replace('Starz Cinema','Starz Cinema')
     s=s.replace('StrzCinm','Starz Cinema')
     s=s.replace('StrzCinmHD','Starz Cinema')     
     s=s.replace('StrzCinmHD','StarzCInema') 
     
     s=s.replace('STARZ COMEDY','Starz Comedy')
     s=s.replace('starz comedy','Starz Comedy')
     s=s.replace('Starz Comedy','Starz Comedy')
     s=s.replace('StrzComedy','Starz Comedy')
     s=s.replace('Starz COMEDY HD - NEW','Starz Comedy')
     s=s.replace('Starz COMEDY HD','Starz Comedy')


     s=s.replace('Starz Edge HD - NEW','Starz Edge')
     s=s.replace('Starz Edge HD','Starz Edge')
     s=s.replace('STARZ EDGE','Starz Edge')
     s=s.replace('starz edge','Starz Edge')
     s=s.replace('StrzEdgeHD','Starz Edge')     
     s=s.replace('Starz EDGE HD','Starz Edge') 
     
     s=s.replace('Starz Black HD - NEW','Starz In Black')
     s=s.replace('STARZ IN BLACK','Starz In Black')
     s=s.replace('starz in black','Starz In Black')
     s=s.replace('Starz In Black','Starz In Black')
     s=s.replace('StrzBlack','Starz In Black')
     s=s.replace('Starz BLACK HD','Starz In Black')
     
     
     s=s.replace('StrzKids','Starz Kids & Family')
     s=s.replace('StrzKidsHD','Starz Kids & Family')
     s=s.replace('Starz KIDZ HD - NEW','Starz Kids & Family')
     s=s.replace('Starz KIDZ HD','Starz Kids & Family')
     
     s=s.replace('SUNDANCE HD','Sundance')     
     s=s.replace('SUNDANCE','Sundance')     
     
     s=s.replace('SYFY UK','Syfy UK')
     s=s.replace('Sky Syfy','Syfy UK')
          
     s=s.replace('SyFy HD','Syfy')
     s=s.replace('SYFY','Syfy')
     s=s.replace('syfy','Syfy')
     
     s=s.replace('TBS HD','TBS')
     s=s.replace('TBS_HD','TBS')
          
     s=s.replace('Tcm UK','TCM UK')
     
     s=s.replace('TCM EAST HD','TCM')
     s=s.replace('TCM HD - NEW','TCM')
     s=s.replace('TCM HD','TCM')
     
     s=s.replace('tg4','TG4')

     s=s.replace('the movie chanel extra','The Movie Channel Extra')
     s=s.replace('the movie chanel','The Movie Channel')
     s=s.replace('THE MOVIE CHANNEL EXTRA','The Movie Channel Extra')
     
     s=s.replace('THE MOVIE CHANNEL','The Movie Channel')

     s=s.replace('ThrillerMAX','ThrillerMax')
     s=s.replace('THRILLERMAX','ThrillerMax')
     s=s.replace('Thrillermax','ThrillerMax')
     s=s.replace('thrillermax','ThrillerMax')
     s=s.replace('THRILLER MAX HD - NEW','ThrillerMax')
     s=s.replace('THRILLER MAX HD','ThrillerMax')     
     
     s=s.replace('TLC HD','TLC')
     s=s.replace('tlc','TLC')
     s=s.replace('The Learning Channel HD','TLC')     
     s=s.replace('The Learning Channel','TLC')    

     s=s.replace('Sky TLC','TLC UK') 
          
     s=s.replace('TNT HD','TNT')          

     s=s.replace('TCM','TCM')

     s=s.replace('Sky TCM','TCM UK')
          
     s=s.replace('Ten Sports HD','Ten Sports Network')         
          
     s=s.replace('TENNIS HD','Tennis Channel')
     
     s=s.replace('The Weather Channel USA','The Weather Channel')     
               
     s=s.replace('TRAVEL HD','Travel')     
     s=s.replace('TRAVEL CHANNEL','Travel') 
     s=s.replace('Travel Channel','Travel') 
          
     s=s.replace('TRAVEL XP HD','TRAVEL XP')      
     
     s=s.replace('TREEHOUSE HD (NA)','TREEHOUSE')       
     
     s=s.replace('TRUE DRAMA','True Drama')
     s=s.replace('true drama','True Drama')

     s=s.replace('TRUE ENTERTAINMENT','True Entertainment')
     s=s.replace('true entertainment','True Entertainment')
     
     s=s.replace('TRUE MOVIES 1','True Movies')
     s=s.replace('true movies 1','True Movies')
     s=s.replace('TRUE_MOVIES1','True Movies')
     s=s.replace('Sky True Movies1','True Movies')
                  
     s=s.replace('TRUE MOVIES 2','True Movies 2')
     s=s.replace('true movies 2','True Movies 2')
     s=s.replace('TRUE_MOVIES2','True Movies 2')
     s=s.replace('Sky True Movies 2','True Movies 2')
          
     s=s.replace('TRU TV HD','truTV')  
     s=s.replace('TruTV HD','truTV')
     s=s.replace('turtv','truTV')
     s=s.replace('TRUTV','truTv')              
     
     s=s.replace('TSN1','TSN1')
     s=s.replace('TSN 1 HD','TSN1')
     s=s.replace('USA TSN 1','TSN1')
     s=s.replace('TSN 1','TSN1')
               
     s=s.replace('TSN2','TSN2')
     s=s.replace('TSN 2 HD','TSN2')
     s=s.replace('USA TSN 2','TSN2')
     s=s.replace('TSN 2','TSN2')
               
     s=s.replace('TSN3','TSN3')
     s=s.replace('TSN 3 HD','TSN3')
     s=s.replace('USA TSN 3','TSN3')
          
     s=s.replace('TSN4','TSN4')
     s=s.replace('TSN 4 HD','TSN4')
     s=s.replace('USA TSN 4','TSN4')
     s=s.replace('TSN 4','TSN4')
               
     s=s.replace('TSN5','TSN5')
     s=s.replace('TSN 5 HD','TSN5')
     s=s.replace('USA TSN 5','TSN5')
     s=s.replace('TSN 5','TSN5')
          
     s=s.replace('TV 3','TV3')
     s=s.replace('tv3','TV3')

     s=s.replace('ultimate event sports','Ultimate Events Sports')
     s=s.replace('ULTIMATE EVENT SPORTS','Ultimate Events Sports')

     s=s.replace('UNIVERSAL CHANNEL','Univesal Channel')
     s=s.replace('universal channel','Univesal Channel')

     s=s.replace('UTV IE','UTV')
     s=s.replace('utv','UTV')
     
     s=s.replace('TV LAND HD','TV Land')     
 
     s=s.replace('TVO HD (NA)','TVO') 
     
     s=s.replace('UFC NETWORK HD','UFC Network')   
     
     s=s.replace('USA NETWORK HD','USA Network')  
     s=s.replace('USA Network HD','USA Network')
     s=s.replace('USA HD','USA Network')  

     s=s.replace('Velocity HD - NEW','Velocity')
     s=s.replace('Velocity HD','Velocity')
     s=s.replace('VELOCITY HD','Velocity')
     
     s=s.replace('Sports Versus HD','Versus')

     s=s.replace('VEVO 1 HD','Vevo 1')
     s=s.replace('VEVO 2 HD','Vevo 2')
     s=s.replace('VEVO 3 HD','Vevo 3')
     s=s.replace('VEVO 4 HD','Vevo 4')
     s=s.replace(' Vevo 3','Vevo 1')
     
     s=s.replace('VH1 Classics','VH1 Classic')

     s=s.replace('VH1 HD','VH1')
     s=s.replace('VH1 US','VH1')
     s=s.replace('vh1','VH1')
     s=s.replace('VH1HD','VH1')
          
     s=s.replace('Sky VH1','VH1 UK')    
     s=s.replace('VH1 uk','VH1 UK')

     s=s.replace('VINTAGE TV','Vintage TV')
     s=s.replace('vintage tv','Vintage TV')

     s=s.replace('viva','VIVA')
     s=s.replace('Viva','VIVA')

     s=s.replace('WATCH','Watch')
     s=s.replace('watch','Watch')

     s=s.replace('VICELAND HD','Viceland')
     s=s.replace('VICELAND','Viceland')

     s=s.replace('VIVID TV - NEW','VIVID')
     s=s.replace('VIVID TV HD','VIVID')
     s=s.replace('Vivid','VIVID')
     
     s=s.replace('W MOVIES HD - NEW','W MOVIES')
     s=s.replace('W MOVIES HD','W MOVIES')

     s=s.replace('W NETWORK HD - NEW','W')
     s=s.replace('W NETWORK HD','W')
          
     s=s.replace('WE TV HD','WE TV')
     s=s.replace('WE Tv','WE TV')
     
     s=s.replace('WEATHER CANADA HD','Weather Canada') 
     s=s.replace('WEATHER CANADA HD','Weather Canada') 

     s=s.replace('WEATHER USA Network','Weather Network') 

     s=s.replace('WGN News Chicago','WGN America')
     
     s=s.replace('Wpix','WPIX')
          
     s=s.replace('WWE NETWORK HD - USA LINK','WWE Network')
     s=s.replace('WWE HD','WWE Network')
     s=s.replace('WWE NETWORK HD','WWE Network')
     s=s.replace('WWE NETWORK','WWE Network')
     s=s.replace('wwe network','WWE Network')
     s=s.replace('wwe HD','WWE Network')
     
     s=s.replace('YANKEES HD - NEW','YANKEES')
     s=s.replace('YANKEES HD','YANKEES')

     s=s.replace('Sky Yesterday','Yesterday')
     s=s.replace('YESTERDAY','Yesterday')
     s=s.replace('yesterday','Yesterday')
     
     s=s.replace('YTV HD (NA)','YTV')
     s=s.replace('YTV HD','YTV')


     #s=s.replace('Sky A','A')
     s=s.replace('Sky B','B')
     s=s.replace('Sky C','C')
     s=s.replace('Sky D','D')     
     s=s.replace('Sky E','E')     
     s=s.replace('Sky F','F')
     s=s.replace('Sky G','G')
     s=s.replace('Sky H','H')
     s=s.replace('Sky I','I')     
     s=s.replace('Sky J','J')       
     s=s.replace('Sky K','K')
     #s=s.replace('Sky L','L')
     #s=s.replace('Sky M','M')
     #s=s.replace('Sky N','N')     
     #s=s.replace('Sky O','O')       
     #s=s.replace('Sky P','P')
     s=s.replace('Sky Q','Q')
     s=s.replace('Sky R','R')
     #s=s.replace('Sky S','S')     
     #s=s.replace('Sky T','T')       
     s=s.replace('Sky U','U')
     s=s.replace('Sky V','V')
     s=s.replace('Sky W','W')
     s=s.replace('Sky X','X')     
     s=s.replace('Sky Y','Y')      
     s=s.replace('Sky Z','Z')



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
     s=s.replace('City TV Vancouver.png','City_TV_Vancouver.png')
     s=s.replace('CTV Regina.png','CTV_Regina.png')
     s=s.replace('CTV Toronto.png','CTV_Toronto.png')
     s=s.replace('CTV Vancouver.png','CTV_Vancouver.png')
     s=s.replace('Cartoon Network.png','Cartoon_Network.png')
     s=s.replace('City TV Toronto.png','City_TV_Toronto.png')
     s=s.replace('Comedy Central.png','Comedy_Central.png')
     s=s.replace('Discovery Science.png','Discovery_Science.png')
     s=s.replace('Discovery Investigation.png','Discovery_Investigation.png')
     s=s.replace('Disney XD.png','Disney_XD.png')
     s=s.replace('Encore Western.png','Encore_Western.png')
     s=s.replace('FOX HD.png','FOX_HD.png')
     s=s.replace('FOX West.png','FOX_West.png')
     s=s.replace('Food Network.png','Food_Network.png')
     s=s.replace('Fox News.png','Fox_News.png')
     s=s.replace('Global BC.png','Global_BC.png')
     s=s.replace('Global Toronto.png','Global_Toronto.png')
     s=s.replace('HBO Comedy.png','HBO_Comedy.png')
     s=s.replace('HBO HD.png','HBO_HD.png')
     s=s.replace('HBO Signature.png','HBO_Signature.png')
     s=s.replace('Movie Time.png','Movie_Time.png')
     s=s.replace('NBC HD.png','NBC_HD.png')
     s=s.replace('NBC West.png','NBC_West.png')
     s=s.replace('Nat Geo Wild.png','Nat_Geo_Wild.png')
     s=s.replace('National Geographic.png','National_Geographic.png')
     s=s.replace('Sky Movies Disney.png','Sky_Movies_Disney.png')
     s=s.replace('Disney XD UK.png','Disney_XD_UK.png')
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
     s=s.replace('Sky Movies Drama.png','Sky_Movies_Drama.png')
     s=s.replace('Sky Movies Action.png','Sky_Movies_Action.png')
     s=s.replace('Sky Movies Comedy.png','Sky_Movies_Comedy.png')
     s=s.replace('Sky Movies Disney.png','Sky_Movies_Disney.png')
     s=s.replace('Sky Movies Family.png','Sky_Movies_Family.png')
     s=s.replace('Sky Movies Premiere.png','Sky_Movies_Premiere.png')
     s=s.replace('Sky Movies Scifi.png','Sky_Movies_Scifi.png')
     s=s.replace('National Geographic UK.png','National_Geographic_UK.png')
     s=s.replace('TV Land.png','TV_Land.png')
     s=s.replace('Travel XP.png','Travel_XP.png')
     s=s.replace('USA Network.png','USA_Network.png')
     s=s.replace('W MOVIES.png','W_MOVIES.png')
     s=s.replace('WE TV.png','WE TV.png')
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
     s=s.replace('Setanta Asia HD.png','Setanta_Asia_HD.png')
     s=s.replace('Sky Sports 1 HD.png','Sky_Sports_1_HD.png')
     s=s.replace('Sky Sports 2.png','Sky_Sports_2.png')
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
     s=s.replace('WWE Network.png','WWE_Network.png')


     s=s.replace('.m3u8.ts','.ts')
 
     #if args.ini_file:
     #    s=s.replace('m3u8','ts')
   
   
     f=open(Clean_Name,'a')
     f.write(s)
     f.close()
     #if os.path.exists(Clean_Name):
     #    if os.path.exists(tmpFile):        
     #        os.remove(tmpFile)

     xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("TV Guide","Done.",3000, icon))
     
if mode=='run_maintenance_ini' : maintenance_ini()
