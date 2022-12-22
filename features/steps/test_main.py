import re

from behave import given, when, then

import main
from main import check_web_page


@given('I have a web page at "{url}" that should contain the pattern "{pattern}"')
def step_impl(context, url, pattern):
    context.url = url
    context.pattern = pattern


@given('I have a web page at "{url}" that should contain the pattern "{pattern}", but does not')
def step_impl(context, url, pattern):
    context.url = url
    context.pattern = pattern
    context.expected_result = (200, False)


@given('I have an invalid web page URL')
def step_impl(context):
    context.url = "http://localhost:8000/path/to/invalidpage.html"
    context.expected_result = (404, "ERROR")
    context.pattern = "this does not matter"


@given(
    'I have checked a web page at "{url}" that contains the pattern "{pattern}" and response had status_code: "{status_code}" and pattern_found: "{pattern_found}", current time was "{timestamp}" and the response time was "{response_time}"')
def step_impl(context, url, pattern, status_code, pattern_found, timestamp, response_time):
    context.log_entry = main.log(timestamp, url,
                                 {"status_code": int(status_code), "pattern_found": pattern_found == "true"},
                                 float(response_time))
    context.timestamp = timestamp
    context.url = url
    context.pattern = pattern
    context.expected_result = "{'status_code': 200, 'pattern_found': True}"
    context.response_time = response_time


@when('I check the web page')
def step_impl(context):
    context.result = check_web_page(context.url, context.pattern)


@then('the HTTP status code should be 200')
def step_impl(context):
    result = context.result["status_code"]
    assert result == 200, f"Expected status code to be 200, but was {result}"


@then('the HTTP status code should not be 200')
def step_impl(context):
    result = context.result["status_code"]
    assert result != 200, f"Expected status code to not be 200, but was {result}"


@then('the content pattern should be found')
def step_impl(context):
    result = context.result["pattern_found"]
    assert result is True, f"Expected True, got {result}"


@then("the content pattern should not be found")
def step_impl(context):
    result = context.result["pattern_found"]
    assert result is False, f"Expected False, got {result}"


@then('the log entry should be valid')
def step_impl(context):
    re_pattern = r'{"timestamp": "\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", "url": "https://[\w\.-]+(/[\w\./-]*)?", "result": {"status_code": \d{3}, "pattern_found": (true|false)}, "response_time": [\d\.]+}'
    assert re.match(re_pattern, context.log_entry), f"Log entry {context.log_entry} did not match pattern: {re_pattern}"
