FROM python:3.11-slim

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

# Email settings variables

ENV EMAIL_HOST_USER=your_example@gmail.com
ENV EMAIL_HOST_PASSWORD=your_password


EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]