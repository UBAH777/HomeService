PIP := dummyenv/bin/pip
PYTHON3 := dummyenv/bin/python3

clear:
	rm -rf dummyenv

venv:
	python3 -m venv dummyenv

install_reqs:
	${PIP} install -r requirements.txt

run:
	${PYTHON3} manage.py runserver

create_migrations:
	${PYTHON3} manage.py makemigrations

migrations:
	${PYTHON3} manage.py migrate

up_service:
	make clear
	make venv
	make install_reqs
	make migrations
	make run

superuser:
	${PYTHON3} manage.py createsuperuser