# SWAML PFC Talk Makefile

DESTDIR =

NAME = swaml

PDFVIEWER = xpdf -fullscreen

all:	$(NAME).pdf

$(NAME).pdf:
	rubber --pdf $(NAME).tex

view:	$(NAME).pdf
	$(PDFVIEWER) $(NAME).pdf

clean:
	rm -f *.aux *.log *.nav *.out *.snm *.toc
	rm -f $(NAME).pdf
	rm -f `find . -name "*.backup"`
	rm -f `find . -name "*~"`


