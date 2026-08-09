from django.db.models import Avg, Count
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (
    APIMetric,
    SQLQueryMetric,
    PerformanceIssue
)
from .models import (
    OptimizationRecommendation
)

class SlowAPIsView(APIView):
    def get(self, request):

        slow_apis = APIMetric.objects.filter(response_time_ms__gt=1000).order_by('-response_time_ms')[:100]

        data = []

        for api in slow_apis:

            data.append({
                "path": api.path,
                "method": api.method,
                "response_time_ms": api.response_time_ms,
                "status_code": api.status_code,
                "created_at": api.created_at,
                "request_id": api.request_id,
            })

        return Response(data)

class PerformanceIssuesView(APIView):

    def get(self, request):

        issues = (
            PerformanceIssue.objects
            .select_related("api_metric")
            .order_by("-created_at")[:100]
        )

        data = []

        for issue in issues:

            data.append({
                "issue_type": issue.issue_type,
                "severity": issue.severity,
                "message": issue.message,
                "path": issue.api_metric.path,
                "created_at": issue.created_at,
            })

        return Response(data)


class TopProblematicAPIsView(APIView):

    def get(self, request):

        metrics = APIMetric.objects.all()
        request_id = request.GET.get("request_id")
        
        if request_id:
            import uuid
            try:
                uuid.UUID(request_id)
                metrics = metrics.filter(request_id=request_id)
            except ValueError:
                metrics = metrics.none()

        apis = (
            metrics
            .values("path")
            .annotate(
                avg_response=Avg("response_time_ms"),
                total_requests=Count("id")
            )
            .order_by("-avg_response")[:100]
        )

        return Response(apis)


class SlowQueriesView(APIView):

    def get(self, request):

        queries = (
            SQLQueryMetric.objects
            .order_by("-execution_time_ms")[:100]
        )

        data = []

        for query in queries:

            data.append({
                "query": query.query,
                "execution_time_ms": query.execution_time_ms,
                "created_at": query.created_at,
            })

        return Response(data)

class DashboardSummaryView(APIView):

    def get(self, request):

        metrics = APIMetric.objects.all()

        request_id = request.GET.get("request_id")

        if request_id:
            import uuid
            try:
                uuid.UUID(request_id)
                metrics = metrics.filter(request_id=request_id)
            except ValueError:
                metrics = metrics.none()

        total_requests = metrics.count()

        total_issues = PerformanceIssue.objects.filter(api_metric__in=metrics).count()

        avg_response = (
            metrics.aggregate(
                Avg("response_time_ms")
            )["response_time_ms__avg"]
        )

        return Response({
            "total_requests": total_requests,
            "total_issues": total_issues,
            "average_response_time_ms": avg_response,
        })

class RecommendationsView(APIView):

    def get(self, request):

        recommendations = (
            OptimizationRecommendation.objects
            .select_related("api_metric")
            .order_by("-created_at")[:100]
        )

        data = []

        for recommendation in recommendations:

            data.append({
                "title": recommendation.title,
                "description": (
                    recommendation.description
                ),
                "severity": recommendation.severity,
                "path": (
                    recommendation.api_metric.path
                ),
                "created_at": (
                    recommendation.created_at
                ),
            })

        return Response(data)

class APIEndpointsView(APIView):
    def get(self, request):
        endpoints = (
            APIMetric.objects
            .values("path", "method")
            .distinct()
            .order_by("path", "method")
        )
        return Response(endpoints)


class APIPerformanceView(APIView):
    def get(self, request):
        path = request.GET.get('path')
        method = request.GET.get('method')
        
        if not path or not method:
            return Response({"error": "path and method are required"}, status=400)
            
        metrics = APIMetric.objects.filter(path=path, method=method)
        
        from django.db.models.functions import TruncMinute
        per_minute = (
            metrics.annotate(minute=TruncMinute('created_at'))
            .values('minute')
            .annotate(avg_response_time=Avg('response_time_ms'))
            .order_by('minute')
        )
        
        buckets = {}
        for row in per_minute:
            minute_dt = row['minute']
            if not minute_dt:
                continue
            bucket_minute = minute_dt.replace(minute=(minute_dt.minute // 5) * 5, second=0, microsecond=0)
            
            if bucket_minute not in buckets:
                buckets[bucket_minute] = []
            buckets[bucket_minute].append(row['avg_response_time'])
            
        data = []
        for bucket, times in sorted(buckets.items()):
            data.append({
                "time": bucket.strftime("%H:%M"),
                "avg_response_time": round(sum(times) / len(times), 2)
            })
            
        return Response({
            "api": path,
            "method": method,
            "data": data
        })