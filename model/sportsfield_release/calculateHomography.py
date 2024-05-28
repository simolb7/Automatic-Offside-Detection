import os
import numpy as np
import torch
import imageio
import matplotlib.pyplot as plt
from PIL import Image
from tqdm import tqdm_notebook as tqdm

from model.sportsfield_release.utils import util
from model.sportsfield_release.utils import image_utils, constant_var
from model.sportsfield_release.models import end_2_end_optimization
from model.sportsfield_release.options import fake_options
import cv2


def calculateOptimHomography(imagePath: str) -> torch.Tensor:
    ''' 
    Funzione che calcola l'omografia ottimizzata per l'immagine passata come parametro. DA FARE: spiegare meglio
    '''
    # if want to run on CPU, please make it False
    constant_var.USE_CUDA = False
    util.fix_randomness()

    # if GPU is RTX 20XX, please disable cudnn
    torch.backends.cudnn.enabled = True


    # set some options
    opt = fake_options.FakeOptions()
    opt.batch_size = 1
    opt.coord_conv_template = True
    opt.error_model = 'loss_surface'
    opt.error_target = 'iou_whole'
    opt.goal_image_path = imagePath
    opt.guess_model = 'init_guess'
    opt.homo_param_method = 'deep_homography'
    opt.load_weights_error_model = 'pretrained_loss_surface'
    opt.load_weights_upstream = 'pretrained_init_guess'
    opt.lr_optim = 1e-5
    opt.need_single_image_normalization = True
    opt.need_spectral_norm_error_model = True
    opt.need_spectral_norm_upstream = False
    opt.optim_criterion = 'l1loss'
    opt.optim_iters = 200
    opt.optim_method = 'stn'
    opt.optim_type = 'adam'
    opt.out_dir = 'model/sportsfield_release/out'
    opt.prevent_neg = 'sigmoid'
    opt.template_path = 'model/sportsfield_release/data/world_cup_template.png'
    opt.warp_dim = 8
    opt.warp_type = 'homography'



    # read original image
    goal_image = imageio.imread(opt.goal_image_path, pilmode='RGB')
    goal_image_toHomograph = imageio.imread(opt.goal_image_path, pilmode='RGB')
    #plt.imshow(goal_image)
    #plt.show()
    # resize image to square shape, 256 * 256, and squash to [0, 1]
    pil_image = Image.fromarray(np.uint8(goal_image))
    pil_image = pil_image.resize([256, 256], resample=Image.NEAREST)
    goal_image = np.array(pil_image)
    #plt.imshow(goal_image)
    #plt.show()
    # covert np image to torch image, and do normalization
    goal_image = util.np_img_to_torch_img(goal_image)
    if opt.need_single_image_normalization:
        goal_image = image_utils.normalize_single_image(goal_image)
    print('mean of goal image: {0}'.format(goal_image.mean()))
    print('std of goal image: {0}'.format(goal_image.std()))

    template_image = imageio.imread(opt.template_path, pilmode='RGB')
    template_imageToHomograph = imageio.imread(opt.template_path, pilmode='RGB')
    template_image = template_image / 255.0
    if opt.coord_conv_template:
        template_image = image_utils.rgb_template_to_coord_conv_template(template_image)
    #plt.imshow(template_image)
    #plt.show()
    # covert np image to torch image, and do normalization
    template_image = util.np_img_to_torch_img(template_image)
    if opt.need_single_image_normalization:
        template_image = image_utils.normalize_single_image(template_image)

    e2e = end_2_end_optimization.End2EndOptimFactory.get_end_2_end_optimization_model(opt)

    orig_homography, optim_homography = e2e.optim(goal_image[None], template_image)
    return optim_homography
