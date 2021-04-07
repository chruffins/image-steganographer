import struct
import numpy
import cv2
import random
from hashlib import sha256

"""
OH YEAH!
"""

IMAGE_OVERRIDE = False # "test.png" # False
MESSAGE_OVERRIDE = False # "The quick brown fox jumps over a lazy dog."
ENCODE_OVERRIDE = False # True - forces encode. False - gives you an option.
OUTPUT_OVERRIDE = False # yeah
PASSWORD_OVERRIDE = False # "69420"

def getBlackPixelsListFromImage(img):
    """
    Return a list of black pixels in [r,c] format.
    """
    rows, columns, channels = img.shape
    r,c = 0,0
    blackPixels = []
    while r < rows:
        if img.item(r,c,0) < 32 and img.item(r,c,1) < 32 and img.item(r,c,2) < 32:
            blackPixels += [[r,c]]
        c = (c + 1) % columns
        r = c == 0 and (r+1) or r
    return blackPixels

def encodeRandomBlackPixelsInFrame(img, msg, password):
    pixels = getBlackPixelsListFromImage(img)

    #assert len(pixels) > len(msg) + 1

    h = sha256()
    h.update(bytes(password,'utf-8'))
    hashish = h.hexdigest()
    random.seed(int(hashish,16))
    
    encodedMsg = ASCIIToUInt4(msg)
    unusedPixels = list(range(len(pixels)))
    while encodedMsg != []:
        i = random.randint(0,len(unusedPixels))
        rP = pixels[i]
    
        img.itemset((rP[0],rP[1],0),(img.item(rP[0],rP[1],0) >> 4 & 15 * 16) + encodedMsg[0])
        img.itemset((rP[0],rP[1],1),(img.item(rP[0],rP[1],1) >> 4 & 15 * 16) + encodedMsg[1])

        encodedMsg = encodedMsg[2:]
        unusedPixels = unusedPixels[:i] + unusedPixels[i+1:]

    return encodedMsg == [] and img
    
def decodeRandomBlackPixelsInFrame(img, password):
    pixels = getBlackPixelsListFromImage(img)

    h = sha256()
    h.update(bytes(password,'utf-8'))
    hashish = h.hexdigest()
    random.seed(int(hashish,16))

    a = 0
    b = 0

    unusedPixels = list(range(len(pixels)))
    intlist = []
    while a != 0 or b != 10:
        i = random.randint(0,len(unusedPixels))
        rP = pixels[i]

        a = img.item(rP[0],rP[1],0) & 15
        b = img.item(rP[0],rP[1],1) & 15
        intlist.append(a)
        intlist.append(b)

        unusedPixels = unusedPixels[:i] + unusedPixels[i+1:]

    return UInt4ToASCII(intlist)

def ASCIIToUInt4(message):
    """
    Turn an ASCII message into a List of unsigned 4-bit ints.
    """
    intlist = []
    for x in message:
        intlist.append(ord(x) >> 4 & 15)
        intlist.append(ord(x) & 15)

    intlist.append(0)
    intlist.append(10)
    return intlist

def UInt4ToASCII(ints):
    """
    Turn a List of unsigned 4-bit ints into ASCII. Pure magic.
    """
    return ''.join([chr((ints[x] << 4) + ints[x+1]) for x in range(0,len(ints),2)])

def encode_image(input_path, output_path, msg, password=PASSWORD_OVERRIDE):
    img = cv2.imread(input_path)

    img = encodeRandomBlackPixelsInFrame(img, msg, password)

    cv2.imwrite(output_path, img)

def decode_image(image_path, password=PASSWORD_OVERRIDE):
    img = cv2.imread(image_path)

    return decodeRandomBlackPixelsInFrame(img, password)

# Let's go!
if __name__ == "__main__":
    filename = IMAGE_OVERRIDE or input("Enter the image you want to use here: ")
    mode = ENCODE_OVERRIDE or input("encode (e) or decode (d) or available space (s): ")
    if mode == "e":
        message = MESSAGE_OVERRIDE or input("Enter the message you want to use: ")
        password = PASSWORD_OVERRIDE or input("Enter a password to secure it: ")
        output_path = OUTPUT_OVERRIDE or input("Enter the filename where it will be stored: ")

        encode_image(filename, output_path, message, password)
    elif mode == "d":
        password = PASSWORD_OVERRIDE or input("Enter a password to decode it: ")

        print("Here's the contents of the image: \n{0}".format(decode_image(filename, password)))
    else:
        img = cv2.imread(filename)

        pixels,pixlen = getBlackPixelsListFromImage(img)
        print("You can fit {0} characters in this image.".format(pixlen))
