# Buxon Makefile

NAME=SWAML
DESTDIR =
ZIP=gzip

install:
	cp setup/buxon $(DESTDIR)/usr/bin/buxon
	chmod 755 $(DESTDIR)/usr/bin/buxon
	mkdir -p $(DESTDIR)/usr/share/buxon/
	cp -r run.py src $(DESTDIR)/usr/share/buxon/
	mkdir -p $(DESTDIR)/usr/share/buxon/includes/images
	cp includes/images/calendar.xpm $(DESTDIR)/usr/share/buxon/includes/images/
	cp -r includes/ui $(DESTDIR)/usr/share/buxon/includes/
	mkdir -p $(DESTDIR)/usr/share/pixmaps
	cp includes/images/rdf.xpm $(DESTDIR)/usr/share/pixmaps/buxon.xpm
	mkdir tmp
	$(ZIP) -9 -c manpages/buxon.1 > tmp/buxon.1.gz
	mv tmp/buxon.1.gz $(DESTDIR)/usr/share/man/man1/
	rm -r tmp
	cp setup/buxon.desktop $(DESTDIR)/usr/share/applications/

uninstall:
	rm -f $(DESTDIR)/usr/bin/buxon
	rm -rf $(DESTDIR)/usr/share/buxon
	rm -f $(DESTDIR)/usr/shar/pixmaps/buxon.xpm
	rm -f $(DESTDIR)/usr/share/man/man1/buxon.1.gz
	rm -f $(DESTDIR)/usr/share/applications/buxon.desktop

clean:
	rm -rf buxon.cache
	rm -f `find . -name "*~"`
	rm -f `find . -name "*.pyc"`

