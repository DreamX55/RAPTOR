import os
import shutil
import matplotlib.pyplot as plt
import matplotlib.patches as patches

PAPER_DIR = "paper"
TEMPLATE_DIR = os.path.join(PAPER_DIR, "IEEE-conference-template-062824")

# ---------------------------------------------------------
# 1. Rename Section 06 -> 06_defense.tex
# ---------------------------------------------------------
for base_d in [PAPER_DIR, TEMPLATE_DIR]:
    old_sec = os.path.join(base_d, "sections", "06_ragshield.tex")
    new_sec = os.path.join(base_d, "sections", "06_defense.tex")
    if os.path.exists(old_sec):
        os.remove(old_sec)
    
    sec_content = """\\section{Retrieval Trust Framework (RAGShield)}
% TODO: Add RAGShield Defense Content
% - RAGShield architecture
% - Retrieval Trust Index (RTI)
% - Defense evaluation
% - Phase 6.5 optimization summary
% - Limitations
% - Transition to future work
"""
    with open(new_sec, "w") as f:
        f.write(sec_content)

# Update ragshield_icdds2026.tex \input statement
tex_file = os.path.join(TEMPLATE_DIR, "ragshield_icdds2026.tex")
if os.path.exists(tex_file):
    with open(tex_file, "r") as f:
        content = f.read()
    content = content.replace(r"\input{sections/06_ragshield.tex}", r"\input{sections/06_defense.tex}")
    with open(tex_file, "w") as f:
        f.write(content)

print("Task 1 Complete: Section 06 renamed to 06_defense.tex and TeX input updated.")

# ---------------------------------------------------------
# 2. Move Table 5 & Table 6 to supplementary_tables/
# ---------------------------------------------------------
for base_d in [PAPER_DIR, TEMPLATE_DIR]:
    supp_tbl_dir = os.path.join(base_d, "supplementary_tables")
    os.makedirs(supp_tbl_dir, exist_ok=True)
    for t_name in ["table5_optimization_results.md", "table6_system_overhead.md"]:
        src = os.path.join(base_d, "tables", t_name)
        dst = os.path.join(supp_tbl_dir, t_name)
        if os.path.exists(src):
            shutil.move(src, dst)

print("Task 2 Complete: Moved Table 5 and Table 6 to supplementary_tables/.")

# ---------------------------------------------------------
# 3. Create RAGShield Architecture Diagram for Figure 5
#    Move RTI distribution plot to supplementary_figures/
# ---------------------------------------------------------
for base_d in [PAPER_DIR, TEMPLATE_DIR]:
    supp_fig_dir = os.path.join(base_d, "supplementary_figures")
    os.makedirs(supp_fig_dir, exist_ok=True)
    
    # Move original trust_index_distribution.png to supplementary_figures
    old_rti = os.path.join(REPORTS_DIR if 'REPORTS_DIR' in locals() else "reports", "phase6", "figures", "trust_index_distribution.png")
    if os.path.exists(old_rti):
        shutil.copyfile(old_rti, os.path.join(supp_fig_dir, "trust_index_distribution.png"))

# Generate RAGShield Architecture Diagram with Matplotlib
def generate_architecture_diagram(output_path):
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off')
    
    # Custom colors
    bg_color = "#f8f9fa"
    border_color = "#212529"
    box_blue = "#d0e1fd"
    box_red = "#fde2e4"
    box_green = "#e2f0d9"
    box_purple = "#e8dff5"
    box_yellow = "#fff2cc"

    # Draw RAGShield Subgraph Box
    rect_ragshield = patches.FancyBboxPatch((2.2, 0.8), 5.6, 4.4, boxstyle="round,pad=0.2",
                                            linewidth=2, edgecolor="#495057", facecolor="#f1f3f5", linestyle="--")
    ax.add_patch(rect_ragshield)
    ax.text(5.0, 4.9, "RAGShield Framework", fontsize=13, fontweight='bold', ha='center', color="#343a40")

    # Define Node Positions (x, y, text, color)
    nodes = {
        "query": (0.8, 3.0, "User Query", box_blue),
        "faiss": (2.6, 3.0, "FAISS\nRetrieval", box_blue),
        "inst": (4.2, 4.2, "Instruction\nDetector", box_red),
        "cons": (4.2, 3.0, "Semantic\nConsensus", box_red),
        "conf": (4.2, 1.8, "Retrieval\nConfidence", box_red),
        "rti": (5.8, 3.0, "Retrieval Trust\nIndex (RTI)", box_yellow),
        "rerank": (7.0, 3.0, "Intelligent\nRe-ranking", box_purple),
        "sanitizer": (7.0, 1.6, "Context\nSanitizer", box_purple),
        "prompt": (8.8, 3.0, "Prompt\nConstruction", box_green),
        "llm": (8.8, 1.6, "Language\nModel (LLM)", box_green),
        "answer": (10.2, 1.6, "Final\nAnswer", box_green)
    }

    # Draw Nodes
    for key, (x, y, label, col) in nodes.items():
        w = 1.0 if "\n" not in label else 1.1
        box = patches.FancyBboxPatch((x - w/2, y - 0.4), w, 0.8, boxstyle="round,pad=0.1",
                                    linewidth=1.5, edgecolor=border_color, facecolor=col)
        ax.add_patch(box)
        ax.text(x, y, label, fontsize=9, fontweight='bold', ha='center', va='center', color=border_color)

    # Draw Connections (Arrows)
    arrows = [
        ("query", "faiss", ""),
        ("faiss", "inst", "Top-k"),
        ("faiss", "cons", ""),
        ("faiss", "conf", ""),
        ("inst", "rti", ""),
        ("cons", "rti", ""),
        ("conf", "rti", ""),
        ("rti", "rerank", "RTI Score"),
        ("rerank", "sanitizer", ""),
        ("sanitizer", "prompt", "Sanitized Context"),
        ("prompt", "llm", ""),
        ("llm", "answer", "")
    ]

    for src, dst, label in arrows:
        x1, y1, _, _ = nodes[src]
        x2, y2, _, _ = nodes[dst]
        
        ax.annotate("", xy=(x2 - 0.55 if x2 > x1 else x2, y2), xytext=(x1 + 0.55 if x1 < x2 else x1, y1),
                    arrowprops=dict(arrowstyle="->", lw=1.5, color="#212529", connectionstyle="arc3,rad=0"))
        
        if label:
            mx, my = (x1 + x2)/2, (y1 + y2)/2
            ax.text(mx, my + 0.15, label, fontsize=8, fontstyle='italic', ha='center', va='center', color="#495057")

    ax.set_xlim(-0.2, 11.0)
    ax.set_ylim(0.5, 5.5)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated RAGShield Architecture Diagram: {output_path}")

for base_d in [PAPER_DIR, TEMPLATE_DIR]:
    fig5_dir = os.path.join(base_d, "figures")
    os.makedirs(fig5_dir, exist_ok=True)
    fig5_path = os.path.join(fig5_dir, "figure5_ragshield_architecture.png")
    generate_architecture_diagram(fig5_path)

print("Task 3 Complete: RAGShield Architecture Diagram generated for Figure 5.")

print("Refinement script setup completed.")
