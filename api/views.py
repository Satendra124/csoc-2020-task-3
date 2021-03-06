from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from .models import Todo
from django.http import JsonResponse


"""
TODO:
Create the appropriate View classes for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""


class TodoCreateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        todo=Todo.objects.get(title=serializer.data['title'])
        ser=self.get_serializer(todo)
        return Response(ser.data,status=status.HTTP_200_OK)

class TodoView(generics.GenericAPIView):
    permission_classes=(permissions.IsAuthenticated,)
    serializer_class=TodoCollaborativeGet
    def get(self,request):
        todo_o=Todo.objects.filter(creator=User.objects.get(username=self.request.user.username))
        todo_c=set()
        for todos in Todo.objects.all():
            if todos.colaborators.filter(username=request.user.username).count()>0:
                todo_c.add(todos)
        serializer_o=TodoSerializer(todo_o,many=True)
        serializer_c=TodoSerializer(todo_c,many=True)
        todolist={
            'collaborations': serializer_c.data,
            'created': serializer_o.data
        }
        serializer=self.get_serializer(data=todolist)
        serializer.is_valid(raise_exception=True) 
        return Response(serializer.data,status=status.HTTP_200_OK)
class PutPatchTodoView(generics.RetrieveAPIView):
    serializer_class=PutPatchSerializer
    permission_classes=(permissions.IsAuthenticated,)
    def put(self,request,id):
        try:
            todo_object=Todo.objects.get(id=id)
            if todo_object.creator==request.user:
                todo_object.title=request.data['title']
                todo_object.save(update_fields=['title'])
                serializer = self.get_serializer(todo_object)
                return Response(serializer.data)
            else:
                return JsonResponse({"Error":"Colaborators cant change title of Todo please contact "+todo_object.creator.username})
        except:
            return JsonResponse({"Error":"Wrong ID of requested todo or some server error"})
    #review
    def patch(self,request,id):
        try:
            todo_object=Todo.objects.get(id=id)
            if todo_object.creator==request.user:
                todo_object.title=request.data['title']
                todo_object.save(update_fields=['title'])
                serializer = self.get_serializer(todo_object)
                return Response(serializer.data)
            else:
                return JsonResponse({"Error":"Colaborators cant change title of Todo please contact "+todo_object.creator.username})
        except:
            return JsonResponse({"Error":"Wrong ID of requested todo or some server error"})
class SpecificTodoView(generics.RetrieveAPIView):
    permission_classes=(permissions.IsAuthenticated,)
    serializer_class=SpecificTodoSerializer
    def get(self,request,id):
        try:
            todo_object = Todo.objects.get(id=id)
            serializer = self.get_serializer(todo_object)
            return Response(serializer.data)
        except:
            return JsonResponse({"Error":"Wrong ID of requested todo or some server error"})
    def delete(self,request,id):
        try:
            todo_object=Todo.objects.get(id=id)
            todo_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return JsonResponse({"Error":"Wrong ID of requested todo or some server error"})
        
class CollaboratorView(generics.GenericAPIView):
    permission_classes=(permissions.IsAuthenticated,)
    serializer_class=ColabSerializer
    def post(self,request,id):
        serializer = self.get_serializer(request.data)
        try:
            todo=Todo.objects.get(id=id)
            if todo.creator==request.user:
                todo.colaborators.add(User.objects.get(username=serializer.data['username']))
                return Response({"details":"Coloborator added"})
            else:
                return Response({"Error":"You are not The owner Of This Todo"})
        except:
            return JsonResponse({"Error":"Wrong ID of requested todo or some server error"})

    def patch(self,request,id):
        serializer = self.get_serializer(request.data)
        try:
            todo=Todo.objects.get(id=id)
            if todo.creator==request.user:
                todo.colaborators.remove(User.objects.get(username=serializer.data['username']))
                return Response({"details":"Coloborator Removed"})
            else:
                return Response({"Error":"You are not The owner Of This Todo"}) 
        except:
            return JsonResponse({"Error":"Wrong ID of requested todo or some server error"})