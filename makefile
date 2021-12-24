web:
	python manage.py runserver 127.0.0.1:8000

tcp:
	python tcpServer.py

gunicorn:
	gunicorn -c conf/gunicorn.conf djangoProject.wsgi
