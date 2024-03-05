from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets

from .models import Company,Article
from .serializers import CompanySerializer,ArticleSerializer

@api_view(['GET'])
def company_info(request):
    info = Company.objects.last()
    serializer = CompanySerializer(info).data
    return Response({'data':serializer})

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = ArticleSerializer
    