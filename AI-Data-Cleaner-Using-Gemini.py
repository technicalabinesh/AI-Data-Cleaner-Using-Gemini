# -*- coding: utf-8 -*-
"""AI Data Cleaner - Premium Edition with PDF Reports & Large Dataset Support"""

import streamlit as st
import pandas as pd
import numpy as np
import io
import time
import datetime
import math
import google.generativeai as genai
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether, ListFlowable, ListItem
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import Flowable
from reportlab.lib.colors import HexColor

# ─────────────────────────────────────────────
# PAGE CONFIG & GLOBAL STYLES
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Gemini The Data Analyzer",
    page_icon="*",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=Inter:wght@300;400;500;600&display=swap');

/* Reset & Base */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #080B14 !important;
    color: #E8EBF4 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* Hero Banner */
.hero {
    background: linear-gradient(135deg, #080B14 0%, #0D1526 40%, #091220 100%);
    border-bottom: 1px solid rgba(64,200,255,0.15);
    padding: 60px 64px 52px;
    position: relative;
    overflow: hidden;
    text-align: center;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 420px; height: 420px;
    background: radial-gradient(circle, rgba(64,200,255,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -80px; left: 20%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(100,80,255,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(64,200,255,0.08);
    border: 1px solid rgba(64,200,255,0.25);
    border-radius: 100px;
    padding: 5px 14px;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #40C8FF;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 22px;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(42px, 6vw, 72px);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    color: #FFFFFF;
    margin-bottom: 18px;
}
.hero-title span {
    background: linear-gradient(90deg, #40C8FF, #7B6EF6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-title .the {
    background: linear-gradient(90deg, #FBBF24, #F87171);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 16px;
    font-weight: 300;
    color: #8B92AA;
    max-width: 600px;
    line-height: 1.7;
    margin: 0 auto;
}
.hero-stats {
    display: flex;
    gap: 40px;
    margin-top: 40px;
    justify-content: center;
}
.stat-item { text-align: center; }
.stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: #40C8FF;
}
.stat-label {
    font-size: 12px;
    color: #5A6178;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 2px;
}

/* Main Layout */
.main-layout {
    display: grid;
    grid-template-columns: 360px 1fr;
    gap: 0;
    min-height: calc(100vh - 200px);
}
.sidebar-panel {
    background: #0A0E1A;
    border-right: 1px solid rgba(255,255,255,0.06);
    padding: 32px 28px;
}
.content-panel {
    padding: 40px 48px;
}

/* Section Headers */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
}
.section-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #40C8FF;
    box-shadow: 0 0 10px rgba(64,200,255,0.6);
    flex-shrink: 0;
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #8B92AA;
}

/* Cards */
.glass-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.glass-card:hover { border-color: rgba(64,200,255,0.2); }
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(64,200,255,0.3), transparent);
}

/* Metric Cards */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 28px;
}
.metric-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 20px 18px;
    position: relative;
    overflow: hidden;
}
.metric-card.accent { border-color: rgba(64,200,255,0.25); background: rgba(64,200,255,0.05); }
.metric-card.accent2 { border-color: rgba(123,110,246,0.25); background: rgba(123,110,246,0.05); }
.metric-card.accent3 { border-color: rgba(255,107,107,0.25); background: rgba(255,107,107,0.05); }
.metric-card.accent4 { border-color: rgba(52,211,153,0.25); background: rgba(52,211,153,0.05); }
.metric-icon { font-size: 18px; margin-bottom: 8px; }
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 26px;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1;
}
.metric-label {
    font-size: 11px;
    color: #5A6178;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 6px;
}

/* Step Indicators */
.step-flow {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 32px;
    flex-wrap: wrap;
}
.step-chip {
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 100px;
    padding: 7px 14px;
    font-size: 12px;
    color: #5A6178;
    transition: all 0.3s;
}
.step-chip.active {
    background: rgba(64,200,255,0.1);
    border-color: rgba(64,200,255,0.4);
    color: #40C8FF;
}
.step-chip.done {
    background: rgba(52,211,153,0.08);
    border-color: rgba(52,211,153,0.3);
    color: #34D399;
}
.step-num {
    width: 18px; height: 18px;
    border-radius: 50%;
    background: rgba(255,255,255,0.1);
    display: flex; align-items: center; justify-content: center;
    font-size: 10px;
    font-family: 'DM Mono', monospace;
}
.step-chip.active .step-num { background: #40C8FF; color: #080B14; }
.step-chip.done .step-num { background: #34D399; color: #080B14; }
.step-arrow { color: #2A2F42; font-size: 14px; }

/* Log Terminal */
.terminal {
    background: #050810;
    border: 1px solid rgba(64,200,255,0.15);
    border-radius: 12px;
    padding: 20px;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    line-height: 1.8;
    max-height: 260px;
    overflow-y: auto;
    margin-bottom: 20px;
}
.terminal::-webkit-scrollbar { width: 4px; }
.terminal::-webkit-scrollbar-track { background: transparent; }
.terminal::-webkit-scrollbar-thumb { background: rgba(64,200,255,0.3); border-radius: 2px; }
.log-line { display: flex; align-items: flex-start; gap: 10px; }
.log-time { color: #2A3550; flex-shrink: 0; }
.log-ok { color: #34D399; }
.log-warn { color: #FBBF24; }
.log-info { color: #40C8FF; }
.log-text { color: #8B92AA; }

/* Column Quality Bars */
.col-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.col-name {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    color: #E8EBF4;
    width: 130px;
    flex-shrink: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.col-type {
    font-size: 10px;
    color: #40C8FF;
    background: rgba(64,200,255,0.1);
    border-radius: 4px;
    padding: 2px 7px;
    flex-shrink: 0;
    font-family: 'DM Mono', monospace;
}
.bar-wrap {
    flex: 1;
    height: 4px;
    background: rgba(255,255,255,0.06);
    border-radius: 2px;
    overflow: hidden;
}
.bar-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 0.6s ease;
}
.col-pct {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #5A6178;
    width: 36px;
    text-align: right;
    flex-shrink: 0;
}

/* AI Report Box */
.ai-report {
    background: linear-gradient(135deg, rgba(64,200,255,0.04) 0%, rgba(123,110,246,0.04) 100%);
    border: 1px solid rgba(64,200,255,0.15);
    border-radius: 16px;
    padding: 28px 32px;
    margin: 24px 0;
    position: relative;
}
.ai-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(64,200,255,0.12);
    border: 1px solid rgba(64,200,255,0.3);
    border-radius: 100px;
    padding: 4px 12px;
    font-size: 11px;
    font-family: 'DM Mono', monospace;
    color: #40C8FF;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 16px;
}
.ai-report p {
    font-size: 14px;
    line-height: 1.8;
    color: #A8B0C8;
    margin-bottom: 12px;
}

/* Download Strip */
.dl-strip {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 28px;
}
.dl-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 20px 22px;
    text-align: center;
    transition: all 0.3s;
    cursor: pointer;
}
.dl-card:hover { border-color: rgba(64,200,255,0.4); background: rgba(64,200,255,0.05); }
.dl-icon { font-size: 24px; margin-bottom: 8px; }
.dl-title {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 600;
    color: #FFFFFF;
}
.dl-desc { font-size: 11px; color: #5A6178; margin-top: 4px; }

/* Streamlit overrides */
.stTextInput > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 10px !important;
    color: #E8EBF4 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
}
.stTextInput > div > div:focus-within {
    border-color: rgba(64,200,255,0.5) !important;
    box-shadow: 0 0 0 3px rgba(64,200,255,0.08) !important;
}
.stFileUploader > div {
    background: rgba(255,255,255,0.02) !important;
    border: 2px dashed rgba(255,255,255,0.10) !important;
    border-radius: 14px !important;
}
.stButton > button {
    background: linear-gradient(135deg, #40C8FF, #7B6EF6) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #080B14 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    padding: 12px 28px !important;
    transition: opacity 0.2s !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #40C8FF, #7B6EF6) !important;
}
.stDataFrame { border-radius: 10px !important; overflow: hidden !important; }
.stAlert { border-radius: 10px !important; }
div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
}
label, .stSelectbox label, .stTextInput label {
    font-family: 'Syne', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    color: #5A6178 !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 10px !important;
    color: #E8EBF4 !important;
}
.stCheckbox > label { text-transform: none !important; letter-spacing: normal !important; }
h1,h2,h3 { font-family: 'Syne', sans-serif !important; }
.stMarkdown p { color: #8B92AA; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">* Google Gemini AI - v2.0 - Enterprise Grade - Built for Scale</div>
  <div class="hero-title"><span>Gemini</span> <span class="the">The</span> Data Analyzer</div>
  <div class="hero-sub">Enterprise-grade intelligent data cleaning powered by Google Gemini AI. Handles up to 10 lakh rows with chunked processing, real-time diagnostics, and structured PDF reports.</div>
  <div class="hero-stats">
    <div class="stat-item"><div class="stat-num">10L+</div><div class="stat-label">Max Rows</div></div>
    <div class="stat-item"><div class="stat-num">AI</div><div class="stat-label">Smart Report</div></div>
    <div class="stat-item"><div class="stat-num">PDF</div><div class="stat-label">Structured Export</div></div>
    <div class="stat-item"><div class="stat-num">INF</div><div class="stat-label">Column Types</div></div>
    <div class="stat-item"><div class="stat-num">RT</div><div class="stat-label">Real-time Logs</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
CHUNK_SIZE = 50_000  # rows per chunk

def get_col_type_label(series):
    if pd.api.types.is_numeric_dtype(series): return "NUM"
    if pd.api.types.is_datetime64_any_dtype(series): return "DATE"
    if pd.api.types.is_bool_dtype(series): return "BOOL"
    return "TXT"

def get_bar_color(pct):
    if pct >= 95: return "#34D399"
    if pct >= 80: return "#FBBF24"
    return "#F87171"

def sanitize_for_pdf(text):
    """Replace unicode chars not in Helvetica/Courier with ASCII equivalents."""
    replacements = {
        '\u2714': '(OK)', '\u2718': '(X)', '\u2022': '-', '\u25b8': '>',
        '\u25c8': '*', '\u25c9': '*', '\u2726': '*', '\u2605': '*',
        '\u2606': '*', '\u2713': 'OK', '\u26a0': '!', '\u2192': '->',
        '\u2190': '<-', '\u2193': 'v', '\u2191': '^', '\u00b7': '.',
        '\u2026': '...', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2013': '-', '\u2014': '--',
        '\u00a0': ' ',
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    # Remove any remaining non-latin1 characters
    return text.encode('latin-1', errors='replace').decode('latin-1')


def build_pdf_report(orig_shape, clean_shape, col_info, cleaning_steps, ai_summary, timestamp):
    """Build and return a PDF bytes object."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        rightMargin=2.2*cm, leftMargin=2.2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )

    # Palette
    DARK     = HexColor("#080B14")
    CARD     = HexColor("#0D1526")
    ACCENT   = HexColor("#40C8FF")
    PURPLE   = HexColor("#7B6EF6")
    GREEN    = HexColor("#34D399")
    YELLOW   = HexColor("#FBBF24")
    RED      = HexColor("#F87171")
    ORANGE   = HexColor("#F97316")
    TEXT     = HexColor("#E8EBF4")
    MUTED    = HexColor("#8B92AA")
    BORDER   = HexColor("#1E2535")
    WHITE    = colors.white

    # Styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("title_s", fontName="Helvetica-Bold",
        fontSize=28, textColor=WHITE, leading=34, spaceAfter=6)
    subtitle_style = ParagraphStyle("sub_s", fontName="Helvetica",
        fontSize=12, textColor=MUTED, leading=18, spaceAfter=4)
    h2_style = ParagraphStyle("h2_s", fontName="Helvetica-Bold",
        fontSize=14, textColor=WHITE, leading=20, spaceBefore=14, spaceAfter=8)
    h3_style = ParagraphStyle("h3_s", fontName="Helvetica-Bold",
        fontSize=11, textColor=ACCENT, leading=16, spaceBefore=8, spaceAfter=5)
    body_style = ParagraphStyle("body_s", fontName="Helvetica",
        fontSize=10, textColor=MUTED, leading=16, spaceAfter=4)
    mono_style = ParagraphStyle("mono_s", fontName="Courier",
        fontSize=9, textColor=TEXT, leading=14)
    badge_style = ParagraphStyle("badge_s", fontName="Helvetica-Bold",
        fontSize=8, textColor=ACCENT, leading=12)

    story = []

    # Cover
    cover_title_sty = ParagraphStyle("ct", fontName="Helvetica-Bold",
        fontSize=30, textColor=WHITE, leading=36, spaceAfter=6, spaceBefore=20)
    cover_sub_sty = ParagraphStyle("cs", fontName="Helvetica",
        fontSize=13, textColor=MUTED, leading=18, spaceAfter=16)
    story.append(Paragraph(sanitize_for_pdf("Gemini The Data Analyzer"), cover_title_sty))
    story.append(Paragraph(sanitize_for_pdf("AI-Powered Data Quality Report"), cover_sub_sty))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=20))

    # Meta row — NOTE: no ROUNDEDCORNERS, it's not a valid TableStyle command
    meta_rows = [
        ["Generated", timestamp],
        ["Original Rows", f"{orig_shape[0]:,}"],
        ["Original Columns", str(orig_shape[1])],
        ["Cleaned Rows", f"{clean_shape[0]:,}"],
        ["Rows Removed", f"{orig_shape[0]-clean_shape[0]:,}"],
    ]
    meta_style_tbl = ParagraphStyle("ms", fontName="Helvetica", fontSize=9, textColor=MUTED)
    meta_val_style = ParagraphStyle("mv", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE)

    meta_tbl_data = [[
        Paragraph(sanitize_for_pdf(r[0]), meta_style_tbl),
        Paragraph(sanitize_for_pdf(r[1]), meta_val_style)
    ] for r in meta_rows]

    meta_tbl = Table(meta_tbl_data, colWidths=[5*cm, 12*cm])
    meta_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), CARD),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [CARD, HexColor("#0A0E1A")]),
        ("LEFTPADDING", (0,0), (-1,-1), 14),
        ("RIGHTPADDING", (0,0), (-1,-1), 14),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("GRID", (0,0), (-1,-1), 0.5, BORDER),
        # FIX: Removed invalid "ROUNDEDCORNERS" command
    ]))
    story.append(meta_tbl)
    story.append(Spacer(1, 20))

    # Summary metrics strip
    rows_saved = orig_shape[0] - clean_shape[0]
    pct_clean = round(100 * clean_shape[0] / orig_shape[0], 1) if orig_shape[0] else 0
    n_steps = len(cleaning_steps)

    metric_style = ParagraphStyle("msty", fontName="Helvetica-Bold", fontSize=22, textColor=WHITE, leading=26)
    metric_lbl = ParagraphStyle("mlbl", fontName="Helvetica", fontSize=8, textColor=MUTED, leading=12)

    metrics_data = [[
        [Paragraph(f"{orig_shape[0]:,}", metric_style), Paragraph("ORIGINAL ROWS", metric_lbl)],
        [Paragraph(f"{rows_saved:,}", metric_style), Paragraph("ROWS REMOVED", metric_lbl)],
        [Paragraph(f"{pct_clean}%", metric_style), Paragraph("DATA RETAINED", metric_lbl)],
        [Paragraph(str(n_steps), metric_style), Paragraph("CLEANING OPS", metric_lbl)],
    ]]
    metrics_tbl = Table(metrics_data, colWidths=[4.25*cm]*4)
    metrics_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), HexColor("#091525")),
        ("BACKGROUND", (1,0), (1,0), HexColor("#120915")),
        ("BACKGROUND", (2,0), (2,0), HexColor("#091520")),
        ("BACKGROUND", (3,0), (3,0), HexColor("#0D1520")),
        ("BOX", (0,0), (0,0), 1, HexColor("#1E3550")),
        ("BOX", (1,0), (1,0), 1, HexColor("#2A1535")),
        ("BOX", (2,0), (2,0), 1, HexColor("#1A3530")),
        ("BOX", (3,0), (3,0), 1, HexColor("#1A2535")),
        ("LEFTPADDING", (0,0), (-1,-1), 16),
        ("RIGHTPADDING", (0,0), (-1,-1), 16),
        ("TOPPADDING", (0,0), (-1,-1), 16),
        ("BOTTOMPADDING", (0,0), (-1,-1), 16),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(metrics_tbl)
    story.append(Spacer(1, 24))

    # AI Summary — compact: one paragraph per section (first 3 sentences max)
    story.append(Paragraph("AI-Generated Analysis", h2_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=10))

    import re as _re

    _section_colors = [ACCENT, RED, YELLOW, PURPLE, GREEN, ORANGE, ACCENT]

    def _first_sentences(text, n=3):
        """Return first n sentences from a block of text, stripped of markdown."""
        text = _re.sub(r'\*\*(.*?)\*\*', r'\1', text)          # strip bold
        text = _re.sub(r'^[-*]\s+', '', text, flags=_re.MULTILINE)  # strip bullets
        text = _re.sub(r'^\d+\.\s+', '', text, flags=_re.MULTILINE) # strip numbered
        text = ' '.join(text.split())                            # collapse whitespace
        # Split on sentence-ending punctuation
        parts = _re.split(r'(?<=[.!?])\s+', text)
        return ' '.join(parts[:n])

    _ai_norm = _re.sub(r'^\s*##\s+', '##SPLIT##', ai_summary.strip(), flags=_re.MULTILINE)
    _raw_sections = _ai_norm.split('##SPLIT##')

    # Build a two-column compact table: [Section title | Summary paragraph]
    sec_label_sty = ParagraphStyle("secl", fontName="Helvetica-Bold", fontSize=8,
        textColor=ACCENT, leading=12, spaceAfter=0)
    sec_body_sty  = ParagraphStyle("secb", fontName="Helvetica", fontSize=8,
        textColor=MUTED, leading=12, spaceAfter=0)

    ai_tbl_rows = []
    _sec_idx = 0
    for _raw in _raw_sections:
        _raw = _raw.strip()
        if not _raw:
            continue
        _lines = _raw.split('\n', 1)
        _sec_title = _re.sub(r'^#+\s*', '', _lines[0]).strip()
        _sec_body  = _lines[1].strip() if len(_lines) > 1 else ""
        if not _sec_title:
            continue

        _col = _section_colors[_sec_idx % len(_section_colors)]
        _sec_idx += 1

        lbl_sty = ParagraphStyle(f"lbl{_sec_idx}", fontName="Helvetica-Bold",
            fontSize=8, textColor=_col, leading=12)
        summary = _first_sentences(_sec_body, 3)
        ai_tbl_rows.append([
            Paragraph(sanitize_for_pdf(_sec_title.upper()), lbl_sty),
            Paragraph(sanitize_for_pdf(summary), sec_body_sty),
        ])

    if ai_tbl_rows:
        ai_tbl = Table(ai_tbl_rows, colWidths=[4.5*cm, 12.7*cm])
        ai_tbl.setStyle(TableStyle([
            ("ROWBACKGROUNDS", (0,0), (-1,-1), [HexColor("#080B14"), HexColor("#0A0D18")]),
            ("GRID", (0,0), (-1,-1), 0.4, BORDER),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
            ("RIGHTPADDING", (0,0), (-1,-1), 8),
            ("TOPPADDING", (0,0), (-1,-1), 7),
            ("BOTTOMPADDING", (0,0), (-1,-1), 7),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
        ]))
        story.append(ai_tbl)

    story.append(Spacer(1, 14))

    # Cleaning Steps
    story.append(Paragraph("Cleaning Operations Log", h2_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=12))

    steps_header = [
        [Paragraph("#", badge_style), Paragraph("TYPE", badge_style), Paragraph("DESCRIPTION", badge_style)]
    ]
    steps_rows = []
    MAX_STEPS_SHOWN = 50
    steps_to_show = cleaning_steps[:MAX_STEPS_SHOWN]
    for i, (stype, sdesc) in enumerate(steps_to_show, 1):
        type_color = YELLOW if stype == "duplicate" else (ACCENT if "num" in stype else GREEN)
        type_sty = ParagraphStyle(f"ts{i}", fontName="Helvetica-Bold", fontSize=8, textColor=type_color)
        desc_sty = ParagraphStyle(f"ds{i}", fontName="Courier", fontSize=8, textColor=TEXT, leading=12)
        steps_rows.append([
            Paragraph(str(i), body_style),
            Paragraph(sanitize_for_pdf(stype.upper()), type_sty),
            Paragraph(sanitize_for_pdf(sdesc[:120]), desc_sty)
        ])
    if len(cleaning_steps) > MAX_STEPS_SHOWN:
        overflow_sty = ParagraphStyle("ov", fontName="Helvetica", fontSize=8, textColor=MUTED)
        steps_rows.append([
            Paragraph("...", body_style),
            Paragraph("MORE", overflow_sty),
            Paragraph(f"...and {len(cleaning_steps) - MAX_STEPS_SHOWN} more ops (see full log in app)", overflow_sty)
        ])

    if not steps_rows:
        steps_rows = [[
            Paragraph("-", body_style),
            Paragraph("NONE", body_style),
            Paragraph("No cleaning operations required.", body_style)
        ]]

    steps_tbl = Table(steps_header + steps_rows, colWidths=[1*cm, 3*cm, 13*cm])
    steps_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), HexColor("#0D1526")),
        ("TEXTCOLOR", (0,0), (-1,0), ACCENT),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [HexColor("#080B14"), HexColor("#0A0D18")]),
        ("GRID", (0,0), (-1,-1), 0.5, BORDER),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 8),
    ]))
    story.append(steps_tbl)
    story.append(Spacer(1, 22))

    # Column Quality Table
    story.append(PageBreak())
    story.append(Paragraph("Column Quality Breakdown", h2_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=12))

    col_header = [[
        Paragraph("COLUMN", badge_style),
        Paragraph("TYPE", badge_style),
        Paragraph("COMPLETENESS", badge_style),
        Paragraph("NULLS", badge_style),
        Paragraph("UNIQUE", badge_style),
        Paragraph("ACTION", badge_style),
    ]]
    col_rows = []
    for cinfo in col_info:
        pct = cinfo["completeness"]
        pct_color = GREEN if pct >= 95 else (YELLOW if pct >= 80 else RED)
        pct_sty = ParagraphStyle("ps", fontName="Helvetica-Bold", fontSize=9, textColor=pct_color)
        name_sty = ParagraphStyle("ns", fontName="Courier", fontSize=9, textColor=WHITE)
        type_sty = ParagraphStyle("ts", fontName="Courier", fontSize=8, textColor=ACCENT)

        col_rows.append([
            Paragraph(sanitize_for_pdf(cinfo["name"][:22]), name_sty),
            Paragraph(sanitize_for_pdf(cinfo["dtype"]), type_sty),
            Paragraph(f"{pct}%", pct_sty),
            Paragraph(str(cinfo["nulls"]), body_style),
            Paragraph(str(cinfo["unique"]), body_style),
            Paragraph(sanitize_for_pdf(cinfo["action"]), body_style),
        ])

    col_tbl = Table(col_header + col_rows, colWidths=[4.5*cm, 1.8*cm, 3*cm, 2*cm, 2*cm, 3.7*cm])
    col_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), HexColor("#0D1526")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [HexColor("#080B14"), HexColor("#0A0D18")]),
        ("GRID", (0,0), (-1,-1), 0.5, BORDER),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(col_tbl)
    story.append(Spacer(1, 24))

    # Footer
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=10))
    footer_sty = ParagraphStyle("fs", fontName="Helvetica", fontSize=8, textColor=HexColor("#2A3550"))
    story.append(Paragraph(
        sanitize_for_pdf(f"Gemini The Data Analyzer - Report generated {timestamp} - Powered by Google Gemini AI"),
        footer_sty
    ))

    doc.build(story)
    buf.seek(0)
    return buf.read()


# ─────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────
left_col, right_col = st.columns([1, 2], gap="large")

with left_col:
    st.markdown('<div style="height:28px"></div>', unsafe_allow_html=True)

    # API Key
    st.markdown("""
    <div class="section-header">
      <div class="section-dot"></div>
      <div class="section-title">Gemini API Key</div>
    </div>
    """, unsafe_allow_html=True)

    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="AIza...................",
        label_visibility="collapsed"
    )

    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("models/gemini-2.5-flash")
            st.markdown("""
            <div style="display:flex;align-items:center;gap:8px;margin:8px 0 20px;
              background:rgba(52,211,153,0.08);border:1px solid rgba(52,211,153,0.25);
              border-radius:8px;padding:8px 14px;font-size:12px;color:#34D399;
              font-family:'DM Mono',monospace;">
              OK - API key verified
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Invalid key: {e}")
            st.stop()
    else:
        st.markdown("""
        <div style="font-size:11px;color:#5A6178;margin-top:6px;line-height:1.6;">
          Get your free key at<br>
          <a href="https://aistudio.google.com/app/apikey" style="color:#40C8FF;">
          aistudio.google.com</a>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # File Upload
    st.markdown("""
    <div class="section-header">
      <div class="section-dot" style="background:#7B6EF6;box-shadow:0 0 10px rgba(123,110,246,0.6)"></div>
      <div class="section-title">Upload Dataset</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel",
        type=["csv", "xlsx"],
        label_visibility="collapsed"
    )

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Options
    st.markdown("""
    <div class="section-header">
      <div class="section-dot" style="background:#FBBF24;box-shadow:0 0 10px rgba(251,191,36,0.5)"></div>
      <div class="section-title">Cleaning Options</div>
    </div>
    """, unsafe_allow_html=True)

    opt_remove_dup  = st.checkbox("Remove duplicates", value=True)
    opt_fill_nulls  = st.checkbox("Fill missing values", value=True)
    opt_strip_ws    = st.checkbox("Strip whitespace (text cols)", value=True)
    opt_lower_case  = st.checkbox("Normalise text case", value=False)
    null_strategy   = st.selectbox(
        "Null-fill strategy (numeric)",
        ["Mean", "Median", "Zero"],
        index=0
    )

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    run_btn = st.button("Run Cleaning Pipeline", use_container_width=True)

# ─────────────────────────────────────────────
# RIGHT PANEL
# ─────────────────────────────────────────────
with right_col:
    if not uploaded_file:
        st.markdown("""
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
          height:480px;text-align:center;opacity:0.4;">
          <div style="font-size:64px;margin-bottom:20px;">&#128194;</div>
          <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:700;color:#E8EBF4;">
            Drop a dataset to begin
          </div>
          <div style="font-size:13px;color:#5A6178;margin-top:8px;">
            CSV or Excel - up to 10 lakh rows supported
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Load preview
        try:
            if uploaded_file.name.endswith(".csv"):
                df_preview = pd.read_csv(uploaded_file, nrows=5)
                uploaded_file.seek(0)
                df_full_shape = pd.read_csv(uploaded_file, usecols=[0]).shape
                uploaded_file.seek(0)
            else:
                df_preview = pd.read_excel(uploaded_file, nrows=5)
                uploaded_file.seek(0)
                df_full_shape = pd.read_excel(uploaded_file, usecols=[0]).shape
                uploaded_file.seek(0)
        except Exception as e:
            st.error(f"Could not read file: {e}")
            st.stop()

        # Step flow
        st.markdown(f"""
        <div class="step-flow">
          <div class="step-chip done"><div class="step-num">1</div>Upload</div>
          <div class="step-arrow">-&gt;</div>
          <div class="step-chip {'done' if run_btn else 'active'}"><div class="step-num">2</div>Analyse</div>
          <div class="step-arrow">-&gt;</div>
          <div class="step-chip {'active' if run_btn else ''}"><div class="step-num">3</div>Clean</div>
          <div class="step-arrow">-&gt;</div>
          <div class="step-chip {'active' if run_btn else ''}"><div class="step-num">4</div>Report</div>
          <div class="step-arrow">-&gt;</div>
          <div class="step-chip"><div class="step-num">5</div>Export</div>
        </div>
        """, unsafe_allow_html=True)

        # Preview
        st.markdown("""
        <div class="section-header" style="margin-top:8px">
          <div class="section-dot"></div>
          <div class="section-title">Dataset Preview</div>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(df_preview, use_container_width=True, height=200)

        if run_btn:
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

            # Full load
            with st.spinner("Loading full dataset..."):
                uploaded_file.seek(0)
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

            orig_shape = df.shape

            # Diagnostics
            st.markdown("""
            <div class="section-header">
              <div class="section-dot" style="background:#FBBF24;box-shadow:0 0 10px rgba(251,191,36,0.5)"></div>
              <div class="section-title">Pre-Clean Diagnostics</div>
            </div>
            """, unsafe_allow_html=True)

            null_total = int(df.isnull().sum().sum())
            dup_total  = int(df.duplicated().sum())
            completeness = round(100 * (1 - null_total / max(df.size, 1)), 1)

            col1m, col2m, col3m, col4m = st.columns(4)
            with col1m:
                st.markdown(f"""
                <div class="metric-card accent">
                  <div class="metric-icon">&#128202;</div>
                  <div class="metric-value">{orig_shape[0]:,}</div>
                  <div class="metric-label">Total Rows</div>
                </div>""", unsafe_allow_html=True)
            with col2m:
                st.markdown(f"""
                <div class="metric-card accent2">
                  <div class="metric-icon">&#128203;</div>
                  <div class="metric-value">{orig_shape[1]}</div>
                  <div class="metric-label">Columns</div>
                </div>""", unsafe_allow_html=True)
            with col3m:
                st.markdown(f"""
                <div class="metric-card accent3">
                  <div class="metric-icon">&#128368;</div>
                  <div class="metric-value">{null_total:,}</div>
                  <div class="metric-label">Missing Values</div>
                </div>""", unsafe_allow_html=True)
            with col4m:
                st.markdown(f"""
                <div class="metric-card accent4">
                  <div class="metric-icon">&#128260;</div>
                  <div class="metric-value">{dup_total:,}</div>
                  <div class="metric-label">Duplicates</div>
                </div>""", unsafe_allow_html=True)

            # Column quality bars
            st.markdown("""
            <div class="section-header" style="margin-top:8px">
              <div class="section-dot" style="background:#7B6EF6;box-shadow:0 0 10px rgba(123,110,246,0.6)"></div>
              <div class="section-title">Column Completeness</div>
            </div>
            """, unsafe_allow_html=True)

            bars_html = ""
            col_info_list = []
            for col in df.columns:
                nulls = int(df[col].isnull().sum())
                pct = round(100 * (1 - nulls / len(df)), 1) if len(df) else 100
                bar_color = get_bar_color(pct)
                dtype_lbl = get_col_type_label(df[col])
                unique = int(df[col].nunique())
                action = ("Fill mean" if dtype_lbl=="NUM" else ("Fill mode" if nulls>0 else "-")) if nulls else "-"
                col_info_list.append({
                    "name": col, "dtype": dtype_lbl, "nulls": nulls,
                    "unique": unique, "completeness": pct, "action": action
                })
                bars_html += f"""
                <div class="col-row">
                  <div class="col-name" title="{col}">{col}</div>
                  <div class="col-type">{dtype_lbl}</div>
                  <div class="bar-wrap"><div class="bar-fill" style="width:{pct}%;background:{bar_color}"></div></div>
                  <div class="col-pct">{pct}%</div>
                </div>"""

            st.markdown(f'<div class="glass-card" style="max-height:300px;overflow-y:auto">{bars_html}</div>',
                        unsafe_allow_html=True)

            # CHUNKED CLEANING
            st.markdown("""
            <div class="section-header" style="margin-top:8px">
              <div class="section-dot" style="background:#34D399;box-shadow:0 0 10px rgba(52,211,153,0.6)"></div>
              <div class="section-title">Cleaning Pipeline</div>
            </div>
            """, unsafe_allow_html=True)

            n_chunks = math.ceil(len(df) / CHUNK_SIZE)
            all_steps = []
            cleaned_chunks = []
            log_lines = []

            progress_bar = st.progress(0)
            status_text  = st.empty()

            t0 = time.time()
            for ci in range(n_chunks):
                chunk = df.iloc[ci*CHUNK_SIZE : (ci+1)*CHUNK_SIZE].copy()
                status_text.markdown(f"<span style='font-family:DM Mono,monospace;font-size:12px;color:#40C8FF'>Processing chunk {ci+1}/{n_chunks} - rows {ci*CHUNK_SIZE+1:,}-{min((ci+1)*CHUNK_SIZE, len(df)):,}</span>", unsafe_allow_html=True)

                if opt_strip_ws:
                    for col in chunk.select_dtypes(include="object").columns:
                        chunk[col] = chunk[col].str.strip()

                if opt_lower_case:
                    for col in chunk.select_dtypes(include="object").columns:
                        chunk[col] = chunk[col].str.lower()

                if opt_remove_dup:
                    dup = chunk.duplicated().sum()
                    if dup:
                        chunk.drop_duplicates(inplace=True)
                        all_steps.append(("duplicate", f"Chunk {ci+1}: Removed {dup} duplicate rows"))
                        log_lines.append(f'<div class="log-line"><span class="log-time">{time.strftime("%H:%M:%S")}</span><span class="log-warn">WARN</span><span class="log-text">Chunk {ci+1}: removed {dup} duplicates</span></div>')

                if opt_fill_nulls:
                    for col in chunk.columns:
                        null_cnt = chunk[col].isnull().sum()
                        if null_cnt == 0:
                            continue
                        if pd.api.types.is_numeric_dtype(chunk[col]):
                            if null_strategy == "Mean":
                                val = chunk[col].mean()
                            elif null_strategy == "Median":
                                val = chunk[col].median()
                            else:
                                val = 0
                            chunk[col].fillna(val, inplace=True)
                            all_steps.append(("null_num", f"Chunk {ci+1} - '{col}': filled {null_cnt} nulls -> {null_strategy.lower()} {val:.3g}"))
                        else:
                            mode_s = chunk[col].mode()
                            val = mode_s[0] if len(mode_s) else "Unknown"
                            chunk[col].fillna(val, inplace=True)
                            all_steps.append(("null_txt", f"Chunk {ci+1} - '{col}': filled {null_cnt} nulls -> mode '{val}'"))
                        log_lines.append(f'<div class="log-line"><span class="log-time">{time.strftime("%H:%M:%S")}</span><span class="log-ok">FIX</span><span class="log-text">Chunk {ci+1} - {col}: {null_cnt} nulls filled</span></div>')

                cleaned_chunks.append(chunk)
                progress_bar.progress((ci + 1) / n_chunks)

            elapsed = round(time.time() - t0, 2)
            cleaned_df = pd.concat(cleaned_chunks, ignore_index=True)
            clean_shape = cleaned_df.shape
            status_text.markdown(f"<span style='font-family:DM Mono,monospace;font-size:12px;color:#34D399'>Done - {len(df):,} rows processed in {elapsed}s</span>", unsafe_allow_html=True)

            # Log terminal
            log_html = "\n".join(log_lines) if log_lines else '<div class="log-line"><span class="log-ok">OK</span><span class="log-text">No issues found - dataset is already clean!</span></div>'
            st.markdown(f'<div class="terminal">{log_html}</div>', unsafe_allow_html=True)

            # Post-clean metrics
            rows_removed = orig_shape[0] - clean_shape[0]
            pct_retained = round(100 * clean_shape[0] / orig_shape[0], 1)
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(f"""<div class="metric-card accent4"><div class="metric-icon">&#9989;</div>
                <div class="metric-value">{clean_shape[0]:,}</div><div class="metric-label">Clean Rows</div></div>""",
                unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class="metric-card accent3"><div class="metric-icon">&#128465;</div>
                <div class="metric-value">{rows_removed:,}</div><div class="metric-label">Rows Removed</div></div>""",
                unsafe_allow_html=True)
            with c3:
                st.markdown(f"""<div class="metric-card accent"><div class="metric-icon">&#128175;</div>
                <div class="metric-value">{pct_retained}%</div><div class="metric-label">Retained</div></div>""",
                unsafe_allow_html=True)
            with c4:
                st.markdown(f"""<div class="metric-card accent2"><div class="metric-icon">&#9889;</div>
                <div class="metric-value">{elapsed}s</div><div class="metric-label">Process Time</div></div>""",
                unsafe_allow_html=True)

            # AI Report
            st.markdown("""
            <div class="section-header" style="margin-top:20px">
              <div class="section-dot" style="background:#7B6EF6;box-shadow:0 0 10px rgba(123,110,246,0.6)"></div>
              <div class="section-title">AI Intelligence Report</div>
            </div>
            """, unsafe_allow_html=True)

            steps_text = "\n".join(f"- [{s[0]}] {s[1]}" for s in all_steps) if all_steps else "No cleaning steps were required."
            prompt = f"""You are a senior data scientist and analyst. Analyze this data cleaning operation and return a DETAILED structured report.

IMPORTANT FORMATTING RULES:
- Use ONLY plain markdown. Do NOT output HTML tags, <div>, <span>, or any HTML whatsoever.
- Use ## for each section heading (exactly two hash symbols).
- Use plain text, bullet points with "- ", and numbered lists with "1. ".
- Bold important words with **double asterisks**.

Use EXACTLY these section headers:

## Dataset Overview
Describe the original dataset size, shape, column count, and what kind of data this likely represents based on the stats.

## Issues Detected
List and explain every data quality issue found: total missing values, which columns had nulls, duplicate rows found, data type inconsistencies, and severity assessment of each issue.

## Cleaning Actions Performed
Explain in detail every cleaning action taken - which columns were fixed, what strategy was used (mean/mode/dedup), how many values were impacted, and why that strategy is appropriate for that column type.

## Data Quality Score
Give an overall data quality score out of 100 before and after cleaning. Break it down into sub-scores: Completeness, Consistency, Uniqueness, and Validity. Explain each score.

## Statistical Impact
Describe the statistical impact of the cleaning: rows retained ({pct_retained}%), rows removed ({rows_removed:,}), processing efficiency ({elapsed}s for {orig_shape[0]:,} rows), and what percentage of cells were affected.

## Recommendations
Give 4-6 specific, actionable recommendations for improving this dataset further.

## Conclusion
Summarize the overall health of the dataset post-cleaning and whether it is ready for analysis or modeling.

--- DATA STATS ---
Original: {orig_shape[0]:,} rows x {orig_shape[1]} columns
After cleaning: {clean_shape[0]:,} rows x {clean_shape[1]} columns
Rows removed: {rows_removed:,} ({100-pct_retained:.1f}%)
Processing time: {elapsed}s
Total missing values fixed: {null_total:,}
Duplicate rows removed: {dup_total:,}
Columns: {list(df.columns[:20])}

Operations log:
{steps_text}

Be thorough and specific. Use real numbers from the stats above. Each section should have at least 3-5 sentences of meaningful insight. Output ONLY markdown, no HTML."""

            with st.spinner("Gemini is writing your detailed report..."):
                try:
                    response = model.generate_content(prompt)
                    ai_text = response.text
                except Exception as e:
                    ai_text = f"## Automated Report\n\n{steps_text}"

            # ── Normalise Gemini output → clean markdown ──────────────────────
            import re, html as _html

            def _gemini_to_markdown(raw):
                """Robustly convert any Gemini output (markdown OR html) to plain markdown."""
                t = str(raw or "")
                # Strip fenced code wrappers Gemini sometimes adds around the whole reply
                t = re.sub(r"^```[a-z]*\n?", "", t.strip(), flags=re.IGNORECASE)
                t = re.sub(r"\n?```$", "", t.strip())
                # If it looks like HTML, convert to plain text + markdown
                if re.search(r"(?i)<(div|span|p|h[1-6]|ul|ol|li|section)\b", t):
                    # Recover bold/strong first
                    t = re.sub(r"(?i)<(?:strong|b)[^>]*>(.*?)</(?:strong|b)>", r"**\1**", t, flags=re.DOTALL)
                    # Recover real h1-h3 tags as ## headings
                    t = re.sub(r"(?i)<h[1-3][^>]*>(.*?)</h[1-3]>", r"\n## \1\n", t, flags=re.DOTALL)
                    # Detect Gemini's section-title pattern: a span whose text matches a known heading
                    # e.g. <span ...>Dataset Overview</span> inside a header div
                    known_headings = [
                        "Dataset Overview", "Issues Detected", "Cleaning Actions Performed",
                        "Data Quality Score", "Statistical Impact", "Recommendations", "Conclusion"
                    ]
                    for heading in known_headings:
                        # Match span containing the heading text (possibly with surrounding whitespace)
                        t = re.sub(
                            r'<span[^>]*>\s*' + re.escape(heading) + r'\s*</span>',
                            f'\n## {heading}\n',
                            t, flags=re.IGNORECASE
                        )
                    # Turn <li> into bullet points
                    t = re.sub(r"(?i)<li[^>]*>(.*?)</li>", r"\n- \1", t, flags=re.DOTALL)
                    # Block-level tags → newlines
                    t = re.sub(r"(?i)<br\s*/?>", "\n", t)
                    t = re.sub(r"(?i)</(div|p|h[1-6]|section|article|ul|ol)>", "\n", t)
                    # Strip all remaining tags
                    t = re.sub(r"<[^>]+>", "", t)
                    t = _html.unescape(t)
                    # Remove lines that are just emoji or whitespace (leftover icon spans)
                    t = re.sub(r"^\s*[\U0001F000-\U0001FFFF\u2600-\u27BF]+\s*$", "", t, flags=re.MULTILINE)
                    # Convert any stray unicode bullets/arrows to "- " list items
                    t = re.sub(r"^\s*[▸►▶•·‣⁃]\s*", "- ", t, flags=re.MULTILINE)
                # Collapse excess blank lines
                t = re.sub(r"\n{3,}", "\n\n", t)
                return t.strip()

            ai_text_clean = _gemini_to_markdown(ai_text)

            # ── Split into sections on ## headings ────────────────────────────
            ai_text_norm = re.sub(r'^\s*##\s+', '##SPLIT##', ai_text_clean, flags=re.MULTILINE)
            raw_sections = ai_text_norm.split('##SPLIT##')

            rendered_sections = ""
            section_icons = {
                "Dataset Overview": "&#128202;",
                "Issues Detected": "&#128269;",
                "Cleaning Actions Performed": "&#129529;",
                "Data Quality Score": "&#128202;",
                "Statistical Impact": "&#128200;",
                "Recommendations": "&#128161;",
                "Conclusion": "&#9989;",
            }
            section_colors = {
                "Dataset Overview": "#40C8FF",
                "Issues Detected": "#F87171",
                "Cleaning Actions Performed": "#FBBF24",
                "Data Quality Score": "#7B6EF6",
                "Statistical Impact": "#34D399",
                "Recommendations": "#F97316",
                "Conclusion": "#40C8FF",
            }

            def _safe(text):
                """HTML-escape plain text for safe insertion into HTML attributes/content."""
                return _html.escape(str(text), quote=False)

            def _render_bold(text):
                """Convert **bold** markdown to <strong> tags (after escaping)."""
                escaped = _safe(text)
                return re.sub(r'\*\*(.*?)\*\*', r'<strong style="color:#E8EBF4;">\1</strong>', escaped)

            for s in raw_sections:
                s = s.strip()
                if not s:
                    continue
                lines = s.split('\n', 1)
                title = re.sub(r'^#+\s*', '', lines[0]).strip()
                body  = lines[1].strip() if len(lines) > 1 else ""
                if not title:
                    continue
                icon  = section_icons.get(title, "&#10022;")
                color = section_colors.get(title, "#40C8FF")

                body_html = ""
                for line in body.split('\n'):
                    line = line.strip()
                    if not line or line == "---":
                        continue
                    if line.startswith('- ') or line.startswith('* '):
                        body_html += (
                            f'<div style="display:flex;gap:10px;margin:6px 0;">'
                            f'<span style="color:{color};flex-shrink:0;margin-top:3px;font-size:11px;">&#9656;</span>'
                            f'<span style="color:#A8B0C8;font-size:13.5px;line-height:1.7;">{_render_bold(line[2:])}</span>'
                            f'</div>'
                        )
                    elif re.match(r'^\d+\.', line):
                        num, rest = line.split('.', 1)
                        body_html += (
                            f'<div style="display:flex;gap:10px;margin:8px 0;">'
                            f'<span style="color:{color};font-family:DM Mono,monospace;font-size:11px;font-weight:700;flex-shrink:0;width:22px;padding-top:2px;">{_safe(num)}.</span>'
                            f'<span style="color:#A8B0C8;font-size:13.5px;line-height:1.7;">{_render_bold(rest.strip())}</span>'
                            f'</div>'
                        )
                    else:
                        body_html += f'<p style="color:#A8B0C8;font-size:13.5px;line-height:1.8;margin:8px 0;">{_render_bold(line)}</p>'

                rendered_sections += (
                    f'<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);'
                    f'border-left:3px solid {color};border-radius:12px;padding:20px 24px;margin-bottom:16px;">'
                    f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">'
                    f'<span style="font-size:18px;">{icon}</span>'
                    f'<span style="font-family:\'Syne\',sans-serif;font-size:13px;font-weight:700;'
                    f'text-transform:uppercase;letter-spacing:0.08em;color:{color};">{_safe(title)}</span>'
                    f'</div><div>{body_html}</div></div>'
                )

            st.markdown(
                f'<div class="ai-report">'
                f'<div class="ai-badge">* Gemini AI - Detailed Analysis Report - {datetime.datetime.now().strftime("%H:%M:%S")}</div>'
                f'{rendered_sections}'
                f'</div>',
                unsafe_allow_html=True
            )

            # Pass clean markdown (not HTML) to PDF builder
            ai_text = ai_text_clean

            # Preview cleaned
            with st.expander("Preview Cleaned Dataset (first 20 rows)"):
                st.dataframe(cleaned_df.head(20), use_container_width=True)

            # Generate PDF
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                pdf_bytes = build_pdf_report(
                    orig_shape, clean_shape, col_info_list,
                    all_steps, ai_text, timestamp
                )
                pdf_ok = True
            except Exception as e:
                st.error(f"PDF generation error: {e}")
                pdf_ok = False

            # CSV export
            csv_buf = io.StringIO()
            cleaned_df.to_csv(csv_buf, index=False)
            csv_bytes = csv_buf.getvalue().encode()

            # Download buttons
            st.markdown("""
            <div class="section-header" style="margin-top:24px">
              <div class="section-dot" style="background:#40C8FF;box-shadow:0 0 10px rgba(64,200,255,0.6)"></div>
              <div class="section-title">Export Results</div>
            </div>
            """, unsafe_allow_html=True)

            dl1, dl2 = st.columns(2)
            with dl1:
                st.download_button(
                    label="Download Cleaned CSV",
                    data=csv_bytes,
                    file_name=f"datapulse_cleaned_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with dl2:
                if pdf_ok:
                    st.download_button(
                        label="Download PDF Report",
                        data=pdf_bytes,
                        file_name=f"datapulse_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

# Footer
st.markdown("""
<div style="text-align:center;padding:32px 0 20px;
  border-top:1px solid rgba(255,255,255,0.05);margin-top:40px">
  <span style="font-family:'DM Mono',monospace;font-size:11px;color:#2A3550;">
    * Gemini The Data Analyzer - Powered by Google Gemini AI - Built for Scale
  </span>
</div>
""", unsafe_allow_html=True)
