from django.urls import path

from .dashboard_views import (
    SlowAPIsView,
    PerformanceIssuesView,
    TopProblematicAPIsView,
    SlowQueriesView,
    DashboardSummaryView,
    RecommendationsView,
    APIEndpointsView,
    APIPerformanceView
)

urlpatterns = [
    path("slow-apis/", SlowAPIsView.as_view()),
    path("issues/", PerformanceIssuesView.as_view()),
    path("top-apis/", TopProblematicAPIsView.as_view()),
    path("slow-queries/", SlowQueriesView.as_view()),
    path("summary/", DashboardSummaryView.as_view()),
    path("recommendations/", RecommendationsView.as_view()),
    path("endpoints/", APIEndpointsView.as_view()),
    path("api-performance/", APIPerformanceView.as_view()),
]