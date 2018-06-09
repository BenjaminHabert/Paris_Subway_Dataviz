pipeline:
	. activate.sh &&\
	python smallstations/pipeline/run_pipeline.py

plot:
	. activate.sh &&\
	python smallstations/pipeline/step_30_make_plot.py

notebook:
	mkdir -m notebooks &&\
	. activate.sh &&\
	jupyter notebook --notebook-dir=notebooks

install: .venv
	. activate.sh &&\
	pip install --upgrade pip &&\
	pip install -r requirements.txt

.venv:
	python3 -m venv .venv
