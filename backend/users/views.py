from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

# 简历图片上传测试视图
class UploadImageView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # 获取上传的图片文件
        image_file = request.FILES.get('image')
        
        # 在实际项目中，这里应该保存图片并返回真实URL
        # 为了演示，我们假设图片已保存并返回一个模拟URL
        
        # 返回模拟数据（待替换为真实OCR解析逻辑）
        return Response({
            'code': 200,
            'data': {
                'name': '张三',
                'education': '清华大学 计算机科学与技术 硕士',
                'experience': '5年全栈开发经验',
                'image_url': request.build_absolute_uri('/media/temp_image.jpg') if image_file else None
            },
            'message': '解析成功'
        }, status=status.HTTP_200_OK)

# 用户注册视图
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

# 用户登录视图
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        print(password)
        if user is not None:
            login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response({'detail': '用户名或密码错误'}, status=status.HTTP_400_BAD_REQUEST)

# 用户登出视图
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'detail': '成功登出'})

# 获取当前用户信息
class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
