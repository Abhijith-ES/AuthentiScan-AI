from typing import Dict, Any


class RiskScorer:

    @staticmethod
    def calculate_risk(
        metadata_result: Dict[str, Any],
        tampering_result: Dict[str, Any],
        ocr_result: Dict[str, Any]
    ) -> Dict[str, Any]:

        risk_score = 0.0
        signals = []

        # Metadata signal
        if metadata_result.get("suspicious"):
            risk_score += 0.25
            signals.append("Editing software detected in metadata")

        # Tampering signal
        if tampering_result.get("suspicious"):
            risk_score += 0.45
            signals.append("Possible image manipulation detected via ELA")

        # OCR signal
        text_length = ocr_result.get("text_length", 0)

        if text_length < 20:
            risk_score += 0.15
            signals.append("Very little text detected in document")

        # Cap score
        risk_score = min(risk_score, 1.0)

        # Risk classification
        if risk_score < 0.3:
            risk_level = "Low"
        elif risk_score < 0.6:
            risk_level = "Medium"
        else:
            risk_level = "High"

        return {
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "fraud_signals": signals
        }