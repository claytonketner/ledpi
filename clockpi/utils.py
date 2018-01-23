from PIL import Image
from PIL import ImageDraw


def send_matrix(driver, matrix):
    image = Image.new('RGB', (64, 32))
    draw = ImageDraw.Draw(image)
    for ii in xrange(len(matrix)):
        for jj in xrange(len(matrix[0])):
            pixel = matrix[ii][jj]
            draw.point((ii, jj), fill=tuple(pixel))
    driver.Clear()
    driver.SetImage(image, 0, 0)
