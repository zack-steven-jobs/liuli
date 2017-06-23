'''
Created on 2012-10-23

@author: qpwang
'''
import os
import random
from settings import FSS, FSS1, IS_DEBUG
from util import get_str_md5
from settings import DEP_MODE_DIANDIAN_INTERNATIONAL, DEP_MODE


def get_path(vol_id, key_url, suffix, root=None, mkdir=True):
    root = FSS.get(vol_id) or FSS1.get(vol_id)
    vol_id = 'vol%s' % vol_id
    md5 = get_str_md5(key_url)
    dir1 = md5[:2]
    dir2 = md5[2:4]
    name = '%s.%s' % (md5, suffix)
    if not os.path.exists(os.path.join(root, vol_id, dir1, dir2)) and mkdir:
        os.makedirs(os.path.join(root, vol_id, dir1, dir2))
    return os.path.join(root, vol_id, dir1, dir2, name)


def get_vol(source, free_disk=20 * 1024 * 1024):
    if DEP_MODE == DEP_MODE_DIANDIAN_INTERNATIONAL:
        return FSS.keys()[0]
    if source == 'ipa.91.com':
        vol_list = FSS1
    else:
        vol_list = FSS.items()
    vol_list = [x for x in vol_list]
    random.shuffle(vol_list)
    for vol, root in vol_list:
        if IS_DEBUG:
            return vol
        root = root[:-1] if root[-1] == '/' else root
        command_str = 'df |grep " %s"|tr -s " "|cut -d " " -f4' % root
        usable = os.popen(command_str).read().strip()
        if not usable or int(usable) < free_disk:
            continue
        else:
            print "Returned Vol=%s; root=%s" % (vol, root)
            return vol


def size(vol_id, key_url, suffix):
    path = get_path(vol_id, key_url, suffix)
    info = os.stat(path)
    return info.st_size

