from django.urls import path
from . import views

urlpatterns = [
    path('api/save-entity/', views.SaveEntityView.as_view(), name='save-entity'),
    # path('api/get-entity/', GetEntityView.as_view(), name='get-entity'),
]
