# # app.py
# import streamlit as st
# import tempfile, os
# from pydub import AudioSegment
# import google.generativeai as genai
# from fpdf import FPDF

# # ---------- Helpers ----------

# def save_uploaded_file(uploaded_file):
#     suffix = os.path.splitext(uploaded_file.name)[1]
#     f = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
#     f.write(uploaded_file.read())
#     f.flush()
#     f.close()
#     return f.name

# def extract_audio_to_wav(input_path):
#     # Returns path to a .wav file
#     audio = AudioSegment.from_file(input_path)
#     out = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
#     audio.export(out.name, format="wav")
#     return out.name

# def call_gemini_transcribe(wav_path, model_name="gemini-2.5-flash"):
#     genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", "") or os.getenv("GEMINI_API_KEY", ""))
#     fref = genai.upload_file(wav_path)
#     model = genai.GenerativeModel(model_name)
#     response = model.generate_content([
#         {"role":"user", "parts": ["Transcribe the speech in this audio file:", fref]}
#     ])
#     return response.text

# def call_gemini_text(prompt, model_name="gemini-2.5-flash"):
#     genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", "") or os.getenv("GEMINI_API_KEY", ""))
#     model = genai.GenerativeModel(model_name)
#     response = model.generate_content([{"role":"user", "parts":[prompt]}])
#     return response.text

# def clean_text(text):
#     if not text:
#         return ""
#     return text.replace("**","").replace("\r","").replace("\t","    ").strip()

# def make_pdf_bytes(title, content):
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()
#     pdf.set_font("Times", size=14)
#     pdf.cell(0, 8, title, ln=True)
#     pdf.ln(4)
#     # split text to lines
#     lines = content.splitlines()
#     for line in lines:
#         pdf.multi_cell(0, 8, line)
#     return pdf.output(dest="S").encode("utf-8")  # <- use utf-8


# # ---------- Streamlit UI ----------

# st.set_page_config(page_title="Voice → Text + Flashcards", layout="wide")
# st.title("🎙️ Lecture-To-Notes")

# # Columns: input / output
# col1, col2 = st.columns([1,2])

# with col1:
#     st.subheader("Input")
#     mode = st.radio("Mode", ["Upload file", "(Optional) Record externally & upload"], index=0)
#     uploaded = st.file_uploader("Choose audio or video", type=["wav","mp3","mp4","m4a","mov","ogg","flac"])
#     if uploaded:
#         st.write("Selected:", uploaded.name)

#     if st.button("Transcribe"):
#         if not uploaded:
#             st.warning("Upload a file first.")
#         else:
#             with st.spinner("Extracting audio and transcribing..."):
#                 tmp = save_uploaded_file(uploaded)
#                 try:
#                     wav = extract_audio_to_wav(tmp)
#                     transcript = call_gemini_transcribe(wav)
#                     st.session_state["transcription"] = clean_text(transcript)
#                     st.success("Transcription ready")
#                 except Exception as e:
#                     st.error("Error: " + str(e))
#                 finally:
#                     try: os.remove(tmp)
#                     except: pass
#                     try: os.remove(wav)
#                     except: pass

# with col2:
#     st.subheader("Output")
#     transcription = st.session_state.get("transcription", "")
#     summary = st.session_state.get("summary", "")
#     flashcards = st.session_state.get("flashcards", "")

#     if transcription:
#         st.markdown("### Transcription")
#         st.write(transcription)

#         # Generate buttons
#         if st.button("Generate Summary"):
#             with st.spinner("Generating summary..."):
#                 prompt = f"Summarize the following content into concise notes:\n\n{transcription}"
#                 out = call_gemini_text(prompt)
#                 st.session_state["summary"] = clean_text(out)
#                 st.success("Summary generated")

#         if st.button("Generate Flashcards"):
#             with st.spinner("Generating flashcards..."):
#                 prompt = f"Create 5-10 simple flashcards (Q: ... A: ...) from the following content:\n\n{transcription}"
#                 out = call_gemini_text(prompt)
#                 st.session_state["flashcards"] = clean_text(out)
#                 st.success("Flashcards generated")

#     # Show summary
#     if summary:
#         st.markdown("### Summary")
#         st.write(summary)
#         pdf_bytes = make_pdf_bytes("Summary", summary)
#         st.download_button("Download Summary (PDF)", data=pdf_bytes, file_name="summary.pdf", mime="application/pdf")

#     # Show flashcards
#     if flashcards:
#         st.markdown("### Flashcards")
#         st.write(flashcards)
#         pdf_bytes2 = make_pdf_bytes("Flashcards", flashcards)
#         st.download_button("Download Flashcards (PDF)", data=pdf_bytes2, file_name="flashcards.pdf", mime="application/pdf")
# main_app.py



# import streamlit as st
# import tempfile, os
# from pydub import AudioSegment
# import google.generativeai as genai
# from fpdf import FPDF
# import base64


# # -------------------- Remove top padding --------------------
# st.markdown(
#     """
#     <style>
#     .css-18e3th9 {padding-top: 0rem;}
#     .css-1d391kg {padding-top: 0rem;}
#     </style>
#     """,
#     unsafe_allow_html=True
# )
# st.markdown(
#     """
#     <style>
#     /* Apply Times New Roman font to all headers and paragraphs */
#     h1, h2, h3, h4, h5, h6, p, div, span, label {
#         font-family: 'Times New Roman', Times, serif !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # -------------------- Navigation --------------------
# if "page" not in st.session_state:
#     st.session_state.page = "home"

# def go_home():
#     st.session_state.page = "home"

# def go_voicetotext():
#     st.session_state.page = "voicetotext"

# # -------------------- Helper functions --------------------
# def save_uploaded_file(uploaded_file):
#     suffix = os.path.splitext(uploaded_file.name)[1]
#     f = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
#     f.write(uploaded_file.read())
#     f.flush()
#     f.close()
#     return f.name

# def extract_audio_to_wav(input_path):
#     audio = AudioSegment.from_file(input_path)
#     out = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
#     audio.export(out.name, format="wav")
#     return out.name

# def call_gemini_transcribe(wav_path, model_name="gemini-2.5-flash"):
#     genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", "") or os.getenv("GEMINI_API_KEY", ""))
#     fref = genai.upload_file(wav_path)
#     model = genai.GenerativeModel(model_name)
#     response = model.generate_content([{"role":"user", "parts": ["Transcribe the speech in this audio file:", fref]}])
#     return response.text

# def call_gemini_text(prompt, model_name="gemini-2.5-flash"):
#     genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", "") or os.getenv("GEMINI_API_KEY", ""))
#     model = genai.GenerativeModel(model_name)
#     response = model.generate_content([{"role":"user", "parts":[prompt]}])
#     return response.text

# def clean_text(text):
#     if not text:
#         return ""
#     return text.replace("**", "").replace("\r", "").replace("\t", "    ").strip()

# def make_pdf_bytes(title, content):
#     # Remove or replace characters not supported in latin1
#     cleaned_content = content.encode("latin1", "replace").decode("latin1")
    
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()
#     pdf.set_font("Times", size=14)
#     pdf.cell(0, 8, title, ln=True)
#     pdf.ln(4)
#     lines = cleaned_content.splitlines()
#     for line in lines:
#         # Ensure each line is also encoded safely
#         safe_line = line.encode("latin1", "replace").decode("latin1")
#         pdf.multi_cell(0, 8, safe_line)
#     return pdf.output(dest="S").encode("latin1")

# # -------------------- Function to show background image --------------------
# def set_bg_image(image_file):
#     with open(image_file, "rb") as f:
#         data = f.read()
#     encoded = base64.b64encode(data).decode()
#     st.markdown(
#         f"""
#         <style>
#         .stApp {{
#             background-image: url("data:image/png;base64,{encoded}");
#             background-size: cover;
#             background-position: center;
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

# # -------------------- HOME PAGE --------------------
# if st.session_state.page == "home":
#     set_bg_image("generated-image.png")
#     # Centered Title and Subtitle with minimal spacing
#     st.markdown(
#         """
#         <div style="
#             display: flex; 
#             flex-direction: column; 
#             justify-content: center; 
#             align-items: center; 
#             height: 50vh;   /* reduce vh if you want less vertical space */
#             margin-bottom: 0px;
#             gap: 0px;
#         ">
#             <h1 style='font-size: 60px; margin-bottom:10px; line-height:1;'>Lecture to Notes</h1>
#             <p style='font-size: 20px; max-width: 600px; margin-bottom:20px; line-height:1.2;'>
#                Welcome! This website allows you to transcribe audio or video content into text, generate summaries, and create interactive flashcards using Generative AI. Enhance your learning, test knowledge, and reinforce understanding with ease
#             </p>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     # Add custom CSS for green button and remove margin
#     st.markdown(
#         """
#         <style>
#         div.stButton > button {
#             background-color: #04AA6D;
#             color: white;
#             border: none;
#             padding: 0.8em 2.5em;
#             border-radius: 8px;
#             font-size: 20px;
#             transition: background 0.2s;
#             margin-top: 0px !important;
#             margin-bottom: 0px !important;
#             display: block;
#             margin-left: auto;
#             margin-right: auto;
#         }
#         div.stButton > button:hover {
#             background-color: #038e57;
#             color: white;
#         }
#         </style>
#         """, unsafe_allow_html=True
#     )
#     cols = st.columns([3, 2, 3]) # adjust ratio for desired width
#     with cols[1]:
#         if st.button("Start Voice to Text", key="start_voicetotext_click", help="Click to go to Voice to Text page"):
#             go_voicetotext()


# # -------------------- VOICE TO TEXT PAGE --------------------
# elif st.session_state.page == "voicetotext":
#     set_bg_image("generated-image.png")
#     st.markdown(
#         "<div style='background-color:black; padding:20px;'>"
#         "<h1 style='color:white;'>Voice to Text</h1></div>",
#         unsafe_allow_html=True
#     )

#     # Center the "Back to Home" button
#     cols = st.columns([3, 2, 3])
#     with cols[1]:
#         if st.button("Back to Home"):
#             go_home()

#     mode = st.radio("Select mode:", ["Upload", "Record"])
#     uploaded_file = None
#     transcription = ""
#     flashcards = ""
#     summary = ""

#     if mode == "Upload":
#         uploaded_file = st.file_uploader("Choose audio/video file", type=["wav", "mp3", "mp4", "mov", "m4a", "ogg", "flac"])
#     else:
#         st.info("Use an external recorder to record, then upload the file.")

#     # Center the "Transcribe" button
#     cols = st.columns([3, 2, 3])
#     with cols[1]:
#         transcribe_clicked = st.button("Transcribe")

#     if transcribe_clicked:
#         if not uploaded_file:
#             st.warning("Please upload a file first!")
#         else:
#             tmp = save_uploaded_file(uploaded_file)
#             wav = extract_audio_to_wav(tmp)
#             with st.spinner("Transcribing..."):
#                 transcription = clean_text(call_gemini_transcribe(wav))
#             st.success("Transcription ready!")
#             os.remove(tmp)
#             os.remove(wav)
#             st.session_state.transcription = transcription # Save to session state
#     else:
#         transcription = st.session_state.get("transcription", "")

#     if transcription:
#         st.markdown("### Transcription")
#         st.write(transcription)

#         # Center the "Generate Summary" button
#         cols = st.columns([3, 2, 3])
#         with cols[0]:
#             summary_clicked = st.button("Generate Summary")

#         # Center the "Generate Flashcards" button
#         with cols[2]:
#             flashcard_clicked = st.button("Generate Flashcards")

#         if summary_clicked:
#             with st.spinner("Generating Summary..."):
#                 summary = clean_text(call_gemini_text(f"Summarize the following content:\n\n{transcription}"))
#             st.success("Summary generated!")
#             st.session_state.summary = summary
#         else:
#             summary = st.session_state.get("summary", "")

#         if flashcard_clicked:
#             with st.spinner("Generating Flashcards..."):
#                 flashcards = clean_text(call_gemini_text(f"Create flashcards from the following content:\n\n{transcription}"))
#             st.success("Flashcards generated!")
#             st.session_state.flashcards = flashcards
#         else:
#             flashcards = st.session_state.get("flashcards", "")
#     if summary:
#         st.markdown("### Summary")
#         st.write(summary)
#         pdf_bytes = make_pdf_bytes("Summary", summary)
#         # Center the download button
#         cols = st.columns([3, 2, 3])
#         with cols[1]:
#             st.download_button("Download Summary (PDF)", data=pdf_bytes, file_name="summary.pdf", mime="application/pdf")

#     if flashcards:
#         st.markdown("### Flashcards")
#         st.write(flashcards)
#         pdf_bytes2 = make_pdf_bytes("Flashcards", flashcards)
#         # Center the download button
#         cols = st.columns([3, 2, 3])
#         with cols[1]:
#             st.download_button("Download Flashcards (PDF)", data=pdf_bytes2, file_name="flashcards.pdf", mime="application/pdf")


import streamlit as st
import tempfile, os
from pydub import AudioSegment
import google.generativeai as genai
from fpdf import FPDF
import base64
import re
import streamlit.components.v1 as components

# -------------------- Remove top padding --------------------
st.markdown(
    """
    <style>
    .css-18e3th9 {padding-top: 0rem;}
    .css-1d391kg {padding-top: 0rem;}
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    /* Apply Times New Roman font to all headers and paragraphs */
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        font-family: 'Times New Roman', Times, serif !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- Navigation --------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_home():
    # Reset everything when going back to home
    for key in ["transcription", "summary", "flashcards"]:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.page = "home"


def go_voicetotext():
    st.session_state.page = "voicetotext"

# -------------------- Helper functions --------------------
def save_uploaded_file(uploaded_file):
    suffix = os.path.splitext(uploaded_file.name)[1]
    f = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    f.write(uploaded_file.read())
    f.flush()
    f.close()
    return f.name

def extract_audio_to_wav(input_path):
    audio = AudioSegment.from_file(input_path)
    out = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio.export(out.name, format="wav")
    return out.name

def call_gemini_transcribe(wav_path, model_name="gemini-2.5-flash"):
    genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", "") or os.getenv("GEMINI_API_KEY", ""))
    fref = genai.upload_file(wav_path)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content([{"role":"user", "parts": ["Transcribe the speech in this audio file:", fref]}])
    return response.text

def call_gemini_text(prompt, model_name="gemini-2.5-flash"):
    genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", "") or os.getenv("GEMINI_API_KEY", ""))
    model = genai.GenerativeModel(model_name)
    response = model.generate_content([{"role":"user", "parts":[prompt]}])
    return response.text

def clean_text(text):
    if not text:
        return ""
    return text.replace("**", "").replace("\r", "").replace("\t", "    ").strip()

def make_pdf_bytes(title, content):
    cleaned_content = content.encode("latin1", "replace").decode("latin1")
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Times", size=14)
    pdf.cell(0, 8, title, ln=True)
    pdf.ln(4)
    lines = cleaned_content.splitlines()
    for line in lines:
        safe_line = line.encode("latin1", "replace").decode("latin1")
        pdf.multi_cell(0, 8, safe_line)
    return pdf.output(dest="S").encode("latin1")

# -------------------- Function to show background image --------------------
def set_bg_image(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------- Flashcards rendering ----------
def parse_flashcards_text(flashcards_text):
    """
    Parse flashcards strictly using Front: and Back: markers.
    Returns list of (question, answer) tuples.
    Ignores incomplete cards and extraneous lines.
    """
    flashcards = []
    # Split into lines
    lines = [line.strip() for line in flashcards_text.splitlines() if line.strip()]
    q, a = None, None

    for line in lines:
        # Match front
        front_match = re.match(r'^\*?\s*Front:\s*(.*)', line, re.I)
        if front_match:
            q = front_match.group(1).strip()
            continue

        # Match back
        back_match = re.match(r'^\*?\s*Back:\s*(.*)', line, re.I)
        if back_match:
            a = back_match.group(1).strip()
            if q and a:
                flashcards.append((q, a))
            q, a = None, None

    return flashcards

def render_flashcards(flashcards):
    """
    Render flashcards with flipping effect.
    Cards auto-adjust to rows.
    """
    if not flashcards:
        st.write("No valid flashcards to display.")
        return

    cards_html = ""
    for q, a in flashcards:
        cards_html += f"""
        <div class="flashcard">
            <div class="flashcard-inner">
                <div class="flashcard-front">{q}</div>
                <div class="flashcard-back">{a}</div>
            </div>
        </div>
        """

    html_code = f"""
    <style>
    .flashcards-container {{
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        justify-content: flex-start;
    }}
    .flashcard {{
        width: 30%;
        min-width: 200px;
        perspective: 1000px;
        cursor: pointer;
        min-height: 150px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
    }}
    .flashcard-inner {{
        position: relative;
        width: 100%;
        height: 100%;
        transition: transform 0.6s;
        transform-style: preserve-3d;
        border-radius: 12px;
    }}
    .flashcard.flipped .flashcard-inner {{
        transform: rotateY(180deg);
    }}
    .flashcard-front, .flashcard-back {{
        position: absolute;
        top:0; left:0; right:0; bottom:0;
        backface-visibility: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 15px;
        font-family: "Times New Roman", serif;
        font-size: 18px;
        text-align: center;
        word-wrap: break-word;
        border-radius: 12px;
        overflow: hidden;
    }}
    .flashcard-front {{
        background-color: #111;
        color: white;
    }}
    .flashcard-back {{
        background-color: #222;
        color: #fff;
        transform: rotateY(180deg);
    }}
    </style>

    <div class="flashcards-container">
        {cards_html}
    </div>

    <script>
    const cards = document.querySelectorAll('.flashcard');
    cards.forEach(card => {{
        card.addEventListener('click', () => {{
            card.classList.toggle('flipped');
        }});
    }});
    </script>
    """

    components.html(html_code, height=600, scrolling=True)




# -------------------- HOME PAGE --------------------
if st.session_state.page == "home":
    set_bg_image("generated-image.png")
    # Centered Title and Subtitle with minimal spacing
    st.markdown(
        """
        <div style="
            display: flex; 
            flex-direction: column; 
            justify-content: center; 
            align-items: center; 
            height: 50vh;   /* reduce vh if you want less vertical space */
            margin-bottom: 0px;
            gap: 0px;
        ">
            <h1 style='font-size: 60px; margin-bottom:10px; line-height:1;'>Lecture to Notes</h1>
            <p style='font-size: 20px; max-width: 600px; margin-bottom:20px; line-height:1.2;'>
               Welcome! This website allows you to transcribe audio or video content into text, generate summaries, and create interactive flashcards using Generative AI. Enhance your learning, test knowledge, and reinforce understanding with ease
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Add custom CSS for green button and remove margin
    st.markdown(
        """
        <style>
        div.stButton > button {
            background-color: #04AA6D;
            color: white;
            border: none;
            padding: 0.8em 2.5em;
            border-radius: 8px;
            font-size: 20px;
            transition: background 0.2s;
            margin-top: 0px !important;
            margin-bottom: 0px !important;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        div.stButton > button:hover {
            background-color: #038e57;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True
    )
    cols = st.columns([3, 2, 3]) # adjust ratio for desired width
    with cols[1]:
        if st.button("Start Voice to Text", key="start_voicetotext_click", help="Click to go to Voice to Text page"):
            go_voicetotext()
            st.rerun()


# -------------------- VOICE TO TEXT PAGE --------------------
elif st.session_state.page == "voicetotext":
    set_bg_image("generated-image.png")
    st.markdown(
        "<div style='background-color:black; padding:20px;'>"
        "<h1 style='color:white;'>Voice to Text</h1></div>",
        unsafe_allow_html=True
    )

    # Center the "Back to Home" button
    cols = st.columns([3, 2, 3])
    with cols[1]:
        if st.button("Back to Home"):
            go_home()
            st.rerun()
    uploaded_file = None
    transcription = ""
    flashcards = ""
    summary = ""
    uploaded_file = st.file_uploader("Choose audio/video file", type=["wav", "mp3", "mp4", "mov", "m4a", "ogg", "flac"])
    # Clear previous transcription, summary, flashcards when a new file is uploaded
    if uploaded_file is not None:
        if 'last_uploaded_file_id' not in st.session_state or st.session_state.last_uploaded_file_id != uploaded_file.name:
            # New file uploaded (different file name from last)
            st.session_state.last_uploaded_file_id = uploaded_file.name
            st.session_state.transcription = ""
            st.session_state.summary = ""
            st.session_state.flashcards = ""

    # Center the "Transcribe" button
    cols = st.columns([3, 2, 3])
    with cols[1]:
        transcribe_clicked = st.button("Transcribe")

    if transcribe_clicked:
        if not uploaded_file:
            st.warning("Please upload a file first!")
        else:
            tmp = save_uploaded_file(uploaded_file)
            wav = extract_audio_to_wav(tmp)
            with st.spinner("Transcribing..."):
                transcription = clean_text(call_gemini_transcribe(wav))
            st.success("Transcription ready!")
            os.remove(tmp)
            os.remove(wav)
            st.session_state.transcription = transcription # Save to session state
    else:
        transcription = st.session_state.get("transcription", "")

    if transcription:
        st.markdown("### Transcription")
        st.write(transcription)
        pdf_bytes = make_pdf_bytes("Transcribe",transcription )
        cols = st.columns(3)
        with cols[1]:
            st.download_button("Download Transcribe", data=pdf_bytes, file_name="transcribe.pdf", mime="application/pdf")
        cols = st.columns(3)
        # Buttons side by side for Summary and Flashcards
        with cols[0]:
            summary_clicked = st.button("Generate Summary")
        with cols[2]:
            flashcard_clicked = st.button("Generate Flashcards")

        if summary_clicked:
            with st.spinner("Generating Summary..."):
                summary = clean_text(call_gemini_text(f"Summarize the following content:\n\n{transcription}"))
            st.success("Summary generated!")
            st.session_state.summary = summary
        else:
            summary = st.session_state.get("summary", "")

        if flashcard_clicked:
            with st.spinner("Generating Flashcards..."):
                flashcards = clean_text(call_gemini_text(f"Create flashcards from the following content:\n\n{transcription}"))
            st.success("Flashcards generated!")
            st.session_state.flashcards = flashcards
        else:
            flashcards = st.session_state.get("flashcards", "")

    if summary:
        st.markdown("### Summary")
        st.write(summary)
        pdf_bytes = make_pdf_bytes("Summary", summary)
        cols = st.columns([3, 2, 3])
        with cols[1]:
            st.download_button("Download Summary", data=pdf_bytes, file_name="summary.pdf", mime="application/pdf")

    if flashcards:
        st.markdown("### Flashcards")
        st.markdown("### Tap on the cards to flip them.")
        cards = parse_flashcards_text(flashcards)
        if cards:
            render_flashcards(cards)
            
            # Add CSS to reduce margin/padding around download button
            st.markdown(
                """
                <style>
                div.stDownloadButton > button {
                    margin-top: 0.2rem !important;
                    margin-bottom: 0.2rem !important;
                    padding-top: 0.3rem !important;
                    padding-bottom: 0.3rem !important;
                }
                </style>
                """, unsafe_allow_html=True
            )
        else:
            st.write("No valid flashcards found to display.")

