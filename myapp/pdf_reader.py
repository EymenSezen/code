from dataclasses import dataclass
import datetime
import re
from typing import List

from pdfminer.high_level import extract_text


@dataclass
class PDFInfo:
    project_name: str
    authors: List[List[str]]
    lesson: str
    project_title: str
    supervisor: str
    juries: List[str]
    date: datetime.date
    summary: str
    keywords: List[str]
    term: str


def read_pdf(filename) -> PDFInfo:
    text = extract_text(filename)
    print(text)
    authors = re.findall("Öğrenci No:([^.]*)\nAdı Soyadı:([^.]*)\n", text)
    project_name = re.search(f"LİSANS TEZİ\\s*(.*?)\n{authors[0][1].strip()}", text, re.DOTALL).group(1).replace('\n', ' ')

    # [['12122', 'isim'], ['433434', 'isim']]
    lesson = re.findall("BİLGİSAYAR MÜHENDİSLİĞİ BÖLÜMÜ\\s*(.*?)\n", text)[1]
    project_title = re.search(f"{lesson}\\s*(.*?)\n{authors[0][1].strip()}", text, re.DOTALL).group(1).replace('\n',' ')
    supervisor = re.search("(.*?)\nDanışman", text).group(1)
    juries = re.findall("(.*?)\nJüri Üyesi", text)
    date = re.search("Tezin Savunulduğu Tarih:\\s*(.*?)\n", text).group(1)
    date = datetime.datetime.strptime(date, "%d.%m.%Y").date()
    month = str(date)[6]
    month = int(month)
    if month == 1:
        term = "Güz Dönemi"
    else:
        term = "Bahar Dönemi"

    summary = re.search("\\s*ÖZET\\s*\n(.*?)Anahtar kelimeler:", text, re.DOTALL).group(
        1
    )
    keywords = list(
        map(
            lambda e: e.strip(),
            re.search("Anahtar kelimeler:([^.]*)\\.?", text).group(1).split(","),
        )
    )

    return PDFInfo(
        project_name,
        authors,
        lesson,
        project_title,
        supervisor,
        juries,
        date,
        summary,
        keywords,
        term,
    )


# print(read_pdf("copy.pdf"))
