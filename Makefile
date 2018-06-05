.venv:
	python3 -m venv .venv

install: .venv
	. activate.sh &&\
	pip install --upgrade pip &&\
	pip install -r requirements.txt

notebook:
	. activate.sh &&\
	jupyter notebook --notebook-dir=notebooks
