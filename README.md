# API Performance Intelligence Platform

## 1. Overview
The **API Performance Intelligence Platform** is a standalone microservice designed to monitor, analyze, and diagnose the performance of APIs across your distributed systems. 

Instead of relying on basic logging, this platform acts as an intelligent sink for telemetry data. It ingests performance metrics from your external applications in real-time, processes them asynchronously, and provides a beautiful, centralized dashboard to help you instantly identify bottlenecks like slow APIs, database N+1 query problems, and overall performance degradation.

---

## 2. Architecture & Technologies Used
The platform is built using a modern, decoupled stack to ensure high throughput and responsiveness:

* **Ingestion Gateway (NGINX)**: Acts as a reverse proxy on Port 80, receiving all incoming telemetry payloads and routing them securely to the backend without blocking.
* **Backend API (Django / Python)**: Provides the REST endpoints for data ingestion (`/ingest/ingest/`) and dashboard data retrieval (`/dashboard/...`).
* **Database (PostgreSQL)**: Stores the raw `APIMetric` and `SQLQueryMetric` data, along with generated `PerformanceIssue`s.
* **Message Broker (Redis)**: Queues incoming analysis tasks so the Django ingestion endpoint can return a `200 OK` instantly without waiting for the heavy calculations to finish.
* **Asynchronous Workers (Celery)**: Picks up tasks from Redis in the background and runs the `recommendation_engine` to analyze the newly ingested metrics for performance flaws.
* **Frontend UI (React / Vite)**: A premium, dark-mode glassmorphism dashboard that pulls aggregated data from the backend to visualize the health of your systems.

---

## 3. How Calculations & Analysis Work
The magic of the platform happens in the background via Celery. When a new API metric is ingested, it triggers the `analyze_metric_task`. This task runs the data through the **Recommendation Engine** (`backend/metrics/recommendation_engine.py`), which uses specific algorithmic thresholds to calculate system health:

### A. Slow API Detection
* **How it calculates:** The engine checks the `response_time_ms` of the incoming request.
* **Threshold:** If the response time is **> 1,000 ms (1 second)**.
* **Action:** It automatically generates a `PerformanceIssue` with a **CRITICAL** severity and recommends adding caching or offloading heavy tasks to a background worker.

### B. N+1 Database Query Problem
* **How it calculates:** The engine looks at the `query_count` (total number of SQL queries executed during that single API request).
* **Threshold:** If the API fires **5 or more queries** during a single request.
* **Action:** It generates a **WARNING** severity issue, indicating a potential N+1 query flaw, and recommends optimizing the ORM calls (e.g., using `select_related` or `prefetch_related` in Django).

### C. Slow Individual SQL Queries
* **How it calculates:** If the ingested payload includes the raw SQL queries and their execution times, the engine iterates through them.
* **Threshold:** If any individual SQL query takes **> 200 ms**.
* **Action:** It generates an `OptimizationRecommendation` targeting that specific query, advising the addition of database indexes or query refactoring.

### D. Dashboard Aggregations
* **Average Response Time**: Calculated on the fly using SQL aggregation (`Avg("response_time_ms")`) across all recorded metrics in `dashboard_views.py`.
* **Top Problematic APIs**: Groups metrics by API `path`, averages their response times, counts their volume, and sorts them descending to highlight the worst offenders.

---

## 4. How to Integrate and Monitor Other Apps
To monitor an external application (like your `phoenix` project), you do not need to install heavy agents. You simply inject a lightweight middleware into the target application that calculates the time and sends a fire-and-forget background HTTP POST request to this platform.

### The Ingestion Payload
The platform expects a JSON payload sent to `http://<platform-ip>/ingest/ingest/`:
```json
{
  "tenant": "my-target-app",
  "path": "/api/users/",
  "method": "GET",
  "status_code": 200,
  "response_time_ms": 145.2,
  "query_count": 2,
  "queries": [
    {"sql": "SELECT * FROM users", "time": 0.052}
  ]
}
```

### Integration: Django Projects (Python)
Drop this middleware into your target project and add it to `MIDDLEWARE` in `settings.py`:

```python
import time
import requests
import threading
from django.db import connection

class APIMonitoringMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ingest_url = "http://<platform-ip>/ingest/ingest/" 

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        response_time_ms = (time.time() - start_time) * 1000

        # Try to get tenant dynamically if using django-tenants
        tenant = request.tenant.schema_name if hasattr(request, "tenant") else "default"

        queries = []
        if hasattr(connection, 'queries'):
            for q in connection.queries:
                try:
                    queries.append({"sql": q.get('sql', ''), "time": float(q.get('time', 0))})
                except (ValueError, TypeError):
                    pass

        payload = {
            "tenant": tenant,
            "path": request.path,
            "method": request.method,
            "status_code": response.status_code,
            "response_time_ms": response_time_ms,
            "query_count": len(queries),
            "queries": queries
        }

        # IMPORTANT: Send asynchronously using a thread so the GIL is released 
        # during the network I/O, ensuring the main API response is never delayed.
        threading.Thread(target=self._send_telemetry, args=(payload,)).start()

        return response

    def _send_telemetry(self, payload):
        try:
            requests.post(self.ingest_url, json=payload, timeout=2)
        except Exception:
            pass # Fails silently to prevent crashing the target app
```

### Integration: Express/Node.js Projects
Drop this middleware into your Node.js application:

```javascript
const axios = require('axios');

const apiMonitorMiddleware = (req, res, next) => {
    const start = Date.now();

    res.on('finish', () => {
        const payload = {
            tenant: "my-node-app",
            path: req.path,
            method: req.method,
            status_code: res.statusCode,
            response_time_ms: Date.now() - start,
            query_count: 0,
            queries: []
        };

        // Fire and forget asynchronous request
        axios.post('http://<platform-ip>/ingest/ingest/', payload).catch(() => {});
    });

    next();
};

app.use(apiMonitorMiddleware);
```
