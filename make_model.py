import sys
import os
sys.path.append('../gansegmentation/face-parsing.PyTorch')
os.environ["CUDA_VISIBLE_DEVICES"] = "4"


from models.stylegan2_generator import *
from models.stylegan2_discriminator import *
from models.stylegan_generator import *
from models.stylegan_discriminator import *
from models.pggan_generator import *
from models.pggan_discriminator import *
###  

from model import *
from resnet import *
from transform import *

import numpy as np
from PIL import Image
import torchvision.transforms as transforms
# import cv2

def segmentation_model(path = '../gansegmentation/face-parsing.PyTorch/res/cp/79999_iter.pth', n_classes = 19):

	with torch.no_grad():
		net = BiSeNet(n_classes = 19)
		net.load_state_dict(torch.load(path))
		net.eval()

	return net

def styleGANv2(path = '../GAN_analy/genforce/stylegan2_ffhq1024.pth', resolution = 1024):

	Gs_style = StyleGAN2Generator(resolution = resolution)
	D_style = StyleGAN2Discriminator(resolution = resolution)

	model = torch.load(path)

	Gs_style.load_state_dict(model['generator_smooth'])
	D_style.load_state_dict(model['discriminator'])

	Gs_style.eval()
	D_style.eval()

	return Gs_style, D_style


def styleGANv1(path = '../GAN_analy/genforce/stylegan_ffhq1024.pth', resolution = 1024):

	Gen = StyleGANGenerator(resolution = resolution)
	Dis = StyleGANDiscriminator(resolution = resolution)

	model = torch.load(path)

	Gen.load_state_dict(model['generator_smooth'])
	Dis.load_state_dict(model['discriminator'])

	Gen.eval()
	Dis.eval()

	return Gen, Dis

def pgGAN(path = '../GAN_analy/genforce/pggan_celebahq1024.pth', resolution = 1024):

	Gen = PGGANGenerator(resolution = resolution)
	Dis = PGGANDiscriminator(resolution = resolution)

	model = torch.load(path)

	Gen.load_state_dict(model['generator_smooth'])
	Dis.load_state_dict(model['discriminator'])

	Gen.eval()
	Dis.eval()

	return Gen, Dis


def img_process(img_path):
	
	to_tensor = transforms.Compose([
		transforms.ToTensor(),
		transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
	    ])

	img = Image.open(img_path)
	image = img.resize((512,512), Image.BILINEAR)
	img = to_tensor(image)
	img = torch.unsqueeze(img, 0)

	return img

