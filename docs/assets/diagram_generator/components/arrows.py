"""
arrows.py
Drawing primitives for SVG arrows and connections.
Handles marker definitions, routing logic, and line styling.
"""

import math
import svgwrite
from typing import Tuple
import components.styles as styles

def _get_or_create_marker(dwg: svgwrite.Drawing, color: str) -> str:
    """
    Dynamically creates an SVG marker in the <defs> block for a specific color.
    Because SVG markers define their own fill color, this ensures that red arrows
    get red heads, blue arrows get blue heads, etc.
    """
    marker_id = f"arrowhead_{color.replace('#', '')}"
    
    # Check if marker already exists to avoid duplicating in the <defs>
    for element in dwg.defs.elements:
        if getattr(element, 'get_id', lambda: None)() == marker_id:
            return marker_id
            
    # Solid triangle matching the uploaded figure
    head_len = styles.ARROWS["head_length"]
    head_wid = styles.ARROWS["head_width"]
    
    # orient="auto" makes the arrowhead follow the path's terminal angle
    marker = dwg.marker(id=marker_id, insert=(head_len, head_wid/2),
                        size=(head_len, head_wid), orient="auto")
    
    # The triangular polygon
    marker.add(dwg.polygon([(0, 0), (head_len, head_wid/2), (0, head_wid)], fill=color))
    dwg.defs.add(marker)
    
    return marker_id


def _get_base_path(dwg: svgwrite.Drawing, color: str, width: float, 
                   dashed: bool = False, dasharray: str = "8,6") -> svgwrite.path.Path:
    """Initializes a Path object with standard styling and attaches the correct arrowhead marker."""
    marker_id = _get_or_create_marker(dwg, color)
    path = dwg.path(fill="none", stroke=color, stroke_width=width, marker_end=f"url(#{marker_id})")
    
    if dashed:
        path['stroke-dasharray'] = dasharray
        
    return path


def draw_horizontal_arrow(dwg: svgwrite.Drawing, start: Tuple[float, float], end: Tuple[float, float], 
                          color: str = styles.COLORS["arrow"], width: float = styles.ARROWS["stroke_width"]) -> svgwrite.path.Path:
    """Draws a straight point-to-point line (typically left-to-right horizontal)."""
    path = _get_base_path(dwg, color, width)
    path.push(f"M {start[0]},{start[1]}")
    path.push(f"L {end[0]},{end[1]}")
    return path


def draw_vertical_arrow(dwg: svgwrite.Drawing, start: Tuple[float, float], end: Tuple[float, float], 
                        color: str = styles.COLORS["arrow"], width: float = styles.ARROWS["stroke_width"]) -> svgwrite.path.Path:
    """Draws a straight point-to-point line (typically top-to-bottom vertical)."""
    path = _get_base_path(dwg, color, width)
    path.push(f"M {start[0]},{start[1]}")
    path.push(f"L {end[0]},{end[1]}")
    return path


def draw_dashed_arrow(dwg: svgwrite.Drawing, start: Tuple[float, float], end: Tuple[float, float], 
                      color: str = styles.COLORS["arrow"], width: float = styles.ARROWS["stroke_width"],
                      dasharray: str = "8,6") -> svgwrite.path.Path:
    """Draws a straight point-to-point dashed arrow."""
    path = _get_base_path(dwg, color, width, dashed=True, dasharray=dasharray)
    path.push(f"M {start[0]},{start[1]}")
    path.push(f"L {end[0]},{end[1]}")
    return path


def draw_feedback_arrow(dwg: svgwrite.Drawing, start: Tuple[float, float], end: Tuple[float, float], 
                        offset_y: float = 60, color: str = styles.COLORS["arrow"], 
                        width: float = styles.ARROWS["stroke_width"], dashed: bool = True) -> svgwrite.path.Path:
    """
    Draws an orthogonal feedback loop arrow (U-shape).
    Used for the 'Iterative Refinement' arrow spanning the bottom of the diagram.
    """
    path = _get_base_path(dwg, color, width, dashed=dashed, dasharray="10,8")
    path.push(f"M {start[0]},{start[1]}")
    # Drop down perpendicularly
    path.push(f"L {start[0]},{start[1] + offset_y}")
    # Traverse horizontally across the diagram
    path.push(f"L {end[0]},{start[1] + offset_y}")
    # Go back up perpendicularly to the target
    path.push(f"L {end[0]},{end[1]}")
    return path


def draw_curved_arrow(dwg: svgwrite.Drawing, start: Tuple[float, float], end: Tuple[float, float], 
                      color: str = styles.COLORS["arrow"], width: float = styles.ARROWS["stroke_width"],
                      dashed: bool = False, sweep_flag: int = 1) -> svgwrite.path.Path:
    """
    Draws an elliptical arc arrow connecting two points.
    Useful for skipping over intermediate boxes or indicating state transitions.
    """
    path = _get_base_path(dwg, color, width, dashed=dashed)
    path.push(f"M {start[0]},{start[1]}")
    
    # Calculate radius based on physical distance for a clean, natural curve
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    dist = math.hypot(dx, dy)
    radius = dist * 0.7  # The larger the multiplier, the flatter the arc
    
    # SVG Arc Command: A rx ry x-axis-rotation large-arc-flag sweep-flag x y
    path.push(f"A {radius},{radius} 0 0,{sweep_flag} {end[0]},{end[1]}")
    return path
