FROM python:3.11-alpine as builder

ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install -qU pip

WORKDIR /app/
COPY requirements.txt ./
RUN pip install --prefix=/install -r requirements.txt


FROM python:3.11-alpine

WORKDIR /app/
COPY --from=builder /install /usr/local

COPY . .
CMD ["python", "main.py"]
