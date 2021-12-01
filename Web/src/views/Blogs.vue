<template>
  <div class = 'Blogs'>
  <carousel :slides="slides" :interval="3000" controls indicators></carousel>
    <div v-if="!user" class="updates">
      <div class="container">
        <router-link class="router-button" :to="{name : 'Delivery'}"
          >Deliver to your home!</router-link>
          
      </div>
    </div>
  </div>
</template>

<script>
import Carousel from "../components/Carousel.vue";
export default {
  name: "Blogs",
  components: { Carousel },
  data: () => ({
    slides: [
      require('../assets/photobook/1.jpg'),
      require('../assets/photobook/2.jpg'),
      require('../assets/photobook/3.jpg'),
      require('../assets/photobook/4.jpg'),
      require('../assets/photobook/5.jpg'),
      require('../assets/photobook/6.jpg'),
      require('../assets/photobook/7.jpg'),
      require('../assets/photobook/8.jpg'),
      require('../assets/photobook/9.jpg'),
      require('../assets/photobook/10.jpg')

    ],
  }),
};
</script>

<style lang="scss" scoped>
.updates {
  .container {

    padding: 50px 25px;
    display: flex;
    flex-direction: column;
    align-items: center;
    @media (min-width: 800px) {

      flex-direction: row;
    }

    .router-button {
      display: flex;
      font-size: 14px;
      text-decoration: none;
      @media (min-width: 800px) {
        align-items: center;
        justify-content: center;
        margin-left: 570px;

      }
    }
    h2 {
      font-weight: 300;
      font-size: 32px;
      max-width: 425px;
      width: 100%;
      text-align: center;
      text-transform: uppercase;
      @media (min-width: 800px) {
        text-align: initial;
        font-size: 40px;
      }
    }
  }
}
</style>