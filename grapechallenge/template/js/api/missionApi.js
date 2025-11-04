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
  },

  /**
   * 미션에 interaction 추가
   * @param {string} missionId - 미션 ID
   * @param {string} emoji - 이모지 (😆, 😮, 💪, 🙏, 👏)
   * @returns {Promise<Object>} 업데이트된 미션 데이터
   */
  async addInteraction(missionId, emoji) {
    try {
      const response = await fetch('/mission/interaction', {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          mission_id: missionId,
          emoji: emoji
        })
      });

      const data = await response.json();

      if (response.ok) {
        return {
          success: true,
          mission: data
        };
      }

      return {
        success: false,
        message: data.message || '인터랙션 추가 실패'
      };
    } catch (error) {
      console.error('인터랙션 추가 오류:', error);
      return {
        success: false,
        message: '네트워크 오류가 발생했습니다'
      };
    }
  }
};
