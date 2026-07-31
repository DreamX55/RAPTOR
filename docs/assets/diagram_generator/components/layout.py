"""
layout.py
Layout engine for automatically computing coordinates and spatial relationships.
Provides reusable object-oriented layout classes.
"""

import components.styles as styles

# Override page dimensions based on the new requirement
styles.PAGE_WIDTH = 1700
styles.PAGE_HEIGHT = 900

class LayoutNode:
    """Base class representing a spatial bounding box."""
    
    def __init__(self, x: float = 0, y: float = 0, width: float = 0, height: float = 0, 
                 padding: float = 0, margin: float = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.padding = padding
        self.margin = margin
        self.children = []

    def add_child(self, child: 'LayoutNode') -> None:
        self.children.append(child)

    @property
    def inner_x(self) -> float:
        return self.x + self.padding

    @property
    def inner_y(self) -> float:
        return self.y + self.padding

    @property
    def inner_width(self) -> float:
        return self.width - (2 * self.padding)

    @property
    def inner_height(self) -> float:
        return self.height - (2 * self.padding)

    @property
    def center_x(self) -> float:
        return self.x + (self.width / 2)

    @property
    def center_y(self) -> float:
        return self.y + (self.height / 2)


class TextBlock(LayoutNode):
    """Handles automatic text positioning, alignment, and styling parameters."""
    
    def __init__(self, text: str, x: float = 0, y: float = 0, width: float = 0, height: float = 0,
                 align: str = 'center', font_style: str = 'body'):
        super().__init__(x, y, width, height)
        self.text = text
        self.align = align
        self.font_style = font_style

    def get_text_anchor(self) -> str:
        if self.align == 'center':
            return 'middle'
        elif self.align == 'right':
            return 'end'
        return 'start'

    def get_draw_x(self) -> float:
        if self.align == 'center':
            return self.center_x
        elif self.align == 'right':
            return self.x + self.width
        return self.x

    def get_draw_y(self) -> float:
        # Approximate vertical centering using a baseline offset
        return self.center_y + 5


class Container(LayoutNode):
    """A visual container typically rendered as a rounded rectangle."""
    
    def __init__(self, x: float = 0, y: float = 0, width: float = 0, height: float = 0,
                 padding: float = 15, margin: float = 10, 
                 corner_radius: float = styles.SHAPES["corner_radius_md"],
                 bg_color: str = styles.COLORS["background"], 
                 border_color: str = styles.COLORS["border"]):
        super().__init__(x, y, width, height, padding, margin)
        self.corner_radius = corner_radius
        self.bg_color = bg_color
        self.border_color = border_color
        self.title_block = None

    def set_title(self, text: str, height: float = 40) -> None:
        """Sets an inner title TextBlock at the top of the container."""
        self.title_block = TextBlock(text, self.inner_x, self.inner_y, self.inner_width, height, 
                                     align='center', font_style='subtitle')

    def arrange_children_vertically(self, spacing: float = 20) -> None:
        """Automatically computes Y coordinates for children to stack them vertically."""
        current_y = self.inner_y
        if self.title_block:
            current_y += self.title_block.height + spacing

        for child in self.children:
            # Horizontally center the child within the container
            child.x = self.inner_x + (self.inner_width - child.width) / 2
            child.y = current_y
            current_y += child.height + spacing


class Header(TextBlock):
    """Page or Section Header."""
    
    def __init__(self, text: str, canvas_width: float = styles.PAGE_WIDTH, height: float = 80):
        super().__init__(text, 0, 0, canvas_width, height, align='center', font_style='title')


class Column(Container):
    """Represents a primary column in the architecture diagram, auto-calculating its X position."""
    
    def __init__(self, title: str, index: int, total_columns: int, 
                 canvas_width: float = styles.PAGE_WIDTH, 
                 canvas_height: float = styles.PAGE_HEIGHT,
                 top_offset: float = 100, 
                 bg_color: str = styles.COLORS["background"]):
        
        # Compute equal width and spacing automatically
        usable_width = canvas_width - (2 * styles.MARGIN)
        
        # Calculate optimal width and spacing
        # If there are N columns, there are N-1 gaps
        gap_ratio = 0.2 # Space between columns relative to column width
        col_width = usable_width / (total_columns + (total_columns - 1) * gap_ratio)
        spacing = col_width * gap_ratio
        
        x = styles.MARGIN + index * (col_width + spacing)
        y = top_offset
        height = canvas_height - top_offset - styles.MARGIN
        
        super().__init__(x, y, col_width, height, padding=20, bg_color=bg_color)
        self.corner_radius = styles.SHAPES["corner_radius_lg"]
        self.border_color = bg_color # Border matches bg for soft headers
        
        # Initialize a sub-container specifically for the column header
        self.header = Container(self.x, self.y, self.width, 60, corner_radius=styles.SHAPES["corner_radius_lg"], 
                                bg_color=bg_color, border_color=bg_color)
        self.header.set_title(title, height=40)


class Section(Container):
    """A horizontal section that can encompass multiple columns or full rows."""
    
    def __init__(self, y: float, height: float, canvas_width: float = styles.PAGE_WIDTH,
                 bg_color: str = styles.COLORS["background"]):
        x = styles.MARGIN
        width = canvas_width - (2 * styles.MARGIN)
        super().__init__(x, y, width, height, padding=20, bg_color=bg_color)
        self.corner_radius = styles.SHAPES["corner_radius_lg"]
