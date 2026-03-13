from groq import Groq
from backend.app.core.config import GROQ_API_KEY, LLM_MODEL


class ReportGenerator:

    @staticmethod
    def generate_report(
        metadata_result,
        tampering_result,
        ocr_result,
        risk_result
    ):

        client = Groq(api_key=GROQ_API_KEY)

        prompt = f"""
        You are a fraud detection analyst.

        Analyze the following document inspection results and generate a structured fraud risk report.

        Metadata Analysis:
        {metadata_result}

        Tampering Analysis:
        {tampering_result}

        OCR Analysis:
        {ocr_result}

        Risk Assessment:
        {risk_result}

        Generate a structured report with these sections:

        1. Document Inspection Summary
        2. Key Fraud Signals
        3. Risk Assessment
        4. Final Conclusion (Genuine / Suspicious)

        Keep the explanation concise and professional.
        """

        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert document fraud analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        report_text = response.choices[0].message.content

        return report_text