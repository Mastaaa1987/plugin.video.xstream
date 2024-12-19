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

SITE_IDENTIFIER = 'movie4k'
SITE_NAME = 'Movie4k'
SITE_ICON = 'movie4k.png'

# Global search function is thus deactivated!
if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'false':
 SITE_GLOBAL_SEARCH = False
 logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)

# Domain Abfrage
DOMAIN = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '.domain', 'movie4k.bid') # Domain Auswahl \xc3\x83\xc2\xbcber die xStream Einstellungen m\xc3\x83\xc2\xb6glich
STATUS = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '_status') # Status Code Abfrage der Domain
ACTIVE = cConfig().getSetting('plugin_' + SITE_IDENTIFIER) # Ob Plugin aktiviert ist oder nicht

URL_MAIN = 'https://' + DOMAIN + '/'
# URL_MAIN = 'https://movie4k.bid/'
URL_KINO = URL_MAIN + 'aktuelle-kinofilme-im-kino'
URL_MOVIES = URL_MAIN + 'kinofilme-online'
URL_SERIES = URL_MAIN + 'serienstream-deutsch'
URL_SEARCH = URL_MAIN + 'index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=%s'

try:
    validater()
except:
    sys.exit()

def load(): # Menu structure of the site plugin
    logger.info('Load %s' % SITE_NAME)
    params = ParameterHandler()
    params.setParam('sUrl', URL_KINO)
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30501), SITE_IDENTIFIER, 'showEntries'), params) # Current films in the cinema
    params.setParam('sUrl', URL_MOVIES)
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30502), SITE_IDENTIFIER, 'showEntries'), params) # Movies
    params.setParam('sUrl', URL_SERIES)
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30511), SITE_IDENTIFIER, 'showEntries'), params) # Series
    params.setParam('sCont', 'Jahr')
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30508), SITE_IDENTIFIER, 'showValue'), params) # Release Year
    params.setParam('sCont', 'Land')
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30402), SITE_IDENTIFIER, 'showValue'), params) # Countries
    params.setParam('sCont', 'Genre')
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30506), SITE_IDENTIFIER, 'showValue'), params) # Genre
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30520), SITE_IDENTIFIER, 'showSearch')) # Search
    cGui().setEndOfDirectory()


def showValue():
    params = ParameterHandler()
    oRequest = cRequestHandler(URL_MAIN)
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 48 # 48 Stunden
    sHtmlContent = oRequest.request()
    isMatch, sContainer = cParser.parseSingleResult(sHtmlContent, '%s<.*?</ul>' % params.getValue('sCont'))
    if isMatch:
        pattern = 'href="([^"]+).*?true">([^"]+)</a>'
        isMatch, aResult = cParser.parse(sContainer, pattern)
        if not isMatch: return
        for sUrl, sName in aResult:
            if sUrl.startswith('/'):
                sUrl = URL_MAIN + sUrl
            if 'ino' in sName or 'erien' in sName: continue
            params.setParam('sUrl', sUrl)
            cGui().addFolder(cGuiElement(sName, SITE_IDENTIFIER, 'showEntries'), params)
    cGui().setEndOfDirectory()


def showEntries(entryUrl=False, sGui=False, sSearchText=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    oRequest = cRequestHandler(entryUrl, ignoreErrors=(sGui is not False))
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 6 # 6 Stunden
    sHtmlContent = oRequest.request()
    pattern = '<article.*?(.*?)<a.*?href="([^"]+).*?<h3>([^<]+).*?(.*?)</article>'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch:
        if not sGui: oGui.showInfo()
        return

    total = len(aResult)
    for sInfo, sUrl, sName, sDummy in aResult:
        if sSearchText and not cParser().search(sSearchText, sName): continue
        # Abfrage der voreingestellten Sprache
        sLanguage = cConfig().getSetting('prefLanguage')
        if (sLanguage == '1' and 'English*' in sName): # Deutsch
            continue
        if (sLanguage == '2' and not 'English*' in sName): # English
            continue
        elif sLanguage == '3': # Japanisch
            cGui().showLanguage()
            continue
        isInfoEpisode, sInfo = cParser.parseSingleResult(sInfo, '</span>([\d]+)') # Episodenanzahl
        isThumbnail, sThumbnail = cParser.parseSingleResult(sDummy, 'data-src="([^"]+)') # Thumbnail
        isQuality, sQuality = cParser.parseSingleResult(sDummy, '<li>([^<]+)') # Qualit\xc3\x83\xc2\xa4t
        isYear, sYear = cParser.parseSingleResult(sDummy, 'class="white">([\d]+)') # Release Jahr
        isTvshow = True if 'taffel' in sName else False
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showEpisodes' if isTvshow else 'showHosters')
        oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
        if isThumbnail:
            sThumbnail = URL_MAIN + sThumbnail
            oGuiElement.setThumbnail(sThumbnail)
        if isYear:
            oGuiElement.setYear(sYear)
        if isQuality:
            oGuiElement.setQuality(sQuality)
        if isInfoEpisode:
            oGuiElement.setInfo(sInfo + ' Episoden')
        params.setParam('entryUrl', sUrl)
        params.setParam('sName', sName)
        params.setParam('sThumbnail', sThumbnail)
        oGui.addFolder(oGuiElement, params, isTvshow, total)
        if not sGui:
            isMatchNextPage, sNextUrl = cParser().parseSingleResult(sHtmlContent, 'N\xc3\x83\xc2\xa4chste[^>]Seite">[^>]*<a[^>]href="([^"]+)')
            if isMatchNextPage:
                if '/xfsearch/' not in entryUrl:
                    params.setParam('sUrl', sNextUrl)
                oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
        oGui.setView('tvshows' if 'taffel' in sName else 'movies')
    oGui.setEndOfDirectory()


def showEpisodes():
    params = ParameterHandler()
    sThumbnail = params.getValue('sThumbnail')
    entryUrl = params.getValue('entryUrl')
    oRequest = cRequestHandler(entryUrl)
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 4 # HTML Cache Zeit 4 Stunden
    sHtmlContent = oRequest.request()
    pattern = 'id="serie-(\d+)[^>](\d+).*?href="#">([^<]+)'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch: return
    isTvshow, sTVShowTitle = cParser.parseSingleResult(sHtmlContent, '<title>([^-]+)')
    isDesc, sDesc = cParser.parseSingleResult(sHtmlContent, 'name="description" content="([^"]+)')
    total = len(aResult)
    for sSeasonNr, sEpisodeNr, sName in aResult:
        oGuiElement = cGuiElement('Episode ' + sEpisodeNr, SITE_IDENTIFIER, 'showHosters')
        if isTvshow:
            oGuiElement.setTVShowTitle(sTVShowTitle.strip())
            oGuiElement.setSeason(sSeasonNr)
            oGuiElement.setEpisode(sEpisodeNr)
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setMediaType('episode')
        if isDesc:
            oGuiElement.setDescription(sDesc)
        params.setParam('sEpisodeNr', sName)
        params.setParam('entryUrl', entryUrl)
        cGui().addFolder(oGuiElement, params, False, total)
        cGui().setView('episodes')
    cGui().setEndOfDirectory()


def showHosters():
    hosters = []
    sHtmlContent = cRequestHandler(ParameterHandler().getValue('entryUrl')).request()
    if ParameterHandler().getValue('sEpisodeNr'):
        pass
    pattern = '%s<.*?</ul>' % ParameterHandler().getValue('sEpisodeNr')
    isMatch, sHtmlContent = cParser.parseSingleResult(sHtmlContent, pattern)
    isMatch, aResult = cParser().parse(sHtmlContent, 'link="([^"]+)">([^<]+)')
    if isMatch:
        sQuality = '720p'
    for sUrl, sName in aResult:
        if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschlie\xc3\x83\xc5\xb8en
        if 'railer' in sName: continue # Youtube Trailer
        elif 'vod' in sUrl: continue # VOD Link
        if sUrl.startswith('//'):
            sUrl = 'https:' + sUrl
        hoster = {'link': sUrl, 'name': sName, 'displayedName': '%s [I][%s][/I]' % (sName, sQuality), 'quality': sQuality, 'resolveable': True}
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

