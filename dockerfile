FROM python:3.10.9

COPY . /app

WORKDIR /app

VOLUME /storage/data.json

RUN pip install -r requirements.txt

EXPOSE 3000

ENTRYPOINT ["python"]

CMD ["main.py"]