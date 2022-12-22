Feature: Check web page

  Scenario: Check web page with valid URL and pattern
    Given I have a web page at "http://localhost:8000/path/to/valid-page.html" that should contain the pattern "hello"
    When I check the web page
    Then the HTTP status code should be 200
    And the content pattern should be found

  Scenario: Check web page with invalid URL
    Given I have an invalid web page URL
    When I check the web page
    Then the HTTP status code should not be 200

  Scenario: Check web page with invalid pattern
    Given I have a web page at "http://localhost:8000/path/to/valid-page.html" that should contain the pattern "hallo auf deutsch", but does not
    When I check the web page
    Then the HTTP status code should be 200
    When I check the web page
    Then the content pattern should not be found

  Scenario: Program creates a valid log entry
    Given I have checked a web page at "https://foo.bar" that contains the pattern "baz" and response had status_code: "200" and pattern_found: "true", current time was "2022-12-22 19:29:46" and the response time was "0.12"
    When I check the web page
    Then the log entry should be valid

