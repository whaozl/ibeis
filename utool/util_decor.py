import sys
from functools import wraps
from .util_iter import isiterable
from .util_print import Indenter


IGNORE_EXC_TB = not '--noignore-exctb' in sys.argv


def ignores_exc_tb(func):
    """ decorator that removes other decorators from traceback """
    if IGNORE_EXC_TB:
        @wraps(func)
        def wrapper_ignore_exctb(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                # Code to remove this decorator from traceback
                exc_type, exc_value, exc_traceback = sys.exc_info()
                # Remove two levels to remove this one as well
                raise exc_type, exc_value, exc_traceback.tb_next.tb_next
        return wrapper_ignore_exctb
    else:
        return func


def indent_decor(lbl):
    def indent_decor_outer_wrapper(func):
        @ignores_exc_tb
        @wraps(func)
        def indent_decor_inner_wrapper(*args, **kwargs):
            with Indenter(lbl):
                return func(*args, **kwargs)
        return indent_decor_inner_wrapper
    return indent_decor_outer_wrapper


def indent_func(func):
    @wraps(func)
    @indent_decor('[' + func.func_name + ']')
    @ignores_exc_tb
    def wrapper_indent_func(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper_indent_func


def accepts_scalar_input(func):
    '''
    accepts_scalar_input is a decorator which expects to be used on class methods.
    It lets the user pass either a vector or a scalar to a function, as long as
    the function treats everything like a vector. Input and output is sanatized
    to the user expected format on return.
    '''
    @ignores_exc_tb
    @wraps(func)
    def wrapper_scalar_input(self, input_, *args, **kwargs):
        is_scalar = not isiterable(input_)
        if is_scalar:
            iter_input = (input_,)
        else:
            iter_input = input_
        result = func(self, iter_input, *args, **kwargs)
        if is_scalar:
            result = result[0]
        return result
    return wrapper_scalar_input


def accepts_scalar_input_vector_output(func):
    '''
    accepts_scalar_input is a decorator which expects to be used on class
    methods.  It lets the user pass either a vector or a scalar to a function,
    as long as the function treats everything like a vector. Input and output is
    sanatized to the user expected format on return.
    '''
    @ignores_exc_tb
    @wraps(func)
    def wrapper_vec_output(self, input_, *args, **kwargs):
        is_scalar = not isiterable(input_)
        if is_scalar:
            iter_input = (input_,)
        else:
            iter_input = input_
        result = func(self, iter_input, *args, **kwargs)
        if is_scalar:
            if len(result) != 0:
                result = result[0]
        return result
    return wrapper_vec_output
