import io
import logging
import os
from html import escape
from html.parser import HTMLParser

if os.name != 'nt':
    try:
        from weasyprint import HTML, CSS
        WEASYPRINT_INSTALLED = True
    except Exception:
        HTML = None
        CSS = None
        WEASYPRINT_INSTALLED = False
else:
    HTML = None
    CSS = None
    WEASYPRINT_INSTALLED = False

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
    REPORTLAB_INSTALLED = True
except ImportError:
    REPORTLAB_INSTALLED = False

logger = logging.getLogger('ats_resume_scorer')


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self._ignored_tags = 0

    def handle_starttag(self, tag, attrs):
        if tag in {'style', 'script'}:
            self._ignored_tags += 1
        elif tag in {'br', 'p', 'div', 'li', 'h1', 'h2', 'h3'}:
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in {'style', 'script'} and self._ignored_tags:
            self._ignored_tags -= 1

    def handle_data(self, data):
        if self._ignored_tags:
            return
        text = ' '.join(data.split())
        if text:
            self.parts.append(text)


def _generate_reportlab_pdf(html_docs: dict[str, str]) -> bytes:
    if not REPORTLAB_INSTALLED:
        raise ImportError(
            'PDF generation requires WeasyPrint with GTK/Pango or the reportlab package.'
        )

    output = io.BytesIO()
    document = SimpleDocTemplate(
        output,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
    )
    styles = getSampleStyleSheet()
    story = []
    for name, html_str in html_docs.items():
        extractor = _TextExtractor()
        extractor.feed(html_str)
        story.append(Paragraph(name.replace('_', ' ').title(), styles['Title']))
        story.append(Spacer(1, 6 * mm))
        for text in extractor.parts:
            if text == '\n':
                story.append(Spacer(1, 2 * mm))
                continue
            story.append(Paragraph(escape(text), styles['BodyText']))
            story.append(Spacer(1, 2 * mm))
        story.append(Spacer(1, 6 * mm))
    document.build(story)
    return output.getvalue()


def generate_combined_pdf(html_docs: dict[str, str]) -> bytes:
    if not WEASYPRINT_INSTALLED:
        return _generate_reportlab_pdf(html_docs)
        
    documents = []
    
    # Render all 3 HTML strings to WeasyPrint Document objects
    for name, html_str in html_docs.items():
        doc = HTML(string=html_str).render()
        documents.append(doc)
    
    # Merge them into the first document
    first_doc = documents[0]
    for other_doc in documents[1:]:
        for page in other_doc.pages:
            first_doc.pages.append(page)
            
    # Write combined PDF bytes
    pdf_bytes = first_doc.write_pdf()
    return pdf_bytes