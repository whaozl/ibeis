# -*- coding: utf-8 -*-
"""
This module defines helper functions to access common input needed to test many
functions. These functions give a rich command line interface to specifically
select subsets of annotations, pipeline configurations, and other filters.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import utool as ut
import six  # NOQA
from ibeis.init import old_main_helpers
(print, print_, printDBG, rrr, profile) = ut.inject(__name__, '[main_helpers]')


# DEPRICATE
get_test_daids = old_main_helpers.get_test_daids
get_test_qaids = old_main_helpers.get_test_qaids

VERB_TESTDATA, VERYVERB_TESTDATA = ut.get_verbflag('testdata', 'td')
VERYVERB_MAIN_HELPERS = VERYVERB_TESTDATA
VERB_MAIN_HELPERS = VERB_TESTDATA

#VERB_TESTDATA = ut.get_argflag(('--verbose-testdata', '--verbtd')) or VERYVERB_TESTDATA
#VERB_MAIN_HELPERS = ut.get_argflag(('--verbose-main-helpers', '--verbmhelp'))
#or ut.VERBOSE or VERB_TESTDATA


def testdata_pipecfg(t=['default']):
    r"""
    Returns:
        dict: pcfgdict

    CommandLine:
        python -m ibeis.init.main_helpers --exec-testdata_pipecfg
        python -m ibeis.init.main_helpers --exec-testdata_pipecfg -t default:AI=False

    Example:
        >>> # ENABLE_DOCTEST
        >>> from ibeis.init.main_helpers import *  # NOQA
        >>> pcfgdict = testdata_pipecfg()
        >>> result = ('pcfgdict = %s' % (ut.dict_str(pcfgdict),))
        >>> print(result)
    """
    from ibeis.expt import experiment_helpers
    test_cfg_name_list = ut.get_argval('-t', type_=list, default=t)
    pcfgdict_list = experiment_helpers.get_pipecfg_list(test_cfg_name_list)[0]
    assert len(pcfgdict_list) == 1, 'can only specify one pipeline config here'
    pcfgdict = pcfgdict_list[0]
    return pcfgdict


def testdata_filtcfg(default=None):
    from ibeis.expt import cfghelpers
    if default is None:
        default = ['']
    filt_cfg = cfghelpers.parse_argv_cfg(('--filt', '-f'), default=default)[0]
    return filt_cfg


def testdata_qreq_(t=None, **kwargs):
    if t is None:
        t = ['default']
    ibs, qaids, daids = testdata_expanded_aids(**kwargs)
    pcfgdict = testdata_pipecfg(t=t)
    qreq_ = ibs.new_query_request(qaids, daids, cfgdict=pcfgdict)
    return qreq_


def testdata_cm(defaultdb=None, default_qaids=None):
    r"""
    CommandLine:
        python -m ibeis.init.main_helpers --test-testdata_cm
        python -m ibeis.init.main_helpers --test-testdata_cm --show

    Example:
        >>> # ENABLE_DOCTEST
        >>> from ibeis.init.main_helpers import *  # NOQA
        >>> cm, qreq_ = testdata_cm()
        >>> cm.print_csv(ibs=qreq_.ibs)
        >>> ut.quit_if_noshow()
        >>> cm.show_single_annotmatch(qreq_, 2)
        >>> ut.show_if_requested()
    """
    qreq_ = testdata_qreq_(defaultdb=defaultdb, default_qaids=default_qaids)
    qaids = qreq_.get_external_qaids()
    print('qaids = %r' % (qaids,))
    assert len(qaids) == 1, 'only one qaid for this tests, qaids=%r' % (qaids,)
    cm = qreq_.ibs.query_chips(qreq_=qreq_, return_cm=True)[0]
    return cm, qreq_


def testdata_cmlist(defaultdb=None, default_qaids=None):
    qreq_ = testdata_qreq_(defaultdb=defaultdb, default_qaids=default_qaids)
    cm_list = qreq_.ibs.query_chips(qreq_=qreq_, return_cm=True)
    return cm_list, qreq_


def testdata_expts(defaultdb='testdb1',
                   default_acfgstr_name_list=['default:qindex=0:10:4,dindex=0:20'],
                   default_test_cfg_name_list=['default'],
                   a=None,
                   t=None,
                   qaid_override=None,
                   ):
    """
    Command line interface to quickly get testdata for test_results
    """
    import ibeis
    from ibeis.expt import experiment_harness
    from ibeis.expt import test_result
    if a is not None:
        default_acfgstr_name_list = a
    if t is not None:
        default_test_cfg_name_list = t

    if isinstance(default_acfgstr_name_list, six.string_types):
        default_acfgstr_name_list = [default_acfgstr_name_list]
    if isinstance(default_test_cfg_name_list, six.string_types):
        default_test_cfg_name_list = [default_test_cfg_name_list]

    #from ibeis.expt import experiment_helpers
    ibs = ibeis.opendb(defaultdb=defaultdb)
    acfg_name_list = ut.get_argval(('--aidcfg', '--acfg', '-a'), type_=list,
                                   default=default_acfgstr_name_list)
    test_cfg_name_list = ut.get_argval('-t', type_=list, default=default_test_cfg_name_list)
    testres_list = experiment_harness.run_test_configurations2(
        ibs, acfg_name_list, test_cfg_name_list, qaid_override=qaid_override)
    testres = test_result.combine_testres_list(ibs, testres_list)
    return ibs, testres
    #return ibs, testres_list


def testdata_expanded_aids(default_qaids=None, a=None, defaultdb=None,
                           ibs=None, verbose=False, return_annot_info=False):
    r"""
    Args:
        default_qaids (list): (default = [1])
        default_daids (str): (default = 'all')
        defaultdb (str): (default = 'testdb1')
        ibs (IBEISController):  ibeis controller object(default = None)
        verbose (bool):  verbosity flag(default = False)
        return_annot_info (bool): (default = False)

    Returns:
        ibs, qaid_list, daid_list, annot_info:

    CommandLine:
        python -m ibeis.init.main_helpers --exec-testdata_expanded_aids
        python -m ibeis.init.main_helpers --exec-testdata_expanded_aids --db PZ_MTEST --acfg default:index=0:25 --verbose-testdata
        python -m ibeis.init.main_helpers --exec-testdata_expanded_aids --db GZ_ALL --acfg ctrl --verbose-testdata

    Example:
        >>> # ENABLE_DOCTEST
        >>> from ibeis.init.main_helpers import *  # NOQA
        >>> import ibeis
        >>> from ibeis.expt import annotation_configs
        >>> ibs, qaid_list, daid_list, aidcfg = testdata_expanded_aids(return_annot_info=True)
        >>> print('Printing annot config')
        >>> annotation_configs.print_acfg(aidcfg)
        >>> print('Printing annotconfig stats')
        >>> #print('qaid_list = %r' % (np.array(qaid_list),))
        >>> ibs.get_annotconfig_stats(qaid_list, daid_list)
        >>> print('Combined annotconfig stats')
        >>> ibs.print_annot_stats(qaid_list + daid_list, yawtext_isect=True)
    """
    print('[testdata_expanded_aids] Getting test annot configs')
    if default_qaids is None:
        default_qaids = [1]
    if defaultdb is None:
        defaultdb = 'testdb1'
    import ibeis
    if ibs is None:
        ibs = ibeis.opendb(defaultdb=defaultdb)
    # TODO: rectify command line with function arguments
    from ibeis.expt import experiment_helpers
    _specified2 = True
    if a is None:
        _specified2 = False
        a = ['default']
    if isinstance(a, six.string_types):
        a = [a]
    aidcfg_name_list, _specified = ut.get_argval(('--aidcfg', '--acfg', '-a'),
                                                 type_=list,
                                                 default=a,
                                                 return_specified=True)

    acfg_list, expanded_aids_list = experiment_helpers.get_annotcfg_list(ibs, aidcfg_name_list)

    #aidcfg = old_main_helpers.get_commandline_aidcfg()
    assert len(acfg_list) == 1, (
        ('multiple acfgs specified, but this function'
         'is built to return only 1. len(acfg_list)=%r') %
        (len(acfg_list),))
    aidcfg = acfg_list[0]

    qaid_list, daid_list = expanded_aids_list[0]

    if not (_specified or _specified2) and default_qaids is not None:
        # hack
        qaid_list = default_qaids

    #ibs.get_annotconfig_stats(qaid_list, daid_list)

    if ut.VERYVERBOSE:
        ibs.print_annotconfig_stats(qaid_list, daid_list)
        #ibeis.other.dbinfo.print_qd_info(ibs, qaid_list, daid_list, verbose=True)
    if return_annot_info:
        return ibs, qaid_list, daid_list, aidcfg
    else:
        return ibs, qaid_list, daid_list


@profile
def testdata_aids(defaultdb=None, a=None, adefault='default', ibs=None, return_acfg=False):
    r"""
    CommandLine:
        python -m ibeis --tf testdata_aids --verbtd --db PZ_ViewPoints
        python -m ibeis --tf testdata_aids --verbtd --db NNP_Master3 -a is_known=True,view_pername='#primary>0&#primary1>=1'
        python -m ibeis --tf testdata_aids --verbtd --db PZ_Master1 -a default:is_known=True,view_pername='#primary>0&#primary1>=1'
        python -m ibeis --tf testdata_aids --verbtd --db PZ_Master1 -a default:species=primary,minqual=ok --verbtd
    python -m ibeis.other.dbinfo --test-latex_dbstats --dblist

    CommandLine:
        python -m ibeis.init.main_helpers --exec-testdata_aids --show

    Example:
        >>> # ENABLE_DOCTEST
        >>> from ibeis.init.main_helpers import *  # NOQA
        >>> from ibeis.expt import annotation_configs
        >>> import ibeis
        >>> #ibs = ibeis.opendb(defaultdb='PZ_ViewPoints')
        >>> ibs = ibeis.opendb(defaultdb='testdb1')
        >>> a = None
        >>> adefault = 'default:is_known=True'
        >>> aids, aidcfg = testdata_aids(ibs=ibs, a=a, adefault=adefault, return_acfg=True)
        >>> print('\n RESULT:')
        >>> annotation_configs.print_acfg(aidcfg, aids, ibs, per_name_vpedge=None)
    """
    from ibeis.init import filter_annots
    from ibeis.expt import annotation_configs
    from ibeis.expt import cfghelpers
    import ibeis
    if a is None:
        a = adefault
    a = ut.get_argval(('--aidcfg', '--acfg', '-a'), type_=str, default=a)
    return_ibs = False
    if ibs is None:
        return_ibs = True
        if defaultdb is None:
            defaultdb = 'testdb1'
        ibs = ibeis.opendb(defaultdb=defaultdb)
    named_defaults_dict = ut.dict_take(annotation_configs.__dict__,
                                       annotation_configs.TEST_NAMES)
    named_qcfg_defaults = dict(zip(annotation_configs.TEST_NAMES,
                                   ut.get_list_column(named_defaults_dict, 'qcfg')))
    # Allow command line override
    aids = ut.get_argval(('--aid', '--aids'), type_=list, default=None)
    aidcfg = None
    if aids is None:
        #base_cfg = annotation_configs.single_default
        aidcfg_combo_list = cfghelpers.parse_cfgstr_list2([a], named_qcfg_defaults, 'acfg', annotation_configs.ALIAS_KEYS, expand_nested=False, is_nestedcfgtype=False)
        #aidcfg_combo = cfghelpers.customize_base_cfg('default', cfgstr_options,
        #                                             base_cfg, 'aids',
        #                                             alias_keys=annotation_configs.ALIAS_KEYS)
        aidcfg_combo = aidcfg_combo_list[0]
        if len(aidcfg_combo_list) != 1:
            raise AssertionError('Error: combinations not handled for single cfg setting')
        if len(aidcfg_combo) != 1:
            raise AssertionError('Error: combinations not handled for single cfg setting')
        aidcfg = aidcfg_combo[0]
        aids = filter_annots.expand_single_acfg(ibs, aidcfg)
    if return_ibs:
        return ibs, aids
    if return_acfg:
        return aids, aidcfg
    else:
        return aids


if __name__ == '__main__':
    """
    CommandLine:
        python -m ibeis.init.main_helpers
        python -m ibeis.init.main_helpers --allexamples
        python -m ibeis.init.main_helpers --allexamples --noface --nosrc
    """
    import multiprocessing
    multiprocessing.freeze_support()  # for win32
    import utool as ut  # NOQA
    ut.doctest_funcs()
