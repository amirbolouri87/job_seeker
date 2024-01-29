from django.urls import path
from collect_data.views import TranslateEnglishText, IsEnglishTextView

urlpatterns = [
    path('translate-english-text', TranslateEnglishText.as_view(), name='translate-english-text'),
    path('is-english-text', IsEnglishTextView.as_view(), name='is-english-text'),
]