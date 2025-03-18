from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from pprint import pprint
from paddlenlp import Taskflow
import fitz  # 用于PDF转图片

# 简历图片上传测试视图
class UploadImageView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # 获取上传的图片文件和实体类型
        image_file = request.FILES.get('file')
        entities = request.data.get('entities', '').split(',')  # 接收前端传来的实体类型

        if not image_file:
            return Response({
                'code': 400,
                'message': '未上传图片文件或文件格式不正确'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证文件类型
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
        if image_file.content_type not in allowed_types:
            return Response({
                'code': 400,
                'message': '不支持的文件类型，请上传JPG或PNG格式的图片'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 生成唯一的文件名
        import os
        from datetime import datetime
        from django.conf import settings
        
        file_name = f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}{os.path.splitext(image_file.name)[1]}"
        
        # 确保media目录存在
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        
        # 使用MEDIA_ROOT构建完整的文件路径
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        
        # 保存文件
        with open(file_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)
        
        # 动态设置schema
        schema = [entity.strip() for entity in entities if entity.strip()]  # 去除空字符串
        if not schema:  # 如果用户没选择，默认使用这些
            schema = ['姓名', '出生日期', '电话']
        
        ie = Taskflow('information_extraction', schema=schema)

        result = ie({"doc": file_path})
        data = {}
        for key in schema:
            if key in result[0]:
                data[key] = result[0][key][0]['text']
        data['image_url'] = request.build_absolute_uri(f'/media/{file_name}')
        
        # 返回数据
        return Response({
            'code': 200,
            'data': data,
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
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        logout(request)
        return Response({'detail': '成功登出'})

# 获取当前用户信息
class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# PDF上传处理视图
class UploadPDFView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # 获取上传的 PDF 文件和实体类型
        pdf_file = request.FILES.get('file')
        entities = request.data.get('entities', '').split(',')  # 接收前端传来的实体类型

        if not pdf_file:
            return Response({
                'code': 400,
                'message': '未上传 PDF 文件或文件格式不正确'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证文件类型
        allowed_types = ['application/pdf']
        if pdf_file.content_type not in allowed_types:
            return Response({
                'code': 400,
                'message': '不支持的文件类型，请上传 PDF 格式的文件'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 生成唯一的文件名
        import os
        from datetime import datetime
        from django.conf import settings
        
        # file_name = f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}{os.path.splitext(pdf_file.name)[1]}"
        file_name = 'test_pdf.pdf'
        
        # 确保 media 目录存在
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        
        # 使用 MEDIA_ROOT 构建完整的文件路径
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        
        # 保存 PDF 文件
        with open(file_path, 'wb+') as destination:
            for chunk in pdf_file.chunks():
                destination.write(chunk)
        
        # PDF 转图片
        pdf_document = fitz.open(file_path)
        image_path = None
        if len(pdf_document) > 0:
            page = pdf_document.load_page(0)
            pix = page.get_pixmap()
            image_name = f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}_page_0.png"
            image_path = os.path.join(settings.MEDIA_ROOT, image_name)
            pix.save(image_path)
        
        # 动态设置 schema
        schema = [entity.strip() for entity in entities if entity.strip()]  # 去除空字符串
        if not schema:  # 如果用户没选择，默认使用这些
            schema = ['姓名', '出生日期', '电话']
        
        # 初始化信息提取模型
        ie = Taskflow('information_extraction', schema=schema)

        # 执行信息提取
        result = ie({"doc": image_path})
        data = {}
        for key in schema:
            if key in result[0]:
                data[key] = result[0][key][0]['text']
        data['pdf_url'] = request.build_absolute_uri(f'/media/{image_name}')
        
        # 返回数据
        return Response({
            'code': 200,
            'data': data,
            'message': '解析成功'
        }, status=status.HTTP_200_OK)