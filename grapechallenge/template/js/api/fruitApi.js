/**
 * Fruit API
 * 모든 과일 관련 API 호출을 중앙에서 관리
 */

export const FruitAPI = {
  /**
   * 현재 진행 중인 과일 조회
   * @returns {Promise<Object|null>} 과일 정보 또는 null
   */
  async fetchCurrentFruit() {
    try {
      const response = await fetch('/fruit/in-progress');
      const data = await response.json();

      if (response.ok && data.fruit && data.fruit.fruit_id) {
        return {
          fruit: data.fruit,
          missions: data.missions || []
        };
      }

      return null;
    } catch (error) {
      console.error('과일 조회 오류:', error);
      return null;
    }
  },

  /**
   * 새로운 과일 생성
   * @param {string|null} templateId - 템플릿 ID (null이면 랜덤)
   * @returns {Promise<Object|null>} 생성된 과일 정보 또는 null
   */
  async createNewFruit(templateId = null) {
    try {
      const body = templateId ? { template_id: templateId } : {};
      const response = await fetch('/fruit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });

      const data = await response.json();
      return (response.ok && data.id) ? data : null;
    } catch (error) {
      console.error('과일 생성 오류:', error);
      return null;
    }
  },

  /**
   * 미션 완료
   * @param {string} fruitId - 과일 ID
   * @param {string} missionName - 미션 이름
   * @param {string|null} content - 미션 내용 (선택)
   * @returns {Promise<Object|null>} 완료된 미션 정보 또는 null
   */
  async completeMission(fruitId, missionName, content = null) {
    try {
      const body = { fruit_id: fruitId, name: missionName };
      if (content) {
        body.content = content;
      }

      const response = await fetch('/mission/complete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });

      if (!response.ok) {
        const text = await response.text();
        console.error('미션 완료 실패:', response.status, text);
        return null;
      }

      const data = await response.json();
      return data.id ? data : null;
    } catch (error) {
      console.error('미션 완료 오류:', error);
      return null;
    }
  },

  /**
   * 완료된 과일 개수 조회
   * @returns {Promise<number>} 완료된 과일 개수
   */
  async fetchCompletedFruitsCount() {
    try {
      const response = await fetch('/fruits/completed/count');
      const data = await response.json();

      if (response.ok) {
        return data.count || 0;
      }
      return 0;
    } catch (error) {
      console.error('완료된 과일 개수 조회 오류:', error);
      return 0;
    }
  },

  /**
   * 이름으로 과일 템플릿 조회
   * @param {string} name - 템플릿 이름
   * @returns {Promise<string|null>} 템플릿 ID 또는 null
   */
  async fetchFruitTemplateByName(name) {
    try {
      const response = await fetch(`/fruit-template?name=${encodeURIComponent(name)}`);
      const data = await response.json();

      if (response.ok && data.fruit_templates && data.fruit_templates.length > 0) {
        return data.fruit_templates[0].id;
      }
      return null;
    } catch (error) {
      console.error('과일 템플릿 조회 오류:', error);
      return null;
    }
  },

  /**
   * 과일 수확
   * @param {string} fruitId - 과일 ID
   * @returns {Promise<Object|null>} 수확된 과일 정보 또는 null
   */
  async harvestFruit(fruitId) {
    try {
      const response = await fetch('/fruit/harvest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fruit_id: fruitId })
      });

      const data = await response.json();
      return (response.ok && data.id) ? data : null;
    } catch (error) {
      console.error('과일 수확 오류:', error);
      return null;
    }
  },

  /**
   * 테스트 미션 완료 (dev 전용, 제한 없음)
   * @param {string} fruitId - 과일 ID
   * @returns {Promise<Object|null>} 완료된 미션 정보 또는 null
   */
  async completeTestMission(fruitId) {
    try {
      const response = await fetch('/mission/test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fruit_id: fruitId })
      });

      if (!response.ok) {
        const text = await response.text();
        console.error('테스트 미션 완료 실패:', response.status, text);
        return null;
      }

      const data = await response.json();
      return data.fruit_id ? data : null;
    } catch (error) {
      console.error('테스트 미션 완료 오류:', error);
      return null;
    }
  }
};
