FROM python:slim
COPY ./requirements.txt /
RUN pip install -r requirements.txt
EXPOSE 5000/tcp
CMD ["/usr/local/bin/gunicorn", "-b", "0.0.0.0:5000", "jimmy:create_app()"]
