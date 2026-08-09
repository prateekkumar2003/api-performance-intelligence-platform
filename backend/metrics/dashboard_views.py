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

        slow_apis = APIMetric.objects.filter(response_time_ms__gt=1000).order_by('-response_time_ms')[:20]

        data = []

        for api in slow_apis:

            data.append({
                "path": api.path,
                "method": api.method,
                "response_time_ms": api.response_time_ms,
                "status_code": api.status_code,
                "created_at": api.created_at,
            })

        return Response(data)

class PerformanceIssuesView(APIView):

    def get(self, request):

        issues = (
            PerformanceIssue.objects
            .select_related("api_metric")
            .order_by("-created_at")[:50]
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

        apis = (
            APIMetric.objects
            .values("path")
            .annotate(
                avg_response=Avg("response_time_ms"),
                total_requests=Count("id")
            )
            .order_by("-avg_response")[:10]
        )

        return Response(apis)


class SlowQueriesView(APIView):

    def get(self, request):

        queries = (
            SQLQueryMetric.objects
            .order_by("-execution_time_ms")[:20]
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
            metrics = metrics.filter(request_id=request_id)

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
            .order_by("-created_at")[:50]
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