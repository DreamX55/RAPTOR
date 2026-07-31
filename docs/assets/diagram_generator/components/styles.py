"""
styles.py
Defines the central design system and visual properties for the RAPTOR architecture SVG.
"""

from typing import Dict, Any

# =============================================================================
# PAGE DIMENSIONS & SPACING
# =============================================================================
PAGE_WIDTH = 1600
PAGE_HEIGHT = 900

# Spacing
PADDING = 20
MARGIN = 30
COLUMN_SPACING = 250
ROW_SPACING = 150

# =============================================================================
# TYPOGRAPHY
# =============================================================================
FONT_FAMILY = "Arial, Helvetica, sans-serif"

FONTS = {
    "title": {"family": FONT_FAMILY, "size": 24, "weight": "bold", "color": "#000000"},
    "subtitle": {"family": FONT_FAMILY, "size": 18, "weight": "bold", "color": "#333333"},
    "body": {"family": FONT_FAMILY, "size": 14, "weight": "normal", "color": "#444444"},
    "small": {"family": FONT_FAMILY, "size": 12, "weight": "normal", "color": "#666666"},
}

# =============================================================================
# COLOR PALETTE
# =============================================================================
COLORS = {
    "text": "#000000",
    "text_light": "#555555",
    "background": "#ffffff",
    
    # Structural Colors
    "border": "#b0bec5",
    "arrow": "#37474f",
    
    # Column Header Backgrounds (matched to the original diagram)
    "col1_bg": "#d9e8f5",  # Data & Knowledge (Blue)
    "col2_bg": "#dcedc8",  # Indexing (Green)
    "col3_bg": "#fff9c4",  # Retrieval (Yellow)
    "col4_bg": "#e1bee7",  # RAGShield (Purple)
    "col5_bg": "#ffcc80",  # Generation (Orange)
    "col6_bg": "#ffcdd2",  # Evaluation (Red)
    
    # Specific Component Colors
    "benign": "#e3f2fd",
    "benign_border": "#2196f3",
    "adversarial": "#ffebee",
    "adversarial_border": "#f44336",
    
    # RAGShield inner boxes
    "ragshield_inner": "#f3e5f5",
    "ragshield_border": "#9c27b0",
    
    # Sanitized state
    "sanitized": "#e8f5e9",
    "sanitized_border": "#4caf50",
}

# =============================================================================
# SHAPES & LINES
# =============================================================================
SHAPES = {
    "corner_radius_lg": 12,
    "corner_radius_md": 8,
    "corner_radius_sm": 4,
    "line_width_thick": 3,
    "line_width_md": 2,
    "line_width_thin": 1,
}

ARROWS = {
    "head_length": 10,
    "head_width": 8,
    "stroke_width": 2,
    "color": COLORS["arrow"]
}

# =============================================================================
# GRADIENTS & SHADOWS (SVG Definitions)
# =============================================================================
# These dicts act as configurations for the SVG <defs> block

GRADIENTS = {
    "bg_gradient": {
        "id": "bgGrad",
        "start_color": "#ffffff",
        "end_color": "#f8f9fa",
        "direction": ("0%", "0%", "0%", "100%") # x1, y1, x2, y2
    }
}

SHADOWS = {
    "box_shadow": {
        "id": "dropShadow",
        "dx": 2,
        "dy": 4,
        "stdDeviation": 4,
        "opacity": 0.15
    }
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_font_style(font_type: str) -> Dict[str, Any]:
    """Retrieves standard kwargs for svgwrite text styling based on type."""
    if font_type not in FONTS:
        font_type = "body"
        
    f = FONTS[font_type]
    return {
        "font_family": f["family"],
        "font_size": f["size"],
        "font_weight": f["weight"],
        "fill": f["color"]
    }

def apply_shadow(element: Any, shadow_id: str = "dropShadow") -> None:
    """Applies a shadow filter definition to an svgwrite element."""
    element['filter'] = f"url(#{shadow_id})"

def setup_svg_defs(dwg: Any) -> None:
    """
    Injects global gradients and filters into the SVG Drawing <defs>.
    Requires the dwg (svgwrite.Drawing) instance.
    """
    # Drop shadows skipped for pure svgwrite compatibility
    pass

    # 2. Setup Gradients
    for grad_key, grad_cfg in GRADIENTS.items():
        grad = dwg.linearGradient(id=grad_cfg["id"], 
                                  start=(grad_cfg["direction"][0], grad_cfg["direction"][1]), 
                                  end=(grad_cfg["direction"][2], grad_cfg["direction"][3]))
        grad.add_stop_color(offset='0%', color=grad_cfg["start_color"])
        grad.add_stop_color(offset='100%', color=grad_cfg["end_color"])
        dwg.defs.add(grad)
        
    # 3. Setup Default Arrow Marker
    marker = dwg.marker(id="arrowhead", insert=(ARROWS["head_length"], ARROWS["head_width"]/2),
                        size=(ARROWS["head_length"], ARROWS["head_width"]), orient="auto")
    marker.add(dwg.polygon([(0, 0), (ARROWS["head_length"], ARROWS["head_width"]/2), (0, ARROWS["head_width"])], 
                           fill=ARROWS["color"]))
    dwg.defs.add(marker)
