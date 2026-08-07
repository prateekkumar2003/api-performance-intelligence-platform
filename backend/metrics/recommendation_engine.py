from .models import (
    OptimizationRecommendation
)

def generate_recommendations(api_metric):

    sql_queries = api_metric.sql_queries.all()

    query_count = sql_queries.count()

    if query_count > 10:

        OptimizationRecommendation.objects.create(
            api_metric=api_metric,
            title="High Query Count Detected",
            description=(
                "API executed many database "
                "queries. Consider reducing ORM "
                "calls or batching queries."
            ),
            recommendation_type="query_optimization",
            severity="warning"
        )

    repeated_patterns = {}

    for query in sql_queries:

        normalized = query.query[:100]

        repeated_patterns.setdefault(
            normalized,
            0
        )

        repeated_patterns[normalized] += 1

    for pattern, count in repeated_patterns.items():

        if count >= 5:

            OptimizationRecommendation.objects.create(
                api_metric=api_metric,
                title="Potential N+1 Optimization",
                description=(
                    "Repeated query patterns "
                    "detected. Consider using "
                    "select_related() or "
                    "prefetch_related()."
                ),
                recommendation_type="n_plus_one",
                severity="critical"
            )

            break
    if api_metric.response_time_ms > 1000:

        OptimizationRecommendation.objects.create(
            api_metric=api_metric,
            title="Slow API Optimization",
            description=(
                "API response time is high. "
                "Consider query optimization, "
                "caching, or async processing."
            ),
            recommendation_type="slow_api",
            severity="critical"
        )

    slow_queries = sql_queries.filter(
        execution_time_ms__gt=200
    )

    if slow_queries.exists():

        OptimizationRecommendation.objects.create(
            api_metric=api_metric,
            title="Database Index Recommendation",
            description=(
                "Slow queries detected. "
                "Consider adding indexes "
                "or optimizing filters."
            ),
            recommendation_type="database_index",
            severity="warning"
        )