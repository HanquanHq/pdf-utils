# -*- coding: utf-8 -*-
import cv2
from io import BytesIO
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

img_path = 'img-raw/1.png'
raw_pdf_path = "pdf-raw/test.pdf"
target_pdf_path = "target/output.pdf"

def resize():
    src = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    scale_percent = 50
    width = int(src.shape[1] * scale_percent / 100)
    height = int(src.shape[0] * scale_percent / 100)
    dsize = (width, height)
    output = cv2.resize(src, dsize)
    cv2.imwrite(img_path, output)

def gen_pdf():
    path = img_path
    img_pdf = PdfFileWriter()
    
    # convert img to pdf
    imgTemp = BytesIO()
    imgDoc = canvas.Canvas(imgTemp, pagesize=A4)
    imgDoc.drawImage(path.format(0), 0, 0) # left bottom corner
    imgDoc.save()
    img_pdf.addPage(PdfFileReader(BytesIO(imgTemp.getvalue())).getPage(0))

    # read raw pdf and write to new pdf
    raw_pdf = PdfFileReader(open(raw_pdf_path, "rb"))
    page_nums = raw_pdf.getNumPages()
    output = PdfFileWriter()
    for num in range(0, page_nums):
        output.addPage(raw_pdf.getPage(num))

    # merge
    output.getPage(page_nums - 1).mergePage(img_pdf.getPage(0))

    # write
    outputStream = open(target_pdf_path, "wb")
    output.write(outputStream)
    outputStream.close()


if __name__ == '__main__':
    resize()
    gen_pdf()