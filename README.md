# python-docker-image-comparison
# python-docker-image-comparison
Build and Compare Lightweight vs Heavyweight Docker Images for a Python Application
# Python Docker Image Comparison: Alpine vs Standard
 
Build the same Python application on two base images, then compare sizes, run both containers, test them and document the results.
 
| Image tag | Base image | Notes |
|---|---|---|
| `python-app:alpine` | `python:3.12-alpine` | Minimal, musl libc |
| `python-app:standard` | `python:3.12` | Debian-based, full toolchain |
 
## Prerequisites
- Docker installed and running (`docker --version`)
- Git and a GitHub account (`git --version`)
- `curl`
 
---
 
## Step 1: Create the GitHub repository
1. On GitHub, click **New repository**, name it `python-docker-image-comparison`, and create it (add no files).
2. Clone it and enter the folder:
   ```bash
   https://github.com/SHARMIgithubrit/python-docker-image-comparison
   cd python-docker-image-comparison
   ```
 
## Step 2: Create the project files
Final structure:
```
python-docker-image-comparison/
├── app.py
├── requirements.txt
├── Dockerfile.alpine
├── Dockerfile.standard
└── README.md
```
 
### 2.1 `app.py`
```python
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import platform
import socket
 
 
class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            response = {
                "status": "healthy",
                "application": "Python Docker Demo",
                "hostname": socket.gethostname(),
                "python_version": platform.python_version(),
                "base_image": os.getenv("BASE_IMAGE", "unknown"),
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Hello from the Python Docker application!")
 
    def log_message(self, format, *args):
        print(f"{self.client_address[0]} - {format % args}", flush=True)
 
 
if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), AppHandler)
    print("Application listening on port 8000", flush=True)
    server.serve_forever()
```
 
### 2.2 `requirements.txt`
```
# No external Python dependencies are required.
```
 
### 2.3 `Dockerfile.alpine`
```dockerfile
FROM python:3.12-alpine
 
ENV BASE_IMAGE=python:3.12-alpine \
    PYTHONUNBUFFERED=1
 
WORKDIR /app
 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
COPY app.py .
 
EXPOSE 8000
 
CMD ["python", "app.py"]
```
 
### 2.4 `Dockerfile.standard`
```dockerfile
FROM python:3.12
 
ENV BASE_IMAGE=python:3.12 \
    PYTHONUNBUFFERED=1
 
WORKDIR /app
 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
COPY app.py .
 
EXPOSE 8000
 
CMD ["python", "app.py"]
```
The two Dockerfiles are identical except for the `FROM` line and the `BASE_IMAGE` value.
 
 
## Step 4: Build both images
```bash
docker build -t app1:v1 -f Dockerfile.alpine.
docker build -t app2:v2 -f Dockerfile.standard .
```
Expected: both builds finish with no errors. Take a screenshot of each.
 
## Step 5: Compare image sizes
```bash
docker images
```
For exact byte counts:
```bash
  docker build -t app1:v1 -f Dockerfile.alpine.--format '{{.Size}}'
  docker build -t app2:v2 -f Dockerfile.standard .--format '{{.Size}}'
```
 
Calculate the reduction:
```
Size reduction (%) = ((Standard size - Alpine size) / Standard size) * 100
                   = ((2390-1808))/2390 *100 =23.351  
```
 
## Step 6: Run the containers
```bash
docker run -d --name Application1 -p 8080:80 app1:v1
docker run -d --name Application2 -p 8081:8000 app2:v2
```
Host ports 8001 and 8002 both map to the app's port 8000 inside each container.
 
## Step 7: Test the application
Alpine container:
```bash
curl http://localhost:8080
curl http://localhost:80
```
Standard container:
```bash
curl http://localhost:8001/
curl http://localhost:8000/health
```
Expected:
- `/` returns `Hello from the Python Docker application!`
- `/health` returns JSON with `status`, `application`, `hostname` (the container ID), `python_version`, and `base_image` (`python:3.12-alpine` or `python:3.12`)
 
You can also open the four URLs in a browser.
 
## Step 8: Verify container status and logs
```bash
docker ps
docker logs containerID
```
Confirm that:
- Both containers show status `Up`
- Each log contains `Application listening on port 8000`
- Each log has request lines for the curl calls you made
 
## Step 9: Clean up
```bash
docker ps - copy the container id
docker stop container_id -stop
docker rm container_id - delete
docker images - list the docker images
docker rmi docker_image_id - delete
 
```
 
## Step 10: Document the results and submit
1. Fill in the Results tables below with your actual output.
2. Commit and push the README:
   ```bash
   git add README.md
   git commit -m "Document image size comparison results"
   git push