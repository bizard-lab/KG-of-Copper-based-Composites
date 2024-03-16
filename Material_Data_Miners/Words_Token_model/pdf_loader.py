import importlib
import sys

importlib.reload(sys)

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams, LTTextBox, LTFigure, LTImage
from pdfminer.converter import PDFPageAggregator
import pandas as pd


def load_pdf(path):
    data = []
    with open(path, 'rb') as f:
        parser = PDFParser(f)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        wordsarr = []
        page_idx = 0
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            layout = device.get_result()
            line_num = 0
            for x in layout:
                # 获取文本对象
                if isinstance(x, LTTextBox):

                    text = x.get_text()

                    if len(text) > 0:

                        wordsarr.append({
                            'text': text.replace('\n', " "),
                            'page_num': page_idx,
                            'line_num': line_num
                        })
                line_num = line_num + 1
            page_idx = page_idx + 1

        for i in wordsarr:
            data.append({
                'doi': path,
                'text': i['text'],
                'page_num': i['page_num'],
                'line_num': i['line_num']
            })
        data = pd.DataFrame(data)
    return data
