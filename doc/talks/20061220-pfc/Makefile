# SWAML PFC Talk Makefile

DESTDIR =

NAME = swaml

PDFVIEWER = xpdf -fullscreen

all:	$(NAME).pdf

$(NAME).pdf:
	rubber --pdf $(NAME).tex

pages:	$(NAME).pdf
	pdfnup --nup "2x3" --offset ".25cm .25cm" --delta ".25cm .5cm" --frame true --scale 0.9 $(NAME).pdf

view:	$(NAME).pdf
	$(PDFVIEWER) $(NAME).pdf

clean:
	rm -f *.aux *.log *.nav *.out *.snm *.toc *.dvi *.pdf
	rm -f $(NAME).pdf
	rm -f `find . -name "*.backup"`
	rm -f `find . -name "*~"`


