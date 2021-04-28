FROM python:slim
COPY Pipfile* /
RUN pip install pipenv
RUN pipenv install --system
EXPOSE 5000/tcp
CMD ["/usr/local/bin/gunicorn", "-b", "0.0.0.0:5000", "jimmy:create_app()"]
