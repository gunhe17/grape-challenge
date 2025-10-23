/**
 * Mission API
 * 모든 미션 관련 API 호출을 중앙에서 관리
 */

export const MissionAPI = {
  /**
   * 이름으로 미션 조회
   * @param {string} name - 미션 템플릿 이름
   * @param {string|null} date - 날짜 필터 ("today" 또는 null)
   * @returns {Promise<Object>} 미션 목록과 개수
   */
  async fetchMissionsByName(name, date = null) {
    try {
      let url = `/mission?name=${encodeURIComponent(name)}`;
      if (date) {
        url += `&date=${encodeURIComponent(date)}`;
      }

      const response = await fetch(url);
      const data = await response.json();

      if (response.ok) {
        return {
          missions: data.missions || [],
          count: data.count || 0
        };
      }

      return { missions: [], count: 0 };
    } catch (error) {
      console.error('미션 조회 오류:', error);
      return { missions: [], count: 0 };
    }
  }
};
