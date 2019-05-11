FROM python:3.6
COPY . /app
WORKDIR /app
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
# RUN pipenv shell
CMD ["pipenv","run","gunicorn", "-k", "gevent", "-b", "0.0.0.0:5000", "run:app"]