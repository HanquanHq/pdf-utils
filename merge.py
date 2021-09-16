# -*- coding: utf-8 -*-
import cv2
from io import BytesIO
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

IMG_PATH = 'img-raw/example.png'
RAW_PDF_PATH = "pdf-raw/test.pdf"
TARGET_PDF_PATH = "target/output.pdf"
HEIGHT_SCALE = 5
WIDTH_SCALE = 10

def gen_pdf():
    path = IMG_PATH
    img_pdf = PdfFileWriter()
    
    # read raw pdf and write to new pdf
    raw_pdf = PdfFileReader(open(RAW_PDF_PATH, "rb"))
    page_nums = raw_pdf.getNumPages()
    output = PdfFileWriter()
    for num in range(0, page_nums):
        output.addPage(raw_pdf.getPage(num))
    
    # calcute width 
    last_page = output.getPage(page_nums - 1)
    if last_page.get('/Rotate', 0) in [90, 270]:
        height, width = last_page['/MediaBox'][2], last_page['/MediaBox'][3]
    else:
        height, width = last_page['/MediaBox'][3], last_page['/MediaBox'][2]
    print(height)
    print(width)

    # convert img to pdf
    imgTemp = BytesIO()
    imgDoc = canvas.Canvas(imgTemp, pagesize=A4)
    # imgDoc.setFillAlpha(0.1) # image transparency
    imgDoc.drawImage(path, 10, 10, int(HEIGHT_SCALE/5), int(WIDTH_SCALE/10), mask='auto') # left bottom corner
    imgDoc.save()
    img_pdf.addPage(PdfFileReader(BytesIO(imgTemp.getvalue())).getPage(0))

    # merge
    last_page.mergePage(img_pdf.getPage(0))

    # write
    outputStream = open(TARGET_PDF_PATH, "wb")
    output.write(outputStream)
    outputStream.close()


if __name__ == '__main__':
    # resize()
    gen_pdf()