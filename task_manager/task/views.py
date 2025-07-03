from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from django.contrib.auth.models import User
from django. shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

class UserRegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User Registered successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user = request.user).order_by('-created_at')
        paginator = PageNumberPagination()
        paginator.page_size = 3

        result_page = paginator.paginate_queryset(tasks, request)
        serializer = TaskSerializer(result_page, many= True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self,request):
        serializer = TaskSerializer(data = request.data)
        if serializer.is_valid():
            task = serializer.save(user=request.user) 
            response_serializer = TaskSerializer(task)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self, pk, user):
        task = get_object_or_404(Task, pk=pk, user=user)
        self.check_object_permissions(self.request, task)
        return task
    
    def get(self, request, pk):
        task = self.get_object(pk, request.user)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def put(self, request, pk):
        task = self.get_object(pk, request.user)
        serializer = TaskSerializer(task, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_object(pk , request.user)
        task.delete()
        return Response({'message': 'Task Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)


