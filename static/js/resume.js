/**
 * Resume Page JavaScript
 * Sends resume text to the backend and displays AI suggestions.
 */

const btnAnalyze = document.getElementById("btn-analyze");
const resumeText = document.getElementById("resume-text");
const suggestionsOutput = document.getElementById("suggestions-output");

btnAnalyze.addEventListener("click", async () => {
    const text = resumeText.value.trim();
    if (!text) {
        alert("Please paste your resume text first.");
        return;
    }

    btnAnalyze.disabled = true;
    btnAnalyze.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Analyzing...';
    suggestionsOutput.innerHTML = '<p class="text-muted text-center">Analyzing your resume...</p>';

    try {
        const res = await fetch("/resume/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ resume_text: text }),
        });
        const data = await res.json();

        // Render markdown-like suggestions (basic formatting)
        suggestionsOutput.innerHTML = `<div class="suggestions-content">${formatMarkdown(data.suggestions)}</div>`;
    } catch (err) {
        suggestionsOutput.innerHTML = '<p class="text-danger">Failed to analyze resume. Please try again.</p>';
    } finally {
        btnAnalyze.disabled = false;
        btnAnalyze.innerHTML = '<i class="bi bi-magic me-1"></i> Analyze Resume';
    }
});

function formatMarkdown(text) {
    // Basic markdown → HTML conversion
    return text
        .replace(/### (.*)/g, "<h5>$1</h5>")
        .replace(/## (.*)/g, "<h4>$1</h4>")
        .replace(/# (.*)/g, "<h3>$1</h3>")
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\n- /g, "\n• ")
        .replace(/\n/g, "<br>");
}
