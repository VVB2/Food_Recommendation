FROM --platform=linux/amd64 python:3.9

EXPOSE 5000

RUN apt-get update -y && \
    apt-get upgrade -y

WORKDIR /food_recommendations
RUN pip install --upgrade pip
COPY ./requirements.txt /food_recommendations
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./static /food_recommendations/static
COPY .env /food_recommendations/
COPY ./data /food_recommendations/data
COPY ./connection /food_recommendations/connection
COPY ./main.py /food_recommendations/
COPY ./server.py /food_recommendations/
COPY ./templates /food_recommendations/templates

CMD ["python", "server.py"]