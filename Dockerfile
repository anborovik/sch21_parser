FROM python:3.10-slim
WORKDIR /tgbot
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD [ "python3", "./sch21_parser.py"]