FROM python:3.6
COPY . /app
WORKDIR /app
RUN pip install pipenv
RUN pipenv install --system --deploy
CMD ["pipenv","run","gunicorn", "-k", "gevent", "-w", "3", "--timeout", "300", "-b", "0.0.0.0:5000", "run:app"]