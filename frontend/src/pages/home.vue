<template>
  <div class="home-page">
    <div v-if="wsStatus !== 'connected'" class="ws-status-tip">WebSocket连接失效，正在尝试连接...</div>
    <dialogBox class="dialog" />
    <illustration class="illustrat" />
    <div class="meswin-bg"></div>
  </div>
</template>

<script setup>
import illustration from './illustration.vue'
import dialogBox from './dialogBox.vue'
import { onMounted } from 'vue'
import { useHomeStore } from '@/stores/home'
import { storeToRefs } from 'pinia'
const homeStore = useHomeStore()
const { audioQueue, wsStatus } = storeToRefs(homeStore)

const playAudio = (blob) => {
  return new Promise((resolve) => {
    const url = URL.createObjectURL(blob)
    const audio = new Audio(url)
    audio.onended = () => {
      URL.revokeObjectURL(url)
      resolve()
    }
    audio.onerror = (e) => {
      console.error('Audio playback error:', e)
      URL.revokeObjectURL(url)
      resolve()
    }
    audio.play().catch(e => {
      console.error('Play failed:', e)
      resolve()
    })
  })
}

const processAudioQueue = async () => {
  let audioBuffer = ''
  while (true) {
    if (audioQueue.length > 0) {
      const chunk = audioQueue.shift()
      if (chunk) {
        audioBuffer += chunk.data
        if (chunk.is_final) {
          try {
            const binaryString = window.atob(audioBuffer)
            const len = binaryString.length
            const bytes = new Uint8Array(len)
            for (let i = 0; i < len; i++) {
              bytes[i] = binaryString.charCodeAt(i)
            }
            const blob = new Blob([bytes], { type: 'audio/wav' })
            await playAudio(blob)
          } catch (error) {
            console.error('音频播放失败:', error)
          } finally {
            audioBuffer = ''
          }
        }
      }
    } else {
      await new Promise(resolve => setTimeout(resolve, 100))
    }
  }
}

onMounted(() => {
  processAudioQueue()
})
</script>

<style scoped>
.illustrat {
  position: absolute;
}

.home-page {
  background-image: url('/bg.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: 100vh;
  position: relative;
}

.ws-status-tip {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  text-align: center;
  color: #e6a23c;
  font-family: 'Microsoft YaHei', 'SimHei', '黑体', 'STHeiti', sans-serif;
  font-size: 2.1vw;
  text-shadow: 2px 2px 6px #000, 0 0 1px #fff;
  padding: 0.5em 0;
  border: none;
  border-bottom: 2px solid #e6a23c;
  letter-spacing: 0.05em;
  line-height: 1.6;
  box-sizing: border-box;
  background: none;
  z-index: 10;
}

.dialog {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2;
}
</style>