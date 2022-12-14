FROM python:3

COPY . /app

WORKDIR /app

VOLUME /storage/data.json

RUN pip install -r requirements.txt

EXPOSE 5001

ENTRYPOINT ["python"]

CMD ["main.py"]