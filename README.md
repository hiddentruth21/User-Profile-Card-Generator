🪪 Profile Card Generator

A full-stack AI-powered web app built with Streamlit and the Anthropic API. Fill in your profile details — the AI backend crafts a punchy tagline, polishes your bio, picks a colour theme, and renders a styled profile card in real time.


Features


Form-based input — name, job title, location, profile image URL, bio, and skills
AI backend — sends a POST request to the Anthropic API (claude-opus-4-6) and receives structured JSON
Dynamic card rendering — profile card rendered as styled HTML directly in the browser
6 colour themes — purple, teal, coral, blue, green, amber (AI picks the best fit)
Skill tags — add up to 8 skills/interests; displayed as coloured pills on the card
Image support — paste any image URL; falls back to initials avatar if it fails
Raw API inspector — expandable panel shows the exact JSON returned by the backend



Project Structure

.
├── app.py        # Main Streamlit app (frontend + backend)
└── README.md     # This file


Prerequisites


Python 3.8 or higher
An Anthropic API key — get one at console.anthropic.com



Setup & Installation

1. Clone or download the project

bashgit clone <your-repo-url>
cd profile-card-generator

2. Install dependencies

bashpip install streamlit anthropic

3. Set your Anthropic API key

Mac / Linux:

bashexport ANTHROPIC_API_KEY=sk-ant-xxxxxxxx

Windows (Command Prompt):

cmdset ANTHROPIC_API_KEY=sk-ant-xxxxxxxx

Windows (PowerShell):

powershell$env:ANTHROPIC_API_KEY="sk-ant-xxxxxxxx"

4. Run the app

bashstreamlit run app.py

The app opens automatically at http://localhost:8501.


How It Works

User fills form
      │
      ▼
[Frontend — Streamlit]
Collects: name, title, location, image URL, bio, skills
      │
      ▼  (POST request on button click)
[Backend — Anthropic API]
Model: claude-opus-4-6
Returns JSON:
  • tagline     — punchy 1-line professional tagline
  • bio_enhanced — polished 2-sentence bio
  • color        — theme matching personality/field
  • emoji        — representative emoji
      │
      ▼
[Frontend — Streamlit]
Renders styled HTML profile card


Usage


Open the app in your browser
Fill in your details in the left panel
Add skills by typing in the skill field and clicking Add skill
Click ✨ Generate profile card
Your profile card appears on the right
Expand Raw API response to inspect the JSON from the backend



Troubleshooting

ProblemFixcommand not found: streamlitRun python -m streamlit run app.pyAPI key errorSet the key in the same terminal you run the app fromPort already in useRun streamlit run app.py --server.port 8502Image not showingCheck the URL is publicly accessible and ends in .jpg/.pngJSON parse errorRarely the model returns malformed JSON — just click Generate again


Customisation


Change the model — edit model="claude-opus-4-6" in generate_card_data() to any Anthropic model
Add more fields — add a new st.text_input() in the form column and include it in the API prompt
Add more themes — extend the COLOR_MAP dict with new colour names and hex values
Persist cards — wrap results in st.download_button() to export the card HTML



License

MIT — free to use and modify
