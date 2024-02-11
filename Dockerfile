FROM alpine:3.19

RUN apk add --no-cache python3-dev py3-pip

RUN apk add --no-cache py3-virtualenv

RUN python3 -m venv /venv

ENV PATH="/venv/bin:$PATH"

WORKDIR /app

COPY . /app

#instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

#ejectuar aplicacion
CMD ["python3", "src/run.py"]