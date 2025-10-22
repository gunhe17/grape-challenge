/**
 * Error Handler
 * 에러 처리 유틸리티
 */

/**
 * 에러 메시지 정의
 */
export const ERROR_MESSAGES = {
  // 네트워크 에러
  NETWORK_ERROR: '네트워크 연결을 확인해주세요.',
  SERVER_ERROR: '서버에서 오류가 발생했습니다. 잠시 후 다시 시도해주세요.',

  // API 에러
  FETCH_FRUIT_ERROR: '과일 정보를 불러오는데 실패했습니다.',
  CREATE_FRUIT_ERROR: '씨앗 심기 중 오류가 발생했습니다.',
  COMPLETE_MISSION_ERROR: '미션 완료 중 오류가 발생했습니다.',
  HARVEST_FRUIT_ERROR: '과일 수확 중 오류가 발생했습니다.',
  FETCH_TEMPLATE_ERROR: '과일 템플릿을 찾을 수 없습니다.',

  // 로그인 에러
  LOGIN_ERROR: '로그인 중 오류가 발생했습니다. 다시 시도해주세요.',
  LOGOUT_ERROR: '로그아웃 중 오류가 발생했습니다.',

  // 유효성 검사 에러
  VALIDATION_ERROR: '입력값을 확인해주세요.',
  MIN_LENGTH_ERROR: '5자 이상 작성해주세요.',

  // 상태 에러
  NOT_HARVESTABLE: '아직 수확할 수 없습니다.',
};

/**
 * 사용자에게 에러 메시지 표시
 * @param {string} message - 표시할 메시지
 */
export function showErrorMessage(message) {
  alert(message);
}
