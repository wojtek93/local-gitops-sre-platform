# Incident 01: High HTTP 500 Error Rate

## Summary

The application started returning HTTP 500 responses from the `/error` endpoint.

Prometheus detected the increased error rate and triggered the `HighHttp500ErrorRate` alert.

---

## Impact

Users may experience:

- failed requests
- degraded application availability
- application instability

---

## Detection

The incident is detected by the following Prometheus alert:

```promql
sum(rate(app_http_requests_total{exported_endpoint="/error"}[1m])) > 0
```

Alert name:

```text
HighHttp500ErrorRate
```

Severity:

```text
warning
```

---

## Symptoms

- Increased HTTP 500 error rate
- Grafana panel `HTTP 500 Error Rate` shows a spike
- Prometheus alert changes from `Inactive` to `Pending`, then `Firing`
- Alertmanager receives the alert

---

## Investigation Steps

### 1. Check application pods

```bash
kubectl get pods -n sre-demo
```

### 2. Check application logs

```bash
kubectl logs deployment/sre-demo-app -n sre-demo
```

### 3. Check recent events

```bash
kubectl get events -n sre-demo --sort-by=.lastTimestamp
```

### 4. Check service endpoints

```bash
kubectl get svc -n sre-demo
kubectl get endpoints -n sre-demo
```

### 5. Check application metrics

```bash
curl -H "Host: sre-demo.local" http://localhost:8081/metrics
```

### 6. Verify Prometheus query

```promql
sum(rate(app_http_requests_total{exported_endpoint="/error"}[1m]))
```

---

## Mitigation

### Faulty deployment

Rollback the deployment:

```bash
kubectl rollout undo deployment/sre-demo-app -n sre-demo
```

### Pod instability

Inspect pod details:

```bash
kubectl describe pod <pod-name> -n sre-demo
kubectl logs <pod-name> -n sre-demo
```

### High load

Check scaling and resource usage:

```bash
kubectl get hpa -n sre-demo
kubectl top pods -n sre-demo
```

---

## Verification

Verify application health:

```bash
curl -H "Host: sre-demo.local" http://localhost:8081/health
```

Verify error metric:

```promql
sum(rate(app_http_requests_total{exported_endpoint="/error"}[1m]))
```

Expected value:

```text
0
```

Verify alert status in Prometheus:

```text
Inactive
```

---

## Root Cause Example

This incident was intentionally generated using the `/error` endpoint.

Possible production causes include:

- application bug
- failed dependency
- database timeout
- network issue
- bad deployment
- configuration error
- resource exhaustion

---

## Permanent Fix

Possible long-term improvements:

- improve application error handling
- add integration tests
- introduce canary deployments
- introduce blue-green deployments
- improve dependency health checks
- tune alert thresholds
- improve deployment validation

---

## Related Components

- FastAPI application
- Prometheus
- Grafana
- Alertmanager
- Kubernetes Service
- ServiceMonitor
- PrometheusRule