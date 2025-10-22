/**
 * Authentication API
 * 인증 관련 API 호출 관리
 */

import { ERROR_MESSAGES } from '../utils/errorHandler.js';

export const AuthAPI = {
  /**
   * 로그인
   * @param {string} cell - 셀 이름
   * @param {string} name - 사용자 이름
   * @returns {Promise<Object>} 로그인 결과 { success: boolean, userId?: string, message?: string }
   */
  async login(cell, name) {
    try {
      const response = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cell, name }),
        credentials: 'same-origin'
      });

      const data = await response.json();

      if (response.ok && data.user_id) {
        return { success: true, userId: data.user_id };
      }

      return {
        success: false,
        message: data.message || ERROR_MESSAGES.LOGIN_ERROR
      };
    } catch (error) {
      return {
        success: false,
        message: ERROR_MESSAGES.LOGIN_ERROR
      };
    }
  },

  /**
   * 로그아웃
   * @returns {Promise<boolean>} 성공 여부
   */
  async logout() {
    try {
      const response = await fetch('/logout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      });

      return response.ok;
    } catch (error) {
      return false;
    }
  },

  /**
   * 로그인 상태 확인
   * @returns {Promise<boolean>} 로그인 여부
   */
  async isLoggedIn() {
    try {
      const response = await fetch('/fruit/in-progress');

      if (response.status === 401) {
        return false;
      }

      if (response.ok) {
        return true;
      }

      return false;
    } catch (error) {
      return false;
    }
  },

  /**
   * 로그인 페이지로 리다이렉트
   */
  redirectToLogin() {
    window.location.href = '/login';
  },

  /**
   * 홈 페이지로 리다이렉트
   */
  redirectToHome() {
    window.location.href = '/home';
  }
};
