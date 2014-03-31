#!/usr/bin/env python
# TODO: ADD COPYRIGHT TAG
from __future__ import print_function, division
#-----
TEST_NAME = 'TEST_GUI_SELECTION'
#-----
import __testing__
import multiprocessing
import utool
from ibeis.dev import params
print, print_, printDBG, rrr, profile = utool.inject(__name__, '[%s]' % TEST_NAME)
printTEST = __testing__.printTEST

RUNGUI = utool.get_flag('--gui')


@__testing__.testcontext
def TEST_GUI_SELECTION():
    # Create a HotSpotter API (hs) and GUI backend (back)
    main_locals = __testing__.main()
    ibs = main_locals['ibs']    # IBEIS Control  # NOQA
    back = main_locals['back']  # IBEIS GUI backend

    dbdir = params.db_to_dbdir('testdb')

    valid_gids = ibs.get_valid_gids()
    valid_rids = ibs.get_valid_rids()

    print(' * len(valid_gids) = %r' % len(valid_gids))
    print(' * len(valid_rids) = %r' % len(valid_rids))
    assert len(valid_gids) > 0, 'database images cannot be empty for test'

    gid = valid_gids[0]
    rid_list = ibs.get_rids_in_gids(gid)
    rid = rid_list[-1]
    back.select_gid(gid, sel_rids=[rid])

    printTEST('[TEST] TEST SELECT dbdir=%r' % dbdir)

    __testing__.main_loop(main_locals, rungui=RUNGUI)


TEST_GUI_SELECTION.func_name = TEST_NAME


if __name__ == '__main__':
    multiprocessing.freeze_support()  # For windows
    TEST_GUI_SELECTION()
