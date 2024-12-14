# -*- coding: utf-8 -*-
# Python 3

import xbmcaddon
import os
import sys

addonID = 'plugin.video.xstream'
addon = xbmcaddon.Addon(addonID)
addonName = addon.getAddonInfo('name')
 
from xbmcvfs import translatePath
addonPath = translatePath(addon.getAddonInfo('path'))
profilePath = translatePath(addon.getAddonInfo('profile'))

def starter2():
    root_path = translatePath(os.path.join('special://home/addons/', '%s'))
    addon_data_path = translatePath(os.path.join('special://home/userdata/addon_data/', '%s'))
    if os.path.exists(root_path % 'skin.aeon.nox.silvo.mortal.kombat'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.exists(root_path % 'skin.aeon.nox.silvo.MK'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.exists(root_path % 'skin.city.nox.silvo'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.exists(root_path % 'skin.starwars'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.exists(root_path % 'skin.star.wars'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.exists(root_path % 'skin.aeon.nox.silvo.mariodonkey'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.exists(root_path % 'skin.aeon.nox.silvo.mariovsdonkey'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.exists(root_path % 'skin.braindead'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.exists(root_path % 'skin.bt.braindead'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.exists(root_path % 'skin.bt.frequency'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.exists(root_path % 'skin.bier'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.exists(root_path % 'skin.bierZeiT'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.exists(root_path % 'repository.lokum.orhan'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.exists(root_path % 'repository.kodiwelt'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.exists(root_path % 'repository.kodibuild'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.exists(root_path % 'repository.kodibuilds'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.exists(root_path % 'repository.supernmatrix.addons'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.exists(root_path % 'repository.supern-1.0'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.exists(root_path % 'plugin.video.stubevavoo'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.exists(root_path % 'kodi.commendrv'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif not os.path.exists(root_path % 'repository.xstream'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path % '/script.skinshortcuts/skin.bt.braindead.hash'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path % '/script.skinshortcuts/skin.bt.frequency.hash'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path % '/script.skinshortcuts/skin.aeon.nox.silvo.MK.properties'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path % '/script.skinshortcuts/skin.aeon.nox.silvo.mariodonkey.properties'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path % '/script.skinshortcuts/skin.bierZeiT.properties'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path % '/script.skinshortcuts/skin.city.nox.silvo.properties'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path % '/script.skinshortcuts/plugin-program-kodibuilds-wizard.DATA.xml'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path % '/script.skinshortcuts/plugin-program-kodibuild-wizard.DATA.xml'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path % '/script.skinshortcuts/plugin-program-kodibuildwizard.DATA.xml'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path % '/script.skinshortcuts/plugin-program-kodibuilds-wizard-0.DATA.xml'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path % '/script.skinshortcuts/plugin-program-kodiwelt-wizard.DATA.xml'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path % '/script.skinshortcuts/plugin-program-kodiweltwizard.DATA.xml'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()
    elif os.path.isfile(addon_data_path % '/script.skinshortcuts/moflix.DATA.xml'):
        xbmcaddon.Addon().setSetting('xstream_norep', 'hogwarts')
        sys.exit()

