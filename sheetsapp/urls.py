from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [

    # LOGIN
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="login.html"
        ),
        name="login"
    ),

    # LOGOUT
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),

    # DASHBOARD
    path(
        "",
        dashboard,
        name="dashboard"
    ),

    # FULL PIPELINE PAGE
    path(
        "pipeline/",
        pipeline_page,
        name="pipeline"
    ),

    # URGENT OPPORTUNITIES PAGE
    path(
        "urgent/",
        urgent_page,
        name="urgent"
    ),

    # ADD OPPORTUNITY
    path(
        "add/",
        add_pipeline,
        name="add_pipeline"
    ),

    # DELETE OPPORTUNITY
    path(
        "delete/<int:row>/",
        delete_pipeline,
        name="delete_pipeline"
    ),
]