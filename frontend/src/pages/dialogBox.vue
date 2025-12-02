<template>
  <div>
    <CenterRevealMask :visible="showMask">
      <img src="/meswin.png" alt="图片丢失" class="bg">
      <meswinName :name="currentName" class="Meswinname" />
      <textarea :readonly="isWaiting" name="dialog-textarea" id="dialog-textarea" class="dialog-textarea"
        v-model="dialogText" @keyup="sendTextToWS" ref="textareaRef"></textarea>
      <SpritePlayer v-if="!isWaiting" src="/ring.png" :rows="12" :columns="5" :fps="45" :width="spriteSize"
        :height="spriteSize" :totalFrames="60" :loop="0"
        :style="{ position: 'fixed', left: caretX + 'px', top: caretY + 'px', pointerEvents: 'none', zIndex: 9999 }" />
    </CenterRevealMask>
  </div>
</template>

<script setup lang="js">
import meswinName from '@/component/meswinName.vue';
import { useHomeStore } from '@/stores/home';
import { ref, onMounted, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import CenterRevealMask from '../component/CenterRevealMask.vue'
import SpritePlayer from '../component/SpritePlayer.vue'
// @ts-ignore
import getCaretCoordinates from 'textarea-caret';

const homeStore = useHomeStore()
const { textQueue, isWaiting, currentName } = storeToRefs(homeStore)
const WS = homeStore.WS
const showMask = ref(false)

const dialogText = ref('');
const caretX = ref(0)
const caretY = ref(0)
const textareaRef = ref()
const spriteSize = ref(window.innerWidth * 0.025)

function updateCaret() {
  const textarea = textareaRef.value;
  if (!textarea) return
  const pos = textarea.value.length; // 末尾位置
  const coords = getCaretCoordinates(textarea, pos);
  caretX.value = coords.left + window.innerWidth * 0.018
  caretY.value = coords.top + window.innerWidth * 0.008
}

function sendTextToWS(e) {
  if (e.key === 'Enter' && !e.shiftKey && !isWaiting.value) {
    e.preventDefault(); // 阻止默认的换行行为
    const message = dialogText.value.trim();
    if (message) {
      WS.send(JSON.stringify({ type: 'user_input', data: message }));
      dialogText.value = ''; // 发送后清空输入框
    }
  }
}

async function processTextQueue() {
  while (true) {
    updateCaret(); // 更新光标位置
    if (!isWaiting.value) {
      await new Promise(resolve => setTimeout(resolve, 100)); // 等待100ms再检查
      continue;
    }
    await nextTick(); // 等待下一帧，防止阻塞
    // 取出所有字符并筛选
    const filtered = textQueue.value.filter(ch => ch !== '\n' && ch.trim() !== '');
    dialogText.value = filtered.join('');
    await new Promise(resolve => setTimeout(resolve, 100)); // 100ms轮询
  }
}

window.addEventListener('resize', () => {
  spriteSize.value = window.innerWidth * 0.025
})

onMounted(() => {
  processTextQueue();
  setTimeout(() => {
    showMask.value = true
    updateCaret()
  }, 1000)
})
</script>

<style>
.Meswinname {
  position: absolute;
  bottom: 2vw;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
}

.dialog-textarea {
  background: rgba(0, 0, 0, 0.0);
  color: #e6e6e6;
  font-family: 'Microsoft YaHei', 'SimHei', '黑体', 'STHeiti', sans-serif;
  font-size: 2.1vw;
  text-shadow: 2px 2px 6px #000, 0 0 1px #fff;
  padding: 0em 6em;
  border: none;
  border-radius: 0.2em;
  letter-spacing: 0.05em;
  line-height: 1.6;
  box-sizing: border-box;
  border-bottom: 2px solid #e6a23c;
  margin: 0 auto;
  overflow: hidden;
  /* 隐藏滚动条 */
  resize: none;

  position: absolute;
  bottom: 0;
  left: 0;

  width: 100vw;
  height: 16vw;
  overflow-y: auto;
  /* 保持可滚动 */
  scrollbar-width: none;
  /* Firefox 隐藏滚动条 */
}

.dialog-textarea::-webkit-scrollbar {
  width: 0px;
  /* Chrome/Safari 隐藏滚动条 */
  background: transparent;
}

.bg {
  width: 100vw;
  display: block;
}
</style>