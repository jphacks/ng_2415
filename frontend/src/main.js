// main.js
import Vue from 'vue';
import App from './App.vue';
import 'bootstrap/dist/css/bootstrap.min.css'; // BootstrapのCSSをインポート
import VueRouter from 'vue-router'; // Vue Routerをインポート
import Vuex from 'vuex'; // Vuexをインポート
import axios from 'axios'; // axiosをインポート

// axiosのデフォルト値を設定
axios.defaults.baseURL = 'http://localhost:8000/api'; // バックエンドと通信するためのURLを設定

// Vue RouterとVuexを使用する
Vue.use(VueRouter);
Vue.use(Vuex);

// ルーティングの設定（必要に応じてルートを追加）
const routes = [
  { path: '/', component: App },
];

const router = new VueRouter({
  mode: 'history',
  routes // ルートの設定
});

// Vuexストアの設定
const store = new Vuex.Store({
  state: {
    currentScreen: 'home',
    matchedSong: null,
    recordingTime: 0,
  },
  mutations: {
    setScreen(state, screen) {
      state.currentScreen = screen; // スクリーンの状態を変更
    },
    setMatchedSong(state, song) {
      state.matchedSong = song; // マッチした歌を設定
    },
    setRecordingTime(state, time) {
      state.recordingTime = time; // 録音時間を設定
    },
  },
  actions: {
    updateScreen({ commit }, screen) {
      commit('setScreen', screen); // スクリーンを更新するアクション
    },
    updateMatchedSong({ commit }, song) {
      commit('setMatchedSong', song); // マッチした歌を更新するアクション
    },
    updateRecordingTime({ commit }, time) {
      commit('setRecordingTime', time); // 録音時間を更新するアクション
    },
  },
});

// Vueインスタンスの作成
Vue.config.productionTip = false;

new Vue({
  router, // ルーターを登録
  store, // ストアを登録
  render: h => h(App), // Appコンポーネントをレンダリング
}).$mount('#app'); // #appにマウント
