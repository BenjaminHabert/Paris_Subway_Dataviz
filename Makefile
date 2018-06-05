pipeline:
	. activate.sh &&\
	python smallstations/pipeline/run_pipeline.py

notebook:
	. activate.sh &&\
	jupyter notebook --notebook-dir=notebooks



install: .venv
	. activate.sh &&\
	pip install --upgrade pip &&\
	pip install -r requirements.txt

.venv:
	python3 -m venv .venv
