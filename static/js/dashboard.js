const currency = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0
});

const numberFormatter = new Intl.NumberFormat("en-US");
const charts = {};

const palette = {
    teal: "#0f9f8f",
    blue: "#2f6fb2",
    gold: "#d89d2b",
    rose: "#cc4965",
    ink: "#17202a",
    muted: "#64748b",
    grid: "#e2e8f0",
    colors: ["#0f9f8f", "#2f6fb2", "#d89d2b", "#cc4965", "#5d7896", "#7c6bb0", "#2f9f55", "#b85f32", "#247b7b", "#8b5c7e"]
};

function setStatus(text, mode = "loading") {
    const badge = document.getElementById("statusBadge");
    badge.textContent = text;
    badge.className = `status-badge ${mode}`;
}

function showError(message) {
    const box = document.getElementById("errorBox");
    box.textContent = message;
    box.classList.remove("d-none");
    setStatus("Error", "error");
}

function clearError() {
    const box = document.getElementById("errorBox");
    box.textContent = "";
    box.classList.add("d-none");
}

async function fetchJson(url) {
    const response = await fetch(url, { headers: { "Accept": "application/json" } });
    if (!response.ok) {
        const body = await response.json().catch(() => ({}));
        throw new Error(body.message || `Request failed: ${url}`);
    }
    return response.json();
}

function destroyChart(id) {
    if (charts[id]) {
        charts[id].destroy();
        delete charts[id];
    }
}

function renderLineChart(id, labels, values) {
    destroyChart(id);
    charts[id] = new Chart(document.getElementById(id), {
        type: "line",
        data: {
            labels,
            datasets: [{
                label: "Revenue",
                data: values,
                borderColor: palette.teal,
                backgroundColor: "rgba(15, 159, 143, 0.12)",
                tension: 0.32,
                fill: true,
                pointRadius: 3
            }]
        },
        options: chartOptions(true)
    });
}

function renderBarChart(id, labels, values, label, color = palette.blue, horizontal = false) {
    destroyChart(id);
    charts[id] = new Chart(document.getElementById(id), {
        type: "bar",
        data: {
            labels,
            datasets: [{
                label,
                data: values,
                backgroundColor: color,
                borderRadius: 5,
                maxBarThickness: 42
            }]
        },
        options: chartOptions(true, horizontal)
    });
}

function renderPieChart(id, labels, values) {
    destroyChart(id);
    charts[id] = new Chart(document.getElementById(id), {
        type: "doughnut",
        data: {
            labels,
            datasets: [{
                data: values,
                backgroundColor: palette.colors,
                borderColor: "#ffffff",
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "bottom", labels: { boxWidth: 12 } }
            },
            cutout: "58%"
        }
    });
}

function chartOptions(showLegend = false, horizontal = false) {
    return {
        indexAxis: horizontal ? "y" : "x",
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: showLegend },
            tooltip: {
                callbacks: {
                    label: (context) => `${context.dataset.label}: ${numberFormatter.format(context.parsed.y ?? context.parsed.x)}`
                }
            }
        },
        scales: {
            x: {
                grid: { color: horizontal ? palette.grid : "transparent" },
                ticks: { color: palette.muted }
            },
            y: {
                beginAtZero: true,
                grid: { color: palette.grid },
                ticks: { color: palette.muted }
            }
        }
    };
}

function setText(id, value) {
    const element = document.getElementById(id);
    element.textContent = value;
    element.classList.remove("skeleton-text");
}

function renderRanking(rows) {
    const body = document.getElementById("customerRankingBody");
    if (!rows.length) {
        body.innerHTML = '<tr><td colspan="3">No customer data available.</td></tr>';
        return;
    }

    body.innerHTML = rows.slice(0, 25).map((row) => `
        <tr>
            <td><strong>${row.rank}</strong></td>
            <td>${row.customer_id}</td>
            <td>${currency.format(row.revenue)}</td>
        </tr>
    `).join("");
}

async function loadDashboard() {
    clearError();
    setStatus("Loading");

    try {
        const [
            totalSales,
            monthlySales,
            topProducts,
            countrySales,
            averageOrderValue,
            customerRanking
        ] = await Promise.all([
            fetchJson("/api/total-sales"),
            fetchJson("/api/monthly-sales"),
            fetchJson("/api/top-products"),
            fetchJson("/api/country-sales"),
            fetchJson("/api/average-order-value"),
            fetchJson("/api/customer-ranking")
        ]);

        setText("totalRevenue", currency.format(totalSales.total_revenue));
        setText("averageOrderValue", currency.format(averageOrderValue.average_order_value));
        setText("topProductUnits", topProducts[0] ? numberFormatter.format(topProducts[0].total_sold) : "0");
        setText("topCountry", countrySales[0] ? countrySales[0].country : "-");

        renderLineChart(
            "monthlySalesChart",
            monthlySales.map((row) => row.month),
            monthlySales.map((row) => row.revenue)
        );

        renderBarChart(
            "topProductsChart",
            topProducts.map((row) => row.description),
            topProducts.map((row) => row.total_sold),
            "Units Sold",
            palette.blue,
            true
        );

        const topCountries = countrySales.slice(0, 8);
        renderPieChart(
            "countryPieChart",
            topCountries.map((row) => row.country),
            topCountries.map((row) => row.revenue)
        );

        renderBarChart(
            "countryBarChart",
            countrySales.slice(0, 12).map((row) => row.country),
            countrySales.slice(0, 12).map((row) => row.revenue),
            "Revenue",
            palette.gold
        );

        renderRanking(customerRanking);
        setStatus("Ready", "ready");
    } catch (error) {
        showError(`Unable to load dashboard data. ${error.message}`);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("refreshBtn").addEventListener("click", loadDashboard);
    loadDashboard();
});
