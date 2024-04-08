from .models import *
import jwt
from datetime import timedelta,datetime
token_my ="mayank212123"

def check_user_exist(email):
    user_info = user_detail.objects.filter(email=email)
    print("ppppppppppppp")
    if user_info.exists():
        return True
    return False

def get_tokens_for_user(user):
    payload = {
    'user_id': user,
    'exp': datetime.utcnow() + timedelta(days=1)
        }   
    # Generate JWT token with the payload and secret key
    token = jwt.encode(payload, token_my, algorithm='HS256')
    
    return token

def validate_jwt_token(request):
    token = request.headers.get('Authorization', None)
    if token:
        try:
            payload = jwt.decode(token, token_my, algorithms=['HS256'])
            request.jwt_payload = payload
            return payload['user_id'], None  # Return user_id and no error
        except jwt.ExpiredSignatureError:
            return None, 'Token has expired'
        except jwt.InvalidTokenError:
            return None, 'Invalid token'
    else:
        return None, 'Token is missing'


def custom_pagination(page, page_size ,data_list):
    final_list = []
    total_data = len(data_list)
    data_remaining = 0
    if page == 1:
        offset = 0
    else:
        off = page * page_size
        offset = off - page_size
    i = 1
    for data in data_list:
        if i > offset and len(final_list) < page_size:
            final_list.append(data)
        else:
            pass
        i += 1
    data_remaining = total_data - offset - len(final_list)
    data_remaining = 0 if data_remaining < 0 else data_remaining
    return final_list, total_data, data_remaining