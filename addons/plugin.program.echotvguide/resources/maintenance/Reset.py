import time
import os
import xbmc
import xbmcgui
import xbmcaddon

databasePath = xbmc.translatePath('special://userdata/addon_data/plugin.program.echotvguide')
d = xbmcgui.Dialog()

for root, dirs, files in os.walk(databasePath,topdown=True):
	dirs[:] = [d for d in dirs]
	for name in files:
		if "guide.cfg" in name:
			try:
				os.remove(os.path.join(root,name))
			except: 
				d = xbmcgui.Dialog()
				d.ok('TV Guide', 'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using ECHO TV Guide[/COLOR]')
				pass
		else:
			continue
			
for root, dirs, files in os.walk(databasePath,topdown=True):
	dirs[:] = [d for d in dirs]
	for name in files:
		if "source.db" in name:
			try:
				os.remove(os.path.join(root,name))
			except: 
				d = xbmcgui.Dialog()
				d.ok('TV Guide', 'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using ECHO TV Guide[/COLOR]')
				pass
		else:
			continue
			
for root, dirs, files in os.walk(databasePath,topdown=True):
	dirs[:] = [d for d in dirs]
	for name in files:
		if "guide.xml" in name:
			try:
				os.remove(os.path.join(root,name))
			except: 
				d = xbmcgui.Dialog()
				d.ok('TV Guide', 'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using ECHO TV Guide[/COLOR]')
				pass
		else:
			continue

d = xbmcgui.Dialog()			
d.ok('TV Guide', 'Please restart the guide for ','the changes to take effect','[COLOR yellow]Thank you for using ECHO TV Guide[/COLOR]')
