/* ===================================================================
   main.js — moves inline JS out of HTML and keeps the same behavior.
   Also includes an "easy mode" if you want to simplify further.
   =================================================================== */

(() => {
  // ====== CONFIG ======
  // Highest priority: runtime-configured API base (stamped by CI)
  const API_BASE =
    (window.__APP_CONFIG__ && typeof window.__APP_CONFIG__.apiBase === 'string'
      ? window.__APP_CONFIG__.apiBase
      : ''
    ).replace(/\/+$/, ''); // trim trailing /

  const ENDPOINT = API_BASE ? `${API_BASE}/visit` : null;

  /*
    INCREMENT_BEHAVIOR:
    - "session": POST (inc 1) only once per browser tab session; otherwise GET
    - "always" : POST every load
    - "never"  : GET only (read-only)
  */
  const INCREMENT_BEHAVIOR = "session";

  // If you want the simplest possible behavior, set EASY_MODE = true.
  // In EASY_MODE we just GET on load and on refresh; no animation, no session logic.
  const EASY_MODE = false;

  // ====== DOM ======
  const elValue = document.getElementById("visit-value");
  const elSub   = document.getElementById("visit-sub");
  const elBtn   = document.getElementById("visit-refresh");
  const printBtn = document.getElementById("print-btn");

  // Hook up print button (moved from inline onclick)
  if (printBtn) {
    printBtn.addEventListener("click", () => window.print());
  }

  // ====== HELPERS ======
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function formatNumber(n){ try{ return Number(n).toLocaleString(undefined); }catch{ return String(n); }}

  function countUp(el, from, to, ms=800){
    if (prefersReducedMotion) { el.textContent = formatNumber(to); return; }
    const start = performance.now();
    function frame(now){
      const t = Math.min(1, (now - start)/ms);
      const eased = t<.5 ? 2*t*t : -1 + (4 - 2*t)*t;
      const val = Math.round(from + (to - from) * eased);
      el.textContent = formatNumber(val);
      if (t < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  function shouldPost(){
    if (INCREMENT_BEHAVIOR === "always") return true;
    if (INCREMENT_BEHAVIOR === "never") return false;
    // "session"
    const KEY = "visitCounter.incremented";
    const isPrerender = document.visibilityState === "prerender";
    const isBot = /bot|crawl|spider|slurp|bingpreview/i.test(navigator.userAgent||"");
    if (sessionStorage.getItem(KEY) || isPrerender || isBot) return false;
    sessionStorage.setItem(KEY, "1");
    return true;
  }

  async function fetchCount({forceGet=false}={}){
    try{
      if (!ENDPOINT) {
          console.warn('Counter API not configured: window.__APP_CONFIG__.apiBase missing');
            elValue.textContent = '—';
             elSub.textContent = 'Counter unavailable (no API configured)';
             return;
      }
      let method = "GET";
      if (!EASY_MODE) {
        method = (shouldPost() && !forceGet) ? "POST" : "GET";
      }
      const url = method === "POST" ? ENDPOINT + "?inc=1" : ENDPOINT;
      elSub.textContent = method === "POST" ? "Counting your visit…" : "Loading…";

      const res = await fetch(url, { method, mode:"cors", cache:"no-store", headers:{ "Accept":"application/json" } });
      if (!res.ok) throw new Error("HTTP "+res.status);
      const data = await res.json();
      const next = Number(data?.count ?? NaN);
      if (!Number.isFinite(next)) throw new Error("Invalid count");

      const current = Number((elValue.textContent || "").replace(/[^0-9]/g,"")) || 0;
      elValue.classList.remove("skeleton");

      if (EASY_MODE) {
        elValue.textContent = formatNumber(next);
      } else {
        countUp(elValue, current, next, 700);
      }

      elSub.textContent = "Last updated just now";
    }catch(err){
      console.error("visit counter error:", err);
      elValue.textContent = "—";
      elSub.textContent = "Couldn’t load counter";
    }
  }

  // ====== INIT ======
  document.addEventListener("DOMContentLoaded", () => {
    if (elBtn) elBtn.addEventListener("click", () => fetchCount({forceGet:true}));
    // Fetch on load
    fetchCount();
  });
})();
