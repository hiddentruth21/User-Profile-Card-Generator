import streamlit as st
import anthropic
import json
import re

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Profile Card Generator",
    page_icon="🪪",
    layout="wide",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Card wrapper */
.profile-card {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #e5e5e5;
    background: #ffffff;
    max-width: 420px;
    margin: 0 auto;
    font-family: 'Segoe UI', sans-serif;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}
.card-banner {
    height: 80px;
    width: 100%;
}
.card-body {
    padding: 0 22px 22px;
}
.avatar-circle {
    width: 68px; height: 68px;
    border-radius: 50%;
    border: 3px solid white;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; font-weight: 700;
    margin-top: -34px; margin-bottom: 10px;
}
.card-name {
    font-size: 20px; font-weight: 700;
    color: #111; margin: 0 0 3px;
}
.card-tagline {
    font-size: 13px; color: #666;
    margin: 0 0 12px;
}
.card-bio {
    font-size: 13px; line-height: 1.65;
    color: #444; margin: 0 0 14px;
}
.tag-row { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px; }
.skill-tag {
    font-size: 11px; padding: 4px 12px;
    border-radius: 20px; font-weight: 600;
}
.card-meta {
    display: flex; gap: 16px; flex-wrap: wrap;
    font-size: 12px; color: #888;
    border-top: 1px solid #f0f0f0;
    padding-top: 12px;
}
.ai-note {
    font-size: 11px; color: #bbb;
    font-style: italic; margin-top: 10px;
    border-top: 1px solid #f5f5f5;
    padding-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# ── Color themes ───────────────────────────────────────────────────────────────
COLOR_MAP = {
    "purple": {"banner": "#534AB7", "tag_bg": "#EEEDFE", "tag_text": "#3C3489", "avatar_bg": "#EEEDFE", "avatar_text": "#3C3489"},
    "teal":   {"banner": "#1D9E75", "tag_bg": "#E1F5EE", "tag_text": "#085041", "avatar_bg": "#E1F5EE", "avatar_text": "#085041"},
    "coral":  {"banner": "#D85A30", "tag_bg": "#FAECE7", "tag_text": "#712B13", "avatar_bg": "#FAECE7", "avatar_text": "#712B13"},
    "blue":   {"banner": "#378ADD", "tag_bg": "#E6F1FB", "tag_text": "#0C447C", "avatar_bg": "#E6F1FB", "avatar_text": "#0C447C"},
    "green":  {"banner": "#639922", "tag_bg": "#EAF3DE", "tag_text": "#27500A", "avatar_bg": "#EAF3DE", "avatar_text": "#27500A"},
    "amber":  {"banner": "#BA7517", "tag_bg": "#FAEEDA", "tag_text": "#633806", "avatar_bg": "#FAEEDA", "avatar_text": "#633806"},
}

# ── Backend: call Anthropic API ────────────────────────────────────────────────
def generate_card_data(name, title, location, bio, skills):
    """POST user data to Anthropic API and return structured card data."""
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY env var

    prompt = f"""You are a profile card generator. Given user details, return a JSON object (no markdown, no backticks) with:
- tagline: punchy 1-line professional tagline (max 12 words)
- bio_enhanced: polished 2-sentence bio (max 40 words), professional but warm
- color: one of ["purple","teal","coral","blue","green","amber"] fitting their personality/field
- emoji: single emoji representing them

User:
Name: {name}
Title: {title or 'Not specified'}
Location: {location or 'Not specified'}
Bio: {bio or 'Not specified'}
Skills: {', '.join(skills) if skills else 'Not specified'}

Return ONLY valid JSON."""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text
    # Strip accidental markdown fences
    clean = re.sub(r"```json|```", "", raw).strip()
    return json.loads(clean)


# ── Frontend: render card HTML ─────────────────────────────────────────────────
def render_profile_card(result, name, title, location, img_url, skills):
    color = result.get("color", "purple")
    c = COLOR_MAP.get(color, COLOR_MAP["purple"])
    emoji = result.get("emoji", "")
    tagline = result.get("tagline", title)
    bio_enhanced = result.get("bio_enhanced", "")

    # Avatar: image or initials
    initials = "".join(w[0] for w in name.split() if w)[:2].upper()
    if img_url:
        avatar_html = f"""
        <img src="{img_url}" alt="{name}"
             style="width:68px;height:68px;border-radius:50%;
                    border:3px solid white;margin-top:-34px;
                    margin-bottom:10px;object-fit:cover;display:block;"
             onerror="this.style.display='none'" />
        """
    else:
        avatar_html = f"""
        <div class="avatar-circle"
             style="background:{c['avatar_bg']};color:{c['avatar_text']};">
            {initials}
        </div>
        """

    # Skill tags
    tags_html = ""
    if skills:
        tags_inner = "".join(
            f'<span class="skill-tag" style="background:{c["tag_bg"]};color:{c["tag_text"]};">{s}</span>'
            for s in skills
        )
        tags_html = f'<div class="tag-row">{tags_inner}</div>'

    # Meta row
    meta_parts = []
    if location:
        meta_parts.append(f"📍 {location}")
    if title:
        meta_parts.append(f"💼 {title}")
    meta_html = f'<div class="card-meta">{"&nbsp;&nbsp;".join(meta_parts)}</div>' if meta_parts else ""

    card = f"""
    <div class="profile-card">
        <div class="card-banner" style="background:{c['banner']};"></div>
        <div class="card-body">
            {avatar_html}
            <p class="card-name">{emoji} {name}</p>
            <p class="card-tagline">{tagline}</p>
            <p class="card-bio">{bio_enhanced}</p>
            {tags_html}
            {meta_html}
            <p class="ai-note">✦ Tagline and bio polished by AI</p>
        </div>
    </div>
    """
    return card


# ── Layout ─────────────────────────────────────────────────────────────────────
st.title("🪪 Profile Card Generator")
st.caption("Fill in your details — the AI backend will craft your tagline, enhance your bio, and pick a colour theme.")

form_col, preview_col = st.columns([1, 1], gap="large")

with form_col:
    st.subheader("Your details")

    name     = st.text_input("Full name *", placeholder="e.g. Priya Sharma")
    title    = st.text_input("Job title / role", placeholder="e.g. Senior UX Designer")
    location = st.text_input("Location", placeholder="e.g. Hyderabad, India")
    img_url  = st.text_input("Profile image URL (optional)", placeholder="https://...")
    bio      = st.text_area("Bio", placeholder="Tell us about your background, interests, or what you're working on…", height=110)

    # Skills tag builder
    st.markdown("**Skills / interests**")
    if "skills" not in st.session_state:
        st.session_state.skills = []

    skill_input = st.text_input("Type a skill and press Add", key="skill_field", placeholder="e.g. React, Figma, Photography")
    add_col, _ = st.columns([1, 3])
    with add_col:
        if st.button("Add skill", use_container_width=True):
            val = skill_input.strip()
            if val and val not in st.session_state.skills and len(st.session_state.skills) < 8:
                st.session_state.skills.append(val)
                st.rerun()

    if st.session_state.skills:
        cols = st.columns(4)
        for i, skill in enumerate(st.session_state.skills):
            with cols[i % 4]:
                if st.button(f"✕ {skill}", key=f"rm_{i}", use_container_width=True):
                    st.session_state.skills.pop(i)
                    st.rerun()

    st.divider()
    generate_btn = st.button("✨ Generate profile card", type="primary", use_container_width=True)

# ── Generation logic ───────────────────────────────────────────────────────────
with preview_col:
    st.subheader("Preview")

    if generate_btn:
        if not name.strip():
            st.error("Please enter a full name.")
        else:
            with st.spinner("Calling the AI backend…"):
                try:
                    result = generate_card_data(
                        name=name,
                        title=title,
                        location=location,
                        bio=bio,
                        skills=st.session_state.skills,
                    )
                    st.session_state.card_result = result
                    st.session_state.card_form = dict(
                        name=name, title=title, location=location,
                        img_url=img_url, skills=list(st.session_state.skills)
                    )
                    st.success("Profile card generated!")
                except Exception as e:
                    st.error(f"API error: {e}")

    if "card_result" in st.session_state:
        f = st.session_state.card_form
        card_html = render_profile_card(
            result=st.session_state.card_result,
            name=f["name"], title=f["title"],
            location=f["location"], img_url=f["img_url"],
            skills=f["skills"],
        )
        st.markdown(card_html, unsafe_allow_html=True)

        # Show raw JSON returned by the API
        with st.expander("🔍 Raw API response (JSON)"):
            st.json(st.session_state.card_result)
    else:
        st.info("👈 Fill in the form and click **Generate profile card**.")
