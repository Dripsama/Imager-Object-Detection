from PIL import Image
import numpy as np
import tensorflow as tf


def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGB', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im

def extractInfo(modelOutput, anchors, numClass):
    featureDim = modelOutput.shape
    numAnchor = anchors.shape[0]  # get the number of anchors, 5 for the Pascal dataset
    modelOutput = tf.reshape(modelOutput, shape=(-1, featureDim[1], featureDim[2], numAnchor, numClass + 5))
    imageShape = featureDim[1:3]  # get the width and height of output feature map
    boxXY = tf.nn.sigmoid(modelOutput[..., :2])  # boxXY now w.r.t top left corner of its grid(on grid scale)
    idx = getOffset(imageShape) # convert box center to grid scale
    idx = tf.cast(idx, modelOutput.dtype)
    anchors = tf.cast(tf.reshape(anchors, (1, 1, 1, numAnchor, 2)), idx.dtype)
    boxXY = (boxXY + idx)  
    boxWH = tf.math.exp(modelOutput[..., 2:4]) 
    boxWH = boxWH * anchors
    objScore = tf.nn.sigmoid(modelOutput[..., 4:5])  # objectiveness score; must be between 0 and 1
    classProb = tf.nn.softmax(modelOutput[..., 5:])  # probability of classes; pass through a softmax gate to obtain prob.
    return boxXY, boxWH, objScore, classProb

def getOffset(shape):
    hIndex = tf.reshape(tf.range(start=0, limit=shape[0]), (shape[0], 1))
    hIndex = tf.tile(hIndex, [1, shape[1]])  # expand in the height direction
    wIndex = tf.reshape(tf.range(start=0, limit=shape[1]), (1, shape[1]))
    wIndex = tf.tile(wIndex, [shape[0], 1])  # expand in the width direction
    idx = tf.stack([wIndex, hIndex], axis=-1)
    idx = tf.reshape(idx, shape=(1, *shape, 1, 2)) # reshape the offset so that it can add to boxXY directly
    return idx

def convertbox(boxes):
	for box in boxes:
		w, h = box[2] - box[0], box[3] - box[1]
		box[2], box[3] = w, h
	return boxes

def getBoxLoc(boxXY, boxWH):
    topLeft = boxXY - boxWH / 2  # top left
    
    bottomRight = boxXY + boxWH / 2  # bottom right
    return tf.concat([topLeft, bottomRight], axis=-1)

def scaleBox(boxLoc, imgw, imgh, scale=(32, 32)):
	height, width = scale[0]*imgw/416.0, scale[1]*imgh/416.0
	shape = tf.stack([height, width, height, width])
	shape = tf.reshape(shape, [1, 4])
	shape = tf.cast(shape, boxLoc.dtype)
	return boxLoc * shape

def filterBox(boxLoc, objScore, classProb, scoreThresh=0.5):
    boxScore = objScore * classProb  # (None, B1, B2, S, NCLASS)
    boxClass = tf.argmax(boxScore, axis=-1)  # shape = (None, S, S, B)
    boxScore = tf.math.reduce_max(boxScore, axis=-1)  # shape = (None, S, S, B)
    mask = boxScore >= scoreThresh
    # filter out low-confidence boxes
    boxes = tf.boolean_mask(boxLoc, mask)
    scores = tf.boolean_mask(boxScore, mask)
    classes = tf.boolean_mask(boxClass, mask)
    return boxes, scores, classes

def nonMaxSuppress(boxLoc, score, classPredict, maxBox=20, iouThresh=0.5):
    boxLoc=np.float32(boxLoc)
    score=np.float32(score)
    idx = tf.image.non_max_suppression(boxLoc, score, maxBox, iou_threshold=iouThresh)
    boxLoc = tf.gather(boxLoc, idx)
    score = tf.gather(score, idx)
    classPredict = tf.gather(classPredict, idx)
    return boxLoc, score, classPredict

def raw2Box(featureMap, anchors, numClass, imgw, imgh,  maxBox=20, scoreThresh=0.5, iouThresh=0.6):
    # convert coordinates
    print('image width and height', imgw, imgh) 
    print('YOLO output shape: ', featureMap.shape)
    batchXY, batchWH, batchScore, batchProb = extractInfo(featureMap, anchors, numClass)
    # convert boxXY,boxWH to corner coordinates 
    batchLoc = getBoxLoc(batchXY, batchWH)
    # scale the coordinates from grid scale to image scale 
    batchLoc = scaleBox(batchLoc, imgw, imgh)
    print('Processed box coordinate shape: ', batchLoc.shape)
    # a for loop is needed because different images have various number of boxes
    # for each image, let's do:
    for boxLoc, objScore, classProb in zip(batchLoc, batchScore, batchProb):
        # filter out low confidence boxes
        boxes, scores, classes = filterBox(boxLoc, objScore, classProb, scoreThresh)
        # filter out overlapped boxes
        boxes, scores, classes = nonMaxSuppress(boxes, scores, classes, maxBox, iouThresh)
        # return a list of boxes for that image 
        print('box count: ', len(boxes))
        return boxes, scores, classes