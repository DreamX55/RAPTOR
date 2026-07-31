import os
import shutil
import subprocess

PAPER_DIR = "paper"
TEMPLATE_DIR = os.path.join(PAPER_DIR, "IEEE-conference-template-062824")

# Directories to ensure
dirs = [
    os.path.join(TEMPLATE_DIR, "sections"),
    os.path.join(TEMPLATE_DIR, "bibliography"),
    os.path.join(TEMPLATE_DIR, "figures"),
    os.path.join(TEMPLATE_DIR, "tables"),
    os.path.join(TEMPLATE_DIR, "notes"),
    os.path.join(TEMPLATE_DIR, "output"),
    os.path.join(PAPER_DIR, "sections"),
    os.path.join(PAPER_DIR, "bibliography")
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

# 1. Create Placeholder Sections in sections/
sections = [
    ("00_title.tex", "% TODO: Add Title, Authors, and Affiliations\n"),
    ("01_abstract.tex", "\\begin{abstract}\n% TODO: Add Abstract\n\\end{abstract}\n\n\\begin{IEEEkeywords}\n% TODO: Add Keywords\n\\end{IEEEkeywords}\n"),
    ("02_introduction.tex", "\\section{Introduction}\n% TODO: Add Introduction content\n"),
    ("03_related_work.tex", "\\section{Related Work}\n% TODO: Add Related Work content\n"),
    ("04_methodology.tex", "\\section{Threat Model and Empirical Attack Analysis}\n% TODO: Add Methodology content\n"),
    ("05_results.tex", "\\section{Experimental Results and Bottleneck Analysis}\n% TODO: Add Results content\n"),
    ("06_ragshield.tex", "\\section{RAGShield Defense Framework and Optimization}\n% TODO: Add RAGShield Defense content\n"),
    ("07_conclusion.tex", "\\section{Conclusion and Future Work}\n% TODO: Add Conclusion content\n")
]

for filename, content in sections:
    for target_dir in [os.path.join(TEMPLATE_DIR, "sections"), os.path.join(PAPER_DIR, "sections")]:
        filepath = os.path.join(target_dir, filename)
        with open(filepath, "w") as f:
            f.write(content)

# 2. Create Bibliography File & Copy IEEEtran.bst
bib_dir = os.path.join(TEMPLATE_DIR, "bibliography")
ref_bib = os.path.join(bib_dir, "references.bib")
if not os.path.exists(ref_bib):
    with open(ref_bib, "w") as f:
        f.write("% IEEE Bibliography File\n% TODO: Populate references\n")

# Copy IEEEtran.bst to template dir & bib dir if available
bst_src = os.path.join(TEMPLATE_DIR, "IEEEtranBST2", "IEEEtran.bst")
if os.path.exists(bst_src):
    shutil.copyfile(bst_src, os.path.join(TEMPLATE_DIR, "IEEEtran.bst"))
    shutil.copyfile(bst_src, os.path.join(bib_dir, "IEEEtran.bst"))

# 3. Create Modular ragshield_icdds2026.tex
main_tex_content = r"""\documentclass[conference]{IEEEtran}
\IEEEoverridecommandlockouts

% Standard IEEE Packages
\usepackage{cite}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{algorithmic}
\usepackage{graphicx}
\usepackage{textcomp}
\usepackage{xcolor}

% Set Graphics Path
\graphicspath{{figures/}}

\def\BibTeX{{\rm B\kern-.05em{\sc i\kern-.025em b}\kern-.08em
    T\kern-.1667em\lower.7ex\hbox{E}\kern-.125emX}}

\begin{document}

\title{RAGShield: Defending Retrieval-Augmented Generation Systems Against Indirect Prompt Injection}

\author{\IEEEauthorblockN{Anonymous Author(s)}
\IEEEauthorblockA{\textit{Department of Computer Science} \\
\textit{Institution}\\
City, Country \\
email@domain.com}
}

\maketitle

\input{sections/01_abstract.tex}
\input{sections/02_introduction.tex}
\input{sections/03_related_work.tex}
\input{sections/04_methodology.tex}
\input{sections/05_results.tex}
\input{sections/06_ragshield.tex}
\input{sections/07_conclusion.tex}

\bibliographystyle{IEEEtran}
\bibliography{bibliography/references}

\end{document}
"""

with open(os.path.join(TEMPLATE_DIR, "ragshield_icdds2026.tex"), "w") as f:
    f.write(main_tex_content)

print("Modular setup completed successfully.")
