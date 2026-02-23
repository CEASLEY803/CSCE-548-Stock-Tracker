from docx import Document

doc = Document("Project 2.docx")
for paragraph in doc.paragraphs:
    print(paragraph.text)
