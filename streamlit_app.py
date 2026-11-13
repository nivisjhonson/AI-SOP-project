import streamlit as st
from huggingface_hub import InferenceClient
import pdfplumber
from docx import Document
import json

# Hugging Face Client
client = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    token="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"
)

st.title("AI SOP to Checklist Generator")

input_method = st.radio(
    "Choose SOP Input Method",
    ["Text", "PDF", "DOCX"]
)

sop_text = ""

# -------- TEXT INPUT --------
if input_method == "Text":
    sop_text = st.text_area(
        "Enter SOP",
        height=250,
        placeholder="Paste SOP steps or paragraph here..."
    )

# -------- PDF INPUT --------
elif input_method == "PDF":
    pdf_file = st.file_uploader("Upload SOP PDF", type=["pdf"])

    if pdf_file:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    sop_text += text + "\n"

# -------- DOCX INPUT --------
elif input_method == "DOCX":
    docx_file = st.file_uploader("Upload SOP DOCX", type=["docx"])

    if docx_file:
        doc = Document(docx_file)
        for para in doc.paragraphs:
            sop_text += para.text + "\n"

# -------- GENERATE CHECKLIST --------
if st.button("Generate Checklist"):

    if sop_text.strip() == "":
        st.warning("Please provide SOP input.")
        st.stop()

    prompt = f"""
Convert the following SOP into checklist steps.

Return ONLY JSON in this format:

{{
 "checklist":[
   {{"step":1,"task":"task description"}}
 ]
}}

SOP:
{sop_text}
"""

    response = client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.1
    )

    result = response.choices[0].message.content

    try:
        json_data = json.loads(result)

        # -------- PRINT JSON IN TERMINAL --------
        print("\nGenerated Checklist JSON:\n")
        print(json.dumps(json_data, indent=2))

        # -------- SHOW IN STREAMLIT --------
        st.subheader("JSON Output")
        st.json(json_data)

        st.subheader("Checklist")
        for item in json_data["checklist"]:
            st.checkbox(f'{item["step"]}. {item["task"]}')

    except Exception as e:
        st.error("Invalid JSON from model")
        print("Raw Output:", result)