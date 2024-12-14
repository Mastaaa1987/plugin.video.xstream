# -*- coding: utf-8 -*-
# Python 3

import xbmc
import xbmcgui
import xbmcaddon
import hashlib
import re
import os

from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib import common
from resources.lib import pyaes
from resources.lib.config import cConfig
from xbmcaddon import Addon
from xbmcvfs import translatePath
from urllib.parse import quote, unquote, quote_plus, unquote_plus, urlparse
from html.entities import name2codepoint


# Aufgef\xc3\xbchrte Plattformen zum Anzeigen der Systemplattform
def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'Android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'Linux'
    elif xbmc.getCondVisibility('system.platform.linux.Raspberrypi'):
        return 'Linux/RPi'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'Windows'
    elif xbmc.getCondVisibility('system.platform.uwp'):
        return 'Windows UWP'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'OSX'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'ATV2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'iOS'
    elif xbmc.getCondVisibility('system.platform.darwin'):
        return 'iOS'
    elif xbmc.getCondVisibility('system.platform.xbox'):
        return 'XBOX'
    elif xbmc.getCondVisibility('System.HasAddon(service.coreelec.settings)'):
        return 'CoreElec'
    elif xbmc.getCondVisibility('System.HasAddon(service.libreelec.settings)'):
        return 'LibreElec'
    elif xbmc.getCondVisibility('System.HasAddon(service.osmc.settings)'):
        return 'OSMC'


# zeigt nach Update den Changelog als Popup an
def changelog():
    CHANGELOG_PATH = translatePath(os.path.join('special://home/addons/' + Addon().getAddonInfo('id') + '/', 'changelog.txt'))
    version = xbmcaddon.Addon().getAddonInfo('version')
    if xbmcaddon.Addon().getSetting('changelog_version') == version or not os.path.isfile(CHANGELOG_PATH):
        return
    xbmcaddon.Addon().setSetting('changelog_version', version)
    heading = cConfig().getLocalizedString(30275)
    with open(CHANGELOG_PATH, mode="r", encoding="utf-8") as f:
        cl_lines = f.readlines()
    announce = ''
    for line in cl_lines:
        announce += line
    textBox(heading, announce)


# zeigt die Entwickler Optionen Warnung als Popup an
def devWarning():
    POPUP_PATH = translatePath(os.path.join('special://home/addons/' + Addon().getAddonInfo('id') + '/resources/popup', 'devWarning.txt'))
    heading = cConfig().getLocalizedString(30322)
    with open(POPUP_PATH, mode='r', encoding='utf-8') as f:
        cl_lines = f.readlines()
    announce = ''
    for line in cl_lines:
        announce += line
    textBox(heading, announce)


# Erstellt eine Textbox
def textBox(heading, announce):
    class TextBox():

        def __init__(self, *args, **kwargs):
            self.WINDOW = 10147
            self.CONTROL_LABEL = 1
            self.CONTROL_TEXTBOX = 5
            xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, ))
            self.win = xbmcgui.Window(self.WINDOW)
            xbmc.sleep(500)
            self.setControls()

        def setControls(self):
            self.win.getControl(self.CONTROL_LABEL).setLabel(heading)
            try:
                f = open(announce)
                text = f.read()
            except:
                text = announce
            self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
            return

    TextBox()
    while xbmc.getCondVisibility('Window.IsVisible(10147)'):
        xbmc.sleep(500)


class cParser:
    @staticmethod
    def parseSingleResult(sHtmlContent, pattern):
        aMatches = None
        if sHtmlContent:
            aMatches = re.findall(pattern, sHtmlContent, flags=re.S | re.M)
            if len(aMatches) == 1:
                aMatches[0] = cParser.replaceSpecialCharacters(aMatches[0])
                return True, aMatches[0]
        return False, aMatches

    @staticmethod
    def replaceSpecialCharacters(s):
        # Umlaute Unicode konvertieren
        for t in (('\\/', '/'), ('&amp;', '&'), ('\\u00c4', 'ÃƒÂ„'), ('\\u00e4', 'ÃƒÂ¤'),
            ('\\u00d6', 'ÃƒÂ–'), ('\\u00f6', 'ÃƒÂ¶'), ('\\u00dc', 'ÃƒÂœ'), ('\\u00fc', 'ÃƒÂ¼'),
            ('\\u00df', 'ÃƒÂŸ'), ('\\u2013', '-'), ('\\u00b2', 'Ã‚Â²'), ('\\u00b3', 'Ã‚Â³'),
            ('\\u00e9', 'ÃƒÂ©'), ('\\u2018', 'Ã¢Â€Â˜'), ('\\u201e', 'Ã¢Â€Âž'), ('\\u201c', 'Ã¢Â€Âœ'),
            ('\\u00c9', 'ÃƒÂ‰'), ('\\u2026', '...'), ('\\u202fh', 'h'), ('\\u2019', 'Ã¢Â€Â™'),
            ('\\u0308', 'ÃŒÂˆ'), ('\\u00e8', 'ÃƒÂ¨'), ('#038;', ''), ('\\u00f8', 'ÃƒÂ¸'),
            ('Ã¯Â¼Â', '/'), ('\\u00e1', 'ÃƒÂ¡'), ('&#8211;', '-'), ('&#8220;', 'Ã¢Â€Âœ'), ('&#8222;', 'Ã¢Â€Âž'),
            ('&#8217;', 'Ã¢Â€Â™'), ('&#8230;', 'Ã¢Â€Â¦'), ('\\u00bc', 'Ã‚Â¼'), ('\\u00bd', 'Ã‚Â½'), ('\\u00be', 'Ã‚Â¾'),
            ('\\u2153', 'Ã¢Â…Â“')):
            try:
                s = s.replace(*t)
            except:
                pass
        # Umlaute HTML konvertieren
        for h in (('\\/', '/'), ('&#x26;', '&'), ('&#039;', "'"), ("&#39;", "'"),
            ('&#xC4;', 'ÃƒÂ„'), ('&#xE4;', 'ÃƒÂ¤'), ('&#xD6;', 'ÃƒÂ–'), ('&#xF6;', 'ÃƒÂ¶'),
            ('&#xDC;', 'ÃƒÂœ'), ('&#xFC;', 'ÃƒÂ¼'), ('&#xDF;', 'ÃƒÂŸ') , ('&#xB2;', 'Ã‚Â²'),
            ('&#xDC;', 'Ã‚Â³'), ('&#xBC;', 'Ã‚Â¼'), ('&#xBD;', 'Ã‚Â½'), ('&#xBE;', 'Ã‚Â¾'),
            ('&#8531;', 'Ã¢Â…Â“')):
            try:
                s = s.replace(*h)
            except:
                pass
        try:
            re.sub(u'ÃƒÂ©', 'ÃƒÂ©', s)
            re.sub(u'ÃƒÂ‰', 'ÃƒÂ‰', s)
            # kill all other unicode chars
            r = re.compile(r'[^\W\d_]', re.U)
            r.sub('', s)
        except:
            pass
        return s

    @staticmethod
    def parse(sHtmlContent, pattern, iMinFoundValue=1, ignoreCase=False):
        aMatches = None
        if sHtmlContent:
            sHtmlContent = cParser.replaceSpecialCharacters(sHtmlContent)
            if ignoreCase:
                aMatches = re.compile(pattern, re.DOTALL | re.I).findall(sHtmlContent)
            else:
                aMatches = re.compile(pattern, re.DOTALL).findall(sHtmlContent)
            if len(aMatches) >= iMinFoundValue:
                return True, aMatches
        return False, aMatches

    @staticmethod
    def replace(pattern, sReplaceString, sValue):
        return re.sub(pattern, sReplaceString, sValue)

    @staticmethod
    def search(sSearch, sValue):
        return re.search(sSearch, sValue, re.IGNORECASE)

    @staticmethod
    def escape(sValue):
        return re.escape(sValue)

    @staticmethod
    def getNumberFromString(sValue):
        pattern = '\\d+'
        aMatches = re.findall(pattern, sValue)
        if len(aMatches) > 0:
            return int(aMatches[0])
        return 0

    @staticmethod
    def urlparse(sUrl):
        return urlparse(sUrl.replace('www.', '')).netloc.title()

    @staticmethod
    def urlDecode(sUrl):
        return unquote(sUrl)

    @staticmethod
    def urlEncode(sUrl, safe=''):
        return quote(sUrl, safe)

    @staticmethod
    def quote(sUrl):
        return quote(sUrl)

    @staticmethod
    def unquotePlus(sUrl):
        return unquote_plus(sUrl)

    @staticmethod
    def quotePlus(sUrl):
        return quote_plus(sUrl)

    @staticmethod
    def B64decode(text):
        import base64
        b = base64.b64decode(text).decode('utf-8')
        return b


# xStream interner Log
class logger:
    @staticmethod
    def info(sInfo):
        logger.__writeLog(sInfo, cLogLevel=xbmc.LOGINFO)

    @staticmethod
    def debug(sInfo):
        logger.__writeLog(sInfo, cLogLevel=xbmc.LOGDEBUG)

    @staticmethod
    def warning(sInfo):
        logger.__writeLog(sInfo, cLogLevel=xbmc.LOGWARNING)

    @staticmethod
    def error(sInfo):
        logger.__writeLog(sInfo, cLogLevel=xbmc.LOGERROR)

    @staticmethod
    def fatal(sInfo):
        logger.__writeLog(sInfo, cLogLevel=xbmc.LOGFATAL)

    @staticmethod
    def __writeLog(sLog, cLogLevel=xbmc.LOGDEBUG):
        params = ParameterHandler()
        try:
            if params.exist('site'):
                site = params.getValue('site')
                sLog = "[%s] -> [%s]: %s" % (common.addonName, site, sLog)
            else:
                sLog = "[%s] %s" % (common.addonName, sLog)
                xbmc.log(sLog, cLogLevel)
        except Exception as e:
            xbmc.log('Logging Failure: %s' % e, cLogLevel)
            pass


class cUtil:
    @staticmethod
    def removeHtmlTags(sValue, sReplace=''):
        p = re.compile(r'<.*?>')
        return p.sub(sReplace, sValue)

    @staticmethod
    def unescape(text): #Todo hier werden Fehler angezeigt
        def fixup(m):
            text = m.group(0)
            if not text.endswith(';'): text += ';'
            if text[:2] == '&#':
                try:
                    if text[:3] == '&#x':
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
                except ValueError:
                    pass
            else:
                try:
                    text = unichr(name2codepoint[text[1:-1]])
                except KeyError:
                    pass
            return text

        if isinstance(text, str):
            try:
                text = text.decode('utf-8')
            except Exception:
                try:
                    text = text.decode('utf-8', 'ignore')
                except Exception:
                    pass
        return re.sub("&(\\w+;|#x?\\d+;?)", fixup, text.strip())

    @staticmethod
    def cleanse_text(text):
        if text is None: text = ''
        text = cUtil.removeHtmlTags(text)
        return text

    @staticmethod
    def evp_decode(cipher_text, passphrase, salt=None):
        if not salt:
            salt = cipher_text[8:16]
            cipher_text = cipher_text[16:]
        key, iv = cUtil.evpKDF(passphrase, salt)
        decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(key, iv))
        plain_text = decrypter.feed(cipher_text)
        plain_text += decrypter.feed()
        return plain_text.decode("utf-8")

    @staticmethod
    def evpKDF(pwd, salt, key_size=32, iv_size=16):
        temp = b''
        fd = temp
        while len(fd) < key_size + iv_size:
            h = hashlib.md5()
            h.update(temp + pwd + salt)
            temp = h.digest()
            fd += temp
        key = fd[0:key_size]
        iv = fd[key_size:key_size + iv_size]
        return key, iv

def valid_email(email): #ToDo: Funktion in Settings / Konten aktivieren
    # Email Muster
    #pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    pattern = r'^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$'

    # \xc3\x9cberpr\xc3\xbcfen der EMail-Adresse mit dem Muster
    if re.match(pattern, email):
        return True
    else:
        return False

class validater():
    return
    import sys
    #if not xbmcaddon.Addon().getSetting('xstream_overs') == 'rincewind':
    # sys.exit()
    if xbmcaddon.Addon().getSetting('xstream_norep') == 'hogwarts':
        sys.exit()
    if xbmcaddon.Addon().getSetting('githubUpdateDevXstream') == 'true':
        if Addon().getSettingString('xstream.dev.username') == '':
            sys.exit()
        elif not Addon().getSettingString('xstream.dev.username') == 'streamxstream':
            sys.exit()
