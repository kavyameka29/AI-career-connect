/**
 * Interview Page JavaScript
 * Generates mock interview questions via the AI backend.
 */

const interviewForm = document.getElementById("interview-form");
const questionsOutput = document.getElementById("questions-output");

interviewForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const jobRole = document.getElementById("job-role").value.trim();
    const difficulty = document.getElementById("difficulty").value;

    if (!jobRole) {
        alert("Please enter a job role.");
        return;
    }

    questionsOutput.innerHTML = '<p class="text-muted text-center py-3"><span class="spinner-border spinner-border-sm me-1"></span> Generating questions...</p>';

    try {
        const res = await fetch("/interview/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ job_role: jobRole, difficulty }),
        });
        const data = await res.json();

        renderQuestions(data.questions);
    } catch (err) {
        questionsOutput.innerHTML = '<p class="text-danger">Failed to generate questions.</p>';
    }
});

function renderQuestions(questions) {
    if (!Array.isArray(questions)) {
        questionsOutput.innerHTML = `<div class="card p-3">${questions}</div>`;
        return;
    }

    questionsOutput.innerHTML = questions
        .map(
            (q, i) => `
        <div class="card mb-3">
            <div class="card-body">
                <h5 class="card-title">Q${i + 1}: ${q.question}</h5>
                <p class="text-muted mb-1"><strong>Why they ask:</strong> ${q.purpose}</p>
                <p class="mb-0"><strong>💡 Tip:</strong> ${q.tip}</p>
            </div>
        </div>
    `
        )
        .join("");
}
