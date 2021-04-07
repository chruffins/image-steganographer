# image-steganographer
creates password-protected messages hidden inside images

it mixes like two cryptography concepts at once:

1. steganography - this script hides ASCII text in any image (that has enough black pixels) without making it readily apparent that the image has been modified. it does this by replacing the 4 least significant bits of the blue and red channels for a single pixel with my own byte of data. 
2. encryption - this script hashes a password to be used as a seed for a random number generator, which is used both to scramble the positions of my bytes and to remember the positions of my bytes when decoding an image

ok cool
