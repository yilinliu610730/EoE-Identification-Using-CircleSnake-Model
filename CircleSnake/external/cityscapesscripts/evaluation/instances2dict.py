#!/usr/bin/python
#
# Convert instances from png files to a dictionary
#

from __future__ import absolute_import, division, print_function

import os
import sys

# Cityscapes imports
from external.cityscapesscripts.evaluation.instance import *
from external.cityscapesscripts.helpers.csHelpers import *


def appendInstanceDict(imageFileName, instanceDict):
    # Load image
    img = Image.open(imageFileName)

    # Image as numpy array
    imgNp = np.array(img)

    # Initialize label categories
    instances = {}
    for label in labels:
        instances[label.name] = []

    # Loop through all instance ids in instance image
    for instanceId in np.unique(imgNp):
        instanceObj = Instance(imgNp, instanceId)

        instances[id2label[instanceObj.labelID].name].append(instanceObj.toDict())

    imgKey = os.path.abspath(imageFileName)
    instanceDict[imgKey] = instances


def instances2dict(imageFileList, verbose=False):
    imgCount = 0
    instanceDict = {}

    if not isinstance(imageFileList, list):
        imageFileList = [imageFileList]

    if verbose:
        print("Processing {} images...".format(len(imageFileList)))

    for imageFileName in imageFileList:
        # Load image
        img = Image.open(imageFileName)

        # Image as numpy array
        imgNp = np.array(img)

        # Initialize label categories
        instances = {}
        for label in labels:
            instances[label.name] = []

        # Loop through all instance ids in instance image
        for instanceId in np.unique(imgNp):
            instanceObj = Instance(imgNp, instanceId)

            instances[id2label[instanceObj.labelID].name].append(instanceObj.toDict())

        imgKey = os.path.abspath(imageFileName)
        instanceDict[imgKey] = instances
        imgCount += 1

        if verbose:
            print("\rImages Processed: {}".format(imgCount), end=" ")
            sys.stdout.flush()

    if verbose:
        print("")

    return instanceDict


def main(argv):
    fileList = []
    if len(argv) > 2:
        for arg in argv:
            if "png" in arg:
                fileList.append(arg)
    instances2dict(fileList, True)


if __name__ == "__main__":
    main(sys.argv[1:])