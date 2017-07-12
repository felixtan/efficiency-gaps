from django.conf.urls import url
from .views import gaps_vs_year_for_all_states

urlpatterns = [
    url(r'$', gaps_vs_year_for_all_states)
]
