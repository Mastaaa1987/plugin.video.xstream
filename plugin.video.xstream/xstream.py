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

uItems=["kinotvbox@givmail.com","p-mayer-1981@web.de","kwakilein@freenet.de","taxero1010@carsik.com","kodibuilds@mail.de","kodiwelt@outlook.de","nicejudge66@youtmail.tk"]
uFitems=["rhaller@hotmail.de"]
uAitems=["rhall@mail.de"]

if xbmcaddon.Addon().getSetting('serienstream.user')in uItems:
    xbmcaddon.Addon().setSetting('serienstream.user','')
    xbmcaddon.Addon().setSetting('serienstream.pass','')
if xbmcaddon.Addon().getSetting('flimmerstube.user')in uFitems:
    xbmcaddon.Addon().setSetting('flimmerstube.user','')
    xbmcaddon.Addon().setSetting('flimmerstube.pass','')
if xbmcaddon.Addon().getSetting('anicloud.user')in uAitems:
    xbmcaddon.Addon().setSetting('anicloud.user','')
    xbmcaddon.Addon().setSetting('anicloud.pass','')
    xbmcaddon.Addon().setSetting('aniworld.user','')
    xbmcaddon.Addon().setSetting('aniworld.pass','')
if xbmcaddon.Addon().getSetting('aniworld.user')in uAitems:
    xbmcaddon.Addon().setSetting('aniworld.user','')
    xbmcaddon.Addon().setSetting('aniworld.pass','')
    xbmcaddon.Addon().setSetting('anicloud.user','')
    xbmcaddon.Addon().setSetting('anicloud.pass','')

def run():
    if chk('plugin.program.UpdateKinoTvBox')==1:
        sys.exit()
    elif chk('plugin.program.kodibuilds')==1:
        sys.exit()
    elif chk('plugin.program.kodibuilds.wizard')==1:
        sys.exit()
    elif chk('plugin.program.kodibuildswizard')==1:
        sys.exit()
    elif chk('plugin.program.kodibuilds-wizard')==1:
        sys.exit()
    elif chk('plugin.program.kodibuild')==1:
        sys.exit()
    elif chk('plugin.program.kodibuild.wizard')==1:
        sys.exit()
    elif chk('plugin.program.kodibuildwizard')==1:
        sys.exit()
    elif chk('plugin.program.kodibuild-wizard')==1:
        sys.exit()
    elif chk('plugin.program.kodiwelt')==1:
        sys.exit()
    elif chk('plugin.program.kodiwelt.wizard')==1:
        sys.exit()
    elif chk('plugin.program.kodiweltwizard')==1:
        sys.exit()
    elif chk('plugin.program.kodiwelt-wizard')==1:
        sys.exit()
    elif chk('script.module.xstream')==1:
        sys.exit()
    elif chk('plugin.program.notjust4nerds')==1:
        sys.exit()
    elif chk('plugin.program.supern')==1:
        sys.exit()
    elif chk('plugin.program.supernmatrix')==1:
        sys.exit()
    elif chk('plugin.video.stubevavoo')==1:
        sys.exit()
    elif chk('repository.xstream')==0:
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    parseUrl()

def chk(name):
    return xbmc.getCondVisibility('System.HasAddon(%s)'%name)==1

def search_dir():
    root_path=translatePath(os.path.join('special://home/addons/','%s'))
    addon_data_path=translatePath(os.path.join('special://home/userdata/addon_data/','%s'))
    if os.path.exists(root_path%'skin.aeon.nox.silvo.mortal.kombat'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.exists(root_path%'skin.aeon.nox.silvo.MK'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.exists(root_path%'skin.city.nox.silvo'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.exists(root_path%'skin.starwars'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.exists(root_path%'skin.star.wars'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.exists(root_path%'skin.aeon.nox.silvo.mariodonkey'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.exists(root_path%'skin.aeon.nox.silvo.mariovsdonkey'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.exists(root_path%'skin.braindead'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.exists(root_path%'skin.bt.braindead'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.exists(root_path%'skin.bt.frequency'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.exists(root_path%'skin.bier'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.exists(root_path%'skin.bierZeiT'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.exists(root_path%'repository.lokum.orhan'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.exists(root_path%'repository.kodiwelt'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.exists(root_path%'repository.kodibuild'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.exists(root_path%'repository.kodibuilds'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.exists(root_path%'repository.supernmatrix.addons'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.exists(root_path%'repository.supern-1.0'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.exists(root_path%'plugin.video.stubevavoo'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.exists(root_path%'kodi.commendrv'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif not os.path.exists(root_path%'repository.xstream'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path%'/script.skinshortcuts/skin.bt.braindead.hash'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path%'/script.skinshortcuts/skin.bt.frequency.hash'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path%'/script.skinshortcuts/skin.aeon.nox.silvo.MK.properties'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path%'/script.skinshortcuts/skin.aeon.nox.silvo.mariodonkey.properties'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path%'/script.skinshortcuts/skin.bierZeiT.properties'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path%'/script.skinshortcuts/skin.city.nox.silvo.properties'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path%'/script.skinshortcuts/plugin-program-kodibuilds-wizard.DATA.xml'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path%'/script.skinshortcuts/plugin-program-kodibuild-wizard.DATA.xml'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path%'/script.skinshortcuts/plugin-program-kodibuildwizard.DATA.xml'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path%'/script.skinshortcuts/plugin-program-kodibuilds-wizard-0.DATA.xml'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path%'/script.skinshortcuts/plugin-program-kodiwelt-wizard.DATA.xml'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path%'/script.skinshortcuts/plugin-program-kodiweltwizard.DATA.xml'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path%'/script.skinshortcuts/moflix.DATA.xml'):
        xbmcaddon.Addon().setSetting('xstream_norep','hogwarts')
        sys.exit()

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
        dialog.update((count + 1) * 50 // numPlugins, cConfig().getLocalizedString(30124) + str(pluginEntry['name']) + '...')
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
        dialog.update((count + 1) * 50 // numPlugins, cConfig().getLocalizedString(30124) + str(pluginEntry['name']) + '...')
        log(LOGMESSAGE + ' -> [xstream]: Searching for %s at %s' % (sSearchText, pluginEntry['id']), LOGNOTICE)

        t = threading.Thread(target=_pluginSearch, args=(pluginEntry, sSearchText, oGui), name=pluginEntry['name'])
        threads += [t]
        t.start()
    for count, t in enumerate(threads):
        t.join()
        if dialog.iscanceled(): return
        dialog.update((count + 1) * 50 // numPlugins + 50, t.getName() + cConfig().getLocalizedString(30125))
    dialog.close()
    # deactivate collectMode attribute because now we want the elements really added
    oGui._collectMode = False
    total = len(oGui.searchResults)
    dialog = xbmcgui.DialogProgress()
    dialog.create(cConfig().getLocalizedString(30126), cConfig().getLocalizedString(30127))
    for count, result in enumerate(sorted(oGui.searchResults, key=lambda k: k['guiElement'].getSiteName()), 1):
        if dialog.iscanceled(): return
        oGui.addFolder(result['guiElement'], result['params'], bIsFolder=result['isFolder'], iTotal=total)
        dialog.update(count * 100 // total, str(count) + cConfig().getLocalizedString(30128) + str(total) + ': ' + result['guiElement'].getTitle())
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
        log(traceback.format_exc())
