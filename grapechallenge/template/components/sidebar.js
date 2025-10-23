/**
 * Sidebar Component
 * 모바일 사이드바 메뉴 컴포넌트
 */

import { AuthAPI } from '../js/api/authApi.js';

export const Sidebar = {
  /**
   * 사이드바 HTML 생성
   * @returns {string} 사이드바 HTML
   */
  createHTML() {
    return `
      <el-dialog>
        <dialog id="mobile-menu" class="backdrop:bg-transparent">
          <div tabindex="0" class="fixed inset-0 focus:outline-none">
            <el-dialog-panel class="fixed inset-y-0 right-0 z-50 w-full overflow-y-auto bg-white p-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10 animate-slide-in">
              <div class="flex items-center justify-between">
                <a href="/home" class="-m-1.5 p-1.5 cursor-pointer">
                  <span class="text-xl font-bold text-black">말씀 챌린지</span>
                </a>
                <button type="button" command="close" commandfor="mobile-menu" class="-m-2.5 rounded-md p-2.5 text-gray-700 hover:bg-gray-100 transition-colors">
                  <span class="sr-only">메뉴 닫기</span>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" data-slot="icon" aria-hidden="true" class="size-6">
                    <path d="M6 18 18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </button>
              </div>
              <div class="mt-6 flow-root">
                <div class="-my-6 divide-y divide-gray-500/10">
                  <div class="space-y-2 py-6">
                    <a href="/grove" class="-mx-3 block rounded-lg px-3 py-2.5 text-base/7 font-semibold text-gray-900 hover:bg-orange-50 hover:text-orange-600 transition-all duration-200">과수원</a>
                    <a href="/diary" class="-mx-3 block rounded-lg px-3 py-2.5 text-base/7 font-semibold text-gray-900 hover:bg-orange-50 hover:text-orange-600 transition-all duration-200">감사일기장</a>
                    <a href="https://www.notion.so/gun17/29470a02a0b780d1b3f6ffb3a80e4189?source=copy_link" target="_blank" rel="noopener noreferrer" class="-mx-3 block rounded-lg px-3 py-2.5 text-base/7 font-semibold text-gray-900 hover:bg-orange-50 hover:text-orange-600 transition-all duration-200">문의하기</a>
                    <button id="sidebar-logout-btn" class="-mx-3 block rounded-lg px-3 py-2.5 text-base/7 font-semibold text-red-600 hover:bg-red-50 hover:text-red-700 transition-all duration-200 w-full text-left">로그아웃</button>
                  </div>
                </div>
              </div>
            </el-dialog-panel>
          </div>
        </dialog>
      </el-dialog>
    `;
  },

  /**
   * 사이드바 초기화 및 이벤트 리스너 설정
   */
  init() {
    const logoutBtn = document.getElementById('sidebar-logout-btn');
    if (logoutBtn) {
      logoutBtn.addEventListener('click', this.handleLogout);
    }
  },

  /**
   * 로그아웃 핸들러
   */
  async handleLogout() {
    if (!confirm('로그아웃 하시겠습니까?')) return;

    await AuthAPI.logout();
    AuthAPI.redirectToLogin();
  }
};
