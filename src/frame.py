'''
    Common tools for drawing compatible frames in a Component's frameRender()
'''
from PyQt5 import QtGui
from PIL import Image
from PIL.ImageQt import ImageQt
import sys
import os


class Frame:
    '''Controller class for all frames.'''


class FramePainter(QtGui.QPainter):
    '''
        A QPainter for a blank frame, which can be converted into a
        Pillow image with finalize()
    '''
    def __init__(self, width, height):
        image = BlankFrame(width, height)
        self.image = QtGui.QImage(ImageQt(image))
        super().__init__(self.image)

    def setPen(self, RgbTuple):
        super().setPen(PaintColor(*RgbTuple))

    def finalize(self):
        self.end()
        imBytes = self.image.bits().asstring(self.image.byteCount())

        return Image.frombytes(
            'RGBA', (self.image.width(), self.image.height()), imBytes
        )


class PaintColor(QtGui.QColor):
    '''Reverse the painter colour if the hardware stores RGB values backward'''
    def __init__(self, r, g, b, a=255):
        if sys.byteorder == 'big':
            super().__init__(r, g, b, a)
        else:
            super().__init__(b, g, r, a)


def FloodFrame(width, height, RgbaTuple):
    return Image.new("RGBA", (width, height), RgbaTuple)


def BlankFrame(width, height):
    '''The base frame used by each component to start drawing.'''
    return FloodFrame(width, height, (0, 0, 0, 0))


def Checkerboard(width, height):
    '''
        A checkerboard to represent transparency to the user.
        TODO: Would be cool to generate this image with numpy instead.
    '''
    image = FloodFrame(1920, 1080, (0, 0, 0, 0))
    image.paste(Image.open(
        os.path.join(Frame.core.wd, "background.png")),
        (0, 0)
    )
    image = image.resize((width, height))
    return image