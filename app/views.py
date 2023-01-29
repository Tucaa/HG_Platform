from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import RiverBasin, Location, Data, Graph
from .forms import LocationForm, UserForm, UploadForm
from django.views import View
from . import utils

# Create your views here.

# Login page view
def loginPage(request):
    #Specifing login page
    page = 'login'
    # Redirecting if user is alredy loged in
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'Username or paswword are incorect')
    context = {'page': page}
    return render(request, 'app/login_register.html', context)

# Logout user
def logoutUser(request):
    logout(request)
    return redirect('home')

#Register page view
def registerPage(request):

    #page = 'register' Dont need this
    # This form adds text for registration minimum char etc.
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            #Saving form (freezin in time)
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            #Login user when its created
            login(request, user)
            return redirect('home')
        else:
            #Eror hanling (add more maybe)
            messages.error(request, 'An error occured during rgistration')

    return render(request, 'app/login_register.html', {'form': form})

# Home page view
def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    locations = Location.objects.filter(
        Q(basin__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    
    basins = RiverBasin.objects.all()[0:5]
    location_count = locations.count()
    location_files = Data.objects.filter(Q(location__basin__name__icontains=q))

    context = {'locations': locations, 'basins': basins, 'location_count': location_count,
             'location_files': location_files} 

    return render(request, 'app/home.html', context)



# View for data. U shoud add graph here
def dataView(request, pk):

    data = Data.objects.get(id=pk)
    # Reading data from csv
    data_frame = utils.read_csv(data.dir)
    # Data for graph returns dictionary with data as a key and gwl as value
    data_dropdown = utils.data_from_csv(data_frame)

    
    #Converting data frame to html view
    data_frame = data_frame.to_html()

    # This is first displayed chart on the page inclues all data 
    chart = utils.get_chart(list(data_dropdown.keys()), list(data_dropdown.values()))

    if request.method == 'POST':
        date1 = request.POST['start_date']
        date2 = request.POST['end_date']
        # Findig index of selected date from dropdown in data
        x1 = list(data_dropdown.keys()).index(date1)
        x2 = list(data_dropdown.keys()).index(date2)
        chart_name = str(date1) + '-' + (date2)
        # This is new range for the chart based on selected dates form drowpdown
        chart_data = utils.chart_range(x1, x2, data_dropdown)
        # New chart
        chart = utils.get_chart(list(chart_data.keys()), list((chart_data.values())), name=chart_name)
        print(date1, date2)
    
    context = {'data': data, 'data_frame': data_frame, 'data_dropdown': list(data_dropdown.keys()),
                'chart': chart}

    return render(request, 'app/data_page.html', context)


# Download file view
class DownloadFile(View):
    model = Data
    fields = ['dir']
    template_name = 'app/data_page.html'

# Location in our case object 
@login_required(login_url='login')
def location(request, pk):

    location = Location.objects.get(id=pk)
    # location message dropbars
    # Files of location/object
    location_files = Data.objects.all()
    participants = location.participants.all()

    # Ovo ce ti treebati samo ako stavis dugme join koje nisi stavio
    # if request.method == 'POST':
    #     location.participants.add(request.user)
    #     #Redirect is needed for fuly page reload
    #     return redirect('location', pk=location.id)

    context = {'location': location, 'participants': participants, 'location_files': location_files}
    return render(request, 'app/location.html', context)

# User profile view
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    locations = user.location_set.all()
    location_files = user.data_set.all()
    basins = RiverBasin.objects.all()
    context = {'user': user, 'locations': locations, 'location_files': location_files, 'basins': basins }    
    return render(request, 'app/profile.html', context)

# Create location (in our case object rename it to object)
@login_required(login_url='login')
def createLocation(request):
    form = LocationForm()
    basins = RiverBasin.objects.all()
    if request.method == 'POST':
        basin_name = request.POST.get('river_basin')
        #Either returns object or creates it.
        basin, create = RiverBasin.objects.get_or_create(name=basin_name)
        
        Location.objects.create(
            host=request.user,
            basin=basin,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
    
        return redirect('home')

    context = {'form': form, 'basins': basins}
    return render(request, 'app/location_form.html', context)

@login_required(login_url='login')
def updateLocation(request, pk):
    location = Location.objects.get(id=pk)
    form = LocationForm(instance=location)
    basins = RiverBasin.objects.all()
    # Statement if user is alowed to edit rom. Is user a host
    if request.user != location.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        basin_name = request.POST.get('name')
        #Either returns object or creates it.
        basin, create = RiverBasin.objects.get_or_create(name=basin_name)
        location.name = request.POST.get('name')
        location.basin = basin
        location.description = request.POST.get('description')
        location.save()
   
        return redirect('home')

    context = {'form': form, 'basins': basins, 'location': location}
    return render(request, 'app/location_form.html', context)

@login_required(login_url='login')
def deleteLocation(request, pk):
    location = Location.objects.get(id=pk)

    # Statement if user is alowed to delete rom. Is user a host
    if request.user != location.host:
        return HttpResponse('You are not allowed here!')
        
    if request.method == 'POST':
        location.delete()
        return redirect('home')
        
    return render(request, 'app/delete.html', {'obj':location})


@login_required(login_url='login')
def deleteFile(request, pk):
    file = Data.objects.get(id=pk)

    # Statement if user is alowed to delete rom. Is user a host
    if request.user != file.host and request.user != file.location.host:
        return HttpResponse('You are not allowed here!')
        
    if request.method == 'POST':
        file.delete()
        return redirect('home')
        
    return render(request, 'app/delete.html', {'obj':file})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'app/update-user.html', {'form': form})


def basinsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    basins = RiverBasin.objects.filter(name__icontains=q)
    return render(request, 'app/basins.html', {'basins': basins})

def activityPage(request):
    files = Data.objects.all()
    return render(request, 'app/activity.html', {'files':files})


# Upload file view:
@login_required(login_url='login')
def uploadFile(request, pk):
    location = Location.objects.get(id=pk)
    # Need this type of form for file upload

    form = UploadForm(request.POST, request.FILES)
    if request.method == 'POST':
        Data.objects.create(
            host=request.user,
            location=location,
            name=request.POST.get('name'),
            # for files
            dir=request.FILES['dir'],
            description=request.POST.get('description') 
        )
        location.participants.add(request.user)
        return redirect('location', pk=location.id)

    context = {'form': form, 'location': location}

    return render(request, 'app/upload-file.html', context)


