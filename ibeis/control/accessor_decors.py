from __future__ import absolute_import, division, print_function
import utool
print, print_, printDBG, rrr, profile = utool.inject(__name__, '[decor]')

#
#-----------------
# IBEIS DECORATORS
#-----------------


# DECORATORS::ADDER


def adder(func):
    @utool.indent_func
    @utool.ignores_exc_tb
    @utool.wraps(func)
    def adder_wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return adder_wrapper


# DECORATORS::SETTER

def setter(func):
    @utool.indent_func
    @utool.ignores_exc_tb
    @utool.wraps(func)
    def adder_wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return adder_wrapper


# DECORATORS::GETTER

def getter(func):
    """ Getter decorator for functions which takes as the first input a unique
    id list and returns a heterogeous list of values """
    @utool.accepts_scalar_input
    @utool.indent_func
    @utool.ignores_exc_tb
    @utool.wraps(func)
    def getter_wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return getter_wrapper


def getter_vector_output(func):
    """ Getter decorator for functions which takes as the first input a unique
    id list and returns a homogenous list of values """
    @utool.accepts_scalar_input_vector_output
    @utool.indent_func
    @utool.ignores_exc_tb
    @utool.wraps(func)
    def getter_vector_wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return getter_vector_wrapper


def getter_numpy(func):
    """ Getter decorator for functions which takes as the first input a unique
    id list and returns a heterogeous list of values """
    getter_func = getter(func)
    @utool.accepts_numpy
    @utool.ignores_exc_tb
    @utool.wraps(func)
    def getter_numpy_wrapper(*args, **kwargs):
        return getter_func(*args, **kwargs)
    return getter_numpy_wrapper


def getter_numpy_vector_output(func):
    """ Getter decorator for functions which takes as the first input a unique
    id list and returns a heterogeous list of values """
    getter_func = getter_vector_output(func)
    @utool.accepts_numpy
    @utool.ignores_exc_tb
    def getter_numpy_vector_wrapper(*args, **kwargs):
        return getter_func(*args, **kwargs)
    return getter_numpy_vector_wrapper


def getter_general(func):
    """ Getter decorator for functions which has no gaurentees """
    @utool.indent_func
    @utool.ignores_exc_tb
    @utool.wraps(func)
    def getter_general_wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return getter_general_wrapper


# DECORATORS::DELETER

def deleter(func):
    @utool.indent_func
    @utool.ignores_exc_tb
    @utool.wraps(func)
    def adder_wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return adder_wrapper
