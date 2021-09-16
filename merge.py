# -*- coding: utf-8 -*-
from io import BytesIO
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def gen_pdf():
    path = 'img-raw/chrome.png'
    new_pdf = PdfFileWriter()

    for num in range(1, 3):  # for each slide
        # Using ReportLab Canvas to insert image into PDF
        imgTemp = BytesIO()
        imgDoc = canvas.Canvas(imgTemp, pagesize=A4)
        # Draw image on Canvas and save PDF in buffer
        imgDoc.drawImage(path.format(num), -0, -0) # from left bottom corner
        # x, y - start position
        imgDoc.save()
        # Use PyPDF to merge the image-PDF into the template
        new_pdf.addPage(PdfFileReader(BytesIO(imgTemp.getvalue())).getPage(0))
    
    existing_pdf = PdfFileReader(open("pdf-raw/test.pdf", "rb"))
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))

    output = PdfFileWriter()
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open("output.pdf", "wb")
    output.write(outputStream)
    outputStream.close()


if __name__ == '__main__':
    gen_pdf()