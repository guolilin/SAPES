import os
import numpy as np
from pathlib import Path

oripath = '/home/mist/gll/hsz_Pointcept/data/IntrA_cls/'
tarpath = '/home/mist/gll/Pointcept/data/intra/'

# anpath = Path(tarpath + 'aneurysm')
# anpath.mkdir(exist_ok=True, parents=True)
# vepath = Path(tarpath + 'vessel')
# vepath.mkdir(exist_ok=True, parents=True)

# ann_count = 1
# neg_count = 1
# for split in range(5):
#     aflist = oripath + 'fileSplit/cls/ann_clsSplit_' + str(split) + '.txt'
#     nflist = oripath + 'fileSplit/cls/negSplit_' + str(split) + '.txt'
#     newlist = open(tarpath + 'intra_split_' + str(split) + '.txt', 'w')
#     with open(aflist, 'r') as fl:
#         for f in fl.readlines():                   
#             output_file_name = f'aneurysm_{ann_count:04d}.txt'  
#             output_file_path = anpath / output_file_name           
#             ad_path = oripath + f.split()[0]
#             with open(ad_path, 'r') as ad_file, open(output_file_path, 'w') as output_file:  
#                 for p_line in ad_file:  
#                     parts = p_line.strip().split()[:6]  
#                     output_file.write(','.join(parts) + '\n')
#             newlist.write(output_file_name + '\n')
#             ann_count += 1
            
#     with open(nflist, 'r') as fl:
#         for f in fl.readlines():                   
#             output_file_name = f'vessel_{neg_count:04d}.txt'  
#             output_file_path = vepath / output_file_name           
#             ad_path = oripath + f.split()[0]
#             with open(ad_path, 'r') as ad_file, open(output_file_path, 'w') as output_file:  
#                 for p_line in ad_file:  
#                     parts = p_line.strip().split()[:6]  
#                     output_file.write(','.join(parts) + '\n')
#             newlist.write(output_file_name + '\n')
#             neg_count += 1
#     newlist.close()

for split in range(5):
    with open(tarpath + 'intra_fold_' + str(split) + '_train.txt', 'w') as trf:
        for i in range(5):
            if i == 4 - split:
                continue
            with open(tarpath + 'intra_split_' + str(i) + '.txt', 'r') as fl:
                for f in fl.readlines():
                    trf.write(f.split()[0].split('.txt')[0] + '\n')
                
    with open(tarpath + 'intra_fold_' + str(split) + '_test.txt', 'w') as tef:   
        with open(tarpath + 'intra_split_' + str(4 - split) + '.txt', 'r') as fl:
            for f in fl.readlines():
                tef.write(f.split()[0].split('.txt')[0] + '\n')
