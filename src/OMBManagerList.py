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

from __future__ import print_function
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Screens.Standby import TryQuitMainloop
from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.ConfigList import ConfigListScreen
from Components.Pixmap import Pixmap
from Components.Sources.List import List
from Components.config import config, ConfigSubsection, ConfigText
from Components.Input import Input
from Screens.InputBox import InputBox
from Components.config import config
from Plugins.Extensions.OpenMultiboot.OMBManagerInstall import OMBManagerInstall, OMB_RM_BIN, BRANDING, BOX_NAME, BOX_MODEL, OMB_GETIMAGEFOLDER, box
from Plugins.Extensions.OpenMultiboot.OMBManagerAbout import OMBManagerAbout
from Plugins.Extensions.OpenMultiboot.OMBManagerCommon import OMB_DATA_DIR, OMB_UPLOAD_DIR
from Components.Label import Label
from Plugins.Extensions.OpenMultiboot.OMBManagerLocale import _
from enigma import eTimer, getDesktop
import os
import fileinput

config.plugins.omb = ConfigSubsection()
config.plugins.omb.alternative_image_folder = ConfigText(default=OMB_GETIMAGEFOLDER, fixed_size=False)

try:
	screenWidth = getDesktop(0).size().width()
except:
	screenWidth = 720


def ismultibootFile():
	multiboot_bin = "/sbin/open_multiboot"
	if not os.path.isfile(multiboot_bin):
		arch = os.popen("uname -m").read()
		if 'mips' in arch:
			MIPS = "/usr/lib/enigma2/python/Plugins/Extensions/OpenMultiboot/bin/mips/open_multiboot"
			if os.path.isfile(MIPS):
				os.chmod(MIPS, 0o755)
				os.system("cp %s /sbin/open_multiboot" % MIPS)
		elif 'armv7l' in arch:
			ARMV71 = "/usr/lib/enigma2/python/Plugins/Extensions/OpenMultiboot/bin/armv7l/open_multiboot"
			if os.path.isfile(ARMV71):
				os.chmod(ARMV71, 0o755)
				os.system("cp %s /sbin/open_multiboot" % ARMV71)
		elif 'sh4' in arch:
			SH4 = "/usr/lib/enigma2/python/Plugins/Extensions/OpenMultiboot/bin/sh4/open_multiboot"
			if os.path.isfile(SH4):
				os.chmod(SH4, 0o755)
				os.system("cp %s /sbin/open_multiboot" % SH4)
		if os.path.isfile(multiboot_bin):
			return True
	else:
		return True
	return False


loadScript = "/usr/lib/enigma2/python/Plugins/Extensions/OpenMultiboot/install-nandsim.sh"


class OMBManagerList(Screen):
	if screenWidth >= 1920:
		skin = """
		<screen position="center,center" size="1000,600">
			<widget name="background" zPosition="1" position="0,0" size="1000,720" alphatest="on" />
			<widget name="label1" zPosition="2" position="10,10" size="940,35" font="Regular;33" foregroundColor="#00999999" halign="center" valign="center" transparent="1" />
			<widget name="label2" zPosition="2" position="10,50" size="940,35" font="Regular;33" halign="center" valign="center" foregroundColor="#00ffc000" transparent="1" />
			<widget name="nextboot" position="10,100" size="940,35" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="#00999999" font="Regular;33" />
			<widget source="list" render="Listbox" position="10,160" itemHeight="35" font="Regular;33" zPosition="3" size="960,315" scrollbarMode="showOnDemand" transparent="1">
				<convert type="StringList" />
			</widget>
			<widget name="key_red" position="0,550" size="230,35" zPosition="5" transparent="1" foregroundColor="white" font="Regular;28" />
			<widget name="key_green" position="240,550" size="230,35" zPosition="5" transparent="1" foregroundColor="white" font="Regular;28" />
			<widget name="key_yellow" position="500,550" size="230,35" zPosition="5" transparent="1" foregroundColor="white" font="Regular;28" />
			<widget name="key_blue" position="750,550" size="230,35" zPosition="5" transparent="1" foregroundColor="white" font="Regular;28" />
			<ePixmap name="red" pixmap="skin_default/buttons/red.png" position="0,540" size="250,60" zPosition="4" transparent="1" alphatest="on" />
			<ePixmap name="green" pixmap="skin_default/buttons/green.png" position="250,540" size="250,60" zPosition="4" transparent="1" alphatest="on" />
			<ePixmap name="yellow" pixmap="skin_default/buttons/yellow.png" position="500,540" size="250,60" zPosition="4" transparent="1" alphatest="on" />
			<ePixmap name="blue" pixmap="skin_default/buttons/blue.png" position="750,540" size="250,60" zPosition="4" transparent="1" alphatest="on" />

			<ePixmap name="info" pixmap="skin_default/buttons/key_info.png" position="920,490" size="50,50" zPosition="4" transparent="1" alphatest="on" />
			<widget name="key_ok" position="0,500" size="900,30" zPosition="5" transparent="1" foregroundColor="#00ffc000" font="Regular;27" />
		</screen>"""
	else:
		skin = """
		<screen position="center,center" size="560,400">
			<widget name="background" zPosition="1" position="0,0" size="560,360" alphatest="on" />
			<widget name="label1" zPosition="2" position="10,10" size="540,25" font="Regular;20" foregroundColor="#00999999" halign="center" valign="center" transparent="1" />
			<widget name="label2" zPosition="2" position="10,40" size="540,25" font="Regular;20" halign="center" valign="center" foregroundColor="#00ffc000" transparent="1" />
			<widget name="nextboot" position="10,70" size="540,20" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="#00999999" font="Regular;20" />
			<widget source="list" render="Listbox" position="10,100" zPosition="3" size="540,260" scrollbarMode="showOnDemand" transparent="1">
				<convert type="StringList" />
			</widget>
			<widget name="key_red" position="0,360" size="140,40" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;17" />
			<widget name="key_green" position="140,360" size="140,40" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;17" />
			<widget name="key_yellow" position="280,360" size="140,40" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;17" />
			<widget name="key_blue" position="420,360" size="140,40" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;17" />
			<ePixmap name="red" pixmap="skin_default/buttons/red.png" position="0,360" size="140,40" zPosition="4" transparent="1" alphatest="on" />
			<ePixmap name="green" pixmap="skin_default/buttons/green.png" position="140,360" size="140,40" zPosition="4" transparent="1" alphatest="on" />
			<ePixmap name="yellow" pixmap="skin_default/buttons/yellow.png" position="280,360" size="140,40" zPosition="4" transparent="1" alphatest="on" />
			<ePixmap name="blue" pixmap="skin_default/buttons/blue.png" position="420,360" size="140,40" zPosition="4" transparent="1" alphatest="on" />
			<ePixmap name="info" pixmap="skin_default/buttons/key_info.png" position="520,340" size="35,25" zPosition="4" transparent="1" alphatest="on" />
			<widget name="key_ok" position="0,340" size="520,20" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="#00ffc000" font="Regular;16" />
		</screen>"""

	def __init__(self, session, mount_point):
		Screen.__init__(self, session)
		self.setTitle(_('openMultiboot Manager') + ": %s" % mount_point)
		self.session = session
		mount_point = mount_point.rstrip("/")
		self.mount_point = mount_point
		self.data_dir = mount_point + '/' + OMB_DATA_DIR
		self.upload_dir = mount_point + '/' + OMB_UPLOAD_DIR
		self.select = None
		self["label1"] = Label(_("Current Running Image:"))
		self["label2"] = Label("")
		self.name = ''
		self["key_ok"] = Button('')
		self["nextboot"] = Button('')
		self.populateImagesList()
		self["list"] = List(self.images_list)
		self["list"].onSelectionChanged.append(self.onSelectionChanged)
		self["background"] = Pixmap()
		self["key_red"] = Button(_('Rename'))
		self["key_yellow"] = Button()
		self["key_blue"] = Button(_('Menu'))
		if BRANDING:
			self["key_green"] = Button(_('Install'))
		else:
			self["key_green"] = Button('')
		self["config_actions"] = ActionMap(["OkCancelActions", "ColorActions", "EPGSelectActions", "MenuActions"],
		{
			"cancel": self.keyCancel,
			"red": self.keyRename,
			"yellow": self.keyDelete,
			"green": self.keyInstall,
			"blue": self.keyExtra,
			"menu": self.keyExtra,
			"info": self.keyAbout,
			"ok": self.KeyOk
		})
		self.setrcType()
		self.checktimer = eTimer()
		self.checktimer.callback.append(self.getMultiboot)
		if self.checkflashImage():
			self.checktimer.start(2000, True)

	def getMultiboot(self):
		if not ismultibootFile():
			self.session.open(MessageBox, _("Warning!\n'/sbin/open_multiboot' not installed!"), MessageBox.TYPE_ERROR)

	def guessImageTitle(self, base_path, identifier):
		image_distro = ""
		image_version = ""
		e2_path = base_path + '/usr/lib/enigma2/python'
		if os.path.exists(e2_path + '/boxbranding.so'):
			helper = os.path.dirname("/usr/bin/python " + os.path.abspath(__file__)) + "/open-multiboot-branding-helper.py"
			try:
				fin, fout = os.popen4(helper + " " + e2_path + " image_distro")
				image_distro = fout.read().strip()
				fin, fout = os.popen4(helper + " " + e2_path + " image_version")
				image_version = fout.read().strip()
			except:
				fout = os.popen(helper + " " + e2_path + " image_distro")
				image_distro = fout.read().strip()
				fout = os.popen(helper + " " + e2_path + " image_version")
				image_version = fout.read().strip()
		if len(image_distro) > 0:
			return image_distro + " " + image_version
		else:
			return identifier

	def imageTitleFromLabel(self, file_entry):
		f = open(self.data_dir + '/' + file_entry)
		label = f.readline().strip()
		f.close()
		return label

	def populateImagesList(self):
		self.images_list = []
		self.images_entries = []
		flashimageLabel = _('Flash image')
		self.name = 'flash'
		next_boot = self.getNextBoot()
		self["label2"].setText(self.currentImage())
		if os.path.exists(self.data_dir + '/.label_flash'):
			flashimageLabel = self.imageTitleFromLabel('.label_flash') + ' (Flash)'
		self.images_entries.append({
			'label': flashimageLabel,
			'identifier': 'flash',
			'path': '/'
		})
		self.images_list.append(self.images_entries[0]['label'])
		if os.path.exists(self.data_dir):
			for file_entry in os.listdir(self.data_dir):
				if not os.path.isdir(self.data_dir + '/' + file_entry):
					continue
				if file_entry[0] == '.':
					continue
				if not self.isCompatible(self.data_dir + '/' + file_entry):
					continue
				if os.path.exists(self.data_dir + '/.label_' + file_entry):
					title = self.imageTitleFromLabel('.label_' + file_entry)
				else:
					title = self.guessImageTitle(self.data_dir + '/' + file_entry, file_entry)
				self.images_entries.append({
					'label': title,
					'identifier': file_entry,
					'path': self.data_dir + '/' + file_entry,
					'labelfile': self.data_dir + '/' + '.label_' + file_entry,
					'kernelbin': self.data_dir + '/' + '.kernels' + '/' + file_entry + '.bin'
				})
				if next_boot:
					if next_boot == file_entry:
						self.name = title
				count = 0
				for d in os.listdir(self.data_dir + '/' + file_entry):
					count += 1
				if not count:
					title = _('(Folder is empty!) ') + title
				elif count < 6:
					title = _('(Unpack error!) ') + title
				elif not os.path.exists(self.data_dir + '/' + file_entry + '/usr/bin/enigma2'):
					title = _('(Unpack error!) ') + title
				else:
					self.checkBackupVerification(self.data_dir + '/' + file_entry)
				self.images_list.append(title)
		if len(self.images_entries) > 1:
			self["key_ok"].setText(_('Press OK to next boot.') + self.checkStatusOMB())
			self["nextboot"].setText(_('Next boot: %s') % self.name)
		else:
			self["key_ok"].setText('')
			self["nextboot"].setText('')

	def refresh(self):
		self.populateImagesList()
		self["list"].setList(self.images_list)

	def getNextBoot(self):
		try:
			f = open(self.data_dir + '/.nextboot')
			boot = f.read()
			f.close()
			return boot
		except:
			pass
		try:
			f = open(self.data_dir + '/.selected')
			boot = f.read()
			f.close()
			return boot
		except:
			pass
		return ""

	def canDeleteEntry(self, entry):
		selected = 'flash'
		try:
			f = open(self.data_dir + '/.selected')
			selected = f.read()
			f.close()
		except:
			pass
		if entry['path'] == '/' or (selected != 'flash' and entry['identifier'] == selected and not self.checkflashImage()):
			return False
		return True

	def currentImage(self):
		selected = 'flash'
		try:
			selected = open(self.data_dir + '/.selected').read()
		except:
			pass
		return selected

	def setrcType(self):
		if self.checkflashImage() and os.path.exists('/proc/stb/ir/rc/type') and os.path.exists('/proc/stb/info/boxtype') and (BOX_NAME != "et8500" and not BOX_NAME.startswith('et7')):
			file_entry = self.data_dir + '/.rctype'
			try:
				if config.plugins.remotecontroltype.rctype.value != 0:
					f = open(file_entry, 'w')
					f.write(str(config.plugins.remotecontroltype.rctype.value))
					f.close()
				elif os.path.exists(file_entry):
					os.system('rm -rf ' + file_entry)
			except:
				pass

	def onSelectionChanged(self):
		if len(self.images_entries) == 0:
			return
		index = self["list"].getIndex()
		if index >= 0 and index < len(self.images_entries):
			entry = self.images_entries[index]
			if self.canDeleteEntry(entry):
				self["key_yellow"].setText(_('Delete'))
			else:
				self["key_yellow"].setText('')

	def KeyOk(self):
		if self.checktimer.isActive():
			return
		if len(self.images_entries) > 1:
			self.select = self["list"].getIndex()
			name = self["list"].getCurrent()
			if name.startswith(_("(Folder")) or name.startswith(_("(Unpack")):
				return
			status = self.checkStatusOMB()
			self.session.openWithCallback(self.confirmNextbootCB, MessageBox, _('Set next boot to %s ?') % name + "\n" + status, MessageBox.TYPE_YESNO)

	def confirmNextbootCB(self, ret):
		if ret:
			image = self.images_entries[self.select]['identifier']
			print("[OMB] set nextboot to %s" % image)
			file_entry = self.data_dir + '/.nextboot'
			f = open(file_entry, 'w')
			f.write(image)
			f.close()
			if not self.session.nav.getRecordings() and self.checkStatusOMB() == _('OMB enabled.'):
				self.session.openWithCallback(self.confirmRebootCB, MessageBox, _('Do you want to reboot now ?'), MessageBox.TYPE_YESNO, default=False)
			else:
				self.refresh()

	def confirmRebootCB(self, ret):
		if ret:
			self.session.open(TryQuitMainloop, 2)
		else:
			self.refresh()

	def checkStatusOMB(self):
		if self.checkflashImage():
			if os.path.isfile('/sbin/open_multiboot'):
				if os.readlink("/sbin/init") == "/sbin/open_multiboot":
					return _('OMB enabled.')
				else:
					return _('OMB disabled.')
			else:
				return _('OMB disabled.')
		else:
			return _('OMB enabled.')
		return ''

	def keyCancel(self):
		self.close()

	def keyAbout(self):
		if self.checktimer.isActive():
			return
		self.session.open(OMBManagerAbout)

	def checkBackupVerification(self, base_path):
		sbin_path = base_path + '/sbin'
		if os.path.exists(sbin_path):
			etc_path = base_path + '/etc'
			if os.path.isfile(sbin_path + '/open_multiboot'):
				os.system('rm -rf ' + sbin_path + '/open_multiboot')
				os.system('rm -rf ' + sbin_path + '/init')
				os.system('ln -s ' + sbin_path + '/init.sysvinit ' + sbin_path + '/init')
			if os.path.isfile(sbin_path + '/open-multiboot-branding-helper.py'):
				os.system('rm -rf ' + sbin_path + '/open-multiboot-branding-helper.py')
			if BOX_NAME and not os.path.exists(etc_path + '/.box_type'):
				box_name = BOX_NAME
				if BOX_MODEL == "vuplus" and BOX_NAME and BOX_NAME[0:2] != "vu":
					box_name = "vu" + BOX_NAME
				os.system("echo %s > %s/.box_type" % (box_name, etc_path))
			if BOX_MODEL and not os.path.exists(etc_path + '/.brand_oem'):
				os.system("echo %s > %s/.brand_oem" % (BOX_MODEL, etc_path))
			os.system('cp /usr/lib/enigma2/python/Plugins/Extensions/OpenMultiboot/open-multiboot-branding-helper.py ' + sbin_path + '/open-multiboot-branding-helper.py')
			if self.checkflashImage():
				if not os.path.exists('/usr/lib/enigma2/python/boxbranding.so') and os.path.exists(base_path + '/usr/lib/enigma2/python/boxbranding.so'):
					if self.isCompatible(base_path):
						os.system("cp " + base_path + "/usr/lib/enigma2/python/boxbranding.so " "/usr/lib/enigma2/python/boxbranding.so")
				if os.path.exists('/usr/lib/enigma2/python/boxbranding.so') and not os.path.exists(base_path + '/usr/lib/enigma2/python/boxbranding.so'):
					if self.isCompatible(base_path):
						os.system("cp /usr/lib/enigma2/python/boxbranding.so " + base_path + "/usr/lib/enigma2/python/boxbranding.so")

	def isCompatible(self, base_path=''):
		box_name = BOX_NAME
		if BOX_MODEL == "vuplus" and BOX_NAME and BOX_NAME[0:2] != "vu":
			box_name = "vu" + BOX_NAME
		if box_name == "et11000":
			box_name = "et1"
		if box_name == "lunix3-4k":
			box_name = "lunix3"
		try:
			archconffile = "%s/etc/opkg/arch.conf" % base_path
			with open(archconffile, "r") as arch:
				for line in arch:
					if box_name in line:
						return True
		except:
			return False
		return False

	def checkflashImage(self):
		if '/omb/open-multiboot' in self.data_dir and os.path.ismount('/usr/lib/enigma2/python/Plugins/Extensions/OpenMultiboot'):
			return False
		return True

	def checkMountFix(self):
		if not os.path.exists('/etc/init.d/volatile-media.sh'):
			return True
		fix = False
		try:
			f = open('/etc/init.d/volatile-media.sh', 'r')
			for line in f.readlines():
				if line.find('mountpoint -q "/media" || mount -t tmpfs -o size=64k tmpfs /media') > -1:
					fix = True
					break
			f.close()
		except:
			pass
		return fix

	def isNextTimeout(self):
		file = self.data_dir + '/.timer'
		if os.path.exists(file):
			try:
				f = open(file)
				timer = f.read()
				f.close()
				next = int(timer)
				if next <= 5 or next > 120:
					os.system('rm -rf ' + file)
				else:
					return next
			except:
				os.system('rm -rf ' + file)
		return 5

	def changeTimeout(self, val):
		if val is not None and val >= 5:
			self.session.openWithCallback(self.inputCallback, InputBox, title=_("Set new timeout (sec)"), text=str(val), maxSize=False, type=Input.NUMBER)

	def inputCallback(self, value):
		if value:
			file = self.data_dir + '/.timer'
			if int(value) < 5 or int(value) > 120:
				self.session.open(MessageBox, _('Incorrect time!'), MessageBox.TYPE_INFO)
			elif int(value) == 5:
				os.system('rm -rf ' + file)
			elif int(value) > 5:
				try:
					f = open(file, 'w')
					f.write(value)
					f.close()
				except:
					self.session.open(MessageBox, _('Error set new timeout!'), MessageBox.TYPE_INFO)

	def keyExtra(self):
		if self.checktimer.isActive():
			return
		text = _("Please select the necessary option...")
		menu = [(_("Readme"), "readme")]
		if self.checkflashImage():
			if BOX_NAME == "hd51" or BOX_NAME == "vs1500" or BOX_NAME == "e4hd" or BOX_NAME == "h7" or BOX_NAME == "gbquad4k" or BOX_NAME == "gbue4k":
				mount_part = os.popen("readlink /dev/root").read()
				if BOX_NAME == "gbquad4k" or BOX_NAME == "gbue4k":
					if 'mmcblk0p5' not in mount_part:
						mount_text = "n/a"
						if 'mmcblk0p7' in mount_text:
							mount_text = "2"
						elif 'mmcblk0p9' in mount_text:
							mount_text = "3"
						self.session.open(MessageBox, _("For this reciever need only first partition muliboot image for use 'openMultiboot'!\nCurrent partition muliboot image - %s") % mount_text, MessageBox.TYPE_INFO)
						return
				else:
					if 'mmcblk0p3' not in mount_part:
						mount_text = "n/a"
						if 'mmcblk0p5' in mount_text:
							mount_text = "2"
						elif 'mmcblk0p7' in mount_text:
							mount_text = "3"
						elif 'mmcblk0p9' in mount_text:
							mount_text = "4"
						self.session.open(MessageBox, _("For this reciever need only first partition muliboot image for use 'openMultiboot'!\nCurrent partition muliboot image - %s") % mount_text, MessageBox.TYPE_INFO)
						return
			if not os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/OpenMultiboot/.autoscan'):
				menu.append((_("Enable autoscan zip archive at mount device"), "enablescan"))
			else:
				menu.append((_("Disable autoscan zip archive at mount device"), "disablescan"))
			if os.path.exists(self.data_dir):
				folder = _("Delete folder %s and all file") % (self.data_dir + '/')
				menu.append((folder, "delete"))
			if os.path.isfile('/sbin/open_multiboot'):
				if os.readlink("/sbin/init") == "/sbin/init.sysvinit":
					menu.append((_("Enable '/sbin/open_multiboot'"), "enable"))
				else:
					menu.append((_("Disable '/sbin/open_multiboot'"), "disable"))
			else:
				menu.append((_("Install '/sbin/open_multiboot'"), "multiboot"))
			if os.path.isfile(self.data_dir + '/.bootmenu.lock'):
				menu.append((_("Enable boot menu"), "bootenable"))
			else:
				menu.append((_("Disable boot menu"), "bootdisable"))
				current_value = self.isNextTimeout()
				name_text = _("Timeout boot menu: next %d sec") % current_value
				menu.append((name_text, "timeout"))
			menu.append((_("Alternative name image folder") + ": %s" % config.plugins.omb.alternative_image_folder.value, "folder"))
		if not self.checkMountFix():
			menu.append((_("Fix mount devices (for PLi)"), "fix_mount"))

		def extraAction(choice):
			if choice:
				if choice[1] == "readme":
					self.session.open(Console, _("Readme"), ["cat /usr/lib/enigma2/python/Plugins/Extensions/OpenMultiboot/readme"])
				elif choice[1] == "bootenable":
					if os.path.isfile(self.data_dir + '/.bootmenu.lock'):
						file_entry = self.data_dir + '/.bootmenu.lock'
						os.system('rm ' + file_entry)
						self.refresh()
				elif choice[1] == "bootdisable":
					if not os.path.isfile(self.data_dir + '/.bootmenu.lock'):
						cmd = "touch " + self.data_dir + '/.bootmenu.lock'
						os.system(cmd)
						self.refresh()
				elif choice[1] == "disable":
					os.system('rm /sbin/init')
					os.system('ln -s /sbin/init.sysvinit /sbin/init')
					os.system('rm -rf /sbin/open-multiboot-branding-helper.py')
					file_entry = self.data_dir + '/.nextboot'
					file_entry1 = self.data_dir + '/.selected'
					os.system('rm ' + file_entry)
					os.system('rm ' + file_entry1)
					self.refresh()
				elif choice[1] == "enable":
					if not self.checkMountFix():
						self.session.open(MessageBox, _("Fix mount devices (for PLi)") + " !", MessageBox.TYPE_INFO)
						return
					if os.path.isfile('/sbin/open_multiboot'):
						os.system('rm /sbin/init')
						os.system('ln -sfn /sbin/open_multiboot /sbin/init')
						os.system('cp /usr/lib/enigma2/python/Plugins/Extensions/OpenMultiboot/open-multiboot-branding-helper.py /sbin/open-multiboot-branding-helper.py')
						self.refresh()
				elif choice[1] == "delete":
					self.session.openWithCallback(self.deleteAnswer, MessageBox, _("Do you want to delete %s?") % (self.data_dir + '/'), MessageBox.TYPE_YESNO)
				elif choice[1] == "fix_mount":
					for line in fileinput.input('/etc/init.d/volatile-media.sh', inplace=True):
						if 'mount -t tmpfs -o size=64k tmpfs /media' in line:
							print("mountpoint -q \"/media\" || mount -t tmpfs -o size=64k tmpfs /media")
						else:
							print(line.rstrip())
					if self.checkMountFix():
						if not self.session.nav.getRecordings() and self.checkStatusOMB() == _('OMB enabled.'):
							self.session.openWithCallback(self.confirmRebootCB, MessageBox, _('Do you want to reboot box now ?'), MessageBox.TYPE_YESNO, default=False)
				elif choice[1] == "enablescan":
					self.setAutoScan(choice[1])
				elif choice[1] == "disablescan":
					self.setAutoScan(choice[1])
				elif choice[1] == "timeout":
					self.changeTimeout(current_value)
				elif choice[1] == "multiboot":
					cmd = "opkg install --force-reinstall openmultiboot"
					text = _("Install")
					self.session.open(Console, text, [cmd])
				elif choice[1] == "folder":
					self.session.openWithCallback(self.renameFolderCallback, VirtualKeyBoard, title=_("Please enter new name:"), text=config.plugins.omb.alternative_image_folder.value)
		dlg = self.session.openWithCallback(extraAction, ChoiceBox, title=text, list=menu)
		dlg.setTitle(_("Open MultiBoot Menu"))

	def renameFolderCallback(self, name):
		if name:
			config.plugins.omb.alternative_image_folder.value = name
			config.plugins.omb.alternative_image_folder.save()
			self.refresh()

	def deleteAnswer(self, answer):
		if answer:
			os.system('rm -rf ' + self.data_dir)
			self.waitmessagebox = self.session.open(MessageBox, _('Please wait 40 seconds, while delete is in progress.'), MessageBox.TYPE_INFO, enable_input=False)
			self.waittimer = eTimer()
			self.waittimer.callback.append(self.deleteFolder)
			self.waittimer.start(40000, True)

	def deleteFolder(self):
		self.waittimer.stop()
		self.waitmessagebox.close()
		self.close()

	def setAutoScan(self, type=''):
		file = '/usr/lib/enigma2/python/Plugins/Extensions/OpenMultiboot/.autoscan'
		if type == "enablescan":
			try:
				open(file, 'wb').close()
			except:
				pass
		else:
			os.system('rm -rf ' + file)

	def keyRename(self):
		if self.checktimer.isActive():
			return
		self.renameIndex = self["list"].getIndex()
		name = self["list"].getCurrent()
		if name.startswith(_("(Folder")) or name.startswith(_("(Unpack")):
			return
		if self["list"].getIndex() == 0:
			if name.endswith('(Flash)'):
				name = name[:-8]
		self.session.openWithCallback(self.renameEntryCallback, VirtualKeyBoard, title=_("Please enter new name:"), text=name)

	def renameEntryCallback(self, name):
		if name:
			renameimage = self.images_entries[self.renameIndex]
			if renameimage['identifier'] == 'flash':
				file_entry = self.data_dir + '/.label_flash'
			else:
				file_entry = self.data_dir + '/.label_' + renameimage['identifier']
			f = open(file_entry, 'w')
			f.write(name)
			f.close()
			self.refresh()

	def deleteConfirm(self, confirmed):
		if confirmed and len(self.entry_to_delete['path']) > 1:
			self.messagebox = self.session.open(MessageBox, _('Please wait while delete is in progress.'), MessageBox.TYPE_INFO, enable_input=False)
			self.timer = eTimer()
			self.timer.callback.append(self.deleteImage)
			self.timer.start(500)

	def deleteImage(self):
		self.timer.stop()
		selected = 'flash'
		try:
			f = open(self.data_dir + '/.selected')
			selected = f.read()
			f.close()
		except:
			pass
		if selected != 'flash' and self.entry_to_delete['identifier'] == selected:
			os.system('rm -rf ' + self.data_dir + '/.selected')
		os.system(OMB_RM_BIN + ' -rf ' + self.entry_to_delete['path'])
		os.system(OMB_RM_BIN + ' -f ' + self.entry_to_delete['kernelbin'])
		os.system(OMB_RM_BIN + ' -f ' + self.entry_to_delete['labelfile'])
		self.messagebox.close()
		self.refresh()

	def keyDelete(self):
		if self.checktimer.isActive():
			return
		if len(self.images_entries) == 0:
			return
		index = self["list"].getIndex()
		if index >= 0 and index < len(self.images_entries):
			self.entry_to_delete = self.images_entries[index]
			if self.canDeleteEntry(self.entry_to_delete):
				self.session.openWithCallback(self.deleteConfirm, MessageBox, _("Do you want to delete %s?") % self.entry_to_delete['label'], MessageBox.TYPE_YESNO)

	def keyInstall(self):
		if self.checktimer.isActive():
			return
		if not BRANDING:
			return
		if not self.checkflashImage():
			return
		upload_list = []
		if os.path.exists(self.upload_dir):
			for file_entry in os.listdir(self.upload_dir):
				if file_entry[0] == '.' or file_entry == 'flash.zip':
					continue
				if len(file_entry) > 4 and file_entry[-4:] == '.zip':
					upload_list.append(file_entry[:-4])

		if len(upload_list) > 0:
			self.session.openWithCallback(self.afterInstall, OMBManagerInstall, self.mount_point, upload_list)
		else:
			self.session.open(MessageBox, _("Please upload an image inside %s") % self.upload_dir, type=MessageBox.TYPE_ERROR)

	def ombImageMountFix(self, file):
		fix = False
		error = False
		try:
			f = open(file, 'r')
			for line in f.readlines():
				if line.find('mountpoint -q "/media" || mount -t tmpfs -o size=64k tmpfs /media') > -1:
					fix = True
					break
			f.close()
		except:
			error = True
		if not fix and not error:
			for line in fileinput.input(file, inplace=True):
				if 'mount -t tmpfs -o size=64k tmpfs /media' in line:
					print("mountpoint -q \"/media\" || mount -t tmpfs -o size=64k tmpfs /media")
				else:
					print(line.rstrip())

	def afterInstall(self, file=None):
		if file is not None:
			mnt = file + '/etc/init.d/volatile-media.sh'
			if os.path.exists(mnt):
				self.ombImageMountFix(mnt)
		self.populateImagesList()
		self["list"].setList(self.images_list)
