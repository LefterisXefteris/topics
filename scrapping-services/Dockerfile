FROM python:3.9-slim


WORKDIR /scrapping-services


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .


CMD ["python", "scraper.py"]