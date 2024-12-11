from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Profile
from .serializers import ProfileSerializer, UserSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token


@api_view(['GET'])
def profiles(request):
    Profiles = Profile.objects.all()
    serializer = ProfileSerializer(Profiles, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_profile(request):
    # Separate serializers for User and Profile
    user_serializer = UserSerializer(data=request.data)
    
    if user_serializer.is_valid():
        user = user_serializer.save()  # Save the user
        
        # Now create a profile for the user
        profile_data = request.data.copy()  # Copy the request data to modify it
        profile_data['user'] = user.id  # Add the user ID to the profile data
        
        # Now validate and save the profile with the user field set
        profile_serializer = ProfileSerializer(data=profile_data)
        
        if profile_serializer.is_valid():
            profile = profile_serializer.save(user=user)
            token = Token.objects.create(user=user)

            return Response({
                'user': user_serializer.data,
                'profile': profile_serializer.data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'profile': profile_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            'user': user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET', 'PUT', 'DELETE'])
def profile_detail(request, pk):
    try:
        profile = Profile.objects.get(id=pk)
    except Profile.DoesNotExist:
        return Response('Profile does not exist', status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProfileSerializer(instance=profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        user = profile.user
        user.delete()
        profile.delete()
        return Response('Profile deleted successfully')
    

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if not user:
        return Response('Invalid credentials', status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    user_serializer = UserSerializer(user)
    profile = Profile.objects.get(user=user)
    profile_serializer = ProfileSerializer(profile)
    return Response({'token': token.key, 'user': user_serializer.data, 'profile': profile_serializer.data})



from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed! for {}".format(request.user.username))