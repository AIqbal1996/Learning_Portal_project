(() => {
  const app = document.getElementById("app");
  const navButtons = Array.from(document.querySelectorAll("[data-route]"));
  const personaButtons = Array.from(document.querySelectorAll("[data-persona]"));
  const commandModal = document.getElementById("commandModal");
  const globalSearch = document.getElementById("globalSearch");
  const commandResults = document.getElementById("commandResults");

  const state = {
    route: location.hash.replace("#", "") || "home",
    persona: localStorage.getItem("learningPersona") || "student",
    courses: [],
    workbookCache: {},
    category: "All",
    search: ""
  };

  const personaCopy = {
    student: {
      eyebrow: "Student-ready learning experience",
      title: "Build job-ready skills with a premium academy experience.",
      copy: "A clean, guided interface helps ambitious university students move from discovery to action without feeling overwhelmed.",
      primaryCta: "Explore courses",
      secondaryCta: "View assessments"
    },
    enterprise: {
      eyebrow: "Enterprise-grade upskilling hub",
      title: "Accelerate workforce capability with measurable learning paths.",
      copy: "Corporate learners get role-based pathways, reduced cognitive friction, and clear progress signals that support retention and completion.",
      primaryCta: "Review learning paths",
      secondaryCta: "Open pilot tracker"
    }
  };

  init();

  async function init() {
    setPersona(state.persona, false);
    attachEvents();
    state.courses = await window.LearningDataService.getCourses();
    await render();
  }

  function attachEvents() {
    window.addEventListener("hashchange", () => {
      state.route = location.hash.replace("#", "") || "home";
      render();
    });

    navButtons.forEach(button => {
      button.addEventListener("click", () => go(button.dataset.route));
      button.addEventListener("keydown", event => {
        if (event.key === "Enter" || event.key === " ") go(button.dataset.route);
      });
    });

    personaButtons.forEach(button => button.addEventListener("click", () => {
      setPersona(button.dataset.persona, true);
      render();
    }));

    document.getElementById("openCommand").addEventListener("click", openCommand);
    document.querySelectorAll("[data-close-modal]").forEach(el => el.addEventListener("click", closeCommand));
    document.addEventListener("keydown", event => {
      const isCommand = (event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k";
      if (isCommand) {
        event.preventDefault();
        openCommand();
      }
      if (event.key === "Escape") closeCommand();
    });
    globalSearch.addEventListener("input", renderCommandResults);
  }

  function go(route) {
    location.hash = route === "home" ? "" : route;
  }

  function setPersona(persona, persist) {
    state.persona = persona;
    if (persist) localStorage.setItem("learningPersona", persona);
    personaButtons.forEach(btn => btn.classList.toggle("active", btn.dataset.persona === persona));
  }

  async function render() {
    navButtons.forEach(btn => btn.classList.toggle("active", btn.dataset.route === state.route || (state.route === "" && btn.dataset.route === "home")));
    app.innerHTML = "";
    app.focus({ preventScroll: true });
    if (state.route === "courses") return renderCourses();
    if (state.route === "training") return renderWorkbook("training");
    if (state.route === "pilots") return renderWorkbook("pilots");
    if (state.route === "assessments") return renderWorkbook("assessments");
    return renderHome();
  }

  async function renderHome() {
    const summary = await window.LearningDataService.getSummary();
    const copy = personaCopy[state.persona];
    app.innerHTML = `
      <section class="hero-panel">
        <div>
          <p class="eyebrow">${copy.eyebrow}</p>
          <h1 class="hero-title">${copy.title.replace("premium", "<span>premium</span>").replace("measurable", "<span>measurable</span>")}</h1>
          <p class="hero-copy">${copy.copy}</p>
          <div class="hero-actions">
            <button class="primary-button" data-action="primaryHero">${copy.primaryCta}</button>
            <button class="secondary-button" data-action="secondaryHero">${copy.secondaryCta}</button>
          </div>
          <div class="trust-row" aria-label="Trust indicators">
            <span><strong>Coursera-style UX</strong> with enterprise polish</span>
            <span><strong>Search-first</strong> content discovery</span>
            <span><strong>Role-ready</strong> learning paths</span>
          </div>
        </div>
        <aside class="insight-card" aria-label="Learning focus snapshot">
          <h3>Capability snapshot</h3>
          <div class="progress-list">
            ${progressItem("Course discovery", 92)}
            ${progressItem("Assessment visibility", 78)}
            ${progressItem("Pilot readiness", 68)}
            ${progressItem("Enterprise adoption", 84)}
          </div>
        </aside>
      </section>

      ${summaryStats(summary)}

      <section class="section-heading">
        <div>
          <h2>Designed for two audiences, one platform</h2>
          <p>Students need momentum and clarity. Corporate employees need credibility, relevance, and proof of value. The V2 interface supports both through persona-based copy, structured paths, and reduced decision fatigue.</p>
        </div>
      </section>

      <div class="card-grid">
        ${featureCard("🎯", "Guided discovery", "Chunked course cards and category filters reduce cognitive load and let learners find the next useful action quickly.")}
        ${featureCard("🏢", "Enterprise confidence", "Executive-grade spacing, restrained color, data cards, and clean table layouts make the portal feel trustworthy.")}
        ${featureCard("📈", "Retention nudges", "Progress cues, duration labels, and visible outcomes increase commitment before launching a course.")}
      </div>

      <section class="section-heading">
        <div>
          <h2>Recommended learning paths</h2>
          <p>Executive-friendly path cards show how the raw course inventory can become a strategy-led academy.</p>
        </div>
      </section>
      <div class="card-grid">
        ${pathCard("University launchpad", "SQL → Power BI → Data Engineering Foundations", "For final-year students building job-ready portfolios.")}
        ${pathCard("Enterprise data engineer", "ETL → Spark → Cloud Data → Governance", "For teams moving from support work to production delivery.")}
        ${pathCard("Assessment readiness", "HackerRank practice → remediation → role validation", "For measurable skill benchmarking and cohort reporting.")}
      </div>
    `;

    app.querySelector("[data-action='primaryHero']").addEventListener("click", () => go(state.persona === "enterprise" ? "training" : "courses"));
    app.querySelector("[data-action='secondaryHero']").addEventListener("click", () => go(state.persona === "enterprise" ? "pilots" : "assessments"));
  }

  function renderCourses() {
    const categories = ["All", ...Object.keys(window.LearningDataService.categoryMapping)];
    const filtered = getFilteredCourses();
    const totalHours = filtered.reduce((sum, course) => sum + course.durationHours, 0);
    const avgHours = filtered.length ? Math.round(totalHours / filtered.length) : 0;

    app.innerHTML = `
      <section class="section-heading">
        <div>
          <p class="eyebrow">Course catalog</p>
          <h2>Premium course discovery</h2>
          <p>Search, filter, scan duration, understand level, and launch the right course with minimal friction.</p>
        </div>
      </section>
      <div class="filter-bar">
        <label class="visually-hidden" for="courseSearch">Search Course</label>
        <input id="courseSearch" class="search-input" type="search" value="${escapeHtml(state.search)}" placeholder="Search courses, cloud, SQL, Spark..." />
        <div class="chip-row" aria-label="Course categories">
          ${categories.map(category => `<button class="chip ${category === state.category ? "active" : ""}" data-category="${escapeHtml(category)}">${category}</button>`).join("")}
        </div>
      </div>
      <div class="stat-grid">
        ${statCard("Visible courses", filtered.length, "Filtered result count")}
        ${statCard("Learning hours", `${totalHours}`, "Total available duration")}
        ${statCard("Avg. hours", `${avgHours}`, "Effort planning cue")}
        ${statCard("Categories", categories.length - 1, "Skill filters available")}
      </div>
      <section class="course-grid" aria-label="Course results">
        ${filtered.length ? filtered.map(courseCard).join("") : emptyState("No courses found", "Try clearing search or selecting another category.")}
      </section>
    `;

    app.querySelector("#courseSearch").addEventListener("input", event => {
      state.search = event.target.value;
      renderCourses();
    });
    app.querySelectorAll("[data-category]").forEach(btn => btn.addEventListener("click", () => {
      state.category = btn.dataset.category;
      renderCourses();
    }));
  }

  function getFilteredCourses() {
    const query = state.search.trim().toLowerCase();
    return state.courses.filter(course => {
      const categoryMatch = state.category === "All" || course.category === state.category;
      const searchMatch = !query || [course.name, course.category, course.level, course.description].some(value => String(value).toLowerCase().includes(query));
      return categoryMatch && searchMatch;
    });
  }

  async function renderWorkbook(type) {
    if (!state.workbookCache[type]) state.workbookCache[type] = await window.LearningDataService.getWorkbook(type);
    const workbook = state.workbookCache[type];
    const activeSheet = workbook.activeSheet || workbook.sheets?.[0]?.name || "";
    const sheet = workbook.sheets?.find(item => item.name === activeSheet) || workbook.sheets?.[0] || { name: "No sheet", rows: [] };
    const rows = sheet.rows || [];
    const query = workbook.search || "";
    const filteredRows = filterRows(rows, query);

    app.innerHTML = `
      <section class="section-heading">
        <div>
          <p class="eyebrow">${escapeHtml(workbook.title || type)}</p>
          <h2>${escapeHtml(workbook.title || type)}</h2>
          <p>${escapeHtml(workbook.subtitle || "Search and export source records in a clean enterprise table.")}</p>
        </div>
      </section>
      <section class="table-panel">
        <div class="panel-toolbar">
          <label class="visually-hidden" for="workbookSearch">Search workbook</label>
          <input id="workbookSearch" class="search-input" type="search" value="${escapeHtml(query)}" placeholder="Search across all visible rows..." />
          <button class="secondary-button" data-download-csv>Download CSV</button>
        </div>
        <div class="tabs" role="tablist" aria-label="Workbook sheets">
          ${(workbook.sheets || []).map(item => `<button class="tab-button ${item.name === sheet.name ? "active" : ""}" data-sheet="${escapeHtml(item.name)}">${escapeHtml(item.name)}</button>`).join("")}
        </div>
        <div class="table-wrap">
          ${renderTable(filteredRows)}
        </div>
      </section>
    `;

    app.querySelector("#workbookSearch").addEventListener("input", event => {
      workbook.search = event.target.value;
      renderWorkbook(type);
    });
    app.querySelectorAll("[data-sheet]").forEach(btn => btn.addEventListener("click", () => {
      workbook.activeSheet = btn.dataset.sheet;
      renderWorkbook(type);
    }));
    app.querySelector("[data-download-csv]").addEventListener("click", () => downloadCsv(`${type}-${sheet.name}.csv`, filteredRows));
  }

  function renderTable(rows) {
    if (!rows.length) return emptyState("No rows found", "Try another search term or select a different sheet.");
    const columns = Array.from(rows.reduce((set, row) => {
      Object.keys(row).forEach(key => set.add(key));
      return set;
    }, new Set()));
    return `
      <table>
        <thead><tr>${columns.map(col => `<th>${escapeHtml(col)}</th>`).join("")}</tr></thead>
        <tbody>
          ${rows.map(row => `<tr>${columns.map(col => `<td>${formatCell(row[col])}</td>`).join("")}</tr>`).join("")}
        </tbody>
      </table>
    `;
  }

  function filterRows(rows, query) {
    const q = String(query || "").trim().toLowerCase();
    if (!q) return rows;
    return rows.filter(row => Object.values(row).some(value => String(value ?? "").toLowerCase().includes(q)));
  }

  function openCommand() {
    commandModal.hidden = false;
    globalSearch.value = "";
    renderCommandResults();
    setTimeout(() => globalSearch.focus(), 0);
  }

  function closeCommand() {
    commandModal.hidden = true;
  }

  function renderCommandResults() {
    const query = globalSearch.value.trim().toLowerCase();
    const results = state.courses
      .filter(course => !query || [course.name, course.category, course.level].some(value => String(value).toLowerCase().includes(query)))
      .slice(0, 8);
    commandResults.innerHTML = results.length ? results.map(course => `
      <button class="result-item" data-result-course="${course.id}">
        <span><strong>${escapeHtml(course.name)}</strong><span>${escapeHtml(course.category)} · ${course.durationHours} hours · ${escapeHtml(course.level)}</span></span>
        <span class="meta-pill">Open</span>
      </button>
    `).join("") : emptyState("No matching courses", "Search another keyword or open the full catalog.");
    commandResults.querySelectorAll("[data-result-course]").forEach(item => item.addEventListener("click", () => {
      state.search = state.courses.find(course => course.id === item.dataset.resultCourse)?.name || "";
      state.category = "All";
      closeCommand();
      go("courses");
    }));
  }

  function progressItem(label, value) {
    return `
      <div class="progress-item">
        <div class="progress-meta"><span>${label}</span><span>${value}%</span></div>
        <div class="progress-track"><div class="progress-fill" style="width:${value}%"></div></div>
      </div>
    `;
  }

  function summaryStats(summary) {
    return `
      <div class="stat-grid">
        ${statCard("Courses", summary.totalCourses, "Catalog records")}
        ${statCard("Hours", Math.round(summary.totalHours), "Learning effort")}
        ${statCard("Skill areas", summary.totalCategories, "Discovery filters")}
        ${statCard("Readiness", `${summary.completionFocus}%`, "Presentation score")}
      </div>
    `;
  }

  function statCard(label, value, caption) {
    return `<article class="stat-card"><p class="stat-label">${label}</p><p class="stat-value">${value}</p><p class="stat-caption">${caption}</p></article>`;
  }

  function featureCard(icon, title, copy) {
    return `<article class="feature-card"><div class="feature-icon">${icon}</div><h3>${title}</h3><p>${copy}</p></article>`;
  }

  function pathCard(title, sequence, copy) {
    return `<article class="path-card"><h3>${title}</h3><p><strong>${sequence}</strong></p><p>${copy}</p><button class="secondary-button" onclick="location.hash='courses'">View courses</button></article>`;
  }

  function courseCard(course) {
    const href = course.link || "#";
    const disabled = !course.link;
    return `
      <article class="course-card">
        <h3>${escapeHtml(course.name)}</h3>
        <div class="course-meta">
          <span class="meta-pill">${escapeHtml(course.category)}</span>
          <span class="meta-pill">${course.durationHours} hours</span>
          <span class="meta-pill">${escapeHtml(course.level)}</span>
        </div>
        <p class="course-description">${escapeHtml(course.description)}</p>
        <div class="course-footer">
          <a class="primary-button" href="${escapeAttribute(href)}" target="_blank" rel="noopener" ${disabled ? "aria-disabled='true' onclick='return false'" : ""}>Launch</a>
          <a class="tiny-link" href="#assessments">Assess readiness</a>
        </div>
      </article>
    `;
  }

  function emptyState(title, copy) {
    return `<div class="empty-state"><strong>${escapeHtml(title)}</strong>${escapeHtml(copy)}</div>`;
  }

  function formatCell(value) {
    if (value === null || value === undefined || value === "") return "—";
    const text = String(value);
    const url = text.match(/https?:\/\/\S+/)?.[0];
    if (url) return `<a class="tiny-link" href="${escapeAttribute(url)}" target="_blank" rel="noopener">Open link</a>`;
    return escapeHtml(text);
  }

  function downloadCsv(filename, rows) {
    if (!rows.length) return;
    const columns = Array.from(rows.reduce((set, row) => {
      Object.keys(row).forEach(key => set.add(key));
      return set;
    }, new Set()));
    const csv = [columns.join(","), ...rows.map(row => columns.map(col => csvEscape(row[col])).join(","))].join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename.replace(/\s+/g, "-").toLowerCase();
    link.click();
    URL.revokeObjectURL(url);
  }

  function csvEscape(value) {
    const text = String(value ?? "");
    return /[",\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
  }

  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function escapeAttribute(value) {
    return escapeHtml(value).replace(/`/g, "&#096;");
  }
})();
