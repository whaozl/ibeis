from __future__ import absolute_import, division, print_function
# Standard
from itertools import izip, chain, imap
import sys
# Science
import numpy as np
# UTool
import utool
# VTool
import vtool.nearest_neighbors as nntool
(print, print_, printDBG, rrr, profile) = utool.inject(
    __name__, '[nnindex]', DEBUG=False)

NOCACHE_FLANN = '--nocache-flann' in sys.argv


@utool.indent_func('[get_flann_cfgstr]')
def get_flann_cfgstr(ibs, aid_list):
    feat_cfgstr   = ibs.cfg.feat_cfg.get_cfgstr()
    sample_cfgstr = utool.hashstr_arr(aid_list, 'daids')
    cfgstr = '_' + sample_cfgstr + feat_cfgstr
    return cfgstr


@utool.indent_func('[agg_desc]')
def aggregate_descriptors(ibs, aid_list):
    """ Aggregates descriptors with inverted information
     Return agg_index to(2) -> desc (descriptor)
                               aid (annotation rowid)
                               fx (feature index w.r.t. aid)
    """
    print('[nn] stacking descriptors from %d annotations' % len(aid_list))
    desc_list = ibs.get_annot_desc(aid_list)
    # Build inverted index of (aid, fx) pairs
    aid_nFeat_iter = izip(aid_list, imap(len, desc_list))
    nFeat_iter = imap(len, desc_list)
    # generate aid inverted index for each feature in each annotation
    _ax2_aid = ([aid] * nFeat for (aid, nFeat) in aid_nFeat_iter)
    # generate featx inverted index for each feature in each annotation
    _ax2_fx  = (xrange(nFeat) for nFeat in nFeat_iter)
    # Flatten generators into the inverted index
    ax2_aid = np.array(list(chain.from_iterable(_ax2_aid)))
    ax2_fx  = np.array(list(chain.from_iterable(_ax2_fx)))
    try:
        # Stack descriptors into numpy array corresponding to inverted inexed
        ax2_desc = np.vstack(desc_list)
        print('[nn] stacked %d descriptors from %d annotations' % (len(ax2_desc), len(aid_list)))
    except MemoryError as ex:
        utool.printex(ex, 'cannot build inverted index', '[!memerror]')
        raise
    return ax2_desc, ax2_aid, ax2_fx


@utool.indent_func('[build_invx]')
def build_flann_inverted_index(ibs, aid_list):
    """
    Build a inverted index (using FLANN)
    """
    try:
        ax2_desc, ax2_aid, ax2_fx = aggregate_descriptors(ibs, aid_list)
    except Exception as ex:
        intostr = ibs.get_infostr()  # NOQA
        utool.printex(ex, 'cannot build inverted index', '[!build_invx]',
                      ['infostr'])
        raise
    # Build/Load the flann index
    flann_cfgstr = get_flann_cfgstr(ibs, aid_list)
    flann_params = {'algorithm': 'kdtree', 'trees': 4}
    precomp_kwargs = {'cache_dir': ibs.get_flann_cachedir(),
                      'cfgstr': flann_cfgstr,
                      'flann_params': flann_params,
                      'force_recompute': NOCACHE_FLANN}
    flann = nntool.flann_cache(ax2_desc, **precomp_kwargs)
    return ax2_desc, ax2_aid, ax2_fx, flann


class NNIndex(object):
    """ Nearest Neighbor (FLANN) Index Class """
    def __init__(nn_index, ibs, daid_list):
        print('[nnindex] building NNIndex object')
        try:
            if len(daid_list) == 0:
                msg = ('len(dir_list) == 0\n'
                       'Cannot build inverted index without features!')
                raise AssertionError(msg)
            ax2_desc, ax2_aid, ax2_fx, flann = build_flann_inverted_index(ibs, daid_list)
        except Exception as ex:
            dbname = ibs.get_dbname()  # NOQA
            num_images = ibs.get_num_images()  # NOQA
            num_annotations = ibs.get_num_annotations()      # NOQA
            num_names = ibs.get_num_names()    # NOQA
            utool.printex(ex, '', '[nn]', locals().keys())
            raise
        # Agg Data
        nn_index.ax2_aid  = ax2_aid
        nn_index.ax2_fx   = ax2_fx
        nn_index.ax2_data = ax2_desc
        # Grab the keypoints names and image ids before query time
        #nn_index.rx2_kpts = ibs.get_annot_kpts(daid_list)
        #nn_index.rx2_gid  = ibs.get_annot_gids(daid_list)
        #nn_index.rx2_nid  = ibs.get_annot_nids(daid_list)
        nn_index.flann = flann

    def __getstate__(nn_index):
        """ This class it not pickleable """
        printDBG('get state NNIndex')
        return None

    #def __del__(nn_index):
    #    """ Ensure flann is propertly removed """
    #    printDBG('deleting NNIndex')
    #    if getattr(nn_index, 'flann', None) is not None:
    #        nn_index.flann.delete_index()
    #        #del nn_index.flann
    #    nn_index.flann = None

    def nn_index2(nn_index, qreq, qfx2_desc):
        """ return nearest neighbors from this data_index's flann object """
        flann   = nn_index.flann
        K       = qreq.cfg.nn_cfg.K
        Knorm   = qreq.cfg.nn_cfg.Knorm
        checks  = qreq.cfg.nn_cfg.checks

        (qfx2_dx, qfx2_dist) = flann.nn_index(qfx2_desc, K + Knorm, checks=checks)
        qfx2_aid = nn_index.ax2_aid[qfx2_dx]
        qfx2_fx  = nn_index.ax2_fx[qfx2_dx]
        return qfx2_aid, qfx2_fx, qfx2_dist, K, Knorm
