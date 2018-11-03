from collections import namedtuple
Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')

ra = Rectangle(0., 0., 500., 500.)
rb = Rectangle(1., 1., 5., 5.0)

def area(a, b):
    a_area = (a.xmax - a.xmin) * (a.ymax - a.ymin)
    b_area = (b.xmax - b.xmin) * (b.ymax - b.ymin)

    dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
    dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)

    overlap_area = dx * dy

    return max(overlap_area / a_area, overlap_area / b_area) * 100

area(ra, rb)