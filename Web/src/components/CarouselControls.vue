<template>
  <div>
  <!-- in vue 2.x you need wrap these buttons in a div -->
  <button class="carousel-control left" @click="$emit('prev')">◁</button>
  <button class="carousel-control right" @click="$emit('next')">▷</button>
  </div>
</template>

<script>
export default {
  emits: ["prev", "next"], // vue v3
};
</script>
<style scoped>
@font-face {
    font-family: 'ONE-Mobile-POP';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2105_2@1.0/ONE-Mobile-POP.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}
.carousel-control {
  font-family: 'ONE-Mobile-POP';
  background-color: rgba(255, 255, 255, 0);
  border: none;
  display: inline-block;
  position: absolute;
  height: 50px;
  width: 70px;
  top: calc(50% - 25px);
  color: #000000;
  font-size: 30px;
  cursor: pointer;
}
.left {
  left: 0;
}
.right {
  right: 0;
}
</style>
