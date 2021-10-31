all: paper clean

paper: paper.tex runs/recent/probfig.png
	pdflatex paper
	Biber paper
	pdflatex paper
	pdflatex paper

clean: 
	rm -f *.aux *.blg *.bbl *.log *.bcf

