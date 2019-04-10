PYTHON_BIN ?= python

format: isort black

black:
	'$(PYTHON_BIN)' -m black  --target-version py36 --exclude '/(\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|_build|buck-out|build|dist|node_modules|webpack_bundles)/' .

isort:
	'$(PYTHON_BIN)' -m isort -rc api
	'$(PYTHON_BIN)' -m isort -rc contrib
	'$(PYTHON_BIN)' -m isort -rc pipeline
	'$(PYTHON_BIN)' -m isort -rc transcoding
	'$(PYTHON_BIN)' -m isort -rc videofront

venv: requirements
	'$(PYTHON_BIN)' -m pip install -r requirements.txt

requirements: requirements/base.txt requirements/dev.txt

%.txt: %.in
	'$(PYTHON_BIN)' -m piptools compile $<
