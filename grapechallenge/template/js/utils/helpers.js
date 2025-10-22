/**
 * Common Utility Functions
 * 공통 유틸리티 함수들
 */

import { STAGE_NAMES, UI_CONSTANTS } from './constants.js';

/**
 * 상태 코드로 단계 정보 조회
 * @param {string} status - 과일 상태 (예: 'FIRST_STATUS')
 * @returns {Object} 단계 정보 { level, name, status }
 */
export function getStageInfo(status) {
  return STAGE_NAMES.find(s => s.status === status) || STAGE_NAMES[0];
}

/**
 * 현재 상태에 맞는 이미지/이모지 가져오기
 * @param {Object} fruit - 과일 객체
 * @returns {string} 이미지 URL 또는 이모지
 */
export function getStatusImage(fruit) {
  if (!fruit) return '🌱';

  const statusMap = {
    'FIRST_STATUS': fruit.first_status,
    'SECOND_STATUS': fruit.second_status,
    'THIRD_STATUS': fruit.third_status,
    'FOURTH_STATUS': fruit.fourth_status,
    'FIFTH_STATUS': fruit.fifth_status,
    'SIXTH_STATUS': fruit.sixth_status,
    'SEVENTH_STATUS': fruit.seventh_status
  };

  return statusMap[fruit.status] || '🌱';
}

/**
 * 문자열이 이미지 URL인지 판단
 * @param {string} str - 검사할 문자열
 * @returns {boolean} URL 여부
 */
export function isImageUrl(str) {
  return str && (str.startsWith('http://') || str.startsWith('https://') || str.startsWith('/'));
}

/**
 * 과일 성장 진행률 계산 (0-98%)
 * @param {string} status - 과일 상태
 * @returns {number} 진행률 (0-98)
 */
export function calculateProgress(status) {
  const index = STAGE_NAMES.findIndex(s => s.status === status);
  if (index === -1) return 0;
  return (index / (STAGE_NAMES.length - 1)) * UI_CONSTANTS.MAX_PROGRESS;
}

/**
 * 날짜 포맷팅 (YYYY.MM.DD)
 * @param {string} dateString - ISO 날짜 문자열
 * @returns {string} 포맷된 날짜
 */
export function formatDate(dateString) {
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}.${month}.${day}`;
}
