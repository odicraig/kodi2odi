import xbmcplugin,xbmcaddon
import time
import datetime
import xbmc
import os
import urllib2,json
import zipfile
import resources.lib.utils as utils
from resources.lib.croniter import croniter
from collections import namedtuple
from shutil import copyfile
import traceback

__addon__ = xbmcaddon.Addon()
__author__ = __addon__.getAddonInfo('author')
__scriptid__ = __addon__.getAddonInfo('id')
__scriptname__ = __addon__.getAddonInfo('name')
__cwd__ = __addon__.getAddonInfo('path')
__version__ = __addon__.getAddonInfo('version')
__language__ = __addon__.getLocalizedString
debug = __addon__.getSetting("debug")
offset1hr = __addon__.getSetting("offset1hr")

class epgUpdater:
    def __init__(self):

        updater_path = os.path.join(xbmc.translatePath('special://userdata'), 'addon_data/service.iptvsubsEpgUpdate')

        try:
          self.iptvsubs_addon = xbmcaddon.Addon('plugin.video.iptvsubs')
          utils.setSetting("pluginmissing", "false")
        except:
          utils.log("Failed to find iptvsubs addon")
          self.iptvsubs_addon = None
          utils.setSetting("pluginmissing", "true")
        try:
          self.pvriptvsimple_addon = xbmcaddon.Addon('pvr.iptvsimple')
        except:
          utils.log("Failed to find pvr.iptvsimple addon")
          self.pvriptvsimple_addon = None

        self.updateGroups()
        self.updateM3u()
 

    def updateGroups(self):
      self.groups = []
      for group in [ "ENGLISH", "SPORTS", "FOR ADULTS", "AFRICAN", "BANGLA", "French", "HINDI", "ITALIAN", "PERSIAN/KURDISH", "POLISH", "PORTUGUESE", "PUNJABI", "SOUTH INDIAN", "SPANISH", "URDU", "VIETNAMESE", "CHINESE", "EUROPEAN/BALKANS", "FILIPINO"]:
        if utils.getSetting(group) == 'true':
          self.groups.append(group)

    def settingsChanged(self):
        utils.log("Settings changed - update")
        old_settings = utils.refreshAddon()
        current_enabled = utils.getSetting("enable_scheduler")
        install_keyboard_file = utils.getSetting("install_keyboard_file")
        if install_keyboard_file == 'true':
          self.installKeyboardFile()
          utils.setSetting('install_keyboard_file', 'false')
          # Return since this is going to be run immediately again
          return
        
        # Update m3u file if wanted groups has changed
        old_groups = self.groups
        self.updateGroups()
        if self.groups != old_groups or old_settings.getSetting("username") != utils.getSetting("username") or old_settings.getSetting("password") != utils.getSetting("password") or old_settings.getSetting("mergem3u_fn") != utils.getSetting("merge3mu_fn") or old_settings.getSetting("mergem3u") != utils.getSetting("mergem3u"):
          self.update_m3u = True

        if old_settings.getSetting("timezone") != utils.getSetting("timezone"):
          if self.pvriptvsimple_addon:
            utils.log("Changing offset")
            self.checkAndUpdatePVRIPTVSetting("epgTimeShift", utils.getSetting("timezone"))

        if(self.enabled == "true"):
            #always recheck the next run time after an update
            utils.log('recalculate start time , after settings update')
            self.findNextRun(time.time())


    def updateM3u(self):
        if self.iptvsubs_addon is None:
            username = utils.getSetting('username')
            password = utils.getSetting('password')
            updater_path = os.path.join(xbmc.translatePath('special://userdata'), 'addon_data/service.iptvsubsEpgUpdate')
        else:
            username = self.iptvsubs_addon.getSetting('kasutajanimi')
            password = self.iptvsubs_addon.getSetting('salasona')
            updater_path = os.path.join(xbmc.translatePath('special://userdata'), 'addon_data/plugin.video.iptvsubs')
        if self.pvriptvsimple_addon is None:
            utils.log("pvriptvsimple addon missing")
            return

        self.checkAndUpdatePVRIPTVSetting("epgCache", "false")
        self.checkAndUpdatePVRIPTVSetting("epgPathType", "0")
        self.checkAndUpdatePVRIPTVSetting("epgPath", updater_path + '/iptvsubs_xmltv.xml.gz')
        self.checkAndUpdatePVRIPTVSetting("m3uPathType", "0")
        self.checkAndUpdatePVRIPTVSetting("m3uPath", "{0}/iptvsubs.m3u".format(updater_path))
        utils.log("Updating m3u file")

        cm_path = os.path.join(xbmc.translatePath('special://home'), 'addons/service.iptvsubsEpgUpdate/channel_guide_map.txt')

        channel_map = {}
        if os.path.isfile(cm_path):
          utils.log('Adding mapped guide ids')
          with open(cm_path) as f:
            for line in f:
              channel_name,guide_id = line.rstrip().split("\t")
              channel_map[channel_name] = guide_id

        panel_url = "http://2.welcm.tv:8000/panel_api.php?username={0}&password={1}".format(username, password)
        try:
          u = urllib2.urlopen(panel_url)
          j = json.loads(u.read())
        except:
          utils.log("Error connecting to server to create m3u file")
          return

        if j['user_info']['auth'] == 0:
          utils.showNotification("EPG Updater", "Error: Couldn't login to iptvsubs")
          self.enabled = False
          utils.setSetting("enable_scheduler", "False")
          return

        Channel = namedtuple('Channel', ['tvg_id', 'tvg_name', 'tvg_logo', 'group_title', 'channel_url'])
        channels = []

        group_idx = {}
        for idx,group in enumerate(self.groups):
          group_idx[group] = idx

        for ts_id, info in j["available_channels"].iteritems():
            channel_url = "http://2.welcm.tv:8000/live/{0}/{1}/{2}.ts".format(username, password, ts_id)
            tvg_id = "" 
            tvg_name = info['name']
            #if info['epg_channel_id'] and info['epg_channel_id'].endswith(".com"):
            #    tvg_id = info['epg_channel_id']
            if tvg_name in channel_map:
                tvg_id = 'tvg-id="{0}"'.format(channel_map[tvg_name])
            else:
                tvg_id = ""
            tvg_id = ""
            tvg_logo = ""
            group_title = info['category_name']
            if group_title == None:
                group_title = 'None'
            channels.append(Channel(tvg_id, tvg_name, tvg_logo, group_title, channel_url))

        wanted_channels = [c for c in channels if c.group_title in self.groups]
        wanted_channels.sort(key=lambda c: "{0}-{1}".format(group_idx[c.group_title], c.tvg_name))

        try:
          with open("{0}/iptvsubs.m3u".format(updater_path), "w") as m3u_f:
              m3u_f.write("#EXTM3U\n")
              for c in wanted_channels:
                  m3u_f.write('#EXTINF:-1 tvg-name="{0}" {1} tvg-logo="{2}" group-title="{3}",{0}\n{4}\n'.format(c.tvg_name, c.tvg_id, c.tvg_logo, c.group_title, c.channel_url))
              if utils.getSetting("mergem3u") == "true":
                mergem3u_fn = utils.getSetting("mergem3u_fn")
                if os.path.isfile(mergem3u_fn):
                  with open(mergem3u_fn) as mergem3u_f:
                    for line in mergem3u_f:
                      if line.startswith("#EXTM3U"):
                        continue
                      m3u_f.write(line)
        except Exception as e:
          utils.log("Error creating m3u file\n{0}\n{1}".format(e,traceback.format_exc()))


    def updateEpg(self):
        epgFileName = 'guide.xml.gz'
        epgFile = None
        if self.iptvsubs_addon is None:
            updater_path = os.path.join(xbmc.translatePath('special://userdata'), 'addon_data/service.iptvsubsEpgUpdate')
        else:
            updater_path = os.path.join(xbmc.translatePath('special://userdata'), 'addon_data/plugin.video.iptvsubs')
        iptvsimple_path = os.path.join(xbmc.translatePath('special://userdata'), 'addon_data/pvr.iptvsimple')

        try:
            response = urllib2.urlopen('https://github.com/psyc0n/epgninja/blob/master/'+epgFileName)
            epgFile = response.read()
        except:
            utils.log('StalkerSettings: Some issue with epg file')
            return

        if epgFile:
            epgFH = open(updater_path + '/iptvsubs_xmltv.xml.gz', "wb")
            epgFH.write(epgFile)
            epgFH.close()

        try:
            response = urllib2.urlopen('https://github.com/psyc0n/epgninja/raw/subs/genres.xml')
            epgFile = response.read()
        except:
            utils.log('StalkerSettings: Some issue with genres file')
            return

        if epgFile:
            epgFH = open(iptvsimple_path + '/genres.xml', "w")
            epgFH.write(epgFile)
            epgFH.close()



if __name__ == "__main__":
  epg_updater = epgUpdater()
  epg_updater.run()
