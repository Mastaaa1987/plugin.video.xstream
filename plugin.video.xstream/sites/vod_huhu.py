# -*- coding: utf-8 -*-
# Python 3
# Always pay attention to the translations in the menu!
# HTML LangzeitCache hinzugef\xc3\x83\xc2\xbcgt
# showGenre: 48 Stunden
# showEntries: 6 Stunden
# showSeasons: 6 Stunden
# showEpisodes: 4 Stunden

import json

from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.tools import logger, cParser, validater
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui

SITE_IDENTIFIER = 'vod_huhu'
SITE_NAME = 'VoD - Huhu'
SITE_ICON = 'vod_huhu.png'

# Global search function is thus deactivated!
#if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'false':
 #SITE_GLOBAL_SEARCH = False
 #logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)
SITE_GLOBAL_SEARCH = False
cConfig().setSetting('global_search_' + SITE_IDENTIFIER, 'false')
logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)

# Domain Abfrage
DOMAIN = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '.domain', 'www.huhu.to') # Domain Auswahl \xc3\x83\xc2\xbcber die xStream Einstellungen m\xc3\x83\xc2\xb6glich
STATUS = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '_status') # Status Code Abfrage der Domain
ACTIVE = cConfig().getSetting('plugin_' + SITE_IDENTIFIER) # Ob Plugin aktiviert ist oder nicht

URL_MAIN = 'https://' + DOMAIN + '/web-vod/'
# URL_MAIN = 'https://www.kool.to/web-vod/'
URL_VALUE = URL_MAIN + 'api/list?id=%s'
URL_ITEM = URL_MAIN + 'api/links?id=%s'
URL_HOSTER = URL_MAIN + 'api/get?link='
URL_SEARCH_MOVIES = URL_MAIN + 'api/list?id=movie.popular.search=%s'
URL_SEARCH_SERIES = URL_MAIN + 'api/list?id=series.popular.search=%s'

try:
    validater()
except:
    sys.exit()

def load(): # Menu structure of the site plugin
    logger.info('Load %s' % SITE_NAME)
    params = ParameterHandler()
    params.setParam('sUrl', URL_VALUE % 'movie.popular') # Url (.null.1) f\xc3\x83\xc2\xbcr Seiten Aufbau 60 Eintr\xc3\x83\xc2\xa4ge pro Seite weiter in +3er Schritten (.null.4) 1/4/7/10/13 usw.
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30521), SITE_IDENTIFIER, 'showEntries'), params) # Popular Movies
    params.setParam('sUrl', URL_VALUE % 'movie.trending')
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30545), SITE_IDENTIFIER, 'showEntries'), params) # Trending Movies
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30547), SITE_IDENTIFIER, 'showSearchMovies')) # Search Movies
    params.setParam('sUrl', URL_VALUE % 'series.popular')
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30519), SITE_IDENTIFIER, 'showEntries'), params) # Popular Series
    params.setParam('sUrl', URL_VALUE % 'series.trending')
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30546), SITE_IDENTIFIER, 'showEntries'), params) # Trending Series
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30548), SITE_IDENTIFIER, 'showSearchSeries')) # Search Series
    cGui().setEndOfDirectory()


def showEntries(entryUrl=False, sGui=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    # Parameter laden
    if not entryUrl:
        entryUrl = params.getValue('sUrl')
    oRequest = cRequestHandler(entryUrl, caching=False, ignoreErrors=True)
    oRequest.addHeaderEntry('Referer', URL_MAIN)
    oRequest.addHeaderEntry('Origin', 'https://' + DOMAIN)
    oRequest.removeNewLines(False)
    jSearch = json.loads(oRequest.request()) # Lade JSON aus dem Request der URL
    if not jSearch: return # Wenn Suche erfolglos - Abbruch
    aResults = jSearch['data']
    sNextUrl = jSearch['next'] # F\xc3\x83\xc2\xbcr die n\xc3\x83\xc2\xa4chste Seite
    total = len(aResults)
    if len(aResults) == 0:
        if not sGui: oGui.showInfo()
        return
    isTvshow = False
    for i in aResults:
        sId = i['id'] # ID des Films / Serie f\xc3\x83\xc2\xbcr die weitere URL
        sName = i['name'] # Name des Films / Serie
        isTvshow = True if 'series' in i['id'] else False
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showSeasons' if isTvshow else 'showHosters')
        if 'releaseDate' in i and len(str(i['releaseDate'].split('-')[0].strip())) != '': oGuiElement.setYear(str(i['releaseDate'].split('-')[0].strip()))
        if 'description' in i and i['description'] != '': oGuiElement.setDescription(i['description']) # Suche nach Desc wenn nicht leer dann setze GuiElement
        # sThumbnail = i['poster']
        if 'poster' in i and i['poster'] != '':
            oGuiElement.setThumbnail (i['poster']) # Suche nach Poster wenn nicht leer dann setze GuiElement
        else:
            oGuiElement.setThumbnail('default.png')
        # sFanart = i['backdrop']
        if 'backdrop' in i and i['backdrop'] != '': oGuiElement.setFanart(i['backdrop']) # Suche nach Fanart wenn nicht leer dann setze GuiElement
        oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
        # Parameter \xc3\x83\xc2\xbcbergeben
        params.setParam('sUrl', URL_ITEM % sId)
        params.setParam('sId', sId)
        params.setParam('sName', sName)
        oGui.addFolder(oGuiElement, params, isTvshow, total)
        if not sGui:
            sNextUrl = URL_MAIN + 'api/list?id=' + sNextUrl
            params.setParam('sUrl', sNextUrl)
            oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
        oGui.setView('tvshows' if isTvshow else 'movies')
    oGui.setEndOfDirectory()


def showSeasons(entryUrl=False, sGui=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    # Parameter laden
    sId = params.getValue('sId')
    if not entryUrl:
        entryUrl = URL_MAIN + 'api/info?id=' + sId
    oRequest = cRequestHandler(entryUrl, caching=False, ignoreErrors=True)
    oRequest.addHeaderEntry('Referer', URL_MAIN)
    oRequest.addHeaderEntry('Origin', 'https://' + DOMAIN)
    oRequest.removeNewLines(False)
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 6 # 6 Stunden
    jSearch = json.loads(oRequest.request()) # Lade JSON aus dem Request der URL
    if not jSearch: return # Wenn Suche erfolglos - Abbruch
    sThumbnail = jSearch['poster']
    if not 'poster' in jSearch: sThumbnail = 'default.png'
    sDesc = jSearch['description']
    if not 'description' in jSearch: sDesc = ''
    sFanart = jSearch['backdrop']
    if not 'backdrop' in jSearch: sFanart = 'default.png'
    aResults = sorted(jSearch['seasons'], key=lambda reverse:True) # Sortiert die Staffeln
    total = len(aResults)
    if len(aResults) == 0:
        if not sGui: oGui.showInfo()
        return
    for sSeasonNr in aResults:
        if sSeasonNr == '0': # Wenn Staffel 0 verf\xc3\x83\xc2\xbcgbar
            oGuiElement = cGuiElement('Extras', SITE_IDENTIFIER, 'showEpisodes')
        else:
            oGuiElement = cGuiElement('Staffel ' + sSeasonNr, SITE_IDENTIFIER, 'showEpisodes')
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setDescription(sDesc)
        oGuiElement.setFanart(sFanart)
        oGuiElement.setMediaType('season')
        oGuiElement.setSeason(sSeasonNr)
        params.setParam('sSeasonNr', sSeasonNr)
        params.setParam('entryUrl', entryUrl)
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('sDesc', sDesc)
        params.setParam('sFanart', sFanart)
        cGui().addFolder(oGuiElement, params, True, total)
        cGui().setView('seasons')
    cGui().setEndOfDirectory()


def showEpisodes(sGui=False):
    oGui = cGui()
    params = ParameterHandler()
    # Parameter laden
    sSeasonNr = params.getValue('sSeasonNr')
    entryUrl = params.getValue('entryUrl')
    sThumbnail = params.getValue('sThumbnail')
    sDesc = params.getValue('sDesc')
    sFanart = params.getValue('sFanart')
    oRequest = cRequestHandler(entryUrl, caching=False, ignoreErrors=True)
    oRequest.addHeaderEntry('Referer', URL_MAIN)
    oRequest.addHeaderEntry('Origin', 'https://' + DOMAIN)
    oRequest.removeNewLines(False)
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 4 # 4 Stunden
    jSearch = json.loads(oRequest.request()) # Lade JSON aus dem Request der URL
    if not jSearch: return # Wenn Suche erfolglos - Abbruch
    aResults = jSearch['seasons'][sSeasonNr] # Ausgabe der Suchresultate von jSearch + Season Nummer
    total = len(aResults) # Anzahl aller Ergebnisse
    if len(aResults) == 0:
        if not sGui: oGui.showInfo()
        return
    for i in aResults:
        sEpisodeNr = str(i['episode']) # Episoden Nummer
        sId = i['id'] # Episoden Id
        sName = i['name'] # Episoden Name
        oGuiElement = cGuiElement('Episode ' + sEpisodeNr + ' - ' + sName, SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setEpisode(sEpisodeNr)
        oGuiElement.setSeason(sSeasonNr)
        oGuiElement.setMediaType('episode')
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setDescription(sDesc)
        oGuiElement.setFanart(sFanart)
        # Parameter setzen
        params.setParam('sUrl', URL_ITEM % sId)
        oGui.addFolder(oGuiElement, params, False, total)
        oGui.setView('episodes')
    oGui.setEndOfDirectory()


def showHosters(sGui=False):
    oGui = sGui if sGui else cGui()
    hosters = []
    params = ParameterHandler()
    sUrl = params.getValue('sUrl')
    oRequest = cRequestHandler(sUrl, caching=False, ignoreErrors=True)
    oRequest.addHeaderEntry('Referer', URL_MAIN)
    oRequest.addHeaderEntry('Origin', 'https://' + DOMAIN)
    oRequest.removeNewLines(False)
    jSearch = json.loads(oRequest.request()) # Lade JSON aus dem Request der URL
    if not jSearch: return # Wenn Suche erfolglos - Abbruch
    sLanguage = cConfig().getSetting('prefLanguage')
    aResults = jSearch
    if len(aResults) == 0:
        if not sGui: oGui.showInfo()
        return
    for i in aResults:
        hUrl = i['url']
        sName = i['name'].split('(')[0].strip()
        if '(' in i['name']: # Wenn Qualit\xc3\x83\xc2\xa4t in Klammern angegeben (1080p)
            sQuality = i['name'].split('(')[1].strip()
            sQuality = sQuality.replace (')','')
        else:
            sQuality = '720p'
        sUrl = URL_HOSTER + hUrl
        sName = cParser.urlparse(sUrl) + ' - ' + sName
        sLang = i['language'].split('(')[0].strip()
        if sLanguage == '1': # Voreingestellte Sprache Deutsch in settings.xml
            if 'en' in sLang:
                continue
            if sLang == 'de':
                sLang = 'Deutsch' # Anzeige der Sprache
        if sLanguage == '2': # Voreingestellte Sprache Englisch in settings.xml
            if 'de' in sLang:
                continue
            if sLang == 'en':
                sLang = 'English' # Anzeige der Sprache
        if sLanguage == '3': # Voreingestellte Sprache Japanisch in settings.xml
            continue
        if sLanguage == '0': # Alle Sprachen
            if sLang == 'de':
                sLang = 'Deutsch' # Anzeige der Sprache
            if sLang == 'en':
                sLang = 'English' # Anzeige der Sprache
        hoster = {'link': sUrl, 'name': sName, 'displayedName': '%s %s [I][%s][/I]' % (sName, sLang, sQuality), 'quality': sQuality, 'languageCode': sLanguage, 'resolveable': True}
        hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters


def getHosterUrl(sUrl=False):
    Request = cRequestHandler(sUrl, caching=False)
    Request.request()
    sUrl = Request.getRealUrl() # hole reale URL von der Umleitung
    return [{'streamUrl': sUrl, 'resolved': False}]


def showSearchMovies():
    sSearchText = cGui().showKeyBoard()
    if not sSearchText: return
    _searchMovies(False, sSearchText)
    cGui().setEndOfDirectory()


def _searchMovies(oGui, sSearchText):
    showEntries(URL_SEARCH_MOVIES % cParser().quotePlus(sSearchText), oGui)


def showSearchSeries():
    sSearchText = cGui().showKeyBoard()
    if not sSearchText: return
    _searchSeries(False, sSearchText)
    cGui().setEndOfDirectory()


def _searchSeries(oGui, sSearchText):
    showEntries(URL_SEARCH_SERIES % cParser().quotePlus(sSearchText), oGui)
