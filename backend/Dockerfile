FROM python:alpine
WORKDIR /app
RUN apk add --no-cache gcc musl-dev python3-dev
COPY requirements.txt /app
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /app
RUN python configure.py
RUN python manage.py collectstatic --noinput
CMD python manage.py runserver 0.0.0.0:8000 --insecure
# TODO serve static files with nginx and remove --insecure
EXPOSE 8000


