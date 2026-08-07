/**
 * Dashboard Page JavaScript
 * Fetches stats from the backend and renders Chart.js charts.
 */

document.addEventListener("DOMContentLoaded", async () => {
    try {
        const res = await fetch("/dashboard/stats");
        const stats = await res.json();

        // Update stat counters
        document.getElementById("stat-users").textContent = stats.total_users;
        document.getElementById("stat-conversations").textContent = stats.total_conversations;
        document.getElementById("stat-messages").textContent = stats.total_messages;

        // Category doughnut chart
        const categories = stats.categories || {};
        const labels = Object.keys(categories);
        const values = Object.values(categories);

        if (labels.length > 0) {
            new Chart(document.getElementById("category-chart"), {
                type: "doughnut",
                data: {
                    labels,
                    datasets: [
                        {
                            data: values,
                            backgroundColor: ["#6366f1", "#06b6d4", "#f59e0b", "#10b981", "#ef4444"],
                        },
                    ],
                },
                options: { responsive: true, plugins: { legend: { position: "bottom" } } },
            });
        }

        // Recent conversations list
        const recentList = document.getElementById("recent-list");
        const recent = stats.recent_conversations || [];
        if (recent.length > 0) {
            recentList.innerHTML = recent
                .map(
                    (c) => `
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <span>${c.title}</span>
                    <span class="badge bg-primary rounded-pill">${c.category}</span>
                </li>
            `
                )
                .join("");
        } else {
            recentList.innerHTML = '<li class="list-group-item text-muted">No conversations yet.</li>';
        }
    } catch (err) {
        console.error("Failed to load dashboard stats:", err);
    }
});
