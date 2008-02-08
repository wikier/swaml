
# A simple paper makefile
# 2007 (c) Sergio Fernandez

DESTDIR =
NAME = swsm2008
PDFVIEWER = evince

all:	compile

compile:	
	rubber --pdf $(NAME).tex

view:	compile
	$(PDFVIEWER) $(NAME).pdf &

clean:
	rm -f *.aux *.log *.dvi *.toc *.pdf *.bbl *.blg *.lof *.bak *.lot *.out
	rm -f `find . -name "*.backup"`
	rm -f `find . -name "*~"`




