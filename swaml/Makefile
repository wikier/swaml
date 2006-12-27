# SWAML Makefile

NAME=SWAML
DESTDIR =
ZIP=gzip
DOCDIR=doc

install:
	cp setup/swaml $(DESTDIR)/usr/bin/swaml
	chmod 755 $(DESTDIR)/usr/bin/swaml
	cp setup/buxon $(DESTDIR)/usr/bin/buxon
	chmod 755 $(DESTDIR)/usr/bin/buxon
	mkdir -p $(DESTDIR)/usr/local/swaml/
	cp -r __init__.py swaml.py buxon.py foaf.py kml.py configWizard.py classes includes $(DESTDIR)/usr/local/swaml/
	mkdir -p $(DESTDIR)/usr/share/doc/swaml/examples
	cp -r config $(DESTDIR)/usr/share/doc/swaml/examples
	mkdir tmp
	$(ZIP) -9 -c manpages/swaml.1 > tmp/swaml.1.gz
	$(ZIP) -9 -c manpages/buxon.1 > tmp/buxon.1.gz
	mv tmp/swaml.1.gz tmp/buxon.1.gz $(DESTDIR)/usr/share/man/man1/
	rm -r tmp

uninstall:
	rm -f $(DESTDIR)/usr/bin/swaml
	rm -f $(DESTDIR)/usr/bin/buxon
	rm -rf $(DESTDIR)/usr/local/swaml
	rm -rf $(DESTDIR)/usr/share/doc/swaml/examples
	rm -f $(DESTDIR)/usr/share/man/man1/swaml.1.gz
	rm -f $(DESTDIR)/usr/share/man/man1/buxon.1.gz

gendoc:
	rm -rf $(DOCDIR)
	mkdir -p $(DOCDIR)
	epydoc -n $(NAME) -o $(DOCDIR) --html __init__.py swaml.py foaf.py kml.py buxon.py configWizard.py classes/

pubdoc:	gendoc
	scp -r $(DOCDIR)/* $(USER)@shell.berlios.de:/home/groups/swaml/htdocs/$(DOCDIR)/

test:
	echo $(NAME) test
	echo **********\n
	echo be pacient...\n
	mkdir -p test
	echo time test
	echo ---------\n
	time python swaml.py -d /tmp/swaml/ > test/time.txt
	rm -rf /tmp/swaml
	cat test/time.txt

clean:
	rm -rf archive/
	rm -rf $(DOCDIR)
	rm -f `find . -name "*~"`
	rm -f `find . -name "*.pyc"`

