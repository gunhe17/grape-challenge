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
  card.className = 'diary-card relative rounded-xl bg-white border border-gray-200 px-6 py-5 hover:shadow-md transition-shadow opacity-0';

  const interactions = diary.interaction || [];
  const interactionCounts = countInteractions(interactions);
  const topInteractions = getTopInteractions(interactionCounts, 2);

  card.innerHTML = `
    <div class="space-y-3">
      <p class="text-base text-gray-800 leading-relaxed whitespace-pre-wrap break-words">${diary.content || '내용이 없습니다.'}</p>

      <!-- Interaction Section -->
      <div class="flex items-center justify-between gap-2 pt-2">
        <div class="flex items-center gap-1.5">
          <!-- Top Interactions Display -->
          <div class="flex -space-x-1.5 overflow-hidden">
            ${topInteractions.map(({ emoji }) => `
              <div class="inline-flex items-center justify-center w-6 h-6 rounded-full ring-2 ring-white bg-gradient-to-br from-orange-100 to-orange-50 text-sm">
                ${emoji}
              </div>
            `).join('')}
          </div>
          <!-- Add Interaction Button -->
          <button
            class="add-interaction-btn inline-flex items-center justify-center w-6 h-6 rounded-full ring-2 ring-white bg-gray-100 hover:bg-gray-200 transition-colors text-gray-600"
            data-mission-id="${diary.id}"
            aria-label="인터랙션 추가"
          >
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
          </button>
        </div>
        <span class="text-sm text-gray-500">${diary.user_name || '익명'}의 감사일기</span>
      </div>
    </div>
  `;

  // Add event listeners
  const addBtn = card.querySelector('.add-interaction-btn');
  let dropdown = null;

  // Toggle dropdown on button click
  addBtn.addEventListener('click', (e) => {
    e.stopPropagation();

    // Remove existing dropdown if any
    if (dropdown) {
      dropdown.remove();
      dropdown = null;
      return;
    }

    // Create dropdown
    dropdown = document.createElement('div');
    dropdown.className = 'fixed bg-white rounded-lg shadow-lg border border-gray-200 p-2';
    dropdown.style.zIndex = '9999';

    dropdown.innerHTML = `
      <div class="flex items-center gap-1">
        ${createInteractionButton('😆', diary.id)}
        ${createInteractionButton('😮', diary.id)}
        ${createInteractionButton('💪', diary.id)}
        ${createInteractionButton('🙏', diary.id)}
        ${createInteractionButton('👏', diary.id)}
      </div>
    `;

    // Position dropdown below the button
    const rect = addBtn.getBoundingClientRect();
    dropdown.style.left = `${rect.left}px`;
    dropdown.style.top = `${rect.bottom + 4}px`;

    document.body.appendChild(dropdown);

    // Handle interaction button clicks
    const interactionBtns = dropdown.querySelectorAll('.interaction-btn');
    interactionBtns.forEach(button => {
      button.addEventListener('click', async (e) => {
        await handleInteractionClick(e);
        if (dropdown) {
          dropdown.remove();
          dropdown = null;
        }
      });
    });

    // Close dropdown when clicking outside
    setTimeout(() => {
      const closeDropdown = (e) => {
        if (dropdown && !dropdown.contains(e.target) && e.target !== addBtn) {
          dropdown.remove();
          dropdown = null;
          document.removeEventListener('click', closeDropdown);
          window.removeEventListener('scroll', closeOnScroll, true);
        }
      };

      const closeOnScroll = () => {
        if (dropdown) {
          dropdown.remove();
          dropdown = null;
          document.removeEventListener('click', closeDropdown);
          window.removeEventListener('scroll', closeOnScroll, true);
        }
      };

      document.addEventListener('click', closeDropdown);
      window.addEventListener('scroll', closeOnScroll, true);
    }, 0);
  });

  // Add staggered animation
  setTimeout(() => {
    card.style.animation = `fadeInUp 0.5s ease-out ${index * 0.05}s forwards`;
  }, 10);

  return card;
}

/**
 * Create interaction button HTML
 * @param {string} emoji - 이모지
 * @param {string} missionId - 미션 ID
 * @returns {string} 버튼 HTML
 */
function createInteractionButton(emoji, missionId) {
  return `
    <button
      class="interaction-btn inline-flex items-center justify-center w-8 h-8 rounded-lg hover:bg-gray-50 transition-colors"
      data-emoji="${emoji}"
      data-mission-id="${missionId}"
    >
      <span class="text-lg">${emoji}</span>
    </button>
  `;
}

/**
 * Count interactions by emoji
 * @param {Array<string>} interactions - 인터랙션 배열
 * @returns {Object} 이모지별 카운트
 */
function countInteractions(interactions) {
  const counts = {
    '😆': 0,
    '😮': 0,
    '💪': 0,
    '🙏': 0,
    '👏': 0
  };

  interactions.forEach(emoji => {
    if (counts.hasOwnProperty(emoji)) {
      counts[emoji]++;
    }
  });

  return counts;
}

/**
 * Get top N interactions by count
 * @param {Object} counts - 이모지별 카운트 객체
 * @param {number} n - 상위 N개
 * @returns {Array<{emoji: string, count: number}>} 상위 N개 인터랙션
 */
function getTopInteractions(counts, n) {
  return Object.entries(counts)
    .map(([emoji, count]) => ({ emoji, count }))
    .filter(item => item.count > 0)
    .sort((a, b) => b.count - a.count)
    .slice(0, n);
}

/**
 * Handle interaction button click
 * @param {Event} event - 클릭 이벤트
 */
async function handleInteractionClick(event) {
  const button = event.currentTarget;
  const emoji = button.dataset.emoji;
  const missionId = button.dataset.missionId;

  // Disable button temporarily
  button.disabled = true;

  // Add interaction via API
  const result = await MissionAPI.addInteraction(missionId, emoji);

  if (result.success) {
    // Re-fetch and re-render diaries to show updated counts
    await fetchDiaries();
    renderDiaries();
  } else {
    console.error('인터랙션 추가 실패:', result.message);
    button.disabled = false;
  }
}

/**
 * Update statistics display
 */
function updateStats() {
  if (elements.statsText) {
    elements.statsText.innerHTML = `전체 <span class="font-semibold text-gray-900">${state.count}</span>개`;
  }
}
