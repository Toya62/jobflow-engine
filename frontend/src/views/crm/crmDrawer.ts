/** CRM detail drawer: shows job description with Email drafting modal popup and CV generation. */

import type { TrackerRecord } from "../../api/types";
import { openEmailModal } from "../common/emailModal";

const ESCAPE_MAP: Record<string, string> = {
  "&": "&amp;",
  "<": "&lt;",
  ">": "&gt;",
  '"': "&quot;",
  "'": "&#39;",
};

export function escapeHtml(value: unknown): string {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ESCAPE_MAP[char]);
}

export interface CrmDrawer {
  element: HTMLElement;
  open(record: TrackerRecord): void;
  close(): void;
}

export function createCrmDrawer(): CrmDrawer {
  const element = document.createElement("div");
  element.className = "kjc-drawer hidden";

  element.innerHTML = `
    <div class="kjc-drawer-backdrop" data-role="backdrop"></div>
    <div class="kjc-drawer-panel" role="dialog" aria-modal="true" aria-label="Application details">
      <div class="kjc-drawer-head">
        <div class="kjc-modal-title-group">
          <div class="kjc-modal-company" data-role="company"></div>
          <h2 class="kjc-modal-title" data-role="title"></h2>
          <div class="kjc-modal-badges" data-role="badges"></div>
        </div>
        <button type="button" class="kjc-drawer-close-btn" data-role="close" aria-label="Close dialog">✕</button>
      </div>
      <div class="kjc-drawer-body" data-role="body"></div>
    </div>`;

  const titleEl = element.querySelector<HTMLElement>('[data-role="title"]');
  const companyEl = element.querySelector<HTMLElement>('[data-role="company"]');
  const badgesEl = element.querySelector<HTMLElement>('[data-role="badges"]');
  const bodyEl = element.querySelector<HTMLElement>('[data-role="body"]');
  let openToken = 0;

  const close = (): void => {
    openToken += 1;
    element.classList.add("hidden");
  };

  element.querySelector('[data-role="backdrop"]')?.addEventListener("click", close);
  element.querySelector('[data-role="close"]')?.addEventListener("click", close);

  const copyDescription = (text: string): void => {
    if (!text) return;
    void navigator.clipboard.writeText(text).then(
      () => {
        const btn = bodyEl?.querySelector<HTMLButtonElement>("[data-role='copy-desc']");
        if (btn) {
          const original = btn.textContent;
          btn.textContent = "✓ Copied!";
          window.setTimeout(() => { if (btn) btn.textContent = original; }, 1500);
        }
      },
      () => {
        const textarea = document.createElement("textarea");
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy");
        textarea.remove();
      },
    );
  };

  const open = (record: TrackerRecord): void => {
    openToken += 1;
    const token = openToken;
    if (titleEl) titleEl.textContent = String(record.position ?? "Application");
    if (companyEl) companyEl.textContent = String(record.company ?? "Company");
    if (badgesEl) {
      badgesEl.innerHTML = `
        <span class="kjc-status-chip">${escapeHtml(record.status || "Prepared")}</span>
        <span class="kjc-meta-pill">📍 ${escapeHtml(record.location || "Germany")}</span>
        <span class="kjc-meta-pill">📅 Applied: ${escapeHtml(record.date_applied || "Recent")}</span>
      `;
    }
    if (bodyEl) {
      const existing = String(record.description ?? "").trim();
      const cvLink = record.cv_pdf_path
        ? `<a class="kjc-btn kjc-btn-primary" href="/${escapeHtml(record.cv_pdf_path)}" target="_blank">📄 Open CV PDF ↗</a>`
        : "";
      const clLink = record.cover_pdf_path
        ? `<a class="kjc-btn" href="/${escapeHtml(record.cover_pdf_path)}" target="_blank">📝 Open Cover Letter ↗</a>`
        : "";
      const jobUrlLink = record.job_url
        ? `<a class="kjc-btn" href="${escapeHtml(record.job_url)}" target="_blank" rel="noopener noreferrer">↗ Open Portal</a>`
        : "";

      bodyEl.innerHTML = `
        <div class="kjc-modal-action-bar">
          ${cvLink}
          ${clLink}
          <button type="button" class="kjc-btn" data-role="generate">⚡ Re-Generate Files</button>
          <button type="button" class="kjc-btn" data-role="email">✉️ Draft Recruiter Email</button>
          ${jobUrlLink}
          <button type="button" class="kjc-btn" data-role="copy-desc" ${existing ? "" : "disabled"}>
            📋 ${existing ? "Copy Description" : "Loading…"}
          </button>
        </div>

        <div class="kjc-modal-card">
          <div class="kjc-card-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
            Job Description
          </div>
          <pre class="kjc-drawer-desc" data-role="desc">${existing ? escapeHtml(existing) : "Loading description…"}</pre>
        </div>`;

      const copyBtn = bodyEl.querySelector<HTMLButtonElement>("[data-role='copy-desc']");
      const descEl = bodyEl.querySelector<HTMLElement>("[data-role='desc']");
      const generateBtn = bodyEl.querySelector<HTMLButtonElement>("[data-role='generate']");
      const emailBtn = bodyEl.querySelector<HTMLButtonElement>("[data-role='email']");
      const closeBtn = bodyEl.querySelector<HTMLButtonElement>("[data-role='close2']");

      copyBtn?.addEventListener("click", () => {
        const text = descEl?.textContent || "";
        void copyDescription(text);
      });

      generateBtn?.addEventListener("click", () => {
        const genDrawer = (window as any).__jobGenDrawer;
        if (genDrawer) {
          genDrawer.open({
            company: record.company,
            title: record.position,
            job_url: record.job_url,
            location: record.location,
            description: record.description,
          } as any, "application");
        } else if (record.job_url) {
          window.open(record.job_url, "_blank", "noopener,noreferrer");
        }
      });

      emailBtn?.addEventListener("click", () => {
        const desc = descEl?.textContent?.trim() || String(record.description || "");
        openEmailModal({
          company: record.company,
          position: record.position,
          job_url: record.job_url,
          description: desc,
        });
      });

      closeBtn?.addEventListener("click", close);

      if (!existing) {
        const fetchUrl = record.job_url ? `/api/job-descriptions?urls=${encodeURIComponent(record.job_url)}` : null;
        if (fetchUrl && descEl && copyBtn) {
          fetch(fetchUrl)
            .then((r) => r.json())
            .then((map) => {
              if (token !== openToken) return;
              const text = map[record.job_url] || "";
              if (text) {
                descEl.textContent = text;
                copyBtn.disabled = false;
                copyBtn.textContent = "Copy";
              } else {
                descEl.textContent = "No description available.";
              }
            })
            .catch(() => {
              if (token !== openToken) return;
              if (descEl) descEl.textContent = "Could not load description.";
            });
        }
      }
    }
    element.classList.remove("hidden");
  };

  return { element, open, close };
}