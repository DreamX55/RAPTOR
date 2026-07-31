"""
icons.py
Programmatic scalable vector icons drawn using pure svgwrite primitives.
All icons are designed on a 100x100 internal canvas and scaled automatically.
"""

import svgwrite
import math

def _icon_container(dwg: svgwrite.Drawing, x: float, y: float, size: float) -> svgwrite.container.Group:
    """
    Creates a translation and scaling container. 
    By setting up a local 100x100 coordinate space, we can draw the icons easily 
    and let SVG transforms handle arbitrary positioning and sizing.
    """
    scale = size / 100.0
    # Offset by -size/2 so that (x,y) represents the center of the icon
    offset_x = x - (size / 2)
    offset_y = y - (size / 2)
    return dwg.g(transform=f"translate({offset_x}, {offset_y}) scale({scale})")

def draw_document_icon(dwg: svgwrite.Drawing, x: float, y: float, size: float = 50, color: str = "#333") -> svgwrite.container.Group:
    """Standard page with a folded top-right corner."""
    g = _icon_container(dwg, x, y, size)
    
    # Document outline
    outline = dwg.path(fill="#fff", stroke=color, stroke_width=6, stroke_linejoin="round")
    outline.push("M 20,10 L 60,10 L 80,30 L 80,90 L 20,90 Z")
    g.add(outline)
    
    # Folded flap
    flap = dwg.path(fill="none", stroke=color, stroke_width=6, stroke_linejoin="round")
    flap.push("M 60,10 L 60,30 L 80,30")
    g.add(flap)
    
    # Text lines
    g.add(dwg.line((35, 45), (65, 45), stroke=color, stroke_width=4, stroke_linecap="round"))
    g.add(dwg.line((35, 60), (65, 60), stroke=color, stroke_width=4, stroke_linecap="round"))
    g.add(dwg.line((35, 75), (50, 75), stroke=color, stroke_width=4, stroke_linecap="round"))
    return g

def draw_report_icon(dwg: svgwrite.Drawing, x: float, y: float, size: float = 50, color: str = "#333") -> svgwrite.container.Group:
    """Document icon with an embedded bar chart representing Analysis & Reporting."""
    g = draw_document_icon(dwg, x, y, size, color)
    # Overlay a small bar chart
    g.add(dwg.rect(insert=(35, 40), size=(8, 25), fill="#2196f3"))
    g.add(dwg.rect(insert=(47, 50), size=(8, 15), fill="#4caf50"))
    g.add(dwg.rect(insert=(59, 30), size=(8, 35), fill="#ff9800"))
    return g

def draw_sanitized_document(dwg: svgwrite.Drawing, x: float, y: float, size: float = 50, color: str = "#333") -> svgwrite.container.Group:
    """Document icon with a green checkmark indicating sanitized state."""
    g = draw_document_icon(dwg, x, y, size, color)
    # Add a checkmark badge in bottom right corner
    g.add(dwg.circle(center=(75, 80), r=12, fill="#4caf50", stroke="#ffffff", stroke_width=2))
    check = dwg.path(fill="none", stroke="#ffffff", stroke_width=3, stroke_linecap="round", stroke_linejoin="round")
    check.push("M 69,80 L 73,84 L 81,75")
    g.add(check)
    return g

def draw_wikipedia_document(dwg: svgwrite.Drawing, x: float, y: float, size: float = 50, color: str = "#333") -> svgwrite.container.Group:
    """Document icon with a large 'W' in the center."""
    g = draw_document_icon(dwg, x, y, size, color)
    g_wiki = _icon_container(dwg, x, y, size)
    outline = dwg.path(fill="#fff", stroke=color, stroke_width=6, stroke_linejoin="round")
    outline.push("M 20,10 L 60,10 L 80,30 L 80,90 L 20,90 Z")
    g_wiki.add(outline)
    flap = dwg.path(fill="none", stroke=color, stroke_width=6, stroke_linejoin="round")
    flap.push("M 60,10 L 60,30 L 80,30")
    g_wiki.add(flap)
    
    w_path = dwg.path(fill="none", stroke=color, stroke_width=6, stroke_linejoin="round", stroke_linecap="round")
    w_path.push("M 30,45 L 40,75 L 50,55 L 60,75 L 70,45")
    g_wiki.add(w_path)
    return g_wiki

def draw_model_logos(dwg: svgwrite.Drawing, x: float, y: float, size: float = 50, color: str = "#333") -> svgwrite.container.Group:
    """Stylized geometric shapes approximating the LLM logos in the diagram."""
    g = _icon_container(dwg, x, y, size)
    
    # Orange M (Mistral-like)
    m_path = dwg.path(fill="none", stroke="#ff9800", stroke_width=12, stroke_linejoin="miter")
    m_path.push("M 15,75 L 15,25 L 35,50 L 55,25 L 55,75")
    g.add(m_path)
    
    # Purple Hex/Star (Qwen/Llama-like)
    # Just draw a cool geometric polygon
    g.add(dwg.polygon([(75, 20), (90, 35), (90, 60), (75, 75), (60, 60), (60, 35)], 
                      fill="none", stroke="#673ab7", stroke_width=8))
    g.add(dwg.circle(center=(75, 47.5), r=6, fill="#673ab7"))
    
    return g

def draw_document_stack(dwg: svgwrite.Drawing, x: float, y: float, size: float = 50, color: str = "#333") -> svgwrite.container.Group:
    """Overlapping document icons."""
    g = _icon_container(dwg, x, y, size)
    
    # Back document
    back = dwg.path(fill="#fff", stroke=color, stroke_width=4, stroke_linejoin="round")
    back.push("M 35,5 L 65,5 L 85,25 L 85,75 L 35,75 Z")
    g.add(back)
    
    # Middle document
    mid = dwg.path(fill="#fff", stroke=color, stroke_width=4, stroke_linejoin="round")
    mid.push("M 25,15 L 55,15 L 75,35 L 75,85 L 25,85 Z")
    g.add(mid)
    
    # Front document
    front = dwg.path(fill="#fff", stroke=color, stroke_width=4, stroke_linejoin="round")
    front.push("M 15,25 L 45,25 L 65,45 L 65,95 L 15,95 Z")
    front_flap = dwg.path(fill="none", stroke=color, stroke_width=4, stroke_linejoin="round")
    front_flap.push("M 45,25 L 45,45 L 65,45")
    g.add(front)
    g.add(front_flap)
    
    return g

def draw_database_cylinder(dwg: svgwrite.Drawing, x: float, y: float, size: float = 50, color: str = "#333") -> svgwrite.container.Group:
    """Standard isometric cylinder for databases."""
    g = _icon_container(dwg, x, y, size)
    
    # Body
    g.add(dwg.path(d="M 20,30 L 20,70 A 30,15 0 0,0 80,70 L 80,30 Z", fill="#fff", stroke=color, stroke_width=6))
    # Internal ring to simulate stack
    g.add(dwg.path(d="M 20,50 A 30,15 0 0,0 80,50", fill="none", stroke=color, stroke_width=6))
    # Top ellipse
    g.add(dwg.ellipse(center=(50, 30), r=(30, 15), fill="#fff", stroke=color, stroke_width=6))
    return g

def draw_vector_network(dwg: svgwrite.Drawing, x: float, y: float, size: float = 50, color: str = "#333") -> svgwrite.container.Group:
    """Network of nodes representing embeddings."""
    g = _icon_container(dwg, x, y, size)
    
    pts = [(20,50), (50,20), (80,50), (50,80), (50,50)]
    
    # Edges
    edges = [(0,1), (1,2), (2,3), (3,0), (0,4), (1,4), (2,4), (3,4)]
    for (i, j) in edges:
        g.add(dwg.line(pts[i], pts[j], stroke=color, stroke_width=4))
        
    # Nodes
    for pt in pts:
        g.add(dwg.circle(center=pt, r=8, fill="#fff", stroke=color, stroke_width=4))
        
    return g

def draw_shield(dwg: svgwrite.Drawing, x: float, y: float, size: float = 50, color: str = "#333") -> svgwrite.container.Group:
    """Security shield."""
    g = _icon_container(dwg, x, y, size)
    
    path = dwg.path(fill="#fff", stroke=color, stroke_width=6, stroke_linejoin="round")
    path.push("M 50,10 L 15,25 L 15,50 C 15,75 50,95 50,95 C 50,95 85,75 85,50 L 85,25 Z")
    g.add(path)
    
    # Inner checkmark or star
    check = dwg.path(fill="none", stroke=color, stroke_width=6, stroke_linecap="round", stroke_linejoin="round")
    check.push("M 35,50 L 45,60 L 65,35")
    g.add(check)
    return g

def draw_magnifying_glass(dwg: svgwrite.Drawing, x: float, y: float, size: float = 50, color: str = "#333") -> svgwrite.container.Group:
    """Search/Retrieval icon."""
    g = _icon_container(dwg, x, y, size)
    
    # Lens
    g.add(dwg.circle(center=(40, 40), r=25, fill="#fff", stroke=color, stroke_width=8))
    # Handle
    g.add(dwg.line((58, 58), (85, 85), stroke=color, stroke_width=12, stroke_linecap="round"))
    return g

def draw_bar_chart(dwg: svgwrite.Drawing, x: float, y: float, size: float = 50, color: str = "#333") -> svgwrite.container.Group:
    """Analytics/Metrics chart."""
    g = _icon_container(dwg, x, y, size)
    
    # Axes
    g.add(dwg.polyline([(15, 15), (15, 85), (85, 85)], fill="none", stroke=color, stroke_width=6, stroke_linejoin="round"))
    # Bars
    g.add(dwg.rect(insert=(25, 55), size=(12, 30), fill=color, rx=2))
    g.add(dwg.rect(insert=(45, 35), size=(12, 50), fill=color, rx=2))
    g.add(dwg.rect(insert=(65, 15), size=(12, 70), fill=color, rx=2))
    return g

def draw_chat_bubble(dwg: svgwrite.Drawing, x: float, y: float, size: float = 50, color: str = "#333") -> svgwrite.container.Group:
    """LLM generation icon."""
    g = _icon_container(dwg, x, y, size)
    
    path = dwg.path(fill="#fff", stroke=color, stroke_width=6, stroke_linejoin="round")
    path.push("M 15,25 C 15,15 25,15 25,15 L 75,15 C 85,15 85,25 85,25 L 85,65 C 85,75 75,75 75,75 L 45,75 L 25,90 L 25,75 C 15,75 15,65 15,65 Z")
    g.add(path)
    
    g.add(dwg.circle(center=(35, 45), r=4, fill=color))
    g.add(dwg.circle(center=(50, 45), r=4, fill=color))
    g.add(dwg.circle(center=(65, 45), r=4, fill=color))
    return g

def draw_clipboard(dwg: svgwrite.Drawing, x: float, y: float, size: float = 50, color: str = "#333") -> svgwrite.container.Group:
    """Evaluation / Prompt Template icon."""
    g = _icon_container(dwg, x, y, size)
    
    # Board
    g.add(dwg.rect(insert=(20, 20), size=(60, 75), rx=5, fill="#fff", stroke=color, stroke_width=6))
    # Clip
    g.add(dwg.rect(insert=(35, 5), size=(30, 25), rx=3, fill="#fff", stroke=color, stroke_width=6))
    g.add(dwg.line((45, 15), (55, 15), stroke=color, stroke_width=4))
    # Lines
    g.add(dwg.line((35, 50), (65, 50), stroke=color, stroke_width=4, stroke_linecap="round"))
    g.add(dwg.line((35, 65), (65, 65), stroke=color, stroke_width=4, stroke_linecap="round"))
    g.add(dwg.line((35, 80), (55, 80), stroke=color, stroke_width=4, stroke_linecap="round"))
    return g

def draw_filter_funnel(dwg: svgwrite.Drawing, x: float, y: float, size: float = 50, color: str = "#333") -> svgwrite.container.Group:
    """Filtering icon."""
    g = _icon_container(dwg, x, y, size)
    
    path = dwg.path(fill="#fff", stroke=color, stroke_width=6, stroke_linejoin="round")
    path.push("M 10,20 L 90,20 L 60,55 L 60,85 L 40,95 L 40,55 Z")
    g.add(path)
    return g

def draw_gauge(dwg: svgwrite.Drawing, x: float, y: float, size: float = 50, color: str = "#333") -> svgwrite.container.Group:
    """Trust Scoring icon."""
    g = _icon_container(dwg, x, y, size)
    
    # Semi-circle dial
    g.add(dwg.path(d="M 15,70 A 35,35 0 0,1 85,70", fill="none", stroke=color, stroke_width=8, stroke_linecap="round"))
    # Needle
    g.add(dwg.circle(center=(50, 70), r=8, fill=color))
    g.add(dwg.line((50, 70), (25, 45), stroke=color, stroke_width=6, stroke_linecap="round"))
    return g

def draw_people_icon(dwg: svgwrite.Drawing, x: float, y: float, size: float = 50, color: str = "#333") -> svgwrite.container.Group:
    """User / Semantic Consensus icon."""
    g = _icon_container(dwg, x, y, size)
    
    # Central person
    g.add(dwg.circle(center=(50, 35), r=15, fill="#fff", stroke=color, stroke_width=6))
    g.add(dwg.path(d="M 25,90 C 25,60 75,60 75,90", fill="#fff", stroke=color, stroke_width=6, stroke_linecap="round"))
    return g

def draw_warning_bug(dwg: svgwrite.Drawing, x: float, y: float, size: float = 50, color: str = "#333") -> svgwrite.container.Group:
    """Poisoning / Injection icon."""
    g = _icon_container(dwg, x, y, size)
    
    # Antennae
    g.add(dwg.path(d="M 35,25 C 25,10 15,20 15,20", fill="none", stroke=color, stroke_width=4, stroke_linecap="round"))
    g.add(dwg.path(d="M 65,25 C 75,10 85,20 85,20", fill="none", stroke=color, stroke_width=4, stroke_linecap="round"))
    
    # Body
    g.add(dwg.circle(center=(50, 55), r=25, fill="#fff", stroke=color, stroke_width=6))
    
    # Legs (Left)
    g.add(dwg.line((25, 45), (10, 40), stroke=color, stroke_width=4, stroke_linecap="round"))
    g.add(dwg.line((25, 55), (10, 55), stroke=color, stroke_width=4, stroke_linecap="round"))
    g.add(dwg.line((25, 65), (10, 70), stroke=color, stroke_width=4, stroke_linecap="round"))
    # Legs (Right)
    g.add(dwg.line((75, 45), (90, 40), stroke=color, stroke_width=4, stroke_linecap="round"))
    g.add(dwg.line((75, 55), (90, 55), stroke=color, stroke_width=4, stroke_linecap="round"))
    g.add(dwg.line((75, 65), (90, 70), stroke=color, stroke_width=4, stroke_linecap="round"))
    
    # Inner stripes
    g.add(dwg.line((35, 45), (65, 45), stroke=color, stroke_width=4))
    g.add(dwg.line((30, 55), (70, 55), stroke=color, stroke_width=4))
    g.add(dwg.line((35, 65), (65, 65), stroke=color, stroke_width=4))
    return g

def draw_terminal_icon(dwg: svgwrite.Drawing, x: float, y: float, size: float = 50, color: str = "#333") -> svgwrite.container.Group:
    """Goal hijacking / Instruction injection icon."""
    g = _icon_container(dwg, x, y, size)
    
    g.add(dwg.rect(insert=(10, 20), size=(80, 60), rx=5, fill=color))
    # Prompt >
    g.add(dwg.polyline([(20, 35), (35, 50), (20, 65)], fill="none", stroke="#fff", stroke_width=6, stroke_linejoin="round", stroke_linecap="round"))
    # Cursor _
    g.add(dwg.line((45, 65), (65, 65), stroke="#fff", stroke_width=6, stroke_linecap="round"))
    return g

def draw_target_icon(dwg: svgwrite.Drawing, x: float, y: float, size: float = 50, color: str = "#333") -> svgwrite.container.Group:
    """Goal hijacking icon."""
    g = _icon_container(dwg, x, y, size)
    
    g.add(dwg.circle(center=(50, 50), r=35, fill="none", stroke=color, stroke_width=8))
    g.add(dwg.circle(center=(50, 50), r=20, fill="none", stroke=color, stroke_width=8))
    g.add(dwg.circle(center=(50, 50), r=6, fill=color))
    
    # Crosshairs
    g.add(dwg.line((50, 0), (50, 25), stroke=color, stroke_width=4))
    g.add(dwg.line((50, 75), (50, 100), stroke=color, stroke_width=4))
    g.add(dwg.line((0, 50), (25, 50), stroke=color, stroke_width=4))
    g.add(dwg.line((75, 50), (100, 50), stroke=color, stroke_width=4))
    return g

def draw_lock_icon(dwg: svgwrite.Drawing, x: float, y: float, size: float = 50, color: str = "#333") -> svgwrite.container.Group:
    """Information extraction icon."""
    g = _icon_container(dwg, x, y, size)
    
    # Body
    g.add(dwg.rect(insert=(20, 45), size=(60, 45), rx=5, fill="#fff", stroke=color, stroke_width=6, stroke_linejoin="round"))
    # Keyhole
    g.add(dwg.circle(center=(50, 60), r=6, fill=color))
    g.add(dwg.path(d="M 47,63 L 45,75 L 55,75 L 53,63 Z", fill=color))
    # Shackle
    g.add(dwg.path(d="M 30,45 L 30,35 A 20,20 0 0,1 70,35 L 70,45", fill="none", stroke=color, stroke_width=8, stroke_linecap="round"))
    return g

def draw_chunks_icon(dwg: svgwrite.Drawing, x: float, y: float, size: float = 50, color: str = "#333") -> svgwrite.container.Group:
    """Small colored rectangles representing text chunks."""
    g = _icon_container(dwg, x, y, size)
    
    colors = ["#90caf9", "#f48fb1", "#ffe082", "#a5d6a7", "#bcaaa4"]
    g.add(dwg.rect(insert=(15, 20), size=(20, 15), fill=colors[0], stroke=color, stroke_width=2))
    g.add(dwg.rect(insert=(40, 20), size=(20, 15), fill=colors[1], stroke=color, stroke_width=2))
    g.add(dwg.rect(insert=(15, 60), size=(20, 15), fill=colors[2], stroke=color, stroke_width=2))
    g.add(dwg.rect(insert=(40, 60), size=(20, 15), fill=colors[3], stroke=color, stroke_width=2))
    
    # Ellipsis dots
    g.add(dwg.circle(center=(75, 40), r=2, fill=color))
    g.add(dwg.circle(center=(85, 40), r=2, fill=color))
    g.add(dwg.circle(center=(95, 40), r=2, fill=color))
    return g
