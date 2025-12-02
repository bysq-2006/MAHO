<template>
  <div class="pixi-container"></div>
</template>

<script setup>
import { onMounted } from 'vue'
import { Application, Assets, Sprite } from 'pixi.js'

onMounted(async () => {
  // 创建 Pixi 应用
  const app = new Application()
  await app.init({
    backgroundAlpha: 0,
    resizeTo: window,
  })

  // 挂载到页面指定容器
  document.querySelector('.pixi-container').appendChild(app.canvas)

  // 加载图片资源
  const texture = await Assets.load('/mahotan.png')
  const bunny = new Sprite(texture)
  bunny.anchor.set(0.5)
  bunny.x = app.screen.width / 2
  bunny.y = app.screen.height / 1.8
  bunny.scale.set(0.35)
  app.stage.addChild(bunny)

  // 动画
  app.ticker.add((time) => {
  })
})
</script>