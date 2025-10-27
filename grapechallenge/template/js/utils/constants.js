/**
 * Application Constants
 * 애플리케이션 전역 상수
 */

/**
 * 과일 성장 단계 정의
 */
export const STAGE_NAMES = [
  { level: 1, name: '씨앗', status: 'FIRST_STATUS' },
  { level: 2, name: '새싹', status: 'SECOND_STATUS' },
  { level: 3, name: '묘목', status: 'THIRD_STATUS' },
  { level: 4, name: '어린나무', status: 'FOURTH_STATUS' },
  { level: 5, name: '큰나무', status: 'FIFTH_STATUS' },
  { level: 6, name: '꽃', status: 'SIXTH_STATUS' },
  { level: 7, name: '열매', status: 'SEVENTH_STATUS' }
];

/**
 * 과일 상태 코드
 */
export const FRUIT_STATUS = {
  FIRST: 'FIRST_STATUS',
  SECOND: 'SECOND_STATUS',
  THIRD: 'THIRD_STATUS',
  FOURTH: 'FOURTH_STATUS',
  FIFTH: 'FIFTH_STATUS',
  SIXTH: 'SIXTH_STATUS',
  SEVENTH: 'SEVENTH_STATUS',
  COMPLETED: 'COMPLETED'
};

/**
 * UI 상수
 */
export const UI_CONSTANTS = {
  CIRCLE_CIRCUMFERENCE: 534.07,  // 진행률 원 둘레
  MAX_PROGRESS: 98,              // 최대 진행률 (100%가 아닌 98%)
  ANIMATION_DELAY_STEP: 0.1,     // 카드 애니메이션 지연 시간 (초)
};

/**
 * 미션 이름 상수
 */
export const MISSION_NAMES = {
  GRATITUDE_DIARY: '감사 일기 작성하기',
  BIBLE_READING: '말씀 읽기',
};

/**
 * 이벤트 과일 템플릿 이름
 */
export const EVENT_FRUIT_TEMPLATES = {
  FIRST: '첫번째 탕이 과일',
  SECOND: '두번째 탕이 과일',
};

/**
 * 이벤트 과일 조건
 */
export const EVENT_FRUIT_CONDITIONS = {
  FIRST: 1,   // 1개 완료 후
  SECOND: 5,  // 5개 완료 후
};
