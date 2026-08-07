from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (
    APIMetric,
    SQLQueryMetric
)

from .tasks import analyze_metric_task

class TelemetryIngestAPIView(APIView):

    def post(self, request):

        api_metric = APIMetric.objects.create(
            tenant=request.data["tenant"],
            path=request.data["path"],
            method=request.data["method"],
            status_code=request.data[
                "status_code"
            ],
            response_time_ms=request.data[
                "response_time_ms"
            ],
            query_count=request.data[
                "query_count"
            ],
        )

        queries = request.data.get(
            "queries",
            []
        )

        for query in queries:

            SQLQueryMetric.objects.create(
                api_metric=api_metric,
                query=query["sql"],
                execution_time_ms=float(
                    query["time"]
                ) * 1000
            )

        analyze_metric_task.delay(
            api_metric.id
        )

        return Response({"status": "ok"})