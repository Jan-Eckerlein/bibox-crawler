import os
from fpdf import FPDF
import os

def create_pdf():
    pdf = FPDF()

    imagelist = os.listdir('./images/')    
    # imagelist is the list with all image filenames
    for image in imagelist:
        pdf.add_page()
        pdf.image('images/' + image, 0, 0, 211)
        break
    pdf.output("output/yourfile.pdf", "F")
