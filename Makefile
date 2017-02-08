all:

install:
	mkdir -p "$(DESTDIR)/usr/lib/ff-watchdog"
	cp watchdog.py "$(DESTDIR)/usr/lib/ff-watchdog/ff-watchdog"
	cp -r parser "$(DESTDIR)/usr/lib/ff-watchdog/"
	cp ff-auto-pull.py "$(DESTDIR)/usr/lib/ff-watchdog/ff-auto-pull"
	cp move_to_segment.sh "$(DESTDIR)/usr/lib/ff-watchdog/"
	mkdir -p "$(DESTDIR)/etc/ffac"
	cp watchdog_config.json "$(DESTDIR)/etc/ffac/"

