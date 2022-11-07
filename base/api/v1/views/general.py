from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(['GET'])
def health(request):
    """
    Check API Health
    """
    if request.method == 'GET':
        return JsonResponse({'health': 'Ok'})
