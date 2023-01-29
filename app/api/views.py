from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from app.models import RiverBasin, Location, Data
from .serializers import LocationSerializer, RiverBasinSerializer, DataSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@api_view(['GET'])
def getRoutes(request):
    
    routes = [
        'GET /api',
        # Locations
        # GET
        'GET /api/locations',
        'GET /api/locations/:id',
        #POST
        'POST /api/create-location',
        # River basin
        # GET
        'GET /api/riverbasins',
        'GET /api/riverbasin/:id',
        #POST
        'POST /api/create-riverbasin',
        ''
        #Data
        # GET
        'GET /api/location/:id/files',
        'GET /api/file/:id',
        #POST
        'POST /api/upload-file' 
    ]
    return Response(routes)

# Location


'''Non class view for api'''
# # GET function for all location
# @api_view(['GET'])
# def getLocations(request):
#     locations = Location.objects.all()
#     serializer = LocationSerializer(locations, many=True)
#     return Response(serializer.data)

# # GET function for single location specified by pk
# @api_view(['GET', 'POST', 'DELETE'])
# def getLocation(request, pk):
#     location = Location.objects.get(id=pk) 
#     serializer = LocationSerializer(location, many=False)
#     return Response(serializer.data)


# # POST function for creating location
# @api_view(['POST'])
# def createLocation(request):
#     serializer = LocationSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     else:
#         return Response(serializer.errors)


'''Class view for ap'''


'''RRIVER BASIN'''

# List of River Basins
class RiverBasinList(APIView):

    def get(self, request):
        basin = RiverBasin.objects.all()
        serializer = RiverBasinSerializer(basin, many=True)
        return Response(serializer.data)

# Create River Basin
class CreateRiverBasin(APIView):

    def post(self, request):
        serializer = RiverBasinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Single River Basin with funciton GET, PUT, POST
class SingleRiverBasin(APIView):

    def get_basin_by_pk(self, pk):
        try:
            basin = RiverBasin.objects.get(id=pk)
            return basin
        except:
            return Response({
                'error': 'River Basin does not exist'
            }, status=status.HTTP_404_NOT_FOUND)
            
    # Gets River Basin
    def get(self, request, pk):
        basin = self.get_basin_by_pk(pk)
        serializer = RiverBasinSerializer(basin)
        return Response(serializer.data)

    # Updates River Basin
    def put(self, request, pk):
        basin = self.get_basin_by_pk(pk)
        serializer = RiverBasinSerializer(basin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Deletes River Basin
    def delete(self, request, pk):
        basin = self.get_basin_by_pk(pk)
        basin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



'''LOCATION'''

# List of locations
class LocationList(APIView):

    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

# Create location
class CreateLocation(APIView):

    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Single loation with funciton GET, PUT, POST
class SingleLocation(APIView):

    def get_location_by_pk(self, pk):
        try:
            location = Location.objects.get(id=pk)
            return location
        except:
            return Response({
                'error': 'Location does not exist'
            }, status=status.HTTP_404_NOT_FOUND)
            
    # Gets location
    def get(self, request, pk):
        location = self.get_location_by_pk(pk)
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    # Updates location
    def put(self, request, pk):
        location = self.get_location_by_pk(pk)
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Deletes location
    def delete(self, request, pk):
        location = self.get_location_by_pk(pk)
        if request.user == location.host:
            location.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


'''DATA/FILES'''

# List of lfiles/data
class FileList(APIView):

    def get(self, request, pk):
        files = Data.objects.filter(location_id=pk)
        serializer =DataSerializer(files, many=True)
        return Response(serializer.data)
       
#Create files/data
class UploadFile(APIView):
  
    def post(self, request):
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Single file/data with funciton GET, PUT, POST
class SingleFile(APIView):

    def get_file_by_pk(self, pk):
        try:
            file = Data.objects.get(id=pk)
            return file
        except:
            return Response({
                'error': 'Location does not exist'
            }, status=status.HTTP_404_NOT_FOUND)
            
    # Gets files/data
    def get(self, request, pk):
        file = self.get_file_by_pk(pk)
        serializer = DataSerializer(file)
        return Response(serializer.data)

    # Updates files/data
    def put(self, request, pk):
        file = self.get_file_by_pk(pk)
        serializer = DataSerializer(file, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Deletes files/data
    def delete(self, request, pk):
        file = self.get_file_by_pk(pk)
        if request.user == file.host:
            file.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)