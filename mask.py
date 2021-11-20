from PIL import Image
import numpy as np
# Open the image form working directory
image = Image.open('SegmentationClass/frame_000000.png')
# summarize some details about the image
print(image.format)
print(image.size)
print(image.mode)

np.set_printoptions(threshold=np.inf)
# convert image to numpy array
data = np.asarray(image)
print(type(data))
# summarize shape
print(data.shape)

# # load and display an image with Matplotlib
# from matplotlib import image
# from matplotlib import pyplot
# # load image as pixel array
# image = image.imread('SegmentationClass/frame_000000.png')
# # summarize shape of the pixel array
# print(image.dtype)
# print(image.shape)
# # display the array of pixels as an image
# pyplot.imshow(image)
# pyplot.show()