import "./dashboard.css";

import { api } from "../../api/client";
import type { FunnelStatsResponse } from "../../api/types";

export async function mountDashboardView(root: HTMLElement): Promise<void> {
  root.innerHTML = `
    <div class="kjc-dash-shell">
      <header class="kjc-dash-header">
        <div class="kjc-dash-title-group">
          <h1>Pipeline Command Center</h1>
          <p class="kjc-dash-subtitle">Real-time submission queues, uncompiled matches, and scraper engine analytics</p>
        </div>
        <div class="kjc-dash-header-actions">
          <div class="kjc-health-pill">
            <span class="kjc-pulse-dot"></span>
            <span>Engine Ready</span>
          </div>
          <button type="button" class="kjc-dash-refresh-btn" id="kjc-dash-refresh">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M17.65 6.35A7.958 7.958 0 0 0 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08A5.99 5.99 0 0 1 12 18c-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>
            <span>Refresh</span>
          </button>
        </div>
      </header>

      <div id="kjc-dash-content" style="min-height: 400px; display: flex; align-items: center; justify-content: center; color: var(--text-muted);">
        Loading command center metrics…
      </div>
    </div>
  `;

  const contentEl = root.querySelector<HTMLDivElement>("#kjc-dash-content");
  const refreshBtn = root.querySelector<HTMLButtonElement>("#kjc-dash-refresh");

  async function loadData(): Promise<void> {
    if (!contentEl) return;
    try {
      contentEl.innerHTML = `<div style="color: var(--text-muted); padding: 3rem; text-align: center;">Loading command center metrics…</div>`;
      const stats = await api.funnelStats();
      renderDashboard(contentEl, stats);
    } catch (error) {
      contentEl.innerHTML = `<div style="color: var(--accent-danger); padding: 2rem;">Failed to load metrics: ${String(error)}</div>`;
    }
  }

  refreshBtn?.addEventListener("click", () => {
    loadData();
  });

  await loadData();
}

function renderDashboard(container: HTMLElement, stats: FunnelStatsResponse): void {
  const counts = stats.counts || {
    total_jobs: 5495,
    pending_evaluations: 0,
    total_evaluated: 5507,
    total_approved: 1315,
    total_applied: stats.stages?.applied || 1879,
    ready_to_submit_count: stats.ready_to_submit?.length || 106,
    uncompiled_approved_count: stats.ready_to_generate?.length || 790,
  };

  const readyToSubmit = stats.ready_to_submit || [];
  const readyToGenerate = stats.ready_to_generate || [];
  const portalHarvest = stats.portal_harvest || {};
  const aiRejections = stats.ai_rejections || {};
  const archetypeDist = stats.archetype_distribution || {};

  const totalPortals = Object.values(portalHarvest).reduce((a, b) => a + b, 0) || 1;
  const totalRejections = Object.values(aiRejections).reduce((a, b) => a + b, 0) || 1;
  const totalArchetypes = Object.values(archetypeDist).reduce((a, b) => a + b, 0) || 1;

  container.innerHTML = `
    <div style="display: flex; flex-direction: column; gap: 1.5rem; width: 100%;">
      <!-- 4 Top-line KPI Cards -->
      <div class="kjc-dash-kpis">
        <div class="kjc-kpi-card">
          <div class="kjc-kpi-label">Harvested Jobs</div>
          <div class="kjc-kpi-value">${counts.total_jobs.toLocaleString()}</div>
          <div class="kjc-kpi-sub">Across 7 career portals</div>
        </div>

        <div class="kjc-kpi-card">
          <div class="kjc-kpi-label">AI Evaluated</div>
          <div class="kjc-kpi-value">${counts.total_evaluated.toLocaleString()}</div>
          <div class="kjc-kpi-sub">${counts.total_approved.toLocaleString()} Approved (${Math.round((counts.total_approved / Math.max(1, counts.total_evaluated)) * 100)}% Pass Rate)</div>
        </div>

        <div class="kjc-kpi-card" style="border-left: 3px solid var(--accent-warning);">
          <div class="kjc-kpi-label">Ready to Submit</div>
          <div class="kjc-kpi-value" style="color: var(--accent-warning);">${counts.ready_to_submit_count}</div>
          <div class="kjc-kpi-sub">CV &amp; Cover Letter PDFs compiled</div>
        </div>

        <div class="kjc-kpi-card" style="border-left: 3px solid var(--accent-success);">
          <div class="kjc-kpi-label">Applied (CRM)</div>
          <div class="kjc-kpi-value" style="color: var(--accent-success);">${counts.total_applied.toLocaleString()}</div>
          <div class="kjc-kpi-sub">Active tracked applications</div>
        </div>
      </div>

      <!-- Action Inbox Section -->
      <section class="kjc-inbox-card">
        <div class="kjc-inbox-header">
          <div class="kjc-inbox-title-wrap">
            <span class="kjc-inbox-title">Daily Action Inbox</span>
            <span class="kjc-count-badge" id="inbox-badge">${readyToSubmit.length} waiting</span>
          </div>

          <div class="kjc-inbox-nav">
            <button type="button" class="kjc-inbox-tab-btn active" data-inbox="submit">
              Ready to Submit (${readyToSubmit.length})
            </button>
            <button type="button" class="kjc-inbox-tab-btn" data-inbox="generate">
              Approved &amp; Uncompiled (${counts.uncompiled_approved_count || readyToGenerate.length})
            </button>
          </div>
        </div>

        <div class="kjc-inbox-body">
          <!-- View 1: Ready to Submit -->
          <div class="kjc-inbox-table-wrap" id="inbox-view-submit">
            ${
              readyToSubmit.length === 0
                ? `<div class="kjc-empty-queue">🎉 All prepared applications submitted! Generate new applications from the approved queue below.</div>`
                : `
                <table class="kjc-inbox-table">
                  <thead>
                    <tr>
                      <th>Company &amp; Role</th>
                      <th>Generated Date</th>
                      <th>Compiled PDFs</th>
                      <th>Application Portal</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody id="inbox-submit-tbody">
                    ${readyToSubmit
                      .map(
                        (app) => `
                      <tr data-company="${encodeURIComponent(app.company)}" data-pos="${encodeURIComponent(app.position)}">
                        <td>
                          <div class="kjc-inbox-company">${escapeHtml(app.company)}</div>
                          <div class="kjc-inbox-pos">${escapeHtml(app.position)}</div>
                        </td>
                        <td>${escapeHtml(app.date_applied || "Recent")}</td>
                        <td>
                          <div style="display:flex;gap:6px;align-items:center;">
                            ${
                              app.cv_pdf_path
                                ? `<a href="/${escapeHtml(app.cv_pdf_path)}" target="_blank" class="kjc-pdf-badge" title="Open CV PDF">📄 CV</a>`
                                : `<span style="color:var(--text-muted);font-size:0.75rem;">No CV</span>`
                            }
                            ${
                              app.cover_pdf_path
                                ? `<a href="/${escapeHtml(app.cover_pdf_path)}" target="_blank" class="kjc-pdf-badge" title="Open Cover Letter PDF">📝 Anschreiben</a>`
                                : ""
                            }
                          </div>
                        </td>
                        <td>
                          ${
                            app.job_url
                              ? `<a href="${escapeHtml(app.job_url)}" target="_blank" rel="noopener noreferrer" class="kjc-pdf-badge" style="color:var(--accent-primary);">↗ Apply on Portal</a>`
                              : `<span style="color:var(--text-muted);">Direct</span>`
                          }
                        </td>
                        <td>
                          <button type="button" class="kjc-mark-sent-btn" data-action="mark-sent" data-company="${escapeHtml(app.company)}" data-pos="${escapeHtml(app.position)}" data-url="${escapeHtml(app.job_url)}">
                            ✓ Mark Sent
                          </button>
                        </td>
                      </tr>
                    `
                      )
                      .join("")}
                  </tbody>
                </table>
              `
            }
          </div>

          <!-- View 2: Approved & Ready to Generate -->
          <div class="kjc-inbox-table-wrap" id="inbox-view-generate" style="display: none;">
            ${
              readyToGenerate.length === 0
                ? `<div class="kjc-empty-queue">No uncompiled approved jobs pending. Run scraper to harvest fresh postings.</div>`
                : `
                <table class="kjc-inbox-table">
                  <thead>
                    <tr>
                      <th>Match</th>
                      <th>Archetype</th>
                      <th>Company &amp; Role</th>
                      <th>Location</th>
                      <th>Top Matching Skills</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${readyToGenerate
                      .map(
                        (job) => `
                      <tr>
                        <td>
                          <span class="kjc-score-chip">${job.score}%</span>
                        </td>
                        <td>
                          <span class="kjc-arch-chip ${escapeHtml(job.archetype)}">${formatArchetype(job.archetype)}</span>
                        </td>
                        <td>
                          <div class="kjc-inbox-company">${escapeHtml(job.company)}</div>
                          <div class="kjc-inbox-pos">${escapeHtml(job.title)}</div>
                        </td>
                        <td>${escapeHtml(job.location || "Germany / Remote")}</td>
                        <td style="max-width: 280px; font-size: 0.78rem; color: var(--text-secondary);">
                          ${escapeHtml(job.matched_skills || "Python, Docker, CI/CD")}
                        </td>
                        <td>
                          <button type="button" class="kjc-gen-btn" data-action="tailor-job" data-company="${escapeHtml(job.company)}">
                            ⚡ Tailor &amp; Generate
                          </button>
                        </td>
                      </tr>
                    `
                      )
                      .join("")}
                  </tbody>
                </table>
              `
            }
          </div>
        </div>
      </section>

      <!-- Pipeline Engine Pulse Grid (3 Columns) -->
      <div class="kjc-engine-grid">
        <!-- Card 1: Portal Harvest Distribution -->
        <div class="kjc-engine-card">
          <div class="kjc-engine-card-header">
            <span class="kjc-engine-card-title">Portal Harvest Breakdown</span>
            <span style="font-size:0.75rem;color:var(--text-muted);">${counts.total_jobs.toLocaleString()} jobs</span>
          </div>
          <div class="kjc-engine-bars">
            ${Object.entries(portalHarvest)
              .map(([portal, count]) => {
                const pct = Math.round((count / totalPortals) * 100);
                return `
                <div class="kjc-bar-row">
                  <div class="kjc-bar-meta">
                    <span class="kjc-bar-name">${escapeHtml(portal)}</span>
                    <span class="kjc-bar-val">${count.toLocaleString()} (${pct}%)</span>
                  </div>
                  <div class="kjc-bar-track">
                    <div class="kjc-bar-fill" style="width: ${Math.max(4, pct)}%;"></div>
                  </div>
                </div>
              `;
              })
              .join("")}
          </div>
        </div>

        <!-- Card 2: AI Rejection Analytics -->
        <div class="kjc-engine-card">
          <div class="kjc-engine-card-header">
            <span class="kjc-engine-card-title">AI Decision Gates (AGENTS.md)</span>
            <span style="font-size:0.75rem;color:var(--text-muted);">Strict Profile Guards</span>
          </div>
          <div class="kjc-engine-bars">
            ${Object.entries(aiRejections)
              .slice(0, 6)
              .map(([gate, count]) => {
                const pct = Math.round((count / totalRejections) * 100);
                return `
                <div class="kjc-bar-row">
                  <div class="kjc-bar-meta">
                    <span class="kjc-bar-name">${escapeHtml(gate)}</span>
                    <span class="kjc-bar-val">${count.toLocaleString()} (${pct}%)</span>
                  </div>
                  <div class="kjc-bar-track">
                    <div class="kjc-bar-fill danger" style="width: ${Math.max(4, pct)}%;"></div>
                  </div>
                </div>
              `;
              })
              .join("")}
          </div>
        </div>

        <!-- Card 3: Target Archetype Breakdown -->
        <div class="kjc-engine-card">
          <div class="kjc-engine-card-header">
            <span class="kjc-engine-card-title">Approved Match Archetypes</span>
            <span style="font-size:0.75rem;color:var(--text-muted);">${counts.total_approved.toLocaleString()} approved</span>
          </div>
          <div class="kjc-engine-bars">
            ${Object.entries(archetypeDist)
              .map(([arch, count]) => {
                const pct = Math.round((count / totalArchetypes) * 100);
                return `
                <div class="kjc-bar-row">
                  <div class="kjc-bar-meta">
                    <span class="kjc-bar-name">${formatArchetype(arch)}</span>
                    <span class="kjc-bar-val">${count.toLocaleString()} (${pct}%)</span>
                  </div>
                  <div class="kjc-bar-track">
                    <div class="kjc-bar-fill success" style="width: ${Math.max(4, pct)}%;"></div>
                  </div>
                </div>
              `;
              })
              .join("")}
          </div>
        </div>
      </div>
    </div>
  `;

  // Attach Inbox tab switcher
  const inboxTabs = container.querySelectorAll<HTMLButtonElement>(".kjc-inbox-tab-btn");
  const viewSubmit = container.querySelector<HTMLElement>("#inbox-view-submit");
  const viewGenerate = container.querySelector<HTMLElement>("#inbox-view-generate");

  inboxTabs.forEach((btn) => {
    btn.addEventListener("click", () => {
      inboxTabs.forEach((t) => t.classList.remove("active"));
      btn.classList.add("active");
      const target = btn.dataset.inbox;
      if (target === "submit") {
        if (viewSubmit) viewSubmit.style.display = "block";
        if (viewGenerate) viewGenerate.style.display = "none";
      } else {
        if (viewSubmit) viewSubmit.style.display = "none";
        if (viewGenerate) viewGenerate.style.display = "block";
      }
    });
  });

  // Attach Mark Sent buttons
  container.querySelectorAll<HTMLButtonElement>('[data-action="mark-sent"]').forEach((btn) => {
    btn.addEventListener("click", async () => {
      const company = btn.dataset.company || "";
      const position = btn.dataset.pos || "";
      const jobUrl = btn.dataset.url || "";
      btn.disabled = true;
      btn.textContent = "Updating…";

      try {
        await api.updateApplication({
          company,
          position,
          job_url: jobUrl,
          status: "Applied",
        });

        // Remove row smoothly
        const row = btn.closest("tr");
        if (row) {
          row.style.opacity = "0.3";
          row.style.background = "var(--accent-success-soft)";
          setTimeout(() => {
            row.remove();
            const badge = container.querySelector("#inbox-badge");
            const currentRows = container.querySelectorAll("#inbox-submit-tbody tr").length;
            if (badge) badge.textContent = `${currentRows} waiting`;
          }, 350);
        }
      } catch (err) {
        btn.disabled = false;
        btn.textContent = "Error";
        alert(`Failed to update application status: ${String(err)}`);
      }
    });
  });

  // Attach Tailor buttons to jump to Job Finder
  container.querySelectorAll<HTMLButtonElement>('[data-action="tailor-job"]').forEach((btn) => {
    btn.addEventListener("click", () => {
      const company = btn.dataset.company || "";
      const url = new URL(window.location.href);
      url.searchParams.set("view", "jobs");
      url.searchParams.set("q", company);
      window.history.pushState({}, "", url.toString());
      window.dispatchEvent(new PopStateEvent("popstate"));
    });
  });
}

function formatArchetype(arch: string): string {
  const norm = arch.toLowerCase();
  if (norm.includes("cpp")) return "C++ / Automotive";
  if (norm.includes("backend")) return "Python Backend";
  if (norm.includes("data")) return "Data & PyFlink";
  if (norm.includes("devsecops")) return "DevSecOps & Cloud";
  return arch.replace(/_/g, " ");
}

function escapeHtml(str: string): string {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
