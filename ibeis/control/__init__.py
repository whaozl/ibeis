# -*- coding: utf-8 -*-
### __init__.py ###
# flake8: noqa
from __future__ import absolute_import, division, print_function

import utool as ut
ut.noinject(__name__, '[ibeis.control.__init__]', DEBUG=False)


from ibeis.control import DBCACHE_SCHEMA
from ibeis.control import DB_SCHEMA
from ibeis.control import IBEISControl
from ibeis.control import SQLDatabaseControl
from ibeis.control import _sql_helpers
from ibeis.control import accessor_decors
import utool
print, print_, printDBG, rrr, profile = utool.inject(
    __name__, '[ibeis.control]')


def reload_subs(verbose=True):
    """ Reloads ibeis.control and submodules """
    rrr(verbose=verbose)
    getattr(DBCACHE_SCHEMA, 'rrr', lambda verbose: None)(verbose=verbose)
    getattr(DB_SCHEMA, 'rrr', lambda verbose: None)(verbose=verbose)
    getattr(IBEISControl, 'rrr', lambda verbose: None)(verbose=verbose)
    getattr(SQLDatabaseControl, 'rrr', lambda verbose: None)(verbose=verbose)
    getattr(_sql_helpers, 'rrr', lambda verbose: None)(verbose=verbose)
    getattr(accessor_decors, 'rrr', lambda verbose: None)(verbose=verbose)
    rrr(verbose=verbose)
rrrr = reload_subs

IMPORT_TUPLES = [
    ('DBCACHE_SCHEMA', None, False),
    ('DB_SCHEMA', None, False),
    ('IBEISControl', None, False),
    ('SQLDatabaseControl', None, False),
    ('_sql_helpers', None, False),
    ('accessor_decors', None, False),
]
"""
Regen Command:
    cd /home/joncrall/code/ibeis/ibeis/control
    makeinit.py -x DBCACHE_SCHEMA_CURRENT DB_SCHEMA_CURRENT _grave_template manual_ibeiscontrol_funcs template_definitions templates _autogen_ibeiscontrol_funcs
"""
# autogenerated __init__.py for: '/home/joncrall/code/ibeis/ibeis/control'
#from __future__ import absolute_import, division, print_function
##from ibeis.control import DB_SCHEMA
##from ibeis.control import IBEISControl
##from ibeis.control import SQLDatabaseControl
##from ibeis.control import _sql_helpers
##from ibeis.control import accessor_decors
#from . import DB_SCHEMA
#from . import IBEISControl
#from . import SQLDatabaseControl
#from . import _sql_helpers
#from . import accessor_decors
#import utool
#print, print_, printDBG, rrr, profile = utool.inject(
#    __name__, '[control]')


#def reload_subs():
#    """ Reloads control and submodules """
#    rrr()
#    getattr(DB_SCHEMA, 'rrr', lambda: None)()
#    getattr(IBEISControl, 'rrr', lambda: None)()
#    getattr(SQLDatabaseControl, 'rrr', lambda: None)()
#    getattr(_sql_helpers, 'rrr', lambda: None)()
#    getattr(accessor_decors, 'rrr', lambda: None)()
#    rrr()
#rrrr = reload_subs

