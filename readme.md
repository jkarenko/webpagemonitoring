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

### 1.3 AWS
```bash
# TODO
```

## 2. Usage
```bash
python main.py
```

## 4. Testing
```bash
behave
```

## 4. TODO
- [x] Monitoring
- [x] Logging
- [x] Tests
- [x] Docker
- [ ] CI/CD
- [ ] AWS
- [ ] Alerting
- [ ] Dashboard