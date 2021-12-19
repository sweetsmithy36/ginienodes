from __future__ import absolute_import, unicode_literals

import datetime
import random
import string

today = datetime.date.today()


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def random_number_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))




def unique_number_generator(instance, matnumber=None):
    """
    Generates a unique matnumber generator. converting the username field into a unique mat number
    """
    
    
    if matnumber is not None:
        investor_id = matnumber
    else:
        investor_id = "INV_01293"
        
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(investor_id=investor_id).exists()
    if qs_exists:
        matnumber = "INV_{matnumber}".format(matnumber=random_number_generator(size=6))
        return unique_number_generator(instance, matnumber=matnumber)
    return investor_id



def unique_staff_id(instance, staffid):
    """
    Generate a unique staff id.
    """
    
    school_initials = instance.school.initials
    year = today.year
    
    if staffid is not None:
        staffID = staffid
    else:
        staffID = f"{school_initials}-{year}-STAFF"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(staffID=staffID).exists()
    if qs_exists:
        staffid = "{school_initials}-{year}-{staffid}".format(school_initials=school_initials, year=year, staffid=random_string_generator(size=6))
        return random_string_generator(instance, staffid=staffid)
    return staffID
