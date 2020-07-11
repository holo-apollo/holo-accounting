release: python manage.py migrate --noinput
web: daphne conf.asgi:application --port $PORT --bind 0.0.0.0
