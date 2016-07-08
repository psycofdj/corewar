# -*- coding: utf-8
#---------------------------------------------------------------------------#

def is_array(p_obj):
    return (type([]) == type(p_obj))

def to_array(p_obj):
    if not is_array(p_obj):
        p_obj = [p_obj]
    return p_obj

def is_int(p_str):
    try:
        l_num = int(p_str)
        return True
    except ValueError:
        return False

def is_bool(p_value):
    return (type(True) == type(p_value))
