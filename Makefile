
run:
	python run.py

install:
	pip install -r requirements.txt

shell:
	flask shell

gunicorn:
	gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app

docker:
	docker build -t prothemesru .
	docker run -p 5000:5000 prothemesru

compose:
	docker-compose up --build
