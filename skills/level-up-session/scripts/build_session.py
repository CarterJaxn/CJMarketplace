#!/usr/bin/env python3
"""
Level Up Session PDF Builder — Reusable Components

This module provides all the building blocks for generating Level Up leadership
program session PDFs. Import and compose these into session-specific scripts.

Usage:
    from build_session import *

    story = []
    story += cover_page("Session 03")
    # ... add tool pages ...
    build_pdf(story, "/path/to/output.pdf")
"""

from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.lib.colors import Color, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    Paragraph, Spacer, PageBreak, Table, TableStyle,
    Frame, PageTemplate, BaseDocTemplate, NextPageTemplate, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
import os

# ═══════════════════════════════════════════════════════════
# FONT REGISTRATION
# ═══════════════════════════════════════════════════════════

FONT_DIR = '/usr/share/fonts/truetype/crosextra'

def register_fonts():
    """Register Carlito font family (Century Gothic substitute)."""
    pdfmetrics.registerFont(TTFont('CG', f'{FONT_DIR}/Carlito-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('CGB', f'{FONT_DIR}/Carlito-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('CGI', f'{FONT_DIR}/Carlito-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('CGBI', f'{FONT_DIR}/Carlito-BoldItalic.ttf'))
    registerFontFamily('CG', normal='CG', bold='CGB', italic='CGI', boldItalic='CGBI')

register_fonts()

# ═══════════════════════════════════════════════════════════
# COLORS — exact values from Session 01
# ═══════════════════════════════════════════════════════════

BANNER      = Color(0.4431, 0.7333, 0.8353)  # #71BBD5 — section title banner fill
COVER_LINE  = Color(0.5451, 0.8157, 0.9137)  # #8BD0E9 — decorative lines, dark OB cells
CELL_LT     = Color(0.7098, 0.8824, 0.9451)  # #B5E1F1 — light cell backgrounds, phase boxes
HEADER_TINT = Color(0.8196, 0.9294, 0.9725)  # #D1EDF8 — very light header tint
DK_TEAL     = Color(0.1412, 0.4549, 0.5686)  # #247491 — section heading text
MD_TEAL     = Color(0.1882, 0.6078, 0.7569)  # #309BC1 — sub-labels, day headers

# ═══════════════════════════════════════════════════════════
# PAGE DIMENSIONS
# ═══════════════════════════════════════════════════════════

PAGE_W, PAGE_H = landscape(letter)  # 792 x 612
M = 0.55 * inch                      # margin
CW = PAGE_W - 2 * M                  # content width (~712.8)
CH = PAGE_H - 2 * M - 10             # content height (~522.8)

# ═══════════════════════════════════════════════════════════
# PARAGRAPH STYLES
# ═══════════════════════════════════════════════════════════

h18_banner = ParagraphStyle('H18BN', fontName='CGB', fontSize=18, leading=22,
                            textColor=BANNER, spaceAfter=6, spaceBefore=4)
h14_teal   = ParagraphStyle('H14T', fontName='CGB', fontSize=14, leading=17,
                            textColor=DK_TEAL, spaceAfter=4, spaceBefore=6)
h11_med    = ParagraphStyle('H11M', fontName='CGB', fontSize=11, leading=14,
                            textColor=MD_TEAL, spaceAfter=3, spaceBefore=4)
body       = ParagraphStyle('B', fontName='CG', fontSize=11, leading=14,
                            textColor=black, spaceAfter=3)
body10     = ParagraphStyle('B10', fontName='CG', fontSize=10, leading=13,
                            textColor=black, spaceAfter=3)
bodyi      = ParagraphStyle('BI', fontName='CGI', fontSize=11, leading=14,
                            textColor=black)
cellb      = ParagraphStyle('CB', fontName='CGB', fontSize=10, leading=12,
                            textColor=black)
cellr      = ParagraphStyle('CR', fontName='CG', fontSize=10, leading=12,
                            textColor=black)
cellb11    = ParagraphStyle('CB11', fontName='CGB', fontSize=11, leading=13,
                            textColor=black)

# ═══════════════════════════════════════════════════════════
# CUSTOM FLOWABLES
# ═══════════════════════════════════════════════════════════

class TealBanner(Flowable):
    """Section title banner — flat teal rectangle with white bold text."""

    def __init__(self, text, width=None, height=25):
        Flowable.__init__(self)
        self.text = text
        self._width = width or CW
        self.height = height

    def wrap(self, aW, aH):
        return self._width, self.height

    def draw(self):
        self.canv.setFillColor(BANNER)
        self.canv.rect(0, 0, self._width, self.height, fill=1, stroke=0)
        self.canv.setFillColor(white)
        self.canv.setFont('CGB', 14)
        self.canv.drawString(8, 7, self.text)


class BLines(Flowable):
    """Blank write-in lines for participant responses."""

    def __init__(self, n=3, width=None, lh=21):
        Flowable.__init__(self)
        self.n = n
        self._width = width or CW
        self.lh = lh

    def wrap(self, aW, aH):
        return self._width, self.n * self.lh

    def draw(self):
        self.canv.setStrokeColor(black)
        self.canv.setLineWidth(0.4)
        for i in range(self.n):
            y = self.n * self.lh - (i + 1) * self.lh + 2
            self.canv.line(0, y, self._width, y)


# ═══════════════════════════════════════════════════════════
# PAGE TEMPLATES
# ═══════════════════════════════════════════════════════════

_page_counter = [0]

def _on_content_page(canvas, doc):
    """Draw page number on content pages."""
    _page_counter[0] += 1
    pn = _page_counter[0] - 1  # subtract 1 because cover is page 0
    if pn > 0:
        canvas.saveState()
        canvas.setFont('CG', 9)
        canvas.setFillColor(black)
        canvas.drawRightString(PAGE_W - M, 20, str(pn))
        canvas.restoreState()


def _on_cover_page(canvas, doc):
    """Draw decorative lines on cover page."""
    canvas.saveState()
    canvas.setStrokeColor(COVER_LINE)
    canvas.setLineWidth(2)
    canvas.line(0, PAGE_H - 28, PAGE_W, PAGE_H - 28)  # top line
    canvas.line(0, 28, PAGE_W, 28)                      # bottom line
    canvas.restoreState()


# ═══════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════

def cover_page(session_label):
    """
    Generate cover page story elements.

    Args:
        session_label: e.g. "Session 03"

    Returns:
        List of Flowables for the cover page.
    """
    cover_style = ParagraphStyle(
        'CoverTitle', fontName='CGB', fontSize=24, leading=30,
        textColor=black, alignment=TA_CENTER
    )
    return [
        Spacer(1, 200),
        Paragraph(session_label, cover_style),
        NextPageTemplate('Content'),
        PageBreak(),
    ]


def opportunity_brief(rows_data, row_heights=None):
    """
    Generate an Opportunity Brief table.

    Args:
        rows_data: List of (label_paragraph, content) tuples.
                   label_paragraph should be a Paragraph with cellb/cellb11 style.
                   content can be '' (empty for write-in) or a Paragraph.
        row_heights: Optional list of row heights. If None, uses 45pt per row.

    Returns:
        List of Flowables.
    """
    table_data = [[label, content] for label, content in rows_data]
    if row_heights is None:
        row_heights = [45] * len(table_data)

    tbl = Table(table_data, colWidths=[188, CW - 188], rowHeights=row_heights)
    cmds = [
        ('GRID', (0, 0), (-1, -1), 0.5, black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]
    for i in range(len(table_data)):
        bg = COVER_LINE if i % 2 == 0 else CELL_LT
        cmds.append(('BACKGROUND', (0, i), (0, i), bg))

    tbl.setStyle(TableStyle(cmds))
    return [TealBanner("Opportunity Brief"), Spacer(1, 6), tbl, PageBreak()]


def five_phases(grid_content, phase5_content):
    """
    Generate Five Phases layout.

    Args:
        grid_content: List of [left_cell, right_cell] pairs for the 2-col grid.
                      Use Paragraph objects with cellr style, or '' for empty.
        phase5_content: Paragraph for the full-width phase 5 box.

    Returns:
        List of Flowables.
    """
    half = CW / 2 - 8
    grid_rows = [[left, right] for left, right in grid_content]
    row_heights = [72, 130, 120][:len(grid_rows)]

    grid = Table(grid_rows, colWidths=[half + 8, half + 8], rowHeights=row_heights)
    g_cmds = [
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]
    for r in range(len(grid_rows)):
        for c in range(2):
            if grid_rows[r][c] != '':
                g_cmds.append(('BACKGROUND', (c, r), (c, r), CELL_LT))
                g_cmds.append(('BOX', (c, r), (c, r), 0.5, black))
    grid.setStyle(TableStyle(g_cmds))

    p5 = Table([[phase5_content]], colWidths=[CW], rowHeights=[80])
    p5.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), CELL_LT),
        ('BOX', (0, 0), (0, 0), 0.5, black),
        ('VALIGN', (0, 0), (0, 0), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, 0), 8),
        ('TOPPADDING', (0, 0), (0, 0), 6),
    ]))

    return [
        TealBanner("Five Phases of Effective Delegation, Collaboration, & Accountability"),
        Spacer(1, 6),
        Paragraph("The Same 5 Steps Work for all 3", h14_teal),
        Spacer(1, 4),
        grid,
        Spacer(1, 6),
        p5,
        PageBreak(),
    ]


def ideal_week():
    """Generate Ideal Week grid page. Returns list of Flowables."""
    day_h = ParagraphStyle('DH', fontName='CGB', fontSize=14, leading=17,
                           textColor=MD_TEAL, alignment=TA_CENTER)
    row_h = ParagraphStyle('RH', fontName='CGB', fontSize=14, leading=17,
                           textColor=DK_TEAL)
    header = [Paragraph("", cellb)] + \
             [Paragraph(d, day_h) for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]]
    rows = [header] + [
        [Paragraph(f"<b>{r}</b>", row_h), '', '', '', '', '']
        for r in ["Morning", "Afternoon", "Daily"]
    ]
    tbl = Table(rows, colWidths=[80] + [(CW - 80) / 5] * 5,
                rowHeights=[24, 130, 130, 90])
    tbl.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (1, 0), (-1, 0), 'CENTER'),
    ]))
    return [
        TealBanner("My Ideal Week - What Would My Focus Be?"),
        Spacer(1, 10),
        tbl,
        Spacer(1, 10),
        Paragraph("Creating an \"Ideal\" rhythm:", h11_med),
        PageBreak(),
    ]


def ab_list(num_rows=25):
    """Generate A-B List worksheet. Returns list of Flowables."""
    abn = ParagraphStyle('ABN', fontName='CGB', fontSize=10.7, textColor=MD_TEAL)
    rows = []
    for i in range(1, num_rows + 1):
        rows.append([Paragraph(str(i), abn), '', Paragraph(str(i), abn), ''])

    tbl = Table(rows, colWidths=[28, CW / 2 - 28, 28, CW / 2 - 28],
                rowHeights=[16] * num_rows)
    cmds = [
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LINEAFTER', (1, 0), (1, -1), 0.5, black),
    ]
    for r in range(num_rows):
        cmds.append(('LINEBELOW', (0, r), (-1, r), 0.3, black))
    tbl.setStyle(TableStyle(cmds))

    return [TealBanner("My A - B List"), Spacer(1, 6), tbl]


def build_pdf(story, output_path):
    """
    Build the final PDF from a story (list of Flowables).

    Args:
        story: List of reportlab Flowables
        output_path: Where to save the PDF

    Returns:
        dict with page_count, file_size_kb, and page_titles
    """
    _page_counter[0] = 0  # reset counter

    doc = BaseDocTemplate(
        output_path,
        pagesize=landscape(letter),
        leftMargin=M, rightMargin=M,
        topMargin=M, bottomMargin=M + 10,
    )
    doc.addPageTemplates([
        PageTemplate(id='Cover', frames=[Frame(M, M + 10, CW, CH, id='c')],
                     onPage=_on_cover_page),
        PageTemplate(id='Content', frames=[Frame(M, M + 10, CW, CH, id='n')],
                     onPage=_on_content_page),
    ])

    doc.build(story)

    # Verify
    result = {
        'page_count': _page_counter[0],
        'file_size_kb': os.path.getsize(output_path) / 1024,
        'page_titles': [],
    }

    try:
        import pdfplumber
        with pdfplumber.open(output_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                title = text.split('\n')[0] if text else '[empty]'
                result['page_titles'].append(f"p{i+1}: {title}")
    except ImportError:
        pass

    return result
