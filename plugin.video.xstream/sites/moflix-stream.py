# -*- coding: utf-8 -*-
# Python 3
# Always pay attention to the translations in the menu!
# HTML LangzeitCache hinzugef\xc3\x83\xc2\xbcgt
# showEntries: 6 Stunden
# showSeasons: 6 Stunden
# showEpisodes: 4 Stunden
# Seite vollst\xc3\x83\xc2\xa4ndig mit JSON erstellt

import json

from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.tools import logger, cParser, validater
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui

SITE_IDENTIFIER = 'moflix-stream'
SITE_NAME = 'Moflix-Stream'
SITE_ICON = 'moflix-stream.png'

# Global search function is thus deactivated!
if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'false':
 SITE_GLOBAL_SEARCH = False
 logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)

# Domain Abfrage
DOMAIN = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '.domain', 'moflix-stream.xyz') # Domain Auswahl \xc3\x83\xc2\xbcber die xStream Einstellungen m\xc3\x83\xc2\xb6glich
STATUS = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '_status') # Status Code Abfrage der Domain
ACTIVE = cConfig().getSetting('plugin_' + SITE_IDENTIFIER) # Ob Plugin aktiviert ist oder nicht

URL_MAIN = 'https://' + DOMAIN + '/'
# URL_MAIN = 'https://moflix-stream.xyz/'
# Search Links
URL_SEARCH = URL_MAIN + 'api/v1/search/%s?query=%s&limit=8'
# Genre
URL_VALUE = URL_MAIN + 'api/v1/channel/%s?channelType=channel&restriction=&paginate=simple'
# Hoster
URL_HOSTER = URL_MAIN + 'api/v1/titles/%s?load=images,genres,productionCountries,keywords,videos,primaryVideo,seasons,compactCredits'

try:
    validater()
except:
    sys.exit()

def load():
    logger.info("Load %s" % SITE_NAME)
    params = ParameterHandler()
    params.setParam('page', (1))
    params.setParam('sUrl', URL_VALUE % 'now-playing')
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30500), SITE_IDENTIFIER, 'showEntries'), params) # Neues
    params.setParam('sUrl', URL_VALUE % 'movies')
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30502), SITE_IDENTIFIER, 'showEntries'), params) # Movies
    params.setParam('sUrl', URL_VALUE % 'top-rated-movies')
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30509), SITE_IDENTIFIER, 'showEntries'), params) # Top Movies
    params.setParam('sUrl', URL_VALUE % 'series')
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30511), SITE_IDENTIFIER, 'showEntries'), params) # Series
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30543), SITE_IDENTIFIER, 'showCollections'), params) # Collections
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30520), SITE_IDENTIFIER, 'showSearch')) # Search
    cGui().setEndOfDirectory()


def showCollections():
    params = ParameterHandler()
    params.setParam('sUrl', URL_VALUE % 'the-dc-universum-collection')
    cGui().addFolder(cGuiElement('The DC Superhelden Collection', SITE_IDENTIFIER, 'showEntries'), params) # The DC Superhelden Collection
    params.setParam('sUrl', URL_VALUE % 'fast-furious-movie-collection')
    cGui().addFolder(cGuiElement('The Fast & Furious Collection', SITE_IDENTIFIER, 'showEntries'), params) # The DC Superhelden Collection
    params.setParam('sUrl', URL_VALUE % 'the-marvel-cinematic-universe-collection')
    cGui().addFolder(cGuiElement('The Marvel Cinematic Universe Collection', SITE_IDENTIFIER, 'showEntries'), params) # The Marvel Cinematic Universe Collection
    params.setParam('sUrl', URL_VALUE % 'bud-spencer-terence-hill-collection')
    cGui().addFolder(cGuiElement('The Bud Spencer & Terence Hill Collection', SITE_IDENTIFIER, 'showEntries'), params) # The Bud Spencer & Terence Hill Collection
    params.setParam('sUrl', URL_VALUE % 'the-star-trek-movies-collection')
    cGui().addFolder(cGuiElement('The Star Trek Kinofilm Collection', SITE_IDENTIFIER, 'showEntries'), params) # The Star Trek Kinofilm Collection
    params.setParam('sUrl', URL_VALUE % 'the-star-wars-collection')
    cGui().addFolder(cGuiElement('The Ultimate Star Wars Collection', SITE_IDENTIFIER, 'showEntries'), params) # The Ultimate Star Wars Collection
    params.setParam('sUrl', URL_VALUE % 'the-james-bond-collection')
    cGui().addFolder(cGuiElement('The James Bond Collection', SITE_IDENTIFIER, 'showEntries'), params) # The James Bond Collection
    params.setParam('sUrl', URL_VALUE % 'the-olsenbande-collection')
    cGui().addFolder(cGuiElement('The Olsenbande Collection', SITE_IDENTIFIER, 'showEntries'), params) # The Olsenbande Collection
    params.setParam('sUrl', URL_VALUE % 'the-mission-impossible-collection')
    cGui().addFolder(cGuiElement('The Ethan Hunt Collection', SITE_IDENTIFIER, 'showEntries'), params) # The Ethan Hunt Collection
    params.setParam('sUrl', URL_VALUE % 'the-jason-bourne-collection')
    cGui().addFolder(cGuiElement('The Jason Bourne Collection', SITE_IDENTIFIER, 'showEntries'), params) # The Jason Bourne Collection
    params.setParam('sUrl', URL_VALUE % 'top-kids-liste')
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30503), SITE_IDENTIFIER, 'showEntries'), params) # Kids
    cGui().setEndOfDirectory()


def showEntries(entryUrl=False, sGui=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    # Parameter laden
    if not entryUrl:
        entryUrl = params.getValue('sUrl')
    iPage = int(params.getValue('page'))
    oRequest = cRequestHandler(entryUrl + '&page=' + str(iPage) if iPage > 0 else entryUrl, ignoreErrors=(sGui is not False))
    oRequest.addHeaderEntry('Referer', params.getValue('sUrl'))
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 6 # 6 Stunden
    jSearch = json.loads(oRequest.request()) # Lade JSON aus dem Request der URL
    if not jSearch: return # Wenn Suche erfolglos - Abbruch
    aResults = jSearch['channel']['content']['data']
    total = len(aResults)
    if len(aResults) == 0:
        if not sGui: oGui.showInfo()
        return
    for i in aResults:
        sId = i['id'] # ID des Films / Serie f\xc3\x83\xc2\xbcr die weitere URL
        sName = i['name'] # Name des Films / Serie
        if 'is_series' in i: isTvshow = i['is_series'] # Wenn True dann Serie
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showSeasons' if isTvshow else 'showHosters')
        if 'release_date' in i and len(str(i['release_date'].split('-')[0].strip())) != '': oGuiElement.setYear(str(i['release_date'].split('-')[0].strip()))
        # sDesc = i['description']
        if 'description' in i and i['description'] != '': oGuiElement.setDescription(i['description']) # Suche nach Desc wenn nicht leer dann setze GuiElement
        # sThumbnail = i['poster']
        if 'poster' in i and i['poster'] != '': oGuiElement.setThumbnail(i['poster']) # Suche nach Poster wenn nicht leer dann setze GuiElement
        # sFanart = i['backdrop']
        if 'backdrop' in i and i['backdrop'] != '': oGuiElement.setFanart(i['backdrop']) # Suche nach Fanart wenn nicht leer dann setze GuiElement
        oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
        # Parameter \xc3\x83\xc2\xbcbergeben
        params.setParam('entryUrl', URL_HOSTER % sId)
        params.setParam('sThumbnail', i['poster'])
        params.setParam('sName', sName)
        oGui.addFolder(oGuiElement, params, isTvshow, total)
        if not sGui:
            sPageNr = int(params.getValue('page'))
            if sPageNr == 0:
                sPageNr = 2
            else:
                sPageNr += 1
        params.setParam('page', int(sPageNr))
        oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
    oGui.setView('tvshows' if isTvshow else 'movies')
    oGui.setEndOfDirectory()


def showSeasons(sGui=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    # Parameter laden
    # https://moflix-stream.xyz/api/v1/titles/dG1kYnxzZXJpZXN8NzE5MTI=?load=images,genres,productionCountries,keywords,videos,primaryVideo,seasons,compactCredits
    entryUrl = params.getValue('entryUrl')
    sThumbnail = params.getValue('sThumbnail')
    oRequest = cRequestHandler(entryUrl)
    oRequest.addHeaderEntry('Referer', entryUrl)
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 6 # 6 Stunden
    jSearch = json.loads(oRequest.request()) # Lade JSON aus dem Request der URL
    if not jSearch: return # Wenn Suche erfolglos - Abbruch
    sDesc = jSearch['title']['description'] # Lade Beschreibung aus JSON
    aResults = jSearch['seasons']['data']
    aResults = sorted(aResults, key=lambda k: k['number']) # Sortiert die Staffeln nach Nummer aufsteigend
    total = len(aResults)
    if len(aResults) == 0:
        if not sGui: oGui.showInfo()
        return
    for i in aResults:
        sId = i['title_id'] # ID \xc3\x83\xc2\xa4ndert sich !!!
        sSeasonNr = str(i['number']) # Staffel Nummer
        oGuiElement = cGuiElement('Staffel ' + sSeasonNr, SITE_IDENTIFIER, 'showEpisodes')
        oGuiElement.setMediaType('season')
        oGuiElement.setSeason(sSeasonNr)
        oGuiElement.setThumbnail(sThumbnail)
        if sDesc != '': oGuiElement.setDescription(sDesc)
        params.setParam('sSeasonNr', sSeasonNr)
        params.setParam('sId', sId)
        cGui().addFolder(oGuiElement, params, True, total)
    cGui().setView('seasons')
    cGui().setEndOfDirectory()


def showEpisodes(sGui=False):
    oGui = cGui()
    params = ParameterHandler()
    # Parameter laden
    sId = params.getValue('sId')
    sSeasonNr = params.getValue('sSeasonNr')
    sUrl = URL_MAIN + 'api/v1/titles/%s/seasons/%s/episodes?perPage=100&query=&page=1' % (sId, sSeasonNr) #Hep 02.12.23: Abfrage f\xc3\x83\xc2\xbcr einzelne Episoden per query force auf 100 erh\xc3\x83\xc2\xb6ht
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('Referer', sUrl)
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 4 # 4 Stunden
    jSearch = json.loads(oRequest.request()) # Lade JSON aus dem Request der URL
    if not jSearch: return # Wenn Suche erfolglos - Abbruch
    #aResults = jSearch['episodes']['data'] # Ausgabe der Suchresultate von jSearch
    aResults = jSearch['pagination']['data'] # Ausgabe der Suchresultate von jSearch
    total = len(aResults) # Anzahl aller Ergebnisse
    if len(aResults) == 0:
        if not sGui: oGui.showInfo()
        return
    for i in aResults:
        sName = i['name'] # Episoden Titel
        sEpisodeNr = str(i['episode_number']) # Episoden Nummer
        sThumbnail = i['poster'] # Episoden Poster
        oGuiElement = cGuiElement('Episode ' + sEpisodeNr + ' - ' + sName, SITE_IDENTIFIER, 'showHosters')
        if 'description' in i and i['description'] != '': oGuiElement.setDescription(i['description']) # Suche nach Desc wenn nicht leer dann setze GuiElement
        oGuiElement.setEpisode(sEpisodeNr)
        oGuiElement.setSeason(sSeasonNr)
        oGuiElement.setMediaType('episode')
        oGuiElement.setThumbnail(sThumbnail)
        # Parameter setzen
        params.setParam('entryUrl', URL_MAIN + 'api/v1/titles/%s/seasons/%s/episodes/%s?load=videos,compactCredits,primaryVideo' % (sId, sSeasonNr, sEpisodeNr))
        oGui.addFolder(oGuiElement, params, False, total)
    oGui.setView('episodes')
    oGui.setEndOfDirectory()


def showSearchEntries(entryUrl=False, sGui=False, sSearchText=''):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    # Parameter laden
    if not entryUrl: entryUrl = params.getValue('sUrl')
    oRequest = cRequestHandler(entryUrl, ignoreErrors=(sGui is not False))
    oRequest.addHeaderEntry('Referer', entryUrl)
    jSearch = json.loads(oRequest.request()) # Lade JSON aus dem Request der URL
    if not jSearch: return # Wenn Suche erfolglos - Abbruch
    aResults = jSearch['results'] # Ausgabe der Suchresultate von jSearch
    total = len(aResults) # Anzahl aller Ergebnisse
    if len(aResults) == 0: # Wenn Resultate 0 zeige Benachrichtigung
        if not sGui: oGui.showInfo()
        return
    isTvshow = False
    for i in aResults:
        if 'person' in i['model_type']: continue # Personen in der Suche ausblenden
        sId = i['id'] # ID des Films / Serie f\xc3\x83\xc2\xbcr die weitere URL
        sName = i['name'] # Name des Films / Serie
        sYear = str(i['release_date'].split('-')[0].strip())
        if sSearchText.lower() and not cParser().search(sSearchText, sName.lower()): continue
        if 'is_series' in i: isTvshow = i['is_series'] # Wenn True dann Serie
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showSeasons' if isTvshow else 'showHosters')
        if sYear != '': oGuiElement.setYear(sYear) # Suche bei year nach 4 stelliger Zahl
        #sDesc = i['description']
        if 'description' in i and i['description'] != '': oGuiElement.setDescription(i['description']) # Suche nach Desc wenn nicht leer dann setze GuiElement
        # sThumbnail = i['poster']
        if 'poster' in i and i['poster'] != '': oGuiElement.setThumbnail(i['poster']) # Suche nach Desc wenn nicht leer dann setze GuiElement
        # sFanart = i['backdrop']
        if 'backdrop' in i and i['backdrop'] != '': oGuiElement.setFanart(i['backdrop']) # Suche nach Desc wenn nicht leer dann setze GuiElement
        oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
        # Parameter setzen
        params.setParam('entryUrl', URL_HOSTER % sId)
        params.setParam('sThumbnail', i['poster'])
        params.setParam('sName', sName)
        oGui.addFolder(oGuiElement, params, isTvshow, total)
    if not sGui:
        oGui.setView('tvshows' if isTvshow else 'movies')
    oGui.setEndOfDirectory()


def showHosters(sGui=False):
    oGui = sGui if sGui else cGui()
    hosters = []
    sUrl = ParameterHandler().getValue('entryUrl')
    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('Referer', sUrl)
    jSearch = json.loads(oRequest.request()) # Lade JSON aus dem Request der URL
    if not jSearch: return # Wenn Suche erfolglos - Abbruch
    if ParameterHandler().getValue('mediaType') == 'movie': #Bei MediaTyp Filme nutze das Result
        aResults = jSearch['title']['videos'] # Ausgabe der Suchresultate von jSearch f\xc3\x83\xc2\xbcr Filme
    else:
        aResults = jSearch['episode']['videos'] # Ausgabe der Suchresultate von jSearch f\xc3\x83\xc2\xbcr Episoden
    # total = len(aResults) # Anzahl aller Ergebnisse
    if len(aResults) == 0:
        if not sGui: oGui.showInfo()
        return
    for i in aResults:
        sQuality = str(i['quality'])
        if 'None' in sQuality: sQuality = '720p'
        sUrl = i['src']
        if 'veev' in sUrl: # Link verf\xc3\x83\xc2\xa4lscht es kann dadurch beim Resolve eine Fehlermeldung geben
            Request = cRequestHandler(sUrl, caching=False)
            Request.request()
            sUrl = Request.getRealUrl() # hole reale URL von der Umleitung
        if 'Mirror' in i['name']: # Wenn Mirror als sName hole realen Name aus der URL
            sName = cParser.urlparse(sUrl)
        else:
            sName = i['name'].split('-')[0].strip()
        if 'Moflix-Stream.Click' in sName:
            sName = 'FileLions'
        if 'Moflix-Stream.Day' in sName:
            sName = 'VidGuard'
        sName = sName.split('.')[0].strip() # Trenne Endung nach . ab
        if cConfig().isBlockedHoster(sUrl)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschlie\xc3\x83\xc5\xb8en
        if 'youtube' in sUrl: continue # Trailer ausblenden
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
    # https://moflix-stream.xyz/api/v1/search/Super%20Mario?query=Super+Mario&limit=8
    # Suche mit Quote und QuotePlus beim Suchtext
    sID1 = cParser().quote(sSearchText)
    sID2 = cParser().quotePlus(sSearchText)
    showSearchEntries(URL_SEARCH % (sID1, sID2), oGui, sSearchText)
