FROM node:latest as frontend
WORKDIR /app
COPY dashboard /app
RUN npm install
RUN npm run build
RUN npm prune --production


FROM python:3.11-slim as backend
RUN groupadd -r web-monitor && useradd -r -g web-monitor web-monitor
WORKDIR /app
COPY *.py requirements-prod.txt *.toml /app/
COPY --from=frontend /app/build /app/build
RUN chown -R web-monitor:web-monitor /app
RUN chmod -R 755 /app
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade setuptools
RUN pip install --no-cache-dir --upgrade wheel
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements-prod.txt
RUN apt update
RUN apt install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt install -y nodejs
RUN npm install -g serve

USER web-monitor
CMD serve -s -l 80 build & uvicorn service:app --host 0.0.0.0 --port 8000