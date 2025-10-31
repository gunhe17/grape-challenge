/**
 * Home Page Logic
 * 홈 페이지의 비즈니스 로직과 이벤트 핸들러
 */

import { FruitAPI } from '../api/fruitApi.js';
import { MissionCard } from '../../components/missionCard.js';
import { getStageInfo, getStatusImage, isImageUrl, calculateProgress } from '../utils/helpers.js';
import { FRUIT_STATUS, UI_CONSTANTS, MISSION_NAMES, EVENT_FRUIT_TEMPLATES, EVENT_FRUIT_CONDITIONS } from '../utils/constants.js';
import { AuthAPI } from '../api/authApi.js';

// ========================
// 전역 상태
// ========================
let currentFruit = null;
let currentMissions = [];
let scrollPosition = 0;

// ========================
// 초기화
// ========================
export async function initHomePage() {
  await fetchAndUpdateFruit();
  updateUI();
  setupEventListeners();
}

function setupEventListeners() {
  // Logout button is now handled by Sidebar component
}

// ========================
// 데이터 조회
// ========================
async function fetchAndUpdateFruit() {
  const data = await FruitAPI.fetchCurrentFruit();

  if (data) {
    currentFruit = data.fruit;
    currentMissions = data.missions;
  } else {
    currentFruit = null;
    currentMissions = [];
  }
}

// ========================
// UI 업데이트
// ========================
async function updateUI() {
  if (!currentFruit) {
    updateProgressCircle(0);
    updateStageDisplay(null, { level: 0, name: '씨앗을 심어주세요' });
    await updateMissions(null);
    return;
  }

  const stageInfo = getStageInfo(currentFruit.status);
  const progress = calculateProgress(currentFruit.status);

  updateProgressCircle(progress);
  updateStageDisplay(currentFruit, stageInfo);
  await updateMissions(currentFruit);
}

function updateProgressCircle(progress) {
  const offset = UI_CONSTANTS.CIRCLE_CIRCUMFERENCE - (progress / 100) * UI_CONSTANTS.CIRCLE_CIRCUMFERENCE;
  document.getElementById('progress-circle').style.strokeDashoffset = offset;
}

function updateStageDisplay(fruit, stageInfo) {
  const emojiElement = document.getElementById('stage-emoji');
  const stageText = `${stageInfo.level}단계`;

  if (!fruit) {
    emojiElement.textContent = '';
    document.getElementById('stage-text').textContent = stageText;
    return;
  }

  const image = getStatusImage(fruit);

  if (isImageUrl(image)) {
    emojiElement.innerHTML = `<img src="${image}" alt="fruit" class="w-full h-full object-contain">`;
  } else {
    emojiElement.textContent = image;
  }

  document.getElementById('stage-text').textContent = stageText;
}

async function updateMissions(fruit) {
  const container = document.getElementById('mission-container');

  // Remove skeleton if it exists
  const skeleton = container.querySelector('.mission-skeleton');
  if (skeleton) {
    skeleton.remove();
  }

  // Clear container
  container.innerHTML = '';

  if (!fruit) {
    const completedCount = await FruitAPI.fetchCompletedFruitsCount();
    const card = MissionCard.createPlantSeedCard(handlePlantSeed, completedCount);
    container.appendChild(card);
    return;
  }

  let cardIndex = 0;

  if (fruit.status === FRUIT_STATUS.SEVENTH) {
    const card = MissionCard.createHarvestActionCard(handleHarvest);
    card.style.animationDelay = `${cardIndex * UI_CONSTANTS.ANIMATION_DELAY_STEP}s`;
    container.appendChild(card);
    return;
  }

  // check if all missions are completed
  const allCompleted = currentMissions.length > 0 && currentMissions.every(m => !m.can_complete);

  if (allCompleted) {
    const completionCard = MissionCard.createAllMissionsCompletedCard();
    completionCard.style.animationDelay = `${cardIndex * UI_CONSTANTS.ANIMATION_DELAY_STEP}s`;
    container.appendChild(completionCard);
    cardIndex++;
  }

  if (currentMissions.length > 0) {
    currentMissions.forEach(mission => {
      const card = MissionCard.createDailyMissionCard(mission, handleCompleteMission);
      card.style.animationDelay = `${cardIndex * UI_CONSTANTS.ANIMATION_DELAY_STEP}s`;
      container.appendChild(card);
      cardIndex++;
    });
  } else {
    const card = MissionCard.createDailyMissionCard(null, handleCompleteMission);
    card.style.animationDelay = `${cardIndex * UI_CONSTANTS.ANIMATION_DELAY_STEP}s`;
    container.appendChild(card);
    cardIndex++;
  }

  // Add test mission card in dev environment
  if (window.APP_ENV === 'dev') {
    const testCard = MissionCard.createTestMissionCard(handleTestMission);
    testCard.style.animationDelay = `${cardIndex * UI_CONSTANTS.ANIMATION_DELAY_STEP}s`;
    container.appendChild(testCard);
    cardIndex++;
  }
}

// ========================
// 이벤트 핸들러
// ========================
async function handlePlantSeed(event) {
  const btn = event.target;
  btn.disabled = true;

  // count completed fruits before creating new fruit
  const completedCount = await FruitAPI.fetchCompletedFruitsCount();

  let templateId = null;
  let templateName = null;

  // check conditions for event fruits
  if (completedCount === EVENT_FRUIT_CONDITIONS.FIRST) {
    templateName = EVENT_FRUIT_TEMPLATES.FIRST;
  } else if (completedCount === EVENT_FRUIT_CONDITIONS.SECOND) {
    templateName = EVENT_FRUIT_TEMPLATES.SECOND;
  }

  // fetch template if event fruit
  if (templateName) {
    templateId = await FruitAPI.fetchFruitTemplateByName(templateName);
    if (!templateId) {
      alert(`${templateName} 템플릿을 찾을 수 없습니다.`);
      btn.textContent = '시작하기';
      btn.disabled = false;
      return;
    }
  }

  const result = await FruitAPI.createNewFruit(templateId);

  if (result) {
    await fetchAndUpdateFruit();
    updateUI();
  } else {
    alert('씨앗 심기 중 오류가 발생했습니다.');
    btn.textContent = '시작하기';
    btn.disabled = false;
  }
}

async function handleCompleteMission(event) {
  const btn = event.target;
  if (!currentFruit) return;

  const missionName = btn.getAttribute('data-mission-name');

  // show modal for gratitude diary
  if (missionName === MISSION_NAMES.GRATITUDE_DIARY) {
    showGratitudeModal(btn);
    return;
  }

  // show modal for bible reading
  if (missionName === MISSION_NAMES.BIBLE_READING) {
    showBibleModal(btn);
    return;
  }

  // complete mission without content
  btn.disabled = true;

  const result = await FruitAPI.completeMission(currentFruit.fruit_id, missionName, null);

  if (result) {
    await fetchAndUpdateFruit();
    updateUI();
  } else {
    alert('미션 완료 중 오류가 발생했습니다.');
    btn.textContent = '완료';
    btn.disabled = false;
  }
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

function showGratitudeModal(btn) {
  const modal = document.getElementById('gratitude-modal');
  const contentTextarea = document.getElementById('gratitude-content');
  const charCountEl = document.getElementById('gratitude-char-count');
  const submitBtn = document.getElementById('gratitude-submit-btn');
  const cancelBtn = document.getElementById('gratitude-cancel-btn');

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

    // Update character count
    charCountEl.textContent = charCount;

    // Update submit button state
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

    // hide modal
    modal.classList.add('hidden');
    unlockBodyScroll();

    // complete mission with content
    btn.disabled = true;

    const result = await FruitAPI.completeMission(currentFruit.fruit_id, MISSION_NAMES.GRATITUDE_DIARY, content);

    if (result) {
      await fetchAndUpdateFruit();
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

async function showBibleModal(btn) {
  const modal = document.getElementById('bible-modal');
  const checkbox = document.getElementById('bible-read-checkbox');
  const closeBtn = document.getElementById('bible-close-btn');

  // Reset state
  checkbox.checked = false;
  closeBtn.disabled = true;

  // Fetch today's bible verse
  try {
    const response = await fetch('/bible/today', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();

    // Display bible verse in modal
    const verseContent = document.getElementById('bible-verse-content');

    if (!response.ok) {
      // Show fallback message
      verseContent.innerHTML = `
        <div class="mb-4">
          <p class="text-base text-gray-800 leading-relaxed text-center">
            ${data.message || '오늘의 말씀이 준비되지 않았습니다. 자유롭게 성경을 읽어보세요!'}
          </p>
        </div>
      `;
    } else {
      // Show bible verse
      verseContent.innerHTML = `
        <div class="mb-4">
          <p class="text-sm font-semibold text-orange-600 mb-4">${data.reference}</p>
          <p class="text-base text-gray-800 leading-relaxed whitespace-pre-wrap">${data.content}</p>
        </div>
      `;
    }

    // lock body scroll
    lockBodyScroll();

    // Show modal
    modal.classList.remove('hidden');

    // Handle checkbox change
    const handleCheckboxChange = () => {
      closeBtn.disabled = !checkbox.checked;
    };

    // Handle close
    const handleClose = async () => {
      if (!checkbox.checked) return;

      modal.classList.add('hidden');
      unlockBodyScroll();

      // Complete mission
      btn.disabled = true;

      const result = await FruitAPI.completeMission(currentFruit.fruit_id, MISSION_NAMES.BIBLE_READING, null);

      if (result) {
        await fetchAndUpdateFruit();
        updateUI();
      } else {
        alert('미션 완료 중 오류가 발생했습니다.');
        btn.textContent = '완료';
        btn.disabled = false;
      }

      cleanup();
    };

    // Cleanup listeners
    const cleanup = () => {
      checkbox.removeEventListener('change', handleCheckboxChange);
      closeBtn.removeEventListener('click', handleClose);
    };

    // Add listeners
    checkbox.addEventListener('change', handleCheckboxChange);
    closeBtn.addEventListener('click', handleClose);

  } catch (error) {
    console.error('Bible verse fetch error:', error);
    alert('오늘의 말씀을 불러오는 중 오류가 발생했습니다.');
  }
}

async function handleHarvest(event) {
  const btn = event.target;
  if (!currentFruit) return;

  if (currentFruit.status !== FRUIT_STATUS.SEVENTH) {
    alert('아직 수확할 수 없습니다.');
    return;
  }

  btn.disabled = true;
  btn.textContent = '수확 중...';

  const result = await FruitAPI.harvestFruit(currentFruit.fruit_id);

  if (result) {
    btn.textContent = '수확 완료! 🎉';
    setTimeout(async () => {
      await fetchAndUpdateFruit();
      updateUI();
    }, 1500);
  } else {
    alert('수확 중 오류가 발생했습니다.');
    btn.textContent = '수확하기';
    btn.disabled = false;
  }
}

async function handleTestMission(event) {
  const btn = event.target;
  if (!currentFruit) return;

  btn.disabled = true;
  btn.textContent = '완료 중...';

  const result = await FruitAPI.completeTestMission(currentFruit.fruit_id);

  if (result) {
    await fetchAndUpdateFruit();
    updateUI();
  } else {
    alert('테스트 미션 완료 중 오류가 발생했습니다.');
    btn.textContent = '완료';
    btn.disabled = false;
  }
}

async function handleLogout() {
  if (!confirm('로그아웃 하시겠습니까?')) return;

  await AuthAPI.logout();
  AuthAPI.redirectToLogin();
}
