all:

install:
	mkdir -p "$(DESTDIR)/usr/sbin"
	cp watchdog.py "$(DESTDIR)/usr/sbin/ff-watchdog"
	cp auto-git-pull.py "$(DESTDIR)/usr/sbin/ff-auto-git-pull"
	mkdir -p "$(DESTDIR)/usr/lib/ff-watchdog"
	cp move_to_segment.sh "$(DESTDIR)/usr/lib/ff-watchdog/"
	mkdir -p "$(DESTDIR)/etc/ffac"
	cp watchdog_config.json "$(DESTDIR)/etc/ffac/"

