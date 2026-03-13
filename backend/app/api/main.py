from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from backend.app.services.image_validator import ImageValidator
from backend.app.services.metadata_analyzer import MetadataAnalyzer
from backend.app.services.tampering_detector import TamperingDetector
from backend.app.services.ocr_extractor import OCRExtractor
from backend.app.services.risk_scoring import RiskScorer
from backend.app.services.report_generator import ReportGenerator
from backend.app.utils.file_cleanup import cleanup_old_files


app = FastAPI(
    title="AuthentiScan AI",
    description="AI-powered ID forgery detection prototype",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="backend/uploads"), name="uploads")


@app.get("/")
def health_check():
    return {"status": "API running"}


@app.post("/analyze-document")
async def analyze_document(file: UploadFile = File(...)):
    validation_result = await ImageValidator.validate_image(file)

    if not validation_result["valid"]:
        return {
            "status": "failed",
            "reason": validation_result["reason"]
        }

    image_path = validation_result["path"]

    metadata_result = MetadataAnalyzer.analyze_metadata(image_path)
    tampering_result = TamperingDetector.run_ela(image_path)
    ocr_result = OCRExtractor.extract_text(image_path)

    risk_result = RiskScorer.calculate_risk(
        metadata_result,
        tampering_result,
        ocr_result
    )

    report_result = ReportGenerator.generate_report(
        metadata_result,
        tampering_result,
        ocr_result,
        risk_result
    )

    fraud_signals = risk_result.get("fraud_signals", [])

    if not fraud_signals:
        fraud_signals = [
            "No metadata anomalies detected",
            "No tampering artifacts detected",
            "OCR extraction completed successfully"
        ]

    ocr_text = ocr_result.get("extracted_text", "")
    document_insights = {
        "ocr_status": "Successful" if ocr_result.get("success") else "Failed",
        "text_length": ocr_result.get("text_length", 0),
        "tampering_score": tampering_result.get("tampering_score", 0),
        "metadata_status": "Suspicious" if metadata_result.get("suspicious") else "Clean"
    }

    cleanup_old_files()

    return {
        "status": "success",
        "image_path": image_path,
        "metadata_analysis": metadata_result,
        "tampering_analysis": tampering_result,
        "ocr_analysis": ocr_result,
        "risk_assessment": risk_result,
        "fraud_report": report_result,
        "fraud_signals": fraud_signals,
        "document_insights": document_insights,
        "ocr_preview": ocr_text[:250]
    }