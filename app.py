import streamlit as st
import requests
import time

from factcheck.pdf_extractor import extract_text_from_pdf
from image_audit.image_analyzer import analyze_image

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="VeritasAI",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Main background */
.stApp {
    background: #0b1020;
    color: #f5f7ff;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #080d1a;
    border-right: 1px solid #20283d;
}

[data-testid="stSidebar"] * {
    color: #e8ecf8;
}

/* Main container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* Headings */
h1 {
    font-size: 42px !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
}

h2 {
    font-size: 28px !important;
}

h3 {
    font-size: 20px !important;
}

/* Logo */
.logo-box {
    padding: 10px 0 25px 0;
}

.logo-title {
    font-size: 25px;
    font-weight: 800;
}

.logo-subtitle {
    color: #8f9bb5;
    font-size: 12px;
    margin-top: -5px;
}

/* Hero */
.hero {
    background: linear-gradient(
        135deg,
        #111a35 0%,
        #10162a 50%,
        #0d1428 100%
    );
    border: 1px solid #273353;
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 25px;
}

.hero-small {
    color: #8f9bb5;
    font-size: 15px;
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero-description {
    color: #aeb8cf;
    font-size: 16px;
}

/* Cards */
.metric-card {
    background: #11182b;
    border: 1px solid #26314b;
    border-radius: 16px;
    padding: 20px;
    min-height: 120px;
}

.metric-label {
    color: #8f9bb5;
    font-size: 13px;
}

.metric-value {
    font-size: 30px;
    font-weight: 800;
    margin-top: 7px;
}

.metric-description {
    color: #7e8aa5;
    font-size: 12px;
}

/* Section */
.section-title {
    font-size: 22px;
    font-weight: 700;
    margin-top: 28px;
    margin-bottom: 15px;
}

/* Agent cards */
.agent-card {
    background: #11182b;
    border: 1px solid #29344e;
    border-radius: 14px;
    padding: 18px;
    text-align: center;
}

.agent-icon {
    font-size: 28px;
}

.agent-name {
    font-weight: 700;
    margin-top: 8px;
}

.agent-status {
    color: #67e8a5;
    font-size: 12px;
    margin-top: 5px;
}

/* Input */
textarea {
    background: #0f1629 !important;
    color: white !important;
    border: 1px solid #34415f !important;
    border-radius: 12px !important;
}

/* Buttons */
.stButton > button {
    background: #4f7cff;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 25px;
    font-weight: 700;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #6b91ff;
    border: none;
}

/* Evidence cards */
.evidence-card {
    background: #10172a;
    border: 1px solid #27334e;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 12px;
}

.evidence-title {
    font-size: 16px;
    font-weight: 700;
}

.evidence-source {
    color: #7f8ba7;
    font-size: 12px;
}

.evidence-text {
    color: #b8c2d8;
    font-size: 14px;
    margin-top: 10px;
}

/* Verdict */
.verdict-supported {
    background: rgba(34, 197, 94, 0.12);
    border: 1px solid rgba(34, 197, 94, 0.35);
    color: #67e8a5;
    padding: 18px;
    border-radius: 14px;
    font-size: 25px;
    font-weight: 800;
}

.verdict-contradicted {
    background: rgba(239, 68, 68, 0.12);
    border: 1px solid rgba(239, 68, 68, 0.35);
    color: #ff8585;
    padding: 18px;
    border-radius: 14px;
    font-size: 25px;
    font-weight: 800;
}

.verdict-warning {
    background: rgba(234, 179, 8, 0.12);
    border: 1px solid rgba(234, 179, 8, 0.35);
    color: #facc15;
    padding: 18px;
    border-radius: 14px;
    font-size: 25px;
    font-weight: 800;
}

/* Info box */
.info-box {
    background: #11182b;
    border: 1px solid #27334d;
    border-radius: 14px;
    padding: 18px;
    color: #aeb8cf;
}

/* Footer */
.footer {
    text-align: center;
    color: #59657e;
    font-size: 12px;
    padding: 30px 0 10px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.markdown("""
    <div class="logo-box">
        <div class="logo-title">🔎 VERITAS<span style="color:#4f7cff">AI</span></div>
        <div class="logo-subtitle">
            Evidence Intelligence Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🔎 Verify Claim",
            "📄 Document Audit",
            "🖼️ Image Audit",
            "🤖 Agent Activity",
            "📚 Evidence Explorer"
        ]
    )

    st.markdown("---")

    st.markdown("""
    <div class="info-box">
        <b>System Status</b><br><br>
        🟢 Backend Online<br>
        🟢 Evidence Search Ready<br>
        🟢 AI Pipeline Ready
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

if page == "🏠 Dashboard":

    st.markdown("""
    <div class="hero">
        <div class="hero-small">AUTONOMOUS AI VERIFICATION</div>
        <div class="hero-title">VeritasAI</div>
        <div class="hero-description">
            Multimodal fact-checking and deepfake audit platform
            powered by evidence retrieval and AI agents.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Verification Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">VERIFICATION ENGINE</div>
            <div class="metric-value">AI</div>
            <div class="metric-description">Evidence-based analysis</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">LIVE EVIDENCE</div>
            <div class="metric-value">WEB</div>
            <div class="metric-description">Real-time source retrieval</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">AGENTS</div>
            <div class="metric-value">3</div>
            <div class="metric-description">Research → Retrieve → Verify</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">MODALITIES</div>
            <div class="metric-value">3</div>
            <div class="metric-description">Text • PDF • Image</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">AI Agent Pipeline</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="agent-card">
            <div class="agent-icon">🧠</div>
            <div class="agent-name">Researcher Agent</div>
            <div class="agent-status">● READY</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="agent-card">
            <div class="agent-icon">🔍</div>
            <div class="agent-name">Retriever Agent</div>
            <div class="agent-status">● READY</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="agent-card">
            <div class="agent-icon">⚖️</div>
            <div class="agent-name">Fact-Checker Agent</div>
            <div class="agent-status">● READY</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">How VeritasAI Works</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="info-box">

    <b>01 — Input</b><br>
    Claim, document or image is submitted.

    <br><br>

    <b>02 — Investigation</b><br>
    AI agents research the content and retrieve supporting evidence.

    <br><br>

    <b>03 — Evidence Analysis</b><br>
    Retrieved sources are compared against the submitted claim.

    <br><br>

    <b>04 — Audit Result</b><br>
    VeritasAI presents the assessment, confidence and evidence.

    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# VERIFY CLAIM
# ---------------------------------------------------------

elif page == "🔎 Verify Claim":

    st.markdown("""
    <div class="hero">
        <div class="hero-small">TEXT VERIFICATION</div>
        <div class="hero-title">Verify a Claim</div>
        <div class="hero-description">
            Submit a factual statement and let VeritasAI
            investigate it using live evidence.
        </div>
    </div>
    """, unsafe_allow_html=True)

    claim = st.text_area(
        "Claim / News Statement",
        placeholder="Example: The Earth revolves around the Sun and takes approximately 365 days to complete one orbit.",
        height=150
    )

    if st.button("🔍 Verify Claim", use_container_width=True):

        if not claim.strip():

            st.warning("Please enter a claim first.")

        else:

            with st.spinner("AI agents are investigating the claim..."):

                try:

                    response = requests.post(
                        "http://127.0.0.1:8000/api/factcheck/verify",
                        json={"claim": claim},
                        timeout=60
                    )

                    if response.status_code == 200:

                        result = response.json()
                        st.session_state["last_result"] = result

                        st.success("Verification completed")

                        # -------------------------------------
                        # AI AGENT EXECUTION
                        # -------------------------------------

                        st.markdown(
                          '<div class="section-title">🤖 AI Agent Investigation</div>',
                           unsafe_allow_html=True
                        )

                        agent_col1, agent_col2, agent_col3 = st.columns(3)
 
                        with agent_col1:
                             st.markdown("""
                             <div class="agent-card">
                                 <div class="agent-icon">🧠</div>
                                 <div class="agent-name">Researcher</div>
                                 <div class="agent-status">● COMPLETED</div>
                             </div>
                             """, unsafe_allow_html=True)

                        with agent_col2:
                             st.markdown("""
                             <div class="agent-card">
                                 <div class="agent-icon">🔍</div>
                                 <div class="agent-name">Retriever</div>
                                 <div class="agent-status">● COMPLETED</div>
                             </div>
                             """, unsafe_allow_html=True)

                        with agent_col3:
                             st.markdown("""
                             <div class="agent-card">
                                 <div class="agent-icon">⚖️</div>
                                 <div class="agent-name">Fact Checker</div>
                                 <div class="agent-status">● COMPLETED</div>
                             </div>
                             """, unsafe_allow_html=True)
                        # -------------------------------------
                        # CLAIM DECOMPOSITION
                        # -------------------------------------

                        claims = result.get("claims", [])

                        if claims:

                         st.markdown(
                             '<div class="section-title">🧩 Claim Decomposition</div>',
                             unsafe_allow_html=True
                         )

                         st.caption(
                             "The Claim Decomposition Agent breaks complex statements "
                             "into independently verifiable claims."
                         )

                         for index, claim_item in enumerate(claims, start=1):

                             individual_claim = claim_item.get(
                               "claim",
                               ""
                             )

                             assessment = claim_item.get(
                               "assessment",
                               {}
                             )

                             individual_verdict = assessment.get(
                               "verdict",
                               "Not assessed"
                             )

                             individual_confidence = assessment.get(
                               "confidence"
                             )

                             with st.expander(
                               f"Claim {index}: {individual_claim}",
                               expanded=True
                             ):

                               col_a, col_b = st.columns(2)

                               with col_a:
                                  st.write("**Claim:**")
                                  st.write(individual_claim)

                               with col_b:

                                  st.write("**Assessment:**")

                                  if individual_verdict.lower() == "supported":

                                    st.success(
                                      f"✅ {individual_verdict}"
                                    )

                                  elif individual_verdict.lower() == "contradicted":

                                    st.error(
                                      f"❌ {individual_verdict}"
                                    )

                                  else:

                                    st.warning(
                                      f"⚠️ {individual_verdict}"
                                    )

                                  if individual_confidence is not None:

                                    st.write(
                                      f"Confidence: **{individual_confidence:.0f}%**"
                                    )

                        # -------------------------------------
                        # RESULT
                        # -------------------------------------

                        st.markdown(
                            '<div class="section-title">Verification Result</div>',
                            unsafe_allow_html=True
                        )

                        verdict = result.get(
                            "verdict",
                            "Unknown"
                        )

                        confidence = result.get(
                            "confidence"
                        )

                        if verdict.lower() == "supported":

                            st.markdown(
                                f"""
                                <div class="verdict-supported">
                                ✅ {verdict.upper()}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        elif verdict.lower() == "contradicted":

                            st.markdown(
                                f"""
                                <div class="verdict-contradicted">
                                ❌ {verdict.upper()}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        else:

                            st.markdown(
                                f"""
                                <div class="verdict-warning">
                                ⚠️ {verdict.upper()}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        st.markdown("")

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric(
                                "Confidence",
                                f"{confidence:.0f}%"
                                if confidence is not None
                                else "N/A"
                            )

                        with col2:
                            evidence_count = len(
                                result.get("evidence", [])
                            )

                            st.metric(
                                "Sources Retrieved",
                                evidence_count
                            )

                        with col3:
                            claims = result.get("claims", [])

                            st.metric(
                                "Claims Analyzed",
                                len(claims)
                                if claims
                                else 1
                            )

                        # -------------------------------------
                        # CLAIM
                        # -------------------------------------

                        st.markdown(
                            '<div class="section-title">Submitted Claim</div>',
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f"""
                            <div class="info-box">
                            {result.get("claim", claim)}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        # -------------------------------------
                        # EXPLANATION
                        # -------------------------------------

                        st.markdown(
                            '<div class="section-title">AI Explanation</div>',
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f"""
                            <div class="info-box">
                            {result.get(
                                "explanation",
                                "No explanation available."
                            )}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        # -------------------------------------
                        # EVIDENCE
                        # -------------------------------------

                        st.markdown(
                            '<div class="section-title">📚 Evidence Explorer</div>',
                            unsafe_allow_html=True
                        )

                        evidence = result.get(
                            "evidence",
                            []
                        )

                        if evidence:

                            for index, item in enumerate(
                                evidence,
                                start=1
                            ):

                                title = item.get(
                                    "title",
                                    "Unknown Source"
                                )

                                url = item.get(
                                    "url"
                                )

                                snippet = item.get(
                                    "snippet",
                                    "No evidence text available."
                                )

                                with st.expander(
                                   f"📄 Source {index} — {title}"
                                ):

                                   st.write(
                                     "**Source:**",
                                     title
                                   )

                                   if url:
                                     st.write(
                                        "**URL:**",
                                        url
                                     )

                                   # -------------------------------------
                                   # SOURCE QUALITY
                                   # -------------------------------------

                                   quality = item.get(
                                     "quality",
                                     "Unknown"
                                   ) 

                                   quality_reason = item.get(
                                     "quality_reason",
                                     "No quality assessment available."
                                   )

                                   source_type = item.get(
                                     "source_type",
                                     "Unknown"
                                   )

                                   st.write(
                                     f"**Source Quality:** {quality}"
                                   )

                                   st.caption(
                                     f"{source_type} — {quality_reason}"
                                   )

                                   st.write(
                                     "**Evidence:**"
                                   )

                                   st.write(snippet)

                        else:

                            st.warning(
                                "No evidence was retrieved."
                            )

                        # -------------------------------------
                        # RESEARCH
                        # -------------------------------------

                        st.markdown(
                            '<div class="section-title">🤖 Agent Research</div>',
                            unsafe_allow_html=True
                        )

                        research = result.get(
                            "research",
                            {}
                        )

                        st.markdown(
                            f"""
                            <div class="info-box">

                            <b>Research Query</b><br>
                            {research.get(
                                "research_query",
                                "N/A"
                            )}

                            <br><br>

                            <b>Research Task</b><br>
                            {research.get(
                                "task",
                                "N/A"
                            )}

                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    else:

                        st.error(
                            f"Backend returned error: {response.status_code}"
                        )

                        try:
                            st.json(response.json())
                        except Exception:
                            st.write(response.text)

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Cannot connect to FastAPI. "
                        "Make sure the backend terminal is running."
                    )

                except requests.exceptions.Timeout:

                    st.error(
                        "The request took too long. Please try again."
                    )

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )


# ---------------------------------------------------------
# DOCUMENT AUDIT
# ---------------------------------------------------------

elif page == "📄 Document Audit":

    st.markdown("""
    <div class="hero">
        <div class="hero-small">DOCUMENT ANALYSIS</div>
        <div class="hero-title">Document Audit</div>
        <div class="hero-description">
            Upload a PDF and analyze factual claims using
            the VeritasAI evidence pipeline.
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload PDF document",
        type=["pdf"]
    )

    if uploaded_file:

        st.success(
          f"File uploaded: {uploaded_file.name}"
        )

        # Save uploaded PDF temporarily
        temp_pdf_path = "temp_uploaded.pdf"

        with open(temp_pdf_path, "wb") as file:
          file.write(uploaded_file.getbuffer())

        # Extract text from PDF
        pdf_text = extract_text_from_pdf(
          temp_pdf_path
        )

        if pdf_text:

          st.markdown(
             '<div class="section-title">📄 Extracted Text</div>',
             unsafe_allow_html=True
          )

          st.text_area(
             "PDF Content",
             pdf_text,
             height=400
          )

          # -------------------------------------
          # VERIFY PDF CONTENT
          # -------------------------------------

          if st.button(
             "🔍 Verify PDF Content",
             use_container_width=True
          ):

             with st.spinner(
                 "VeritasAI is analyzing the PDF..."
             ):

                 try:

                    response = requests.post(
                        "http://127.0.0.1:8000/api/factcheck/verify",
                        json={
                            "claim": pdf_text[:5000]
                        },
                        timeout=60
                    )

                    if response.status_code == 200:

                       pdf_result = response.json()

                       st.success(
                          "PDF analysis completed"
                       )

                       st.markdown(
                          '<div class="section-title">📊 PDF Verification Result</div>',
                          unsafe_allow_html=True
                       )

                       st.write(
                          "**Verdict:**",
                          pdf_result.get(
                             "verdict",
                             "Unknown"
                          )
                       )

                       st.write(
                          "**Confidence:**",
                          pdf_result.get(
                              "confidence",
                              "N/A"
                          )
                       )

                       st.write(
                          "**Explanation:**"
                       )

                       st.write(
                          pdf_result.get(
                             "explanation",
                             "No explanation available."
                          )
                       )

                    else:

                       st.error(
                          f"Backend returned error: "
                          f"{response.status_code}"
                       )

                 except requests.exceptions.ConnectionError:

                    st.error(
                      "Cannot connect to FastAPI. "
                      "Make sure the backend terminal is running."
                    ) 

                 except requests.exceptions.Timeout:

                    st.error(
                      "The PDF analysis took too long."
                    )

        else:

           st.warning(
             "No readable text was found in this PDF."
           )

    else:

        st.markdown("""
        <div class="info-box">
        📄 Upload a research paper, report or news document
        to begin document verification.
        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------
# IMAGE AUDIT
# ---------------------------------------------------------

elif page == "🖼️ Image Audit":

    st.markdown("""
    <div class="hero">
        <div class="hero-small">MEDIA FORENSICS</div>
        <div class="hero-title">Image Audit</div>
        <div class="hero-description">
            Inspect image characteristics and forensic indicators
            associated with possible manipulation.
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_image = st.file_uploader(
        "Upload image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_image:

        st.image(
            uploaded_image,
            caption="Uploaded Image",
            use_container_width=True
        )

        if uploaded_image:

           st.success(
              f"Image uploaded: {uploaded_image.name}"
           )

           st.image(
              uploaded_image,
              caption="Uploaded Image",
              use_container_width=True
           )

           # Save image temporarily
           temp_image_path = "temp_uploaded_image"

           with open(temp_image_path, "wb") as file:
              file.write(uploaded_image.getbuffer())

           # -------------------------------------
           # ANALYZE IMAGE
           # -------------------------------------

           if st.button(
               "🔍 Analyze Image",
               use_container_width=True
           ):

               with st.spinner(
                    "VeritasAI is analyzing the image..."
               ):

                    result = analyze_image(
                       temp_image_path
                    )

               if result["success"]:

                  st.success(
                      "Image analysis completed"
                  )

                  st.markdown(
                      '<div class="section-title">🧪 Image Forensic Report</div>',
                      unsafe_allow_html=True
                  )

                  col1, col2, col3, col4 = st.columns(4)

                  with col1:
                      st.metric(
                         "Width",
                         f'{result["width"]} px'
                      )

                  with col2: 
                      st.metric(
                         "Height",
                         f'{result["height"]} px'
                      )

                  with col3:
                      st.metric(
                         "Format",
                         result["format"]
                      )

                  with col4:
                      st.metric(
                         "File Size",
                         f'{result["file_size_kb"]} KB'
                      )

                  st.write(
                     "**Color Mode:**",
                     result["color_mode"]
                  )

                  st.markdown(
                     "### 🔎 Forensic Indicators"
                  )

                  for indicator in result["indicators"]:

                     st.write(
                         f'**{indicator["name"]}:** '
                         f'{indicator["result"]}'
                     )

                  st.markdown(
                      "### 🧪 What VeritasAI Checked"
                  )

                  checks = [
                    "EXIF metadata",
                    "Image format and dimensions",
                    "Brightness characteristics",
                    "Pixel/noise variation",
                    "Edge activity"
                  ]

                  for check in checks:
                      st.write(f"✓ {check}")

                  st.caption(
                    "These checks provide forensic signals for review. "
                    "They do not by themselves determine whether an image "
                    "is authentic, edited, or AI-generated."
                  )

                  st.info(
                     result["warning"]
                  )

                  if result["metadata"]:

                     st.markdown(
                         "### 📋 Image Metadata"
                     )

                     st.json(
                         result["metadata"]
                     )

               else:

                    st.error(
                       f'Image analysis failed: '
                       f'{result["error"]}'
                    )

        else: 

           st.info(
              "Upload an image to begin forensic analysis."
           )

    else:

        st.markdown("""
        <div class="info-box">
        🖼️ Upload an image to begin forensic inspection.
        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------
# AUDIO AUDIT
# ---------------------------------------------------------

elif page == "🎙️ Audio Audit":

    st.markdown("""
    <div class="hero">
        <div class="hero-small">AUDIO FORENSICS</div>
        <div class="hero-title">Audio Audit</div>
        <div class="hero-description">
            Analyze speech characteristics and audio forensic
            indicators for potential synthetic-media signals.
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_audio = st.file_uploader(
        "Upload audio",
        type=["wav", "mp3", "ogg", "m4a"]
    )

    if uploaded_audio:

        st.audio(
            uploaded_audio
        )

        st.info(
            "Audio forensic analysis module will be connected "
            "after the core verification features are complete."
        )

    else:

        st.markdown("""
        <div class="info-box">
        🎙️ Upload a voice recording for audio forensic analysis.
        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------
# AGENT ACTIVITY
# ---------------------------------------------------------

elif page == "🤖 Agent Activity":

    st.markdown("""
    <div class="hero">
        <div class="hero-small">MULTI-AGENT SYSTEM</div>
        <div class="hero-title">Agent Activity</div>
        <div class="hero-description">
            Observe how VeritasAI moves from research to evidence
            and final assessment.
        </div>
    </div>
    """, unsafe_allow_html=True)

    agents = [
       ("🧠", "Researcher Agent",
        "Analyzes the submitted claim and creates a research task."),

       ("🔍", "Retriever Agent",
        "Searches for relevant web evidence supporting or contradicting the claim."),

       ("⚖️", "Fact-Checker Agent",
        "Compares the claim against retrieved evidence and produces an assessment.")
    ]

    for icon, name, description in agents:

        st.markdown(
            f"""
            <div class="evidence-card">

                <div style="font-size:30px;">
                    {icon}
                </div>

                <div class="evidence-title">
                    {name}
                </div>

                <div class="evidence-text">
                    {description}
                </div>

                <div class="agent-status">
                    ● READY
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ---------------------------------------------------------
# EVIDENCE EXPLORER
# ---------------------------------------------------------

elif page == "📚 Evidence Explorer":

    st.markdown("""
    <div class="hero">
        <div class="hero-small">SOURCE INTELLIGENCE</div>
        <div class="hero-title">Evidence Explorer</div>
        <div class="hero-description">
            Explore the evidence retrieved during verification.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "last_result" not in st.session_state:

        st.info(
            "Run a verification from the Verify Claim page "
            "to populate evidence."
        )

    else:

        result = st.session_state["last_result"]

        evidence = result.get("evidence", [])

        if not evidence:

            st.warning(
                "No evidence was retrieved for the latest verification."
            )

        else:

            st.markdown("### 🔎 Retrieved Evidence")

            st.caption(
                f"{len(evidence)} source(s) retrieved during verification."
            )

            for index, item in enumerate(evidence, start=1):

                title = item.get(
                    "title",
                    "Untitled source"
                )

                url = item.get("url")

                snippet = item.get(
                    "snippet",
                    "No evidence text available."
                )

                quality = item.get(
                    "quality",
                    "Unknown"
                )

                source_type = item.get(
                    "source_type",
                    "Unknown"
                )

                quality_reason = item.get(
                    "quality_reason",
                    "No quality assessment available."
                )

                with st.expander(
                    f"📄 Source {index} — {title}"
                ):

                    st.write(
                        "**Source:**",
                        title
                    )

                    if url:
                        st.write(
                            "**URL:**",
                            url
                        )

                    st.write(
                        f"**Source Quality:** {quality}"
                    )

                    st.caption(
                        f"{source_type} — {quality_reason}"
                    )

                    st.write("**Evidence:**")

                    st.write(snippet)
# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("""
<div class="footer">
    VeritasAI • Autonomous Multimodal Fact-Checking & Deepfake Audit Platform
    <br>
    Evidence-based analysis • AI-assisted verification • Human review recommended
</div>
""", unsafe_allow_html=True)