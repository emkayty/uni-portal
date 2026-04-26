"""
URL configuration for University Portal API
"""
from django.contrib import admin
from django.urls import path

# Import the API routers
from university.api import router as university_router
from academic.api import router as academic_router
from finance.api import router as finance_router
from students.api import router as students_router
from admission.api import router as admission_router
from messaging.api import router as messaging_router
from config_api import api

# Add all routers to the main API
api.add_router("/university", university_router)
api.add_router("/academic", academic_router)
api.add_router("/finance", finance_router)
api.add_router("/students", students_router)
api.add_router("/admission", admission_router)
api.add_router("/messaging", messaging_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api.urls),  # Root goes to API
    path('api/', api.urls),  # /api/ also works
]
