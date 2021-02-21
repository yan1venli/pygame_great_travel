from PIL import Image


def mirror(name):
    f = open(f'map/making/{name}.txt', 'w')
    im = Image.open(f'map/shablon/{name}.png')
    im.thumbnail((128, 128))
    pixels = im.load()
    x, y, = im.size
    for i in range(x):
        f.write('\n')
        for j in range(y):
            if pixels[i, j][0] > 160 and pixels[i, j][0] < 255 and \
                    pixels[i, j][1] > 100 and pixels[i, j][1] < 255 and \
                    pixels[i, j][2] > 100 and pixels[i, j][2] < 255:
                f.write('_, ')
            if pixels[i, j][0] > 0 and pixels[i, j][0] < 50 and \
                    pixels[i, j][0] > 0 and pixels[i, j][0] < 51 and \
                    pixels[i, j][0] > 0 and pixels[i, j][0] < 51:
                f.write('1, ')
            if pixels[i, j][0] > 60 and pixels[i, j][0] < 160 and \
                    pixels[i, j][0] > 60 and pixels[i, j][0] < 160 and \
                    pixels[i, j][0] > 60 and pixels[i, j][0] < 160:
                f.write('0, ')
            else:
                f.write('_, ')

