#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur dossier.md -> dossier.tex (moteur cible : pdflatex).

Ce script n'est PAS le « builder » : il produit une fois le fichier
dossier.tex (artefact versionné). La compilation .tex -> .pdf se fait
ensuite via le Makefile (pdflatex). On le garde uniquement pour pouvoir
régénérer le .tex si le .md change.

Usage :
    python build_tex.py      # depuis le dossier report/
Écrit : dossier.tex
"""

import re

SOURCE = "dossier.md"
CIBLE = "dossier.tex"

# ---------------------------------------------------------------------------
# Préambule + page de garde (rédigés à la main : front-matter « propre »).
# ---------------------------------------------------------------------------
PREAMBULE = r"""\documentclass[11pt,a4paper]{article}

\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[french]{babel}
\usepackage{lmodern}
\usepackage{textcomp}
\usepackage{graphicx}
\usepackage{array}
\usepackage{longtable}
\usepackage[a4paper,margin=2.5cm]{geometry}
\usepackage{parskip}
\usepackage[hidelinks]{hyperref}

% --- Caractères Unicode non couverts par inputenc, pour pdflatex ---------
\DeclareUnicodeCharacter{2264}{\ensuremath{\leq}}
\DeclareUnicodeCharacter{2265}{\ensuremath{\geq}}
\DeclareUnicodeCharacter{2260}{\ensuremath{\neq}}
\DeclareUnicodeCharacter{2192}{\ensuremath{\rightarrow}}
\DeclareUnicodeCharacter{2194}{\ensuremath{\leftrightarrow}}
\DeclareUnicodeCharacter{27F7}{\ensuremath{\longleftrightarrow}}
\DeclareUnicodeCharacter{22C8}{\ensuremath{\bowtie}}
\DeclareUnicodeCharacter{2248}{\ensuremath{\approx}}
\DeclareUnicodeCharacter{2212}{\ensuremath{-}}
\DeclareUnicodeCharacter{221D}{\ensuremath{\propto}}
\DeclareUnicodeCharacter{1D49}{\textsuperscript{e}}
\DeclareUnicodeCharacter{00B2}{\textsuperscript{2}}
\DeclareUnicodeCharacter{00B3}{\textsuperscript{3}}
\DeclareUnicodeCharacter{FFFD}{?}

\title{Projet Data en Python\\[0.2cm]\large Accidents de la route}
\author{Rayan Leveque}
\date{Juin 2026}

\begin{document}

\begin{titlepage}
\centering
\vspace*{2cm}
{\large\textbf{M2 MIMO --- Université Paris 1 Panthéon-Sorbonne}}\\[0.3cm]
{\large Année universitaire 2025-2026}\\[3cm]
{\Huge\bfseries Projet Data en Python\par}
\vspace{0.4cm}
{\Huge\bfseries Accidents de la route\par}
\vspace{0.8cm}
{\Large Analyse du fichier BAAC, années 2005--2015\par}
\vspace{3cm}
{\large Encadrants : Georges Grosz, Louis Giron}\\[0.6cm]
{\large\textbf{Auteur : Rayan Leveque}}\\[0.3cm]
{\large Juin 2026}
\vfill
\end{titlepage}

"""

PIED = "\n\\end{document}\n"

# ---------------------------------------------------------------------------
# Échappement LaTeX
# ---------------------------------------------------------------------------
_ECHAPPE = {
    "\\": r"\textbackslash{}",
    "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
    "_": r"\_", "{": r"\{", "}": r"\}",
    "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
}


def echappe(texte):
    """Échappe les caractères spéciaux LaTeX, caractère par caractère
    (pour ne pas ré-échapper les antislashs qu'on vient d'insérer)."""
    return "".join(_ECHAPPE.get(c, c) for c in texte)


def en_ligne(texte):
    """Convertit le markup en ligne : code `...`, liens, gras, italique."""
    jetons = []

    def ranger(s):
        jetons.append(s)
        return f"\x00{len(jetons) - 1}\x00"

    # code `...` -> \texttt{...}
    texte = re.sub(r"`([^`]+)`",
                   lambda m: ranger(r"\texttt{" + echappe(m.group(1)) + "}"),
                   texte)
    # liens [txt](url) -> \href{url}{txt}
    texte = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                   lambda m: ranger(r"\href{" + m.group(2) + "}{" + echappe(m.group(1)) + "}"),
                   texte)
    # échappement du texte restant
    texte = echappe(texte)
    # gras puis italique (les marqueurs * survivent à l'échappement)
    texte = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", texte)
    texte = re.sub(r"\*([^*]+)\*", r"\\emph{\1}", texte)
    # restauration des jetons
    texte = re.sub(r"\x00(\d+)\x00", lambda m: jetons[int(m.group(1))], texte)
    return texte


# ---------------------------------------------------------------------------
# Conversion bloc par bloc (machine à états ligne par ligne)
# ---------------------------------------------------------------------------
NIVEAU = {1: "section", 2: "subsection", 3: "subsubsection",
          4: "paragraph", 5: "paragraph", 6: "paragraph"}


def titre_latex(niveau, titre):
    cmd = NIVEAU[niveau]
    t = en_ligne(titre)
    return f"\\{cmd}*{{{t}}}\n\\addcontentsline{{toc}}{{{cmd}}}{{{t}}}\n"


def alignement(cellule):
    c = cellule.strip()
    if c.startswith(":") and c.endswith(":"):
        return "c"
    if c.endswith(":"):
        return "r"
    return "l"


def cellules(ligne):
    """Découpe une ligne de tableau markdown en cellules."""
    parties = ligne.split("|")
    # retire les bouts vides de début/fin dus aux | extérieurs
    if parties and parties[0].strip() == "":
        parties = parties[1:]
    if parties and parties[-1].strip() == "":
        parties = parties[:-1]
    return [p.strip() for p in parties]


def rend_tableau(lignes):
    entete = cellules(lignes[0])
    aligns = [alignement(c) for c in cellules(lignes[1])]
    corps = [cellules(l) for l in lignes[2:]]
    n = len(entete)
    # complète/tronque les alignements au nombre de colonnes
    while len(aligns) < n:
        aligns.append("l")
    aligns = aligns[:n]
    spec = " ".join(aligns)

    out = ["\\begin{center}", f"\\begin{{tabular}}{{{spec}}}", "\\hline"]
    out.append(" & ".join(r"\textbf{" + en_ligne(c) + "}" for c in entete) + r" \\")
    out.append("\\hline")
    for ligne in corps:
        # ajuste la ligne au nombre de colonnes
        ligne = (ligne + [""] * n)[:n]
        out.append(" & ".join(en_ligne(c) for c in ligne) + r" \\")
    out.append("\\hline")
    out += ["\\end{tabular}", "\\end{center}", ""]
    return "\n".join(out)


def rend_image(legende, chemin):
    leg = en_ligne(legende)
    return ("\\begin{figure}[h]\n\\centering\n"
            f"\\includegraphics[width=0.85\\linewidth]{{{chemin}}}\n"
            f"\\caption{{{leg}}}\n\\end{{figure}}\n")


RE_TITRE = re.compile(r"^(#{1,6})\s+(.*)$")
RE_IMAGE = re.compile(r"^!\[(.*?)\]\((.*?)\)\s*$")
RE_HR = re.compile(r"^---+\s*$")
RE_COMMENT = re.compile(r"^<!--.*-->\s*$")
RE_PUCE = re.compile(r"^-\s+(.*)$")


def convertir(lignes):
    sortie = []
    mode = None          # None | 'para' | 'liste' | 'tableau'
    tampon = []          # lignes en cours d'accumulation
    sauter_section = False  # ignorer le contenu d'une section (Page de garde)

    def vider():
        nonlocal mode, tampon
        if not tampon:
            mode = None
            return
        if mode == "para":
            sortie.append(en_ligne(" ".join(tampon)) + "\n")
        elif mode == "liste":
            sortie.append("\\begin{itemize}")
            for item in tampon:
                sortie.append("\\item " + en_ligne(item))
            sortie.append("\\end{itemize}\n")
        elif mode == "tableau":
            sortie.append(rend_tableau(tampon))
        tampon = []
        mode = None

    for ligne in lignes:
        brut = ligne.rstrip("\n")

        m = RE_TITRE.match(brut)
        if m:
            vider()
            niveau = len(m.group(1))
            titre = m.group(2).strip()
            # cas particuliers du front-matter
            if titre == "Page de garde":
                sauter_section = True
                continue
            if titre == "Table des matières":
                sauter_section = True
                sortie.append("\\tableofcontents\n\\newpage\n")
                continue
            sauter_section = False
            sortie.append(titre_latex(niveau, titre))
            continue

        if sauter_section:
            continue

        if RE_COMMENT.match(brut.strip()):
            continue

        if brut.strip() == "":
            vider()
            continue

        if RE_HR.match(brut):
            vider()
            continue

        mi = RE_IMAGE.match(brut)
        if mi:
            vider()
            sortie.append(rend_image(mi.group(1), mi.group(2)))
            continue

        if brut.lstrip().startswith("|"):
            if mode != "tableau":
                vider()
                mode = "tableau"
            tampon.append(brut.strip())
            continue

        mp = RE_PUCE.match(brut)
        if mp:
            if mode != "liste":
                vider()
                mode = "liste"
            tampon.append(mp.group(1).strip())
            continue

        # texte ordinaire -> paragraphe
        if mode != "para":
            vider()
            mode = "para"
        tampon.append(brut.strip())

    vider()
    return "\n".join(sortie)


def main():
    with open(SOURCE, encoding="utf-8") as f:
        contenu = f.read()

    lignes = contenu.split("\n")
    # on saute le bloc YAML (entre les deux premiers ---) et on démarre
    # le corps converti à « # En-tête » (la page de garde est dans le préambule).
    debut = next(i for i, l in enumerate(lignes) if l.strip() == "# En-tête")
    corps = convertir(lignes[debut:])

    with open(CIBLE, "w", encoding="utf-8") as f:
        f.write(PREAMBULE)
        f.write(corps)
        f.write(PIED)

    print(f"{CIBLE} généré ({corps.count(chr(10))} lignes de corps).")


if __name__ == "__main__":
    main()
