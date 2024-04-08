from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction
from rest_framework.parsers import JSONParser
from .udf import *
from .serializers import *
from django.conf import settings


@csrf_exempt
def user_registration(request):
    try:
        with transaction.atomic():
            user_data = JSONParser().parse(request) 
            if request.method =="POST":
                user_email = user_data["email"]
                refrral_code = user_data["referral_code"]
                if not check_user_exist(user_email):
                    if refrral_code != "":
                        check_user = user_detail.objects.filter(id = refrral_code)
                        if check_user.exists():
                            check_user = check_user[0]
                            p_point = check_user.points
                            check_user.points=p_point+1
                            user_serializer = UserSerializer(data=user_data)
                            if user_serializer.is_valid():
                                all_data = user_serializer.save()
                                check_user.save()
                                user_id = all_data.id
                                token = get_tokens_for_user(user_id)
                                token_string = token.decode('utf-8')
                                return JsonResponse({
                                    "status": "Success",
                                    "message": "Admin signup Successfully",
                                    "data": {
                                        "user_id": user_id,
                                        "token":token_string
                                    }
                                })
                            return JsonResponse({
                                "status": "Failed",
                                "error_code": settings.ERROR_INVALID_DATA,
                                "message": user_serializer.errors
                            })
                        return JsonResponse({
                            "status": "Failed",
                            "error_code": settings.ERROR_ERROR_EXIST,
                            "message": "User with that refrral code is not exist"
                        })
                        
                    else:
                        user_serializer = UserSerializer(data=user_data)
                        if user_serializer.is_valid():
                            all_data = user_serializer.save()
                            user_id = all_data.id
                            token = get_tokens_for_user(user_id)
                            token_string = token.decode('utf-8')
                            return JsonResponse({
                                "status": "Success",
                                "message": "Admin signup Successfully",
                                "data": {
                                    "user_id": user_id,
                                    "token":token_string
                                }
                            })
                        return JsonResponse({
                                "status": "Failed",
                                "error_code": settings.ERROR_INVALID_DATA,
                                "message": user_serializer.errors
                            })
                return JsonResponse({
                    "status": "Failed",
                    "error_code": settings.ERROR_ERROR_EXIST,
                    "message": "Email is already registered"
                })
            return JsonResponse({
                "status":
                "Failed",
                "error_code":
                settings.ERROR_INVALID_REQUEST,
                "message":
                f"Not a valid request {request.method}"
            })
    except Exception as e:
        print("error",e)
        return JsonResponse({
            "status": "Failed",
            "error_code": settings.ERROR_ERROR_UNKNOWN,
            "message": f"Unknown Error - {e}"
        })

@csrf_exempt
def get_user(request):
    try:
        with transaction.atomic():
            if request.method =="GET":
                user_id, error_message = validate_jwt_token(request)
                print(user_id,error_message,"oo")
                if error_message:
                    return JsonResponse({'error': error_message}, status=401 if error_message == 'Token is missing' else 403)
                user_data = user_detail.objects.filter(id = user_id)
                if user_data.exists():
                    user_data = user_data[0]
                    list1 = []
                    dict = {}
                    dict["id"] = user_data.id
                    dict["first_name"] = user_data.name
                    dict["last_name"] = user_data.email
                    dict["referral_code"] = user_data.referral_code
                    dict["timestamp"] = user_data.created_at
                    list1.append(dict)
                    return JsonResponse({'message': 'Access granted','data':list1})
                return JsonResponse({
                                "status": "Failed",
                                "error_code": settings.ERROR_NOT_EXIST ,
                                "message": "No Result found"
                            })
            return JsonResponse({
                "status":
                "Failed",
                "error_code":
                settings.ERROR_INVALID_REQUEST,
                "message":
                f"Not a valid request {request.method}"
            })
            
    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'Token has expired'}, status=403)
    except jwt.InvalidTokenError:
        return JsonResponse({'error': 'Invalid token'}, status=402)
    except Exception as e:
        return JsonResponse({
            "status": "Failed",
            "error_code": settings.ERROR_ERROR_UNKNOWN,
            "message": f"Unknown Error - {e}"
        })
    
@csrf_exempt
def refrral_user(request):
    try:
        with transaction.atomic():
            if request.method =="GET":
                data = JSONParser().parse(request)

                user_id, error_message = validate_jwt_token(request)
                print(user_id,error_message,"oo")
                if error_message:
                    return JsonResponse({'error': error_message}, status=401 if error_message == 'Token is missing' else 403)
                user_data = user_detail.objects.filter(referral_code = user_id)
                if user_data.exists():
                    list1 = []
                    for k in user_data:
                        # user_data = user_data[0]
                        dict = {}
                        dict["id"] = k.id
                        dict["first_name"] = k.name
                        dict["last_name"] = k.email
                        dict["referral_code"] = k.referral_code
                        dict["timestamp"] = k.created_at
                        list1.append(dict)
                    page = data['page']
                    page_size = data['page_size']
                    paginated_data = custom_pagination(page, page_size ,list1)
                    return  JsonResponse({
                        "status": "Success",
                        "data" : {
                            "final_data" : paginated_data[0],
                            "total_data": paginated_data[1],
                            "data_remaining": paginated_data[2]
                        }
                    })
                return JsonResponse({
                                "status": "Failed",
                                "error_code": settings.ERROR_NOT_EXIST ,
                                "message": "No Result found"
                            })
            return JsonResponse({
                "status":
                "Failed",
                "error_code":
                settings.ERROR_INVALID_REQUEST,
                "message":
                f"Not a valid request {request.method}"
            })           
    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'Token has expired'}, status=403)
    except jwt.InvalidTokenError:
        return JsonResponse({'error': 'Invalid token'}, status=402)
    except Exception as e:
        return JsonResponse({
            "status": "Failed",
            "error_code": settings.ERROR_ERROR_UNKNOWN,
            "message": f"Unknown Error - {e}"
        })



