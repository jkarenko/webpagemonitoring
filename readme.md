[![Deploy to ECR](https://github.com/jkarenko/webpagemonitoring/actions/workflows/deploy.yml/badge.svg)](https://github.com/jkarenko/webpagemonitoring/actions/workflows/deploy.yml)

# Webpage Monitor Demo
Naive implementation of a web page monitor.  
Checks webpages every N seconds and logs the result to a file as JSON.

Edit [config.toml](config.toml) to change monitored pages and polling intervals.

## 1. Installation
### 1.1 Local

```bash
git clone git@github.com:jkarenko/webpagemonitoring.git
cd webpagemonitoring
pip install -r requirements.txt
```

### 1.2 Docker
```bash
docker build --rm -t webpage-monitor:latest . && docker run -p 80:80 --name webpage-monitor webpage-monitor:latest 
```

### 1.3 CI/CD
Via GitHub actions.
Pushing to master triggers a two-phase action that first builds and pushes a new docker container to AWS ECR and then deploys the container as a new task to an AWS ECS cluster.

### 1.4 Dashboard
```bash
cd dashboard
npm install
```


## 2. Usage locally
### 2.1 Configuration
Edit [config.toml](config.toml) to change monitored pages and polling intervals.

### 2.2 Run
#### 2.2.1 Start HTTP server
```bash
uvicorn service:app --reload
```
This starts a local HTTP server on port 8000.
The main program runs in an infinite loop started by service.py that launches a dedicated thread for each web page defined in the config file. Each thread sends a request every N seconds as defined in the [config](config.toml) file. If a pattern is defined in the config file, the program will try to match it to the response to determine if the polled service is up.

#### 2.2.2 Start dashboard
```bash
cd dashboard
npm start
```
This starts a local HTTP server on port 3000.
The dashboard is a simple React app that displays the results of each web page monitored as a graph. The graph is updated every 30 seconds by polling the HTTP server. Consider implementing a websocket connection to the backend HTTP server to avoid polling.

#### 2.2.4 API endpoints
The backend HTTP server exposes the following endpoints:
- GET /api/v1/ - returns a list of all monitored web pages
- GET /api/v1/log - returns an excerpt of all log files as JSON
- GET /api/v1/log/{webpage} - returns an excerpt of the log file for a specific web page as JSON
- GET /api/v1/log/{webpage}/{datetime} - returns all from the log file since {datetime} for a specific web page as JSON
- GET /api/v1/log/{webpage}/{datetime1}/{datetime2} - returns all from the log file since {datetime1} to {datetime2} for a specific web page as JSON
  - example: http://localhost:8000/api/v1/log/my%20homepage/2022-12-27%2017:55/2022-12-27%2017:59

## 3. Testing locally
Tests are written using [Behave](https://github.com/behave/behave) and everything relating to them is in [features](features) directory.
Behave provides function definitions in a natural language style and helps keep tests readable.
Run the tests with the command:
```bash
behave
```
The test suite starts a HTTP server to mock needed responses.


## 4. TODO
- [x] Monitoring
- [x] Logging
- [x] Tests
- [x] Docker
- [x] CI/CD
- [x] AWS
- [ ] Alerting
- [x] Dashboard

## 5. Scaling, security and other concerns
- Multiple agents could be deployed to different regions to report back to a central server.  
- The central server collects the reports, stores the data in a database and generates reports.
- Agents might use REST APIs or secure message queues (AWS SQS) to communicate to the central server
- The ELK stack could be a good solution for ingesting, transforming, storing, searching, analysing and visualising the data.
- All traffic from agents should use E2E encryption.
- Agents should be authenticated before allowing them to send data to the central server. API-key, token or OAuth.
- The central server may be subject to heavy traffic due to multiple agents sending data constantly. Consider using a load balancer and an auto scaling group to keep high availability.

## 6. Demo
A demo might be running at http://ec2-13-53-71-166.eu-north-1.compute.amazonaws.com/