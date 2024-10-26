<template>
  <!-- <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div> -->
  <div class="min-h-screen bg-background flex flex-col">
    <header class="w-full py-4 striped-background relative">
      <h1 class="text-2xl font-bold text-center text-white relative z-10">StandTogether</h1>
    </header>

    <main class="flex-grow flex items-center justify-center p-4">
      <div class="w-full max-w-md bg-white rounded-lg shadow-xl overflow-hidden">
        <div class="p-8">
          <div v-if="currentScreen === 'home'">
            <div class="flex flex-col items-center">
              <button @click="startRecording" class="homebase-button">
                <mic-icon class="mr-2 h-4 w-4" /> 録音開始
              </button>
              <p class="mt-4 text-center text-sm text-gray-600">
                周囲の音声を録音して、最適な応援歌を見つけましょう
              </p>
            </div>
          </div>

          <div v-else-if="currentScreen === 'recording'" class="flex flex-col items-center space-y-4">
            <button @click="stopRecording" class="px-4 py-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition duration-300">
              <square-icon class="mr-2 h-4 w-4" /> 録音停止
            </button>
            <p class="text-lg">録音中: {{ recordingTime }}秒</p>
            <p class="text-sm text-gray-600">周囲の音声を録音しています...</p>
          </div>

          <div v-else-if="currentScreen === 'matching'" class="flex flex-col items-center space-y-4">
            <loader-2-icon class="h-8 w-8 animate-spin" />
            <p class="text-lg">音声を分析中...</p>
            <p class="text-sm text-gray-600">最適な応援歌を探しています</p>
          </div>

          <div v-else-if="currentScreen === 'results' && matchedSong" class="space-y-4">
            <div class="space-y-2">
              <h2 class="text-xl font-semibold">応援歌: {{ matchedSong.title }}</h2>
              <p class="text-gray-600 whitespace-pre-line">
                {{ matchedSong.lyrics }}
              </p>
            </div>
            <div class="flex justify-between">
              <button @click="startRecording" class="px-4 py-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition duration-300">
                <mic-icon class="mr-2 h-4 w-4" /> 新しい録音を開始
              </button>
              <button @click="goHome" class="px-4 py-2 bg-gray-200 text-gray-800 rounded-full hover:bg-gray-300 transition duration-300">
                <home-icon class="mr-2 h-4 w-4" /> ホームに戻る
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
/*import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}
*/
import { ref, onUnmounted } from 'vue'
import axios from 'axios'
//import { MicIcon, SquareIcon, Loader2Icon, HomeIcon } from 'lucide-vue-next'

export default {
  setup() {
    const currentScreen = ref('home')
    const isRecording = ref(false)
    const matchedSong = ref(null)
    const recordingTime = ref(0)
    let timerInterval = null
    let audioContext = null
    let mediaRecorder = null
    let audioChunks = []

    const startRecording = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        audioContext = new AudioContext()
        const source = audioContext.createMediaStreamSource(stream)
        const processor = audioContext.createScriptProcessor(1024, 1, 1)

        source.connect(processor)
        processor.connect(audioContext.destination)

        mediaRecorder = new MediaRecorder(stream)
        mediaRecorder.ondataavailable = (event) => {
          audioChunks.push(event.data)
          sendAudioChunk(event.data)
        }

        mediaRecorder.start(100) // 100ms ごとにデータを送信

        isRecording.value = true
        currentScreen.value = 'recording'
        recordingTime.value = 0
        timerInterval = setInterval(() => {
          recordingTime.value++
        }, 1000)
      } catch (error) {
        console.error('録音の開始に失敗しました:', error)
      }
    }

    const stopRecording = () => {
      if (mediaRecorder) {
        mediaRecorder.stop()
      }
      if (audioContext) {
        audioContext.close()
      }
      clearInterval(timerInterval)
      isRecording.value = false
      currentScreen.value = 'matching'
      // simulateMatching() の呼び出しを削除
    }


    const goHome = () => {
      currentScreen.value = 'home'
      matchedSong.value = null
      recordingTime.value = 0
      audioChunks = []
    }

    const sendAudioChunk = async (chunk) => {
      try {
        const formData = new FormData()
        formData.append('audio', chunk, 'audio.webm')
        const response = await axios.post('/api/audio', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        if (response.data.matchedSong) {
          matchedSong.value = response.data.matchedSong
          currentScreen.value = 'results'
        }
      } catch (error) {
        console.error('音声データの送信に失敗しました:', error)
      }
    }

    onUnmounted(() => {
      clearInterval(timerInterval)
      if (audioContext) {
        audioContext.close()
      }
    })

    return {
      currentScreen,
      isRecording,
      matchedSong,
      recordingTime,
      startRecording,
      stopRecording,
      goHome,
    }
  }
}
</script>

<style>
/*#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}*/
.striped-background::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: repeating-linear-gradient(
    to right,
    #002569, #002569 8.33%,
    #aacd17 8.33%, #aacd17 16.66%,
    #FF2B06 16.66%, #FF2B06 25%,
    #0055A5 25%, #0055A5 33.33%,
    #FFE201 33.33%, #FFE201 41.66%,
    #F97709 41.66%, #F97709 50%,
    #F5C700 50%, #F5C700 58.33%,
    #4C7B98 58.33%, #4C7B98 66.66%,
    #221815 66.66%, #221815 75%,
    #860010 75%, #860010 83.33%,
    #E2D69E 83.33%, #E2D69E 91.66%,
    #1F366A 91.66%, #1F366A 100%
  );
}

.homebase-button {
  width: 120px;
  height: 120px;
  background-color: #0055A5;
  color: white;
  clip-path: polygon(0% 0%, 100% 0%, 100% 85%, 50% 100%, 0% 85%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

.homebase-button:hover {
  background-color: #003d75;
}
</style>
