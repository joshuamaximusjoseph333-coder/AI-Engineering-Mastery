# Day 15 — FastAPI Fundamentals

## Date

September 4, 2026

---

## Today's Goal

The goal of Day 15 was to introduce the Engineering Workbench to web API development using FastAPI.

Until this point, the project could mainly be accessed through Python execution and the CLI.

Today I built the foundation for a second interface:

```text
Client
   ↓
HTTP
   ↓
FastAPI API
```

The API is intentionally basic today. Connecting it to the real Engineering Workbench analytical service layer will be the next step.

---

## What I Learned

### 1. API Fundamentals

I learned that API stands for:

**Application Programming Interface**

An API provides a defined way for one software system to communicate with another.

For a web API, communication commonly happens using HTTP requests and responses.

Basic model:

```text
Client
   ↓
HTTP Request
   ↓
Server
   ↓
HTTP Response
   ↓
Client
```

---

### 2. CLI vs API

The Engineering Workbench now has two interface concepts:

```text
CLI
→ receives command-line input

API
→ receives HTTP requests
```

Both interfaces should eventually reuse the same service layer instead of implementing duplicate analytical logic.

Target architecture:

```text
        CLI
         │
         ▼
    Service Layer
         ▲
         │
        API
```

---

### 3. HTTP Fundamentals

I learned the basic role of HTTP in client-server communication.

I studied common HTTP methods:

```text
GET
POST
PUT
PATCH
DELETE
```

Day 15 focused primarily on:

```text
GET
```

for retrieving information.

I also learned the difference between:

- HTTP method
- path
- route
- endpoint
- request
- response
- headers
- response body
- status code

---

### 4. HTTP Status Codes

Important status codes encountered or discussed today:

```text
200
→ successful request

404
→ requested route/resource not found

422
→ request input failed validation

500
→ internal server-side error
```

I also learned that an HTTP status code is different from a field inside a JSON response.

For example:

```text
HTTP status:
200 OK
```

is different from:

```json
{
  "status": "ok"
}
```

The first belongs to HTTP.

The second is application-defined response data.

---

## FastAPI

I installed and introduced FastAPI into the Engineering Workbench.

The API module is:

```text
src/engineering_workbench/api.py
```

The FastAPI application is created using:

```python
from fastapi import FastAPI

app = FastAPI()
```

I learned that routes can then be registered on the application.

Example:

```python
@app.get("/health")
def health():
    return {
        "status": "ok",
    }
```

This means:

```text
GET /health
      ↓
FastAPI routing
      ↓
health()
      ↓
JSON response
```

---

## Production Endpoints Created

At the end of Day 15, the actual project API contains:

```text
GET /
GET /health
```

### Root Endpoint

```text
GET /
```

returns:

```json
{
  "message": "Engineering Workbench API"
}
```

### Health Endpoint

```text
GET /health
```

returns:

```json
{
  "status": "ok"
}
```

---

## JSON Responses

I learned that FastAPI can convert returned Python dictionaries into JSON responses.

For example:

```python
return {
    "status": "ok",
}
```

becomes an HTTP response containing JSON data.

---

## Uvicorn

I learned that FastAPI and Uvicorn have different responsibilities.

```text
FastAPI
→ defines the API application and routes

Uvicorn
→ runs/serves the application and accepts network requests
```

I started the API locally using:

```powershell
uvicorn engineering_workbench.api:app --reload
```

I learned how:

```text
engineering_workbench.api:app
```

identifies:

```text
engineering_workbench
→ package

api
→ api.py module

app
→ FastAPI application object
```

I also learned that:

```text
--reload
```

is useful during development because Uvicorn automatically reloads when source code changes.

---

## Localhost and Ports

The API ran locally at:

```text
http://127.0.0.1:8000
```

I learned that:

```text
127.0.0.1
```

refers to the local machine through the loopback interface.

The:

```text
8000
```

is the port used by the server.

---

## Swagger UI

FastAPI automatically generated interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

Using Swagger UI, I could:

- inspect endpoints,
- see parameters,
- send requests,
- inspect status codes,
- inspect response bodies.

This also demonstrated that both a browser and Swagger UI can act as clients of the same API.

---

## Path Parameters

I created temporary learning endpoints to understand how clients can provide values to an API.

A path parameter places a variable value directly inside the URL path.

Example:

```text
/orders/5
```

with a route pattern:

```text
/orders/{order_id}
```

I learned how FastAPI extracts the value and passes it into the Python function.

---

## Type Validation

I experimented with:

```python
order_id: int
```

and learned that FastAPI can use Python type declarations to validate and convert incoming request data.

A valid request such as:

```text
/orders/5
```

can provide an integer value.

An invalid request such as:

```text
/orders/banana
```

cannot satisfy the expected integer type and results in a validation response.

This showed me that Python type hints are especially useful in FastAPI because they can participate in the API contract and runtime validation.

---

## Query Parameters

I learned how query parameters work.

Example:

```text
/search?minimum_price=3000
```

I also learned how default values can make query parameters optional:

```python
minimum_price: int = 0
```

If the client does not provide the value, the default can be used.

---

## Multiple Query Parameters

I experimented with:

```text
/search?minimum_price=3000&limit=5
```

I learned that:

```text
?
```

begins the query string, while:

```text
&
```

separates multiple query parameters.

The practice endpoints used to learn path and query parameters were removed afterward because they were not real Engineering Workbench requirements.

---

## Automated API Testing

I created:

```text
tests/test_api.py
```

and used:

```python
from fastapi.testclient import TestClient
```

to test the API automatically.

The test client was connected to the real application:

```python
client = TestClient(app)
```

I learned that automated API tests can make requests such as:

```python
response = client.get("/health")
```

and inspect:

```python
response.status_code
```

and:

```python
response.json()
```

The tests verify both the HTTP result and the expected response contract.

---

## Dependency Problem Encountered

The first API test run failed during pytest collection.

The important error stated that Starlette's TestClient required:

```text
httpx2
```

The tests had not actually executed yet because the error occurred while importing the testing dependency.

I installed:

```powershell
python -m pip install httpx2
```

and added:

```text
httpx2
```

to:

```text
requirements.txt
```

This reinforced the difference between:

```text
Installing a dependency
→ changes the current environment

Recording a dependency
→ allows the environment to be recreated
```

---

## API Test Result

After resolving the dependency:

```text
2 passed, 1 warning
```

The two API tests verified:

```text
GET /
GET /health
```

---

## Regression Testing

After the API tests passed independently, I ran the entire project test suite.

Before Day 15:

```text
39 tests passed
```

Day 15 added:

```text
2 API tests
```

Final local result:

```text
41 passed, 1 warning
```

This confirmed that adding FastAPI did not break existing Engineering Workbench functionality.

---

## Third-Party Warning

The test suite produced a deprecation warning originating from:

```text
starlette/testclient.py
```

related to an AnyIO `BlockingPortal` alias.

The tests still passed.

I learned that warnings should be examined before reacting to them.

In this case, the warning originated from third-party package code rather than our own application.

---

## Docker Verification

Because Day 15 added new dependencies, I rebuilt the Docker image:

```powershell
docker build -t engineering-workbench .
```

This was necessary because an already-built Docker image does not automatically receive dependency changes made afterward.

I then ran:

```powershell
docker run --rm engineering-workbench python -m pytest
```

Docker result:

```text
41 passed, 1 warning
```

This confirmed that the project and its new API testing dependencies could be reproduced successfully inside Docker.

---

## Running FastAPI Inside Docker

I also ran the API server inside the container.

Command:

```powershell
docker run --rm -p 8000:8000 engineering-workbench uvicorn engineering_workbench.api:app --host 0.0.0.0 --port 8000
```

I learned two important Docker networking concepts from this.

### Port Mapping

```text
-p 8000:8000
```

means:

```text
HOST PORT : CONTAINER PORT
```

For this project:

```text
Windows :8000
     ↓
Docker
     ↓
Container :8000
```

This allows the Windows browser to communicate with Uvicorn running inside the container.

### `0.0.0.0`

Inside Docker, Uvicorn was started with:

```text
--host 0.0.0.0
```

This allows Uvicorn to listen on the container's available network interfaces so Docker-forwarded traffic can reach it.

I learned not to confuse:

```text
127.0.0.1
```

with:

```text
0.0.0.0
```

`127.0.0.1` is a loopback address used to access the local environment.

`0.0.0.0` is commonly used as a server bind address meaning to listen on all available interfaces.

---

## Current Architecture

At the end of Day 15:

```text
Browser / Swagger / TestClient
             │
             │ HTTP
             ▼
          Uvicorn
             │
             ▼
          FastAPI
             │
       ┌─────┴─────┐
       ▼           ▼
    GET /      GET /health
       │           │
       └─────┬─────┘
             ▼
        JSON Response
```

When running through Docker:

```text
Windows Client
      │
      ▼
Host Port 8000
      │
      ▼
Docker Port Mapping
      │
      ▼
Container Port 8000
      │
      ▼
Uvicorn
      │
      ▼
FastAPI
```

---

## Important Engineering Lesson

The API should be an **interface**, not a second implementation of the application.

The future architecture should be:

```text
              CLI
               │
               ▼
        ┌──────────────┐
        │ Service Layer│
        └──────────────┘
               ▲
               │
              API
```

The CLI and API should reuse the same underlying service logic.

This avoids duplicated analytical code and keeps responsibilities separated.

---

## Problems Encountered

### Problem 1 — Missing TestClient Dependency

**Symptom:**

```text
collected 0 items / 1 error
```

Starlette reported that `httpx2` was required.

**Cause:**

The testing dependency required by the installed Starlette TestClient was not present.

**Solution:**

Installed `httpx2` and recorded it in `requirements.txt`.

---

### Problem 2 — Deprecation Warning

**Symptom:**

Tests passed but produced a Starlette/AnyIO deprecation warning.

**Decision:**

No project code was changed because the warning originated from third-party package code and did not cause the test suite to fail.

---

## Final Verification

### API Tests

```text
2 passed
```

### Full Local Test Suite

```text
41 passed, 1 warning
```

### Full Docker Test Suite

```text
41 passed, 1 warning
```

### API Verification

Verified:

```text
GET /
GET /health
GET /docs
```

with the API running through Uvicorn and Docker port mapping.

---

## Day 15 Outcome

Day 15 successfully introduced a web API layer to the Engineering Workbench.

I can now explain at a foundational level:

- what an API is,
- client-server communication,
- HTTP requests and responses,
- GET requests,
- routes and endpoints,
- JSON responses,
- HTTP status codes,
- FastAPI,
- Uvicorn,
- Swagger UI,
- path parameters,
- query parameters,
- FastAPI type validation,
- automated API testing,
- TestClient,
- API regression testing,
- Docker port mapping,
- and the difference between local and container network binding.

The project now has a tested and container-verified FastAPI foundation.

---

## Next — Day 16

Day 16 will move from:

```text
FastAPI
   ↓
simple static endpoints
```

toward:

```text
HTTP Client
    ↓
FastAPI API Layer
    ↓
Engineering Workbench Service Layer
    ↓
Profiler / Statistics / Database / Loader
    ↓
Real Analytical Results
    ↓
JSON Response
```

This will connect the web API to the actual analytical capabilities developed earlier in the project.