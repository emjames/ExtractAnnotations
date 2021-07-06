#!/usr/bin/env python3
# From https://stackoverflow.com/questions/21050551/extracting-text-from-highlighted-annotations-in-a-pdf-file
# Requirements:
# sudo dnf install python3-poppler-qt5

import popplerqt5
import PyQt5
import sys
import urllib
import os
import math

supported_colors = [
        {'name': 'Red',     'value': [255, 0, 0]},
        {'name': 'Green',   'value': [0, 255, 0]},
        {'name': 'Blue',    'value': [0, 0, 255]},
        {'name': 'Yellow',  'value': [255, 255, 0]},
        {'name': 'Cyan',    'value': [0, 255, 255]}]

def get_named_color(color_rgb):
    """
    Convert RGB to a named color by calculating the distance between the
        annotation's RGB and the supported colors
    """
    least_distant_color = None
    least_distance = 999

    # Measure the distance between two colors:
    #   https://www.micro-epsilon.com/service/glossar/Farbabstand.html
    for color in supported_colors:
        distance = 0
        for v1, v2 in zip(color['value'], color_rgb):
            distance += (v1 - float(v2))**2
        distance = math.sqrt(distance)

        if distance <= least_distance:
            least_distant_color = color
            least_distance = distance

    return least_distant_color


def main():

    input_filename = sys.argv[1]
    document = popplerqt5.Poppler.Document.load(input_filename)

    n_pages = document.numPages()
    # A list of annotations that have the color as key and the annotation
    # information as value
    annotations_by_color = {}
    for c in supported_colors:
        annotations_by_color[c['name']] = []

    
    for i in range(n_pages):
        page = document.page(i)
        (pwidth, pheight) = (page.pageSize().width(), page.pageSize().height())
        annotations = page.annotations()
        if len(annotations) > 0:
            for annotation in annotations:
                color = annotation.style().color().getRgb()

                # [:3] since we only want the RGB bit
                named_color = get_named_color(color[:3])

                if isinstance(annotation, popplerqt5.Poppler.Annotation):
                    if isinstance(annotation, popplerqt5.Poppler.HighlightAnnotation):
                        
                        quads = annotation.highlightQuads()
                        txt = ""
                        for quad in quads:
                            rect = (quad.points[0].x() * pwidth,
                                    quad.points[0].y() * pheight,
                                    quad.points[2].x() * pwidth,
                                    quad.points[2].y() * pheight)
                            body = PyQt5.QtCore.QRectF()
                            body.setCoords(*rect)
                            txt = txt + str(page.text(body)) + ' '

                        annotations_by_color[named_color['name']].append({
                                'page': i+1,
                                'content': str(txt),
                                'type': 'HighlightAnnotation'
                                })
                    elif isinstance(annotation, popplerqt5.Poppler.TextAnnotation):
                        print('TEXTBOX ANNOTATIONS')
                        print('!!!!!!')
                        print(annotation.contents())
                        color = annotation.style().color().getRgb()
                        named_color = get_named_color(color[:3])

                        annotations_by_color[named_color['name']].append({
                                'page': i+1,
                                'content': str(annotation.contents()),
                                'type': 'TextAnnotation'
                                })
                    else:
                        print('Not HighlightAnnotation but something else')
                        print('******')
    print(annotations_by_color['Yellow'])
        # else:
        #     print('No annotations found')


if __name__ == "__main__":
    main()
