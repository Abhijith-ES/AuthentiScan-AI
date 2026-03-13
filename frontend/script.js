const uploadArea = document.getElementById("uploadArea");
const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");

/* Click upload */

uploadArea.addEventListener("click", () => {
fileInput.click();
});

/* File selection */

fileInput.addEventListener("change", () => {

if(fileInput.files.length > 0){
fileName.innerText = fileInput.files[0].name;
}

});

/* Drag and Drop */

uploadArea.addEventListener("dragover", (e) => {
e.preventDefault();
uploadArea.style.background = "#e0f2fe";
});

uploadArea.addEventListener("dragleave", () => {
uploadArea.style.background = "#fafafa";
});

uploadArea.addEventListener("drop", (e) => {

e.preventDefault();

fileInput.files = e.dataTransfer.files;

fileName.innerText = fileInput.files[0].name;

uploadArea.style.background = "#fafafa";

});


async function analyzeDocument(){

const file = fileInput.files[0];

if(!file){
alert("Please upload a document first.");
return;
}

const formData = new FormData();
formData.append("file", file);

/* Show loader */

document.getElementById("loading").classList.remove("hidden");
document.getElementById("results").classList.add("hidden");

try{

const response = await fetch("http://127.0.0.1:8000/analyze-document", {
method:"POST",
body:formData
});

const data = await response.json();

/* Hide loader */

document.getElementById("loading").classList.add("hidden");
document.getElementById("results").classList.remove("hidden");


/* Risk badge color */

let riskLevel = data.risk_assessment.risk_level.toLowerCase();
let riskClass = riskLevel+"-risk";

document.getElementById("riskScore").innerHTML =
`<span class="${riskClass}">
${data.risk_assessment.risk_level}
</span>
 (Score: ${data.risk_assessment.risk_score})`;


/* Render markdown report */

document.getElementById("fraudReport").innerHTML =
marked.parse(data.fraud_report);


/* Correct image rendering */

const originalFile = data.image_path.split("/").pop();
const elaFile = data.tampering_analysis.ela_image.split("/").pop();

document.getElementById("originalImage").src =
`http://127.0.0.1:8000/uploads/${originalFile}`;

document.getElementById("elaImage").src =
`http://127.0.0.1:8000/uploads/${elaFile}`;

}
catch(error){

document.getElementById("loading").classList.add("hidden");

alert("Error connecting to backend.");

}

}