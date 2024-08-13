import os
import numpy as np
from pathlib import Path

path = '/home/mist/gll/Pointcept/data/intra/'

for split in range(5):
    sdir = Path(path + 'split_' + str(split))
    sdir.mkdir(exist_ok=True, parents=True)
    
    fl = '/home/mist/gll/IntrA/fileSplit/seg/annSplit_' + str(split) + '.txt'
    with open(fl, 'r') as f:
        for line in f.readlines():
            ad = '/home/mist/gll/IntrA/' + line.split()[0]
            case = ad.split('/')[-1].split('_')[0]
            cdir = sdir / case
            cdir.mkdir(exist_ok=True, parents=True)
            coord = []
            normal = []
            segment = []
            with open(ad, 'r') as points:
                for p in points.readlines():
                    label = int(p.split()[-1])
                    if label > 1:
                        label = 1
                    segment.append([label])
                    coord.append(np.array(p.split()[0:3]).astype(np.float32))
                    normal.append(np.array(p.split()[3:6]).astype(np.float32))          
            np.save(cdir / 'segment.npy',np.array(segment))
            np.save(cdir / 'coord.npy',np.array(coord))
            np.save(cdir / 'normal.npy',np.array(normal))