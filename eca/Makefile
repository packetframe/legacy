all: clean build

define CONTROL_FILE
Package: packetframe-eca
Version: 0.0.1
Depends: bind9, python3
Section: utils
Priority: optional
Architecture: amd64
Maintainer: PacketFrame <nate@packetframe.com>
Description: Edge Cache Appliance for the PacketFrame CDN
endef

define VARS
$(CONTROL_FILE)
endef
export VARS

build:
	mkdir -p {debian/DEBIAN/,debian/etc/packetframe-eca/,debian/var/packetframe-eca/,debian/usr/bin/,/etc/systemd/system/}
	cp eca.py debian/usr/bin/packetframe-eca.py
	cp packetframe-eca.service /etc/systemd/system/
	echo "$$VARS" > debian/DEBIAN/control
	echo "Copyright 2020 PacketFrame." > debian/DEBIAN/copyright
	dpkg-deb --build debian
	mv debian.deb packetframe-eca.deb

clean:
	rm -rf packetframe-eca*.deb debian/
