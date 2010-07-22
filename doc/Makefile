all: article.pdf slides.pdf

article.pdf: article.tex article.aux bib.png
	pdflatex article.tex
	pdflatex article.tex

article.aux: article.bib bib.png
	pdflatex article.tex
	bibtex article

bib.png: bib.dot
	dot -Tpng -o bib.png bib.dot

slides.pdf: slides.tex
	pdflatex slides.tex
	pdflatex slides.tex



bib.pdf: bib.tex bib.aux
	pdflatex bib.tex
	pdflatex bib.tex

bib.aux: article.bib
	pdflatex bib.tex
	bibtex bib



clean:
	@echo "suppression des fichiers de compilation"
	@rm -f *.log *.aux *.dvi *.toc *.lot *.lof *.out *.nav *.snm *.bbl *.blg bib.png

init: clean
	@echo "suppression des fichiers cibles"
	@rm -f *.pdf
