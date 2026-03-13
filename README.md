# AuthentiScan AI

**AuthentiScan AI** is a prototype system that analyzes identity document images and generates a structured **forgery risk report** indicating whether the document appears **genuine or potentially tampered**.

The system combines multiple AI-powered analysis steps including:

- Image validation
- Metadata inspection
- Image tampering detection using ELA (Error Level Analysis)
- OCR-based text extraction
- Risk scoring and fraud signal identification
- LLM-powered fraud report generation

The goal of this prototype is not perfect accuracy but to demonstrate a **clear approach to document fraud detection**, combining multiple AI techniques into a coherent analysis pipeline.

---

# Demo Overview

AuthentiScan AI processes an uploaded ID document and produces:

• Tampering analysis using forensic techniques  
• Metadata inspection results  
• OCR extracted text insights  
• Fraud signals explaining potential risks  
• A structured fraud analysis report  
• A final risk classification (Low / Medium / High)

The results are presented in an **interactive dashboard** that provides:

- Original document preview
- ELA forensic visualization
- Risk assessment summary
- Fraud signal explanations
- Detailed analysis report

---

# System Architecture

The system follows a modular analysis pipeline:

```
User Upload
     │
     ▼
Image Validation
     │
     ▼
Metadata Analysis
     │
     ▼
Tampering Detection (ELA)
     │
     ▼
OCR Text Extraction
     │
     ▼
Risk Scoring Engine
     │
     ▼
LLM Fraud Report Generation
     │
     ▼
Dashboard Visualization
```

Each stage contributes signals that are aggregated to produce the final fraud risk assessment.

---

# Project Structure

```
AuthentiScan-AI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── main.py               # FastAPI entry point exposing the analysis API
│   │   ├── core/
│   │   │   └── config.py             # Environment configuration and project settings
│   │   ├── services/
│   │   │   ├── image_validator.py    # Validates uploaded image format and saves file
│   │   │   ├── metadata_analyzer.py  # Extracts and inspects EXIF metadata
│   │   │   ├── ocr_extractor.py      # Performs OCR text extraction using Tesseract
│   │   │   ├── report_generator.py   # Generates structured fraud report using LLM
│   │   │   ├── risk_scoring.py       # Aggregates signals and computes risk score
│   │   │   └── tampering_detector.py # Detects potential tampering using ELA analysis
│   │   └── utils/
│   │       └── file_cleanup.py       # Removes old uploaded files to prevent storage growth
│   │
│   └── uploads/                     # Temporary storage for uploaded documents
│
├── frontend/
│   ├── index.html                   # Dashboard UI
│   ├── script.js                    # Frontend logic and API communication
│   └── styles.css                   # Dashboard styling
│
├── .env                             # Environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Key Technologies Used

### Backend

- **Python**
- **FastAPI** – API server
- **Tesseract OCR** – Text extraction
- **Pillow / OpenCV** – Image processing
- **Groq LLM API** – Fraud report generation

### Frontend

- HTML
- CSS
- JavaScript
- Markdown rendering for reports

---

# Analysis Components

## 1 Image Validation

Ensures the uploaded file:

- Is a supported image format
- Can be opened safely
- Is stored for analysis

---

## 2 Metadata Analysis

Extracts EXIF metadata and checks for:

- Editing software indicators
- Suspicious metadata patterns
- Metadata inconsistencies

---

## 3 Tampering Detection (ELA)

Error Level Analysis highlights compression differences in the image which may indicate **edited regions or manipulated areas**.

The ELA visualization is displayed alongside the original document.

---

## 4 OCR Extraction

Text is extracted using **Tesseract OCR**.

The extracted text provides:

- Document context
- Text length insights
- Consistency checks for risk scoring

---

## 5 Risk Scoring Engine

Signals from metadata, tampering analysis, and OCR results are combined to produce:

- Fraud signals
- A risk score
- A risk classification

Risk levels:

- **Low**
- **Medium**
- **High**

---

## 6 LLM Fraud Report Generation

A structured fraud analysis report is generated using a large language model.

The report explains:

- Document inspection findings
- Fraud indicators
- Risk reasoning
- Final authenticity assessment

---

# Environment Variables

Create a `.env` file in the project root.

```
GROQ_API_KEY=your_api_key_here
LLM_MODEL=llama-3.3-70b-versatile
```

These are used for generating the fraud analysis report using Groq's LLM API.

---

# Installation

## 1 Clone the repository

```
git clone https://github.com/Abhijith-ES/AuthentiScan-AI.git
cd AuthentiScan-AI
```

---

## 2 Install dependencies

```
pip install -r requirements.txt
```

---

## 3 Install Tesseract OCR

Download and install Tesseract:

https://github.com/tesseract-ocr/tesseract

Ensure it is accessible in your system PATH.

Verify installation:

```
tesseract --version
```

---

# Running the Project

## Start Backend Server

```
uvicorn backend.app.api.main:app --reload
```

Backend API will run at:

```
http://127.0.0.1:8000
```

---

## Start Frontend

Open the frontend dashboard:

```
frontend/index.html
```

Or run:

```
start frontend/index.html
```

---

# Example Workflow

1 Upload identity document  
2 System validates image  
3 Metadata inspection runs  
4 Tampering detection performs ELA analysis  
5 OCR extracts document text  
6 Risk scoring engine evaluates fraud signals  
7 LLM generates structured fraud report  
8 Results displayed in dashboard

---

# Example Output

The dashboard presents:

- Original document
- ELA forensic visualization
- Fraud signals
- Risk score
- Document insights
- Full fraud analysis report

---

# Limitations

This prototype focuses on demonstrating the **approach to fraud detection**, not production-level accuracy.

Limitations include:

- Limited document type awareness
- Basic forensic analysis techniques
- OCR quality dependent on image clarity
- No large-scale dataset training

---

# Future Improvements

Possible extensions include:

- Deep learning based forgery detection
- Document template validation
- Signature and face verification
- Multi-document support
- Confidence scoring models
- Automated dataset training

---

# Author

**E S Abhijith**

Email:  
abhijithsankar.66@gmail.com

GitHub:  
https://github.com/Abhijith-ES

LinkedIn:  
https://www.linkedin.com/in/abhijith-e-s-943a7226a/

---

# License

This project is created for an **AI/ML engineering prototype demonstration** and evaluation task.