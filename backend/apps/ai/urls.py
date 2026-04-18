from django.urls import path

from .views import AskQuestionView

app_name = "ai"

urlpatterns = [
    path("ask/", AskQuestionView.as_view(), name="ask"),
]
