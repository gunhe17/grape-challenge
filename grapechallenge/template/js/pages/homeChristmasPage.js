/**
 * Home Christmas Page Logic
 * 크리스마스 홈 페이지 - EVENT 미션 전용
 */

import { FruitAPI } from '../api/fruitApi.js';
import { MissionCard } from '../../components/missionCard.js';
import { UI_CONSTANTS } from '../utils/constants.js';

// ========================
// 전역 상태
// ========================
let currentMissions = [];
let scrollPosition = 0;

// ========================
// 초기화
// ========================
export async function initHomeChristmasPage() {
  await fetchEventMissions();
  updateUI();
}

// ========================
// 데이터 조회
// ========================
async function fetchEventMissions() {
  currentMissions = await FruitAPI.fetchEventMissions();
}

// ========================
// UI 업데이트
// ========================
function updateUI() {
  const container = document.getElementById('mission-container');

  // Remove skeleton if it exists
  const skeleton = container.querySelector('.mission-skeleton');
  if (skeleton) {
    skeleton.remove();
  }

  // Clear container
  container.innerHTML = '';

  let cardIndex = 0;

  // check if all missions are completed
  const allCompleted = currentMissions.length > 0 && currentMissions.every(m => !m.can_complete);

  if (allCompleted) {
    const completionCard = MissionCard.createAllMissionsCompletedCard({ transparent: true });
    completionCard.style.animationDelay = `${cardIndex * UI_CONSTANTS.ANIMATION_DELAY_STEP}s`;
    container.appendChild(completionCard);
    cardIndex++;
  }

  if (currentMissions.length > 0) {
    currentMissions.forEach(mission => {
      const card = MissionCard.createDailyMissionCard(mission, handleCompleteMission, { transparent: true, theme: 'christmas' });
      card.style.animationDelay = `${cardIndex * UI_CONSTANTS.ANIMATION_DELAY_STEP}s`;
      container.appendChild(card);
      cardIndex++;
    });
  } else {
    // 미션이 없는 경우
    const emptyCard = document.createElement('div');
    emptyCard.className = 'rounded-xl bg-white/20 backdrop-blur-sm px-7 py-5 shadow-sm ring-1 ring-white/30 animate-fade-in';
    emptyCard.innerHTML = `
      <p class="text-sm text-gray-300 text-center">오늘의 미션이 없습니다.</p>
    `;
    container.appendChild(emptyCard);
  }
}

// ========================
// 이벤트 핸들러
// ========================
async function handleCompleteMission(event) {
  const btn = event.target;
  const missionName = btn.getAttribute('data-mission-name');

  // 미션 데이터 찾기
  const mission = currentMissions.find(m => m.name === missionName);

  if (!mission) {
    alert('미션을 찾을 수 없습니다.');
    return;
  }

  // EVENT 미션은 모달을 통해 내용 입력
  showMissionModal(btn, mission);
}

// ========================
// 모달 유틸리티
// ========================
function lockBodyScroll() {
  scrollPosition = window.pageYOffset;
  document.body.style.overflow = 'hidden';
  document.body.style.position = 'fixed';
  document.body.style.top = `-${scrollPosition}px`;
  document.body.style.width = '100%';
}

function unlockBodyScroll() {
  document.body.style.removeProperty('overflow');
  document.body.style.removeProperty('position');
  document.body.style.removeProperty('top');
  document.body.style.removeProperty('width');
  window.scrollTo(0, scrollPosition);
}

// ========================
// 동적 미션 모달
// ========================
function showMissionModal(btn, mission) {
  const modal = document.getElementById('mission-modal');
  const titleEl = document.getElementById('mission-modal-title');
  const descriptionEl = document.getElementById('mission-modal-description');
  const contentTextarea = document.getElementById('mission-content');
  const charCountEl = document.getElementById('mission-char-count');
  const submitBtn = document.getElementById('mission-submit-btn');
  const cancelBtn = document.getElementById('mission-cancel-btn');

  // 미션 정보로 모달 제목/설명 설정
  titleEl.textContent = mission.name || '';
  descriptionEl.textContent = mission.content || '';

  // reset textarea and disable submit button
  contentTextarea.value = '';
  charCountEl.textContent = '0';
  submitBtn.disabled = true;
  submitBtn.classList.add('opacity-50', 'cursor-not-allowed');

  // lock body scroll
  lockBodyScroll();

  // show modal
  modal.classList.remove('hidden');

  // focus textarea
  setTimeout(() => contentTextarea.focus(), 100);

  // handle input change
  const handleInput = () => {
    const content = contentTextarea.value.trim();
    const charCount = contentTextarea.value.length;

    charCountEl.textContent = charCount;

    if (content.length >= 5 && content.length <= 1000) {
      submitBtn.disabled = false;
      submitBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    } else {
      submitBtn.disabled = true;
      submitBtn.classList.add('opacity-50', 'cursor-not-allowed');
    }
  };

  // handle cancel
  const handleCancel = () => {
    modal.classList.add('hidden');
    unlockBodyScroll();
    cleanup();
  };

  // handle submit
  const handleSubmit = async () => {
    const content = contentTextarea.value.trim();

    if (content.length < 5) {
      alert('5자 이상 작성해주세요.');
      return;
    }

    modal.classList.add('hidden');
    unlockBodyScroll();

    btn.disabled = true;

    const result = await FruitAPI.completeEventMission(mission.name, content);

    if (result) {
      await fetchEventMissions();
      updateUI();
    } else {
      alert('미션 완료 중 오류가 발생했습니다.');
      btn.textContent = '완료';
      btn.disabled = false;
    }

    cleanup();
  };

  // cleanup listeners
  const cleanup = () => {
    contentTextarea.removeEventListener('input', handleInput);
    submitBtn.removeEventListener('click', handleSubmit);
    cancelBtn.removeEventListener('click', handleCancel);
  };

  // add listeners
  contentTextarea.addEventListener('input', handleInput);
  submitBtn.addEventListener('click', handleSubmit);
  cancelBtn.addEventListener('click', handleCancel);
}
