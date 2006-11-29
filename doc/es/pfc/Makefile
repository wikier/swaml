# SWAML PFC Makefile

DESTDIR =

NAME = swaml

PDFVIEWER = evince

IMAGES= images/swaml-owl.png images/sad.png

all:	clean $(NAME).pdf

$(NAME).pdf: $(IMAGES)	
	umbrello --export png --directory images/uml/ uml/swaml.xmi 2> /dev/null
	umbrello --export png --directory images/uml/ uml/swaml-clases.xmi 2> /dev/null
	rubber --pdf $(NAME).tex

%.png:  %.dia
	dia -t png $?

view:	$(NAME).pdf
	$(PDFVIEWER) $(NAME).pdf &

src:
	python2.4 python2text.py ../../swaml/trunk/*.py #output dir?

clean:
	rm -f $(IMAGES)
	rm -f *.aux *.log *.dvi *.toc *.pdf *.bbl *.blg *.lof *.bak *.lot *.out
	rm -f `find . -name "*.backup"`
	rm -f `find . -name "*~"`
	rm -f images/uml/*

