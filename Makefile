# make django_startapp name=users
django_startapp:
	python manage.py startapp ${name}
	mv ${name} apps
