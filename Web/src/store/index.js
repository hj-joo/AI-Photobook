import Vue from 'vue';
import Vuex from 'vuex';
import firebase from "firebase/app";
import "firebase/auth";
import db from "../firebase/firebaseInit";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    sampleBlogCards: [
      {
        blogTitle: "Photo Book",
        blogCoverPhoto: "stock-1",
        blogDate: "포토북 만들기",
      },
      {
        blogTitle: "Calender",
        blogCoverPhoto: "stock-2",
        blogDate: "달력",
      },
      {
        blogTitle: "Fan Book",
        blogCoverPhoto: "stock-3",
        blogDate: "팬북",
      },
      {
        blogTitle: "Frame",
        blogCoverPhoto: "stock-4",
        blogDate: "액자",
      },
    ],
    photoFileURL: null,
    photoPreview: null,
    editPost: null,
    user: null,
    profileEmail: null,
    profileName: null,
    profileUsername: null,
    profileId: null,
    profileShipping: null,
    profileInitials: null,
  },
  mutations: {
    toggleEditPost(state, payload){
      state.editPost = payload;
    },
    updataUser(state, payload){
      state.user = payload;
    },
    setProfileInfo(state, doc){
      state.profileId = doc.id;
      state.profileEmail = doc.data().email;
      state.profileName = doc.data().Name;
      state.profileUsername = doc.data().username;
      state.profileShipping = doc.data().shipping;
      
    },
    setProfileInitials(state) {
      state.profileInitials = 
      state.profileFirstName.match(/(\b\S)?/g).join("") +
      state.profileLastName.match(/(\b\S)?/g).join("");

    },
    changeName(state, payload){
      state.profileName = payload;
    },
    changeUsername(state, payload){
      state.profileUsername = payload;
    },
    changeShipping(state, payload){
      state.profileShipping = payload;
    },
    
  },
  actions: {
    async getCurrentUser({commit}) {
      const dataBase = await db.collection("users").doc(firebase.auth().currentUser.uid);
      const dbResults = await dataBase.get();
      commit("setProfileInfo", dbResults);
      commit("setProfileInitials");
      console.log(dbResults);
    },
    async updateUserSetting({commit, state}) {
      const dataBase = await db.collection('users').doc(state.profileId);
      await dataBase.update({
        Name: state.profileName,
        username: state.profileUsername,
        shipping: state.profileShipping,
      });
      commit("setProfileInitials");
    },
    async updateUserSettings({commit, state}) {
      const dataBase = await db.collection('users').doc(state.profileId);
      await dataBase.update({
        Name: state.profileName,
        username: state.profileUsername,
        shipping: state.profileShipping,
      });
      commit("setProfileInitials");
    }
  },
  modules: {
  }
});
