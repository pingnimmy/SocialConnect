from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import get_user_model
from rest_framework import throttling
from .serializers import RegistrationSerializer, FriendRequestSerializer, UserSerializer
from .models import User, FriendRequest
from .throttling import FriendRequestRateThrottle

class Registration_view(APIView):
    def post(self, request, format=None):
        serializer = RegistrationSerializer(data=request.data)
      
        if serializer.is_valid():
            account = serializer.save()
            
        return Response({"Successfully Registered"}, status=status.HTTP_200_OK)

class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.get(email=username)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.auth.delete()
        return Response({'detail': 'Successfully logged out'})

class FriendRequestHandle_view(APIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    throttle_classes = [FriendRequestRateThrottle]

    def post(self, request):
        
        receiver_obj = User.objects.get(id=request.data.get('receiver'))
        requestpost_object = FriendRequest(
            sender=request.user,
            receiver=receiver_obj
            )
        requestpost_object.save()
        return Response({'Successfully send the request'})

    def patch(self, request, pk=None):
        friendrequest_object = FriendRequest.objects.get(id=request.data.get('request_id'))
        if request.data.get("status") == "accept":
            friendrequest_object.status = "accepted"
        else:
            friendrequest_object.status = "rejected"
        friendrequest_object.save()
        return Response({'Successfully changed the status'})

class FriendList_view(APIView):
 
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return FriendRequest.objects.all().filter(status="accepted")

    def get(self, request, *args, **kwargs):
        
        queryset = self.get_queryset().filter(sender__id=request.user.id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class PendingFriendList_view(APIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return FriendRequest.objects.all().filter(status="pending")

    def get(self, request, *args, **kwargs):

        queryset = self.get_queryset().filter(receiver=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class UserSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        search_keyword = request.GET.get('search')

        if not search_keyword:
            return Response({'error': 'Search keyword is required'}, status=status.HTTP_400_BAD_REQUEST)

        user_model = get_user_model()

        # Search by exact email
        email_user = user_model.objects.filter(email__iexact=search_keyword).first()
        if email_user:
            serializer = UserSerializer(email_user)
            return Response(serializer.data)

        # Search by name
        name_users = user_model.objects.filter(name__icontains=search_keyword)
        paginator = Paginator(name_users, 10)

        page = request.GET.get('page', 1)
        try:
            name_users_page = paginator.page(page)
        except PageNotAnInteger:
            name_users_page = paginator.page(1)
        except EmptyPage:
            name_users_page = paginator.page(paginator.num_pages)

        serializer = UserSerializer(name_users_page, many=True)
        return Response({
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'current_page': name_users_page.number,
            'results': serializer.data
        })



