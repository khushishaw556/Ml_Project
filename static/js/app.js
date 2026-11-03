/* ============================================================
   AI StudyMate — app.js
   Vanilla JS — no jQuery / React
   ============================================================ */

/* ─── Constants ──────────────────────────────────────────────────── */
const LABEL_COLOR = {
  'Good':               { ring: '#22e58b', badgeClass: 'badge-good' },
  'Average':            { ring: '#f5a524', badgeClass: 'badge-avg'  },
  'Needs Improvement':  { ring: '#f43f5e', badgeClass: 'badge-bad'  },
};

const SPLIT_COLORS = ['#7c3aed', '#22e58b', '#f5a524', '#f43f5e', '#60a5fa', '#e879f9'];

/* ─── State ──────────────────────────────────────────────────────── */
let coursesData = {};      // { course: [subjects] }
let planOpen    = false;

/* ─── DOM refs ───────────────────────────────────────────────────── */
const courseSelect    = document.getElementById('course-select');
const marksContainer  = document.getElementById('marks-container');
const hoursSlider     = document.getElementById('hours-slider');
const hoursDisplay    = document.getElementById('hours-display');
const analyzeForm     = document.getElementById('analyze-form');
const analyzeBtn      = document.getElementById('analyze-btn');
const btnLabel        = document.getElementById('btn-label');
const btnSpinner      = document.getElementById('btn-spinner');
const emptyState      = document.getElementById('empty-state');
const resultsContent  = document.getElementById('results-content');

/* ════════════════════════════════════════════════════════════════════
   1. On page load — fetch courses
════════════════════════════════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const res = await fetch('/api/courses');
    if (!res.ok) throw new Error('Failed to load courses');
    coursesData = await res.json();

    // Populate course <select>
    courseSelect.innerHTML = '';
    Object.keys(coursesData).forEach((course, i) => {
      const opt = document.createElement('option');
      opt.value = course;
      opt.textContent = course;
      if (i === 0) opt.selected = true;
      courseSelect.appendChild(opt);
    });

    // Render first course marks
    renderMarkInputs(courseSelect.value);
  } catch (err) {
    courseSelect.innerHTML = '<option value="">Error loading courses</option>';
    console.error(err);
  }
});

/* ════════════════════════════════════════════════════════════════════
   2. Course change → re-render subject mark inputs
════════════════════════════════════════════════════════════════════ */
courseSelect.addEventListener('change', () => {
  renderMarkInputs(courseSelect.value);
});

/**
 * Build number inputs for each subject of the selected course.
 * Empty default value for new user input.
 */
function renderMarkInputs(course) {
  const subjects = coursesData[course];
  if (!subjects || subjects.length === 0) {
    marksContainer.innerHTML = '<p class="muted-hint">No subjects found.</p>';
    return;
  }

  let html = '<div class="field-group"><label>Subject Marks <span style="font-weight:400;text-transform:none;letter-spacing:0">(Enter 0 – 100 for each)</span></label></div>';
  html += '<div class="marks-grid">';
  subjects.forEach(subj => {
    const id = `mark-${slugify(subj)}`;
    html += `
      <div class="mark-field">
        <label for="${id}" title="${subj}">${subj}</label>
        <input
          type="number"
          id="${id}"
          data-subject="${subj}"
          min="0" max="100" step="1"
          placeholder="e.g. 70"
          value=""
          class="mark-input"
          required
        />
      </div>`;
  });
  html += '</div>';
  marksContainer.innerHTML = html;
}

/* ════════════════════════════════════════════════════════════════════
   3. Study hours slider
════════════════════════════════════════════════════════════════════ */
hoursSlider.addEventListener('input', () => {
  hoursDisplay.textContent = `${parseFloat(hoursSlider.value).toFixed(1)} h`;
});

/* ════════════════════════════════════════════════════════════════════
   4. Form submit → POST /api/analyze
════════════════════════════════════════════════════════════════════ */
analyzeForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  const nameInput = document.getElementById('student-name');
  const studentName = nameInput.value.trim();
  if (!studentName) {
    nameInput.focus();
    alert('Please enter your full name.');
    return;
  }

  // Gather marks
  const markInputs = marksContainer.querySelectorAll('.mark-input');
  const marks = {};
  let valid = true;
  let firstInvalid = null;
  let missingSubject = null;

  markInputs.forEach(inp => {
    const raw = inp.value.trim();
    if (raw === '') {
      valid = false;
      inp.classList.add('input-error');
      if (!firstInvalid) {
        firstInvalid = inp;
        missingSubject = inp.dataset.subject;
      }
      return;
    }

    const val = parseFloat(raw);
    if (isNaN(val) || val < 0 || val > 100) {
      valid = false;
      inp.classList.add('input-error');
      if (!firstInvalid) {
        firstInvalid = inp;
        missingSubject = inp.dataset.subject;
      }
    } else {
      inp.classList.remove('input-error');
      marks[inp.dataset.subject] = val;
    }
  });

  if (!valid) {
    if (firstInvalid) firstInvalid.focus();
    if (missingSubject) {
      alert(`Please enter a valid score (0–100) for "${missingSubject}". All subjects are required.`);
    } else {
      alert('Please enter valid marks (0–100) for all subjects.');
    }
    return;
  }

  const payload = {
    name:   studentName,
    course: courseSelect.value,
    marks,
    hours:  parseFloat(hoursSlider.value),
  };

  // Show spinner
  setLoading(true);

  try {
    const res  = await fetch('/api/analyze', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload),
      signal: AbortSignal.timeout(60000),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || `Server error ${res.status}`);
    }

    const data = await res.json();
    renderResults(data);

    // Smooth scroll to results
    document.getElementById('results-panel').scrollIntoView({ behavior: 'smooth', block: 'start' });

  } catch (err) {
    let message = err.message;
    if (err.name === 'TimeoutError') {
      message = 'The analysis took too long. Please wait a moment and try again.';
    } else if (err instanceof TypeError && err.message.toLowerCase().includes('fetch')) {
      message = 'Cannot reach the Flask server. Make sure the app is running at http://localhost:5000, then try again.';
    }
    alert(`Analysis failed: ${message}`);
    console.error(err);
  } finally {
    setLoading(false);
  }
});

/* ════════════════════════════════════════════════════════════════════
   5. Render results
════════════════════════════════════════════════════════════════════ */
function renderResults(d) {
  // Hide empty state, show results
  emptyState.classList.add('hidden');
  resultsContent.classList.remove('hidden');
  resultsContent.classList.add('fade-in');

  // ── Hero banner ──────────────────────────────────────────────
  const heroBanner  = document.getElementById('hero-banner');
  const heroLabel   = document.getElementById('hero-label');
  const heroGreeting= document.getElementById('hero-greeting');
  const heroScore   = document.getElementById('hero-score');
  const heroPct     = document.getElementById('hero-pct');

  heroGreeting.textContent = `${d.name}, your overall performance is`;
  heroLabel.textContent    = d.overall_label;
  heroLabel.className      = 'hero-label ' + labelCssClass(d.overall_label);
  heroScore.textContent    = `${d.overall}%`;
  heroPct.textContent      = `${d.overall_pct.toFixed(0)}% of ${d.course}`;

  // Animate hero border color
  const borderColor = LABEL_COLOR[d.overall_label]?.ring || '#7c3aed';
  heroBanner.style.borderColor = borderColor + '80';

  // ── Subject cards ─────────────────────────────────────────────
  const grid = document.getElementById('subjects-grid');
  grid.innerHTML = '';

  d.subjects.forEach(subj => {
    const m    = d.marks[subj];
    const info = d.info[subj];
    const col  = LABEL_COLOR[info.label]?.ring || '#7c3aed';
    const bc   = LABEL_COLOR[info.label]?.badgeClass || 'badge-good';

    const card = document.createElement('div');
    card.className = 'subject-card fade-in';

    // SVG ring params
    const radius = 36;
    const circ   = 2 * Math.PI * radius;
    const pct    = Math.min(Math.max(m, 0), 100);
    const offset = circ - (pct / 100) * circ;

    card.innerHTML = `
      <div class="subject-name">${subj}</div>
      <div class="ring-wrap">
        <svg class="ring-svg" width="90" height="90" viewBox="0 0 90 90">
          <circle class="ring-track" cx="45" cy="45" r="${radius}" />
          <circle
            class="ring-fill"
            cx="45" cy="45" r="${radius}"
            stroke="${col}"
            stroke-dasharray="${circ.toFixed(1)}"
            stroke-dashoffset="${circ.toFixed(1)}"
            data-offset="${offset.toFixed(1)}"
          />
        </svg>
        <div class="ring-center">${Math.round(m)}</div>
      </div>
      <span class="badge ${bc}">${info.label}</span>
      <div class="subject-meta">
        Expected: ${info.expected}<br/>
        Top ${(100 - info.percentile).toFixed(0)}%
      </div>
    `;
    grid.appendChild(card);
  });

  // Animate rings after a short delay (so they're painted first)
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      grid.querySelectorAll('.ring-fill').forEach(ring => {
        ring.style.strokeDashoffset = ring.dataset.offset;
      });
    });
  });

  // ── Study plan ────────────────────────────────────────────────
  const worst     = d.worst;
  const worstInfo = d.info[worst];

  document.getElementById('plan-focus').innerHTML =
    `Focus most on: <b style="color:#c4b5fd">${worst}</b> — ` +
    `need +${worstInfo.need} marks to reach target ${worstInfo.target}`;

  // Hour splits bars
  const splitsEl = document.getElementById('plan-splits');
  splitsEl.innerHTML = '';
  const maxHours = Math.max(...Object.values(d.split));

  d.subjects.slice(0, 3).forEach((subj, i) => {
    const h    = d.split[subj];
    const pct  = (h / maxHours) * 100;
    const col  = SPLIT_COLORS[i % SPLIT_COLORS.length];
    splitsEl.innerHTML += `
      <div class="split-row">
        <span class="split-subj">${subj}</span>
        <div class="split-bar-wrap">
          <div class="split-bar" style="width:${pct}%;background:${col}"></div>
        </div>
        <span class="split-hours">${h} h</span>
      </div>`;
  });

  // Full plan list
  const planList = document.getElementById('plan-list');
  planList.innerHTML = '';
  d.plan.forEach((item, i) => {
    const li = document.createElement('li');
    li.className = 'plan-item';
    // Extract "Day X:" prefix
    const match = item.match(/^(Day \d+:?)\s*(.*)/i);
    if (match) {
      li.innerHTML = `<span class="plan-day">${match[1]}</span><span>${match[2]}</span>`;
    } else {
      li.innerHTML = `<span class="plan-day">Day ${i+1}:</span><span>${item}</span>`;
    }
    planList.appendChild(li);
  });

  // Reset toggle state
  planOpen = false;
  planList.classList.add('hidden');
  document.getElementById('plan-toggle').textContent = 'View Full Plan ▾';

  // ── Key Insights ──────────────────────────────────────────────
  const insightsList = document.getElementById('insights-list');
  const insights = [
    { icon: '🏆', text: `Best Subject: <b>${d.best} (${d.marks[d.best]})</b>` },
    { icon: '⚠️', text: `Weakest Subject: <b>${d.worst} (${d.marks[d.worst]})</b>` },
    { icon: '🔴', text: `Needs Improvement: <b>${d.low_subjects.length ? d.low_subjects.join(', ') : 'None'}</b>` },
    { icon: '🟠', text: `Average subjects: <b>${d.avg_subjects.length ? d.avg_subjects.join(', ') : 'None'}</b>` },
    { icon: '📉', text: `Below expected: <b>${d.below_expected.length ? d.below_expected.join(', ') : 'None'}</b>` },
    { icon: '⭐', text: `Overall Strength: <b>${d.overall_label}</b>` },
  ];

  insightsList.innerHTML = insights.map(({ icon, text }) =>
    `<li class="insight-item">
       <span class="insight-icon">${icon}</span>
       <span class="insight-text">${text}</span>
     </li>`
  ).join('');

  // ── Next Steps ────────────────────────────────────────────────
  const weakNames = [...d.low_subjects, ...d.avg_subjects].slice(0, 2).join(', ') || 'all subjects';
  const steps = [
    `Focus on weak subjects: <b>${weakNames}</b>`,
    'Take <b>mock tests</b> at least twice a week',
    'Strengthen <b>core concepts</b> before solving advanced problems',
    'Track your progress <b>weekly</b> and adjust the plan',
  ];

  document.getElementById('next-steps-list').innerHTML = steps.map((text, i) =>
    `<li class="step-item">
       <span class="step-num">${i + 1}</span>
       <span class="step-text">${text}</span>
     </li>`
  ).join('');

  // ── Learning Resources (based on analysis) ─────────────────────
  renderResources(d.recommended_resources);
}

/* ════════════════════════════════════════════════════════════════════
   6. Toggle study plan
════════════════════════════════════════════════════════════════════ */
function togglePlan() {
  planOpen = !planOpen;
  const list   = document.getElementById('plan-list');
  const toggle = document.getElementById('plan-toggle');
  list.classList.toggle('hidden', !planOpen);
  toggle.textContent = planOpen ? 'Hide Plan ▴' : 'View Full Plan ▾';
}

/* ════════════════════════════════════════════════════════════════════
   6.5. Render Learning Resources (Categorized by Weak & Strong Areas)
════════════════════════════════════════════════════════════════════ */
function getResourceIcon(type) {
  const t = (type || '').toLowerCase();
  if (t.includes('video') || t.includes('lecture')) return '🎥';
  if (t.includes('interactive') || t.includes('practice') || t.includes('coding') || t.includes('challenge') || t.includes('lab')) return '💻';
  if (t.includes('doc') || t.includes('notes') || t.includes('book') || t.includes('guide') || t.includes('textbook')) return '📖';
  if (t.includes('project') || t.includes('deep dive') || t.includes('advanced')) return '🚀';
  return '🔗';
}

function renderResources(resourcesList) {
  const container = document.getElementById('resources-container');
  if (!container) return;

  if (!resourcesList || resourcesList.length === 0) {
    container.innerHTML = '<p class="muted-hint">No recommendations available for this selection.</p>';
    return;
  }

  // Count priorities
  const highCount = resourcesList.filter(r => r.label === 'Needs Improvement').length;
  const medCount  = resourcesList.filter(r => r.label === 'Average').length;
  const goodCount = resourcesList.filter(r => r.label === 'Good').length;

  let html = `
    <div class="resources-toolbar">
      <div class="resources-filter-tabs">
        <button class="res-tab active" data-filter="all">All Subjects (${resourcesList.length})</button>
        ${highCount > 0 ? `<button class="res-tab tab-high" data-filter="Needs Improvement">🚨 Focus First (${highCount})</button>` : ''}
        ${medCount > 0 ? `<button class="res-tab tab-med" data-filter="Average">⚡ Practice & Review (${medCount})</button>` : ''}
        ${goodCount > 0 ? `<button class="res-tab tab-good" data-filter="Good">⭐ Advanced Mastery (${goodCount})</button>` : ''}
      </div>
    </div>
    <div class="resources-groups-grid">
  `;

  resourcesList.forEach((group) => {
    const isWeak = group.label === 'Needs Improvement';
    const borderStyle = isWeak ? 'border-color: rgba(244, 63, 94, 0.4);' : '';

    html += `
      <div class="subject-res-card fade-in" data-category="${group.label}" style="${borderStyle}">
        <div class="subject-res-head">
          <div class="subject-res-title-col">
            <div class="subject-res-title-row">
              <span class="subject-res-name">${group.subject}</span>
              <span class="badge ${group.priority_class}">${group.priority_badge}</span>
            </div>
            <div class="subject-res-meta">
              Score: <strong class="${isWeak ? 'accent-red' : (group.label === 'Average' ? 'accent-yellow' : 'accent-green')}">${Math.round(group.score)}%</strong>
              &nbsp;&bull;&nbsp;
              ${isWeak
                ? `<span class="target-alert">Need +${group.need} to hit target (${group.target}%)</span>`
                : `<span class="target-info">Target: ${group.target}%</span>`}
            </div>
          </div>
        </div>

        <div class="res-items-grid">
          ${group.resources.map(res => `
            <a href="${res.url}" target="_blank" rel="noopener noreferrer" class="res-item-card">
              <div class="res-item-header">
                <span class="res-type-badge">${getResourceIcon(res.type)} ${res.type}</span>
                <span class="res-arrow">↗</span>
              </div>
              <div class="res-item-title">${res.title}</div>
              <div class="res-item-desc">${res.desc}</div>
            </a>
          `).join('')}
        </div>
      </div>
    `;
  });

  html += '</div>';
  container.innerHTML = html;

  // Tab filtering behavior
  const tabs = container.querySelectorAll('.res-tab');
  const cards = container.querySelectorAll('.subject-res-card');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const filter = tab.dataset.filter;

      cards.forEach(card => {
        if (filter === 'all' || card.dataset.category === filter) {
          card.classList.remove('hidden');
        } else {
          card.classList.add('hidden');
        }
      });
    });
  });
}

/* ════════════════════════════════════════════════════════════════════
   7. Helpers
════════════════════════════════════════════════════════════════════ */

/** Map performance label → CSS class suffix */
function labelCssClass(label) {
  if (label === 'Good')              return 'good';
  if (label === 'Average')           return 'avg';
  if (label === 'Needs Improvement') return 'bad';
  return '';
}

/** Simple slug for element IDs */
function slugify(str) {
  return str.toLowerCase().replace(/[^a-z0-9]+/g, '-');
}

/** Show/hide loading state on the Analyze button */
function setLoading(on) {
  analyzeBtn.disabled = on;
  btnLabel.classList.toggle('hidden', on);
  btnSpinner.classList.toggle('hidden', !on);
}
