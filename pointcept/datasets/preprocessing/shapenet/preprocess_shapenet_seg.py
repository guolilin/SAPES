import os
import numpy as np
from pathlib import Path
import json

path = '/home/mist/gll/Pointcept/data/shapenet/'

id2name = dict()
id2seg = dict()
with open(path+'synsetoffset2category.txt', 'r') as f1:
    for l1 in f1.readlines():
        cname = l1.split()[0]
        cid = l1.split()[1]
        id2name[cid] = cname
        id2seg[cid] = set()
        sdir = Path(path + cname + '/train')
        sdir.mkdir(exist_ok=True, parents=True)
        sdir = Path(path + cname + '/test')
        sdir.mkdir(exist_ok=True, parents=True)

with open(path+'train_test_split/shuffled_train_file_list.json', 'r') as f:
    fl = json.load(f)
    for ff in fl:
        cid = ff.split('/')[1]
        case = ff.split('/')[2]
        sdir = Path(path + id2name[cid] + '/train/' + case)
        sdir.mkdir(exist_ok=True, parents=True)
        ad = path + cid + '/points/' + case + '.pts'
        coord = []
        with open(ad, 'r') as points:
            for p in points.readlines():
                coord.append(np.array(p.split()).astype(np.float32))
                
        label = path + cid + '/points_label/' + case + '.seg'
        seg = []
        with open(label, 'r') as points:
            for p in points.readlines():
                sp = int(p.split()[0]) - 1
                id2seg[cid].add(sp)
                seg.append([sp])
        np.save(sdir / 'segment.npy',np.array(seg))
        np.save(sdir / 'coord.npy',np.array(coord))

                
with open(path+'train_test_split/shuffled_test_file_list.json', 'r') as f:
    fl = json.load(f)
    for ff in fl:
        cid = ff.split('/')[1]
        case = ff.split('/')[2]
        sdir = Path(path + id2name[cid] + '/test/' + case)
        sdir.mkdir(exist_ok=True, parents=True)
        ad = path + cid + '/points/' + case + '.pts'
        coord = []
        with open(ad, 'r') as points:
            for p in points.readlines():
                coord.append(np.array(p.split()).astype(np.float32))
                
        label = path + cid + '/points_label/' + case + '.seg'
        seg = []
        with open(label, 'r') as points:
            for p in points.readlines():
                sp = int(p.split()[0]) - 1
                id2seg[cid].add(sp)
                seg.append([sp])
        np.save(sdir / 'segment.npy',np.array(seg))
        np.save(sdir / 'coord.npy',np.array(coord))
