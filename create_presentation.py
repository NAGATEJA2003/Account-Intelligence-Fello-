"""
Generate 2-slide PowerPoint presentation for Fello AI Builder Hackathon
Usage: pip install python-pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Colors
PRIMARY_BLUE = RGBColor(26, 95, 122)  # #1A5F7A
ACCENT_ORANGE = RGBColor(255, 107, 53)  # #FF6B35
SUCCESS_GREEN = RGBColor(46, 204, 113)  # #2ECC71
DARK_GRAY = RGBColor(52, 73, 94)  # #34495E
WHITE = RGBColor(255, 255, 255)


def create_presentation():
    """Create exactly 2 slides"""
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # ==================== SLIDE 1: Problem & Solution ====================
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.15), Inches(9), Inches(0.6))
    tf = title_box.text_frame
    tf.text = "AI Account Intelligence & Enrichment System"
    p = tf.paragraphs[0]
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.alignment = PP_ALIGN.CENTER

    # Subtitle
    subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.7), Inches(9), Inches(0.35))
    tf = subtitle_box.text_frame
    tf.text = "Transform Anonymous Web Traffic into Actionable Sales Intelligence"
    p = tf.paragraphs[0]
    p.font.size = Pt(18)
    p.font.color.rgb = DARK_GRAY
    p.alignment = PP_ALIGN.CENTER

    # Left column - THE PROBLEM
    problem_header = slide.shapes.add_textbox(Inches(0.3), Inches(1.25), Inches(4.5), Inches(0.4))
    tf = problem_header.text_frame
    tf.text = "THE PROBLEM"
    p = tf.paragraphs[0]
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ORANGE

    problem_box = slide.shapes.add_textbox(Inches(0.3), Inches(1.65), Inches(4.5), Inches(3.8))
    tf = problem_box.text_frame
    tf.word_wrap = True

    problem_items = [
        "70% of buyer journey complete before prospects identify themselves",
        "",
        "Sales Teams Are Flying Blind:",
        "  • No visibility into anonymous visitors",
        "  • High-intent prospects go undetected",
        "  • Hours wasted on manual research",
        "  • Generic, unpersonalized outreach",
        "  • Can't prioritize accounts to pursue",
        "",
        "Result: Qualified pipeline walks away unnoticed"
    ]

    for i, item in enumerate(problem_items):
        p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p.text = item
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_GRAY
        p.space_after = Pt(6)

    # Right column - THE SOLUTION
    solution_header = slide.shapes.add_textbox(Inches(5.2), Inches(1.25), Inches(4.5), Inches(0.4))
    tf = solution_header.text_frame
    tf.text = "THE SOLUTION"
    p = tf.paragraphs[0]
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ORANGE

    solution_box = slide.shapes.add_textbox(Inches(5.2), Inches(1.65), Inches(4.5), Inches(3.8))
    tf = solution_box.text_frame
    tf.word_wrap = True

    solution_items = [
        "Fello Account Intelligence Engine",
        "",
        "Pipeline: Signals → AI (Groq/Llama-3) → Intel",
        "",
        "KEY FEATURES:",
        "  • Real-time company identification",
        "  • AI-powered persona inference",
        "  • Intent scoring (1-10 scale)",
        "  • Firmographics & tech stack analysis",
        "  • Personalized sales hooks & actions",
        "  • One-click GitHub Actions automation",
        "  • Salesforce CRM integration",
        "  • Serverless, zero infrastructure costs",
        "",
        "Impact: 90% reduction in research time"
    ]

    for i, item in enumerate(solution_items):
        p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p.text = item
        if "KEY FEATURES" in item:
            p.font.bold = True
            p.font.size = Pt(14)
            p.font.color.rgb = ACCENT_ORANGE
        else:
            p.font.size = Pt(12)
            p.font.color.rgb = DARK_GRAY
        p.space_after = Pt(6)

    # Bottom tech stack bar
    tech_box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.3), Inches(5.6), Inches(9.4), Inches(1.2)
    )
    tech_box.fill.solid()
    tech_box.fill.fore_color.rgb = RGBColor(44, 62, 80)
    tech_box.line.fill.background()

    tech_text = tech_box.text_frame
    tech_text.word_wrap = True
    tech_text.text = "Tech Stack: Python + Groq (Llama-3) + GitHub Actions + Salesforce    |    17+ data points per account    |    ~2 min for 10 accounts    |    Open Source"
    p = tech_text.paragraphs[0]
    p.font.size = Pt(14)
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER
    tech_text.vertical_anchor = MSO_ANCHOR.MIDDLE

    # ==================== SLIDE 2: Demo & Results ====================
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Header
    header_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.15), Inches(9), Inches(0.5))
    tf = header_box.text_frame
    tf.text = "Live Demonstration: How It Works & Sample Output"
    p = tf.paragraphs[0]
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.alignment = PP_ALIGN.CENTER

    # Left: How It Works
    how_header = slide.shapes.add_textbox(Inches(0.3), Inches(0.8), Inches(3), Inches(0.35))
    tf = how_header.text_frame
    tf.text = "HOW IT WORKS"
    p = tf.paragraphs[0]
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ORANGE

    how_box = slide.shapes.add_textbox(Inches(0.3), Inches(1.2), Inches(3), Inches(2.5))
    tf = how_box.text_frame
    tf.word_wrap = True

    steps = [
        "1️⃣ Trigger Workflow",
        "   GitHub Actions → Run → Execute",
        "",
        "2️⃣ AI Enrichment",
        "   • Company identification",
        "   • Leadership analysis",
        "   • Intent scoring",
        "   • Sales recommendations",
        "",
        "3️⃣ Results in ~2 min",
        "   JSON + Salesforce ready"
    ]

    for i, step in enumerate(steps):
        p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p.text = step
        p.font.size = Pt(11)
        if "1️⃣" in step or "2️⃣" in step or "3️⃣" in step:
            p.font.bold = True
        p.font.color.rgb = DARK_GRAY
        p.space_after = Pt(4)

    # Middle: Sample Output
    sample_header = slide.shapes.add_textbox(Inches(3.5), Inches(0.8), Inches(3), Inches(0.35))
    tf = sample_header.text_frame
    tf.text = "SAMPLE OUTPUT"
    p = tf.paragraphs[0]
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ORANGE

    sample_box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.5), Inches(1.2), Inches(3), Inches(2.5)
    )
    sample_box.fill.solid()
    sample_box.fill.fore_color.rgb = RGBColor(44, 62, 80)
    sample_box.line.color.rgb = ACCENT_ORANGE
    sample_box.line.width = Pt(2)

    sample_text = sample_box.text_frame
    sample_text.word_wrap = True
    sample_text.margin_left = Inches(0.08)
    sample_text.margin_right = Inches(0.08)

    sample_content = """TechCorp Solutions
techcorp.io | Fintech | 200-500 emp

Intent Score: 8/10 ⚡ High Intent!
Persona: VP Engineering - scalability tools

Leadership: Sarah Chen (CTO)

AI Summary: Series B Fintech, $45M raised.
Expanding to Europe. Researching fraud
detection and payment orchestration.

Sales Hook: Hiring Senior Backend Engs =
strong infrastructure expansion signal.

Action: Fintech case studies + fraud
detection ROI metrics."""

    sample_text.text = sample_content
    for paragraph in sample_text.paragraphs:
        paragraph.font.size = Pt(9)
        paragraph.font.color.rgb = WHITE
        paragraph.font.name = "Consolas"

    # Right: Key Features Detail
    features_header = slide.shapes.add_textbox(Inches(6.7), Inches(0.8), Inches(3), Inches(0.35))
    tf = features_header.text_frame
    tf.text = "KEY FEATURES"
    p = tf.paragraphs[0]
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ORANGE

    features_box = slide.shapes.add_textbox(Inches(6.7), Inches(1.2), Inches(3), Inches(2.5))
    tf = features_box.text_frame
    tf.word_wrap = True

    features = [
        "🎯 Intent Scoring",
        "  1-10 scale, purchase readiness",
        "",
        "👤 Persona Detection",
        "  Decision-maker identification",
        "",
        "🏢 Firmographics",
        "  Industry, size, location",
        "",
        "🤖 AI Summary",
        "  Llama-3 deep analysis",
        "",
        "💬 Sales Hooks",
        "  Personalized messaging",
        "",
        "🔄 Automation",
        "  One-click GitHub Actions"
    ]

    for i, feature in enumerate(features):
        p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p.text = feature
        p.font.size = Pt(10)
        if "🎯" in feature or "👤" in feature or "🏢" in feature or "🤖" in feature or "💬" in feature or "🔄" in feature:
            p.font.bold = True
        p.font.color.rgb = DARK_GRAY
        p.space_after = Pt(4)

    # ==================== DATA FLOW TEXT SECTION ====================
    # Header
    flow_header = slide.shapes.add_textbox(Inches(0.3), Inches(3.7), Inches(9.4), Inches(0.35))
    tf = flow_header.text_frame
    tf.text = "DATA FLOW"
    p = tf.paragraphs[0]
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ORANGE
    p.alignment = PP_ALIGN.CENTER

    # Flow diagram as text in a rounded box
    flow_box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(4.05), Inches(7), Inches(0.55)
    )
    flow_box.fill.solid()
    flow_box.fill.fore_color.rgb = RGBColor(44, 62, 80)
    flow_box.line.fill.background()

    flow_text = flow_box.text_frame
    flow_text.word_wrap = True
    flow_text.text = "  Anonymous Visitors  →  AI Analysis (Llama-3)  →  Intent Score + Persona  →  Salesforce CRM"

    for paragraph in flow_text.paragraphs:
        paragraph.font.size = Pt(13)
        paragraph.font.bold = True
        paragraph.font.color.rgb = WHITE

    flow_text.vertical_anchor = MSO_ANCHOR.MIDDLE

    # Bottom: Before/After + Impact
    impact_box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.3), Inches(4.75), Inches(9.4), Inches(2.4)
    )

    # Bottom: Before/After + Impact
    impact_box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.3), Inches(4.65), Inches(9.4), Inches(2.4)
    )
    impact_box.fill.solid()
    impact_box.fill.fore_color.rgb = SUCCESS_GREEN
    impact_box.line.fill.background()

    impact_text = impact_box.text_frame
    impact_text.word_wrap = True
    impact_text.margin_left = Inches(0.2)
    impact_text.margin_right = Inches(0.2)
    impact_text.margin_top = Inches(0.15)
    impact_text.margin_bottom = Inches(0.15)

    impact_content = """BEFORE → AFTER IMPACT:
  2-3 hours manual research → 10 seconds automated
  Generic outreach emails → Personalized AI hooks
  Unknown visitor intent → Intent-scored leads (1-10)

BUSINESS VALUE:
  ✓ Convert anonymous traffic into qualified pipeline
  ✓ Prioritize sales outreach based on intent scores
  ✓ Reduce research time by 90%"""

    impact_text.text = impact_content
    for paragraph in impact_text.paragraphs:
        paragraph.font.size = Pt(12)
        paragraph.font.bold = True
        paragraph.font.color.rgb = WHITE

    return prs


if __name__ == "__main__":
    print("Creating 2-slide PowerPoint presentation...")
    prs = create_presentation()
    filename = "Fello_AI_Hackathon_2Slides_Final.pptx"
    prs.save(filename)
    print(f"Presentation saved as: {filename}")
    print(f"\nTo open: Start '{filename}' or double-click the file")
