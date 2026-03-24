#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project Architecture Design Document PDF Generator (Template)
项目架构设计文档 PDF 生成器（模板）

Usage:
    This is a TEMPLATE script. Claude should:
    1. Copy this file to the target project root directory
    2. Fill in the document content sections with actual analysis results
    3. Execute the script to generate the PDF
    4. Delete the temporary copy

The script provides:
    - Chinese font registration (macOS / Linux / Windows)
    - PDF page layout and styles
    - Reusable drawing utilities for diagrams (boxes, arrows, flowcharts, sequence diagrams)
    - Chapter and section formatting
    - Table rendering
    - Code block rendering

Dependencies:
    pip3 install reportlab
"""

import os
import sys
import platform
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable, Flowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.graphics import renderPDF


# =============================================================================
# Section 0: Configuration — MODIFY THESE FOR EACH PROJECT
# =============================================================================

# Output PDF file path (relative to script location or absolute)
OUTPUT_PDF = "Project_Module_Design_Document.pdf"

# Document title shown on the cover page
DOC_TITLE = "项目模块架构设计文档"

# Document subtitle
DOC_SUBTITLE = "核心架构设计 · 设计模式 · 流程图 · 时序图 · 调用链"

# Module name for headers
MODULE_NAME = "Module Name"

# Author info
AUTHOR = "AI Architecture Analyzer"

# Page margins
LEFT_MARGIN = 2.0 * cm
RIGHT_MARGIN = 2.0 * cm
TOP_MARGIN = 2.0 * cm
BOTTOM_MARGIN = 2.0 * cm


# =============================================================================
# Section 1: Font Registration
# =============================================================================

def register_fonts():
    """Register Chinese fonts based on the operating system."""
    system = platform.system()

    font_candidates = {
        'Darwin': [
            ('/System/Library/Fonts/STHeiti Light.ttc', 0),
            ('/System/Library/Fonts/Hiragino Sans GB.ttc', 0),
            ('/System/Library/Fonts/PingFang.ttc', 0),
            ('/Library/Fonts/Arial Unicode.ttf', None),
        ],
        'Linux': [
            ('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 0),
            ('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 0),
            ('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 0),
        ],
        'Windows': [
            ('C:/Windows/Fonts/msyh.ttc', 0),
            ('C:/Windows/Fonts/simhei.ttf', None),
            ('C:/Windows/Fonts/simsun.ttc', 0),
        ],
    }

    candidates = font_candidates.get(system, [])
    for path, subfont_index in candidates:
        if os.path.exists(path):
            try:
                if subfont_index is not None:
                    pdfmetrics.registerFont(TTFont('ChineseFont', path, subfontIndex=subfont_index))
                    pdfmetrics.registerFont(TTFont('ChineseFontBold', path, subfontIndex=subfont_index))
                else:
                    pdfmetrics.registerFont(TTFont('ChineseFont', path))
                    pdfmetrics.registerFont(TTFont('ChineseFontBold', path))
                print(f"已注册字体: {path}")
                return True
            except Exception as e:
                print(f"字体注册失败 {path}: {e}")
                continue

    print("警告: 未找到中文字体，将使用默认字体（中文可能显示为方块）")
    return False


HAS_CHINESE_FONT = register_fonts()


# =============================================================================
# Section 2: Style Definitions
# =============================================================================

def get_font_name():
    return 'ChineseFont' if HAS_CHINESE_FONT else 'Helvetica'


def get_font_name_bold():
    return 'ChineseFontBold' if HAS_CHINESE_FONT else 'Helvetica-Bold'


def create_styles():
    """Create all paragraph styles used in the document."""
    styles = getSampleStyleSheet()
    font = get_font_name()
    font_bold = get_font_name_bold()

    custom_styles = {}

    # Cover page title
    custom_styles['CoverTitle'] = ParagraphStyle(
        'CoverTitle', parent=styles['Title'],
        fontName=font_bold, fontSize=28, leading=36,
        alignment=TA_CENTER, spaceAfter=12,
        textColor=colors.HexColor('#1a1a2e'),
    )

    # Cover subtitle
    custom_styles['CoverSubtitle'] = ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName=font, fontSize=14, leading=20,
        alignment=TA_CENTER, spaceAfter=6,
        textColor=colors.HexColor('#4a4a6a'),
    )

    # Chapter title (e.g., "第1章 模块概述")
    custom_styles['ChapterTitle'] = ParagraphStyle(
        'ChapterTitle', parent=styles['Heading1'],
        fontName=font_bold, fontSize=20, leading=28,
        spaceBefore=20, spaceAfter=12,
        textColor=colors.HexColor('#16213e'),
        borderWidth=0, borderPadding=0,
        leftIndent=0,
    )

    # Section title (e.g., "1.1 架构概览")
    custom_styles['SectionTitle'] = ParagraphStyle(
        'SectionTitle', parent=styles['Heading2'],
        fontName=font_bold, fontSize=15, leading=22,
        spaceBefore=14, spaceAfter=8,
        textColor=colors.HexColor('#1a1a5e'),
    )

    # Sub-section title (e.g., "1.1.1 分层设计")
    custom_styles['SubSectionTitle'] = ParagraphStyle(
        'SubSectionTitle', parent=styles['Heading3'],
        fontName=font_bold, fontSize=13, leading=18,
        spaceBefore=10, spaceAfter=6,
        textColor=colors.HexColor('#2d2d7e'),
    )

    # Body text
    custom_styles['BodyText'] = ParagraphStyle(
        'BodyText', parent=styles['Normal'],
        fontName=font, fontSize=10.5, leading=17,
        spaceBefore=3, spaceAfter=6,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#333333'),
    )

    # Bullet list item
    custom_styles['BulletItem'] = ParagraphStyle(
        'BulletItem', parent=styles['Normal'],
        fontName=font, fontSize=10.5, leading=16,
        leftIndent=20, bulletIndent=8,
        spaceBefore=2, spaceAfter=2,
        textColor=colors.HexColor('#333333'),
    )

    # Code block text
    custom_styles['CodeBlock'] = ParagraphStyle(
        'CodeBlock', parent=styles['Code'],
        fontName='Courier', fontSize=9, leading=13,
        leftIndent=12, rightIndent=12,
        spaceBefore=6, spaceAfter=6,
        backColor=colors.HexColor('#f5f5f5'),
        borderWidth=0.5, borderColor=colors.HexColor('#ddd'),
        borderPadding=8,
        textColor=colors.HexColor('#2d2d2d'),
    )

    # Table header text
    custom_styles['TableHeader'] = ParagraphStyle(
        'TableHeader', parent=styles['Normal'],
        fontName=font_bold, fontSize=10, leading=14,
        alignment=TA_CENTER,
        textColor=colors.white,
    )

    # Table cell text
    custom_styles['TableCell'] = ParagraphStyle(
        'TableCell', parent=styles['Normal'],
        fontName=font, fontSize=9.5, leading=14,
        textColor=colors.HexColor('#333333'),
    )

    # Table cell centered
    custom_styles['TableCellCenter'] = ParagraphStyle(
        'TableCellCenter', parent=styles['Normal'],
        fontName=font, fontSize=9.5, leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#333333'),
    )

    # Highlight / callout text
    custom_styles['Highlight'] = ParagraphStyle(
        'Highlight', parent=styles['Normal'],
        fontName=font_bold, fontSize=10.5, leading=16,
        spaceBefore=4, spaceAfter=4,
        textColor=colors.HexColor('#0f3460'),
    )

    # Caption text (for diagrams)
    custom_styles['Caption'] = ParagraphStyle(
        'Caption', parent=styles['Normal'],
        fontName=font, fontSize=9, leading=13,
        alignment=TA_CENTER, spaceBefore=4, spaceAfter=10,
        textColor=colors.HexColor('#666666'),
    )

    return custom_styles


STYLES = create_styles()


# =============================================================================
# Section 3: Reusable Drawing Utilities
# =============================================================================

class BoxFlowable(Flowable):
    """A colored box with text, used for architecture diagram nodes."""

    def __init__(self, text, width=120, height=30,
                 bg_color='#e8f4fd', border_color='#2196F3',
                 text_color='#1565C0', font_size=9):
        super().__init__()
        self.text = text
        self.box_width = width
        self.box_height = height
        self.bg_color = colors.HexColor(bg_color)
        self.border_color = colors.HexColor(border_color)
        self.text_color = colors.HexColor(text_color)
        self.font_size = font_size
        self.width = width
        self.height = height

    def draw(self):
        self.canv.setFillColor(self.bg_color)
        self.canv.setStrokeColor(self.border_color)
        self.canv.setLineWidth(1)
        self.canv.roundRect(0, 0, self.box_width, self.box_height, 4, fill=1)
        self.canv.setFillColor(self.text_color)
        self.canv.setFont(get_font_name(), self.font_size)
        text_width = self.canv.stringWidth(self.text, get_font_name(), self.font_size)
        x = (self.box_width - text_width) / 2
        y = (self.box_height - self.font_size) / 2
        self.canv.drawString(x, y, self.text)


class DiagramFlowable(Flowable):
    """
    A generic diagram flowable that renders a list of drawing instructions.

    Instructions format:
    [
        ('rect', x, y, w, h, fill_color, border_color),
        ('text', x, y, text, font_size, color),
        ('line', x1, y1, x2, y2, color, width),
        ('arrow', x1, y1, x2, y2, color, width),
        ('dashed', x1, y1, x2, y2, color, width),
        ('roundrect', x, y, w, h, r, fill_color, border_color),
    ]
    """

    def __init__(self, width, height, instructions):
        super().__init__()
        self.width = width
        self.height = height
        self.instructions = instructions

    def draw(self):
        c = self.canv
        for instr in self.instructions:
            cmd = instr[0]
            try:
                if cmd == 'rect':
                    _, x, y, w, h, fill, border = instr
                    c.setFillColor(colors.HexColor(fill))
                    c.setStrokeColor(colors.HexColor(border))
                    c.setLineWidth(1)
                    c.rect(x, y, w, h, fill=1)
                elif cmd == 'roundrect':
                    _, x, y, w, h, r, fill, border = instr
                    c.setFillColor(colors.HexColor(fill))
                    c.setStrokeColor(colors.HexColor(border))
                    c.setLineWidth(1)
                    c.roundRect(x, y, w, h, r, fill=1)
                elif cmd == 'text':
                    _, x, y, text, font_size, color = instr
                    c.setFillColor(colors.HexColor(color))
                    c.setFont(get_font_name(), font_size)
                    c.drawString(x, y, text)
                elif cmd == 'text_center':
                    _, x, y, text, font_size, color = instr
                    c.setFillColor(colors.HexColor(color))
                    c.setFont(get_font_name(), font_size)
                    tw = c.stringWidth(text, get_font_name(), font_size)
                    c.drawString(x - tw / 2, y, text)
                elif cmd == 'text_bold':
                    _, x, y, text, font_size, color = instr
                    c.setFillColor(colors.HexColor(color))
                    c.setFont(get_font_name_bold(), font_size)
                    c.drawString(x, y, text)
                elif cmd == 'text_center_bold':
                    _, x, y, text, font_size, color = instr
                    c.setFillColor(colors.HexColor(color))
                    c.setFont(get_font_name_bold(), font_size)
                    tw = c.stringWidth(text, get_font_name_bold(), font_size)
                    c.drawString(x - tw / 2, y, text)
                elif cmd == 'text_code':
                    _, x, y, text, font_size, color = instr
                    c.setFillColor(colors.HexColor(color))
                    c.setFont('Courier', font_size)
                    c.drawString(x, y, text)
                elif cmd == 'line':
                    _, x1, y1, x2, y2, color_val, width = instr
                    c.setStrokeColor(colors.HexColor(color_val))
                    c.setLineWidth(width)
                    c.line(x1, y1, x2, y2)
                elif cmd == 'arrow':
                    _, x1, y1, x2, y2, color_val, width = instr
                    c.setStrokeColor(colors.HexColor(color_val))
                    c.setFillColor(colors.HexColor(color_val))
                    c.setLineWidth(width)
                    c.line(x1, y1, x2, y2)
                    # Draw arrowhead
                    import math
                    angle = math.atan2(y2 - y1, x2 - x1)
                    arrow_len = 8
                    arrow_angle = 0.4
                    ax1 = x2 - arrow_len * math.cos(angle - arrow_angle)
                    ay1 = y2 - arrow_len * math.sin(angle - arrow_angle)
                    ax2 = x2 - arrow_len * math.cos(angle + arrow_angle)
                    ay2 = y2 - arrow_len * math.sin(angle + arrow_angle)
                    p = c.beginPath()
                    p.moveTo(x2, y2)
                    p.lineTo(ax1, ay1)
                    p.lineTo(ax2, ay2)
                    p.close()
                    c.drawPath(p, fill=1)
                elif cmd == 'dashed':
                    _, x1, y1, x2, y2, color_val, width = instr
                    c.setStrokeColor(colors.HexColor(color_val))
                    c.setLineWidth(width)
                    c.setDash(4, 3)
                    c.line(x1, y1, x2, y2)
                    c.setDash()  # Reset
                elif cmd == 'ellipse':
                    _, x, y, w, h, fill, border = instr
                    c.setFillColor(colors.HexColor(fill))
                    c.setStrokeColor(colors.HexColor(border))
                    c.setLineWidth(1)
                    c.ellipse(x, y, x + w, y + h, fill=1)
                elif cmd == 'diamond':
                    _, cx, cy, size, fill, border = instr
                    c.setFillColor(colors.HexColor(fill))
                    c.setStrokeColor(colors.HexColor(border))
                    c.setLineWidth(1)
                    p = c.beginPath()
                    p.moveTo(cx, cy + size)
                    p.lineTo(cx + size, cy)
                    p.lineTo(cx, cy - size)
                    p.lineTo(cx - size, cy)
                    p.close()
                    c.drawPath(p, fill=1)
            except Exception as e:
                print(f"绘图指令执行失败 {cmd}: {e}")
                continue


# =============================================================================
# Section 4: Helper Functions
# =============================================================================

def create_cover_page(story):
    """Add a cover page to the document."""
    story.append(Spacer(1, 80))
    story.append(Paragraph(DOC_TITLE, STYLES['CoverTitle']))
    story.append(Spacer(1, 16))
    story.append(HRFlowable(
        width="60%", thickness=2,
        color=colors.HexColor('#2196F3'),
        spaceAfter=16, spaceBefore=0,
    ))
    story.append(Paragraph(DOC_SUBTITLE, STYLES['CoverSubtitle']))
    story.append(Spacer(1, 40))
    story.append(Paragraph(
        f"模块：{MODULE_NAME}", STYLES['CoverSubtitle']
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        f"生成工具：{AUTHOR}", STYLES['CoverSubtitle']
    ))
    story.append(Spacer(1, 12))

    from datetime import datetime
    today = datetime.now().strftime('%Y年%m月%d日')
    story.append(Paragraph(f"生成日期：{today}", STYLES['CoverSubtitle']))
    story.append(PageBreak())


def add_chapter(story, chapter_num, title):
    """Add a chapter heading."""
    story.append(Paragraph(
        f"第{chapter_num}章 {title}", STYLES['ChapterTitle']
    ))
    story.append(HRFlowable(
        width="100%", thickness=1.5,
        color=colors.HexColor('#2196F3'),
        spaceAfter=10,
    ))


def add_section(story, number, title):
    """Add a section heading (e.g., '2.1 架构概览')."""
    story.append(Paragraph(f"{number} {title}", STYLES['SectionTitle']))


def add_subsection(story, number, title):
    """Add a sub-section heading."""
    story.append(Paragraph(f"{number} {title}", STYLES['SubSectionTitle']))


def add_body(story, text):
    """Add a body paragraph."""
    story.append(Paragraph(text, STYLES['BodyText']))


def add_bullet(story, text):
    """Add a bullet list item."""
    story.append(Paragraph(f"• {text}", STYLES['BulletItem']))


def add_highlight(story, text):
    """Add a highlighted/callout text."""
    story.append(Paragraph(text, STYLES['Highlight']))


def add_code(story, text):
    """Add a code block."""
    # Replace special chars for XML
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    text = text.replace('\n', '<br/>')
    story.append(Paragraph(text, STYLES['CodeBlock']))


def add_caption(story, text):
    """Add a caption (typically below a diagram)."""
    story.append(Paragraph(text, STYLES['Caption']))


def add_spacer(story, height=8):
    """Add vertical space."""
    story.append(Spacer(1, height))


def add_table(story, headers, rows, col_widths=None):
    """
    Add a formatted table.

    Args:
        headers: list of header strings
        rows: list of lists of cell strings
        col_widths: optional list of column widths
    """
    # Build table data with Paragraph objects
    header_row = [Paragraph(h, STYLES['TableHeader']) for h in headers]
    data_rows = []
    for row in rows:
        data_rows.append([
            Paragraph(str(cell), STYLES['TableCell']) for cell in row
        ])
    table_data = [header_row] + data_rows

    if col_widths is None:
        # Auto-calculate even widths
        available_width = A4[0] - LEFT_MARGIN - RIGHT_MARGIN
        col_widths = [available_width / len(headers)] * len(headers)

    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5276')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), get_font_name_bold()),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        # Data rows
        ('FONTNAME', (0, 1), (-1, -1), get_font_name()),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        # Alternating row colors
        *[('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f8f9fa'))
          for i in range(1, len(table_data), 2)],
    ]))
    story.append(t)
    story.append(Spacer(1, 10))


def add_diagram(story, width, height, instructions, caption=None):
    """
    Add a diagram to the document.

    Args:
        width: diagram width in points
        height: diagram height in points
        instructions: list of drawing instructions (see DiagramFlowable)
        caption: optional caption text below the diagram
    """
    story.append(DiagramFlowable(width, height, instructions))
    if caption:
        add_caption(story, caption)


def add_page_break(story):
    """Add a page break."""
    story.append(PageBreak())


# =============================================================================
# Section 5: Document Content — FILL IN WITH ACTUAL ANALYSIS
# =============================================================================

def build_document_content(story):
    """
    Build the document content.

    >>> IMPORTANT: This function is a TEMPLATE.
    >>> Replace the placeholder content below with actual analysis results
    >>> from the source code exploration phase.
    """

    # ------ Cover Page ------
    create_cover_page(story)

    # ========================
    # Chapter 1: 模块概述
    # ========================
    add_chapter(story, 1, "模块概述")

    add_section(story, "1.1", "模块定位")
    add_body(story, "【请在此填入模块的整体定位和职责描述】")

    add_section(story, "1.2", "核心目标")
    add_bullet(story, "【目标1】")
    add_bullet(story, "【目标2】")
    add_bullet(story, "【目标3】")

    add_section(story, "1.3", "源码文件一览")
    add_table(story,
        headers=["文件名", "行数", "职责描述"],
        rows=[
            ["ExampleClass.java", "200", "【描述】"],
            ["AnotherClass.java", "150", "【描述】"],
        ],
        col_widths=[180, 60, 280],
    )

    add_page_break(story)

    # ========================
    # Chapter 2: 核心架构设计
    # ========================
    add_chapter(story, 2, "核心架构设计")

    add_section(story, "2.1", "整体架构图")
    add_body(story, "【请在此描述架构分层和组件关系】")

    # Example architecture diagram
    add_diagram(story, 500, 200, [
        # Layer boxes
        ('roundrect', 50, 150, 400, 35, 5, '#e3f2fd', '#1976D2'),
        ('text_center', 250, 163, '【API 层 — 公共接口】', 11, '#1565C0'),

        ('roundrect', 50, 100, 400, 35, 5, '#e8f5e9', '#388E3C'),
        ('text_center', 250, 113, '【核心层 — 业务逻辑】', 11, '#2E7D32'),

        ('roundrect', 50, 50, 400, 35, 5, '#fff3e0', '#F57C00'),
        ('text_center', 250, 63, '【基础设施层 — 存储/网络】', 11, '#E65100'),

        # Arrows between layers
        ('arrow', 250, 150, 250, 138, '#666666', 1),
        ('arrow', 250, 100, 250, 88, '#666666', 1),
    ], caption="图2-1 整体分层架构图（请替换为实际架构）")

    add_page_break(story)

    # ========================
    # Chapter 3: 设计模式详解
    # ========================
    add_chapter(story, 3, "核心类设计模式详解")

    add_section(story, "3.1", "【类名】 — 【模式名】模式")
    add_body(story, "【请在此填入设计模式分析】")
    add_body(story, "<b>模式说明：</b>【解释该类如何体现这一设计模式】")
    add_body(story, "<b>关键方法：</b>")
    add_bullet(story, "<b>methodName()</b> — 【方法作用】")
    add_bullet(story, "<b>anotherMethod()</b> — 【方法作用】")

    add_page_break(story)

    # ========================
    # Chapter 4: 核心流程图
    # ========================
    add_chapter(story, 4, "核心流程图")

    add_section(story, "4.1", "【流程名称】")
    add_body(story, "【请在此描述流程概述】")

    # Example flowchart
    add_diagram(story, 500, 250, [
        # Start
        ('ellipse', 200, 210, 100, 30, '#C8E6C9', '#388E3C'),
        ('text_center', 250, 220, '开始', 10, '#2E7D32'),

        ('arrow', 250, 210, 250, 195, '#666666', 1),

        # Step 1
        ('roundrect', 175, 160, 150, 30, 5, '#e3f2fd', '#1976D2'),
        ('text_center', 250, 170, '步骤1', 10, '#1565C0'),

        ('arrow', 250, 160, 250, 145, '#666666', 1),

        # Decision
        ('diamond', 250, 120, 20, '#FFF9C4', '#F9A825'),
        ('text_center', 250, 117, '判断?', 9, '#F57F17'),

        # End
        ('ellipse', 200, 50, 100, 30, '#FFCDD2', '#D32F2F'),
        ('text_center', 250, 60, '结束', 10, '#C62828'),

        ('arrow', 250, 100, 250, 83, '#666666', 1),
    ], caption="图4-1 【流程名称】流程图（请替换为实际流程）")

    add_page_break(story)

    # ========================
    # Chapter 5: 时序图
    # ========================
    add_chapter(story, 5, "核心时序图")

    add_section(story, "5.1", "【场景名称】时序图")
    add_body(story, "【请在此描述时序图场景】")

    # Example sequence diagram
    seq_w = 500
    add_diagram(story, seq_w, 200, [
        # Participants
        ('roundrect', 20, 170, 80, 25, 3, '#e3f2fd', '#1976D2'),
        ('text_center', 60, 178, '客户端', 9, '#1565C0'),
        ('roundrect', 180, 170, 80, 25, 3, '#e8f5e9', '#388E3C'),
        ('text_center', 220, 178, '服务A', 9, '#2E7D32'),
        ('roundrect', 340, 170, 80, 25, 3, '#fff3e0', '#F57C00'),
        ('text_center', 380, 178, '服务B', 9, '#E65100'),

        # Lifelines
        ('dashed', 60, 170, 60, 20, '#999999', 0.5),
        ('dashed', 220, 170, 220, 20, '#999999', 0.5),
        ('dashed', 380, 170, 380, 20, '#999999', 0.5),

        # Message 1
        ('arrow', 60, 145, 220, 145, '#1976D2', 1),
        ('text', 90, 148, '1. 请求', 8, '#333333'),

        # Message 2
        ('arrow', 220, 120, 380, 120, '#388E3C', 1),
        ('text', 250, 123, '2. 转发', 8, '#333333'),

        # Response
        ('dashed', 380, 95, 220, 95, '#F57C00', 1),
        ('text', 250, 98, '3. 响应', 8, '#333333'),

        ('dashed', 220, 70, 60, 70, '#1976D2', 1),
        ('text', 90, 73, '4. 返回', 8, '#333333'),
    ], caption="图5-1 【场景名称】时序图（请替换为实际时序）")

    add_page_break(story)

    # ========================
    # Chapter 6: 关键场景调用链
    # ========================
    add_chapter(story, 6, "关键场景调用链")

    add_section(story, "6.1", "场景一：【场景名称】")
    add_body(story, "<b>触发条件：</b>【何时触发】")
    add_body(story, "<b>调用链路：</b>")
    add_body(story, "")
    add_table(story,
        headers=["步骤", "类.方法", "说明"],
        rows=[
            ["1", "ClassA.method()", "【描述】"],
            ["2", "ClassB.method()", "【描述】"],
            ["3", "ClassC.method()", "【描述】"],
        ],
        col_widths=[40, 200, 280],
    )

    add_page_break(story)

    # ========================
    # Chapter 7: 配置与扩展
    # ========================
    add_chapter(story, 7, "配置与扩展")

    add_section(story, "7.1", "配置属性")
    add_table(story,
        headers=["配置项", "默认值", "说明"],
        rows=[
            ["property.name", "default", "【描述】"],
        ],
        col_widths=[180, 80, 260],
    )

    add_page_break(story)

    # ========================
    # Chapter 8: 设计亮点与总结
    # ========================
    add_chapter(story, 8, "设计亮点与总结")

    add_section(story, "8.1", "设计亮点")
    add_bullet(story, "<b>亮点1：</b>【描述】")
    add_bullet(story, "<b>亮点2：</b>【描述】")

    add_section(story, "8.2", "设计限制")
    add_bullet(story, "<b>限制1：</b>【描述】")

    add_section(story, "8.3", "质量评估")
    add_table(story,
        headers=["评估维度", "评分", "说明"],
        rows=[
            ["代码结构", "★★★★☆", "【描述】"],
            ["设计模式运用", "★★★★☆", "【描述】"],
            ["可扩展性", "★★★★☆", "【描述】"],
            ["文档完整度", "★★★☆☆", "【描述】"],
        ],
        col_widths=[130, 100, 290],
    )


# =============================================================================
# Section 6: Main Entry Point
# =============================================================================

def main():
    """Generate the PDF document."""
    print(f"开始生成文档: {OUTPUT_PDF}")

    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
        title=DOC_TITLE,
        author=AUTHOR,
    )

    story = []
    build_document_content(story)

    doc.build(story)

    file_size = os.path.getsize(OUTPUT_PDF)
    print(f"文档生成完成: {OUTPUT_PDF} ({file_size / 1024:.1f} KB)")


if __name__ == '__main__':
    main()
