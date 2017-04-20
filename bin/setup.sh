#!/bin/bash
# This Shell Script was forked from https://github.com/zardus/ctf-tools/blob/master/bin/manage-tools
set -eu -o pipefail
# set -x

function usage()
{
	cat <<END
Usage: $(basename $0) [-sv] (list|setup|install|uninstall|bin|search) tool
Where:
    -s      allow running things with sudo (i.e., to install debs)
    -v      verbose mode. print log while installing
    -f      force certain actions (such as installing over an installed tool)
    tool    the name of the tool. if "all", does the action on all tools
Actions:
    setup       set up the environment (adds ctf-tools/bin to your \$PATH in .bashrc)
    list        list all tools (-i: only installed, -u: only uninstalled)
    install     installs a tool
    uninstall   uninstalls a tool
    reinstall   reinstalls a tool
    upgrade     upgrades a tool
    bin         re-links tool binaries into ctf-tools/bin
    search      search description and name of tools
END
}

function tool_log()
{
	echo "$(tput setaf 4 2>/dev/null)TOOLS | $TOOL |$(tput sgr0 2>/dev/null) $@"
}


function detect_distribution()
{
	if which pacman >/dev/null 2>&1; then
		echo "archlinux"
	elif which apt-get >/dev/null 2>&1; then
		if lsb_release -a 2>/dev/null | grep -i ubuntu >/dev/null 2>&1; then
			echo "ubuntu"
		else
			echo "debian"
		fi
	elif which dnf >/dev/null 2>&1; then
		echo "fedora"
	else
		echo ""
	fi
}


function base_build_setup_debian()
{
	PACKAGE_REQS="build-essential libtool g++ gcc texinfo curl wget automake autoconf python python-dev git subversion unzip virtualenvwrapper lsb-release"
	PACKAGE_COUNT=$(echo $PACKAGE_REQS | tr ' ' '\n' | wc -l)
	if [ $(dpkg -l $PACKAGE_REQS | grep "^ii" | wc -l) -ne $PACKAGE_COUNT ]
	then
		if [ "$ALLOW_SUDO" -eq 1 ]; then
			sudo apt-get -y install $PACKAGE_REQS
		else
			TOOL=SETUP tool_log "Please install the following packages: $PACKAGE_REQS"
		fi
	fi

	if ! dpkg --print-foreign-architectures | grep -q i386
	then
		if [ "$ALLOW_SUDO" -eq 1 ]
		then
			sudo dpkg --add-architecture i386
			sudo apt-get update
		else
			TOOL=SETUP tool_log "Certain tools need i386 libraries (enable with 'dpkg --add-architecture i386; apt-get update')."
		fi
	fi
}


function base_build_setup_arch()
{
	PACKAGE_REQS="curl wget python2 python3 git subversion unzip python-virtualenvwrapper"
	if [ "$ALLOW_SUDO" -eq 1 ]; then
		sudo pacman -Syu --noconfirm --needed $PACKAGE_REQS
		sudo pacman -Syu --noconfirm --needed base-devel || true
	else
		TOOL=SETUP tool_log "Please install the following packages: $PACKAGE_REQS"
	fi

	if ! grep "^\[multilib\]$" /etc/pacman.conf >/dev/null; then
		if [ "$ALLOW_SUDO" -eq 1 ]; then
			sudo sh -c 'cat >> /etc/pacman.conf' <<EOF
[multilib]
Include = /etc/pacman.d/mirrorlist
EOF
		else
			TOOL=SETUP tool_log "Certain tools need i386 libraries (enable multilib in /etc/pacman.conf')."
			return
		fi
	fi

	if [ "$ALLOW_SUDO" -eq 1 ] \
		&& grep "^\[multilib\]$" /etc/pacman.conf >/dev/null \
		&& ! sudo pacman -Qk gcc-multilib >/dev/null
	then
		sudo pacman -Syy --noconfirm
		#sudo pacman -Syu --noconfirm multilib-devel
		# unfortunately we cannot do --noconfirm if we might choose to replace
		# a package such as gcc with gcc-multilib, therefore this workaround
		printf "\ny\ny\ny\n" | sudo pacman -Syu multilib-devel
	fi
}


function base_build_setup_fedora()
{
	PACKAGE_REQS="libtool gcc gcc-c++ clang cmake texinfo curl wget automake autoconf python python-devel git subversion unzip python-virtualenvwrapper redhat-rpm-config"
	if [ "$ALLOW_SUDO" -eq 1 ]; then
		sudo dnf -y install $PACKAGE_REQS
	else
		TOOL=SETUP tool_log "Please install the following packages: $PACKAGE_REQS"
	fi

	# TODO: check whether we have to explicitly enable i386 package support
}


function base_build_setup()
{
	case "$1" in
		"ubuntu")
			;&  # fallthrough
		"debian")
			base_build_setup_debian
			;;
		"archlinux")
			base_build_setup_arch
			export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
			;;
		"fedora")
			base_build_setup_fedora
			;;
		*)
			TOOL=SETUP tool_log "Cannot detect or unsupported distribution"
	esac

	## setup PATH for several shells

	echo "export PATH=\"$PWD/bin:\$PATH\"" >> ~/.bashrc

	if [ -e ~/.zshrc ]
	then
		echo "export PATH=\"$PWD/bin:\$PATH\"" >> ~/.zshrc
	fi

	if [ -e ~/.config/fish/config.fish ]; then
		echo "set -x PATH $PWD/bin \$PATH " >> ~/.config/fish/config.fish
	fi

	if [[ ! -e "$PWD/bin/ctf-tools-pip3" ]]; then
		ln -s "$PWD/bin/ctf-tools-pip" "$PWD/bin/ctf-tools-pip3"
	fi

	# create the py2 virtualenv
	"$PWD/bin/ctf-tools-pip" freeze 2>&1 >/dev/null

	# create the py3 virtualenv
	"$PWD/bin/ctf-tools-pip3" freeze 2>&1 >/dev/null
}


if [[ $# -eq 0 ]]; then
	usage
	exit 1
fi

DISTRI=$(detect_distribution)

while [[ $1 == -* ]]
do
	case $1 in
		-s)
			export ALLOW_SUDO=1
			;;
		-f)
			export FORCE=1
			;;
		-v)
			export VERBOSE_OUTPUT=1
			;;
		*)
			usage
			exit
			;;
	esac
	shift
done

[[ -z ${ALLOW_SUDO+x} ]] && export ALLOW_SUDO=0
[[ -z ${FORCE+x} ]] && export FORCE=0
[[ -z ${VERBOSE_OUTPUT+x} ]] && export VERBOSE_OUTPUT=0
export EXPECTFAIL=${EXPECTFAIL:-0}

if [[ $# -ge 1 ]]; then
	ACTION="$1"
fi
if [[ $# -eq 2 ]]; then
	TOOL="$2"
else
	TOOL=""
fi

if [ "$TOOL" == "all" ]
then
	for t in $($0 list)
	do
		$0 $ACTION $t
	done
elif [ -z "$TOOL" -a "$ACTION" != "list" -a "$ACTION" != "setup" ]
then
	usage
	exit
fi

cd $(dirname "${BASH_SOURCE[0]}")/..

case $ACTION in
	setup)

		base_build_setup "$DISTRI"
		;;
	list)
		for t in *
		do
			[ ! -e "$t/install" ] && continue
			echo $t
		done
		;;
	bin)
		cd bin
		if [ -d ../$TOOL/bin ]; then
			ln -sf ../$TOOL/bin/* .
			tool_log "bin symlinks updated"
		fi
		cd ..
		;;
	install)
		cd $TOOL
		if [ "$FORCE" -eq 0 ] && git status --ignored . | egrep -q 'Untracked|Ignored'
		then
			tool_log "appears to already be installed. Uninstall first?"
			exit 0
		fi

		# the first line in all install and uninstall scripts should have the -e flag, otherwise fail
		if [ $(for i in install* uninstall test; do if [ -e "$i" ]; then head -1 "$i"; fi; done | sort | uniq | grep -v '^#!/bin/bash -ex$' | wc -l) -ne 0 ];
		then
			tool_log "not all install/uninstall/test scripts start with '#!/bin/bash -ex', which is a must for accurate testing."
			exit 1
		fi

		tool_log "starting install, logging to $PWD/install.log"
		rm -f install.log

		# first get distri specific dependencies
		if [[ $(find . -name 'install-root*' | wc -l) -ge 1 ]]; then
			INSTALL_ROOT_SCRIPT="./install-root-$DISTRI"
			# use debian install script if we are on ubuntu and no ubuntu
			# specific install script exists
			if [[ "$DISTRI" == "ubuntu" \
				&& ! -x "$INSTALL_ROOT_SCRIPT" \
				&& -x "./install-root-debian" ]]
			then
				INSTALL_ROOT_SCRIPT="./install-root-debian"
			fi
			if [[ -x "$INSTALL_ROOT_SCRIPT" && "$ALLOW_SUDO" -eq 1 ]]; then
				if ! sudo env DISTRI=$DISTRI "$INSTALL_ROOT_SCRIPT" >> install.log 2>&1;
				then
					tool_log "INSTALL FAILED"
					cat install.log >&2
					exit 1
				fi
			else
				tool_log "Warning: make sure build dependencies are installed!"
			fi
		fi

		# execute install script
		set +e
		if [ "$VERBOSE_OUTPUT" -eq 1 ]; then
			DISTRI=$DISTRI ./install 2>&1 | tee -a install.log
		else
			DISTRI=$DISTRI ./install >>install.log 2>&1
		fi
		INSTALL_FAILED=$?
		set -e

		if [ "$INSTALL_FAILED" -eq 0 ]; then
			tool_log "install finished"
		else
			tool_log "INSTALL FAILED"
			cat install.log >&2
			exit 1
		fi

		cd ..
		$0 bin $TOOL
		;;
	uninstall)
		cd $TOOL

		tool_log "starting uninstall, logging to $PWD/uninstall.log"
		[ -x ./uninstall ] && ./uninstall >> uninstall.log 2>&1
		git clean -dffx . >/dev/null 2>&1
		tool_log "uninstall finished"

		cd ..
		;;
	upgrade)
		cd $TOOL
		if [ -x ./upgrade ]
		then
			./upgrade
			tool_log "upgrade complete!"
		else
			tool_log "no upgrade script -- reinstalling"
			$0 uninstall $TOOL
			$0 install $TOOL
		fi
		;;
	reinstall)
		$0 uninstall $TOOL
		$0 install $TOOL
		;;
	search)
		cat README.md | grep "<\!--tool-->" | sed "s/<\!--[^-]*-->//g" | grep -i "$TOOL"
		;;
	test)
		if [ "$FORCE" -eq 0 ] && ! cat README.md | grep "<\!--tool-->" | grep "| \[$TOOL\](" | grep -q -- "--test--"
		then
			tool_log "Tests not enabled."
			if [ "$EXPECTFAIL" -eq "1" ]; then exit 1; fi
		else
			if (
			if ! $0 install $TOOL; then exit 1; fi

			cd $TOOL || exit 1
			if [ -f ./test ]
			then
				tool_log "Running test script."
				if ! ./test
				then
					tool_log "$TOOL test failed!"
					exit 1
				fi
				tool_log "test script succeeded!"
			else
				tool_log "Install succeeded. No test script!"
			fi
			exit 0
			);
			then
				if [ "$EXPECTFAIL" -eq "1" ]; then exit 1; else exit 0; fi
			else
				if [ "$EXPECTFAIL" -eq "1" ]; then exit 0; else exit 1; fi
			fi
		fi
		;;
	*)
		echo "TOOLS | ERROR | unknown action $ACTION"
		;;
esac
