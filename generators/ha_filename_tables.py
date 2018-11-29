
from .constants import *
from .table_mapper import ha_filename_table
from .utils import mdata_dir


ha_filename_tables = [
    ('filenames_HCY5HCCXY.tsv', {}),
    ('filenames_HMC2KCCXY.tsv', {'description_key': BC}),
    ('filenames_HMCMJCCXY.tsv', {'description_key': BC, 'strict': False}),
    ('air_samples.filenames_HK7G5CCXY.txt', {}),


    ('haib17CEM4890_filenames_H2NYMCCXY.txt', {'description_key': METASUB_NAME}),
    ('haib17CEM4890_filenames_H3KHWCCXY.txt', {'description_key': METASUB_NAME}),
    ('haib17CEM4890_filenames_H75CGCCXY.txt', {'description_key': METASUB_NAME}),
    ('haib17CEM4890_filenames_H7KYMCCXY.txt', {'description_key': METASUB_NAME}),
    ('haib17CEM4890_filenames_HKC32ALXX.txt', {'description_key': METASUB_NAME}),
    ('haib17CEM4890_filenames_HMCMJCCXY.txt', {'description_key': METASUB_NAME}),

    ('haib17CEM5080_filenames_H7VL7CCXY.txt', {}),

    ('haib17CEM5106_filenames_HCCGHCCXY.txt', {}),
    ('haib17CEM5106_filenames_HCV72CCXY.txt', {}),
    ('haib17CEM5106_filenames_HCVMTCCXY.txt', {}),
    ('haib17CEM5106_filenames_HCY5HCCXY.txt', {}),
    ('haib17CEM5106_filenames_HCY5JCCXY.txt', {}),

    ('haib17CEM5241_filenames_HMCMJCCXY.txt', {}),
    ('haib17CEM5241_filenames_HMGTJCCXY.txt', {
        'description_key': BC,
        'token_val_funcs': {BC: lambda x: x.split('_')[-1]}
    }),  # kyiv, ukraine_2_235114675
    ('haib17CEM5241_filenames_HMGW3CCXY.txt', {
        'description_key': BC,
        'token_val_funcs': {BC: lambda x: x.split('_')[-1]}
    }),  # kyiv, ukraine_2_235114675
    ('haib17CEM5241_filenames_HMGMHCCXY.txt', {
        'description_key': BC,
        'token_val_funcs': {BC: lambda x: x.split('_')[-1]}
    }),  # kyiv, ukraine_2_235114672

    ('haib17DB4959_filenames_H3MGVCCXY.txt', {}),
    ('haib17DB4959_filenames_HMCMJCCXY.txt', {}),
    ('haib17DB4959_filenames_HMGTJCCXY.txt', {}),  # Inbound5_B_2
    ('haib17DB4959_filenames_HMGW3CCXY.txt', {}),  # Inbound2_A_7

    ('haib17KIU4866_filenames_H7HJMCCXY.txt', {}),  # standard DNA prep with sequencing on the X
    ('haib17KIU4866_filenames_HMCMJCCXY.txt', {}),  # standard DNA prep with sequencing on the X

    ('haib18CEM5332_filenames_HK7G5CCXY.txt', {'description_key': METASUB_NAME}),  # gCSD17-HKG-AS1
    ('haib18CEM5332_filenames_HMCMJCCXY.txt', {'description_key': METASUB_NAME}),  # gCSD17-OSL-AS17
    ('haib18CEM5332_filenames_HMGTJCCXY.txt', {'description_key': METASUB_NAME}),  # gCSD17-NYC-AS01
    ('haib18CEM5332_filenames_HMGW3CCXY.txt', {'description_key': METASUB_NAME}),  # gCSD17-NYC-AS01

    ('haib18CEM5453_filenames_HMC2KCCXY.txt', {'description_key': BC}),  # 0235023170
    ('haib18CEM5453_filenames_HMCMJCCXY.txt', {}),
    ('haib18CEM5453_filenames_HMGTJCCXY.txt', {'description_key': BC}),  # 235185269
    ('haib18CEM5453_filenames_HMGW3CCXY.txt', {'description_key': BC}),  # 0235075616
    ('haib18CEM5453_filenames_HNGH3CCXY.txt', {'description_key': BC}),
    ('haib18CEM5453_filenames_HMGN5CCXY.txt', {'description_key': BC}),
    ('haib18CEM5453_filenames_HNHKFCCXY.txt', {'description_key': BC}),
    ('haib18CEM5453_filenames_HT5YVCCXY.txt', {'description_key': BC}),

    ('haib18CEM5526_filenames_HMGTJCCXY.txt', {'description_key': BC}),  # 232023295
    ('haib18CEM5526_filenames_HMGW3CCXY.txt', {'description_key': BC}),  # 232023295
    ('haib18CEM5526_filenames_HMGMHCCXY.txt', {'description_key': BC}),  # 235040613
]
HA_FILENAME_TABLES = [
    ha_filename_table(
        mdata_dir('hudson_alpha_filename_files/' + filename),
        **kwargs
    )
    for filename, kwargs in ha_filename_tables
]
