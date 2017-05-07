#!/usr/bin/env python
# coding=utf-8
# NOTE:
# for iphone photos, it use exif extension to store orientation of a jpg
# but the width/height is all the same, which result in rotated pic in browser
# we need to rotate the picture according to its exif orientation info
#
# on linux, install exiftran (apt-get install exiftran)
# and run "exiftran -ai <pic>"
#
# another issue, do not let image file size too large if taken on iphone.
# use command to convert(keep width to fix size)
#   for f in *.jpg ; do convert $f -resize '1000' $f ; done
# use command "identify *.jpg" can see image info.
#
# preview markdown, can use atom text editor, and Ctrl+Shift+m
#
"""
generate README.md based on path containing pics
"""
import os
import sys
import argparse
from string import Template

PICS_STORE_FOLDER='records'
SINGLE_MD_HEADER=(
    '# ${title}\n'
    '\n'
)
SINGLE_MD_ITEM=(
    '### ${item_name}  \n'
    '![](${item_pic})\n'
    '\n'
)

class PicGroup(object):
    """A class contains pictures and info"""
    def __init__(self):
        self.root=None      # root path
        self.pics=[]        # pic file names, without path
        self.date=None      # date of the pic group
        self.readme=None    # README.md file. maybe none
    def gen_readme(self):
        if self.readme:
            # no need to gen
            return
        readme_str = Template(SINGLE_MD_HEADER).substitute(title=self.date)
        for pic in self.pics:
            readme_str += Template(SINGLE_MD_ITEM).\
                    substitute(item_name=os.path.splitext(pic)[0],\
                               item_pic=pic)
        #print readme_str
        with open(os.path.join(self.root,'README.md'),'w+') as f:
            f.write(readme_str)

def check_python_version():
    if sys.version_info < (2,7):
        print ("python version at least 2.7")
        print ("your python is %s"%sys.version)
        return False
    return True

# path should be a return value of os.path.abspath
# where the triling slash '/' is ignored!
def gen_pic_group(path):
    files = os.listdir(path)
    if not files:
        print("ERROR, no picture found in %s"%p)
        return None
    pi=PicGroup()
    pi.root=path
    pi.date=os.path.basename(path)  # TODO: validate date
    for _f in files:
        if _f.endswith('.jpg') or _f.endswith('.jpeg'):
            pi.pics.append(_f)
        if _f == "README.md" or _f == "readme.md":
            pi.readme=_f
    if not pi.pics:
        print("no pictures found under %s"%path)
        return None;
    return pi

if __name__ == '__main__':
    if not check_python_version():
        exit(1)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pic_path',nargs='*',\
                        metavar='p',help='path to the pics')
    args = parser.parse_args()
    _pic_path = args.pic_path
    if not _pic_path:
        # not parsed in, we generate a default list
        for _one in os.listdir(PICS_STORE_FOLDER):
            _1 = os.path.join(PICS_STORE_FOLDER,_one)
            if os.path.isdir(_1):
                _pic_path.append(_1)

    #print args.pic_path
    for _p in _pic_path:
        p = os.path.abspath(_p)
        if not os.path.isdir(p):
            print ("path not exist! %s"%p)
            #parser.print_usage()
            continue
        print('parsing %s ...'%_p)
        pic_group=gen_pic_group(p)
        if not pic_group:
            continue
        if pic_group.readme:
            print("   readme.md already exist, ignore %s"%_p)
            continue
        pic_group.gen_readme()
        print('done %s.'%_p)
