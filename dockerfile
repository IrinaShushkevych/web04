FROM python:3.10

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

VOLUME /storage/data.json

EXPOSE 3000

ENTRYPOINT ["python"]

CMD ["main.py"]