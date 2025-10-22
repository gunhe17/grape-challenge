/**
 * Grove Page Logic
 * 과수원 페이지의 비즈니스 로직과 이벤트 핸들러
 */

import { getStageInfo, getStatusImage, isImageUrl, calculateProgress, formatDate } from '../utils/helpers.js';
import { FRUIT_STATUS } from '../utils/constants.js';
import { AuthAPI } from '../api/authApi.js';

// ========================
// State Management
// ========================
const state = {
  currentFruit: null,
  completedFruits: [],
  groveMode: 'my', // 'my', 'cell', or 'other-cell'
  selectedCell: null,
  allCells: []
};

// ========================
// DOM Elements Cache
// ========================
const elements = {
  // buttons
  logoutBtn: null,
  groveModeButton: null,
  gridBtn: null,
  basketBtn: null,

  // containers
  groveModeMenu: null,
  otherCellsContainer: null,
  gridView: null,
  basketView: null,

  // text elements
  groveModeText: null,
  statsText: null,

  // cards
  currentTreeCard: null,
  currentTreeEmoji: null,
  currentTreeProgress: null,
  currentTreeStage: null,
  currentTreeBasketEmoji: null
};

/**
 * Initialize DOM elements cache
 */
function cacheElements() {
  elements.logoutBtn = document.getElementById('logout-btn');
  elements.groveModeButton = document.getElementById('grove-mode-button');
  elements.gridBtn = document.getElementById('grid-btn');
  elements.basketBtn = document.getElementById('basket-btn');

  elements.groveModeMenu = document.getElementById('grove-mode-menu');
  elements.otherCellsContainer = document.getElementById('other-cells-container');
  elements.gridView = document.getElementById('grid-view');
  elements.basketView = document.getElementById('basket-view');

  elements.groveModeText = document.getElementById('grove-mode-text');
  elements.statsText = document.querySelector('.mb-5.px-2 p');

  elements.currentTreeCard = document.getElementById('current-tree-card');
  elements.currentTreeEmoji = document.getElementById('current-tree-emoji');
  elements.currentTreeProgress = document.getElementById('current-tree-progress');
  elements.currentTreeStage = document.getElementById('current-tree-stage');
  elements.currentTreeBasketEmoji = document.getElementById('current-tree-basket-emoji');
}

// ========================
// Initialization
// ========================
export async function initGrovePage() {
  cacheElements();
  await Promise.all([
    fetchCurrentFruit(),
    fetchCompletedFruits(),
    fetchAllCells()
  ]);
  updateCurrentTree();
  renderCompletedFruits();
  updateStatistics();
  setupEventListeners();
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
  elements.logoutBtn.addEventListener('click', handleLogout);
  elements.groveModeButton.addEventListener('click', handleDropdownToggle);

  // dropdown options
  document.querySelectorAll('.grove-mode-option').forEach(option => {
    option.addEventListener('click', handleModeOptionClick);
  });

  // close dropdown on outside click
  document.addEventListener('click', handleOutsideClick);

  updateModeSelection();
}

/**
 * Handle dropdown toggle
 */
function handleDropdownToggle(e) {
  e.stopPropagation();
  const isHidden = elements.groveModeMenu.classList.toggle('hidden');
  elements.groveModeButton.setAttribute('aria-expanded', isHidden ? 'false' : 'true');
}

/**
 * Handle mode option click
 */
async function handleModeOptionClick(e) {
  const mode = e.currentTarget.getAttribute('data-mode');
  await handleGroveModeChange(mode, null);
  closeDropdown();
}

/**
 * Handle outside click to close dropdown
 */
function handleOutsideClick() {
  if (!elements.groveModeMenu.classList.contains('hidden')) {
    closeDropdown();
  }
}

/**
 * Close dropdown menu
 */
function closeDropdown() {
  elements.groveModeMenu.classList.add('hidden');
  elements.groveModeButton.setAttribute('aria-expanded', 'false');
}

// ========================
// API 호출 함수
// ========================

/**
 * Fetch current fruit
 */
async function fetchCurrentFruit() {
  try {
    const response = await fetch('/fruit/in-progress');
    const data = await response.json();

    if (response.ok && data.fruit?.fruit_id) {
      state.currentFruit = data.fruit;
      return data.fruit;
    }
    state.currentFruit = null;
    return null;
  } catch (error) {
    console.error('Failed to fetch current fruit:', error);
    state.currentFruit = null;
    return null;
  }
}

/**
 * Fetch completed fruits
 */
async function fetchCompletedFruits() {
  try {
    const response = await fetch('/fruits/mine');
    const data = await response.json();

    if (response.ok && data.fruits) {
      state.completedFruits = data.fruits.filter(f => f.status === FRUIT_STATUS.COMPLETED);
      return state.completedFruits;
    }
    state.completedFruits = [];
    return [];
  } catch (error) {
    console.error('Failed to fetch completed fruits:', error);
    state.completedFruits = [];
    return [];
  }
}

/**
 * Get user cell from cookie
 */
function getUserCellSync() {
  try {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      const [name, value] = cookie.trim().split('=');
      if (name === 'user_cell') {
        return decodeURIComponent(value);
      }
    }
    return null;
  } catch (error) {
    console.error('Failed to get user cell:', error);
    return null;
  }
}

/**
 * Fetch all cells
 */
async function fetchAllCells() {
  try {
    const response = await fetch('/cells');
    const data = await response.json();

    if (response.ok && data.cells) {
      state.allCells = data.cells;
      renderCellOptions();
      return state.allCells;
    }
    state.allCells = [];
    return [];
  } catch (error) {
    console.error('Failed to fetch cells:', error);
    state.allCells = [];
    return [];
  }
}

/**
 * Fetch fruits by cell
 */
async function fetchCellFruits(cellName = null) {
  try {
    const targetCell = cellName || getUserCellSync();
    if (!targetCell) {
      console.error('User cell not found');
      state.completedFruits = [];
      return [];
    }

    const response = await fetch('/fruits/cell', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ cell: targetCell })
    });
    const data = await response.json();

    if (response.ok && data.fruits) {
      state.completedFruits = data.fruits.filter(f => f.status === FRUIT_STATUS.COMPLETED);
      return state.completedFruits;
    }
    state.completedFruits = [];
    return [];
  } catch (error) {
    console.error('Failed to fetch cell fruits:', error);
    state.completedFruits = [];
    return [];
  }
}

// ========================
// UI 업데이트 함수
// ========================

/**
 * Render cell options in dropdown
 */
function renderCellOptions() {
  const userCell = getUserCellSync();

  if (!state.allCells?.length) {
    elements.otherCellsContainer.innerHTML =
      '<div class="px-4 py-2.5 text-sm text-gray-500 text-center">셀이 없습니다</div>';
    return;
  }

  const otherCells = state.allCells.filter(cell => cell !== userCell);

  if (!otherCells.length) {
    elements.otherCellsContainer.innerHTML =
      '<div class="px-4 py-2.5 text-sm text-gray-500 text-center">다른 셀이 없습니다</div>';
    return;
  }

  elements.otherCellsContainer.innerHTML = otherCells.map(cell => `
    <button data-cell="${cell}" class="cell-option w-full text-left px-4 py-2.5 hover:bg-orange-50 transition-colors flex items-center justify-between">
      <span class="text-sm font-medium text-gray-900">${cell}의 과수원</span>
      <svg class="cell-check hidden w-4 h-4 text-orange-600" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
      </svg>
    </button>
  `).join('');

  // add click handlers to cell options
  elements.otherCellsContainer.querySelectorAll('.cell-option').forEach(option => {
    option.addEventListener('click', handleCellOptionClick);
  });
}

/**
 * Handle cell option click
 */
async function handleCellOptionClick(e) {
  e.stopPropagation();
  const cell = e.currentTarget.getAttribute('data-cell');
  await handleGroveModeChange('other-cell', cell);
  closeDropdown();
}

/**
 * Update current tree display
 */
function updateCurrentTree() {
  const shouldShow = state.groveMode === 'my' && state.currentFruit;

  elements.currentTreeCard.style.display = shouldShow ? 'block' : 'none';
  elements.currentTreeBasketEmoji.style.display = shouldShow ? 'block' : 'none';

  if (!shouldShow) return;

  const stageInfo = getStageInfo(state.currentFruit.status);
  const progress = calculateProgress(state.currentFruit.status);
  const image = getStatusImage(state.currentFruit);

  // update grid view
  if (isImageUrl(image)) {
    elements.currentTreeEmoji.innerHTML = `<img src="${image}" alt="fruit" class="w-20 h-20 object-contain">`;
  } else {
    elements.currentTreeEmoji.textContent = image;
  }

  elements.currentTreeProgress.textContent = Math.round(progress);
  elements.currentTreeStage.textContent = `${stageInfo.level}단계 · ${stageInfo.name}`;

  // update basket view
  if (isImageUrl(image)) {
    elements.currentTreeBasketEmoji.innerHTML = `<img src="${image}" alt="fruit" class="w-16 h-16 object-contain">`;
  } else {
    elements.currentTreeBasketEmoji.textContent = image;
  }
  elements.currentTreeBasketEmoji.setAttribute('title', `현재 나무 - ${stageInfo.level}단계 ${stageInfo.name}`);
}

/**
 * Render completed fruits
 */
function renderCompletedFruits() {
  const basketViewContainer = elements.basketView.querySelector('.relative.z-10');

  // remove existing completed fruit cards
  elements.gridView.querySelectorAll('.relative.rounded-2xl:not(#current-tree-card)').forEach(card => card.remove());
  basketViewContainer.querySelectorAll('div:not(#current-tree-basket-emoji)').forEach(fruit => fruit.remove());

  // render completed fruits (newest first)
  [...state.completedFruits].reverse().forEach((fruit) => {
    const image = fruit.seventh_status || '🍎';
    const fruitName = fruit.template_name || '과일';
    const displayDate = fruit.updated_at ? formatDate(fruit.updated_at) : '';

    // insert into grid view
    const card = createFruitCard(image, fruitName, displayDate);
    elements.gridView.insertBefore(card, elements.currentTreeCard);

    // insert into basket view
    const basketFruit = createBasketFruit(image, fruitName, displayDate);
    basketViewContainer.insertBefore(basketFruit, elements.currentTreeBasketEmoji);
  });

  updateStatistics();
}

/**
 * 과일 카드 생성 (그리드 뷰용)
 */
function createFruitCard(image, fruitName, displayDate) {
  const card = document.createElement('div');
  card.className = 'relative rounded-2xl bg-white px-6 py-6 shadow-sm outline outline-1 -outline-offset-1 outline-gray-200 hover:outline-orange-300 transition-all hover:shadow-md';

  const imageHtml = isImageUrl(image)
    ? `<img src="${image}" alt="${fruitName}" class="w-20 h-20 object-contain mr-2">`
    : `<span class="text-5xl mr-2">${image}</span>`;

  card.innerHTML = `
    <div class="flex items-start justify-between">
      <div class="flex-1">
        <div class="flex items-center gap-x-3">
          ${imageHtml}
          <div>
            <p class="text-sm font-semibold text-gray-900">${fruitName}</p>
            <p class="text-xs text-green-600">완성</p>
            <p class="text-xs text-gray-600">${displayDate}</p>
          </div>
        </div>
      </div>
    </div>
  `;

  return card;
}

/**
 * 바구니 과일 생성 (바구니 뷰용)
 */
function createBasketFruit(image, fruitName, displayDate) {
  const basketFruit = document.createElement('div');
  basketFruit.className = 'transform hover:scale-110 transition-transform cursor-pointer';
  basketFruit.title = `${fruitName} - ${displayDate}`;

  if (isImageUrl(image)) {
    basketFruit.innerHTML = `<img src="${image}" alt="${fruitName}" class="w-24 h-24 object-contain">`;
  } else {
    basketFruit.className += ' text-6xl';
    basketFruit.textContent = image;
  }

  return basketFruit;
}

/**
 * Update statistics display
 */
function updateStatistics() {
  const inProgressCount = (state.groveMode === 'my' && state.currentFruit) ? 1 : 0;
  const total = state.completedFruits.length + inProgressCount;

  if (elements.statsText) {
    elements.statsText.innerHTML = `
      전체 <span class="font-semibold text-gray-900">${total}</span>
    `;
  }
}

// ========================
// 이벤트 핸들러
// ========================

/**
 * Handle grove mode change
 */
async function handleGroveModeChange(mode, cellName = null) {
  state.groveMode = mode;
  state.selectedCell = cellName;

  // fetch data based on mode
  if (mode === 'my') {
    await fetchCompletedFruits();
  } else if (mode === 'cell' || (mode === 'other-cell' && cellName)) {
    await fetchCellFruits(cellName);
  }

  // update UI
  updateModeSelection();
  updateCurrentTree();
  renderCompletedFruits();
  updateStatistics();
}

/**
 * Update mode selection UI
 */
function updateModeSelection() {
  // update button text
  const modeTexts = {
    'my': '나의 과수원',
    'cell': '우리 셀의 과수원',
    'other-cell': state.selectedCell ? `${state.selectedCell}의 과수원` : '과수원'
  };
  elements.groveModeText.textContent = modeTexts[state.groveMode];

  // update checkmarks for main options
  document.querySelectorAll('.grove-mode-option').forEach(option => {
    const check = option.querySelector('.mode-check');
    const optionMode = option.getAttribute('data-mode');
    const shouldShow = optionMode === state.groveMode && state.groveMode !== 'other-cell';
    check.classList.toggle('hidden', !shouldShow);
  });

  // update checkmarks for cell options
  document.querySelectorAll('.cell-option').forEach(option => {
    const check = option.querySelector('.cell-check');
    const cellName = option.getAttribute('data-cell');
    const shouldShow = state.groveMode === 'other-cell' && cellName === state.selectedCell;
    check.classList.toggle('hidden', !shouldShow);
  });
}

/**
 * 로그아웃 핸들러
 */
async function handleLogout() {
  if (!confirm('로그아웃 하시겠습니까?')) return;

  await AuthAPI.logout();
  AuthAPI.redirectToLogin();
}

// ========================
// 뷰 토글 함수 (전역으로 노출)
// ========================

/**
 * 그리드/바구니 뷰 전환
 * @param {string} view - 'grid' 또는 'basket'
 */
export function toggleView(view) {
  const gridView = document.getElementById('grid-view');
  const basketView = document.getElementById('basket-view');
  const gridBtn = document.getElementById('grid-btn');
  const basketBtn = document.getElementById('basket-btn');

  if (view === 'grid') {
    gridView.classList.remove('hidden');
    basketView.classList.add('hidden');
    gridBtn.classList.add('bg-orange-100', 'text-orange-700');
    gridBtn.classList.remove('text-gray-700', 'hover:bg-gray-100');
    basketBtn.classList.remove('bg-orange-100', 'text-orange-700');
    basketBtn.classList.add('text-gray-700', 'hover:bg-gray-100');
  } else {
    gridView.classList.add('hidden');
    basketView.classList.remove('hidden');
    basketBtn.classList.add('bg-orange-100', 'text-orange-700');
    basketBtn.classList.remove('text-gray-700', 'hover:bg-gray-100');
    gridBtn.classList.remove('bg-orange-100', 'text-orange-700');
    gridBtn.classList.add('text-gray-700', 'hover:bg-gray-100');
  }
}
