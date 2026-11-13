from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from huggingface_hub import InferenceClient
import pdfplumber
from docx import Document
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AI Model Client
client = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    token="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"
)

# -------- Extract Text From PDF --------
def extract_pdf_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    return text


# -------- Extract Text From DOCX --------
def extract_docx_text(file):
    document = Document(file)
    text = ""
    for para in document.paragraphs:
        text += para.text + "\n"
    return text


# -------- Generate Checklist --------
def generate_checklist(sop_text):

    prompt = f"""
Convert the following SOP into a structured checklist template.
The output MUST be a JSON object with the following structure:
{{
  "templateId": "unique_id_string",
  "title": "Clear Title",
  "sections": [
    {{
      "sectionTitle": "Section Name",
      "questions": [
        {{ "questionId": "q1", "text": "Question text?", "type": "boolean", "required": true }}
      ]
    }}
  ]
}}

SOP:
{sop_text}

Return ONLY valid JSON.
"""

    response = client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
        temperature=0.2
    )

    result = response.choices[0].message.content

    try:
        import re
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return json.loads(result)
    except:
        return {"error": "Invalid JSON returned by model", "raw_output": result}


# -------- Main API Endpoint --------
@app.post("/generate-checklist")
async def generate_checklist_api(
    text: str = Form(None),
    file: UploadFile = File(None)
):

    sop_text = ""

    # If text input is provided
    if text:
        sop_text = text

    # If file uploaded
    if file:

        if file.filename.endswith(".pdf"):
            sop_text = extract_pdf_text(file.file)

        elif file.filename.endswith(".docx"):
            sop_text = extract_docx_text(file.file)

        else:
            return {"error": "Unsupported file type"}

    if sop_text.strip() == "":
        return {"error": "No SOP content provided"}

    checklist_json = generate_checklist(sop_text)

    return checklist_json