# Builder LaTeX du dossier — compile dossier.tex -> dossier.pdf (pdflatex).
# Le .tex est un artefact versionné ; ce Makefile ne le régénère pas depuis
# le .md (utiliser `python build_tex.py` pour cela).

TEX    = dossier.tex
PDF    = dossier.pdf
ENGINE = pdflatex
FLAGS  = -interaction=nonstopmode -halt-on-error

.PHONY: all clean

all: $(PDF)

# Double passe pour résoudre la table des matières.
$(PDF): $(TEX)
	$(ENGINE) $(FLAGS) $(TEX)
	$(ENGINE) $(FLAGS) $(TEX)

clean:
	rm -f dossier.aux dossier.log dossier.out dossier.toc
