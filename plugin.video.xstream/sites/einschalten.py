# -*- coding: utf-8 -*-
# Python 3
# Always pay attention to the translations in the menu!
# HTML LangzeitCache hinzugef\xc3\x83\xc2\xbcgt
# showValue: 48 Stunden
# showEntries: 6 Stunden
# showEpisodes: 4 Stunden

from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.tools import logger, cParser, validater
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui

SITE_IDENTIFIER = 'einschalten'
SITE_NAME = 'Einschalten'
SITE_ICON = 'einschalten.png'

# Global search function is thus deactivated!
if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'false':
 SITE_GLOBAL_SEARCH = False
 logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)

# Domain Abfrage
DOMAIN = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '.domain', 'einschalten.in') # Domain Auswahl \xc3\x83\xc2\xbcber die xStream Einstellungen m\xc3\x83\xc2\xb6glich
STATUS = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '_status') # Status Code Abfrage der Domain
ACTIVE = cConfig().getSetting('plugin_' + SITE_IDENTIFIER) # Ob Plugin aktiviert ist oder nicht

URL_MAIN = 'https://' + DOMAIN
# URL_MAIN = 'https://einschalten.in'
URL_NEW_MOVIES = URL_MAIN + '/movies'
URL_LAST_MOVIES = URL_MAIN + '/movies?order=added'
URL_COLLECTIONS = URL_MAIN + '/collections'
URL_SEARCH = URL_MAIN + '/search?query=%s'

try:
    validater()
except:
    sys.exit()

def load(): # Menu structure of the site plugin
    logger.info('Load %s' % SITE_NAME)
    params = ParameterHandler()
    params.setParam('sUrl', URL_NEW_MOVIES)
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30541), SITE_IDENTIFIER, 'showEntries'), params) # New Movies
    params.setParam('sUrl', URL_LAST_MOVIES)
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30549), SITE_IDENTIFIER, 'showEntriesLast'), params) # Recently added movies
    params.setParam('sUrl', URL_COLLECTIONS)
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30543), SITE_IDENTIFIER, 'showEntries'), params) # Collections
    params.setParam('sUrl', URL_NEW_MOVIES)
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30506), SITE_IDENTIFIER, 'showGenre'), params) # Genre
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30520), SITE_IDENTIFIER, 'showSearch')) # Search
    cGui().setEndOfDirectory()


def showGenre():
    params = ParameterHandler()
    oRequest = cRequestHandler(URL_NEW_MOVIES)
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 48 # 48 Stunden
    sHtmlContent = oRequest.request()
    pattern = '<select id="genre"(.*?)</select>'
    isMatch, sHtmlContainer = cParser.parseSingleResult(sHtmlContent, pattern)
    if isMatch:
        isMatch, aResult = cParser.parse(sHtmlContainer, 'value="([^"]+).*?>([^<]+)')
    if not isMatch:
        cGui().showInfo()
        return
    for sUrl, sName in aResult:
        entryUrl = URL_NEW_MOVIES + '?genre=' + sUrl
        params.setParam('sUrl', entryUrl)
        cGui().addFolder(cGuiElement(sName, SITE_IDENTIFIER, 'showEntries'), params)
    cGui().setEndOfDirectory()


def showEntries(entryUrl=False, sGui=False, sSearchText=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    oRequest = cRequestHandler(entryUrl, ignoreErrors=(sGui is not False))
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 6 # 6 Stunden
    iPage = int(params.getValue('page'))
    oRequest = cRequestHandler(entryUrl + '?page=' + str(iPage) if iPage > 0 else entryUrl, ignoreErrors=(sGui is not False))
    sHtmlContent = oRequest.request()
    pattern = 'class="group.*?href="([^"]+).*?title="([^"]+).*?img src="([^"]+).*?(.*?)</a>'
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    if not isMatch:
        if not sGui: oGui.showInfo()
        return

    total = len(aResult)
    for sUrl, sName, sThumbnail, sDummy in aResult:
        if sSearchText and not cParser.search(sSearchText, sName):
            continue
        isYear, sYear = cParser.parseSingleResult(sDummy, '</svg>\s([\d]+)</div>') # Release Jahr
        isCollections, aResult = cParser.parse(sUrl, '/collections')
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showCollections' if isCollections else 'showHosters')
        if isYear:
            oGuiElement.setYear(sYear)
        oGuiElement.setThumbnail(URL_MAIN + sThumbnail)
        oGuiElement.setMediaType('movie')
        params.setParam('sName', sName)
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('entryUrl', sUrl)
        oGui.addFolder(oGuiElement, params, isCollections, total)
        if not sGui and not sSearchText:
            sPageNr = int(params.getValue('page'))
        if sPageNr == 0:
            sPageNr = 2
        else:
            sPageNr += 1
        params.setParam('page', int(sPageNr))
        params.setParam('sUrl', entryUrl)
        oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
        oGui.setView('movies')
    oGui.setEndOfDirectory()


def showCollections(sGui=False, sSearchText=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    entryUrl = URL_MAIN + params.getValue('entryUrl')
    oRequest = cRequestHandler(entryUrl, ignoreErrors=(sGui is not False))
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 6 # 6 Stunden
    sHtmlContent = oRequest.request()
    pattern = 'class="group.*?href="([^"]+).*?title="([^"]+).*?img src="([^"]+).*?(.*?)</a>'
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    if not isMatch:
        if not sGui: oGui.showInfo()
        return
    total = len(aResult)
    for sUrl, sName, sThumbnail, sDummy in aResult:
        if sSearchText and not cParser.search(sSearchText, sName):
            continue
        isYear, sYear = cParser.parseSingleResult(sDummy, '</svg>\s([\d]+)</div>') # Release Jahr
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')
        if isYear:
            oGuiElement.setYear(sYear)
        oGuiElement.setThumbnail(URL_MAIN + sThumbnail)
        oGuiElement.setMediaType('movie')
        params.setParam('sName', sName)
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('entryUrl', sUrl)
        oGui.addFolder(oGuiElement, params, False, total)
        if not sGui and not sSearchText:
            params.setParam('sUrl', entryUrl)
        oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
        oGui.setView('movies')
    oGui.setEndOfDirectory()


def showEntriesLast(entryUrl=False, sGui=False, sSearchText=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    oRequest = cRequestHandler(entryUrl, ignoreErrors=(sGui is not False))
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 6 # 6 Stunden
    iPage = int(params.getValue('page'))
    oRequest = cRequestHandler(entryUrl + '&page=' + str(iPage) if iPage > 0 else entryUrl, ignoreErrors=(sGui is not False))
    sHtmlContent = oRequest.request()
    pattern = 'class="group.*?href="([^"]+).*?title="([^"]+).*?img src="([^"]+).*?(.*?)</a>'
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    if not isMatch:
        if not sGui: oGui.showInfo()
        return
    total = len(aResult)
    for sUrl, sName, sThumbnail, sDummy in aResult:
        if sSearchText and not cParser.search(sSearchText, sName):
            continue
        isYear, sYear = cParser.parseSingleResult(sDummy, '</svg>\s([\d]+)</div>') # Release Jahr
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')
        if isYear:
            oGuiElement.setYear(sYear)
        oGuiElement.setThumbnail(URL_MAIN + sThumbnail)
        oGuiElement.setMediaType('movie')
        params.setParam('sName', sName)
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('entryUrl', sUrl)
        oGui.addFolder(oGuiElement, params, False, total)
        if not sGui and not sSearchText:
            sPageNr = int(params.getValue('page'))
        if sPageNr == 0:
            sPageNr = 2
        else:
            sPageNr += 1
        params.setParam('page', int(sPageNr))
        params.setParam('sUrl', entryUrl)
        oGui.addNextPage(SITE_IDENTIFIER, 'showEntriesLast', params)
        oGui.setView('movies')
    oGui.setEndOfDirectory()


def showHosters():
    params = ParameterHandler()
    entryUrl = params.getValue('entryUrl')
    hosters = []
    sUrl = URL_MAIN + '/api' + entryUrl + '/watch'
    sHtmlContent = cRequestHandler(sUrl).request()
    pattern = 'streamUrl":"([^"]+)'
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    if not isMatch: return
    sQuality = '720p'
    for sUrl in aResult:
        sName = cParser.urlparse(sUrl)
        if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschlie\xc3\x83\xc5\xb8en
        hoster = {'link': sUrl, 'name': sName, 'displayedName': '%s [I][%s][/I]' % (sName, sQuality), 'quality': sQuality, 'resolved': True}
        hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters


def getHosterUrl(sUrl=False):
    return [{'streamUrl': sUrl, 'resolved': False}]


def showSearch():
    sSearchText = cGui().showKeyBoard()
    if not sSearchText: return
        _search(False, sSearchText)
    cGui().setEndOfDirectory()


def _search(oGui, sSearchText):
    showEntries(URL_SEARCH % cParser.quotePlus(sSearchText), oGui, sSearchText)'
