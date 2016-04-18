# -*- coding: utf-8 -*-
# Autogenerated on 15:42:03 2016/04/18
# flake8: noqa
from __future__ import absolute_import, division, print_function, unicode_literals
from ibeis.algo.detect import grabmodels
from ibeis.algo.detect import randomforest
from ibeis.algo.detect import yolo
from ibeis.algo.detect import background
from ibeis.algo.detect import classifier
from ibeis.algo.detect import labeler
from ibeis.algo.detect import orientation
from ibeis.algo.detect import saliency
import utool
print, rrr, profile = utool.inject2(__name__, '[ibeis.algo.detect]')


def reassign_submodule_attributes(verbose=True):
    """
    why reloading all the modules doesnt do this I don't know
    """
    import sys
    if verbose and '--quiet' not in sys.argv:
        print('dev reimport')
    # Self import
    import ibeis.algo.detect
    # Implicit reassignment.
    seen_ = set([])
    for tup in IMPORT_TUPLES:
        if len(tup) > 2 and tup[2]:
            continue  # dont import package names
        submodname, fromimports = tup[0:2]
        submod = getattr(ibeis.algo.detect, submodname)
        for attr in dir(submod):
            if attr.startswith('_'):
                continue
            if attr in seen_:
                # This just holds off bad behavior
                # but it does mimic normal util_import behavior
                # which is good
                continue
            seen_.add(attr)
            setattr(ibeis.algo.detect, attr, getattr(submod, attr))


def reload_subs(verbose=True):
    """ Reloads ibeis.algo.detect and submodules """
    if verbose:
        print('Reloading submodules')
    rrr(verbose=verbose)
    def wrap_fbrrr(mod):
        def fbrrr(*args, **kwargs):
            """ fallback reload """
            if verbose:
                print('No fallback relaod for mod=%r' % (mod,))
            # Breaks ut.Pref (which should be depricated anyway)
            # import imp
            # imp.reload(mod)
        return fbrrr
    def get_rrr(mod):
        if hasattr(mod, 'rrr'):
            return mod.rrr
        else:
            return wrap_fbrrr(mod)
    def get_reload_subs(mod):
        return getattr(mod, 'reload_subs', wrap_fbrrr(mod))
    get_rrr(grabmodels)(verbose=verbose)
    get_rrr(randomforest)(verbose=verbose)
    get_rrr(yolo)(verbose=verbose)
    get_reload_subs(background)(verbose=verbose)
    get_reload_subs(classifier)(verbose=verbose)
    get_reload_subs(labeler)(verbose=verbose)
    get_reload_subs(orientation)(verbose=verbose)
    get_reload_subs(saliency)(verbose=verbose)
    rrr(verbose=verbose)
    try:
        # hackish way of propogating up the new reloaded submodule attributes
        reassign_submodule_attributes(verbose=verbose)
    except Exception as ex:
        print(ex)
rrrr = reload_subs

IMPORT_TUPLES = [
    ('grabmodels', None),
    ('randomforest', None),
    ('yolo', None),
    ('background', None, True),
    ('classifier', None, True),
    ('labeler', None, True),
    ('orientation', None, True),
    ('saliency', None, True),
]
"""
Regen Command:
    cd /Users/bluemellophone/code/ibeis/ibeis/algo/detect
    makeinit.py --modname=ibeis.algo.detect
"""