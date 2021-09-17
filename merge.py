# -*- coding: utf-8 -*-
import os 
from io import BytesIO
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

IMG_PATH = 'img-raw/example.png'
RAW_PDF_PATH = "/home/gly/workspace/pdf-utils/pdf-raw"
TARGET_PDF_PATH = "target/"
HEIGHT_SCALE = 5
WIDTH_SCALE = 10

def gen_pdf(pdf_path, pdf_name):
    print(os.path.join(pdf_path, pdf_name))

    img_path = IMG_PATH
    img_pdf = PdfFileWriter()
    
    # read raw pdf and write to new pdf
    raw_pdf = PdfFileReader(open(os.path.join(pdf_path, pdf_name), "rb"))
    page_nums = raw_pdf.getNumPages()
    output = PdfFileWriter()
    for num in range(0, page_nums):
        output.addPage(raw_pdf.getPage(num))
    
    # calculate width 
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
    imgDoc.drawImage(img_path, 10, 10, int(HEIGHT_SCALE/5), int(WIDTH_SCALE/10), mask='auto') # left bottom corner
    imgDoc.save()
    img_pdf.addPage(PdfFileReader(BytesIO(imgTemp.getvalue())).getPage(0))

    # merge
    last_page.mergePage(img_pdf.getPage(0))

    # write
    outputStream = open(os.path.join(TARGET_PDF_PATH, pdf_name), "wb")
    output.write(outputStream)
    outputStream.close()

def traverse():
    g = os.walk(RAW_PDF_PATH)
    for path,dir_list,file_list in g:
        for file_name in file_list:
            gen_pdf(RAW_PDF_PATH, file_name)

if __name__ == '__main__':
    traverse()