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

if cConfig().getSetting('bypassDNSlock') == 'true':
    from resources.lib.handler.requestHandler import cRequestHandlerwDNS as cRequestHandler

SITE_IDENTIFIER = 'megakino'
SITE_NAME = 'Megakino'
SITE_ICON = 'megakino.png'

# Global search function is thus deactivated!
if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'false':
    SITE_GLOBAL_SEARCH = False
    logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)

# Domain Abfrage
DOMAIN = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '.domain', 'megakino.rip') # Domain Auswahl \xc3\x83\xc2\xbcber die xStream Einstellungen m\xc3\x83\xc2\xb6glich
STATUS = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '_status') # Status Code Abfrage der Domain
ACTIVE = cConfig().getSetting('plugin_' + SITE_IDENTIFIER) # Ob Plugin aktiviert ist oder nicht

URL_MAIN = 'https://' + DOMAIN + '/'
# URL_MAIN = 'https://megakino.rip/'
URL_KINO = URL_MAIN + 'kinofilme/'
URL_MOVIES = URL_MAIN + 'films/'
URL_SERIES = URL_MAIN + 'serials/'
URL_ANIMATION = URL_MAIN + 'multfilm/'
URL_DOKU = URL_MAIN + 'documentary/'
URL_SEARCH = URL_MAIN + '?do=search&subaction=search&story=%s'

try:
    validater()
except:
    sys.exit()

def load(): # Menu structure of the site plugin
    logger.info('Load %s' % SITE_NAME)
    params = ParameterHandler()
    params.setParam('sUrl', URL_MAIN)
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30500), SITE_IDENTIFIER, 'showEntries'), params) # New
    params.setParam('sUrl', URL_KINO)
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30501), SITE_IDENTIFIER, 'showEntries'), params) # Current films in the cinema
    params.setParam('sUrl', URL_MOVIES)
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30502), SITE_IDENTIFIER, 'showEntries'), params) # Movies
    params.setParam('sUrl', URL_ANIMATION)
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30504), SITE_IDENTIFIER, 'showEntries'), params) # Animated Films
    params.setParam('sUrl', URL_SERIES)
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30511), SITE_IDENTIFIER, 'showEntries'), params) # Series
    params.setParam('sUrl', URL_DOKU)
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30505), SITE_IDENTIFIER, 'showEntries'), params) # Documentations
    params.setParam('sUrl', URL_MAIN)
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30506), SITE_IDENTIFIER, 'showGenre'), params) # Genre
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30520), SITE_IDENTIFIER, 'showSearch')) # Search
    cGui().setEndOfDirectory()


def showGenre():
    params = ParameterHandler()
    entryUrl = params.getValue('sUrl')
    oRequest = cRequestHandler(entryUrl)
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
    oRequest.cacheTime = 60 * 60 * 48  # 48 Stunden
    sHtmlContent = oRequest.request()
    pattern = '<div\s+class="side-block__title">Genres</div>(.*?)</ul>\s*</div>'
    isMatch, sHtmlContainer = cParser.parseSingleResult(sHtmlContent, pattern)
    if isMatch:
        pattern = 'href="([^"]+)">([^<]+)</a>'
        isMatch, aResult = cParser.parse(sHtmlContainer, pattern)
    if not isMatch:
        cGui().showInfo()
        return

    for sUrl, sName in aResult:
        params.setParam('sUrl', sUrl)
        cGui().addFolder(cGuiElement(sName, SITE_IDENTIFIER, 'showEntries'), params)
    cGui().setEndOfDirectory()


def showEntries(entryUrl=False, sGui=False, sSearchText=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    isTvshow = False
    if not entryUrl: entryUrl = params.getValue('sUrl')
    oRequest = cRequestHandler(entryUrl, ignoreErrors=(sGui is not False))
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 6  # 6 Stunden
    sHtmlContent = oRequest.request()
    pattern = '<a[^>]*class="poster grid-item.*?href="([^"]+).*?<img data-src="([^"]+).*?alt="([^"]+)".*?(.*?)</a>'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch:
        if not sGui: oGui.showInfo()
        return

    total = len(aResult)
    for sUrl, sThumbnail, sName, sDummy in aResult:
        if sSearchText and not cParser.search(sSearchText, sName):
            continue
        isQuality, sQuality = cParser.parseSingleResult(sDummy, 'poster__label">\+([\d]+)')  # Episoden Info mit +
        if not isQuality:
            isQuality, sQuality = cParser.parseSingleResult(sDummy, 'poster__label">\+\s([\d]+)') # Episoden Info mit + und Leerzeichen
        if not isQuality:
            isQuality, sQuality = cParser.parseSingleResult(sDummy, 'poster__label">([^<]+)') # QualitÃ¤t bei Filmen
        isYear, sYear = cParser.parseSingleResult(sDummy, '([\d]+)</li>\s+<li>')  # Release Jahr
        isDesc, sDesc = cParser.parseSingleResult(sDummy, 'class="poster__text[^"]+">([^<]+)')  # Beschreibung
        isTvshow, aResult = cParser.parse(sName, '\s+-\s+Staffel\s+\d+')
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showEpisodes' if isTvshow else 'showHosters')
        if isQuality:
            if isTvshow is True:
                if sQuality == 'Komplett':
                    oGuiElement.setQuality('Komplette Staffel')
                else:
                    oGuiElement.setQuality(sQuality + ' Episoden')
            else:
                oGuiElement.setQuality(sQuality)
        if isYear:
            oGuiElement.setYear(sYear)
        if isDesc:
            if sDesc[-1] != '.':
                sDesc += '...'
            oGuiElement.setDescription(sDesc)
        oGuiElement.setThumbnail(URL_MAIN + sThumbnail)
        oGuiElement.setMediaType('season' if isTvshow else 'movie')
        params.setParam('entryUrl', sUrl)
        params.setParam('sName', sName)
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('sDesc', sDesc)
        oGui.addFolder(oGuiElement, params, isTvshow, total)
    if not sGui and not sSearchText:
        isMatchNextPage, sNextUrl = cParser().parseSingleResult(sHtmlContent, '">\s*<a\s+href="([^"]+)">\D')
        if isMatchNextPage:
            params.setParam('sUrl', sNextUrl)
            oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
        oGui.setView('tvshows' if isTvshow else 'movies')
        oGui.setEndOfDirectory()


def showEpisodes():
    params = ParameterHandler()
    sUrl = params.getValue('entryUrl')
    sThumbnail = params.getValue("sThumbnail")
    sName = params.getValue('sName')
    sDesc = params.getValue('sDesc')
    isMatch, sShowName = cParser.parseSingleResult(sName, '(.*?)\s+-\s+Staffel\s+\d+')
    if not isMatch:
        cGui().showInfo()
        return
    isMatch, sSeason = cParser.parseSingleResult(sName, '\s+-\s+Staffel\s+(\d+)')
    if not isMatch:
        cGui().showInfo()
        return

    oRequest = cRequestHandler(sUrl)
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 4  # HTML Cache Zeit 4 Stunden
    sHtmlContent = oRequest.request()
    pattern = '<option\s+value="ep([^"]+)">([^<]+)</option>'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    total = len(aResult)
    for episode, episodeName in aResult:
        params.setParam('episodeId', episode)
        oGuiElement = cGuiElement(str(episodeName), SITE_IDENTIFIER, 'showEpisodeHosters')
        oGuiElement.setThumbnail(URL_MAIN + sThumbnail)
        oGuiElement.setDescription(sDesc)
        oGuiElement.setTVShowTitle(sName)
        oGuiElement.setSeason(sSeason)
        oGuiElement.setEpisode(episode)
        oGuiElement.setMediaType('episode')
        cGui().addFolder(oGuiElement, params, False, total)
    cGui().setView('episodes')
    cGui().setEndOfDirectory()


def showHosters():
    hosters = []
    sUrl = ParameterHandler().getValue('entryUrl')
    sHtmlContent = cRequestHandler(sUrl).request()
    #pattern = '<iframe.*?src="([^"]+)'
    #isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    pattern = '<iframe.*?src=([^\s]+)'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if isMatch:
        for sUrl in aResult:
            sQuality = '720'
        sUrl = sUrl.replace('"', '')
        if 'youtube' in sUrl: continue # Youtube Trailer
        sName =cParser.urlparse(sUrl)
        if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschlie\xc3\x83\xc5\xb8en
            hoster = {'link': sUrl, 'name': sName, 'displayedName': '%s [I][%sp][/I]' % (sName, sQuality), 'quality': sQuality, 'resolveable': True}
            hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters


def showEpisodeHosters():
    hosters = []
    sUrl = ParameterHandler().getValue('entryUrl')
    episodeId = 'ep' + ParameterHandler().getValue('episodeId')
    sHtmlContent = cRequestHandler(sUrl).request()
    pattern = '<select\s+name="pmovie__select-items"\s+class="[^"]+"\s+style="[^"]+"\s+id="%s">\s*(.*?)\s*</select>' % episodeId
    isMatch, sContainer = cParser.parseSingleResult(sHtmlContent, pattern)
    if isMatch:
        pattern = '<option\s+value="([^"]+)">'
        isMatch, aResult = cParser.parse(sContainer, pattern)
        if isMatch:
            for sUrl in aResult:
                hoster = {'link': sUrl, 'name': cParser.urlparse(sUrl)}
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
    showEntries(URL_SEARCH % cParser.quotePlus(sSearchText), oGui, sSearchText)
