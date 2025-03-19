from django.http import JsonResponse

def handle_upload(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        text = request.POST.get('text', '')
        # 处理文件和文字的逻辑
        return JsonResponse({'status': 'success', 'text': text})
    return JsonResponse({'status': 'error'}, status=400)