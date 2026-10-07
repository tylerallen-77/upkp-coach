.PHONY: test pycheck
pycheck:
	python -m compileall -q api upkp

test: pycheck
	COOKIE_SECURE=0 pytest -q tests
