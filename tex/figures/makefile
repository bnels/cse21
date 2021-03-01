DVIFLAGS = --scale=4
# --font-format=woff

default: chaincomplex.png chainmap.png homfunctor.png persistence.png zigzag.png primary_circle.png secondary_circle.png klein_bottle.png persistence_quiver.png zigzag_quiver.png fiber.png Atilde_quiver.png spectral_sequence.png torus_proj.png interleaving.png

%.dvi: %.tex
	latex $<

%.pdf: %.tex
	pdflatex $<

%.png: %.pdf
	convert -density 300 $< -quality 90 $@

%.svg: %.dvi
	dvisvgm $(DVIFLAGS) $<

.PHONY: clean
clean:
	rm -f *.dvi *.aux *.log *.log *.pdf
