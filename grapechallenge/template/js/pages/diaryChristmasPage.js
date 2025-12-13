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
  '성탄절에 대한 질문': 'bg-blue-50 text-blue-700',
  '성탄절을 기다리는 기도': 'bg-green-50 text-green-700'
};

/**
 * 미션 이름에 따른 배지 색상 반환
 * @param {string} missionName - 미션 이름
 * @returns {string} Tailwind 클래스
 */
function getBadgeColor(missionName) {
  return BADGE_COLORS[missionName] || 'bg-red-50 text-red-700';
}

// ========================
// State Management
// ========================

const state = {
  diaries: [],
  count: 0,
  currentUserId: ''
};

// ========================
// DOM Elements Cache
// ========================

const elements = {
  diaryList: null,
  statsText: null,
  skeleton: null,
  emptyState: null,
  helpIconBtn: null
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
  elements.helpIconBtn = document.getElementById('help-icon-btn');
}

/**
 * Initialize diary christmas page
 */
export async function initDiaryChristmasPage() {
  cacheElements();
  await fetchDiaries();
  renderDiaries();
  initHelpIconDropdown();
}

// ========================
// Data Fetching
// ========================

/**
 * Fetch diaries from API (EVENT 미션들)
 */
async function fetchDiaries() {
  const allMissions = [];

  // 각 EVENT 미션 이름으로 조회
  for (const missionName of EVENT_MISSION_NAMES) {
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

// ========================
// Help Icon Dropdown
// ========================

/**
 * Initialize help icon dropdown
 */
function initHelpIconDropdown() {
  if (!elements.helpIconBtn) return;

  let helpDropdown = null;

  elements.helpIconBtn.addEventListener('click', (e) => {
    e.stopPropagation();

    // Remove existing dropdown if any
    if (helpDropdown) {
      helpDropdown.remove();
      helpDropdown = null;
      return;
    }

    // Create dropdown
    helpDropdown = document.createElement('div');
    helpDropdown.className = 'fixed bg-white rounded-lg shadow-lg border border-gray-200 p-3 max-w-xs';
    helpDropdown.style.zIndex = '9999';

    helpDropdown.innerHTML = `
      <p class="text-sm text-gray-700">
        각 일기마다 가장 많은 공감을 받은<br>이모티콘 두 개가 보여집니다.
      </p>
    `;

    // Position dropdown below the button (right-aligned)
    const rect = elements.helpIconBtn.getBoundingClientRect();
    helpDropdown.style.right = `${window.innerWidth - rect.right}px`;
    helpDropdown.style.top = `${rect.bottom + 4}px`;

    document.body.appendChild(helpDropdown);

    // Close dropdown when clicking outside
    setTimeout(() => {
      const closeDropdown = (e) => {
        if (helpDropdown && !helpDropdown.contains(e.target) && e.target !== elements.helpIconBtn) {
          helpDropdown.remove();
          helpDropdown = null;
          document.removeEventListener('click', closeDropdown);
          window.removeEventListener('scroll', closeOnScroll, true);
        }
      };

      const closeOnScroll = () => {
        if (helpDropdown) {
          helpDropdown.remove();
          helpDropdown = null;
          document.removeEventListener('click', closeDropdown);
          window.removeEventListener('scroll', closeOnScroll, true);
        }
      };

      document.addEventListener('click', closeDropdown);
      window.addEventListener('scroll', closeOnScroll, true);
    }, 0);
  });
}
