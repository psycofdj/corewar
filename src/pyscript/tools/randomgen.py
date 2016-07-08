# -*- coding: utf-8
#---------------------------------------------------------------------------#

import string
import random

#---------------------------------------------------------------------------#

def gen_password(p_size = 8, p_chars = string.ascii_uppercase + string.ascii_lowercase + string.digits):
    try:
        return ''.join(random.choice(p_chars) for x in range(p_size))
    except:
        raise Exception(str(dir(random)))

