FROM python:slim
COPY ./requirements.txt /
RUN pip install -r requirements.txt
EXPOSE 8000/tcp
CMD ["/usr/local/bin/gunicorn", "-b", "0.0.0.0", "jimmy:create_app()"]
