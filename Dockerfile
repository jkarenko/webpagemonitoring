FROM python:3.11-slim

RUN groupadd -r web-monitor && useradd -r -g web-monitor web-monitor
WORKDIR /app
COPY *.py requirements-prod.txt *.toml /app/
RUN chown -R web-monitor:web-monitor /app
RUN chmod -R 755 /app

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade setuptools
RUN pip install --no-cache-dir --upgrade wheel

RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements-prod.txt

USER web-monitor


CMD ["python", "main.py"]
