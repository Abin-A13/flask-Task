
import jwt
from time import time


API_KEY="7FjQ9-asTPap1xpxTHiPGA"
API_SECRET="czetI1r8hlbAyg1znRD9ABYWGqeJypAOjgma"

def generate_token():
    token = jwt.encode({'iss':API_KEY,'exp':time()+5000},API_SECRET,algorithm='HS256')
    return token