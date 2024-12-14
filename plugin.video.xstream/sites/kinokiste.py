# -*- coding: utf-8 -*-
# Python 3
# Always pay attention to the translations in the menu!
# HTML LangzeitCache hinzugef\xc3\x83\xc2\xbcgt
# showValue: 24 Stunden
# showEntries: 6 Stunden
# showEpisodes: 4 Stunden
 
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.tools import logger, cParser, validater
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui

SITE_IDENTIFIER = 'kinokiste'
SITE_NAME = 'Kinokiste'
SITE_ICON = 'kinokistetech.png'

# Global search function is thus deactivated!
if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'false':
 SITE_GLOBAL_SEARCH = False
 logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)

# Domain Abfrage
DOMAIN = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '.domain', 'kinokiste.cloud') # Domain Auswahl \xc3\x83\xc2\xbcber die xStream Einstellungen m\xc3\x83\xc2\xb6glich
STATUS = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '_status') # Status Code Abfrage der Domain
ACTIVE = cConfig().getSetting('plugin_' + SITE_IDENTIFIER) # Ob Plugin aktiviert ist oder nicht

URL_MAIN = 'https://' + DOMAIN + '/'
# URL_MAIN = 'https://kinokiste.cloud/'
URL_NEW = URL_MAIN + 'kinofilme-online/'
URL_KINO = URL_MAIN + 'aktuelle-kinofilme-im-kino/'
URL_ANIMATION = URL_MAIN + 'animation/'
URL_SERIES = URL_MAIN + 'serienstream-deutsch/'
URL_SEARCH = URL_MAIN + '?do=search&subaction=search&story=%s'

try:
    validater()
except:
    sys.exit()

def load(): # Menu structure of the site plugin
    logger.info('Load %s' % SITE_NAME)
    params = ParameterHandler()
    params.setParam('sUrl', URL_NEW)
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30500), SITE_IDENTIFIER, 'showEntries'), params) # New
    params.setParam('sUrl', URL_KINO)
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30501), SITE_IDENTIFIER, 'showEntries'), params) # Current films in the cinema
    params.setParam('sUrl', URL_ANIMATION)
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30504), SITE_IDENTIFIER, 'showEntries'), params) # Animated Films
    params.setParam('sUrl', URL_SERIES)
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30511), SITE_IDENTIFIER, 'showEntries'), params) # Series
    params.setParam('sUrl', URL_MAIN)
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30506), SITE_IDENTIFIER, 'showGenre'), params) # Genre
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30520), SITE_IDENTIFIER, 'showSearch')) # Search
    cGui().setEndOfDirectory()


def showGenre():
    folder = []
    params = ParameterHandler()
    entryUrl = params.getValue('sUrl')
    oRequest = cRequestHandler(entryUrl)
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 48  # 48 Stunden
    sHtmlContent = oRequest.request()
    pattern = '<nav\s+class="header-nav">(.*?)</nav>'
    isMatch, sHtmlContainer = cParser.parseSingleResult(sHtmlContent, pattern)
    if isMatch:
        pattern = '<li>\s*<a\s+href="([^"]+)">([^<]+)</a></li>'
        isMatch, aResult = cParser.parse(sHtmlContainer, pattern)
    if not isMatch:
        cGui().showInfo()
        return

    for sUrl, sName in aResult:
        if cParser.search('DMCA', sName):
            continue
        params.setParam('sUrl', sUrl)
        cGui().addFolder(cGuiElement(sName, SITE_IDENTIFIER, 'showEntries'), params)
    cGui().setEndOfDirectory()


def showEntries(entryUrl=False, sGui=False, sSearchText=False):
    folder = []
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    isTvshow = False
    if not entryUrl: entryUrl = params.getValue('sUrl')
    oRequest = cRequestHandler(entryUrl, ignoreErrors=(sGui is not False))
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 6  # 6 Stunden
    sHtmlContent = oRequest.request()
    pattern = '<section class="fl-item.*?href="([^"]+).*?alt="([^"]+).*?src="([^"]+).*?(.*?)</section>'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch:
        if not sGui: oGui.showInfo()
        return

    total = len(aResult)
    for sUrl, sName, sThumbnail, sDummy in aResult:
        # Abfrage der voreingestellten Sprache
        sLanguage = cConfig().getSetting('prefLanguage')
        if (sLanguage == '1' and 'English*' in sName):   # Deutsch
            continue
        if (sLanguage == '2' and not 'English*' in sName):   # English
            continue
        elif sLanguage == '3':    # Japanisch
            cGui().showLanguage()
            continue
        if sSearchText and not cParser.search(sSearchText, sName):
            continue
        if sThumbnail[0] == '/':
            sThumbnail = sThumbnail[1:]
        isQuality, sQuality = cParser.parseSingleResult(sDummy, 'fl-quality[^"]+">([^<]+)')  # QualitÃ¤t
        isInfoEpisode, sInfoEpisode = cParser.parseSingleResult(sDummy, 'mli-ep">ep.([\d]+)')  # Episodenanzahl
        isTvshow, aResult = cParser.parse(sName, '\s+-\s+Staffel\s+\d+')
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showEpisodes' if isTvshow else 'showHosters')
        oGuiElement.setThumbnail(URL_MAIN + sThumbnail)
        oGuiElement.setMediaType('season' if isTvshow else 'movie')
        if isQuality:
            oGuiElement.setQuality(sQuality)
        if isInfoEpisode:
            oGuiElement.setInfo(sInfoEpisode + ' Episoden')
        params.setParam('entryUrl', sUrl)
        params.setParam('sName', sName)
        params.setParam('sThumbnail', sThumbnail)

        oGui.addFolder(oGuiElement, params, isTvshow, total)

    if not sGui and not sSearchText:
        isMatchNextPage, sNextUrl = cParser().parseSingleResult(sHtmlContent, '<span\s+class="swchItem">\s*<a\s+href="([^"]+)">&raquo;</a>\s*</span>')
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
    pattern = '<li\s+id="serie-([^"]+)">\s*<a\s+href="#">([^<]+)</a>'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)

    isDesc, sDesc = cParser.parseSingleResult(sHtmlContent, '"description"[^>]content="([^"]+)')
    total = len(aResult)
    for episode, episodeName in aResult:
        params.setParam('episodeId', episode)
        oGuiElement = cGuiElement(str(episodeName), SITE_IDENTIFIER, 'showEpisodeHosters')
        oGuiElement.setThumbnail(URL_MAIN + sThumbnail)
        if isDesc:
            oGuiElement.setDescription(sDesc)
        oGuiElement.setTVShowTitle(sShowName)
        oGuiElement.setSeason(sSeason)
        if '_' in episode:
            oGuiElement.setEpisode(episode.partition('_')[2])
        else:
            oGuiElement.setEpisode(episode)
        oGuiElement.setMediaType('episode')
        cGui().addFolder(oGuiElement, params, False, total)
    cGui().setView('episodes')
    cGui().setEndOfDirectory()



def showHosters():
    hosters = []
    sUrl = ParameterHandler().getValue('entryUrl')
    sHtmlContent = cRequestHandler(sUrl).request()
    pattern = '<li>\s*<a\s+href="#"\s+data-link="([^"]+)">\s*<i>\s*</i>\s*([^<]+)</a>\s*</li>'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if isMatch:
        for sUrl, sHoster in aResult:
            sName = cParser.urlparse(sUrl)
            if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschlieÃŸen
            hoster = {'link': sUrl, 'name': sHoster}
            hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters


def showEpisodeHosters():
    hosters = []
    sUrl = ParameterHandler().getValue('entryUrl')
    episodeId = ParameterHandler().getValue('episodeId')
    sHtmlContent = cRequestHandler(sUrl).request()
    pattern = '<li>\s*<a\s+href="#"\s+id="[^"]+-%s"\s+data-link="([^"]+)">\s*([^<]+)</a>\s*</li>' % episodeId
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if isMatch:
        for sUrl, sHoster in aResult:
            sName = cParser.urlparse(sUrl)
            #if cConfig().isBlockedHoster(sName, checkResolver=True): continue # Hoster aus settings.xml oder deaktivierten Resolver ausschlieÃŸen
            if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschlieÃŸen
            hoster = {'link': sUrl, 'name': sHoster}
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
