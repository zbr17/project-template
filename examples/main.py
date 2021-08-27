import sys
import os
from os.path import abspath as opa
from os.path import join as opj
sys.path.append(
    opa(__file__ + "/../../")
)
import logging
logging.getLogger().setLevel(logging.INFO)
import torch.backends.cudnn as cudnn
import logging
import argparse
import time

from thudml.launcher.creators import ConfigHandler
from thudml.launcher.misc import utils
from thudml.launcher.misc import ParserWithConvert

proj_path = opa(opj(__file__, "../../src/NAME"))

# argparser
csv_path = opj(proj_path, "config/args.csv")
parser = ParserWithConvert(csv_path=csv_path, name="NAME")
opt, convert_dict = parser.render()

# args postprocess
if opt.is_resume:
    opt.delete_old = False

### Hyper-parameters
opt.link_path = opj(proj_path, "config/link/", "link_" +opt.setting + ".yaml")
opt.assert_path = opj(proj_path, "config/assert.yaml")
opt.save_path = opj(opt.save_path, "{}/".format(time.strftime("%Y-%m-%d", time.localtime())), opt.save_name)
opt.wrapper_path = opj(proj_path, "config/wrapper")
opt.params_path = opj(proj_path, "config/param")
warmup = opt.warmup

phase = opt.phase
is_test = not opt.not_test
setting = opt.setting
start_epoch = 0
is_save = True
cudnn.deterministic = True
cudnn.benchmark = True

# get confighandler
config_handler = ConfigHandler(
    convert_dict=convert_dict,
    link_path=opt.link_path,
    assert_path=opt.assert_path,
    params_path=opt.params_path,
    wrapper_path=opt.wrapper_path,
    is_confirm_first=True
)

# register packages

# initiate params_dict
config_handler.get_params_dict(
    modify_link_dict={
        "datasets": [
            {"train": "{}_train.yaml".format(opt.dataset)},
            {"test": "{}_test.yaml".format(opt.dataset)}
        ],
    }
)

# delete redundant options
convert_opt_list = list(config_handler.convert_dict.keys())
for k in list(opt.__dict__.keys()):
    if k not in convert_opt_list:
        delattr(opt, k)

# modify parameters
objects_dict = config_handler.create_all(opt.__dict__)

# get manager
manager = utils.get_default(objects_dict, "managers")

warm_up_list = None
# start
manager.run(
    phase=phase,
    start_epoch=start_epoch,
    is_test=is_test,
    is_save=is_save,
    warm_up=warmup,
    warm_up_list=None
)