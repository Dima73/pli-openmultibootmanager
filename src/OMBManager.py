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

from Components.Harddisk import harddiskmanager
from Screens.MessageBox import MessageBox
from Screens.Console import Console
from OMBManagerList import OMBManagerList
from OMBManagerCommon import OMB_MAIN_DIR, OMB_DATA_DIR, OMB_UPLOAD_DIR
from OMBManagerInstall import OMB_GETIMAGEFILESYSTEM, OMB_UNJFFS2_BIN, BOX_MODEL, BOX_NAME, BRANDING, OMB_NFIDUMP_BIN
from OMBManagerLocale import _
from enigma import eTimer
import os

nandsim_alrenative_module = [] #['formuler1', 'formuler3', 'formuler4']
loadScript = "/usr/lib/enigma2/python/Plugins/Extensions/OpenMultiboot/install-nandsim.sh"

class OMBManagerInit:
	def __init__(self, session):
		self.session = session

		message = _("Where do you want to install openMultiboot?")
		disks_list = []
		for p in harddiskmanager.getMountedPartitions():
			if p and os.path.exists(p.mountpoint) and os.access(p.mountpoint, os.F_OK|os.R_OK) and p.device and p.mountpoint != '/' and (p.device[:2] == 'sd' or (p.device.startswith('mmcblk0p') and BOX_NAME not in ('5008', 'et13000', 'et11000',' et1x000', 'duo4k', 'uno4k', 'uno4kse', 'ultimo4k', 'solo4k', 'zero4k', 'hd51', 'hd52', 'dm820', 'dm7080', 'sf4008', 'dm900', 'dm920', 'gbquad4k', 'gbue4k', 'lunix3-4k', 'lunix4k', 'vs1500', 'h7', '8100s', 'e4hd'))) and isMounted(p.mountpoint):
				disks_list.append((p.description + ' (%s)' % p.mountpoint, p))

		if len(disks_list) > 0:
			disks_list.append((_("Cancel"), None))
			self.session.openWithCallback(self.initCallback, MessageBox, message, list=disks_list)
		else:
			self.session.open(MessageBox, _("No suitable devices found"), type = MessageBox.TYPE_ERROR)

	def getFSType(self, device):
		try:
			fin,fout = os.popen4("mount | cut -f 1,5 -d ' '")
			tmp = fout.read().strip()
		except:
			fout = os.popen("mount | cut -f 1,5 -d ' '")
			tmp = fout.read().strip()
		for line in tmp.split('\n'):
			parts = line.split(' ')
			if len(parts) == 2:
				if parts[0] == '/dev/' + device:
					return parts[1]
		return  "none"

	def createDir(self, partition):
		data_dir = partition.mountpoint + '/' + OMB_DATA_DIR
		upload_dir = partition.mountpoint + '/' + OMB_UPLOAD_DIR
		try:
			if not os.path.exists(data_dir):
				os.makedirs(data_dir)
			if not os.path.exists(upload_dir):
				os.makedirs(upload_dir)
		except OSError as exception:
			self.session.open(MessageBox, _("Cannot create data folder"), type = MessageBox.TYPE_ERROR)
			return

#		if os.path.isfile('/sbin/open_multiboot'):
#			os.system("ln -sfn /sbin/open_multiboot /sbin/init")

		self.session.open(OMBManagerList, partition.mountpoint)

	def formatDevice(self, confirmed):
		if confirmed:
			self.messagebox = self.session.open(MessageBox, _('Please wait while format is in progress.'), type = MessageBox.TYPE_INFO, enable_input=False)
			self.timer = eTimer()
			self.timer.callback.append(self.doFormatDevice)
			self.timer.start(100, True)

	def doFormatDevice(self):
		self.timer.stop()
		self.error_message = ''
		if os.system('umount /dev/' + self.response.device) != 0:
			self.error_message = _('Cannot umount the device')
		else:
			if os.system('/sbin/mkfs.ext4 /dev/' + self.response.device) != 0:
				self.error_message = _('Cannot format the device')
			else:
				if os.system('mount /dev/' + self.response.device + ' ' + self.response.mountpoint) != 0:
					self.error_message = _('Cannot remount the device')
		self.messagebox.close()
		self.timer = eTimer()
		self.timer.callback.append(self.afterFormat)
		self.timer.start(100, True)

	def afterFormat(self):
		self.timer.stop()
		if len(self.error_message) > 0:
			self.session.open(MessageBox, self.error_message, type = MessageBox.TYPE_ERROR)
		else:
			self.createDir(self.response)

	def initCallback(self, response):
		if response:
			fs_type = self.getFSType(response.device)
			if fs_type not in ['ext3', 'ext4']:
				self.response = response
				self.session.openWithCallback( self.formatDevice, MessageBox, _("Filesystem not supported\nDo you want format your drive?"), type = MessageBox.TYPE_YESNO, default=False)
			else:
				self.createDir(response)

class OMBManagerKernelModule:
	def __init__(self, session, kernel_module, branding=False):
		self.session = session
		self.kernel_module = kernel_module
		if branding:
			self.timer = eTimer()
			self.timer.callback.append(self.warningMessage)
			self.timer.start(500, True)
			return
		message = _("You need the module ") + self.kernel_module + _(" to use openMultiboot\nDo you want install it?")
		self.session.openWithCallback(self.installCallback, MessageBox, message, MessageBox.TYPE_YESNO)

	def warningMessage(self):
		self.timer.stop()
		self.session.open(MessageBox, _('Not found boxbranding.so!'),type = MessageBox.TYPE_ERROR)

	def installCallback(self, confirmed):
		if confirmed:
			if self.kernel_module != "nfidump":
				self.messagebox = self.session.open(MessageBox,_('Please wait while installation is in progress.'), MessageBox.TYPE_INFO, enable_input = False)
			self.timer = eTimer()
			self.timer.callback.append(self.installModule)
			self.timer.start(100, True)

	def installModule(self):
		self.timer.stop()
		self.error_message = ''
		if self.kernel_module == "nfidump":
			os.system("chmod 755 %s" % loadScript)
			cmd = 'opkg update && opkg install python-subprocess\n'
			cmd += "%s dmm_nfidump" % loadScript
			text = _("Install")
			self.session.openWithCallback(self.afterLoadNfidumpInstall, Console, text, [cmd])
			return
		os.system('opkg update && opkg install python-subprocess')
		if os.system('opkg install ' + self.kernel_module) != 0:
			self.error_message = _('Cannot install ') + self.kernel_module
		self.messagebox.close()
		self.timer = eTimer()
		self.timer.callback.append(self.afterInstall)
		self.timer.start(100, True)

	def afterLoadNfidumpInstall(self):
		if not os.path.exists(OMB_NFIDUMP_BIN):
			self.error_message = _('Cannot install ') + self.kernel_module
			self.session.open(MessageBox, self.error_message, type = MessageBox.TYPE_ERROR)
		else:
			OMBManager(self.session)

	def alterInstallCallback(self, confirmed):
		if confirmed:
			os.system("chmod 755 %s" % loadScript)
			cmd = "%s %s" % (loadScript, BOX_NAME)
			text = _("Install")
			self.session.openWithCallback(self.afterLoadInstall, Console, text, [cmd])

	def afterLoadInstall(self):
		if os.system('opkg list_installed | grep ' + self.kernel_module) != 0:
			self.error_message = _('Cannot install ') + self.kernel_module
			self.session.open(MessageBox, self.error_message, type = MessageBox.TYPE_ERROR)
		else:
			OMBManager(self.session)

	def afterInstall(self):
		self.timer.stop()
		if len(self.error_message) > 0:
			if self.kernel_module == 'kernel-module-nandsim' and nandsim_alrenative_module and BOX_NAME:
				for name in nandsim_alrenative_module:
					if BOX_NAME == name:
						message = _("You want to install an alternative kernel-module-nandsim?\nLinux version may be different from the module!")
						self.session.openWithCallback(self.alterInstallCallback, MessageBox, message, MessageBox.TYPE_YESNO)
						return
			self.session.open(MessageBox, self.error_message, type = MessageBox.TYPE_ERROR)
		else:
			OMBManager(self.session)

def OMBManager(session, **kwargs):
	found = False
	omb_image = os.path.ismount('/usr/lib/enigma2/python/Plugins/Extensions/OpenMultiboot')

	if not omb_image:
		kernel_module = 'kernel-module-nandsim'
		if "jffs2" in OMB_GETIMAGEFILESYSTEM and BOX_MODEL != "dreambox":
			if os.path.exists(OMB_UNJFFS2_BIN):
				kernel_module = None
			else:
				kernel_module = 'kernel-module-block2mtd'

		if "tar.bz2" in OMB_GETIMAGEFILESYSTEM:
			kernel_module = None

		# When use nfidump
		if BOX_MODEL == "dreambox":
			kernel_module = None
			if BOX_NAME == "dm500hd" or BOX_NAME == "dm800" or BOX_NAME == "dm800se" or BOX_NAME == "dm7020hd" or BOX_NAME == "dm7020hdv2" or BOX_NAME == "dm8000" or "dm500hdv2" or BOX_NAME == "dm800sev2":
				if not os.path.exists(OMB_NFIDUMP_BIN):
					OMBManagerKernelModule(session, "nfidump")
					return

		if not BRANDING:
			OMBManagerKernelModule(session, kernel_module, branding=True)

		if kernel_module and os.system('opkg list_installed | grep ' + kernel_module) != 0 and BRANDING:
			OMBManagerKernelModule(session, kernel_module)
			return

	data_dir = OMB_MAIN_DIR + '/' + OMB_DATA_DIR
	if os.path.exists(data_dir):
		session.open(OMBManagerList, OMB_MAIN_DIR)
		found = True
	else:
		for p in harddiskmanager.getMountedPartitions():
			if p and p.device and p.mountpoint != '/' and (p.device[:2] == 'sd' or (p.device.startswith('mmcblk0p') and BOX_NAME not in ('5008', 'et13000', 'et11000',' et1x000', 'uno4k', 'uno4kse', 'ultimo4k', 'solo4k', 'zero4k', 'hd51', 'hd52', 'dm820', 'dm7080', 'sf4008', 'dm900', 'dm920', 'gb7252', 'lunix3-4k', 'vs1500', 'h7', '8100s'))):
				data_dir = p.mountpoint + '/' + OMB_DATA_DIR
				if os.path.exists(data_dir) and os.access(p.mountpoint, os.F_OK|os.R_OK) and isMounted(p.mountpoint):
					#if not os.path.ismount('/usr/lib/enigma2/python/Plugins/Extensions/OpenMultiboot'):
					#	if os.readlink("/sbin/init") == "/sbin/init.sysvinit":
					#		if os.path.isfile('open_multiboot'):
					#			os.system("ln -sfn /sbin/open_multiboot /sbin/init")
					session.open(OMBManagerList, p.mountpoint)
					found = True
					break
	if not found:
		if not omb_image:
			OMBManagerInit(session)

def isMounted(device):
	try:
		for line in open("/proc/mounts"):
			if line.find(device[:-1]) > -1:
				return True
	except:
		pass
	return False
