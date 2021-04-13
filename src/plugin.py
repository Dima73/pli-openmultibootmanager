#############################################################################
#
# Copyright (C) 2014 Impex-Sat Gmbh & Co.KG
# Written by Sandro Cavazzoni <sandro@skanetwork.com>
# All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#############################################################################
from OMBManagerLocale import _
from Plugins.Plugin import PluginDescriptor
from OMBManager import OMBManager, isMounted
from OMBManagerCommon import OMB_MAIN_DIR, OMB_DATA_DIR, OMB_UPLOAD_DIR
from Components.Harddisk import harddiskmanager
import os
from Tools.BoundFunction import boundFunction
from Screens.MessageBox import MessageBox
from Tools.Notifications import AddPopup
from mimetypes import add_type
add_type("application/zip", ".zip")

class MoveToupload(MessageBox):
	def __init__(self, session, file):
		MessageBox.__init__(self, session, _("Do you really want add %s with image in 'open-multiboot-upload'?") % file, MessageBox.TYPE_YESNO)
		self.skinName = "MessageBox"

def msgAddZipClosed(ret, curfile=None):
	if ret and curfile:
		try:
			found_dir = ''
			data_dir = OMB_MAIN_DIR + '/' + OMB_DATA_DIR
			if os.path.exists(data_dir):
				upload_dir = OMB_MAIN_DIR + '/' + OMB_UPLOAD_DIR
				if os.path.exists(upload_dir):
					found_dir = upload_dir
			else:
				for p in harddiskmanager.getMountedPartitions():
					if p and os.access(p.mountpoint, os.F_OK | os.R_OK) and p.mountpoint != '/':
						data_dir = p.mountpoint + '/' + OMB_DATA_DIR
						if os.path.exists(data_dir) and isMounted(p.mountpoint):
							upload_dir = p.mountpoint + '/' + OMB_UPLOAD_DIR
							if os.path.exists(upload_dir):
								found_dir = upload_dir
								break
			if found_dir:
				ret = os.system("cp %s %s" % (curfile, found_dir))
				if ret == 0:
					txt = _("zip archive was successfully added to '%s' OMB!") % (found_dir)
				else:
					txt = _("Error adding zip archive!")
				AddPopup(txt, type=MessageBox.TYPE_INFO, timeout=10, id="InfoAddZipArchive")
		except:
			pass

def filescanOpen(list, session, **kwargs):
	try:
		file = list[0].path
		if file:
			session.openWithCallback(boundFunction(msgAddZipClosed, curfile=file), MoveToupload, file)
		else:
			session.open(MessageBox, _("Read error current dir, sorry."), MessageBox.TYPE_ERROR)
	except:
		pass

def startFilescan(**kwargs):
	from Components.Scanner import Scanner, ScanPath
	if not os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/OpenMultiboot/.autoscan'):
		return []
	return \
		Scanner(mimetypes=["application/zip"],
			paths_to_scan=[
					ScanPath(path="", with_subdirs=False),
				],
			name="Open Multiboot",
			description=_("Add zip archive with image in 'open-multiboot-upload'"),
			openfnc=filescanOpen,
		)

def Plugins(**kwargs):
	return [PluginDescriptor(name=_("OpenMultiboot"), description=_("Multi boot loader for enigma2 box"), icon='plugin.png', where=[PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_PLUGINMENU],fnc=OMBManager),
			PluginDescriptor(name=_("Open Multiboot"), where=PluginDescriptor.WHERE_FILESCAN, fnc=startFilescan)]
