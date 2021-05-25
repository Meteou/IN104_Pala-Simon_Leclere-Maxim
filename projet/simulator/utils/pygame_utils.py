import pygame as pg
from math import cos, sin, pi, sqrt


def draw_text(surf, font, text, pos,
              antialiasing=True,
              color=(255, 255, 255),
              anchor="northwest"):
    """ Draw a text on a Surface and return it 
        (cf https://www.pygame.org/docs/ref/font.html#pygame.font.Font.render)

        Mandatory arguments:
            text: the string to draw
            x: abscissa
            y: ordinate

        Keyword arguments:
            antialiasing:
            color:
            anchor: can be one of north, south, west, east, northwest, northeast,
                    southwest, southeast, center
    """
    x, y = pos
    s = font.render(text, antialiasing, color)
    s_rect = s.get_rect()

    if "north" in anchor:
        s_rect.y = y
    elif "south" in anchor:
        s_rect.y = y - s_rect.h
    else:
        s_rect.y = y - s_rect.h/2

    if "west" in anchor:
        s_rect.x = x
    elif "east" in anchor:
        s_rect.x = x - s_rect.w
    else:
        s_rect.x = x - s_rect.w/2

    surf.blit(s, s_rect)


def draw_dashed_line(surf, color, begin, end, width=1, dash_length=10):
    x1, y1 = begin
    x2, y2 = end
    dispx = x2 - x1
    dispy = y2 - y1
    length = sqrt(dispx ** 2 + dispy ** 2)
    slopex = dispx/length
    slopey = dispy/length

    for index in range(0, int(length/dash_length), 2):
        xi1 = int(x1 + (slopex * index * dash_length))
        yi1 = int(y1 + (slopey * index * dash_length))
        xi2 = int(x1 + (slopex * (index+1) * dash_length))
        yi2 = int(y1 + (slopey * (index+1) * dash_length))
        pg.draw.line(surf, color, (xi1, yi1), (xi2, yi2), width)
