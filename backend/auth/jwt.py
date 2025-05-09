import os
from dotenv import load_dotenv
from datetime import timezone, datetime, timedelta
from typing import Literal
from flask import make_response, jsonify, request, g
from jwt.exceptions import ExpiredSignatureError
import jwt
from ..Schema import Users, db
load_dotenv()


def encode(username:str, type:Literal['ACCESS', 'REFRESH'])->str:
    """
    Generate (encode and sign) a JWT.

    Args:
        username: The user identifier to embed as the token’s subject (“sub” claim).
        token_type: Kind of token being generated — either `"ACCESS"` or `"REFRESH"`.

    Returns:
        The compact JWT string.
    """
    #Checking which token they need, and setting expiration time
    key = os.getenv(f'{type.upper()}_TOKEN_SECRET')
    if type.upper() == 'ACCESS': 
        expiresIn = 30
    else:
        expiresIn = 24*60*60
    #creating and sending token
    return jwt.encode({
        "username": username,
        'exp': datetime.now(tz=timezone.utc) + timedelta(seconds=expiresIn)
    }, key, algorithm='HS256')


def verify():
    """
    Verifies that a user's Access Token is valid

    Requires:
        Request to inlclude Authorization Header.
    
    Returns:
        None | Response in case of an error
    """
    #Getting the data
    req = request.headers.get('Authorization')
    if not req:
        return jsonify({"message": 'missing required field: authorization'}), 401
    authHeader = req.split(' ')[1]
    try:
        #Checking if it's valid, and adding to g
        res = jwt.decode(authHeader, os.getenv('ACCESS_TOKEN_SECRET'), algorithms='HS256', options={'require':['exp', 'username'], 'verify_exp':'verify_signature'})
        g.username = res['username']
        return None
    except ExpiredSignatureError:
        #In case of timing out
        return make_response(jsonify({'message': 'access token has timed out'}), 403)
    except Exception as e:
        #In case of tampering
        return make_response(jsonify({'message': 'authHeader was tampered with', 'error': str(e)}), 403)

def clean_up_jwt(username:str):
    """
    for the user with username = username, removes any jwt that has expired. 

    Requires:
        username (string):
            The username, the user has to exist in the database. 
    
    Returns:
        None - But you should call db.session.commit() after it. 
    """
    user = Users.query.filter_by(username=username).first()
    if not user:
        raise LookupError(f"{username} is not in the database")
    for rt in user.refresh_tokens:
        try:
            jwt.decode(rt.refresh_token_string, os.getenv('REFRESH_TOKEN_SECRET'), algorithms='HS256', options={'require':['exp', 'username'], 'verify_exp':'verify_signature'})
        except ExpiredSignatureError:
            db.session.delete(rt)
        except Exception as e:
            raise RuntimeError(f"token with {rt.id} has been tampered with in the database.")