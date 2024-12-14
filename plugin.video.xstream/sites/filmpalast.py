# -*- coding: utf-8 -*-
# Python 3
# Always pay attention to the translations in the menu!
# Sprachauswahl f\xc3\x83\xc2\xbcr Filme
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

if cConfig().getSetting('bypassDNSlock') == 'true':
    from resources.lib.handler.requestHandler import cRequestHandlerwDNS as cRequestHandler


SITE_IDENTIFIER = 'filmpalast'
SITE_NAME = 'FilmPalast'
SITE_ICON = 'filmpalast.png'

# Global search function is thus deactivated!
if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'false':
    SITE_GLOBAL_SEARCH = False
    logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)

# Domain Abfrage
DOMAIN = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '.domain', 'filmpalast.to') # Domain Auswahl \xc3\x83\xc2\xbcber die xStream Einstellungen m\xc3\x83\xc2\xb6glich
STATUS = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '_status') # Status Code Abfrage der Domain
ACTIVE = cConfig().getSetting('plugin_' + SITE_IDENTIFIER) # Ob Plugin aktiviert ist oder nicht

URL_MAIN = 'https://' + DOMAIN
# URL_MAIN = 'https://filmpalast.to'
URL_MOVIES = URL_MAIN + '/movies/%s'
URL_SERIES = URL_MAIN + '/serien/view'
URL_ENGLISH = URL_MAIN + '/search/genre/Englisch'
URL_SEARCH = URL_MAIN + '/search/title/%s'

try:
    validater()
except:
    sys.exit()

def load(): # Menu structure of the site plugin
    logger.info('Load %s' % SITE_NAME)
    params = ParameterHandler()
    params.setParam('sUrl', URL_MAIN)
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30500), SITE_IDENTIFIER, 'showEntries'), params) # New
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30502), SITE_IDENTIFIER, 'showMovieMenu'), params) # Movies
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30511), SITE_IDENTIFIER, 'showSeriesMenu'), params) # Series
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30520), SITE_IDENTIFIER, 'showSearch'), params) # Search
    cGui().setEndOfDirectory()


def showMovieMenu(): # Menu structure of movie menu
    params = ParameterHandler()
    sLanguage = cConfig().getSetting('prefLanguage')
    if sLanguage == '0' or '1':    # Alle Sprachen oder Deutsch
        params.setParam('sUrl', URL_MOVIES % 'new')
        cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30500), SITE_IDENTIFIER, 'showEntries'), params)   # New
        params.setParam('sUrl', URL_MOVIES % 'top')
        cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30509), SITE_IDENTIFIER, 'showEntries'), params)  # Top movies
        params.setParam('sUrl', URL_MOVIES % 'imdb')
        cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30510), SITE_IDENTIFIER, 'showEntries'), params) # IMDB rating
        if sLanguage == '0': # Nur bei Alle Sprachen
            params.setParam('sUrl', URL_ENGLISH)
            cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30104), SITE_IDENTIFIER, 'showEntries'), params) # English
        params.setParam('sUrl', URL_MOVIES % 'new')
        params.setParam('value', 'genre')
        cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30506), SITE_IDENTIFIER, 'showValue'), params)    # Genre
        params.setParam('value', 'movietitle')
        cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30517), SITE_IDENTIFIER, 'showValue'), params)  # From A-Z
        cGui().setEndOfDirectory()
    if sLanguage == '2':    # English
        params.setParam('sUrl', URL_ENGLISH)
        cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30104), SITE_IDENTIFIER, 'showEntries'), params) # English
        cGui().setEndOfDirectory()
    elif sLanguage == '3':    # Japanisch
        cGui().showLanguage()
        cGui().setEndOfDirectory()


def showSeriesMenu(): # Menu structure of series menu
    params = ParameterHandler()
    params.setParam('sUrl', URL_SERIES)
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30511), SITE_IDENTIFIER, 'showEntries'), params)  # Series
    params.setParam('value', 'movietitle')
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30517), SITE_IDENTIFIER, 'showValue'), params)  # From A-Z
    cGui().setEndOfDirectory()


def showValue():
    params = ParameterHandler()
    value = params.getValue("value")
    oRequest = cRequestHandler(params.getValue('sUrl'))
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 24 # HTML Cache Zeit 1 Tag
    sHtmlContent = oRequest.request()
    pattern = '<section[^>]id="%s">(.*?)</section>' % value # Suche in der Section EintrÃ¤ge
    isMatch, sContainer = cParser.parseSingleResult(sHtmlContent, pattern)
    if isMatch:
        isMatch, aResult = cParser.parse(sContainer, 'href="([^"]+)">([^<]+)')
    if not isMatch:
        cGui().showInfo()
        return

    for sUrl, sName in aResult:
        #sUrl = sUrl.replace('Ã¶', '&#xF6') # Fix fÃ¼r Genre KomÃ¶die #Todo global setzten
        params.setParam('sUrl', sUrl)
        cGui().addFolder(cGuiElement(sName, SITE_IDENTIFIER, 'showEntries'), params)
    cGui().setEndOfDirectory()


def showEntries(entryUrl=False, sGui=False, sSearchText=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    oRequest = cRequestHandler(entryUrl, ignoreErrors=(sGui is not False))
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 6  # 6 Stunden
    sHtmlContent = oRequest.request()
    pattern = '<article[^>]*>\s*<a href="([^"]+)" title="([^"]+)">\s*<img src=["\']([^"\']+)["\'][^>]*>(.*?)</article>'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch:
        pattern = '<a[^>]*href="([^"]*)"[^>]*title="([^"]*)"[^>]*>[^<]*<img[^>]*src=["\']([^"\']*)["\'][^>]*>\s*</a>(\s*)</article>'
        isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch:
        if not sGui: oGui.showInfo()
        return

    total = len(aResult)
    for sUrl, sName, sThumbnail, sDummy in aResult:
        isTvshow, aResult = cParser.parse(sName, 'S\d\dE\d\d')
        # seriesname should not be crippled here!
        if sSearchText and not cParser().search(sSearchText, sName):
            continue
        if sThumbnail.startswith('/'):
            sThumbnail = URL_MAIN + sThumbnail
        isYear, sYear = cParser.parseSingleResult(sDummy, 'Jahr:[^>]([\d]+)')
        isDuration, sDuration = cParser.parseSingleResult(sDummy, '[Laufzeit][Spielzeit]:[^>]([\d]+)')
        isRating, sRating = cParser.parseSingleResult(sDummy, 'Imdb:[^>]([^<]+)')
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showSeasons' if isTvshow else 'showHosters')
        oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
        oGuiElement.setThumbnail(sThumbnail)
        if isYear:
            oGuiElement.setYear(sYear)
        if isDuration:
            oGuiElement.addItemValue('duration', sDuration)
        if isRating:
            oGuiElement.addItemValue('rating', sRating.replace(',', '.'))
        # Parameter Ã¼bergeben
        if sUrl.startswith('//'):
            params.setParam('entryUrl', 'https:' + sUrl)
        else:
            params.setParam('entryUrl', sUrl)
        params.setParam('sName', sName)
        params.setParam('sThumbnail', sThumbnail)
        oGui.addFolder(oGuiElement, params, isTvshow, total)
    if not sGui and not sSearchText:
        pattern = '<a class="pageing[^"]*"\s*href=([^>]+)>[^\+]+\+</a>\s*</div>'
        isMatchNextPage, sNextUrl = cParser.parseSingleResult(sHtmlContent, pattern)
        if isMatchNextPage:
            sNextUrl = sNextUrl.replace("'", "").replace('"', '')
            if sNextUrl.startswith('/'):
                sNextUrl = URL_MAIN + sNextUrl
            params.setParam('sUrl', sNextUrl)
            oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
        oGui.setView('tvshows' if isTvshow else 'movies')
        oGui.setEndOfDirectory()


def showSeasons():
    params = ParameterHandler()
    # Parameter laden
    sUrl = params.getValue('entryUrl')
    sThumbnail = params.getValue("sThumbnail")
    sName = params.getValue('sName')
    oRequest = cRequestHandler(sUrl)
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 6  # HTML Cache Zeit 6 Stunden
    sHtmlContent = oRequest.request()
    pattern = '<a[^>]*class="staffTab"[^>]*data-sid="(\d+)"[^>]*>'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch:
        cGui().showInfo()
        return

    isDesc, sDesc = cParser.parseSingleResult(sHtmlContent, '"description">([^<]+)')
    total = len(aResult)
    for sSeason in aResult:
        oGuiElement = cGuiElement('Staffel ' + str(sSeason), SITE_IDENTIFIER, 'showEpisodes')
        oGuiElement.setTVShowTitle(sName)
        oGuiElement.setSeason(sSeason)
        oGuiElement.setMediaType('season')
        oGuiElement.setThumbnail(sThumbnail)
        if isDesc:
            oGuiElement.setDescription(sDesc)
        cGui().addFolder(oGuiElement, params, True, total)
    cGui().setView('seasons')
    cGui().setEndOfDirectory()


def showEpisodes():
    params = ParameterHandler()
    # Parameter laden
    sUrl = params.getValue('entryUrl')
    sThumbnail = params.getValue("sThumbnail")
    sSeason = params.getValue('season')
    sShowName = params.getValue('TVShowTitle')
    oRequest = cRequestHandler(sUrl)
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 4  # HTML Cache Zeit 4 Stunden
    sHtmlContent = oRequest.request()
    pattern = '<div[^>]*class="staffelWrapperLoop[^"]*"[^>]*data-sid="%s">(.*?)</ul></div>' % sSeason
    isMatch, sContainer = cParser.parseSingleResult(sHtmlContent, pattern)
    if not isMatch:
        cGui().showInfo()
        return

    pattern = 'href="([^"]+)'
    isMatch, aResult = cParser.parse(sContainer, pattern)
    isDesc, sDesc = cParser.parseSingleResult(sHtmlContent, '"description">([^<]+)')
    total = len(aResult)
    for sUrl in aResult:
        isMatch, sName = cParser.parseSingleResult(sUrl, 'e(\d+)')
        oGuiElement = cGuiElement('Episode ' + str(sName), SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setTVShowTitle(sShowName)
        oGuiElement.setSeason(sSeason)
        oGuiElement.setEpisode(sName)
        oGuiElement.setMediaType('episode')
        if sUrl.startswith('//'):
            params.setParam('entryUrl', 'https:' + sUrl)
        else:
            params.setParam('entryUrl', sUrl)
        if isDesc:
            oGuiElement.setDescription(sDesc)
        cGui().addFolder(oGuiElement, params, False, total)
    cGui().setView('episodes')
    cGui().setEndOfDirectory()


def showHosters():
    sUrl = ParameterHandler().getValue('entryUrl')
    sHtmlContent = cRequestHandler(sUrl).request()
    pattern = 'hostName">([^<]+).*?(http[^"]+)' # Hoster Link
    releaseQuality = 'class="rb">.*?(\d\d\d+)p\.' # Release QualitÃ¤t
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    isQuality, sQuality = cParser.parseSingleResult(sHtmlContent, releaseQuality)  # sReleaseQuality auslesen z.B. 1080
    if not isQuality: sQuality = '720'
    hosters = []
    if isMatch:
        for sName, sUrl in aResult:
            if 'filemoon' or 'swiftload' in sUrl:
                sName = cParser.urlparse(sUrl).split('.')[0].strip()
                sUrl = sUrl + '$$https://filmpalast.to/' # Referer hinzugef\xc3\x83\xc2\xbcgt
            if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschlie\xc3\x83\xc5\xb8en
            hoster = {'link': sUrl, 'name': sName, 'displayedName': '%s [I][%sp][/I]' % (sName, sQuality),
            'quality': sQuality} # Qualit\xc3\x83\xc2\xa4t Anzeige aus Release Eintrag
            hosters.append(hoster)
        else:
            sName = cParser.urlparse(sUrl).split('.')[0].strip()
            if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschlie\xc3\x83\xc5\xb8en
            hoster = {'link': sUrl, 'name': sName, 'displayedName': '%s [I][%sp][/I]' % (sName, sQuality), 'quality': sQuality} # Qualit\xc3\x83\xc2\xa4t Anzeige aus Release Eintrag
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
    showEntries(URL_SEARCH % cParser().quotePlus(sSearchText), oGui, sSearchText)

