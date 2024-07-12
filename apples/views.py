from .models import Municipality, Establishment, Category, Service, Apple, AppleService, Women, Attendance
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse 
from django.core.exceptions import ObjectDoesNotExist
import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from rest_framework.decorators import api_view, permission_classes
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .permissions import IsAdminRole, IsUserRole, IsWomenRole
from rest_framework.permissions import IsAuthenticated
import re


# Create your views here.


#AUTH

User = get_user_model()

def generate_token(user):
    refresh = RefreshToken.for_user(user)
    refresh['email'] = user.email  # Añadir email al token
    refresh['role'] = user.role    # Añadir rol al token
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
@csrf_exempt
def register_admin(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'response': 'Invalid JSON'}, status=400)
    
    email = data.get('email')
    password = data.get('password')

    if len(email) <= 2 or len(email) > 50 or len(password) <= 5 or len(password) > 30:
        return JsonResponse({'response': 'Parameters with incorrect length'}, status=400)
    
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'response': 'Invalid email format'}, status=400)

    if not email or not password:
        return JsonResponse({'response': 'Email and password are required'}, status=400)
    
    if User.objects.filter(email=email).exists():
        return JsonResponse({'response': 'Email already exists'}, status=400)
    
    user = User.objects.create_superuser(email=email, password=password)
    token = generate_token(user)

    return JsonResponse({
        'token': token,
        'user': {
            'email': user.email,
            'role': user.role
        }
    }, status=201)

@api_view(['POST'])
@csrf_exempt
def register_user(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'response': 'Invalid JSON'}, status=400)
    
    email = data.get('email')
    password = data.get('password')

    if len(email) <= 2 or len(email) > 50 or len(password) <= 5 or len(password) > 30:
        return JsonResponse({'response': 'Parameters with incorrect length'}, status=400)
    
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'response': 'Invalid email format'}, status=400)

    if not email or not password:
        return JsonResponse({'response': 'Email and password are required'}, status=400)
    
    if User.objects.filter(email=email).exists():
        return JsonResponse({'response': 'Email already exists'}, status=400)
    
    user = User.objects.create_user(email=email, password=password)
    token = generate_token(user)

    return JsonResponse({
        'token': token,
        'user': {
            'email': user.email,
            'role': user.role
        }
    }, status=201)

@api_view(['POST'])
@csrf_exempt
def login(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'response': 'Invalid JSON'}, status=400)
    
    email = data.get('email')
    password = data.get('password')

    if len(email) <= 2 or len(email) > 50 or len(password) <= 5 or len(password) > 30:
        return JsonResponse({'response': 'Parameters with incorrect length'}, status=400)
    
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'response':'Invalid email format'}, status=400)
    
    if not email or not password:
        return JsonResponse({'response': 'Email and password are required'}, status=400)

    user = authenticate(request, email=email, password=password)
    if user is None:
        return JsonResponse({'response': 'Invalid credentials'}, status=400)
    
    token = generate_token(user)

    return JsonResponse({'token': token,}, status=200)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details (request):
    user = request.user

    if user.role == "Women":
        women = Women.objects.get(user=user)
        return JsonResponse({
                'name': women.name,
                'email': women.user.email,
                'document_type': women.document_type,
                'identification_number': women.identification_number,
                'phone': women.phone,
                'city': women.city,
                'direction': women.direction,
                'ocupation': women.ocupation,
                'profile_picture': user.profile_picture.url
            }, status=200)
    
    return JsonResponse({
            'email': user.email,
            'profile_picture': user.profile_picture.url
        }, status=200)

@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminRole])
def delete_user(request, id):
    try:
        user = User.objects.get(pk=id)
        if user.role == "Women":
            women = Women.objects.get(user=user)
            women.delete()
        user.delete()
        return JsonResponse({'user': 'Successfully deleted user'}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'response': 'Element not found'}, status=404)
    

#CRUD WOMEN
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsUserRole])
def register_women(request):
    user = request.user

    if Women.objects.filter(user=user).exists():
        return JsonResponse({'response':'You are already registered as a woman'}, status=400)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'response':'Invalid JSON'}, status=400)
    
    document_type = data.get('document_type')
    identification_number = data.get('identification_number')
    name = data.get('name')
    phone = data.get('phone')
    city = data.get('city')
    direction = data.get('direction')
    ocupation = data.get('ocupation')

    if not re.match(r'^\d+$', identification_number):
        return JsonResponse({'response': 'Identification number must contain only digits'}, status=400)
    
    if Women.objects.filter(identification_number=identification_number).exists():
        return JsonResponse({'response':'The identification document already exists'}, status=400)
    
    if not re.match(r'^\d+$', phone):
        return JsonResponse({'response': 'Phone number must contain only digits'}, status=400)
    
    if not document_type or not identification_number or not name or not phone or not city or not direction or not ocupation:
        return JsonResponse({'response':'All data is required'}, status=400)
    
    new_women = Women.objects.create(
        user=user,
        document_type=document_type,
        identification_number=identification_number,
        name=name,
        phone=phone,
        city=city,
        direction=direction,
        ocupation=ocupation
    )

    new_women.save()
    
    user.role = "Women"
    user.save()

    return JsonResponse({'women':{
        'name': new_women.name,
        'email': new_women.user.email,
        'role': new_women.user.role,
        'document_type': new_women.document_type,
        'identification_number': new_women.identification_number,
        'phone': new_women.phone,
        'city': new_women.city,
        'direction': new_women.direction,
        'ocupation': new_women.ocupation
    }}, status=201)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsWomenRole])
def edit_women(request):
    user = request.user
    
    try:
        women = Women.objects.get(user=user)
    except Women.DoesNotExist:
        return JsonResponse({'response':'You have not registered as a woman'}, status=400)

    name = request.POST.get('name')
    phone = request.POST.get('phone')
    city = request.POST.get('city')
    direction = request.POST.get('direction')
    ocupation = request.POST.get('ocupation')
    profile_picture = request.FILES.get('profile_picture', None)

    
    if not re.match(r'^\d+$', phone):
        return JsonResponse({'response': 'Phone number must contain only digits'}, status=400)
    
    if not name or not phone or not city or not direction or not ocupation:
        return JsonResponse({'response':'All data is required'}, status=400)
    
    women.name = name
    women.phone = phone
    women.city = city
    women.direction = direction
    women.ocupation = ocupation

    women.save()

    if profile_picture:
        user.profile_picture = profile_picture
        user.save()


    return JsonResponse({'women':{
        'name': women.name,
        'email': women.user.email,
        'document_type': women.document_type,
        'identification_number': women.identification_number,
        'phone': women.phone,
        'city': women.city,
        'direction': women.direction,
        'ocupation': women.ocupation,
        'profile_picture': women.user.profile_picture.url
    }}, status=200)


#CRUD ATTENDANCE

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsWomenRole])
def create_attendance(request):
    user = request.user

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'response':'Invalid JSON'}, status=400)

    apple = data.get('apple')
    apple_service = data.get('apple_service')
    date = data.get('date')

    try:
        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
        if date < datetime.now():
            return JsonResponse({'response': 'The date and time cannot be in the past'}, status=400)
    except ValueError:
        return JsonResponse({'response': 'Invalid date format'}, status=400)
    
    if not Apple.objects.filter(apple=apple).exists():
        return JsonResponse({'response':'The apple with that id was not found'}, status=404)

    if not AppleService.objects.filter(pk=apple_service).exists():
        return JsonResponse({'response':'The service with that id was not found'}, status=404)

    if Attendance.objects.filter(date=date, apple=apple, apple_service=apple_service).exists():
        return JsonResponse({'response': 'There is already an attendance scheduled for this date and time'}, status=409)
    
    new_attendance = Attendance(
        user= user,
        apple=apple,
        apple_service= apple_service,
        date=date
    )

    new_attendance.save()

    return JsonResponse({'attendance':'Attendance created successfully'}, status=201)
    


#CRUD MUNICIPALITIES
@csrf_exempt
def municipalities(request):
    if request.method == 'GET':
        municipalities = Municipality.objects.all().values('id','name', 'image')
        municipalities_list = list(municipalities)
        return JsonResponse({'municipalities': municipalities_list}, status=200)
    else:
        return JsonResponse({'response':'Invalid HTTP method'}, status=405)


@csrf_exempt
def create_municipality(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image', None)

        if len(name) <= 2 or len(name) > 50:
            return JsonResponse({'response': 'Parameters with incorrect length'}, status=400)

        try:
            Municipality.objects.get(name=name)
            return JsonResponse({'response': 'Municipality with this name already exists'}, status=400)
        except ObjectDoesNotExist:
            if not image:
                new_municipality = Municipality.objects.create(
                    name = name
                )
            else:
                new_municipality = Municipality.objects.create(
                    name=name,
                    image=image
                )

            return JsonResponse({
                'municipality': {
                    'id': new_municipality.id,
                    'name': new_municipality.name,
                    'image': new_municipality.image.url
                }
            }, status=201)
    else:
        return JsonResponse({'response': 'Invalid HTTP method'}, status=405)
    

@csrf_exempt
def edit_municipality(request, id):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image', None)

        if len(name) <= 2 or len(name) > 50:
            return JsonResponse({'response': 'Parameters with incorrect length'}, status=400)

        try:
            Municipality.objects.get(name=name)
            return JsonResponse({'response': 'Municipality with this name already exists'}, status=400)
        except ObjectDoesNotExist:
            edit_municipality = Municipality.objects.get(pk=id)

            if not image:
                edit_municipality.name = name
            else:
                edit_municipality.name = name
                edit_municipality.image = image
            
            edit_municipality.save()
            return JsonResponse({
                'municipality': {
                    'id': edit_municipality.id,
                    'name': edit_municipality.name,
                    'image': edit_municipality.image.url
                }
            }, status=200)
    else:
        return JsonResponse({'response': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def delete_municipality(request, id):
    if request.method == "DELETE":
        try:
            delete_municipality = Municipality.objects.get(pk=id)
            delete_municipality.delete()
            return JsonResponse({
                'municipality': {
                    'id': id,
                    'name': delete_municipality.name,
                    'image': delete_municipality.image.url
                    }
                }, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'response': 'Element not was found'}, status=404)
    else:
        return JsonResponse({'response': 'Invalid HTTP method'}, status=405)



#CRUD ESTABLISHMENTS
@csrf_exempt
def establishments(request):
    if request.method == 'GET':
        establishments = Establishment.objects.all().values('id','code', 'name', 'responsible', 'direction', 'image')
        establishments_list = list(establishments)
        return JsonResponse({'establishments': establishments_list}, status=200)
    else:
        return JsonResponse({'response':'Invalid HTTP method'}, status=405)


@csrf_exempt
def create_establishment(request):
    if request.method == 'POST':
        code = request.POST.get('code', '')
        name = request.POST.get('name')
        responsible = request.POST.get('responsible')
        direction = request.POST.get('direction')
        image = request.FILES.get('image')

        if len(name) <= 2 or len(name) >= 100 or len(responsible) <= 2 or len(responsible) > 50 or len(direction) <= 2 or len(direction) > 100:
            return JsonResponse({'response': 'Parameters with incorrect length'}, status=400)

        if Establishment.objects.filter(name=name).exists():
            return JsonResponse({'response': 'Establishment with this name already exists'}, status=400)
        if Establishment.objects.filter(direction=direction).exists():
            return JsonResponse({'response': 'Establishment with this direction already exists'}, status=400)
        if Establishment.objects.filter(code=code).exists():
            return JsonResponse({'response': 'Establishment with this code already exists'}, status=400)

        new_establishment = Establishment(
            name=name,
            responsible=responsible,
            direction=direction,
        )

        if code:
            new_establishment.code = code

        if image:
            new_establishment.image = image

        new_establishment.save()

        return JsonResponse({'establishment': {
                    'id': new_establishment.id,
                    'code': new_establishment.code,
                    'name': new_establishment.name,
                    'responsible': new_establishment.responsible,
                    'direction': new_establishment.direction,
                    'image': new_establishment.image.url
                }}, status=201)
    else:
        return JsonResponse({'response': 'Invalid HTTP method'}, status=405)
    

@csrf_exempt
def edit_establishment(request, id):
    if request.method == 'POST':

        try:
            edit_establishment = Establishment.objects.get(pk=id)
        except Establishment.DoesNotExist:
            return JsonResponse({'response': 'Element not was found'}, status=404)
        
        code = request.POST.get('code', '')
        name = request.POST.get('name')
        responsible = request.POST.get('responsible')
        direction = request.POST.get('direction')
        image = request.FILES.get('image')

        if code != '' and len(code) != 10:
            return JsonResponse({'response':'Parameters with incorrect length'}, status=400)

        if len(name) <= 2 or len(name) >= 100 or len(responsible) <= 2 or len(responsible) > 50 or len(direction) <= 2 or len(direction) > 100:
            return JsonResponse({'response': 'Parameters with incorrect length'}, status=400)
            

        if Establishment.objects.filter(name=name).exclude(pk=id).exists():
            return JsonResponse({'response': 'Establishment with this name already exists'}, status=400)
        if Establishment.objects.filter(direction=direction).exclude(pk=id).exists():
            return JsonResponse({'response': 'Establishment with this direction already exists'}, status=400)
        if code and Establishment.objects.filter(code=code).exclude(pk=id).exists():
            return JsonResponse({'response': 'Establishment with this code already exists'}, status=400)


        edit_establishment.name = name
        edit_establishment.responsible = responsible
        edit_establishment.direction = direction
        if code:
            edit_establishment.code = code

        if image:
            edit_establishment.image = image   


        edit_establishment.save()

        return JsonResponse({'establishment': {
                    'id': edit_establishment.id,
                    'code': edit_establishment.code,
                    'name': edit_establishment.name,
                    'responsible': edit_establishment.responsible,
                    'direction': edit_establishment.direction,
                    'image': edit_establishment.image.url
                }}, status=200)
    else:
        return JsonResponse({'response': 'Invalid HTTP method'}, status=405)
    

@csrf_exempt
def delete_establishment(request, id):
    if request.method == "DELETE":
        try:
            delete_establishment = Establishment.objects.get(pk=id)
            delete_establishment.delete()
            return JsonResponse({
                'municipality': {
                    'id': id,
                    'code': delete_establishment.code,
                    'name': delete_establishment.name,
                    'responsible': delete_establishment.responsible,
                    'direction': delete_establishment.direction,
                    'image': delete_establishment.image.url
                    }
                }, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'response': 'Element not was found'}, status=404)
    else:
        return JsonResponse({'response': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def categories(request):
    if request.method == 'GET':
        categories = Category.objects.all().values('id','name', 'description', 'image')
        categories_list = list(categories)
        return JsonResponse({'categories': categories_list}, status=200)
    else:
        return JsonResponse({'response':'Invalid HTTP method'}, status=405)
    

@csrf_exempt
def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image =  request.FILES.get('image')

        if len(name) <= 2 or len(name) > 50 or len(description) <=2 or len(description) > 300:
            return JsonResponse({'response': 'Parameters with incorrect length'}, status=400)

        try:
            Category.objects.get(name=name)
            return JsonResponse({'response':'Category with this name already exists'}, status=400)
        except ObjectDoesNotExist:
            new_category = Category(
                name = name,
                description = description
            )

            if image:
                new_category.image = image

            new_category.save()

            return JsonResponse({'category':{
                'id': new_category.id,
                'name': new_category.name,
                'description': new_category.description,
                'image': new_category.image.url
            }}, status=201)
    else:
        return JsonResponse({'response':'Invalid HTTP method'}, status=405)
    

@csrf_exempt
def edit_category(request, id):
    if request.method == 'POST':

        try:
            edit_category = Category.objects.get(pk=id)
        except Category.DoesNotExist:
            return JsonResponse({'response': 'Element not was found'}, status=404)
        
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if len(name) <= 2 or len(name) > 50 or len(description) <=2 or len(description) > 300:
            return JsonResponse({'response': 'Parameters with incorrect length'}, status=400)
            

        if Category.objects.filter(name=name).exclude(pk=id).exists():
            return JsonResponse({'response': 'Category with this name already exists'}, status=400)


        edit_category.name = name
        edit_category.description = description

        if image:
            edit_category.image = image   


        edit_category.save()

        return JsonResponse({'category': {
                    'id': edit_category.id,
                    'name': edit_category.name,
                    'description': edit_category.description,
                    'image': edit_category.image.url
                }}, status=200)
    else:
        return JsonResponse({'response': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def delete_category(request, id):
    if request.method == "DELETE":
        try:
            delete_category = Category.objects.get(pk=id)
            delete_category.delete()
            return JsonResponse({
                'category': {
                    'id': id,
                    'name': delete_category.name,
                    'description': delete_category.description,
                    'image': delete_category.image.url
                    }
                }, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'response': 'Element not was found'}, status=404)
    else:
        return JsonResponse({'response': 'Invalid HTTP method'}, status=405)
    

@csrf_exempt
def services(request):
    if request.method == "GET":
        services = Service.objects.all()
        list_services = []
        for service in services:
            list_services.append({
                "id": service.id,
                "code": service.code,
                "name": service.name,
                "description": service.description,
                "category": {
                    "id": service.category.id,
                    "name": service.category.name
                },
                "establishment": {
                    "id": service.establishment.id,
                    "name": service.establishment.name
                },
                "image": service.image.url
            })
        return JsonResponse({'services': list_services}, status=200)
    else:
        return JsonResponse({'response': 'Invalid HTTP method'}, status=405)
    

@csrf_exempt
def create_service (request):
    if request.method == "POST":
        category_id = request.POST.get('category')
        establishment_id = request.POST.get('establishment')
        code = request.POST.get('code', '')
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return JsonResponse({'response':'Category not was found'}, status=404)
        
        try:
            establishment = Establishment.objects.get(pk=establishment_id)
        except Establishment.DoesNotExist:
            return JsonResponse({'response':'Establishment not was found'}, status=404)
        
        if len(name) <= 2 or len(name) > 100 or len(description) <= 2 or len(description) > 300:
            return JsonResponse({'response': 'Parameters with incorrect length'}, status=400)

        if Service.objects.filter(name=name).exists():
            return JsonResponse({'response': 'Service with this name already exists'}, status=400)
        if Service.objects.filter(code=code).exists():
            return JsonResponse({'response': 'Service with this code already exists'}, status=400)


        new_service = Service(
            category = category,
            establishment = establishment,
            name = name,
            description = description
        )

        if code:
            new_service.code = code
        
        if image:
            new_service.image = image

        new_service.save()
        return JsonResponse({'service':{
            "id": new_service.id,
            "code": new_service.code,
            "name": new_service.name,
            "description": new_service.description,
            "category": {
                "id": new_service.category.id,
                "name": new_service.category.name
            },
            "establishment": {
                "id": new_service.establishment.id,
                "name": new_service.establishment.name
            },
            "image": new_service.image.url
        }}, status=201)
    else:
        return JsonResponse({'response':'Invalid HTTP method'}, status=405)
    

@csrf_exempt
def edit_service(request, id):
    if request.method == "POST":

        try:
            edit_service = Service.objects.get(pk=id)
        except Service.DoesNotExist:
            return JsonResponse({'response':'Element not was found'}, status=404)

        category_id = request.POST.get('category')
        establishment_id = request.POST.get('establishment')
        code = request.POST.get('code')
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return JsonResponse({'response':'Category not was found'}, status=404)
        
        try:
            establishment = Establishment.objects.get(pk=establishment_id)
        except Establishment.DoesNotExist:
            return JsonResponse({'response':'Establishment not was found'}, status=404)


        if len(code) != 10 or len(name) <= 2 or len(name) >= 100 or len(description) <= 2 or len(description) > 300:
            return JsonResponse({'response': 'Parameters with incorrect length'}, status=400)

        if Service.objects.filter(name=name).exclude(pk=id).exists():
            return JsonResponse({'response': 'Service with this name already exists'}, status=400)
        if Service.objects.filter(code=code).exclude(pk=id).exists():
            return JsonResponse({'response': 'Service with this code already exists'}, status=400)

        edit_service.category = category
        edit_service.establishment = establishment
        edit_service.name = name
        edit_service.description = description

        if code:
            edit_service.code = code
        
        if image:
            edit_service.image = image
        
        edit_service.save()
        return JsonResponse({'service':{
            "id": edit_service.id,
            "code": edit_service.code,
            "name": edit_service.name,
            "description": edit_service.description,
            "category": {
                "id": edit_service.category.id,
                "name": edit_service.category.name
            },
            "establishment": {
                "id": edit_service.establishment.id,
                "name": edit_service.establishment.name
            },
            "image": edit_service.image.url
        }}, status=200)
    else:
        return JsonResponse({'response':'Invalid HTTP method'}, status=405)


@csrf_exempt
def delete_service (request, id):
    if request.method == "DELETE":
        
        try:
            delete_service = Service.objects.get(pk=id)
            delete_service.delete() 
            return JsonResponse({'service':{
                'id': id,
                'code': delete_service.code,
                'name': delete_service.name,
                'description': delete_service.description,
                'category':{
                    'id': delete_service.category.id,
                    'name': delete_service.category.name
                },
                "establishment": {
                    "id": delete_service.establishment.id,
                    "name": delete_service.establishment.name
                },
                "image": delete_service.image.url
            }}, status=200)
        except Service.DoesNotExist:
            return JsonResponse({'response':'Element not was found'}, status=404)
    else:
        return JsonResponse({'response':'Invalid HTTP method'}, status=405)


@csrf_exempt
def apples (request):
    if request.method == "GET":
        apples = Apple.objects.all()
        list_apples = []

        for apple in apples:
            list_services = [
                {"id": service.id, "code": service.code, "name": service.name}
                for service in apple.services.all()
            ]

            apple_data = {
                "id": apple.id,
                "code": apple.code,
                "name": apple.name,
                "direction": apple.direction,
                "municipality": {
                    "id": apple.municipality.id,
                    "name": apple.municipality.name
                },
                "services": list_services
            }

            list_apples.append(apple_data)

            return JsonResponse({'apples': list_apples}, status=200)
    else:
        return JsonResponse({'response':'Invalid HTTP method'}, status=405)
    

@csrf_exempt
def create_apple (request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'response': 'Invalid JSON'}, status=400)

        code = data.get("code", "")
        name = data.get("name")
        direction = data.get("direction")
        municipality_id = data.get("municipality")
        services = data.get("services", [])

        if not isinstance(services, list) or not all(isinstance(service_id, int) for service_id in services):
            return JsonResponse({'response':'Services must be a list of integers'}, status=400)
        
        if len(services) < 1 or len(services) > Service.objects.all().count():
            return JsonResponse({'response':'The number of services entered is incorrect'}, status=400)
        
        if len(name) <= 2 or len(name) > 100 or len(direction) <= 5 or len(direction) > 50:
            return JsonResponse({'response': 'Parameters with incorrect length'}, status=400)
        
        if code and len(code) != 10:
            return JsonResponse({'response': 'Parameter code must have length 10'}, status=400)
        
        try:
            municipality = Municipality.objects.get(pk=municipality_id)
        except Municipality.DoesNotExist:
            return JsonResponse({'response':'Municipality not was found'}, status=404)

        if Apple.objects.filter(name=name).exists():
            return JsonResponse({'response':'Apple with this name already exists'}, status=400)
        
        if Apple.objects.filter(code=code).exists():
            return JsonResponse({'response':'Apple with this code already exists'}, status=400)
        
        if Apple.objects.filter(direction=direction).exists():
            return JsonResponse({'response':'Apple with this direction already exists'}, status=400)
        
        create_apple = Apple(
            name = name,
            direction = direction,
            municipality = municipality
        )

        if code:
            create_apple.code = code
        
        create_apple.save()

        created_services = []
        for service_id in services:
            try:
                service = Service.objects.get(pk=service_id)
                AppleService.objects.create(apple=create_apple, service=service)
                service_data = {
                    "id": service.id,
                    "code": service.code,
                    "name": service.name
                }
                created_services.append(service_data)
            except Service.DoesNotExist:
                return JsonResponse({'response': f'Service with id {service_id} does not exist'}, status=404)
            
        return JsonResponse({'Apple':{
            'id': create_apple.id,
            'code': create_apple.code,
            'name': create_apple.name,
            'direction': create_apple.direction,
            'municipality': {
                'id': create_apple.municipality.id,
                'name': create_apple.municipality.name
            },
            'services': created_services
        }}, status=201)
    
    else:
        return JsonResponse({'response': 'Invalid HTTP method'}, status=405)
    

@csrf_exempt
def edit_apple (request, id):
    if request.method == "POST":
        
        try:
            edit_apple = Apple.objects.get(pk=id)
        except Apple.DoesNotExist:
            return JsonResponse({'response':'Element was not found'}, status=404)
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'response':'Invalid JSON'}, status=400)
        
        code = data.get("code", "")
        name = data.get("name")
        direction = data.get("direction")
        municipality_id = data.get("municipality")
        services = data.get("services", [])

        if not isinstance(services, list) or not all(isinstance(service_id, int) for service_id in services):
            return JsonResponse({'response':'Services must be a list of integers'}, status=400)
        
        if len(services) < 1 or len(services) > Service.objects.all().count():
            return JsonResponse({'response':'The number of services entered is incorrect'}, status=400)
        
        if len(name) <= 2 or len(name) > 100 or len(direction) <= 5 or len(direction) > 50:
            return JsonResponse({'response': 'Parameters with incorrect length'}, status=400)
        
        if code and len(code) != 10:
            return JsonResponse({'response': 'Parameter code must have length 10'}, status=400)
        
        try:
            municipality = Municipality.objects.get(pk=municipality_id)
        except Municipality.DoesNotExist:
            return JsonResponse({'response':'Municipality not was found'}, status=404)

        if Apple.objects.filter(name=name).exclude(pk=id).exists():
            return JsonResponse({'response':'Apple with this name already exists'}, status=400)
        
        if Apple.objects.filter(code=code).exclude(pk=id).exists():
            return JsonResponse({'response':'Apple with this code already exists'}, status=400)
        
        if Apple.objects.filter(direction=direction).exclude(pk=id).exists():
            return JsonResponse({'response':'Apple with this direction already exists'}, status=400)

        edit_apple.name = name
        edit_apple.direction = direction
        edit_apple.municipality = municipality

        if code:
            edit_apple.code = code

        edit_apple.save()

        AppleService.objects.filter(apple=edit_apple).delete()

        edit_services = []
        for service_id in services:
            try:
                service = Service.objects.get(pk=service_id)
                AppleService.objects.create(apple=edit_apple, service=service)
                service_data = {
                    "id": service.id,
                    "code": service.code,
                    "name": service.name
                }
                edit_services.append(service_data)
            except Service.DoesNotExist:
                return JsonResponse({'response': f'Service with id {service_id} does not exist'}, status=404)
            
        return JsonResponse({'Apple':{
            'id': edit_apple.id,
            'code': edit_apple.code,
            'name': edit_apple.name,
            'direction': edit_apple.direction,
            'municipality': {
                'id': edit_apple.municipality.id,
                'name': edit_apple.municipality.name
            },
            'services': edit_services
        }}, status=201)
    
    else:
        return JsonResponse({'response':'Invalid HTTP method'}, status=405)
    

@csrf_exempt
def delete_apple (request, id):
    if request.method == "DELETE":
        
        try:
            delete_apple = Apple.objects.get(pk=id)
            
            list_services = []
            delete_services = AppleService.objects.filter(apple=delete_apple)
            if delete_services.exists():
                for service in delete_services:
                    service_data = {
                        "id": service.service.id,
                        "code": service.service.code,
                        "name": service.service.name
                    }
                    list_services.append(service_data)
                delete_services.delete()

            delete_apple.delete()
            return JsonResponse({'Apple':{
                "id": id,
                "code": delete_apple.code,
                "name": delete_apple.name,
                "direction": delete_apple.direction,
                "municipality": {
                    "id": delete_apple.municipality.id,
                    "name": delete_apple.municipality.name
                },
                "services": list_services
            }}, status=200)
        
        except Apple.DoesNotExist:
            return JsonResponse({'response':'Element not was found'}, status=404)

    else:
        return JsonResponse({'response':'Invalid HTTP method'}, status=405)