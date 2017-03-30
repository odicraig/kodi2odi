
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
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#

import xbmc
import xbmcgui
import os
import zipfile



import xbmcaddon
import xbmcgui
import re
#import verify
import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import cookielib
import pickle
import time
import datetime


import xbmcvfs

HOME  = xbmc.translatePath('special://profile/')
addon = 'plugin.program.echotvguide'
PROFILE = xbmc.translatePath(os.path.join(HOME, 'addon_data', addon))
LINE1 = 'Backup file now being created.'
LINE2 = 'Please wait, this may take a while.'


def doBackup(backup):
    CUSTOM = '1'
    
    '''
    chanType = GetSetting('chan.type')
    logoType = GetSetting('logo.type')
    print 'Backup: Channel setting is %s' % chanType
    print 'Backup: Logo setting is %s' % logoType


    if (chanType == CUSTOM) or (logoType == CUSTOM):
        DialogOK('It appears you are using a custom location', 'for your channels or logos (Home Networking).', 'Please back-up EPG manually.')
        return
    '''
    
    print 'fuck'
    try:
        folder = getFolder('Please select a back-up folder location')

        if not folder:
            return False

        backupName = ''

        if backup == 'full':
            backupName = getText('Please enter a name for your full back-up', backupName)
        else:
            backupName = getText('Please enter a name for your line-up', backupName)

        filename = os.path.join(folder, backupName + '.zip')

        dp = Progress(LINE1, LINE2)

        success = doZipfile(backup, filename, dp)

        dp.close()

        if success: 
            DialogOK('Back-up successfully created')
        else:
            #dixie.DeleteFile(filename)
            print 'felete'
            
        return True

    except Exception, e:
        print e
    return False


def doZipfile(backup, outputFile, dp):
    zip = None

    if backup == 'full':
        ROOT = PROFILE
    else:
        ROOT = os.path.join(PROFILE, 'channels')

    source  = ROOT
    relroot = os.path.abspath(os.path.join(source, os.pardir))

    total = float(0)
    index = float(0)

    for root, dirs, files in os.walk(source):
        total += 1
        for file in files:
            total += 1

    for root, dirs, files in os.walk(source):
        if zip == None:
            zip = zipfile.ZipFile(outputFile, 'w', zipfile.ZIP_DEFLATED)

        index   += 1
        percent  = int(index / total * 100)
        if not updateProgress(dp, percent):
            return False

        local = os.path.relpath(root, relroot)

        for file in files:
            index   += 1
            percent  = int(index / total * 100)
            if not updateProgress(dp, percent):
                return False

            arcname  = os.path.join(local, file)
            filename = os.path.join(root, file)
            zip.write(filename, arcname)

    return True


def updateProgress(dp, percent):
    dp.update(percent, LINE1, LINE2)
    if not dp.iscanceled():
        return True

    return False


def getFolder(title):
    root   = xbmc.translatePath('special://userdata').split(os.sep, 1)[0] + os.sep
    folder = xbmcgui.Dialog().browse(3, title, 'files', '', False, False, root)

    return xbmc.translatePath(folder)


def getText(title, text='', hidden=False):
    kb = xbmc.Keyboard(text, title)
    kb.setHiddenInput(hidden)
    kb.doModal()
    if not kb.isConfirmed():
        return None

    text = kb.getText().strip()

    if len(text) < 1:
        return None

    return text






# 1
def GetSetting(param):
    return xbmcaddon.Addon(ADDONID).getSetting(param)
# 2
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

# 3
def DialogOK(line1, line2='', line3=''):
    d = xbmcgui.Dialog()
    d.ok(TITLE + ' - ' + VERSION, line1, line2 , line3)





if __name__ == '__main__':
    try:
        backup = sys.argv[1]
        doBackup(backup)
    except: pass

