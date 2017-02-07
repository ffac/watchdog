all:

install:
	mkdir -p "$(DESTDIR)/usr/sbin"
	cp watchdog.py "$(DESTDIR)/usr/sbin/ff-watchdog"
	cp ff-auto-pull.py "$(DESTDIR)/usr/sbin/ff-auto-pull"
	mkdir -p "$(DESTDIR)/usr/lib/ff-watchdog"
	cp move_to_segment.sh "$(DESTDIR)/usr/lib/ff-watchdog/"
	mkdir -p "$(DESTDIR)/etc/ffac"
	cp watchdog_config.json "$(DESTDIR)/etc/ffac/"
	mkdir -p "$(DESTDIR)/usr/share/ff-watchdog/"
	cp -r parser "$(DESTDIR)/usr/share/ff-watchdog/"

