from PIL import Image, ImageFilter, ImageOps
from setuptools import setup, find_packages


def blur(uname):
    before = Image.open('static\\images\\{}.png'.format(uname))
    after = before.filter(ImageFilter.BoxBlur(10))
    after.save('static\\images\\{}.png'.format(uname))

def gray(uname):
    before = Image.open('static\\images\\{}.png'.format(uname))
    after = before.convert("L")
    after.save('static\\images\\{}.png'.format(uname))

def solarize(uname):
    before = Image.open('static\\images\\{}.png'.format(uname))
    after = ImageOps.solarize(before, threshold=125)
    after.save('static\\images\\{}.png'.format(uname))



setup(
    name = 'package_two',
    packages = find_packages()
)