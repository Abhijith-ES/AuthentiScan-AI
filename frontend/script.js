const uploadArea = document.getElementById("uploadArea");
const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const loading = document.getElementById("loading");
const analyzeBtn = document.getElementById("analyzeBtn");

const reportPlaceholder = document.getElementById("reportPlaceholder");
const reportContent = document.getElementById("reportContent");
const resultsPlaceholder = document.getElementById("resultsPlaceholder");
const resultsContent = document.getElementById("resultsContent");

uploadArea.addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", () => {
    updateSelectedFileName();
});

uploadArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadArea.classList.add("dragover");
});

uploadArea.addEventListener("dragleave", () => {
    uploadArea.classList.remove("dragover");
});

uploadArea.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadArea.classList.remove("dragover");

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
        fileInput.files = files;
        updateSelectedFileName();
    }
});

function updateSelectedFileName() {
    if (fileInput.files.length > 0) {
        fileName.textContent = fileInput.files[0].name;
    } else {
        fileName.textContent = "No file selected";
    }
}

function setLoadingState(isLoading) {
    if (isLoading) {
        loading.classList.remove("hidden");
        analyzeBtn.disabled = true;
        analyzeBtn.textContent = "Analyzing...";
    } else {
        loading.classList.add("hidden");
        analyzeBtn.disabled = false;
        analyzeBtn.textContent = "Analyze Document";
    }
}

function normalizeReport(report) {
    if (typeof report === "string") {
        return report;
    }

    if (report && typeof report === "object" && report.fraud_report) {
        return report.fraud_report;
    }

    return "Fraud report could not be rendered.";
}

function getImageUrl(path) {
    const filename = path.split("/").pop();
    return `http://127.0.0.1:8000/uploads/${filename}`;
}

function renderFraudSignals(signals) {
    const signalBox = document.getElementById("fraudSignals");

    const items = (signals || []).map(signal => {
        return `
            <li>
                <i class="fa-solid fa-circle-check"></i>
                <span>${signal}</span>
            </li>
        `;
    }).join("");

    signalBox.innerHTML = `
        <h3>Key Fraud Signals</h3>
        <ul class="signal-list">
            ${items}
        </ul>
    `;
}

function renderRisk(riskAssessment) {
    const riskLevel = (riskAssessment.risk_level || "Low").toLowerCase();
    const score = riskAssessment.risk_score ?? 0;

    const riskBadge = document.getElementById("riskBadge");
    const riskLevelText = document.getElementById("riskLevelText");
    const riskScoreText = document.getElementById("riskScoreText");
    const riskIcon = document.getElementById("riskIcon");

    riskBadge.classList.remove("low", "medium", "high");
    riskBadge.classList.add(riskLevel);

    riskLevelText.textContent = riskAssessment.risk_level || "Low";
    riskScoreText.textContent = `Score: ${score}`;

    riskIcon.className = "fa-solid";
    if (riskLevel === "low") {
        riskIcon.classList.add("fa-circle-check");
        riskIcon.style.color = "#1f9d45";
    } else if (riskLevel === "medium") {
        riskIcon.classList.add("fa-triangle-exclamation");
        riskIcon.style.color = "#d97706";
    } else {
        riskIcon.classList.add("fa-circle-exclamation");
        riskIcon.style.color = "#dc2626";
    }
}

function renderInsights(documentInsights, ocrPreview) {
    document.getElementById("ocrStatus").textContent = documentInsights.ocr_status || "-";
    document.getElementById("textLength").textContent = documentInsights.text_length ?? "-";
    document.getElementById("tamperingScore").textContent = documentInsights.tampering_score ?? "-";
    document.getElementById("metadataStatus").textContent = documentInsights.metadata_status || "-";
    document.getElementById("ocrPreview").textContent = ocrPreview || "No OCR preview available.";
}

function showDashboardResults(data) {
    reportPlaceholder.classList.add("hidden");
    reportContent.classList.remove("hidden");

    resultsPlaceholder.classList.add("hidden");
    resultsContent.classList.remove("hidden");

    document.getElementById("originalImage").src = getImageUrl(data.image_path);
    document.getElementById("elaImage").src = getImageUrl(data.tampering_analysis.ela_image);

    renderRisk(data.risk_assessment);
    renderFraudSignals(data.fraud_signals || []);
    renderInsights(data.document_insights || {}, data.ocr_preview || "");

    const reportText = normalizeReport(data.fraud_report);
    document.getElementById("fraudReport").innerHTML = marked.parse(reportText);
}

async function analyzeDocument() {
    const file = fileInput.files[0];

    if (!file) {
        alert("Please upload a document first.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoadingState(true);

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze-document", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok || data.status === "failed") {
            throw new Error(data.reason || "Analysis failed.");
        }

        showDashboardResults(data);
    } catch (error) {
        alert(error.message || "Error connecting to backend.");
    } finally {
        setLoadingState(false);
    }
}