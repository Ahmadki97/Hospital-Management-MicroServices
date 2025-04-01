FROM python:3.12.6

WORKDIR /usr/src/app/

RUN apt update && apt install -y gcc python3-dev musl-dev default-libmysqlclient-dev build-essential


# Prevent python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# ensure python output is sent directly to terminal 
ENV PYTHONUNBUFFERED 1

COPY 4-Appointment_Service/packages.txt .

RUN pip install --upgrade pip

RUN pip install -r packages.txt


WORKDIR /usr/src/app


ENTRYPOINT ["python", "main.py"]

# ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]