from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from drf_yasg.utils import swagger_auto_schema

from notes_app.models import Note
from notes_api.serializers import NoteSerializer, NoteCreateUpdateSerializer, UserRegisterSerializer, UserLoginSerializer


class NoteListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: HttpRequest):
        notes = Note.objects.filter(author=request.user)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NoteDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: HttpRequest, pk: int):
        note = get_object_or_404(Note, pk=pk, author=request.user)
        serializer = NoteSerializer(note)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class NoteCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=NoteCreateUpdateSerializer)
    def post(self, request: HttpRequest):
        serializer = NoteCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            note = serializer.save(author=request.user)
            return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class NoteUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=NoteCreateUpdateSerializer)
    def put(self, request: HttpRequest, pk: int):
        try:
            note = Note.objects.get(pk=pk, author=request.user)
        except Note.DoesNotExist:
            return Response({"detail": "Ничего не найдено"}, status=status.HTTP_404_NOT_FOUND)
        serializer = NoteCreateUpdateSerializer(note, data=request.data, partial=True)
        if serializer.is_valid():
            note = serializer.save()
            return Response(NoteSerializer(note).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class NoteDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={200: "Успешно удалено"})
    def delete(self, request: HttpRequest, pk: int):
        note = get_object_or_404(Note, pk=pk, author=request.user)
        note.delete()
        return Response({"detail": "Успешно удалено"})


class UserRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=UserRegisterSerializer)
    def post(self, request: HttpRequest):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user=user)
            return Response({"refresh": str(refresh), "access": str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=UserLoginSerializer)
    def post(self, request: HttpRequest):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request=request, username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user=user)
            return Response({"refresh": str(refresh), "access": str(refresh.access_token)})
        return Response({"error": "Неверные учётные данные"}, status=status.HTTP_401_UNAUTHORIZED)