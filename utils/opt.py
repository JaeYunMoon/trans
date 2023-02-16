import argparse
import logging
import os
from .read_to_path import update_config
from .make_name import create_name

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser(description='sim2real')

parser.add_argument('--config',
                    help='custom_data',
                    required=True)
parser.add_argument('--data_path',
                    help='experiment configure file name',
                    default='./data/datasets/',
                    type=str)
parser.add_argument('--concat',
                    help='experiment configure file name',
                    default= False,
                    type=str2bool)
parser.add_argument('--seg_bool',
                    help='experiment configure file name',
                    default= False,
                    type=str2bool)
parser.add_argument('--pdf',
                    help='experiment configure file name',
                    default=True,
                    type=str2bool)
parser.add_argument('--custom',
                    help='experiment configure file name',
                    default=True,
                    type=str2bool)
parser.add_argument('--custom_label',
                    help='experiment configure file name',
                    default=True,
                    type=str2bool)
parser.add_argument('--rbox',
                    help='experiment configure file name',
                    default=False,
                    type=str2bool)
parser.add_argument('--box3DPX',
                    help='experiment configure file name',
                    default=False,
                    type=str2bool)
parser.add_argument('--keypoint3d',
                    help='experiment configure file name',
                    default=False,
                    type=str2bool)
parser.add_argument('--keypoint2d',
                    help='experiment configure file name',
                    default=False,
                    type=str2bool)


opt = parser.parse_args()
cfg = update_config(opt.config)

# path 검사
cn = create_name(opt.config)
log = cn.log_name
print('log',log)


if not os.path.exists("./result/log"):
    os.makedirs("./result/log")

filehandler = logging.FileHandler(
    './result/{}/{}.log'.format('log',log))
streamhandler = logging.StreamHandler()

logger = logging.getLogger('')
logger.setLevel(logging.INFO)
logger.addHandler(filehandler)
logger.addHandler(streamhandler)


 