# SWAML PFC Makefile

DESTDIR =

NAME = swaml

PDFVIEWER = evince

IMAGES= images/swaml-owl.png

all:	clean $(NAME).pdf

$(NAME).pdf: $(IMAGES)	
	rubber --pdf $(NAME).tex

%.png:  %.dia
	dia -t png $?

view:	$(NAME).pdf
	$(PDFVIEWER) $(NAME).pdf &

src:
	python2.4 python2text.py ../../swaml/trunk/*.py #output dir?

clean:
	rm -f $(IMAGES)
	rm -f *.aux *.log *.dvi *.toc *.pdf *.bbl *.blg *.lof
	rm -f `find . -name "*.backup"`
	rm -f `find . -name "*~"`

