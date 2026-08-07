from django.db import models

class APIMetric(models.Model):
    tenant = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()

    response_time_ms = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    query_count = models.IntegerField(
        default=0
    )

    def __str__(self):
        return f"{self.method} {self.path}"


class SQLQueryMetric(models.Model):

    api_metric = models.ForeignKey(
        APIMetric,
        on_delete=models.CASCADE,
        related_name="sql_queries"
    )

    query = models.TextField()

    execution_time_ms = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.execution_time_ms} ms"

class DummyData(models.Model):

    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

class PerformanceIssue(models.Model):

    ISSUE_TYPES = (
        ("slow_api", "Slow API"),
        ("slow_query", "Slow Query"),
        ("high_query_count", "High Query Count"),
        ("n_plus_one", "N+1 Query"),
        ("regression", "Performance Regression"),
    )

    api_metric = models.ForeignKey(
        APIMetric,
        on_delete=models.CASCADE,
        related_name="issues"
    )

    issue_type = models.CharField(
        max_length=50,
        choices=ISSUE_TYPES
    )

    message = models.TextField()

    severity = models.CharField(
        max_length=20,
        default="warning"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.issue_type

class OptimizationRecommendation(models.Model):

    api_metric = models.ForeignKey(
        APIMetric,
        on_delete=models.CASCADE,
        related_name="recommendations"
    )

    title = models.CharField(max_length=255)

    description = models.TextField()

    recommendation_type = models.CharField(
        max_length=100
    )

    severity = models.CharField(
        max_length=20,
        default="info"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title