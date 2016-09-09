#!/bin/sh


case $1 in
	formuler1)
		SRC="https://raw.githubusercontent.com/Dima73/pli-openmultibootmanager/master/nandsim/formuler1/kernel-module-nandsim.ipk"
		DEST=/tmp/kernel-module-nandsim.ipk
		if which curl >/dev/null 2>&1 ; then
			curl -o $DEST $SRC
		else
			echo >&2 "install-nandsim: cannot find curl"
			opkg update && opkg install curl
			if which curl >/dev/null 2>&1 ; then
				curl -o $DEST $SRC
			fi
		fi
		if ! [ -f $DEST ] ; then
			echo >&2 "install-nandsim: download failed"
			exit 1
		else
			opkg install /tmp/kernel-module-nandsim.ipk
		fi
		exit 0
	;;
	formuler3)
		SRC="https://raw.githubusercontent.com/Dima73/pli-openmultibootmanager/master/nandsim/formuler3/kernel-module-nandsim.ipk"
		DEST=/tmp/kernel-module-nandsim.ipk
		if which curl >/dev/null 2>&1 ; then
			curl -o $DEST $SRC
		else
			echo >&2 "install-nandsim: cannot find curl"
			opkg update && opkg install curl
			if which curl >/dev/null 2>&1 ; then
				curl -o $DEST $SRC
			fi
		fi
		if ! [ -f $DEST ] ; then
			echo >&2 "install-nandsim: download failed"
			exit 1
		else
			opkg install /tmp/kernel-module-nandsim.ipk
		fi
		exit 0
	;;
	formuler4)
		SRC="https://raw.githubusercontent.com/Dima73/pli-openmultibootmanager/master/nandsim/formuler4/kernel-module-nandsim.ipk"
		DEST=/tmp/kernel-module-nandsim.ipk
		if which curl >/dev/null 2>&1 ; then
			curl -o $DEST $SRC
		else
			echo >&2 "install-nandsim: cannot find curl"
			opkg update && opkg install curl
			if which curl >/dev/null 2>&1 ; then
				curl -o $DEST $SRC
			fi
		fi
		if ! [ -f $DEST ] ; then
			echo >&2 "install-nandsim: download failed"
			exit 1
		else
			opkg install /tmp/kernel-module-nandsim.ipk
		fi
		exit 0
	;;
	*)
		echo " "
		echo "Options: $0 {formuler1|formuler3|formuler4}"
		echo " "
esac

echo "Done..."

exit 0

