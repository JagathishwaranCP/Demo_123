
import streamlit as st

from chatbot import financial_chatbot
from fraud_analyzer import analyze_report
from utils.pdf_reader import extract_text_from_pdf


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="FinIntelligence AI",
    page_icon="🏦",
    layout="wide"
)


# ==========================================
# APPLICATION HEADER
# ==========================================

st.title("🏦 FinIntelligence AI")

st.caption(
    "AI-Powered Financial Advisory and Fraud Monitoring System"
)


# ==========================================
# SESSION STATE
# ==========================================

if "history" not in st.session_state:
    st.session_state.history = []

if "report_text" not in st.session_state:
    st.session_state.report_text = None

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("FinIntelligence AI")

page = st.sidebar.radio(
    "Choose Application",
    [
        "Financial Advisor",
        "Fraud Report Analyzer"
    ]
)


# ==========================================
# BOT 1: FINANCIAL ADVISOR
# ==========================================

if page == "Financial Advisor":

    st.header("🤖 AI Financial Advisor")

    st.write(
        "Ask questions about banking, savings, "
        "loans, mutual funds and investments."
    )

    for message in st.session_state.history:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        "Ask your financial question..."
    )

    if question:

        with st.chat_message("user"):
            st.markdown(question)

        try:

            with st.spinner("AI is preparing your answer..."):

                answer = financial_chatbot(
                    question,
                    st.session_state.history
                )

            st.session_state.history.extend([
                {
                    "role": "user",
                    "content": question
                },
                {
                    "role": "assistant",
                    "content": answer
                }
            ])

            st.rerun()

        except Exception as error:

            st.error(f"Chatbot Error: {error}")

    if st.sidebar.button("Clear Chat"):

        st.session_state.history = []
        st.rerun()


# ==========================================
# BOT 2: FRAUD REPORT ANALYZER
# ==========================================

elif page == "Fraud Report Analyzer":

    st.header("🔍 Financial Fraud Report Analyzer")

    st.write(
        "Upload a financial report in PDF format "
        "to identify potential suspicious indicators."
    )

    uploaded_file = st.file_uploader(
        "Upload Financial Report",
        type=["pdf"],
        max_upload_size=10
    )

    if uploaded_file:

        # Check whether a new PDF was uploaded

        if (
            st.session_state.uploaded_filename
            != uploaded_file.name
        ):

            st.session_state.report_text = None
            st.session_state.analysis_result = None

            st.session_state.uploaded_filename = (
                uploaded_file.name
            )

        try:

            # Extract PDF text only once

            if st.session_state.report_text is None:

                with st.spinner("Extracting PDF text..."):

                    report = extract_text_from_pdf(
                        uploaded_file
                    )

                if not report or not report.strip():

                    st.warning(
                        "No readable text found. "
                        "Scanned PDFs require OCR."
                    )

                else:

                    st.session_state.report_text = report

                    st.success(
                        "PDF uploaded and text extracted successfully!"
                    )

            # Display extracted report

            if st.session_state.report_text:

                report = st.session_state.report_text

                st.subheader("📄 Extracted Report")

                with st.expander("View Report Text"):

                    st.text_area(
                        "Extracted Content",
                        report,
                        height=250,
                        disabled=True
                    )

                st.info(
                    f"Extracted characters: {len(report):,}"
                )

                if st.button(
                    "Analyze Financial Report",
                    type="primary"
                ):

                    try:

                        with st.spinner(
                            "AI is analyzing the financial report..."
                        ):

                            result = analyze_report(report)

                        # Save the result as a STRING

                        if not isinstance(result, str):

                            raise TypeError(
                                "analyze_report() must return a string. "
                                "Check fraud_analyzer.py."
                            )

                        st.session_state.analysis_result = result

                        st.success(
                            "Financial report analysis completed!"
                        )

                    except Exception as error:

                        st.error(
                            f"Analysis Error: {error}"
                        )

                # Display analysis result

                if st.session_state.analysis_result:

                    st.divider()

                    st.subheader("📊 Analysis Results")

                    # IMPORTANT:
                    # analyze_report returns a STRING.
                    # Do not use result.get() here.

                    st.markdown(
                        st.session_state.analysis_result
                    )

                    st.divider()

                    st.warning(
                        """
                        AI-generated preliminary assessment only.
                        Unusual transactions do not prove fraud.
                        Verify all findings using original records
                        and qualified human investigation.
                        """
                    )

                    # Download analysis

                    st.download_button(
                        label="⬇️ Download Analysis Report",
                        data=st.session_state.analysis_result,
                        file_name="financial_fraud_analysis.txt",
                        mime="text/plain"
                    )

        except Exception as error:

            st.error(
                f"Report processing error: {error}"
            )

    else:

        st.info(
            "Upload a PDF financial report to begin analysis."
        )


# ==========================================
# FOOTER
# ==========================================

st.sidebar.divider()

st.sidebar.caption(
    "FinIntelligence AI | Powered by Groq"
)

st.sidebar.caption(
    "Educational NLP Project"
)
