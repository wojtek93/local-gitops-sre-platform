from fastapi import FastAPI, Response, status
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = FastAPI(title="SRE Demo App", version="1.0.0")

REQUEST_COUNT = Counter(
    "app_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "app_http_request_duration_seconds",
    "HTTP request latency",
    ["endpoint"],
)


@app.get("/health")
def health():
    REQUEST_COUNT.labels("GET", "/health", "200").inc()
    return {"status": "ok"}


@app.get("/ready")
def ready():
    REQUEST_COUNT.labels("GET", "/ready", "200").inc()
    return {"status": "ready"}


@app.get("/version")
def version():
    REQUEST_COUNT.labels("GET", "/version", "200").inc()
    return {"version": "1.0.0"}


@app.get("/error")
def error():
    REQUEST_COUNT.labels("GET", "/error", "500").inc()
    return Response(
        content='{"error":"simulated internal server error"}',
        media_type="application/json",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@app.get("/load")
def load():
    start = time.time()

    total = 0
    for i in range(500000):
        total += i * i

    REQUEST_LATENCY.labels("/load").observe(time.time() - start)
    REQUEST_COUNT.labels("GET", "/load", "200").inc()

    return {"status": "load generated", "result": total}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)