<template>
  <div class="home">
    <BlogPost v-if="!user" :post="welcomeScreen" />
    <BlogPost
      :post="post"
      v-for="(post, index) in sampleBlogPost"
      :key="index"
    />





  </div>
</template>

<script>
import BlogPost from "../components/BlogPost";



export default {
  name: "Home",
  components: { BlogPost },
  data() {
    return {

      sampleBlogPost: [
        {
          title: "배송 시작",
          blogHTML: "안전하게 배달해드릴게요!!",
          blogCoverPhoto: "delivery",
        },

      ],
    };
  },
  computed: {

    user() {
      return this.$store.state.user;
    },
  },
};
</script>

<style lang="scss" scoped>
@font-face {
    font-family: 'GowunBatang-Regular';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2108@1.1/GowunBatang-Regular.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}
.blog-card-wrap {
  h3 {
    font-weight: 300;
    font-size: 28px;
    margin-bottom: 32px;
  }
}


</style>
