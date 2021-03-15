FROM python:slim
COPY ./requirements.txt /
RUN pip install -r requirements.txt
CMD ["/usr/local/bin/gunicorn", "-b", "0.0.0.0", "jimmy:create_app()"]
