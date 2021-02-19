"""retro_tools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from columns.views import ColumnViewSet
from cards.views import CardViewSet
from boards import views
from django.contrib import admin
from django.urls import include, re_path
from .views import BoardViewSet
from rest_framework_nested import routers

# http://localhost:8000/boards/6/columns/4/cards

router = routers.SimpleRouter(trailing_slash=False)
router.register('boards', BoardViewSet, basename="board")

board_router = routers.NestedSimpleRouter(router, r'boards', lookup='boards')
board_router.register(r'columns', ColumnViewSet, basename='boards-columns')
board_router.register(r'cards', CardViewSet, basename='boards-cards')

urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^', include(board_router.urls)),
]