import re
from typing import Union
from fpdf import FPDF


def make_pdf(article_title: str, article_text: str, article_image: Union[str, None]) -> str:
    """
    Creates a pdf file containing the chosen article.

    Returns the file name as a string
    """

    pdf = FPDF()
    file_name = "./assets/fonts/07558_CenturyGothic.ttf"

    pdf.add_font("TNR", "", file_name, uni=True)
    pdf.add_font("TNRB", "", file_name, uni=True)
    pdf.set_margins(30, 23, 30)
    pdf.add_page()

    # create title
    pdf.set_font("TNRB", size=28)
    pdf.multi_cell(150, 12, txt=article_title, align="L")

    if isinstance(article_image, str):
        # insert image
        pdf.cell(150, 5, ln=2)
        pdf.set_y(pdf.get_y())
        pdf.image(article_image, w=(pdf.w - 60))
        pdf.cell(150, 5, ln=2)
    else:
        # insert line break
        pdf.cell(150, 7, ln=2)

    # create text
    # TODO change to aa font that supports macrons
    pdf.set_font("TNR", size=12)
    pdf.set_y(pdf.get_y())
    pdf.multi_cell(150, 8, txt=article_text, align="L")

    article_title = re.sub(r"[^a-zA-Z0-9]", "", article_title)
    article_title = article_title.replace(" ", "")

    # save the pdf as article_title.pdf
    import os
    os.mkdir("./assets/articles/")
    file = f"./assets/articles/{article_title}.pdf"
    pdf.output(file)

    # returns the file name as a string
    return file
