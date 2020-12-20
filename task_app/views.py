from django.core.cache import cache
from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TaskSerializer
from .models import Tasks


class TaskClass(APIView):
    def get(self, request, id=''):
        try:
            task = Tasks.objects.get(id=id)
            task_serializer = TaskSerializer(task)

            return Response({'code': '200', 'message': "Data updated successfully ", 'data': task_serializer.data}, status=status.HTTP_200_OK)
        except Tasks.DoesNotExist:
            return Response({'code': '404', 'message': "Data not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"code": 500, "message": "something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, id=''):
        data = request.data
        transaction.set_autocommit(False)
        try:
            print(data)
            task_serializer = TaskSerializer(data=data)
            if task_serializer.is_valid():
                task_serializer.save()
                transaction.commit()
                task_data = task_serializer.data

            else:
                transaction.rollback()
                print(task_serializer.errors)
                return Response({'code': '400', 'message': task_serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)

            transaction.commit()
            return Response({'code': '200', 'message': "Data added successfully ",'data':task_data }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"code": 500, "message": "something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            transaction.set_autocommit(True)

    def put(self, request, id=''):
        if (not id):
            return Response({'code': '400', 'message': "Invalid inputs"}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        transaction.set_autocommit(False)
        try:
            task = Tasks.objects.get(id=id)
            task_serializer = TaskSerializer(task, data=data)
            if task_serializer.is_valid():
                task_serializer.save()
                transaction.commit()
                task_data = task_serializer.data

            else:
                transaction.rollback()
                print(task_serializer.errors)
                return Response({'code': '400', 'message': task_serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)

            transaction.commit()
            self.get(request, id)
            return Response({'code': '200', 'message': "Data updated successfully ", 'data':task_data}, status=status.HTTP_200_OK)
        except Tasks.DoesNotExist:
            return Response({'code': '404', 'message': "Data not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"code": 500, "message": "something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            transaction.set_autocommit(True)

    def delete(self, request, id=''):
        if not id:
            return Response({'code': '400', 'message': "Invalid inputs"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task = Tasks.objects.get(id=id)
            task.delete()
            return Response({'code': '200', 'message': "Data deleted successfully ", }, status=status.HTTP_200_OK)
        except Tasks.DoesNotExist:
            return Response({'code': '404', 'message': "Data not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def taskList(request):
    try:
        task = Tasks.objects.all()
        task_serializer = TaskSerializer(task,many=True)
        return Response({'code': '200', 'message': "Data retrieved successfully ", 'data': task_serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"code": 500, "message": "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)