# Level Up Session PDF — Full Design Specification

Reverse-engineered from Session 01 and validated against Session 02.

## Page Dimensions

- Orientation: Landscape letter
- Size: 792 x 612 pt (11" x 8.5")
- Margins: 0.55" all sides (M = 0.55 * 72 = 39.6 pt)
- Content width (CW): 792 - 2*39.6 = 712.8 pt
- Content height (CH): 612 - 2*39.6 - 10 = 522.8 pt (10pt reserved for page number area)
- Usable content height per page: ~490 pt (accounting for frame padding)

## Fonts

| Weight | reportlab Name | TTF Path |
|--------|---------------|----------|
| Regular | CG | /usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf |
| Bold | CGB | /usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf |
| Italic | CGI | /usr/share/fonts/truetype/crosextra/Carlito-Italic.ttf |
| Bold Italic | CGBI | /usr/share/fonts/truetype/crosextra/Carlito-BoldItalic.ttf |

Register family as 'CG' with bold='CGB', italic='CGI', boldItalic='CGBI'.

The original documents use Century Gothic. Carlito is a metrically-compatible substitute that works with reportlab's TTFont loader (unlike URW Gothic OTF files which have CFF outlines and are incompatible).

## Color Palette (exact values)

```python
BANNER     = Color(0.4431, 0.7333, 0.8353)  # #71BBD5 — section title banner fill
COVER_LINE = Color(0.5451, 0.8157, 0.9137)  # #8BD0E9 — cover decorative lines, dark OB cells
CELL_LT    = Color(0.7098, 0.8824, 0.9451)  # #B5E1F1 — light cell backgrounds, phase boxes
HEADER_TINT= Color(0.8196, 0.9294, 0.9725)  # #D1EDF8 — very light header tint
DK_TEAL    = Color(0.1412, 0.4549, 0.5686)  # #247491 — section heading text
MD_TEAL    = Color(0.1882, 0.6078, 0.7569)  # #309BC1 — sub-labels, day headers, list numbers
```

These were extracted from Session 01 using pdfplumber color analysis. Do NOT approximate — the exact values matter for visual consistency.

## Paragraph Styles

| Style Name | Font | Size | Leading | Color | Use |
|-----------|------|------|---------|-------|-----|
| h18_banner | CGB | 18pt | 22pt | BANNER | Large teal headings (rare) |
| h14_teal | CGB | 14pt | 17pt | DK_TEAL | Section sub-headings (Check-in:, Exercise:, Debrief:) |
| h11_med | CGB | 11pt | 14pt | MD_TEAL | Minor headings |
| body | CG | 11pt | 14pt | black | Standard body text |
| body10 | CG | 10pt | 13pt | black | Slightly smaller body (for dense content) |
| bodyi | CGI | 11pt | 14pt | black | Italic body text |
| cellb | CGB | 10pt | 12pt | black | Bold table cell text |
| cellr | CG | 10pt | 12pt | black | Regular table cell text |
| cellb11 | CGB | 11pt | 13pt | black | Larger bold cell text |

## Component Specifications

### TealBanner
- Height: 25pt
- Fill: BANNER color
- No rounded corners (flat rectangle)
- Text: white, CGB 14pt, drawString at x=8, y=7
- Width: spans full content area (CW)
- No stroke

### Page Numbering
- Cover page: NO page number
- Content pages: numbered starting at 1
- Position: bottom-right corner
- Font: CG 9pt, black
- x position: PAGE_W - M (right-aligned)
- y position: 20pt from bottom

### Cover Page
- Decorative horizontal lines at top and bottom of page (full page width, not just content area)
- Line color: COVER_LINE
- Line width: 2pt
- Top line: y = PAGE_H - 28
- Bottom line: y = 28
- Session label: centered, CGB 24pt, black
- Spacer of ~200pt above the session label to center it vertically

### Blank Write-In Lines (BLines)
- Line weight: 0.4pt
- Line color: black
- Vertical spacing: ~21pt between lines
- Full content width

### Tables
- Grid lines: 0.5pt black
- Cell padding: left=6pt, top=4pt, bottom=3pt
- Vertical alignment: TOP

### Opportunity Brief Table
- Label column width: 188pt
- Content column: remaining width (CW - 188)
- Row backgrounds alternate: COVER_LINE (even rows) / CELL_LT (odd rows) on label column only
- Each row has specific height tuned to content (~40-75pt per row)
- Total must fit within ~490pt

### Five Phases Layout
- 2-column grid
- Column width: CW/2 - 8 (with 16pt gutter)
- Cell background: CELL_LT
- Cell border: 0.5pt black BOX (not full grid)
- Phase 5: full-width box at bottom
- Row heights vary: ~72pt, ~130pt, ~120pt for main grid; ~80pt for phase 5

### A-B List
- 25 rows
- 4 columns: [number(28pt), content(CW/2-28), number(28pt), content(CW/2-28)]
- Row height: 16pt
- Numbers: CGB 10.7pt, MD_TEAL color
- Horizontal rules: 0.3pt black between rows
- Vertical divider: 0.5pt black between A and B columns

### Ideal Week Grid
- Columns: label(80pt) + 5 day columns ((CW-80)/5 each)
- Rows: header(24pt) + Morning(130pt) + Afternoon(130pt) + Daily(90pt)
- Day headers: CGB 14pt, MD_TEAL, centered
- Row labels: CGB 14pt, DK_TEAL
- Grid: 0.5pt black
