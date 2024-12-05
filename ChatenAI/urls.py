"""
URL configuration for PortdexAI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from ChatenAI import views
from ChatenAI import dashboard
from ChatenAI import generator
from ChatenAI import pages

urlpatterns = [
    path('admin/', admin.site.urls),


    path('', views.index, name = 'index'),
    path('dashboard', views.dashboard, name = 'dashboard'),
    path('products', views.product_list, name = 'products'),
    path('developers/', views.freelancers_list, name='developers'),
    path('ai-repositories/', views.ai_repositories, name='ai-repositories'),
    path('ai-developers/', views.ai_developers, name='ai-developers'),

    path('crypto-currencies/', views.all_coins, name='cryptocurrency'),
    path('currencies/<str:coin_slug>/<int:crypto_id>/', views.coin_detail, name='coin_detail'),


    # Dashboard routes
    path('dashboard/appearance', dashboard.appearance, name = 'appearance'),
    path('dashboard/application', dashboard.application, name = 'application'),
    path('dashboard/chat-export', dashboard.chatExport, name = 'chatExport'),
    path('dashboard/help', dashboard.help, name = 'help'),
    path('dashboard/notification', dashboard.notification, name = 'notification'),
    path('dashboard/plans-billing', dashboard.plansBilling, name = 'plansBilling'),
    path('dashboard/profile-details', dashboard.profileDetails, name = 'profileDetails'),
    path('dashboard/release-notes', dashboard.releaseNotes, name = 'releaseNotes'),
    path('dashboard/sessions', dashboard.sessions, name = 'sessions'),

    # Generator routes
    
    # path('generator/text-generator', generator.textGenerator, name='textGenerator'),
    # path('generator/finance-verify', generator.financeverify, name='financeverify'),
    # path('generator/financeverify/', views.text_generator, name='financeverify'),
    # path('generator/text-generator/', views.text_generator, name='textGenerator'),
    # path('send_message/', views.send_message, name='send_message'),
    path('generator/<str:chat_id>/', views.text_generator, name='financeverify'),
    path('generator/<str:chat_id>/', views.text_generator, name='textGenerator'),

    path('send_message/<str:chat_id>/', views.send_message, name='send_message'),
    # In urls.py

    # Pages routes
    path('pages/blog', pages.blog, name='blog'),
    path('pages/blog-details', pages.blogDetails, name='blogDetails'),
    path('pages/contact', pages.contact, name='contact'),
    path('pages/pricing', pages.pricing, name='pricing'),
    path('pages/privacy-policy', pages.privacyPolicy, name='privacyPolicy'),
    path('pages/roadmap', pages.roadmap, name='roadmap'),
    path('pages/signin', pages.signin, name='signin'),
    path('pages/signup', pages.signup, name='signup'),
    path('pages/style-guide', pages.styleGuide, name='styleGuide'),
    path('pages/team', pages.team, name='team'),
    path('pages/terms-policy', pages.termsPolicy, name='termsPolicy'),
    path('pages/utilize', pages.utilize, name='utilize'),

]
