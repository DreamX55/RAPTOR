"""
boxes.py
Drawing primitives for rendering SVG structural components.
Converts layout objects into stylized svgwrite elements.
"""

import svgwrite
from typing import List

import components.styles as styles
from components.layout import LayoutNode, TextBlock

def wrap_text(text: str, max_chars: int = 22) -> List[str]:
    """Wraps text into multiple lines based on a character limit."""
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= max_chars:
            current_line += (word + " ") if current_line else word + " "
        else:
            if current_line:
                lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return lines

def _draw_text_multiline(dwg: svgwrite.Drawing, parent_group: svgwrite.container.Group, 
                         node: TextBlock, max_chars: int = 22, offset_y: float = 0) -> None:
    """Helper to render text logic with word wrapping into the SVG container."""
    lines = wrap_text(node.text, max_chars)
    
    font_style = styles.get_font_style(node.font_style)
    anchor = node.get_text_anchor()
    
    # Calculate starting Y to vertically center the multi-line block
    line_height = font_style["font_size"] * 1.3
    total_height = len(lines) * line_height
    # The font size / 3 offset is a typical baseline adjustment in SVG text
    start_y = node.center_y - (total_height / 2) + (font_style["font_size"] / 1.5) + offset_y
    
    for i, line in enumerate(lines):
        txt_elem = dwg.text(line, insert=(node.get_draw_x(), start_y + (i * line_height)), text_anchor=anchor)
        for key, val in font_style.items():
            txt_elem[key.replace('_', '-')] = val
        parent_group.add(txt_elem)

def draw_round_box(dwg: svgwrite.Drawing, node: LayoutNode, text: str = "", 
                   bg_color: str = styles.COLORS["background"], 
                   border_color: str = styles.COLORS["border"], 
                   font_style: str = "body",
                   shadow: bool = True,
                   max_chars: int = 22) -> svgwrite.container.Group:
    """Draws a generic rounded rectangle with centered text."""
    g = dwg.g()
    
    rect = dwg.rect(insert=(node.x, node.y), size=(node.width, node.height), 
                    rx=styles.SHAPES["corner_radius_md"], ry=styles.SHAPES["corner_radius_md"],
                    fill=bg_color, stroke=border_color, stroke_width=styles.SHAPES["line_width_md"])
    if shadow:
        styles.apply_shadow(rect)
    g.add(rect)
    
    if text:
        tb = TextBlock(text, node.x, node.y, node.width, node.height, align="center", font_style=font_style)
        _draw_text_multiline(dwg, g, tb, max_chars=max_chars)
        
    return g

def draw_header(dwg: svgwrite.Drawing, node: LayoutNode, text: str) -> svgwrite.container.Group:
    """Draws the top-level gradient page header."""
    g = dwg.g()
    
    rect = dwg.rect(insert=(node.x, node.y), size=(node.width, node.height), 
                    fill=f"url(#{styles.GRADIENTS['bg_gradient']['id']})", 
                    stroke="none")
    g.add(rect)
    
    tb = TextBlock(text, node.x, node.y, node.width, node.height, align="center", font_style="title")
    _draw_text_multiline(dwg, g, tb, max_chars=150)
    
    line = dwg.line(start=(node.x, node.y + node.height), end=(node.x + node.width, node.y + node.height), 
                    stroke=styles.COLORS["border"], stroke_width=styles.SHAPES["line_width_thick"])
    g.add(line)
    
    return g

def draw_title(dwg: svgwrite.Drawing, node: LayoutNode, text: str) -> svgwrite.container.Group:
    """Draws a standalone title text block."""
    g = dwg.g()
    tb = TextBlock(text, node.x, node.y, node.width, node.height, align="center", font_style="subtitle")
    _draw_text_multiline(dwg, g, tb, max_chars=40)
    return g

def draw_subtitle(dwg: svgwrite.Drawing, node: LayoutNode, text: str) -> svgwrite.container.Group:
    """Draws a standalone subtitle text block."""
    g = dwg.g()
    tb = TextBlock(text, node.x, node.y, node.width, node.height, align="center", font_style="small")
    _draw_text_multiline(dwg, g, tb, max_chars=40)
    return g

def draw_group_box(dwg: svgwrite.Drawing, node: LayoutNode, title: str = "", 
                   bg_color: str = styles.COLORS["col1_bg"]) -> svgwrite.container.Group:
    """Draws a large column or section background panel."""
    g = dwg.g()
    
    rect = dwg.rect(insert=(node.x, node.y), size=(node.width, node.height), 
                    rx=styles.SHAPES["corner_radius_lg"], ry=styles.SHAPES["corner_radius_lg"],
                    fill=bg_color, stroke="none")
    g.add(rect)
    
    if title:
        # Title block is placed in the top area of the group
        title_block = TextBlock(title, node.x, node.y + 10, node.width, 50, align="center", font_style="subtitle")
        _draw_text_multiline(dwg, g, title_block, max_chars=35)
        
    return g

def draw_inner_box(dwg: svgwrite.Drawing, node: LayoutNode, text: str, 
                   bg_color: str = styles.COLORS["background"], 
                   border_color: str = styles.COLORS["border"]) -> svgwrite.container.Group:
    """Draws a standard component box inside a group (wrapper for draw_round_box)."""
    return draw_round_box(dwg, node, text, bg_color=bg_color, border_color=border_color, 
                          font_style="body", shadow=True, max_chars=22)

def draw_metric_box(dwg: svgwrite.Drawing, node: LayoutNode, title: str, metrics: List[str], 
                    bg_color: str = styles.COLORS["background"]) -> svgwrite.container.Group:
    """Draws an evaluation/metrics box with a header and bullet points."""
    g = dwg.g()
    
    rect = dwg.rect(insert=(node.x, node.y), size=(node.width, node.height), 
                    rx=styles.SHAPES["corner_radius_sm"], ry=styles.SHAPES["corner_radius_sm"],
                    fill=bg_color, stroke=styles.COLORS["border"], stroke_width=styles.SHAPES["line_width_thin"])
    styles.apply_shadow(rect)
    g.add(rect)
    
    # Header block
    title_h = 30
    tb_title = TextBlock(title, node.x, node.y + 5, node.width, title_h, align="center", font_style="subtitle")
    _draw_text_multiline(dwg, g, tb_title, max_chars=25)
    
    # Divider line
    line_y = node.y + title_h + 15
    g.add(dwg.line(start=(node.x + 15, line_y), end=(node.x + node.width - 15, line_y), 
                   stroke=styles.COLORS["border"], stroke_width=1))
    
    # Render bullet list
    bullet_y = line_y + 25
    f_style = styles.get_font_style("small")
    for metric in metrics:
        txt = dwg.text(f"• {metric}", insert=(node.x + 20, bullet_y), text_anchor="start")
        for key, val in f_style.items():
            txt[key.replace('_', '-')] = val
        g.add(txt)
        bullet_y += f_style["font_size"] * 1.5
        
    return g

def draw_footer(dwg: svgwrite.Drawing, node: LayoutNode, text: str) -> svgwrite.container.Group:
    """Draws bottom-aligned annotation/footer text."""
    g = dwg.g()
    tb = TextBlock(text, node.x, node.y, node.width, node.height, align="center", font_style="small")
    _draw_text_multiline(dwg, g, tb, max_chars=200)
    return g
