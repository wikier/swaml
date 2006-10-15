# SWAML Makefile

NAME=SWAML
DESTDIR =
DOCDIR=doc

install:
	mkdir -p $(DESTDIR)/etc/swaml

uninstall:
	echo unavailable

gendoc:
	rm -rf $(DOCDIR)
	mkdir -p $(DOCDIR)
	epydoc -n $(NAME) -o $(DOCDIR) --html swaml.py foaf.py kml.py classes/

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
