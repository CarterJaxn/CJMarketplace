---
name: level-up-session
description: Generate Level Up leadership program session PDFs with exact brand-matched layout — teal banners, color palette, landscape letter format. Use this skill whenever the user mentions "Level Up session", "session PDF", "build a session", "generate session 03", or any request to create a new leadership program session document. Also trigger when the user references tools from the Level Up materials (e.g., "Opportunity Brief", "Ideal Week", "A-B List", "Success Clarity", "Five Phases", "Coaching and Feedback", "DiSC") in the context of building a session workbook. This skill is client-agnostic — it works for 4Patriots or any future client.
---

# Level Up Session PDF Generator

You are building a PDF for the **Level Up** leadership development program, run by M2 Consulting. Each session is a workbook-style document containing a curated set of tools from the master materials library.

## When to Use This Skill

Any time the user asks to generate a Level Up session PDF. The request will typically include a session number and a list of tools to include. If the user doesn't specify tools, ask which ones they want — check `references/tool-index.md` for the full catalog.

## Key Concepts

- **Session**: A numbered workbook (Session 01, Session 02, etc.) containing 4-8 tools
- **Tool**: A leadership exercise from the master library (e.g., Success Clarity, Opportunity Brief, Ideal Week). Each tool becomes one or more pages in the PDF.
- **Client**: The company receiving the program. Currently 4Patriots, but the skill must work for any client. The cover page should just say "Session NN" — no company name baked in.

## Build Process

### Step 1: Gather Requirements

Confirm with the user:
1. **Session number** (e.g., "Session 03")
2. **Tools to include** — reference `references/tool-index.md` for the full list with categories and time estimates
3. **Any modifications** to standard tools (custom questions, different framing)

### Step 2: Extract Tool Content

Each tool's raw content lives in the source PDFs. Use `pdfplumber` to extract text from:

- **Master materials**: `LevelUp Archive 2-7/4P Level UP Materials.pdf` (64 pages — the canonical tool library)
- **Previous sessions**: `LevelUp Archive 2-7/4P Level Up Session NN.pdf` (for tools already formatted in past sessions — copy the structure)
- **Supplemental materials**: `Level Up Materials/` folder for newer tools (Sessions 09, 10, etc.)
- **Ideal Week specifically**: `LevelUp Archive 2-7/4P Level Up Session 06 Ideal Week_8-9-24.pdf`

The tool index in `references/tool-index.md` maps tool names to categories. To find the right pages, search the master materials PDF for the tool name.

### Step 3: Generate the PDF

Use the bundled build script at `scripts/build_session.py`. This script provides all layout components as importable building blocks. Read it to understand what's available, then write a session-specific script that composes tools into pages.

**The standard approach:**

1. Read `scripts/build_session.py` to load all components
2. Write a session-specific script that imports from it and assembles the story
3. Run the script to generate the PDF
4. Verify the output

The build script provides these core components:
- `TealBanner(text)` — section title banner
- `BLines(n)` — blank write-in lines
- Color constants: `BANNER`, `COVER_LINE`, `CELL_LT`, `HEADER_TINT`, `DK_TEAL`, `MD_TEAL`
- Paragraph styles: `h18_banner`, `h14_teal`, `h11_med`, `body`, `body10`, `bodyi`, `cellb`, `cellr`, `cellb11`
- Page templates with automatic numbering (cover has no number, content pages start at 1)
- Helper function `cover_page(session_label)` — returns story elements for the cover

Each tool needs custom page composition because the content and layout varies. The common patterns:

**Pattern A — Intro + Questions + Write Space:**
```
TealBanner("Tool Name")
Spacer
Intro paragraph(s)
"Check-in:" heading (h14_teal) + questions
"Exercise:" heading (h14_teal) + instructions
"Debrief:" heading + questions
BLines(n) for write space
PageBreak
```

**Pattern B — Structured Form (like Opportunity Brief):**
```
TealBanner("Tool Name")
Table with label column (188pt, alternating COVER_LINE/CELL_LT) + content column
PageBreak
```

**Pattern C — Grid Layout (like Five Phases):**
```
TealBanner("Tool Name")
2-column Table with CELL_LT background boxes
Full-width box at bottom
PageBreak
```

**Pattern D — Worksheet (like A-B List, Ideal Week):**
```
TealBanner("Tool Name")
Grid table for participant input
PageBreak
```

### Step 4: Verify Output

After generating:
1. Check page count matches expected (cover + pages per tool)
2. Use pdfplumber to print first line of each page
3. Confirm file size is reasonable (30-80 KB typical)
4. If possible, take a screenshot to visually confirm layout

## Design Spec (Quick Reference)

The full spec is in `references/design-spec.md`. Critical elements:

### Page Format
- **Landscape letter**: 792 x 612 pt
- **Margins**: ~0.55" all sides
- **Font**: Carlito TTF (Century Gothic substitute) — Regular, Bold, Italic, BoldItalic

### Color Palette

| Name | RGB (0-1) | Hex | Use |
|------|-----------|-----|-----|
| Banner fill | (0.443, 0.733, 0.835) | #71BBD5 | Section title banners |
| Cover lines | (0.545, 0.816, 0.914) | #8BD0E9 | Decorative lines, dark table cells |
| Cell light | (0.710, 0.882, 0.945) | #B5E1F1 | Highlights, phase boxes |
| Header tint | (0.820, 0.929, 0.973) | #D1EDF8 | Very light headers |
| Dark teal | (0.141, 0.455, 0.569) | #247491 | Section heading text |
| Medium teal | (0.188, 0.608, 0.757) | #309BC1 | Sub-labels, numbers |
| Body | (0, 0, 0) | #000000 | All body text — pure black |

### Critical Layout Rules
- **TealBanner**: 25pt flat rectangle, white CGB 14pt text, 8pt left padding
- **Page numbers**: Bottom-right, CG 9pt black. Cover = no number. Content = 1, 2, 3...
- **Tables**: 0.5pt black grid lines
- **Blank lines**: 0.4pt black, ~21pt vertical spacing
- **Watch for overflow** — this is the #1 issue. Always calculate total content height vs available space (~490pt content height per page). If tight, reduce spacing or split across pages.

## Troubleshooting

**Content overflows page**: Reduce row heights, spacers, or font sizes. The available content height is approximately 490pt per page. Calculate total heights before building.

**Bullet characters render as (cid:NNN)**: Use `-` dashes instead of `•` bullets. Carlito doesn't render the bullet Unicode glyph reliably.

**Font not found**: Carlito is at `/usr/share/fonts/truetype/crosextra/Carlito-*.ttf`. If the sandbox doesn't have it, install with: `apt-get install -y fonts-crosextra-carlito`

**PDF looks "off" compared to reference**: Check that you're using the exact RGB values above, not approximations. The difference between #4BACC6 and #71BBD5 is visible.
