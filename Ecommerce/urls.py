"""Ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from website import views as webviews
from user import views as userviews
from django.conf import settings
from django.conf.urls.static import static
from website.views import ProductDetailView,add_to_cart,remove_from_cart,OrderSummaryView

app_name = 'website'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('a/',webviews.index,name="Website-index"),
    path('',userviews.signup,name="signup"),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('signin/',userviews.signin,name="signin"),
    path('logout/',userviews.logout,name="logout"),
    path('upload/',webviews.upload_prod,name="upload"),
    path('product/<slug>/', ProductDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
