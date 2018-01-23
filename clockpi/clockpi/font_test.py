import time

from clockpi.alphanum.alphanum import ALL as ALL_ALPHANUM
from clockpi.alphanum.numbers_small import ALL_NUMBERS as ALL_NUMBERS_SMALL
from clockpi.constants import ARRAY_HEIGHT
from clockpi.constants import ARRAY_WIDTH
from clockpi.graphics.utils import add_items_to_matrix
from clockpi.graphics.utils import add_to_matrix
from clockpi.graphics.utils import MatrixGenerator
from clockpi.utils import send_matrix


def show_result(arduino, matrix):
    send_matrix(arduino, matrix)
    time.sleep(2)
    inverse_matrix = MatrixGenerator.generate_empty_matrix([255, 0, 0])
    add_to_matrix(inverse_matrix, matrix, 0, 0, transpose=False, bit_xor=True)
    send_matrix(arduino, matrix)
    time.sleep(2)


def font_test(arduino, padding=0):
    matrix = MatrixGenerator.generate_empty_matrix()
    send_matrix(arduino, matrix)

    for alphanum_subset in ALL_ALPHANUM:
        current_x = padding
        current_y = padding
        row_max_height = 0
        for character in alphanum_subset:
            char_width = len(character[0])
            char_height = len(character)
            if (current_x + padding + char_width) > ARRAY_WIDTH:
                # Wrap to the next line, if we can. Otherwise, print and wait
                next_row_max_y = (current_y + row_max_height + char_height +
                                  padding)
                if next_row_max_y <= ARRAY_HEIGHT:
                    # Wrap to a new line
                    current_y += row_max_height + padding
                    current_x = 0
                    row_max_height = 0
                else:
                    # Can't fit this character on this page - show what we have
                    show_result(arduino, matrix)
                    matrix = MatrixGenerator.generate_empty_matrix()
                    current_x = padding
                    current_y = padding
            # Add the next character
            row_max_height = max(row_max_height, char_height)
            current_x += padding
            add_items_to_matrix([character], matrix, current_x, current_y, 0,
                                [255, 255, 255])
            current_x += char_width
        show_result(arduino, matrix)
        matrix = MatrixGenerator.generate_empty_matrix()


def marquee_test(arduino, padding=1):
    matrix = MatrixGenerator.generate_empty_matrix()
    send_matrix(arduino, matrix)

    characters = ALL_NUMBERS_SMALL
    x_offset = len(matrix) + 10
    for ii in xrange(x_offset + 100):
        matrix = MatrixGenerator.generate_empty_matrix()
        add_items_to_matrix(characters, matrix, x_offset - ii, padding,
                            padding, [255, 255, 255])
        send_matrix(arduino, matrix)
