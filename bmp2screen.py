
import os
import pygame 

screen = pygame.display.set_mode()


def readbmp(filename):
        def lebytes_to_int(bytes):
            n = 0x00
            while len(bytes) > 0:
                n <<= 8
                n |= bytes.pop()
            return int(n)

        f = open(filename, 'rb') 
        img_bytes = list(bytearray(f.read(26))) # just read header
        start_pos = lebytes_to_int(img_bytes[10:14])

        width = lebytes_to_int(img_bytes[18:22])
        height = lebytes_to_int(img_bytes[22:26])
        
        if (width > 120) : scale = 2
        scale = 1
        seektostart = f.read(start_pos - 26)
    
        for x in range(height):
            colrow = list(bytearray(f.read(3 * width)))
            for y in range(width):
                b,g,r = colrow[y*3:y*3+3]
                pen = (r >> 0,g >> 0,b >> 0)
                screen.set_at(( y // scale,(height - x) // scale), pen)
		#pixel(y // scale,(height - x) // scale)
        f.close()
        pygame.display.flip()
        return 

if __name__=='__main__':
    readbmp("lena.bmp")
    while True:
           p = 0  
