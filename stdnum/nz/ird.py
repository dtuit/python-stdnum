from stdnum.exceptions import *
from stdnum.util import clean
import string 
import re

"""
NZ IRD numbers

https://www.ird.govt.nz/resources/d/8/d8e49dce-1bda-4875-8acf-9ebf908c6e17/rwt-nrwt-spec-2014.pdf

"""

def compact(number):
    return re.sub('[^0-9]','', number)    

def checksum(number):
    weights = [3, 2, 7, 6, 5, 4, 3, 2]
    weights2 = [7, 4, 3, 2, 5, 2, 7, 6]    
    
    def calc_cksum(weights, number):
        r = sum( w *int(n) for w, n in zip(weights, number)) % 11
        if r == 0:
            return 0
        else:
            return 11 - r
    
    csum = calc_cksum(weights, number)
    if csum < 10:
        return csum
    else:
        csum = calc_cksum(weights2, number)
        if csum < 10:
            return csum
        else:
            raise InvalidChecksum()

def validate(number):
    num_str = compact(number)
    if not 8 <= len(num_str) <= 9:
        raise InvalidLength()
    if 10**7 < int(num_str) < 15*10**7:

        if len(num_str) == 8:
            num_str = '0' + num_str
        try:
            chk = checksum(num_str[0:-1])
            if chk == int(num_str[-1]):
                return num_str
        except InvalidChecksum:
            raise
    else:
        raise InvalidLength() 

def is_valid(number):
    try:
        return bool(validate(number))
    except ValidationError:
        return False

if __name__ == "__main__":
    irds = ['109 682 624','63 178 640', '63-563-803', '123456789', '24-882-403']
    y = [is_valid(x) for x in irds]
    print(y)