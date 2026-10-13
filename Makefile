PY ?= python

doctor:
	$(PY) -m museforge.cli doctor

test:
	$(PY) -m unittest discover -s tests -t .

bench:
	$(PY) -m museforge.cli bench

serve:
	$(PY) -m museforge.cli serve

.PHONY: doctor test bench serve
