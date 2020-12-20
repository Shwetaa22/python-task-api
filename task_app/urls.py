from django.conf.urls import url
from .views import TaskClass, taskList

urlpatterns = [
    url(r'^(?P<id>\w+)$', TaskClass.as_view()),
    url(r'task-list', taskList)
]