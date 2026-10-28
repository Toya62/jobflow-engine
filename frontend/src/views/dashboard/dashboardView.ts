import "./dashboard.css";

import { api } from "../../api/client";
import type { FunnelStatsResponse } from "../../api/types";

export async function mountDashboardView(root: HTMLElement): Promise<void> {
  root.innerHTML = `
    <div class="kjc-dash-shell">
      <header class="kjc-dash-header">
        <div class="kjc-dash-greeting">
          <h1 class="kjc-dash-title">Executive Pipeline Funnel</h1>
          <p class="kjc-dash-subtitle">High-velocity ATS applications, verified profile alignment &amp; interview pipeline</p>
        </div>
        <div class="kjc-dash-meta-badge">
          <span>●</span> 100% Verified Profile Integrity (AGENTS.md)
        </div>
      </header>

      <!-- Loading skeleton -->
      <div id="kjc-dash-content" style="min-height: 400px; display: flex; align-items: center; justify-content: center; color: var(--text-muted);">
        Loading pipeline analytics…
      </div>
    </div>
  `;

  const contentEl = root.querySelector<HTMLDivElement>("#kjc-dash-content");
  if (!contentEl) return;

  try {
    const stats: FunnelStatsResponse = await api.funnelStats();
    renderDashboard(contentEl, stats);
  } catch (error) {
    contentEl.innerHTML = `<div style="color: var(--accent-danger);">Failed to load funnel statistics: ${String(error)}</div>`;
  }
}

function renderDashboard(container: HTMLElement, stats: FunnelStatsResponse): void {
  const { stages, conversions, weekly_activity, top_recommendations } = stats;

  const totalTracked = stages.total || (stages.draft + stages.applied + stages.screening + stages.interview + stages.offer + stages.rejected);
  const activeCount = stages.applied + stages.screening + stages.interview;
  const interviewCount = stages.interview;
  const convRate = conversions.applied_to_interview;

  container.innerHTML = `
    <div style="display: flex; flex-direction: column; gap: 1.75rem; width: 100%;">
      <!-- KPI Row -->
      <div class="kjc-dash-kpis">
        <div class="kjc-kpi-card blue">
          <div class="kjc-kpi-label">Total Applications</div>
          <div class="kjc-kpi-value">${totalTracked}</div>
          <div class="kjc-kpi-sub">Lifetime applications in CRM</div>
        </div>

        <div class="kjc-kpi-card brass">
          <div class="kjc-kpi-label">Active Pipeline</div>
          <div class="kjc-kpi-value">${activeCount}</div>
          <div class="kjc-kpi-sub">Currently in review or active</div>
        </div>

        <div class="kjc-kpi-card purple">
          <div class="kjc-kpi-label">Interviews Scheduled</div>
          <div class="kjc-kpi-value">${interviewCount}</div>
          <div class="kjc-kpi-sub">Screening &amp; technical interviews</div>
        </div>

        <div class="kjc-kpi-card green">
          <div class="kjc-kpi-label">Interview Conversion</div>
          <div class="kjc-kpi-value">${convRate}%</div>
          <div class="kjc-kpi-sub">Applied-to-interview yield</div>
        </div>
      </div>

      <!-- Application Funnel (Dossier-style) -->
      <section class="kjc-dash-section">
        <div class="kjc-section-header">
          <div class="kjc-section-title">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3z"/></svg>
            Application Funnel Stages
          </div>
          <div style="font-size: 0.8rem; color: var(--text-muted);">
            Updated in real-time from PostgreSQL &amp; SQLite
          </div>
        </div>

        <div class="kjc-funnel-stages">
          <div class="kjc-funnel-node stage-draft">
            <div class="kjc-node-title">Prepared / Draft</div>
            <div class="kjc-node-count">${stages.draft}</div>
            <div class="kjc-node-conversion">Ready to submit</div>
          </div>

          <div class="kjc-funnel-node stage-applied">
            <div class="kjc-node-title">Applied / Sent</div>
            <div class="kjc-node-count">${stages.applied}</div>
            <div class="kjc-node-conversion">Awaiting first response</div>
          </div>

          <div class="kjc-funnel-node stage-interview">
            <div class="kjc-node-title">Interview</div>
            <div class="kjc-node-count">${stages.interview}</div>
            <div class="kjc-node-conversion">${conversions.applied_to_interview}% interview rate</div>
          </div>

          <div class="kjc-funnel-node stage-offer">
            <div class="kjc-node-title">Offer</div>
            <div class="kjc-node-count">${stages.offer}</div>
            <div class="kjc-node-conversion">${conversions.interview_to_offer}% offer yield</div>
          </div>

          <div class="kjc-funnel-node stage-rejected">
            <div class="kjc-node-title">Archived / Closed</div>
            <div class="kjc-node-count">${stages.rejected}</div>
            <div class="kjc-node-conversion">Declined or filled</div>
          </div>
        </div>
      </section>

      <!-- Two-Column Grid: Recommendations + Weekly Velocity -->
      <div class="kjc-dash-grid">
        <!-- Top Recommendations -->
        <section class="kjc-dash-section">
          <div class="kjc-section-header">
            <div class="kjc-section-title">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
              What's Worth a Look Next
            </div>
            <a href="?view=jobs" style="font-size: 0.8rem; color: var(--accent-primary); text-decoration: none;">View All Jobs →</a>
          </div>

          <div class="kjc-rec-list" id="kjc-rec-container">
            ${
              top_recommendations.length === 0
                ? `<div style="color: var(--text-muted); font-size: 0.9rem; padding: 1.5rem; text-align: center;">All top recommendations have applications prepared! Run scraper for new jobs.</div>`
                : top_recommendations
                    .map(
                      (job) => `
              <div class="kjc-rec-card" data-job-id="${job.id}">
                <div class="kjc-rec-info">
                  <div class="kjc-rec-topline">
                    <span class="kjc-rec-company">${escapeHtml(job.company)}</span>
                    <span class="kjc-rec-role">— ${escapeHtml(job.title)}</span>
                  </div>
                  <div style="font-size: 0.8rem; color: var(--text-muted);">
                    📍 ${escapeHtml(job.location || "Germany")} • Scraped ${escapeHtml(job.scraped_at ? job.scraped_at.slice(0, 10) : "Recent")}
                  </div>
                  ${
                    job.matched_skills
                      ? `<div class="kjc-rec-tags">
                      ${job.matched_skills
                        .split(",")
                        .slice(0, 4)
                        .map((s) => `<span class="kjc-rec-tag">${escapeHtml(s.trim())}</span>`)
                        .join("")}
                    </div>`
                      : ""
                  }
                </div>
                <div class="kjc-rec-actions">
                  <span class="kjc-score-badge">${job.score}%</span>
                  <button type="button" class="kjc-btn-sm kjc-gen-rec-btn" data-job-id="${job.id}" data-company="${escapeHtml(job.company)}" data-title="${escapeHtml(job.title)}" data-url="${escapeHtml(job.url)}" data-location="${escapeHtml(job.location || "")}">
                    ⚡ Tailor
                  </button>
                </div>
              </div>
            `
                    )
                    .join("")
            }
          </div>
        </section>

        <!-- Activity & Next Steps -->
        <section class="kjc-dash-section">
          <div class="kjc-section-header">
            <div class="kjc-section-title">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
              Weekly Application Velocity
            </div>
          </div>

          <div class="kjc-activity-bars">
            ${
              weekly_activity.length === 0
                ? `<div style="width: 100%; text-align: center; color: var(--text-muted); font-size: 0.85rem; align-self: center;">No activity recorded yet in current window.</div>`
                : weekly_activity
                    .map((item) => {
                      const maxVal = Math.max(...weekly_activity.map((w) => w.applied + w.prepared), 1);
                      const totalH = Math.min(100, Math.round(((item.applied + item.prepared) / maxVal) * 100));
                      const appliedH = item.applied + item.prepared > 0 ? Math.round((item.applied / (item.applied + item.prepared)) * 100) : 0;
                      return `
                <div class="kjc-activity-col">
                  <div class="kjc-bar-stack" style="height: ${Math.max(totalH, 8)}%;">
                    <div class="kjc-bar-applied" style="height: ${appliedH}%;"></div>
                  </div>
                  <span class="kjc-bar-label">${escapeHtml(item.week)}</span>
                </div>
              `;
                    })
                    .join("")
            }
          </div>

          <!-- Quick Next Actions -->
          <div style="display: flex; flex-direction: column; gap: 0.75rem; margin-top: 0.5rem;">
            <div style="font-size: 0.82rem; font-weight: 600; text-transform: uppercase; color: var(--text-muted);">
              Recommended Next Actions
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.75rem 1rem; background: var(--bg-elevated); border: 1px solid var(--border-color); border-radius: var(--radius-sm); font-size: 0.85rem;">
              <span>⚡ <strong>Run scraper</strong> across all 7 portals to ingest latest 24h postings</span>
              <a href="?view=scraper" class="kjc-btn-sm" style="text-decoration: none; padding: 0.25rem 0.65rem;">Scraper</a>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.75rem 1rem; background: var(--bg-elevated); border: 1px solid var(--border-color); border-radius: var(--radius-sm); font-size: 0.85rem;">
              <span>📋 <strong>Review CRM</strong> board for applications awaiting follow-up</span>
              <a href="?view=crm" class="kjc-btn-sm" style="text-decoration: none; padding: 0.25rem 0.65rem;">CRM Board</a>
            </div>
          </div>
        </section>
      </div>
    </div>
  `;

  // Attach 1-click generator handler to top recommendation buttons
  container.querySelectorAll<HTMLButtonElement>(".kjc-gen-rec-btn").forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      e.stopPropagation();
      const company = btn.dataset.company || "";
      const position = btn.dataset.title || "";
      const jobUrl = btn.dataset.url || "";
      const location = btn.dataset.location || "";

      btn.disabled = true;
      btn.textContent = "Generating…";

      try {
        const resp = await api.generateApplication({
          company,
          position,
          description: "",
          job_url: jobUrl,
          location,
          language: "de",
        });

        if (resp.success || resp.status === "completed" || resp.status === "already_exists") {
          btn.textContent = "✓ Done";
          btn.style.background = "var(--accent-success)";
          btn.style.borderColor = "var(--accent-success)";
          setTimeout(() => {
            window.location.search = `?view=crm&q=${encodeURIComponent(company)}`;
          }, 800);
        } else {
          btn.textContent = "Queued…";
          setTimeout(() => {
            window.location.search = `?view=crm&q=${encodeURIComponent(company)}`;
          }, 1000);
        }
      } catch (err) {
        btn.disabled = false;
        btn.textContent = "Error";
        alert(`Failed to start generation: ${String(err)}`);
      }
    });
  });
}

function escapeHtml(text: string): string {
  const map: Record<string, string> = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  };
  return String(text).replace(/[&<>"']/g, (m) => map[m]);
}
