import json
from datetime import datetime
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import main
from config import Config

main.main()
app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc")
app.router = APIRouter(prefix="/api/v1")
origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
config = Config().get_config()


@app.get("/")
def get_sites():
    return config["web_page"]


@app.get("/log")
async def get_main():
    web_pages = config["web_page"]
    for web_page in web_pages:
        # read log entries
        with open(web_page["name"] + ".log", "r", encoding="utf-8") as log_file:
            log_entries = log_file.readlines()[-25:]
        log_entries[:] = [json.loads(log_entry) for log_entry in log_entries]
        web_page["log_entries"] = log_entries
    return web_pages


@app.get("/log/{name}")
async def get_log(name: str):
    with open(f"{name}.log", "r", encoding="utf-8") as log_file:
        log_entries = log_file.readlines()[-25:]
    log_entries[:] = [json.loads(log_entry) for log_entry in log_entries]
    return log_entries


def _get_log(name: str, date_from: str, date_to: str):
    with open(f"{name}.log", "r", encoding="utf-8") as log_file:
        log_entries = log_file.readlines()
    # load entries into individual json objects
    log_entries[:] = [json.loads(log_entry) for log_entry in log_entries]
    # filter by date
    log_entries[:] = [log_entry for log_entry in log_entries if date_from <= log_entry["timestamp"] <= date_to]
    return log_entries


@app.get("/log/{name}/{date_from}/{date_to}")
async def get_log(name: str, date_from: str, date_to: str):
    return _get_log(name, date_from, date_to)


@app.get("/log/{name}/{date_from}")
async def get_log(name: str, date_from: str):
    return _get_log(name, date_from, datetime.now().strftime("%Y-%m-%d" + "T" + "%H:%M:%S"))
