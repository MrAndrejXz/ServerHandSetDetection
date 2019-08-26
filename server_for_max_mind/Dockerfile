FROM python:3.6-stretch
WORKDIR /usr/src/app
COPY /server ./server
RUN pip install --no-cache-dir -r server/requirements.txt
ENV PYTHONPATH "server/packages/"
CMD python server/main.py
