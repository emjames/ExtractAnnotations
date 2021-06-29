#!/usr/bin/env python3
# From https://stackoverflow.com/questions/21050551/extracting-text-from-highlighted-annotations-in-a-pdf-file
# Requirements:
# sudo dnf install python3-poppler-qt5

import popplerqt5
import PyQt5
import sys
import urllib
import os

def main():

    input_filename = sys.argv[1]
    document = popplerqt5.Poppler.Document.load(input_filename)

    n_pages = document.numPages()
    
    for i in range(n_pages):
        page = document.page(i)
        (pwidth, pheight) = (page.pageSize().width(), page.pageSize().height())
        annotations = page.annotations()
        if len(annotations) > 0:
            for annotation in annotations:
                print(annotation.Style().color().value())
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


                        print(str(txt))
                        print(f'Page: {i+1}')
                        print('======')
                    elif isinstance(annotation, popplerqt5.Poppler.TextAnnotation):
                        print('TEXTBOX ANNOTATIONS')
                        print('!!!!!!')
                        print(annotation.contents())

                        print(f'Page: {i}')
                        print('======')
                    else:
                        print('Not HighlightAnnotation but something else')
                        print('******')
        else:
            print('No annotations found')

def ex_main():
  input_filename = sys.argv[1]
  document = poppler.document_new_from_file('file://%s' % urllib.pathname2url(os.path.abspath(input_filename)), None)

  n_pages = document.get_n_pages()
  all_annots = 0

  for i in range(n_pages):
        page = document.get_page(i)
        annot_mappings = page.get_annot_mapping ()
        num_annots = len(annot_mappings)
        if num_annots > 0:
            for annot_mapping in annot_mappings:
                if  annot_mapping.annot.get_annot_type().value_name != 'POPPLER_ANNOT_LINK':
                    all_annots += 1
                    print('Page: {0:3}, {1:10}, type: {2:10}, content: {3}'.format(i+1, annot_mapping.annot.get_modified(), annot_mapping.annot.get_annot_type().value_nick, annot_mapping.annot.get_contents()))

  if all_annots > 0:
    print(str(all_annots) + " annotation(s) found")
  else:
    print("No annotations found")

if __name__ == "__main__":
    main()
