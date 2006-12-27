# Buxon Makefile

NAME=SWAML
DESTDIR =
ZIP=gzip

install:
	cp setup/buxon $(DESTDIR)/usr/bin/buxon
	chmod 755 $(DESTDIR)/usr/bin/buxon
	mkdir -p $(DESTDIR)/usr/share/buxon/
	cp -r buxon.py includes $(DESTDIR)/usr/share/buxon/
	mkdir tmp
	$(ZIP) -9 -c manpages/buxon.1 > tmp/buxon.1.gz
	mv tmp/buxon.1.gz $(DESTDIR)/usr/share/man/man1/
	rm -r tmp

uninstall:
	rm -f $(DESTDIR)/usr/bin/buxon
	rm -rf $(DESTDIR)/usr/share/buxon
	rm -f $(DESTDIR)/usr/share/man/man1/buxon.1.gz

clean:
	rm -rf buxon.cache
	rm -f `find . -name "*~"`
	rm -f `find . -name "*.pyc"`

