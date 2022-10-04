all: paper clean

paper: paper.tex runs/recent/probfig.png
	pdflatex paper
	Biber paper
	pdflatex paper
	pdflatex paper

clean: 
	rm -f *.aux *.blg *.bbl *.log *.bcf *.run.xml




# BELOW THIS LINE ARE COMMANDS TO RESTART AND SETUP DEMO
# THEY WOULD NOT BE PART OF A REAL PROJECT



restartdemo: clean
	rm -rf primesenv
	rm -rf runs
	rm -f paper.pdf
	rm -f probfig.png
	git checkout no_options

makeplot:
	git checkout main
	bash run_experiment.sh log_with_confidence

rundemo: makeplot paper clean
