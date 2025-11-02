/**
 * Grove Page Logic
 * 과수원 페이지의 비즈니스 로직과 이벤트 핸들러
 */

import { getStageInfo, getStatusImage, isImageUrl, formatDate } from '../utils/helpers.js';
import { FRUIT_STATUS } from '../utils/constants.js';
import { AuthAPI } from '../api/authApi.js';

// ========================
// Constants
// ========================
const GROVE_MODES = {
  MY: 'my',
  CELL: 'cell',
  OTHER_CELL: 'other-cell'
};

const MODE_TEXTS = {
  [GROVE_MODES.MY]: '나의 과수원',
  [GROVE_MODES.CELL]: '우리 셀의 과수원',
  [GROVE_MODES.OTHER_CELL]: '과수원'
};

const IMAGE_SIZES = {
  GRID: 'w-10 h-10',
  BASKET: 'w-12 h-12'
};

// ========================
// State Management
// ========================
const state = {
  currentFruit: null,
  completedFruits: [],
  groveMode: GROVE_MODES.MY,
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
  currentTreeName: null,
  currentTreeDate: null,
  currentTreeBasketEmoji: null
};

// ========================
// Initialization
// ========================

/**
 * Initialize DOM elements cache
 */
function cacheElements() {
  elements.groveModeButton = document.getElementById('grove-mode-button');
  elements.gridBtn = document.getElementById('grid-btn');
  elements.basketBtn = document.getElementById('basket-btn');

  elements.groveModeMenu = document.getElementById('grove-mode-menu');
  elements.otherCellsContainer = document.getElementById('other-cells-container');
  elements.gridView = document.getElementById('grid-view');
  elements.basketView = document.getElementById('basket-view');

  elements.groveModeText = document.getElementById('grove-mode-text');
  elements.statsText = document.getElementById('stats-text');

  elements.currentTreeCard = document.getElementById('current-tree-card');
  elements.currentTreeEmoji = document.getElementById('current-tree-emoji');
  elements.currentTreeName = document.getElementById('current-tree-name');
  elements.currentTreeDate = document.getElementById('current-tree-date');
  elements.currentTreeBasketEmoji = document.getElementById('current-tree-basket-emoji');
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
  // Logout button is now handled by Sidebar component
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
 * Initialize grove page
 */
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

// ========================
// API Functions
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
// Rendering Functions
// ========================

/**
 * Render image or emoji element
 * @param {string} image - Image URL or emoji
 * @param {string} size - Size class (e.g., 'w-10 h-10')
 * @param {string} fruitName - Fruit name for alt text
 * @returns {string} HTML string
 */
function renderImageElement(image, size, fruitName = 'fruit') {
  if (isImageUrl(image)) {
    return `<img src="${image}" alt="${fruitName}" class="${size} object-contain">`;
  }
  return `<div class="${size} flex items-center justify-center text-2xl">${image}</div>`;
}

/**
 * Update image element (for dynamic updates)
 * @param {HTMLElement} element - DOM element to update
 * @param {string} image - Image URL or emoji
 * @param {string} size - Size class
 * @param {string} additionalClasses - Additional CSS classes
 */
function updateImageElement(element, image, size, additionalClasses = '') {
  if (isImageUrl(image)) {
    element.innerHTML = `<img src="${image}" alt="fruit" class="${size} object-contain">`;
    element.className = additionalClasses;
  } else {
    element.textContent = image;
    element.className = `${size} flex items-center justify-center text-2xl ${additionalClasses}`.trim();
  }
}

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

  // Filter out user's cell and admin cell
  const otherCells = state.allCells.filter(cell => cell !== userCell && cell !== '관리자');

  if (!otherCells.length) {
    elements.otherCellsContainer.innerHTML =
      '<div class="px-4 py-2.5 text-sm text-gray-500 text-center">다른 셀이 없습니다</div>';
    return;
  }

  const checkmarkSvg = `
    <svg class="cell-check hidden w-4 h-4 text-orange-600" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
    </svg>
  `;

  elements.otherCellsContainer.innerHTML = otherCells.map(cell => `
    <button data-cell="${cell}" class="cell-option w-full text-left px-4 py-2.5 hover:bg-orange-50 transition-colors flex items-center justify-between">
      <span class="text-sm font-medium text-gray-900">${cell}의 과수원</span>
      ${checkmarkSvg}
    </button>
  `).join('');

  // add click handlers to cell options
  elements.otherCellsContainer.querySelectorAll('.cell-option').forEach(option => {
    option.addEventListener('click', handleCellOptionClick);
  });
}

/**
 * Update current tree display
 */
function updateCurrentTree() {
  const shouldShow = state.groveMode === GROVE_MODES.MY && state.currentFruit;

  if (!shouldShow) {
    if (elements.currentTreeCard) {
      elements.currentTreeCard.style.display = 'none';
    }
    if (elements.currentTreeBasketEmoji) {
      elements.currentTreeBasketEmoji.style.display = 'none';
    }
    return;
  }

  const stageInfo = getStageInfo(state.currentFruit.status);
  const image = getStatusImage(state.currentFruit);
  const fruitName = state.currentFruit.name || '과일';
  const displayDate = state.currentFruit.created_at ? formatDate(state.currentFruit.created_at) : '';

  // update grid view
  elements.currentTreeName.textContent = fruitName;
  elements.currentTreeDate.textContent = displayDate;
  updateImageElement(elements.currentTreeEmoji, image, IMAGE_SIZES.GRID);

  // show with animation
  elements.currentTreeCard.classList.remove('hidden');
  elements.currentTreeCard.classList.add('grid-item-animate');
  elements.currentTreeCard.style.display = 'block';

  // update basket view
  updateImageElement(
    elements.currentTreeBasketEmoji,
    image,
    IMAGE_SIZES.BASKET,
    'transform hover:scale-110 transition-transform cursor-pointer'
  );
  elements.currentTreeBasketEmoji.setAttribute('title', `${fruitName} - ${stageInfo.level}단계 ${stageInfo.name}`);
  elements.currentTreeBasketEmoji.style.display = 'block';
}

/**
 * Render completed fruits
 */
function renderCompletedFruits() {
  const basketViewContainer = elements.basketView.querySelector('.relative.z-10');

  // remove skeleton
  const skeleton = elements.gridView.querySelector('.grid-skeleton');
  if (skeleton) {
    skeleton.remove();
  }

  // remove existing completed fruit cards (but keep current tree card)
  const allCards = elements.gridView.querySelectorAll('.relative.rounded-xl');
  allCards.forEach(card => {
    if (card.id !== 'current-tree-card') {
      card.remove();
    }
  });

  // remove basket fruits
  if (basketViewContainer) {
    basketViewContainer.querySelectorAll('div:not(#current-tree-basket-emoji)').forEach(fruit => fruit.remove());
  }

  // render completed fruits (newest first) with staggered animation
  [...state.completedFruits].reverse().forEach((fruit, index) => {
    const image = fruit.seventh_status || '🍎';
    const baseFruitName = fruit.name || '과일';

    // Add user name if not in "my" mode
    const fruitName = state.groveMode !== GROVE_MODES.MY && fruit.user_name
      ? `${fruit.user_name}의 ${baseFruitName}`
      : baseFruitName;

    const displayDate = fruit.updated_at ? formatDate(fruit.updated_at) : '';

    // insert into grid view with animation
    const card = createFruitCard(image, fruitName, displayDate);
    card.classList.add('grid-item-animate');
    card.style.animationDelay = `${index * 0.05}s`;
    elements.gridView.insertBefore(card, elements.currentTreeCard);

    // insert into basket view
    if (basketViewContainer) {
      const basketFruit = createBasketFruit(image, fruitName, displayDate);
      basketViewContainer.insertBefore(basketFruit, elements.currentTreeBasketEmoji);
    }
  });

  updateStatistics();
}

/**
 * Create fruit card for grid view
 * @param {string} image - Image URL or emoji
 * @param {string} fruitName - Fruit name
 * @param {string} displayDate - Display date
 * @returns {HTMLElement} Fruit card element
 */
function createFruitCard(image, fruitName, displayDate) {
  const card = document.createElement('div');
  card.className = 'relative rounded-xl bg-white px-4 py-4 shadow-sm outline outline-1 -outline-offset-1 outline-gray-200 hover:outline-orange-300 transition-all hover:shadow-md';

  const imageHtml = renderImageElement(image, IMAGE_SIZES.GRID, fruitName);

  card.innerHTML = `
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-x-2">
        ${imageHtml}
        <div>
          <p class="text-xs font-semibold text-gray-900">${fruitName}</p>
          <p class="text-xs text-gray-600">${displayDate}</p>
        </div>
      </div>
      <div>
        <p class="text-xs text-green-600 text-right">완성</p>
      </div>
    </div>
  `;

  return card;
}

/**
 * Create fruit element for basket view
 * @param {string} image - Image URL or emoji
 * @param {string} fruitName - Fruit name
 * @param {string} displayDate - Display date
 * @returns {HTMLElement} Basket fruit element
 */
function createBasketFruit(image, fruitName, displayDate) {
  const basketFruit = document.createElement('div');
  basketFruit.className = 'transform hover:scale-110 transition-transform cursor-pointer';
  basketFruit.title = `${fruitName} - ${displayDate}`;

  if (isImageUrl(image)) {
    basketFruit.innerHTML = `<img src="${image}" alt="${fruitName}" class="${IMAGE_SIZES.BASKET} object-contain">`;
  } else {
    basketFruit.className += ` ${IMAGE_SIZES.BASKET} flex items-center justify-center text-3xl`;
    basketFruit.textContent = image;
  }

  return basketFruit;
}

/**
 * Update statistics display
 */
function updateStatistics() {
  const inProgressCount = (state.groveMode === GROVE_MODES.MY && state.currentFruit) ? 1 : 0;
  const total = state.completedFruits.length + inProgressCount;

  if (elements.statsText) {
    elements.statsText.innerHTML = `
      전체 <span class="font-semibold text-gray-900">${total}</span>
    `;
  }
}

/**
 * Update mode selection UI
 */
function updateModeSelection() {
  // update button text
  const displayText = state.groveMode === GROVE_MODES.OTHER_CELL && state.selectedCell
    ? `${state.selectedCell}의 과수원`
    : MODE_TEXTS[state.groveMode];

  elements.groveModeText.textContent = displayText;

  // update checkmarks for main options
  document.querySelectorAll('.grove-mode-option').forEach(option => {
    const check = option.querySelector('.mode-check');
    const optionMode = option.getAttribute('data-mode');
    const shouldShow = optionMode === state.groveMode && state.groveMode !== GROVE_MODES.OTHER_CELL;
    check.classList.toggle('hidden', !shouldShow);
  });

  // update checkmarks for cell options
  document.querySelectorAll('.cell-option').forEach(option => {
    const check = option.querySelector('.cell-check');
    const cellName = option.getAttribute('data-cell');
    const shouldShow = state.groveMode === GROVE_MODES.OTHER_CELL && cellName === state.selectedCell;
    check.classList.toggle('hidden', !shouldShow);
  });
}

// ========================
// Event Handlers
// ========================

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
}

/**
 * Handle cell option click
 */
async function handleCellOptionClick(e) {
  e.stopPropagation();
  const cell = e.currentTarget.getAttribute('data-cell');
  await handleGroveModeChange(GROVE_MODES.OTHER_CELL, cell);
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

/**
 * Handle grove mode change
 */
async function handleGroveModeChange(mode, cellName = null) {
  // 1. Update state
  state.groveMode = mode;
  state.selectedCell = cellName;

  // 2. Update dropdown UI (button text and checkmarks)
  updateModeSelection();

  // 3. Close dropdown menu
  closeDropdown();

  // 4. Show loading state
  showLoadingState();

  // 5. Fetch data based on mode
  if (mode === GROVE_MODES.MY) {
    await Promise.all([
      fetchCurrentFruit(),
      fetchCompletedFruits()
    ]);
  } else if (mode === GROVE_MODES.CELL) {
    const userCell = getUserCellSync();
    await fetchCellFruits(userCell);
  } else if (mode === GROVE_MODES.OTHER_CELL && cellName) {
    await fetchCellFruits(cellName);
  }

  // 6. Update content UI with loaded data
  updateCurrentTree();
  renderCompletedFruits();
  updateStatistics();
}

/**
 * Show loading state
 */
function showLoadingState() {
  // DON'T clear state data here - it will be updated by fetch functions

  // Reset stats to 0
  if (elements.statsText) {
    elements.statsText.innerHTML = '전체 <span class="font-semibold text-gray-900">0</span>';
  }

  // Hide current tree card
  if (elements.currentTreeCard) {
    elements.currentTreeCard.style.display = 'none';
  }
  if (elements.currentTreeBasketEmoji) {
    elements.currentTreeBasketEmoji.style.display = 'none';
  }

  // Remove existing skeleton first
  const existingSkeleton = elements.gridView.querySelector('.grid-skeleton');
  if (existingSkeleton) {
    existingSkeleton.remove();
  }

  // Remove all existing fruit cards (except current tree card)
  const allCards = elements.gridView.querySelectorAll('.relative.rounded-xl');
  allCards.forEach(card => {
    if (card.id !== 'current-tree-card') {
      card.remove();
    }
  });

  // Remove basket fruits
  const basketViewContainer = elements.basketView.querySelector('.relative.z-10');
  if (basketViewContainer) {
    basketViewContainer.querySelectorAll('div:not(#current-tree-basket-emoji)').forEach(fruit => fruit.remove());
  }

  // Add skeleton
  const skeleton = document.createElement('div');
  skeleton.className = 'grid-skeleton rounded-xl bg-gray-100 px-4 py-4 animate-pulse';
  skeleton.innerHTML = `
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-x-2">
        <div class="w-10 h-10 bg-gray-200 rounded"></div>
        <div class="space-y-2">
          <div class="h-3 w-16 bg-gray-200 rounded"></div>
          <div class="h-3 w-20 bg-gray-200 rounded"></div>
        </div>
      </div>
      <div class="h-3 w-10 bg-gray-200 rounded"></div>
    </div>
  `;
  elements.gridView.insertBefore(skeleton, elements.currentTreeCard);
}

// ========================
// View Toggle Functions
// ========================

/**
 * Toggle between grid and basket views
 * @param {string} view - 'grid' or 'basket'
 */
export function toggleView(view) {
  const isGridView = view === 'grid';

  // toggle view visibility
  elements.gridView.classList.toggle('hidden', !isGridView);
  elements.basketView.classList.toggle('hidden', isGridView);

  // update button states
  const activeClasses = ['bg-orange-100', 'text-orange-700'];
  const inactiveClasses = ['text-gray-700', 'hover:bg-gray-100'];

  if (isGridView) {
    elements.gridBtn.classList.add(...activeClasses);
    elements.gridBtn.classList.remove(...inactiveClasses);
    elements.basketBtn.classList.remove(...activeClasses);
    elements.basketBtn.classList.add(...inactiveClasses);
  } else {
    elements.basketBtn.classList.add(...activeClasses);
    elements.basketBtn.classList.remove(...inactiveClasses);
    elements.gridBtn.classList.remove(...activeClasses);
    elements.gridBtn.classList.add(...inactiveClasses);
  }
}
