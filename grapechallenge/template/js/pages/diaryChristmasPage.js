/**
 * Diary Christmas Page Logic
 * 성탄 챌린지 일기장 페이지 - EVENT 미션 내용 조회
 */

import { MissionAPI } from '../api/missionApi.js';

// ========================
// 미션 이름 상수
// ========================
const EVENT_MISSION_NAMES = [
  '성탄절에 대한 질문',
  '성탄절을 기다리는 기도'
];

// 미션 이름별 배지 색상
const BADGE_COLORS = {
  '성탄절에 대한 질문': 'bg-red-50 text-red-700',
  '성탄절을 기다리는 기도': 'bg-green-50 text-green-700'
};

/**
 * 미션 이름에 따른 배지 색상 반환
 * @param {string} missionName - 미션 이름
 * @returns {string} Tailwind 클래스
 */
function getBadgeColor(missionName) {
  return BADGE_COLORS[missionName] || 'bg-white/80 text-gray-700';
}

// ========================
// Filter Constants
// ========================
const FILTER_MODES = {
  ALL: 'all'
};

const FILTER_TEXTS = {
  [FILTER_MODES.ALL]: '성탄 일기장'
};

// ========================
// State Management
// ========================

const state = {
  diaries: [],
  count: 0,
  currentUserId: '',
  filterMode: FILTER_MODES.ALL
};

// ========================
// DOM Elements Cache
// ========================

const elements = {
  diaryList: null,
  statsText: null,
  skeleton: null,
  emptyState: null,
  // Filter dropdown elements
  filterButton: null,
  filterMenu: null,
  filterText: null
};

// ========================
// Initialization
// ========================

/**
 * Initialize DOM elements cache
 */
function cacheElements() {
  elements.diaryList = document.getElementById('diary-list');
  elements.statsText = document.getElementById('diary-stats-text');
  elements.skeleton = document.querySelector('.diary-skeleton');
  elements.emptyState = document.getElementById('diary-empty');
  // Filter dropdown elements
  elements.filterButton = document.getElementById('diary-filter-button');
  elements.filterMenu = document.getElementById('diary-filter-menu');
  elements.filterText = document.getElementById('diary-filter-text');
}

/**
 * Initialize diary christmas page
 */
export async function initDiaryChristmasPage() {
  cacheElements();
  setupFilterDropdown();
  await fetchDiaries();
  renderDiaries();
}

// ========================
// Data Fetching
// ========================

/**
 * Fetch diaries from API (EVENT 미션들)
 * @param {string} filterMode - 필터 모드 ('all' 또는 미션 이름)
 */
async function fetchDiaries(filterMode = null) {
  const currentFilter = filterMode || state.filterMode;
  const allMissions = [];

  // 필터 모드에 따라 조회할 미션 결정
  const missionsToFetch = currentFilter === FILTER_MODES.ALL
    ? EVENT_MISSION_NAMES
    : [currentFilter];

  // 각 미션 이름으로 조회
  for (const missionName of missionsToFetch) {
    const result = await MissionAPI.fetchMissionsByName(missionName, 'today');
    if (result.missions && result.missions.length > 0) {
      allMissions.push(...result.missions);
    }
    if (!state.currentUserId && result.user_id) {
      state.currentUserId = result.user_id;
    }
  }

  // 시간순 정렬 (최신순)
  allMissions.sort((a, b) => {
    const dateA = new Date(a.content_created_at || 0);
    const dateB = new Date(b.content_created_at || 0);
    return dateB - dateA;
  });

  state.diaries = allMissions;
  state.count = allMissions.length;
}

// ========================
// Rendering Functions
// ========================

/**
 * Render diaries list
 */
function renderDiaries() {
  // Hide skeleton
  if (elements.skeleton) {
    elements.skeleton.remove();
  }

  // Update stats
  updateStats();

  // Show empty state if no diaries
  if (state.count === 0) {
    if (elements.emptyState) {
      elements.emptyState.classList.remove('hidden');
    }
    return;
  }

  // Hide empty state
  if (elements.emptyState) {
    elements.emptyState.classList.add('hidden');
  }

  // Render diary cards
  const diaryCards = state.diaries.map((diary, index) => createDiaryCard(diary, index));

  // Clear existing content (except skeleton which is already removed)
  const existingCards = elements.diaryList.querySelectorAll('.diary-card');
  existingCards.forEach(card => card.remove());

  // Append new cards
  diaryCards.forEach(card => {
    elements.diaryList.appendChild(card);
  });
}

/**
 * Create a diary card element
 * @param {Object} diary - 일기 데이터
 * @param {number} index - 인덱스
 * @returns {HTMLElement} 일기 카드 엘리먼트
 */
function createDiaryCard(diary, index) {
  const card = document.createElement('div');
  card.className = 'diary-card relative rounded-xl bg-white/20 backdrop-blur-sm px-6 py-5 outline outline-1 -outline-offset-1 outline-white/30 opacity-0';

  const badgeColor = getBadgeColor(diary.name);

  card.innerHTML = `
    <div class="space-y-3">
      <!-- Mission Name Badge -->
      <div class="flex items-center gap-2">
        <span class="inline-flex items-center rounded-full ${badgeColor} px-2 py-1 text-xs font-medium">
          ${diary.name || '미션'}
        </span>
      </div>

      <p class="text-base text-white text-outline-thin leading-relaxed whitespace-pre-wrap break-words">${diary.content || '내용이 없습니다.'}</p>

      <!-- Author -->
      <div class="flex items-center justify-end pt-2">
        <span class="text-sm text-gray-300">${diary.user_name || '익명'}</span>
      </div>
    </div>
  `;

  // Add staggered animation
  setTimeout(() => {
    card.style.animation = `fadeInUp 0.5s ease-out ${index * 0.05}s forwards`;
  }, 10);

  return card;
}

/**
 * Update statistics display
 */
function updateStats() {
  if (elements.statsText) {
    elements.statsText.innerHTML = `전체 <span class="font-semibold">${state.count}</span>개`;
  }
}

/**
 * Show loading state
 */
function showLoadingState() {
  // Reset stats
  if (elements.statsText) {
    elements.statsText.innerHTML = `전체 <span class="font-semibold">0</span>개`;
  }

  // Remove existing cards
  const existingCards = elements.diaryList.querySelectorAll('.diary-card');
  existingCards.forEach(card => card.remove());

  // Hide empty state
  if (elements.emptyState) {
    elements.emptyState.classList.add('hidden');
  }

  // Add skeleton
  const skeleton = document.createElement('div');
  skeleton.className = 'diary-skeleton';
  skeleton.innerHTML = `
    <div class="rounded-xl bg-white/20 backdrop-blur-sm px-6 py-5 animate-pulse">
      <div class="space-y-3">
        <div class="h-4 bg-white/30 rounded w-full"></div>
        <div class="h-4 bg-white/20 rounded w-4/5"></div>
        <div class="flex items-center justify-end">
          <div class="h-3 bg-white/20 rounded w-24"></div>
        </div>
      </div>
    </div>
  `;
  elements.diaryList.appendChild(skeleton);
  elements.skeleton = skeleton;
}

// ========================
// Filter Dropdown
// ========================

/**
 * Setup filter dropdown event listeners
 */
function setupFilterDropdown() {
  if (!elements.filterButton || !elements.filterMenu) return;

  // Toggle dropdown on button click
  elements.filterButton.addEventListener('click', handleFilterDropdownToggle);

  // Handle filter option clicks
  document.querySelectorAll('.diary-filter-option').forEach(option => {
    option.addEventListener('click', handleFilterOptionClick);
  });

  // Close dropdown on outside click
  document.addEventListener('click', handleOutsideClick);

  // Initialize selection UI
  updateFilterSelection();
}

/**
 * Handle dropdown toggle
 */
function handleFilterDropdownToggle(e) {
  e.stopPropagation();
  const isHidden = elements.filterMenu.classList.toggle('hidden');
  elements.filterButton.setAttribute('aria-expanded', isHidden ? 'false' : 'true');
}

/**
 * Handle filter option click
 */
async function handleFilterOptionClick(e) {
  const filter = e.currentTarget.getAttribute('data-filter');
  await handleFilterChange(filter);
}

/**
 * Handle outside click to close dropdown
 */
function handleOutsideClick(e) {
  if (elements.filterMenu &&
      !elements.filterMenu.classList.contains('hidden') &&
      !elements.filterButton.contains(e.target) &&
      !elements.filterMenu.contains(e.target)) {
    closeFilterDropdown();
  }
}

/**
 * Close filter dropdown
 */
function closeFilterDropdown() {
  elements.filterMenu.classList.add('hidden');
  elements.filterButton.setAttribute('aria-expanded', 'false');
}

/**
 * Handle filter change
 */
async function handleFilterChange(filter) {
  // Update state
  state.filterMode = filter;

  // Update UI
  updateFilterSelection();

  // Close dropdown
  closeFilterDropdown();

  // Show loading state
  showLoadingState();

  // Fetch data with new filter
  await fetchDiaries(filter);

  // Re-render
  renderDiaries();
}

/**
 * Update filter selection UI (checkmarks and button text)
 */
function updateFilterSelection() {
  // Update button text
  const displayText = state.filterMode === FILTER_MODES.ALL
    ? FILTER_TEXTS[FILTER_MODES.ALL]
    : state.filterMode;

  if (elements.filterText) {
    elements.filterText.textContent = displayText;
  }

  // Update checkmarks
  document.querySelectorAll('.diary-filter-option').forEach(option => {
    const check = option.querySelector('.filter-check');
    const optionFilter = option.getAttribute('data-filter');
    const shouldShow = optionFilter === state.filterMode;
    check.classList.toggle('hidden', !shouldShow);
  });
}
