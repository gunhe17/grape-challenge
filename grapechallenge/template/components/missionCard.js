/**
 * Mission Card Components
 * 미션 카드 UI 컴포넌트들
 */

import { EVENT_FRUIT_CONDITIONS } from '../js/utils/constants.js';

export const MissionCard = {
  /**
   * 씨앗 심기 카드 생성
   * @param {Function} onPlantSeed - 씨앗 심기 핸들러
   * @param {number} completedCount - 완료된 과일 개수
   * @returns {HTMLElement} 카드 엘리먼트
   */
  createPlantSeedCard(onPlantSeed, completedCount = 0) {
    const isEventFruit = completedCount === EVENT_FRUIT_CONDITIONS.FIRST ||
                         completedCount === EVENT_FRUIT_CONDITIONS.SECOND;

    const cardClass = isEventFruit
      ? 'relative rounded-xl bg-gradient-to-br from-yellow-50 via-orange-50 to-red-50 px-7 py-5 shadow-lg outline outline-3 -outline-offset-1 outline-orange-400 animate-scale-in'
      : 'relative rounded-xl bg-gradient-to-br from-green-50 to-emerald-50 px-7 py-5 shadow-sm outline outline-2 -outline-offset-1 outline-green-300 animate-scale-in';

    const icon = isEventFruit ? '🎁' : '🌱';
    const title = isEventFruit ? '탕이를 발견했어요!' : '새로운 씨앗 심기';
    const description = isEventFruit ? '탕이가 남긴 씨앗을 키워보세요.' : '새로운 씨앗을 심어보세요.';

    const buttonClass = isEventFruit
      ? 'plant-seed-btn rounded-lg bg-gradient-to-r from-orange-500 to-red-500 px-4 py-2 text-sm font-semibold text-white shadow-md hover:from-orange-600 hover:to-red-600 animate-pulse'
      : 'plant-seed-btn rounded-lg bg-green-600 px-4 py-2 text-sm font-semibold text-white shadow-xs hover:bg-green-500';

    const card = document.createElement('div');
    card.className = cardClass;
    card.innerHTML = `
      <div class="flex items-center justify-between gap-x-5">
        <div class="flex-1 min-w-0">
          <p class="text-base font-semibold tracking-tight text-gray-900">${icon} ${title}</p>
          <p class="mt-1 text-sm text-gray-600">${description}</p>
        </div>
        <div class="flex-none">
          <button class="${buttonClass}">
            시작하기
          </button>
        </div>
      </div>
    `;
    card.querySelector('.plant-seed-btn').addEventListener('click', onPlantSeed);
    return card;
  },

  /**
   * 모든 미션 완료 알림 카드 생성
   * @returns {HTMLElement} 카드 엘리먼트
   */
  createAllMissionsCompletedCard() {
    const card = document.createElement('div');
    card.className = 'relative rounded-xl bg-gradient-to-br from-orange-50 to-amber-50 px-7 py-5 mb-3.5 shadow-sm outline outline-2 -outline-offset-1 outline-orange-300 animate-scale-in';
    card.innerHTML = `
      <div class="flex items-center gap-x-3.5">
        <div class="flex-none text-2xl">🎉</div>
        <div class="flex-1 min-w-0">
          <p class="text-base font-semibold tracking-tight text-gray-900">오늘의 미션을 모두 완료했어요!</p>
          <p class="mt-1 text-sm text-gray-600">내일 또 새로운 미션으로 만나요</p>
        </div>
      </div>
    `;
    return card;
  },

  /**
   * 수확하기 카드 생성
   * @param {Function} onHarvest - 수확하기 핸들러
   * @returns {HTMLElement} 카드 엘리먼트
   */
  createHarvestActionCard(onHarvest) {
    const card = document.createElement('div');
    card.className = 'relative rounded-xl bg-gradient-to-br from-yellow-50 to-orange-50 px-7 py-5 mb-3.5 shadow-sm outline outline-2 -outline-offset-1 outline-yellow-300 animate-scale-in';
    card.innerHTML = `
      <div class="flex items-center justify-between gap-x-5">
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-x-2.5">
            <div class="flex-none text-2xl">🎉</div>
            <div>
              <p class="text-base font-semibold tracking-tight text-gray-900">과일이 완성되었습니다!</p>
              <p class="mt-1 text-sm text-gray-600">수확하기 버튼을 눌러 과일을 수확하세요</p>
            </div>
          </div>
        </div>
        <div class="flex-none">
          <button class="harvest-btn rounded-lg bg-yellow-600 px-4 py-2 text-sm font-semibold text-white shadow-xs hover:bg-yellow-500">
            수확하기
          </button>
        </div>
      </div>
    `;
    card.querySelector('.harvest-btn').addEventListener('click', onHarvest);
    return card;
  },

  /**
   * 일반 미션 카드 생성
   * @param {Object|null} mission - 미션 정보
   * @param {Function} onCompleteMission - 미션 완료 핸들러
   * @returns {HTMLElement} 카드 엘리먼트
   */
  createDailyMissionCard(mission, onCompleteMission) {
    const missionName = mission?.name || '오늘의 미션';
    const missionContent = mission?.content || '말씀 한 장 읽기';
    const canComplete = mission?.can_complete ?? true;

    const buttonDisabled = canComplete ? '' : 'disabled';
    const buttonClass = canComplete
      ? 'rounded-lg bg-orange-500 px-4 py-2 text-sm font-semibold text-white shadow-xs hover:bg-orange-400'
      : 'rounded-lg bg-orange-100 px-4 py-2 text-sm font-semibold text-orange-600 shadow-xs cursor-not-allowed';
    const buttonText = canComplete ? '완료' : '완료됨';

    const card = document.createElement('div');
    card.className = 'relative rounded-xl bg-white px-7 py-5 mb-3.5 shadow-sm outline outline-1 -outline-offset-1 outline-gray-200 hover:outline-orange-200 animate-fade-in-up';

    card.innerHTML = `
      <div class="flex items-center justify-between gap-x-5">
        <div class="flex-1 min-w-0">
          <p class="text-base font-semibold tracking-tight text-gray-900">${missionName}</p>
          <p class="mt-1 text-sm text-gray-600">${missionContent}</p>
        </div>
        <div class="flex-none">
          <button class="complete-mission-btn ${buttonClass}" ${buttonDisabled} data-mission-name="${missionName}">
            ${buttonText}
          </button>
        </div>
      </div>
    `;

    if (canComplete) {
      card.querySelector('.complete-mission-btn').addEventListener('click', onCompleteMission);
    }
    return card;
  },

  /**
   * 테스트 미션 카드 생성
   * @param {Function} onTestMission - 테스트 미션 핸들러
   * @returns {HTMLElement} 카드 엘리먼트
   */
  createTestMissionCard(onTestMission) {
    const card = document.createElement('div');
    card.className = 'relative rounded-xl bg-gradient-to-br from-purple-50 to-pink-50 px-7 py-5 mb-3.5 shadow-sm outline outline-2 -outline-offset-1 outline-purple-300 animate-fade-in-up';
    card.innerHTML = `
      <div class="flex items-center justify-between gap-x-5">
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-x-2">
            <p class="text-base font-semibold tracking-tight text-gray-900">🧪 테스트 미션 (말씀 읽기)</p>
            <span class="inline-flex items-center rounded-md bg-purple-100 px-2 py-1 text-xs font-medium text-purple-700">TEST</span>
          </div>
          <p class="mt-1 text-sm text-gray-600">테스트용 미션 - 제한 없이 반복 가능</p>
          <p class="mt-1 text-xs text-purple-600">⚠️ 개발/테스트 전용 미션입니다</p>
        </div>
        <div class="flex-none">
          <button class="test-mission-btn rounded-lg bg-purple-500 px-4 py-2 text-sm font-semibold text-white shadow-xs hover:bg-purple-400">
            완료
          </button>
        </div>
      </div>
    `;
    card.querySelector('.test-mission-btn').addEventListener('click', onTestMission);
    return card;
  }
};
