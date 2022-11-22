from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.views import Location # Proveri ovo
from .serializers import locationSerializer

@api_view(['GET'])
def getRoutes(request):
    
    routes = [
        'GET /api',
        'GET /api/locations',
        'GET /api/locations/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getLocations(request):
    locations = Location.objects.all()
    serializer = locationSerializer(locations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getLocation(request, pk):
    location = Location.objects.get(id=pk) 
    serializer = locationSerializer(location, many=False)
    return Response(serializer.data)