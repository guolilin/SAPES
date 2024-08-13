_base_ = ["../_base_/default_runtime.py"]
# misc custom setting
batch_size = 32  # bs: total bs in all gpus
num_worker = 16
batch_size_val = 8
empty_cache = False
enable_amp = False

# model settings
model = dict(
    type="DefaultClassifier",
    num_classes=2,
    backbone_embed_dim=512,
    backbone=dict(
        type="PT-v3m1",
        in_channels=6,
        order=("z", "z-trans", "hilbert", "hilbert-trans"),
        stride=(2, 2, 2, 2),
        enc_depths=(2, 2, 2, 6, 2),
        enc_channels=(32, 64, 128, 256, 512),
        enc_num_head=(2, 4, 8, 16, 32),
        enc_patch_size=(1024, 1024, 1024, 1024, 1024),
        dec_depths=(2, 2, 2, 2),
        dec_channels=(64, 64, 128, 256),
        dec_num_head=(4, 4, 8, 16),
        dec_patch_size=(1024, 1024, 1024, 1024),
        mlp_ratio=4,
        qkv_bias=True,
        qk_scale=None,
        attn_drop=0.0,
        proj_drop=0.0,
        drop_path=0.3,
        shuffle_orders=True,
        pre_norm=True,
        enable_rpe=False,
        enable_flash=False,
        upcast_attention=False,
        upcast_softmax=False,
        cls_mode=True,
        pdnorm_bn=False,
        pdnorm_ln=False,
        pdnorm_decouple=True,
        pdnorm_adaptive=False,
        pdnorm_affine=True,
        pdnorm_conditions=("ScanNet", "S3DIS", "Structured3D"),
    ),
    criteria=[
        dict(type="CrossEntropyLoss", loss_weight=1.0, ignore_index=-1),
        dict(type="LovaszLoss", mode="multiclass", loss_weight=1.0, ignore_index=-1),
    ],
)

# scheduler settings
epoch = 30000
# optimizer = dict(type="SGD", lr=0.1, momentum=0.9, weight_decay=0.0001, nesterov=True)
# scheduler = dict(type="MultiStepLR", milestones=[0.6, 0.8], gamma=0.1)
optimizer = dict(type="AdamW", lr=0.001, weight_decay=0.01)
scheduler = dict(
    type="OneCycleLR",
    max_lr=[0.001, 0.0001],
    pct_start=0.05,
    anneal_strategy="cos",
    div_factor=10.0,
    final_div_factor=1000.0,
)
param_dicts = [dict(keyword="block", lr=0.0001)]

# dataset settings
dataset_type = "ModelNetDataset"
data_root = "data/intra"
cache_data = False
class_names = [
    "vessel",
    "aneurysm"
]

data = dict(
    num_classes=2,
    ignore_index=-1,
    names=class_names,
    train=dict(
        type=dataset_type,
        split="fold_3_train",
        data_root=data_root,
        class_names=class_names,
        transform=[
            dict(type="NormalizeCoord"),
            dict(type="RandomScale", scale=[0.7, 1.5], anisotropic=True),
            dict(type="RandomShift", shift=((-0.2, 0.2), (-0.2, 0.2), (-0.2, 0.2))),
            dict(
                type="GridSample",
                grid_size=0.01,
                hash_type="fnv",
                mode="train",
                keys=("coord", "normal"),
                return_grid_coord=True,
            ),
            
            dict(type="ShufflePoint"),
            dict(type="ToTensor"),
            dict(
                type="Collect",
                keys=("coord", "grid_coord", "category"),
                feat_keys=["coord", "normal"],
            ),
        ],
        test_mode=False,
    ),
    val=dict(
        type=dataset_type,
        split="fold_3_test",
        data_root=data_root,
        class_names=class_names,
        transform=[
            dict(type="NormalizeCoord"),
            dict(
                type="GridSample",
                grid_size=0.01,
                hash_type="fnv",
                mode="train",
                keys=("coord", "normal"),
                return_grid_coord=True,
            ),
            dict(type="ToTensor"),
            dict(
                type="Collect",
                keys=("coord", "grid_coord", "category"),
                feat_keys=["coord", "normal"],
            ),
        ],
        test_mode=False,
    ),
    test=dict(
        type=dataset_type,
        split="fold_3_test",
        data_root=data_root,
        class_names=class_names,
        transform=[
            dict(type="NormalizeCoord"),
        ],
        test_mode=True,
        test_cfg=dict(
            post_transform=[
                dict(
                    type="GridSample",
                    grid_size=0.01,
                    hash_type="fnv",
                    mode="train",
                    keys=("coord", "normal"),
                    return_grid_coord=True,
                ),
                dict(type="ToTensor"),
                dict(
                    type="Collect",
                    keys=("coord", "grid_coord"),
                    feat_keys=["coord", "normal"],
                ),
            ],
            aug_transform=[
                [dict(type="RandomScale", scale=[1, 1], anisotropic=True)],  # 1
                [dict(type="RandomScale", scale=[0.8, 1.2], anisotropic=True)],  # 2
                [dict(type="RandomScale", scale=[0.8, 1.2], anisotropic=True)],  # 3
                [dict(type="RandomScale", scale=[0.8, 1.2], anisotropic=True)],  # 4
                [dict(type="RandomScale", scale=[0.8, 1.2], anisotropic=True)],  # 5
                [dict(type="RandomScale", scale=[0.8, 1.2], anisotropic=True)],  # 5
                [dict(type="RandomScale", scale=[0.8, 1.2], anisotropic=True)],  # 6
                [dict(type="RandomScale", scale=[0.8, 1.2], anisotropic=True)],  # 7
                [dict(type="RandomScale", scale=[0.8, 1.2], anisotropic=True)],  # 8
                [dict(type="RandomScale", scale=[0.8, 1.2], anisotropic=True)],  # 9
            ],
        ),
    ),
)

# hooks
hooks = [
    dict(type="CheckpointLoader"),
    dict(type="IterationTimer", warmup_iter=2),
    dict(type="InformationWriter"),
    dict(type="ClsEvaluator"),
    dict(type="CheckpointSaver", save_freq=None),
    dict(type="PreciseEvaluator", test_last=False),
]

# tester
test = dict(type="ClsVotingTester", num_repeat=100)
