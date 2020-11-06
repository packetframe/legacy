all: clean build

define CONTROL_FILE
Package: delivr-eca
Version: 0.0.1
Depends: bind9, python3
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Nate Sales <nate@natesales.net>
Description: Edge Cache Appliance for delivr.dev
endef

define VARS
$(CONTROL_FILE)
endef
export VARS

build:
	mkdir -p {debian/DEBIAN/,debian/etc/delivr-eca/,debian/var/delivr-eca/,debian/usr/bin/}
	cp eca.py debian/usr/bin/delivr-eca.py
	echo "$$VARS" > debian/DEBIAN/control
	echo "Copyright 2020 Nathan Sales." > debian/DEBIAN/copyright
	dpkg-deb --build debian
	mv debian.deb delivr-eca.deb

clean:
	rm -rf delivr-eca*.deb debian/
