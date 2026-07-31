"""
generate_pipeline.py
Orchestrator script that generates the complete architecture diagram.
Assembles all six columns, draws connectors, and exports to SVG, PNG, and PDF.
"""

import svgwrite
import components.styles as styles
from components.layout import Column, Container, TextBlock
import components.boxes as boxes
import components.icons as icons
import components.arrows as arrows

# We will use this dictionary to store the bounding boxes of key elements 
# so we can draw connecting arrows between them after all columns are drawn.
bounds = {}

def draw_column_1(dwg):
    col1 = Column("1. Data & Knowledge\nSources", index=0, total_columns=6, 
                  bg_color=styles.COLORS["col1_bg"], top_offset=50)
    dwg.add(boxes.draw_group_box(dwg, col1.header, title="1. Data & Knowledge\nSources", bg_color=styles.COLORS["col1_bg"]))
    
    benign_y = col1.header.y + col1.header.height + 30
    benign_h = 240
    benign_box = Container(col1.x, benign_y, col1.width, benign_h)
    dwg.add(boxes.draw_round_box(dwg, benign_box, bg_color="#ffffff", border_color=styles.COLORS["border"]))
    
    pill_w = benign_box.width * 0.8
    pill_x = benign_box.x + (benign_box.width - pill_w) / 2
    benign_pill = Container(pill_x, benign_box.y + 15, pill_w, 30)
    dwg.add(boxes.draw_round_box(dwg, benign_pill, text="Benign Knowledge Base", 
                                 bg_color=styles.COLORS["col1_bg"], border_color=styles.COLORS["col1_bg"], shadow=False, font_style="small"))
    
    wiki_x = benign_box.x + (benign_box.width * 0.28)
    wiki_y = benign_box.y + 120
    dwg.add(icons.draw_wikipedia_document(dwg, wiki_x, wiki_y, size=60, color=styles.COLORS["border"]))
    tb_wiki = TextBlock("Wikipedia Dump\n(Hotpot / NQ)", wiki_x - 50, wiki_y + 40, 100, 40, align="center", font_style="small")
    boxes._draw_text_multiline(dwg, dwg, tb_wiki, max_chars=18)
    
    docs_x = benign_box.x + (benign_box.width * 0.72)
    docs_y = benign_box.y + 120
    dwg.add(icons.draw_document_stack(dwg, docs_x, docs_y, size=60, color=styles.COLORS["border"]))
    tb_docs = TextBlock("Other Trusted\nDocuments", docs_x - 50, docs_y + 40, 100, 40, align="center", font_style="small")
    boxes._draw_text_multiline(dwg, dwg, tb_docs, max_chars=18)
    
    adv_y = benign_y + benign_h + 30
    adv_h = 320
    adv_box = Container(col1.x, adv_y, col1.width, adv_h)
    dwg.add(boxes.draw_round_box(dwg, adv_box, bg_color="#ffffff", border_color=styles.COLORS["border"]))
    
    adv_pill_h = 45
    adv_pill = Container(pill_x, adv_box.y + 15, pill_w, adv_pill_h)
    dwg.add(boxes.draw_round_box(dwg, adv_pill, text="Adversarial Additions\n(Poisoned Documents)", 
                                 bg_color="#ffcdd2", border_color="#f44336", shadow=False, font_style="small"))
    
    attack_start_y = adv_box.y + 100
    attacks = [
        ("Knowledge Poisoning", icons.draw_warning_bug),
        ("Instruction Injection", icons.draw_terminal_icon),
        ("Goal Hijacking", icons.draw_target_icon),
        ("Information Extraction", icons.draw_lock_icon),
    ]
    
    for i, (text, icon_fn) in enumerate(attacks):
        ay = attack_start_y + i * 55
        icon_color = "#37474f" if i > 0 else "#d32f2f"
        dwg.add(icon_fn(dwg, adv_box.x + 40, ay, size=35, color=icon_color))
        tb = TextBlock(text, adv_box.x + 75, ay - 10, adv_box.width - 80, 30, align="start", font_style="body")
        boxes._draw_text_multiline(dwg, dwg, tb, max_chars=30)
        
    bounds["col1"] = {"x_out": col1.x + col1.width, "y_center": adv_box.y - 15, "x_in": col1.x + (col1.width / 2), "y_bottom": adv_box.y + adv_box.height}

def draw_column_2(dwg):
    col2 = Column("2. Document Indexing\n(Offline)", index=1, total_columns=6, 
                  bg_color=styles.COLORS["col2_bg"], top_offset=50)
    dwg.add(boxes.draw_group_box(dwg, col2.header, title="2. Document Indexing\n(Offline)", bg_color=styles.COLORS["col2_bg"]))
    
    outer_box = Container(col2.x, col2.header.y + col2.header.height + 30, col2.width, 590)
    dwg.add(boxes.draw_round_box(dwg, outer_box, bg_color="#ffffff", border_color=styles.COLORS["border"]))
    
    inner_w = outer_box.width - 30
    inner_x = outer_box.x + 15
    
    chunk_box = Container(inner_x, outer_box.y + 25, inner_w, 130)
    dwg.add(boxes.draw_round_box(dwg, chunk_box, bg_color="#ffffff", border_color=styles.COLORS["border"], shadow=False))
    tb_chunk = TextBlock("Text Chunking\n(Overlap, Cleaning)", chunk_box.x, chunk_box.y + 10, chunk_box.width, 40, align="center", font_style="small")
    boxes._draw_text_multiline(dwg, dwg, tb_chunk, max_chars=25)
    dwg.add(icons.draw_chunks_icon(dwg, chunk_box.center_x, chunk_box.y + 85, size=70, color=styles.COLORS["border"]))
    dwg.add(arrows.draw_vertical_arrow(dwg, (chunk_box.center_x, chunk_box.y + 135), (chunk_box.center_x, chunk_box.y + 165)))
    
    embed_box = Container(inner_x, chunk_box.y + 170, inner_w, 160)
    dwg.add(boxes.draw_round_box(dwg, embed_box, bg_color="#ffffff", border_color=styles.COLORS["border"], shadow=False))
    tb_embed = TextBlock("Embedding\n(Sentence Encoder)", embed_box.x, embed_box.y + 10, embed_box.width, 40, align="center", font_style="small")
    boxes._draw_text_multiline(dwg, dwg, tb_embed, max_chars=25)
    dwg.add(icons.draw_vector_network(dwg, embed_box.center_x, embed_box.y + 100, size=70, color="#1976d2")) 
    dwg.add(arrows.draw_vertical_arrow(dwg, (embed_box.center_x, embed_box.y + 165), (embed_box.center_x, embed_box.y + 195)))
    
    db_box = Container(inner_x, embed_box.y + 200, inner_w, 130)
    dwg.add(boxes.draw_round_box(dwg, db_box, bg_color="#ffffff", border_color=styles.COLORS["border"], shadow=False))
    tb_db = TextBlock("Vector Database\n(FAISS Index)", db_box.x, db_box.y + 10, db_box.width, 40, align="center", font_style="small")
    boxes._draw_text_multiline(dwg, dwg, tb_db, max_chars=25)
    dwg.add(icons.draw_database_cylinder(dwg, db_box.center_x, db_box.y + 85, size=60, color="#1976d2"))
    
    bounds["col2"] = {"x_in": col2.x, "x_out": col2.x + col2.width, "y_center": embed_box.center_y}

def draw_column_3(dwg):
    col3 = Column("3. Query & Retrieval", index=2, total_columns=6, 
                  bg_color=styles.COLORS["col3_bg"], top_offset=50)
    dwg.add(boxes.draw_group_box(dwg, col3.header, title="3. Query & Retrieval", bg_color=styles.COLORS["col3_bg"]))
    
    outer_box = Container(col3.x, col3.header.y + col3.header.height + 30, col3.width, 590)
    dwg.add(boxes.draw_round_box(dwg, outer_box, bg_color="#ffffff", border_color=styles.COLORS["border"]))
    
    inner_w = outer_box.width - 30
    inner_x = outer_box.x + 15
    
    query_box = Container(inner_x, outer_box.y + 25, inner_w, 130)
    dwg.add(boxes.draw_round_box(dwg, query_box, bg_color="#ffffff", border_color=styles.COLORS["border"], shadow=False))
    tb_query = TextBlock("User Query", query_box.x, query_box.y + 10, query_box.width, 30, align="center", font_style="body")
    boxes._draw_text_multiline(dwg, dwg, tb_query, max_chars=25)
    
    query_pill = Container(inner_x + (inner_w * 0.1), query_box.y + 50, inner_w * 0.8, 60)
    dwg.add(boxes.draw_round_box(dwg, query_pill, bg_color="#f5f5f5", border_color=styles.COLORS["border"], shadow=False))
    tb_query_text = TextBlock('e.g., "What causes\nType 2 Diabetes?"', query_pill.x, query_pill.y + 12, query_pill.width, 40, align="center", font_style="small")
    boxes._draw_text_multiline(dwg, dwg, tb_query_text, max_chars=25)
    
    dwg.add(arrows.draw_vertical_arrow(dwg, (query_box.center_x, query_box.y + 135), (query_box.center_x, query_box.y + 165)))
    
    embed_box = Container(inner_x, query_box.y + 170, inner_w, 160)
    dwg.add(boxes.draw_round_box(dwg, embed_box, bg_color="#ffffff", border_color=styles.COLORS["border"], shadow=False))
    tb_embed = TextBlock("Query Embedding", embed_box.x, embed_box.y + 15, embed_box.width, 30, align="center", font_style="body")
    boxes._draw_text_multiline(dwg, dwg, tb_embed, max_chars=25)
    dwg.add(icons.draw_vector_network(dwg, embed_box.center_x, embed_box.y + 90, size=70, color="#fbc02d")) 
    
    dwg.add(arrows.draw_vertical_arrow(dwg, (embed_box.center_x, embed_box.y + 165), (embed_box.center_x, embed_box.y + 195)))
    
    db_box = Container(inner_x, embed_box.y + 200, inner_w, 160)
    dwg.add(boxes.draw_round_box(dwg, db_box, bg_color="#ffffff", border_color=styles.COLORS["border"], shadow=False))
    tb_db = TextBlock("Top-k Retrieval\n(FAISS)", db_box.x, db_box.y + 10, db_box.width, 40, align="center", font_style="small")
    boxes._draw_text_multiline(dwg, dwg, tb_db, max_chars=25)
    
    list_x = db_box.center_x - 50
    cy = db_box.y + 60
    c_cols = ["#90caf9", "#a5d6a7", "#ffe082"]
    for i, (n, col) in enumerate([("1", c_cols[0]), ("2", c_cols[1]), ("k", c_cols[2])]):
        y_offset = cy + (i * 30)
        if i == 2: y_offset += 15 # Gap for colon
        dwg.add(dwg.text(n, insert=(list_x, y_offset + 15), fill=styles.COLORS["text"], font_family=styles.FONT_FAMILY, font_size="14px", font_weight="bold"))
        dwg.add(dwg.rect(insert=(list_x + 25, y_offset), size=(60, 20), fill=col, stroke=styles.COLORS["border"], stroke_width=2))
        dwg.add(dwg.text("...", insert=(list_x + 95, y_offset + 15), fill=styles.COLORS["text"], font_family=styles.FONT_FAMILY, font_size="16px", font_weight="bold"))
    
    dwg.add(dwg.text(":", insert=(list_x, cy + 70), fill=styles.COLORS["text"], font_family=styles.FONT_FAMILY, font_size="14px", font_weight="bold"))
    
    bounds["col3"] = {"x_in": col3.x, "x_out": col3.x + col3.width, "y_center": embed_box.center_y}

def draw_column_4(dwg):
    col4 = Column("4. (Optional) RAGShield\nRetrieval Filtering", index=3, total_columns=6, 
                  bg_color=styles.COLORS["col4_bg"], top_offset=50)
    dwg.add(boxes.draw_group_box(dwg, col4.header, title="4. (Optional) RAGShield\nRetrieval Filtering", bg_color=styles.COLORS["col4_bg"]))
    
    outer_box = Container(col4.x, col4.header.y + col4.header.height + 30, col4.width, 590)
    dwg.add(boxes.draw_round_box(dwg, outer_box, bg_color="#ffffff", border_color=styles.COLORS["border"]))
    
    inner_w = outer_box.width - 30
    inner_x = outer_box.x + 15
    current_y = outer_box.y + 20
    
    steps = [
        ("Instruction Detector\n(Heuristic / LLM-based)", icons.draw_shield, styles.COLORS["ragshield_inner"], styles.COLORS["ragshield_border"]),
        ("Semantic Consensus\n(Embedding Similarity)", icons.draw_people_icon, styles.COLORS["ragshield_inner"], styles.COLORS["ragshield_border"]),
        ("Trust Scoring\n(Retrieval Trust Index)", icons.draw_gauge, styles.COLORS["ragshield_inner"], styles.COLORS["ragshield_border"]),
        ("Re-ranking & Filtering\n(Threshold τ)", icons.draw_filter_funnel, styles.COLORS["ragshield_inner"], styles.COLORS["ragshield_border"]),
        ("Sanitized Context\n(Filtered Chunks)", icons.draw_sanitized_document, styles.COLORS["sanitized"], styles.COLORS["sanitized_border"])
    ]
    
    prev_box = None
    for i, (text, icon_fn, bg, border) in enumerate(steps):
        box = Container(inner_x, current_y, inner_w, 75)
        dwg.add(boxes.draw_round_box(dwg, box, bg_color=bg, border_color=border, shadow=False))
        dwg.add(icon_fn(dwg, box.x + 35, box.center_y, size=40, color=border))
        tb = TextBlock(text.replace("tau", "τ"), box.x + 70, box.y + 12, box.width - 75, box.height, align="start", font_style="small")
        boxes._draw_text_multiline(dwg, dwg, tb, max_chars=30)
        
        if prev_box is not None:
            dwg.add(arrows.draw_vertical_arrow(dwg, (prev_box.center_x, prev_box.y + prev_box.height + 5), (box.center_x, box.y - 5)))
        prev_box = box
        current_y += 110
        
    bounds["col4"] = {"x_in": col4.x, "x_out": col4.x + col4.width, "y_center": outer_box.center_y}

def draw_column_5(dwg):
    col5 = Column("5. Prompt Construction\n& Generation", index=4, total_columns=6, 
                  bg_color=styles.COLORS["col5_bg"], top_offset=50)
    dwg.add(boxes.draw_group_box(dwg, col5.header, title="5. Prompt Construction\n& Generation", bg_color=styles.COLORS["col5_bg"]))
    
    outer_box = Container(col5.x, col5.header.y + col5.header.height + 30, col5.width, 590)
    dwg.add(boxes.draw_round_box(dwg, outer_box, bg_color="#ffffff", border_color=styles.COLORS["border"]))
    
    inner_w = outer_box.width - 40
    inner_x = outer_box.x + 20
    
    prompt_box = Container(inner_x, outer_box.y + 25, inner_w, 200)
    dwg.add(boxes.draw_round_box(dwg, prompt_box, bg_color="#ffffff", border_color=styles.COLORS["border"], shadow=False))
    tb_prompt = TextBlock("Prompt Template", prompt_box.x, prompt_box.y + 15, prompt_box.width, 30, align="center", font_style="body")
    boxes._draw_text_multiline(dwg, dwg, tb_prompt, max_chars=25)
    dwg.add(icons.draw_clipboard(dwg, prompt_box.x + 35, prompt_box.y + 110, size=50, color=styles.COLORS["border"]))
    
    for i, item in enumerate(["+ System Prompt", "+ Instructions", "+ Retrieved Context", "+ User Query"]):
        dwg.add(dwg.text(item, insert=(prompt_box.x + 70, prompt_box.y + 80 + (i * 25)), 
                         fill=styles.COLORS["text"], font_family=styles.FONT_FAMILY, font_size="12px", font_weight="bold"))
                         
    dwg.add(arrows.draw_vertical_arrow(dwg, (prompt_box.center_x, prompt_box.y + 205), (prompt_box.center_x, prompt_box.y + 235)))
    
    llm_box = Container(inner_x, prompt_box.y + 240, inner_w, 190)
    dwg.add(boxes.draw_round_box(dwg, llm_box, bg_color="#ffffff", border_color=styles.COLORS["border"], shadow=False))
    tb_llm = TextBlock("LLM Generation\n(Local Models)", llm_box.x, llm_box.y + 15, llm_box.width, 40, align="center", font_style="small")
    boxes._draw_text_multiline(dwg, dwg, tb_llm, max_chars=25)
    dwg.add(icons.draw_model_logos(dwg, llm_box.center_x, llm_box.y + 100, size=90))
    dwg.add(dwg.text("Mistral · Qwen2.5 · Llama 3.1", insert=(llm_box.center_x, llm_box.y + 165), 
                     text_anchor="middle", fill=styles.COLORS["text_light"], font_family=styles.FONT_FAMILY, font_size="11px", font_weight="bold"))
                     
    dwg.add(arrows.draw_vertical_arrow(dwg, (llm_box.center_x, llm_box.y + 195), (llm_box.center_x, llm_box.y + 225)))
    
    out_box = Container(inner_x, llm_box.y + 230, inner_w, 110)
    dwg.add(boxes.draw_round_box(dwg, out_box, bg_color="#ffffff", border_color=styles.COLORS["border"], shadow=False))
    tb_out = TextBlock("Model Output\n(Response)", out_box.x, out_box.y + 15, out_box.width, 40, align="center", font_style="small")
    boxes._draw_text_multiline(dwg, dwg, tb_out, max_chars=25)
    
    out_pill = Container(out_box.x + 10, out_box.y + 55, out_box.width - 20, 45)
    dwg.add(boxes.draw_round_box(dwg, out_pill, bg_color="#f5f5f5", border_color=styles.COLORS["border"], shadow=False))
    dwg.add(icons.draw_chat_bubble(dwg, out_pill.x + 25, out_pill.center_y, size=35, color=styles.COLORS["border"]))
    tb_ans = TextBlock("Generated Answer", out_pill.x + 55, out_pill.y + 12, out_pill.width - 55, 30, align="start", font_style="small")
    boxes._draw_text_multiline(dwg, dwg, tb_ans, max_chars=25)
    
    bounds["col5"] = {"x_in": col5.x, "x_out": col5.x + col5.width, "y_center": llm_box.center_y}

def draw_column_6(dwg):
    col6 = Column("6. Evaluation\n(Offline)", index=5, total_columns=6, 
                  bg_color=styles.COLORS["col6_bg"], top_offset=50)
    dwg.add(boxes.draw_group_box(dwg, col6.header, title="6. Evaluation\n(Offline)", bg_color=styles.COLORS["col6_bg"]))
    
    outer_box = Container(col6.x, col6.header.y + col6.header.height + 30, col6.width, 590)
    dwg.add(boxes.draw_round_box(dwg, outer_box, bg_color="#ffffff", border_color=styles.COLORS["border"]))
    
    current_y = outer_box.y + 10
    sections = [
        ("Security Metrics", icons.draw_shield, ["• ASR (Attack Success Rate)", "• Containment Accuracy", "• Failure Mode Analysis"], "#1976d2"),
        ("Retrieval Metrics", icons.draw_magnifying_glass, ["• RCR (Retrieval Corruption Rate)", "• nDCG / Recall@k"], "#455a64"),
        ("Utility Metrics", icons.draw_bar_chart, ["• Answer F1 / EM", "• Semantic Similarity", "• Answer Relevance"], "#455a64"),
        ("Analysis & Reporting", icons.draw_report_icon, ["• Attack-wise Analysis", "• Model-wise Comparison", "• RAGShield Impact"], "#1976d2")
    ]
    
    for i, (title, icon_fn, points, icon_color) in enumerate(sections):
        section_h = 45 + (len(points) * 23)
        dwg.add(dwg.text(title, insert=(outer_box.center_x, current_y + 20), 
                         fill=styles.COLORS["text"], font_family=styles.FONT_FAMILY, 
                         font_size="13px", font_weight="bold", text_anchor="middle"))
        
        icon_x = outer_box.x + 35
        dwg.add(icon_fn(dwg, icon_x, current_y + 60, size=40, color=icon_color))
        
        for j, pt in enumerate(points):
            dwg.add(dwg.text(pt, insert=(icon_x + 30, current_y + 48 + (j * 23)), 
                             fill=styles.COLORS["text"], font_family=styles.FONT_FAMILY, 
                             font_size="11px", font_weight="bold"))
                             
        current_y += section_h
        if i < len(sections) - 1:
            dwg.add(dwg.line((outer_box.x + 15, current_y + 5), (outer_box.x + outer_box.width - 15, current_y + 5), 
                             stroke=styles.COLORS["border"], stroke_width=1))
            current_y += 10
            
    bounds["col6"] = {"x_in": col6.x, "y_center": outer_box.center_y, "x_center": col6.x + (col6.width / 2), "y_bottom": outer_box.y + outer_box.height}


def draw_connections(dwg):
    """Draws horizontal arrows between columns and the feedback loop."""
    arr_color = "#1976d2"
    
    # 1 -> 2
    dwg.add(arrows.draw_horizontal_arrow(dwg, (bounds["col1"]["x_out"], bounds["col1"]["y_center"]), 
                                              (bounds["col2"]["x_in"], bounds["col1"]["y_center"]), color=arr_color))
    # 2 -> 3
    dwg.add(arrows.draw_horizontal_arrow(dwg, (bounds["col2"]["x_out"], bounds["col2"]["y_center"]), 
                                              (bounds["col3"]["x_in"], bounds["col2"]["y_center"]), color=arr_color))
    # 3 -> 4
    dwg.add(arrows.draw_horizontal_arrow(dwg, (bounds["col3"]["x_out"], bounds["col3"]["y_center"]), 
                                              (bounds["col4"]["x_in"], bounds["col3"]["y_center"]), color=arr_color))
    # 4 -> 5
    dwg.add(arrows.draw_horizontal_arrow(dwg, (bounds["col4"]["x_out"], bounds["col4"]["y_center"]), 
                                              (bounds["col5"]["x_in"], bounds["col4"]["y_center"]), color=arr_color))
    # 5 -> 6
    dwg.add(arrows.draw_horizontal_arrow(dwg, (bounds["col5"]["x_out"], bounds["col5"]["y_center"]), 
                                              (bounds["col6"]["x_in"], bounds["col5"]["y_center"]), color=arr_color))
                                              
    # Feedback loop: from Col 6 bottom to Col 1 bottom
    fb_start = (bounds["col6"]["x_center"], bounds["col6"]["y_bottom"] + 10)
    fb_end = (bounds["col1"]["x_in"], bounds["col1"]["y_bottom"] + 10)
    # The arrow drops down, goes left, goes up. We can use draw_feedback_arrow
    dwg.add(arrows.draw_feedback_arrow(dwg, fb_start, fb_end, offset_y=60, color="#757575", dashed=True))
    
    # Add feedback loop text
    text_x = styles.PAGE_WIDTH / 2
    text_y = fb_start[1] + 80
    dwg.add(dwg.text("Iterative Refinement (Attack Generation / Parameter Tuning / Threshold Adjustment)", 
                     insert=(text_x, text_y), text_anchor="middle", fill="#757575", 
                     font_family=styles.FONT_FAMILY, font_size="14px", font_weight="bold"))


def generate():
    # Initialize Canvas
    dwg = svgwrite.Drawing('pipeline.svg', size=(styles.PAGE_WIDTH, styles.PAGE_HEIGHT + 100))
    styles.setup_svg_defs(dwg)
    
    # Draw all columns
    draw_column_1(dwg)
    draw_column_2(dwg)
    draw_column_3(dwg)
    draw_column_4(dwg)
    draw_column_5(dwg)
    draw_column_6(dwg)
    
    # Draw Connections
    draw_connections(dwg)
    
    # Save SVG
    dwg.save()
    print("Successfully generated pipeline.svg")
    
    # Export to PDF and PNG
    try:
        import cairosvg
        print("Exporting to pipeline.pdf...")
        cairosvg.svg2pdf(url='pipeline.svg', write_to='pipeline.pdf')
        print("Exporting to pipeline.png...")
        cairosvg.svg2png(url='pipeline.svg', write_to='pipeline.png')
        print("All formats successfully exported!")
    except Exception as e:
        print(f"Export failed (cairosvg/cairo might not be installed properly): {e}")

if __name__ == '__main__':
    generate()
