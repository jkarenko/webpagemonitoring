from http.client import BadStatusLine
from urllib.request import urlopen
from urllib.error import URLError
import re
import time
import threading
import toml
from logentry import LogEntry


def check_web_page(url, content_pattern):
    # Send an HTTP request to the web page
    try:
        response = urlopen(url)
        if encoding := response.headers.get_content_charset():
            page_content = response.read().decode(encoding)
        else:
            page_content = response.read().decode('utf-8')
        # Check that the url response is ok and the page content matches the content pattern
        status_code = response.getcode()
        pattern_found = re.search(content_pattern, page_content)
        if status_code == 200:
            return {"status_code": status_code, "pattern_found": bool(pattern_found)}
    except (URLError, UnicodeDecodeError, BadStatusLine) as e:
        status_code = 404
    return {"status_code": status_code, "pattern_found": "ERROR"}


def periodic_check(url, content_pattern, interval):
    while True:
        elapsed_time, result, timestamp = request_web_page(content_pattern, url)
        log_message = log(timestamp, url, result, elapsed_time)
        with open("all_sites.log", "a", encoding="utf-8") as log_file:
            log_file.write(log_message + "\n")
        # Wait to start the next check
        time.sleep(interval)


def log(timestamp, url, result, elapsed_time):
    log_entry = LogEntry(timestamp, url, result, elapsed_time)
    return log_entry.to_json()


def request_web_page(content_pattern, url):
    # Measure the time it takes to complete the request
    start_time = time.perf_counter()
    result = check_web_page(url, content_pattern)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    return elapsed_time, result, timestamp


def main():
    # Load the configuration from the TOML file
    with open("config.toml", "r") as f:
        config = toml.load(f)

    # Get the list of web pages and content patterns from the configuration
    web_pages = config["web_page"]

    # Iterate over the web pages and start a separate thread for each one
    for web_page in web_pages:
        url = web_page["url"]
        content_pattern = web_page["content_pattern"]
        interval = web_page.get("interval", 60)  # Use a default interval of 60 seconds if not specified
        print(f"Starting thread for {url}, checking every {interval} seconds for '{content_pattern}'")
        thread = threading.Thread(target=periodic_check, args=(url, content_pattern, interval))
        thread.start()


if __name__ == "__main__":
    main()
