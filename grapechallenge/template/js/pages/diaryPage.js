/**
 * Diary Page Logic
 * 감사일기장 페이지의 비즈니스 로직과 이벤트 핸들러
 */

import { MissionAPI } from '../api/missionApi.js';

// ========================
// State Management
// ========================

const state = {
  diaries: [],
  count: 0
};

// ========================
// DOM Elements Cache
// ========================

const elements = {
  diaryList: null,
  statsText: null,
  skeleton: null,
  emptyState: null
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
}

/**
 * Initialize diary page
 */
export async function initDiaryPage() {
  cacheElements();
  await fetchDiaries();
  renderDiaries();
}

// ========================
// Data Fetching
// ========================

/**
 * Fetch diaries from API
 */
async function fetchDiaries() {
  const result = await MissionAPI.fetchMissionsByName('감사 일기 작성하기', 'today');
  state.diaries = result.missions;
  state.count = result.count;
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
  card.className = 'diary-card rounded-xl bg-white border border-gray-200 px-6 py-5 hover:shadow-md transition-shadow opacity-0';

  card.innerHTML = `
    <div class="space-y-3">
      <p class="text-base text-gray-800 leading-relaxed whitespace-pre-wrap break-words">${diary.content || '내용이 없습니다.'}</p>
      <div class="flex items-center justify-end">
        <span class="text-sm text-gray-500">${diary.user_name || '익명'}의 감사일기</span>
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
    elements.statsText.innerHTML = `전체 <span class="font-semibold text-gray-900">${state.count}</span>개`;
  }
}
