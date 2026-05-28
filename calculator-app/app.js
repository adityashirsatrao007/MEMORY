/**
 * Calculator App — app.js
 * Features: chained operations, keyboard support, history log, error handling,
 *           auto-sizing display text, press animations, full accessibility.
 */

'use strict';

// ─── State ───────────────────────────────────────────────────────────────────
const state = {
  current: '0',
  previous: '',
  operator: null,
  expression: '',
  justComputed: false,
  replaceNext: false,
  history: [],
  historyOpen: false,
};

// ─── DOM ─────────────────────────────────────────────────────────────────────
const $ = (id) => document.getElementById(id);

const resultRow    = $('resultRow');
const expressionRow= $('expressionRow');
const historyList  = $('historyList');
const historyEmpty = $('historyEmpty');
const historyPanel = $('historyPanel');
const historyToggle= $('historyToggle');
const clearHistBtn = $('clearHistoryBtn');
const acKey        = $('key-ac');

// ─── Helpers ─────────────────────────────────────────────────────────────────

function formatNumber(num) {
  if (!isFinite(num)) return num > 0 ? '∞' : num < 0 ? '-∞' : 'Error';
  if (isNaN(num)) return 'Error';
  const abs = Math.abs(num);
  if (abs !== 0 && (abs >= 1e10 || abs < 1e-6)) {
    return parseFloat(num.toPrecision(8)).toExponential();
  }
  return parseFloat(num.toPrecision(10)).toString();
}

function fitText(text) {
  const len = text.length;
  if      (len <= 8)  resultRow.style.fontSize = '54px';
  else if (len <= 12) resultRow.style.fontSize = '40px';
  else if (len <= 16) resultRow.style.fontSize = '30px';
  else                resultRow.style.fontSize = '22px';
}

function compute(a, op, b) {
  a = parseFloat(a);
  b = parseFloat(b);
  switch (op) {
    case '+': return a + b;
    case '−': return a - b;
    case '×': return a * b;
    case '÷': return b === 0 ? NaN : a / b;
    default:  return b;
  }
}

function escapeHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// ─── Render ───────────────────────────────────────────────────────────────────

function render() {
  resultRow.textContent = state.current;
  fitText(state.current);
  expressionRow.textContent = state.expression;

  // AC vs C
  acKey.textContent =
    (state.current !== '0' || state.operator || state.previous) ? 'C' : 'AC';

  // Highlight active operator
  document.querySelectorAll('.key--operator').forEach((btn) => {
    btn.classList.toggle(
      'selected',
      btn.dataset.value === state.operator && !state.justComputed
    );
  });
}

function animatePulse() {
  resultRow.classList.remove('pulse');
  void resultRow.offsetWidth;
  resultRow.classList.add('pulse');
  resultRow.addEventListener('animationend', () => resultRow.classList.remove('pulse'), { once: true });
}

function animateShake() {
  resultRow.classList.remove('shake');
  void resultRow.offsetWidth;
  resultRow.classList.add('shake');
  resultRow.addEventListener('animationend', () => resultRow.classList.remove('shake'), { once: true });
}

// ─── Actions ─────────────────────────────────────────────────────────────────

function handleDigit(digit) {
  if (state.current === 'Error') {
    handleAC();
    return;
  }

  if (state.justComputed || state.replaceNext) {
    state.current = digit === '0' ? '0' : digit;
    if (state.justComputed) {
      state.expression = '';
      state.operator = null;
      state.previous = '';
      state.justComputed = false;
    }
    state.replaceNext = false;
  } else if (state.current === '0' && digit !== '.') {
    state.current = digit;
  } else {
    if (state.current.replace('-', '').replace('.', '').length >= 12) return;
    state.current += digit;
  }
  render();
}

function handleDecimal() {
  if (state.current === 'Error') return;

  if (state.justComputed || state.replaceNext) {
    state.current = '0.';
    if (state.justComputed) {
      state.expression = '';
      state.operator = null;
      state.previous = '';
      state.justComputed = false;
    }
    state.replaceNext = false;
  } else if (!state.current.includes('.')) {
    state.current += '.';
  }
  render();
}

function handleOperator(op) {
  if (state.current === 'Error') return;

  // Chain operations: if we already have a pending op and a real b, compute first
  if (state.operator && !state.replaceNext && state.previous !== '') {
    const result = compute(state.previous, state.operator, state.current);
    const formatted = formatNumber(result);
    if (formatted === 'Error' || isNaN(result)) {
      animateShake();
      state.current = 'Error';
      state.expression = '';
      state.operator = null;
      state.previous = '';
      state.justComputed = false;
      state.replaceNext = false;
      render();
      return;
    }
    state.current = formatted;
    state.expression = formatted + ' ' + op;
    state.previous = formatted;
  } else {
    state.expression = state.current + ' ' + op;
    state.previous = state.current;
  }

  state.operator = op;
  state.justComputed = false;
  state.replaceNext = true;
  render();
}

function handleEquals() {
  if (state.current === 'Error') { handleAC(); return; }
  if (!state.operator || state.previous === '') { animatePulse(); return; }

  const b = state.replaceNext ? state.previous : state.current;
  const fullExpr = state.expression + ' ' + (state.replaceNext ? '' : state.current);
  const result = compute(state.previous, state.operator, b);
  const formatted = formatNumber(result);

  if (formatted === 'Error' || isNaN(result)) {
    animateShake();
    state.current = 'Error';
    state.expression = '';
    state.operator = null;
    state.previous = '';
    state.justComputed = true;
    state.replaceNext = false;
    render();
    return;
  }

  const expr = state.expression.trimEnd() + (state.replaceNext ? '' : ' ' + b);
  pushHistory(expr.trim(), formatted);

  state.current = formatted;
  state.expression = expr.trim() + ' =';
  state.operator = null;
  state.previous = '';
  state.justComputed = true;
  state.replaceNext = false;
  animatePulse();
  render();
}

function handleAC() {
  state.current = '0';
  state.previous = '';
  state.operator = null;
  state.expression = '';
  state.justComputed = false;
  state.replaceNext = false;
  render();
}

function handleSign() {
  if (state.current === '0' || state.current === 'Error') return;
  state.current = state.current.startsWith('-')
    ? state.current.slice(1)
    : '-' + state.current;
  render();
}

function handlePercent() {
  const val = parseFloat(state.current);
  if (isNaN(val)) return;
  state.current = formatNumber(val / 100);
  // Remove trailing dot if any
  if (state.current.endsWith('.')) state.current = state.current.slice(0, -1);
  render();
}

function handleBackspace() {
  if (state.current === 'Error' || state.justComputed) { handleAC(); return; }
  if (state.current.length <= 1 ||
     (state.current.length === 2 && state.current.startsWith('-'))) {
    state.current = '0';
  } else {
    state.current = state.current.slice(0, -1);
    // Clean trailing dot
    if (state.current === '-' || state.current === '-0') state.current = '0';
  }
  render();
}

// ─── History ─────────────────────────────────────────────────────────────────

function pushHistory(expr, result) {
  state.history.unshift({ expr, result });
  if (state.history.length > 50) state.history.pop();
  renderHistory();
}

function renderHistory() {
  historyEmpty.style.display = state.history.length === 0 ? '' : 'none';

  // Remove old items (leave the empty placeholder)
  historyList.querySelectorAll('.history-item').forEach((el) => el.remove());

  state.history.forEach((item, i) => {
    const li = document.createElement('li');
    li.className = 'history-item';
    li.setAttribute('role', 'button');
    li.setAttribute('tabindex', '0');
    li.setAttribute('aria-label', `Recall result ${item.result}`);
    li.innerHTML = `
      <div class="history-item-expr">${escapeHtml(item.expr)}</div>
      <div class="history-item-result">${escapeHtml(item.result)}</div>
    `;
    li.addEventListener('click', () => recallHistory(i));
    li.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); recallHistory(i); }
    });
    historyList.appendChild(li);
  });
}

function recallHistory(index) {
  const item = state.history[index];
  if (!item) return;
  state.current = item.result;
  state.expression = item.expr + ' =';
  state.operator = null;
  state.previous = '';
  state.justComputed = true;
  state.replaceNext = false;
  animatePulse();
  render();
}

function clearHistory() {
  state.history = [];
  renderHistory();
}

// ─── Toggle History Panel ─────────────────────────────────────────────────────

function toggleHistory() {
  state.historyOpen = !state.historyOpen;
  historyPanel.classList.toggle('open', state.historyOpen);
  historyToggle.classList.toggle('active', state.historyOpen);
  historyToggle.setAttribute('aria-pressed', String(state.historyOpen));
}

historyToggle.addEventListener('click', toggleHistory);
clearHistBtn.addEventListener('click', clearHistory);

// ─── Keypad Click Handler ─────────────────────────────────────────────────────

document.querySelector('.keypad').addEventListener('click', (e) => {
  const btn = e.target.closest('[data-action]');
  if (!btn) return;

  switch (btn.dataset.action) {
    case 'digit':    handleDigit(btn.dataset.value); break;
    case 'decimal':  handleDecimal(); break;
    case 'operator': handleOperator(btn.dataset.value); break;
    case 'equals':   handleEquals(); break;
    case 'ac':       handleAC(); break;
    case 'sign':     handleSign(); break;
    case 'percent':  handlePercent(); break;
  }

  flashButton(btn);
});

// ─── Keyboard Support ─────────────────────────────────────────────────────────

const keyMap = {
  '0': () => handleDigit('0'),
  '1': () => handleDigit('1'),
  '2': () => handleDigit('2'),
  '3': () => handleDigit('3'),
  '4': () => handleDigit('4'),
  '5': () => handleDigit('5'),
  '6': () => handleDigit('6'),
  '7': () => handleDigit('7'),
  '8': () => handleDigit('8'),
  '9': () => handleDigit('9'),
  '.': handleDecimal,
  ',': handleDecimal,
  '+': () => handleOperator('+'),
  '-': () => handleOperator('−'),
  '*': () => handleOperator('×'),
  '/': () => handleOperator('÷'),
  'Enter': handleEquals,
  '=': handleEquals,
  'Escape': handleAC,
  'Backspace': handleBackspace,
  'Delete': handleAC,
  '%': handlePercent,
  'h': toggleHistory,
};

const keyToButtonId = {
  '0':'key-0','1':'key-1','2':'key-2','3':'key-3','4':'key-4',
  '5':'key-5','6':'key-6','7':'key-7','8':'key-8','9':'key-9',
  '.':'key-decimal',',':'key-decimal',
  '+':'key-add','-':'key-subtract','*':'key-multiply','/':'key-divide',
  'Enter':'key-equals','=':'key-equals',
  'Escape':'key-ac','Delete':'key-ac','Backspace':'key-ac',
  '%':'key-percent',
};

document.addEventListener('keydown', (e) => {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
  if (e.metaKey || e.ctrlKey || e.altKey) return;

  const handler = keyMap[e.key];
  if (handler) {
    e.preventDefault();
    handler();
    const btnId = keyToButtonId[e.key];
    if (btnId) flashButton($(btnId));
  }
});

function flashButton(btn) {
  if (!btn) return;
  btn.style.transform = 'scale(0.93)';
  setTimeout(() => { btn.style.transform = ''; }, 120);
}

// ─── Init ─────────────────────────────────────────────────────────────────────
render();
