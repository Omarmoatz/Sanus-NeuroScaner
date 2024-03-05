from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Company,Article
from .serializers import CompanySerializer,ArticleSerializer

@api_view(['GET'])
def company_info(request):
    info = Company.objects.last()
    serializer = CompanySerializer(info).data
    return Response({'data':serializer})
