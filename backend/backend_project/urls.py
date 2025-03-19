"""
URL configuration for backend_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import UploadPDFView
from users.views import UploadPDFViewAll
from users.views import UploadWordView
from users.views import UploadMultiplePDFView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/pdf/upload/', UploadPDFView.as_view(), name='upload_pdf'),
    path('api/pdf/upload/', UploadPDFViewAll.as_view(), name='upload_pdfall'),
    path('api/word/upload/', UploadWordView.as_view(), name='upload_word'),
    path('api/upload-multiple-pdfs/', UploadMultiplePDFView.as_view(), name='upload_multiple_pdfs'),  # 添加新的路由
]

# 添加媒体文件的URL配置
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
