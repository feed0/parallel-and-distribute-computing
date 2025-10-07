import jwt
import datetime


def create_token(user, expireminutes, secretkey):
    creation_date = datetime.datetime.now()
    expiration_date = creation_date + datetime.timedelta(minutes=expireminutes)

    creation_date = creation_date.timestamp()
    expiration_date = expiration_date.timestamp()

    payload = {
        'user': user,
        'iat': creation_date,
        'exp': expiration_date
    }

    try:
        token_encode = jwt.encode(payload,
                                  secretkey,
                                  algorithm="HS256")
    except:
        token_encode = None

    return token_encode




def verify_token(token, secretkey):

    try:
        dec_token = jwt.decode(token,
                               secretkey,
                               algorithms=["HS256"],
                               options={"verify_signature": True})

        if dec_token['exp'] >= datetime.datetime.now().timestamp():
            payload = {
                'user': dec_token['user'],
                'iat': datetime.datetime.fromtimestamp(dec_token['iat']),
                'exp': datetime.datetime.fromtimestamp(dec_token['exp'])
            }
        else:
            payload = None
    except:
        payload = None


    return payload