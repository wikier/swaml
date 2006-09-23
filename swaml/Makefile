# SWAML Makefile

DESTDIR =

install:
	mkdir -p $(DESTDIR)/etc/swaml

uninstall:
	echo unavailable

test:
	echo SWAML test
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
	rm -f `find . -name "*~"`
	rm -f `find . -name "*.pyc"`
