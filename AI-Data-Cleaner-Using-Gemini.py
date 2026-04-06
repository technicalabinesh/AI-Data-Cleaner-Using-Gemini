# -*- coding: utf-8 -*-
"""AI Data Cleaner - Premium Edition with PDF Reports, Large Dataset Support & Dataset Chatbot"""

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
    gap: 14px;
    margin-top: 40px;
    justify-content: center;
    flex-wrap: wrap;
}
.stat-item {
    text-align: center;
    min-width: 132px;
    padding: 12px 14px;
    border-radius: 12px;
    border: 1px solid rgba(64,200,255,0.14);
    background: rgba(255,255,255,0.02);
}
.stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 25px;
    font-weight: 700;
    color: #40C8FF;
    line-height: 1.1;
}
.stat-label {
    font-size: 11px;
    color: #8B92AA;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 6px;
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

/* ── CHATBOT STYLES ─────────────────────────────── */
.chat-container {
    background: linear-gradient(160deg, #080B14 0%, #0A0F1E 100%);
    border: 1px solid rgba(64,200,255,0.18);
    border-radius: 20px;
    overflow: hidden;
    margin-top: 32px;
    position: relative;
}
.chat-container::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #40C8FF, #7B6EF6, #F87171);
}
.chat-header {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 20px 28px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    background: rgba(255,255,255,0.02);
}
.chat-avatar {
    width: 40px; height: 40px;
    border-radius: 12px;
    background: linear-gradient(135deg, #40C8FF, #7B6EF6);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}
.chat-header-info {}
.chat-header-name {
    font-family: 'Syne', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: #FFFFFF;
}
.chat-header-status {
    display: flex;
    align-items: center;
    gap: 6px;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #34D399;
    margin-top: 2px;
}
.chat-status-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #34D399;
    box-shadow: 0 0 6px rgba(52,211,153,0.6);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}
.chat-body {
    padding: 20px 24px;
    max-height: 520px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 16px;
}
.chat-body::-webkit-scrollbar { width: 4px; }
.chat-body::-webkit-scrollbar-track { background: transparent; }
.chat-body::-webkit-scrollbar-thumb { background: rgba(64,200,255,0.25); border-radius: 2px; }
.msg-row {
    display: flex;
    gap: 10px;
    align-items: flex-start;
}
.msg-row.user { flex-direction: row-reverse; }
.msg-avatar-sm {
    width: 30px; height: 30px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px;
    flex-shrink: 0;
}
.msg-avatar-ai {
    background: linear-gradient(135deg, rgba(64,200,255,0.2), rgba(123,110,246,0.2));
    border: 1px solid rgba(64,200,255,0.3);
}
.msg-avatar-user {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
}
.msg-bubble {
    max-width: 78%;
    padding: 12px 16px;
    border-radius: 14px;
    font-size: 13.5px;
    line-height: 1.7;
}
.msg-bubble.ai {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-top-left-radius: 4px;
    color: #C8D0E4;
}
.msg-bubble.user {
    background: linear-gradient(135deg, rgba(64,200,255,0.12), rgba(123,110,246,0.12));
    border: 1px solid rgba(64,200,255,0.2);
    border-top-right-radius: 4px;
    color: #E8EBF4;
}
.msg-time {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    color: #2A3550;
    margin-top: 5px;
    padding: 0 4px;
}
.msg-row.user .msg-time { text-align: right; }
.chat-suggestions {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding: 0 24px 16px;
}
.suggestion-chip {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(64,200,255,0.2);
    border-radius: 100px;
    padding: 6px 14px;
    font-size: 11px;
    font-family: 'DM Mono', monospace;
    color: #40C8FF;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
}
.suggestion-chip:hover {
    background: rgba(64,200,255,0.1);
    border-color: rgba(64,200,255,0.5);
}
.chat-welcome {
    text-align: center;
    padding: 40px 20px;
    opacity: 0.7;
}
.chat-welcome-icon { font-size: 48px; margin-bottom: 12px; }
.chat-welcome-title {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #E8EBF4;
    margin-bottom: 8px;
}
.chat-welcome-sub { font-size: 13px; color: #5A6178; line-height: 1.6; }
/* ─────────────────────────────────────────────── */

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
  <div class="hero-sub">Enterprise-grade intelligent data cleaning powered by Google Gemini AI. Handles up to 10 lakh rows with chunked processing, real-time diagnostics, structured PDF reports, and an AI chatbot for your dataset.</div>
  <div class="hero-stats">
        <div class="stat-item"><div class="stat-num">10L+</div><div class="stat-label">Rows Supported</div></div>
        <div class="stat-item"><div class="stat-num">AI</div><div class="stat-label">Insight Report</div></div>
        <div class="stat-item"><div class="stat-num">PDF</div><div class="stat-label">Structured Export</div></div>
        <div class="stat-item"><div class="stat-num">INF</div><div class="stat-label">Type Inference</div></div>
        <div class="stat-item"><div class="stat-num">BOT</div><div class="stat-label">Dataset Chatbot</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
CHUNK_SIZE = 50_000

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
    return text.encode('latin-1', errors='replace').decode('latin-1')


def build_dataset_context(df, max_rows=30):
    """Build a rich context string about the dataset for the chatbot."""
    ctx = []
    ctx.append(f"DATASET SHAPE: {df.shape[0]:,} rows x {df.shape[1]} columns")
    ctx.append(f"COLUMNS: {list(df.columns)}")
    ctx.append("")
    ctx.append("COLUMN DETAILS:")
    for col in df.columns:
        dtype = get_col_type_label(df[col])
        nulls = int(df[col].isnull().sum())
        unique = int(df[col].nunique())
        pct_null = round(100 * nulls / len(df), 1) if len(df) else 0
        if dtype == "NUM":
            try:
                stats = f"min={df[col].min():.3g}, max={df[col].max():.3g}, mean={df[col].mean():.3g}, std={df[col].std():.3g}"
            except:
                stats = "N/A"
            ctx.append(f"  - {col} [{dtype}]: {unique} unique, {nulls} nulls ({pct_null}%), {stats}")
        else:
            try:
                top_vals = df[col].value_counts().head(5).to_dict()
                top_str = str({str(k): v for k, v in list(top_vals.items())[:3]})
            except:
                top_str = "N/A"
            ctx.append(f"  - {col} [{dtype}]: {unique} unique, {nulls} nulls ({pct_null}%), top values: {top_str}")
    ctx.append("")
    ctx.append("SAMPLE DATA (first 10 rows):")
    ctx.append(df.head(10).to_string())
    ctx.append("")
    ctx.append("DESCRIPTIVE STATISTICS:")
    try:
        ctx.append(df.describe(include='all').to_string())
    except:
        ctx.append("N/A")
    return "\n".join(ctx)


def build_pdf_report(orig_shape, clean_shape, col_info, cleaning_steps, ai_summary, timestamp):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        rightMargin=2.2*cm, leftMargin=2.2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )
    DARK=HexColor("#080B14"); CARD=HexColor("#0D1526"); ACCENT=HexColor("#40C8FF")
    PURPLE=HexColor("#7B6EF6"); GREEN=HexColor("#34D399"); YELLOW=HexColor("#FBBF24")
    RED=HexColor("#F87171"); ORANGE=HexColor("#F97316"); TEXT=HexColor("#E8EBF4")
    MUTED=HexColor("#8B92AA"); BORDER=HexColor("#1E2535"); WHITE=colors.white

    styles = getSampleStyleSheet()
    title_style=ParagraphStyle("title_s",fontName="Helvetica-Bold",fontSize=28,textColor=WHITE,leading=34,spaceAfter=6)
    subtitle_style=ParagraphStyle("sub_s",fontName="Helvetica",fontSize=12,textColor=MUTED,leading=18,spaceAfter=4)
    h2_style=ParagraphStyle("h2_s",fontName="Helvetica-Bold",fontSize=14,textColor=WHITE,leading=20,spaceBefore=14,spaceAfter=8)
    h3_style=ParagraphStyle("h3_s",fontName="Helvetica-Bold",fontSize=11,textColor=ACCENT,leading=16,spaceBefore=8,spaceAfter=5)
    body_style=ParagraphStyle("body_s",fontName="Helvetica",fontSize=10,textColor=MUTED,leading=16,spaceAfter=4)
    mono_style=ParagraphStyle("mono_s",fontName="Courier",fontSize=9,textColor=TEXT,leading=14)
    badge_style=ParagraphStyle("badge_s",fontName="Helvetica-Bold",fontSize=8,textColor=ACCENT,leading=12)

    story = []
    cover_title_sty=ParagraphStyle("ct",fontName="Helvetica-Bold",fontSize=30,textColor=WHITE,leading=36,spaceAfter=6,spaceBefore=20)
    cover_sub_sty=ParagraphStyle("cs",fontName="Helvetica",fontSize=13,textColor=MUTED,leading=18,spaceAfter=16)
    story.append(Paragraph(sanitize_for_pdf("Gemini The Data Analyzer"), cover_title_sty))
    story.append(Paragraph(sanitize_for_pdf("AI-Powered Data Quality Report"), cover_sub_sty))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=20))

    meta_rows=[
        ["Generated",timestamp],["Original Rows",f"{orig_shape[0]:,}"],
        ["Original Columns",str(orig_shape[1])],["Cleaned Rows",f"{clean_shape[0]:,}"],
        ["Rows Removed",f"{orig_shape[0]-clean_shape[0]:,}"],
    ]
    meta_style_tbl=ParagraphStyle("ms",fontName="Helvetica",fontSize=9,textColor=MUTED)
    meta_val_style=ParagraphStyle("mv",fontName="Helvetica-Bold",fontSize=9,textColor=WHITE)
    meta_tbl_data=[[Paragraph(sanitize_for_pdf(r[0]),meta_style_tbl),Paragraph(sanitize_for_pdf(r[1]),meta_val_style)] for r in meta_rows]
    meta_tbl=Table(meta_tbl_data,colWidths=[5*cm,12*cm])
    meta_tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),CARD),("ROWBACKGROUNDS",(0,0),(-1,-1),[CARD,HexColor("#0A0E1A")]),
        ("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),
        ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("GRID",(0,0),(-1,-1),0.5,BORDER),
    ]))
    story.append(meta_tbl)
    story.append(Spacer(1, 20))

    rows_saved=orig_shape[0]-clean_shape[0]
    pct_clean=round(100*clean_shape[0]/orig_shape[0],1) if orig_shape[0] else 0
    n_steps=len(cleaning_steps)
    metric_style=ParagraphStyle("msty",fontName="Helvetica-Bold",fontSize=22,textColor=WHITE,leading=26)
    metric_lbl=ParagraphStyle("mlbl",fontName="Helvetica",fontSize=8,textColor=MUTED,leading=12)
    metrics_data=[[
        [Paragraph(f"{orig_shape[0]:,}",metric_style),Paragraph("ORIGINAL ROWS",metric_lbl)],
        [Paragraph(f"{rows_saved:,}",metric_style),Paragraph("ROWS REMOVED",metric_lbl)],
        [Paragraph(f"{pct_clean}%",metric_style),Paragraph("DATA RETAINED",metric_lbl)],
        [Paragraph(str(n_steps),metric_style),Paragraph("CLEANING OPS",metric_lbl)],
    ]]
    metrics_tbl=Table(metrics_data,colWidths=[4.25*cm]*4)
    metrics_tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0),HexColor("#091525")),("BACKGROUND",(1,0),(1,0),HexColor("#120915")),
        ("BACKGROUND",(2,0),(2,0),HexColor("#091520")),("BACKGROUND",(3,0),(3,0),HexColor("#0D1520")),
        ("BOX",(0,0),(0,0),1,HexColor("#1E3550")),("BOX",(1,0),(1,0),1,HexColor("#2A1535")),
        ("BOX",(2,0),(2,0),1,HexColor("#1A3530")),("BOX",(3,0),(3,0),1,HexColor("#1A2535")),
        ("LEFTPADDING",(0,0),(-1,-1),16),("RIGHTPADDING",(0,0),(-1,-1),16),
        ("TOPPADDING",(0,0),(-1,-1),16),("BOTTOMPADDING",(0,0),(-1,-1),16),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    story.append(metrics_tbl)
    story.append(Spacer(1, 24))

    story.append(Paragraph("AI-Generated Analysis", h2_style))
    story.append(HRFlowable(width="100%",thickness=0.5,color=BORDER,spaceAfter=10))

    import re as _re
    _section_colors=[ACCENT,RED,YELLOW,PURPLE,GREEN,ORANGE,ACCENT]
    def _first_sentences(text,n=3):
        text=_re.sub(r'\*\*(.*?)\*\*',r'\1',text)
        text=_re.sub(r'^[-*]\s+','',text,flags=_re.MULTILINE)
        text=_re.sub(r'^\d+\.\s+','',text,flags=_re.MULTILINE)
        text=' '.join(text.split())
        parts=_re.split(r'(?<=[.!?])\s+',text)
        return ' '.join(parts[:n])

    _ai_norm=_re.sub(r'^\s*##\s+','##SPLIT##',ai_summary.strip(),flags=_re.MULTILINE)
    _raw_sections=_ai_norm.split('##SPLIT##')
    sec_label_sty=ParagraphStyle("secl",fontName="Helvetica-Bold",fontSize=8,textColor=ACCENT,leading=12,spaceAfter=0)
    sec_body_sty=ParagraphStyle("secb",fontName="Helvetica",fontSize=8,textColor=MUTED,leading=12,spaceAfter=0)
    ai_tbl_rows=[]
    _sec_idx=0
    for _raw in _raw_sections:
        _raw=_raw.strip()
        if not _raw: continue
        _lines=_raw.split('\n',1)
        _sec_title=_re.sub(r'^#+\s*','',_lines[0]).strip()
        _sec_body=_lines[1].strip() if len(_lines)>1 else ""
        if not _sec_title: continue
        _col=_section_colors[_sec_idx%len(_section_colors)]
        _sec_idx+=1
        lbl_sty=ParagraphStyle(f"lbl{_sec_idx}",fontName="Helvetica-Bold",fontSize=8,textColor=_col,leading=12)
        summary=_first_sentences(_sec_body,3)
        ai_tbl_rows.append([Paragraph(sanitize_for_pdf(_sec_title.upper()),lbl_sty),Paragraph(sanitize_for_pdf(summary),sec_body_sty)])

    if ai_tbl_rows:
        ai_tbl=Table(ai_tbl_rows,colWidths=[4.5*cm,12.7*cm])
        ai_tbl.setStyle(TableStyle([
            ("ROWBACKGROUNDS",(0,0),(-1,-1),[HexColor("#080B14"),HexColor("#0A0D18")]),
            ("GRID",(0,0),(-1,-1),0.4,BORDER),
            ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
            ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
            ("VALIGN",(0,0),(-1,-1),"TOP"),
        ]))
        story.append(ai_tbl)
    story.append(Spacer(1,14))

    story.append(Paragraph("Cleaning Operations Log", h2_style))
    story.append(HRFlowable(width="100%",thickness=0.5,color=BORDER,spaceAfter=12))
    steps_header=[[Paragraph("#",badge_style),Paragraph("TYPE",badge_style),Paragraph("DESCRIPTION",badge_style)]]
    steps_rows=[]
    MAX_STEPS_SHOWN=50
    steps_to_show=cleaning_steps[:MAX_STEPS_SHOWN]
    for i,(stype,sdesc) in enumerate(steps_to_show,1):
        type_color=YELLOW if stype=="duplicate" else(ACCENT if "num" in stype else GREEN)
        type_sty=ParagraphStyle(f"ts{i}",fontName="Helvetica-Bold",fontSize=8,textColor=type_color)
        desc_sty=ParagraphStyle(f"ds{i}",fontName="Courier",fontSize=8,textColor=TEXT,leading=12)
        steps_rows.append([Paragraph(str(i),body_style),Paragraph(sanitize_for_pdf(stype.upper()),type_sty),Paragraph(sanitize_for_pdf(sdesc[:120]),desc_sty)])
    if len(cleaning_steps)>MAX_STEPS_SHOWN:
        overflow_sty=ParagraphStyle("ov",fontName="Helvetica",fontSize=8,textColor=MUTED)
        steps_rows.append([Paragraph("...",body_style),Paragraph("MORE",overflow_sty),Paragraph(f"...and {len(cleaning_steps)-MAX_STEPS_SHOWN} more ops",overflow_sty)])
    if not steps_rows:
        steps_rows=[[Paragraph("-",body_style),Paragraph("NONE",body_style),Paragraph("No cleaning operations required.",body_style)]]

    steps_tbl=Table(steps_header+steps_rows,colWidths=[1*cm,3*cm,13*cm])
    steps_tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),HexColor("#0D1526")),("TEXTCOLOR",(0,0),(-1,0),ACCENT),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[HexColor("#080B14"),HexColor("#0A0D18")]),
        ("GRID",(0,0),(-1,-1),0.5,BORDER),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("VALIGN",(0,0),(-1,-1),"TOP"),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,0),8),
    ]))
    story.append(steps_tbl)
    story.append(Spacer(1,22))

    story.append(PageBreak())
    story.append(Paragraph("Column Quality Breakdown", h2_style))
    story.append(HRFlowable(width="100%",thickness=0.5,color=BORDER,spaceAfter=12))
    col_header=[[Paragraph("COLUMN",badge_style),Paragraph("TYPE",badge_style),Paragraph("COMPLETENESS",badge_style),Paragraph("NULLS",badge_style),Paragraph("UNIQUE",badge_style),Paragraph("ACTION",badge_style)]]
    col_rows=[]
    for cinfo in col_info:
        pct=cinfo["completeness"]
        pct_color=GREEN if pct>=95 else(YELLOW if pct>=80 else RED)
        pct_sty=ParagraphStyle("ps",fontName="Helvetica-Bold",fontSize=9,textColor=pct_color)
        name_sty=ParagraphStyle("ns",fontName="Courier",fontSize=9,textColor=WHITE)
        type_sty=ParagraphStyle("ts",fontName="Courier",fontSize=8,textColor=ACCENT)
        col_rows.append([
            Paragraph(sanitize_for_pdf(cinfo["name"][:22]),name_sty),
            Paragraph(sanitize_for_pdf(cinfo["dtype"]),type_sty),
            Paragraph(f"{pct}%",pct_sty),Paragraph(str(cinfo["nulls"]),body_style),
            Paragraph(str(cinfo["unique"]),body_style),Paragraph(sanitize_for_pdf(cinfo["action"]),body_style),
        ])
    col_tbl=Table(col_header+col_rows,colWidths=[4.5*cm,1.8*cm,3*cm,2*cm,2*cm,3.7*cm])
    col_tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),HexColor("#0D1526")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[HexColor("#080B14"),HexColor("#0A0D18")]),
        ("GRID",(0,0),(-1,-1),0.5,BORDER),
        ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    story.append(col_tbl)
    story.append(Spacer(1,24))

    story.append(HRFlowable(width="100%",thickness=0.5,color=BORDER,spaceAfter=10))
    footer_sty=ParagraphStyle("fs",fontName="Helvetica",fontSize=8,textColor=HexColor("#2A3550"))
    story.append(Paragraph(sanitize_for_pdf(f"Gemini The Data Analyzer - Report generated {timestamp} - Powered by Google Gemini AI"),footer_sty))
    doc.build(story)
    buf.seek(0)
    return buf.read()


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "df_for_chat" not in st.session_state:
    st.session_state.df_for_chat = None
if "chat_context" not in st.session_state:
    st.session_state.chat_context = ""
if "chat_input_key" not in st.session_state:
    st.session_state.chat_input_key = 0


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
        "API Key", type="password",
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
        "Upload CSV or Excel", type=["csv","xlsx"],
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

    opt_remove_dup = st.checkbox("Remove duplicates", value=True)
    opt_fill_nulls = st.checkbox("Fill missing values", value=True)
    opt_strip_ws   = st.checkbox("Strip whitespace (text cols)", value=True)
    opt_lower_case = st.checkbox("Normalise text case", value=False)
    null_strategy  = st.selectbox("Null-fill strategy (numeric)", ["Mean","Median","Zero"], index=0)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    run_btn = st.button("Run Cleaning Pipeline", use_container_width=True)

    # ── CHATBOT SIDEBAR PANEL ──────────────────────────
    if st.session_state.df_for_chat is not None:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section-header">
          <div class="section-dot" style="background:#F97316;box-shadow:0 0 10px rgba(249,115,22,0.6)"></div>
          <div class="section-title">Clear Chat</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()

        st.markdown("""
        <div style="margin-top:16px;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);
          border-radius:12px;padding:16px 18px;">
          <div style="font-family:'Syne',sans-serif;font-size:11px;font-weight:700;
            text-transform:uppercase;letter-spacing:0.1em;color:#5A6178;margin-bottom:12px;">
            Quick Questions
          </div>
        </div>
        """, unsafe_allow_html=True)

        quick_qs = [
            "What are the column names?",
            "Which columns have missing data?",
            "What is the data type of each column?",
            "Summarise the dataset in 3 sentences",
            "What are the top 5 most common values?",
            "Are there any outliers?",
            "What correlations exist between numeric columns?",
            "Give me insights about this data",
        ]
        for q in quick_qs:
            if st.button(q, key=f"quick_{q}", use_container_width=True):
                st.session_state.chat_messages.append({
                    "role": "user", "content": q,
                    "time": datetime.datetime.now().strftime("%H:%M")
                })
                with st.spinner("Thinking..."):
                    ctx = st.session_state.chat_context
                    history_text = "\n".join(
                        f"{m['role'].upper()}: {m['content']}"
                        for m in st.session_state.chat_messages[:-1][-6:]
                    )
                    full_prompt = f"""You are a data analyst expert. Answer the question about the dataset below.
Be concise, specific, and use actual numbers from the data. Use markdown formatting.

DATASET CONTEXT:
{ctx}

CONVERSATION HISTORY:
{history_text}

USER QUESTION: {q}

Answer directly and precisely. If calculations are needed, show them."""
                    try:
                        resp = model.generate_content(full_prompt)
                        answer = resp.text
                    except Exception as e:
                        answer = f"Sorry, I couldn't process that: {e}"
                st.session_state.chat_messages.append({
                    "role": "assistant", "content": answer,
                    "time": datetime.datetime.now().strftime("%H:%M")
                })
                st.rerun()


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
          <div class="step-chip {'done' if st.session_state.df_for_chat is not None else ''}"><div class="step-num">5</div>Chat</div>
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
            completeness = round(100 * (1 - null_total / max(df.size,1)), 1)

            col1m, col2m, col3m, col4m = st.columns(4)
            with col1m:
                st.markdown(f"""<div class="metric-card accent"><div class="metric-icon">&#128202;</div>
                <div class="metric-value">{orig_shape[0]:,}</div><div class="metric-label">Total Rows</div></div>""", unsafe_allow_html=True)
            with col2m:
                st.markdown(f"""<div class="metric-card accent2"><div class="metric-icon">&#128203;</div>
                <div class="metric-value">{orig_shape[1]}</div><div class="metric-label">Columns</div></div>""", unsafe_allow_html=True)
            with col3m:
                st.markdown(f"""<div class="metric-card accent3"><div class="metric-icon">&#128368;</div>
                <div class="metric-value">{null_total:,}</div><div class="metric-label">Missing Values</div></div>""", unsafe_allow_html=True)
            with col4m:
                st.markdown(f"""<div class="metric-card accent4"><div class="metric-icon">&#128260;</div>
                <div class="metric-value">{dup_total:,}</div><div class="metric-label">Duplicates</div></div>""", unsafe_allow_html=True)

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
                pct = round(100*(1-nulls/len(df)),1) if len(df) else 100
                bar_color = get_bar_color(pct)
                dtype_lbl = get_col_type_label(df[col])
                unique = int(df[col].nunique())
                action = ("Fill mean" if dtype_lbl=="NUM" else ("Fill mode" if nulls>0 else "-")) if nulls else "-"
                col_info_list.append({"name":col,"dtype":dtype_lbl,"nulls":nulls,"unique":unique,"completeness":pct,"action":action})
                bars_html += f"""
                <div class="col-row">
                  <div class="col-name" title="{col}">{col}</div>
                  <div class="col-type">{dtype_lbl}</div>
                  <div class="bar-wrap"><div class="bar-fill" style="width:{pct}%;background:{bar_color}"></div></div>
                  <div class="col-pct">{pct}%</div>
                </div>"""
            st.markdown(f'<div class="glass-card" style="max-height:300px;overflow-y:auto">{bars_html}</div>', unsafe_allow_html=True)

            # CHUNKED CLEANING
            st.markdown("""
            <div class="section-header" style="margin-top:8px">
              <div class="section-dot" style="background:#34D399;box-shadow:0 0 10px rgba(52,211,153,0.6)"></div>
              <div class="section-title">Cleaning Pipeline</div>
            </div>
            """, unsafe_allow_html=True)

            n_chunks = math.ceil(len(df)/CHUNK_SIZE)
            all_steps = []
            cleaned_chunks = []
            log_lines = []

            progress_bar = st.progress(0)
            status_text  = st.empty()

            t0 = time.time()
            for ci in range(n_chunks):
                chunk = df.iloc[ci*CHUNK_SIZE:(ci+1)*CHUNK_SIZE].copy()
                status_text.markdown(f"<span style='font-family:DM Mono,monospace;font-size:12px;color:#40C8FF'>Processing chunk {ci+1}/{n_chunks} - rows {ci*CHUNK_SIZE+1:,}-{min((ci+1)*CHUNK_SIZE,len(df)):,}</span>", unsafe_allow_html=True)
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
                        if null_cnt == 0: continue
                        if pd.api.types.is_numeric_dtype(chunk[col]):
                            val = chunk[col].mean() if null_strategy=="Mean" else (chunk[col].median() if null_strategy=="Median" else 0)
                            chunk[col].fillna(val, inplace=True)
                            all_steps.append(("null_num", f"Chunk {ci+1} - '{col}': filled {null_cnt} nulls -> {null_strategy.lower()} {val:.3g}"))
                        else:
                            mode_s = chunk[col].mode()
                            val = mode_s[0] if len(mode_s) else "Unknown"
                            chunk[col].fillna(val, inplace=True)
                            all_steps.append(("null_txt", f"Chunk {ci+1} - '{col}': filled {null_cnt} nulls -> mode '{val}'"))
                        log_lines.append(f'<div class="log-line"><span class="log-time">{time.strftime("%H:%M:%S")}</span><span class="log-ok">FIX</span><span class="log-text">Chunk {ci+1} - {col}: {null_cnt} nulls filled</span></div>')
                cleaned_chunks.append(chunk)
                progress_bar.progress((ci+1)/n_chunks)

            elapsed = round(time.time()-t0, 2)
            cleaned_df = pd.concat(cleaned_chunks, ignore_index=True)
            clean_shape = cleaned_df.shape
            status_text.markdown(f"<span style='font-family:DM Mono,monospace;font-size:12px;color:#34D399'>Done - {len(df):,} rows processed in {elapsed}s</span>", unsafe_allow_html=True)

            # Store cleaned df for chatbot
            st.session_state.df_for_chat = cleaned_df
            st.session_state.chat_context = build_dataset_context(cleaned_df)
            st.session_state.chat_messages = []  # reset on new run

            log_html = "\n".join(log_lines) if log_lines else '<div class="log-line"><span class="log-ok">OK</span><span class="log-text">No issues found - dataset is already clean!</span></div>'
            st.markdown(f'<div class="terminal">{log_html}</div>', unsafe_allow_html=True)

            rows_removed = orig_shape[0]-clean_shape[0]
            pct_retained = round(100*clean_shape[0]/orig_shape[0],1)
            c1,c2,c3,c4 = st.columns(4)
            with c1:
                st.markdown(f"""<div class="metric-card accent4"><div class="metric-icon">&#9989;</div>
                <div class="metric-value">{clean_shape[0]:,}</div><div class="metric-label">Clean Rows</div></div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class="metric-card accent3"><div class="metric-icon">&#128465;</div>
                <div class="metric-value">{rows_removed:,}</div><div class="metric-label">Rows Removed</div></div>""", unsafe_allow_html=True)
            with c3:
                st.markdown(f"""<div class="metric-card accent"><div class="metric-icon">&#128175;</div>
                <div class="metric-value">{pct_retained}%</div><div class="metric-label">Retained</div></div>""", unsafe_allow_html=True)
            with c4:
                st.markdown(f"""<div class="metric-card accent2"><div class="metric-icon">&#9889;</div>
                <div class="metric-value">{elapsed}s</div><div class="metric-label">Process Time</div></div>""", unsafe_allow_html=True)

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
- Use ONLY plain markdown. Do NOT output HTML tags.
- Use ## for each section heading.
- Use plain text, bullet points with "- ", and numbered lists with "1. ".
- Bold important words with **double asterisks**.

Use EXACTLY these section headers:
## Dataset Overview
## Issues Detected
## Cleaning Actions Performed
## Data Quality Score
## Statistical Impact
## Recommendations
## Conclusion

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

Be thorough and specific. Use real numbers. Output ONLY markdown, no HTML."""

            with st.spinner("Gemini is writing your detailed report..."):
                try:
                    response = model.generate_content(prompt)
                    ai_text = response.text
                except Exception as e:
                    ai_text = f"## Automated Report\n\n{steps_text}"

            import re, html as _html

            def _gemini_to_markdown(raw):
                t = str(raw or "")
                t = re.sub(r"^```[a-z]*\n?","",t.strip(),flags=re.IGNORECASE)
                t = re.sub(r"\n?```$","",t.strip())
                if re.search(r"(?i)<(div|span|p|h[1-6]|ul|ol|li|section)\b",t):
                    t = re.sub(r"(?i)<(?:strong|b)[^>]*>(.*?)</(?:strong|b)>",r"**\1**",t,flags=re.DOTALL)
                    t = re.sub(r"(?i)<h[1-3][^>]*>(.*?)</h[1-3]>",r"\n## \1\n",t,flags=re.DOTALL)
                    known_headings=["Dataset Overview","Issues Detected","Cleaning Actions Performed","Data Quality Score","Statistical Impact","Recommendations","Conclusion"]
                    for heading in known_headings:
                        t = re.sub(r'<span[^>]*>\s*'+re.escape(heading)+r'\s*</span>',f'\n## {heading}\n',t,flags=re.IGNORECASE)
                    t = re.sub(r"(?i)<li[^>]*>(.*?)</li>",r"\n- \1",t,flags=re.DOTALL)
                    t = re.sub(r"(?i)<br\s*/?>","\n",t)
                    t = re.sub(r"(?i)</(div|p|h[1-6]|section|article|ul|ol)>","\n",t)
                    t = re.sub(r"<[^>]+>","",t)
                    t = _html.unescape(t)
                    t = re.sub(r"^\s*[\U0001F000-\U0001FFFF\u2600-\u27BF]+\s*$","",t,flags=re.MULTILINE)
                    t = re.sub(r"^\s*[▸►▶•·‣⁃]\s*","- ",t,flags=re.MULTILINE)
                t = re.sub(r"\n{3,}","\n\n",t)
                return t.strip()

            ai_text_clean = _gemini_to_markdown(ai_text)
            ai_text_norm = re.sub(r'^\s*##\s+','##SPLIT##',ai_text_clean,flags=re.MULTILINE)
            raw_sections = ai_text_norm.split('##SPLIT##')

            rendered_sections = ""
            section_icons={"Dataset Overview":"&#128202;","Issues Detected":"&#128269;","Cleaning Actions Performed":"&#129529;","Data Quality Score":"&#128202;","Statistical Impact":"&#128200;","Recommendations":"&#128161;","Conclusion":"&#9989;"}
            section_colors={"Dataset Overview":"#40C8FF","Issues Detected":"#F87171","Cleaning Actions Performed":"#FBBF24","Data Quality Score":"#7B6EF6","Statistical Impact":"#34D399","Recommendations":"#F97316","Conclusion":"#40C8FF"}

            def _safe(text): return _html.escape(str(text),quote=False)
            def _render_bold(text):
                escaped=_safe(text)
                return re.sub(r'\*\*(.*?)\*\*',r'<strong style="color:#E8EBF4;">\1</strong>',escaped)

            for s in raw_sections:
                s=s.strip()
                if not s: continue
                lines=s.split('\n',1)
                title=re.sub(r'^#+\s*','',lines[0]).strip()
                body=lines[1].strip() if len(lines)>1 else ""
                if not title: continue
                icon=section_icons.get(title,"&#10022;")
                color=section_colors.get(title,"#40C8FF")
                body_html=""
                for line in body.split('\n'):
                    line=line.strip()
                    if not line or line=="---": continue
                    if line.startswith('- ') or line.startswith('* '):
                        body_html+=(f'<div style="display:flex;gap:10px;margin:6px 0;"><span style="color:{color};flex-shrink:0;margin-top:3px;font-size:11px;">&#9656;</span><span style="color:#A8B0C8;font-size:13.5px;line-height:1.7;">{_render_bold(line[2:])}</span></div>')
                    elif re.match(r'^\d+\.',line):
                        num,rest=line.split('.',1)
                        body_html+=(f'<div style="display:flex;gap:10px;margin:8px 0;"><span style="color:{color};font-family:DM Mono,monospace;font-size:11px;font-weight:700;flex-shrink:0;width:22px;padding-top:2px;">{_safe(num)}.</span><span style="color:#A8B0C8;font-size:13.5px;line-height:1.7;">{_render_bold(rest.strip())}</span></div>')
                    else:
                        body_html+=f'<p style="color:#A8B0C8;font-size:13.5px;line-height:1.8;margin:8px 0;">{_render_bold(line)}</p>'
                rendered_sections+=(f'<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-left:3px solid {color};border-radius:12px;padding:20px 24px;margin-bottom:16px;"><div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;"><span style="font-size:18px;">{icon}</span><span style="font-family:\'Syne\',sans-serif;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:{color};">{_safe(title)}</span></div><div>{body_html}</div></div>')

            st.markdown(f'<div class="ai-report"><div class="ai-badge">* Gemini AI - Detailed Analysis Report - {datetime.datetime.now().strftime("%H:%M:%S")}</div>{rendered_sections}</div>', unsafe_allow_html=True)

            ai_text = ai_text_clean

            with st.expander("Preview Cleaned Dataset (first 20 rows)"):
                st.dataframe(cleaned_df.head(20), use_container_width=True)

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                pdf_bytes = build_pdf_report(orig_shape, clean_shape, col_info_list, all_steps, ai_text, timestamp)
                pdf_ok = True
            except Exception as e:
                st.error(f"PDF generation error: {e}")
                pdf_ok = False

            csv_buf = io.StringIO()
            cleaned_df.to_csv(csv_buf, index=False)
            csv_bytes = csv_buf.getvalue().encode()

            st.markdown("""
            <div class="section-header" style="margin-top:24px">
              <div class="section-dot" style="background:#40C8FF;box-shadow:0 0 10px rgba(64,200,255,0.6)"></div>
              <div class="section-title">Export Results</div>
            </div>
            """, unsafe_allow_html=True)

            dl1, dl2 = st.columns(2)
            with dl1:
                st.download_button(label="Download Cleaned CSV", data=csv_bytes,
                    file_name=f"datapulse_cleaned_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv", use_container_width=True)
            with dl2:
                if pdf_ok:
                    st.download_button(label="Download PDF Report", data=pdf_bytes,
                        file_name=f"datapulse_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf", use_container_width=True)

        # ── CHATBOT SECTION ────────────────────────────────────────────
        if st.session_state.df_for_chat is not None:
            st.markdown("""
            <div class="section-header" style="margin-top:36px">
              <div class="section-dot" style="background:#F97316;box-shadow:0 0 10px rgba(249,115,22,0.7)"></div>
              <div class="section-title">Dataset Chatbot — Ask Anything</div>
            </div>
            """, unsafe_allow_html=True)

            # Chat container header
            st.markdown("""
            <div class="chat-container">
              <div class="chat-header">
                <div class="chat-avatar">&#129302;</div>
                <div class="chat-header-info">
                  <div class="chat-header-name">Gemini Data Assistant</div>
                  <div class="chat-header-status">
                    <div class="chat-status-dot"></div>
                    Ready to answer questions about your dataset
                  </div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Chat history display
            msgs = st.session_state.chat_messages
            if not msgs:
                df_chat = st.session_state.df_for_chat
                col_preview = ", ".join(df_chat.columns[:5].tolist())
                if len(df_chat.columns) > 5:
                    col_preview += f" ... +{len(df_chat.columns)-5} more"
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);
                  border-radius:16px;padding:32px;text-align:center;margin-bottom:16px;">
                  <div style="font-size:48px;margin-bottom:14px;">&#129302;</div>
                  <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:700;color:#E8EBF4;margin-bottom:8px;">
                    Hi! I know your dataset inside out.
                  </div>
                  <div style="font-size:13px;color:#5A6178;line-height:1.7;max-width:500px;margin:0 auto;">
                    Your cleaned dataset has <strong style="color:#40C8FF">{st.session_state.df_for_chat.shape[0]:,} rows</strong> and 
                    <strong style="color:#7B6EF6">{st.session_state.df_for_chat.shape[1]} columns</strong>.<br>
                    Columns: <span style="font-family:'DM Mono',monospace;color:#34D399;font-size:11px;">{col_preview}</span><br><br>
                    Ask me anything — trends, distributions, outliers, correlations, or plain English summaries.
                  </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                chat_html = '<div style="display:flex;flex-direction:column;gap:14px;padding:16px 0;max-height:500px;overflow-y:auto;">'
                for msg in msgs:
                    role = msg["role"]
                    content = msg["content"]
                    ts = msg.get("time","")
                    import html as _html2
                    # Convert markdown bold/bullets in response to HTML
                    def _md_to_html_inline(text):
                        text = _html2.escape(text)
                        text = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color:#E8EBF4">\1</strong>', text)
                        text = re.sub(r'^- (.+)$', r'<div style="margin:3px 0;padding-left:12px;border-left:2px solid rgba(64,200,255,0.3);color:#A8B0C8;">\1</div>', text, flags=re.MULTILINE)
                        text = text.replace('\n', '<br>')
                        return text

                    if role == "user":
                        chat_html += f'''
                        <div style="display:flex;flex-direction:row-reverse;gap:10px;align-items:flex-start;">
                          <div style="width:30px;height:30px;border-radius:8px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0;">&#128100;</div>
                          <div>
                            <div style="max-width:500px;padding:12px 16px;border-radius:14px;border-top-right-radius:4px;background:linear-gradient(135deg,rgba(64,200,255,0.12),rgba(123,110,246,0.12));border:1px solid rgba(64,200,255,0.2);color:#E8EBF4;font-size:13.5px;line-height:1.7;">{_html2.escape(content)}</div>
                            <div style="font-family:'DM Mono',monospace;font-size:9px;color:#2A3550;margin-top:4px;text-align:right;padding-right:4px;">{ts}</div>
                          </div>
                        </div>'''
                    else:
                        chat_html += f'''
                        <div style="display:flex;gap:10px;align-items:flex-start;">
                          <div style="width:30px;height:30px;border-radius:8px;background:linear-gradient(135deg,rgba(64,200,255,0.2),rgba(123,110,246,0.2));border:1px solid rgba(64,200,255,0.3);display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0;">&#129302;</div>
                          <div style="flex:1;">
                            <div style="max-width:620px;padding:14px 18px;border-radius:14px;border-top-left-radius:4px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#C8D0E4;font-size:13.5px;line-height:1.75;">{_md_to_html_inline(content)}</div>
                            <div style="font-family:'DM Mono',monospace;font-size:9px;color:#2A3550;margin-top:4px;padding-left:4px;">{ts} · Gemini</div>
                          </div>
                        </div>'''
                chat_html += '</div>'
                st.markdown(chat_html, unsafe_allow_html=True)

            # Chat input
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            chat_col1, chat_col2 = st.columns([5, 1])
            with chat_col1:
                user_input = st.text_input(
                    "Ask a question about your dataset",
                    placeholder="e.g. What is the average value of column X? Which rows have the highest Y?",
                    label_visibility="collapsed",
                    key=f"chat_input_{st.session_state.chat_input_key}"
                )
            with chat_col2:
                send_btn = st.button("Send ➤", use_container_width=True, key="send_chat")

            if send_btn and user_input.strip():
                user_msg = user_input.strip()
                st.session_state.chat_messages.append({
                    "role": "user", "content": user_msg,
                    "time": datetime.datetime.now().strftime("%H:%M")
                })
                st.session_state.chat_input_key += 1

                with st.spinner("Gemini is analyzing your data..."):
                    ctx = st.session_state.chat_context
                    history_text = "\n".join(
                        f"{m['role'].upper()}: {m['content']}"
                        for m in st.session_state.chat_messages[:-1][-8:]
                    )
                    full_prompt = f"""You are a professional data analyst with deep expertise in statistics and data science.
The user has uploaded and cleaned a dataset. Answer their question using the dataset context below.

RULES:
- Be precise and use actual numbers from the data wherever possible
- Use markdown formatting (bold, bullets, tables if needed)
- If you perform calculations, show the steps briefly
- If the question is outside dataset scope, say so politely
- Keep responses concise but complete

DATASET CONTEXT:
{ctx}

CONVERSATION HISTORY:
{history_text}

USER QUESTION: {user_msg}

Provide a helpful, accurate, data-driven answer."""

                    try:
                        resp = model.generate_content(full_prompt)
                        answer = resp.text
                    except Exception as e:
                        answer = f"Sorry, I encountered an error: {e}"

                st.session_state.chat_messages.append({
                    "role": "assistant", "content": answer,
                    "time": datetime.datetime.now().strftime("%H:%M")
                })
                st.rerun()

            # Suggested questions chips (only shown if no messages)
            if not st.session_state.chat_messages:
                st.markdown("""
                <div style="margin-top:12px;">
                  <div style="font-family:'DM Mono',monospace;font-size:10px;color:#2A3550;margin-bottom:8px;text-transform:uppercase;letter-spacing:0.08em;">
                    Try asking →
                  </div>
                  <div style="display:flex;flex-wrap:wrap;gap:8px;">
                """, unsafe_allow_html=True)

                suggestions = [
                    "Summarise this dataset",
                    "Which columns have missing data?",
                    "What are the numeric column stats?",
                    "Find any potential outliers",
                    "What insights can you give me?",
                ]
                for sug in suggestions:
                    st.markdown(f'<span class="suggestion-chip">{sug}</span>', unsafe_allow_html=True)
                st.markdown("</div></div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center;padding:32px 0 20px;
  border-top:1px solid rgba(255,255,255,0.05);margin-top:40px">
  <span style="font-family:'DM Mono',monospace;font-size:11px;color:#2A3550;">
    * Gemini The Data Analyzer - Powered by Google Gemini AI - Built for Scale
  </span>
</div>
""", unsafe_allow_html=True)