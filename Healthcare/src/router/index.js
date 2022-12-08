import { createWebHistory, createRouter } from "vue-router";
import HomePage from "../components/HomePage.vue";
import LoginPage from "../components/LoginPage.vue";
import RegisterPage from "../components/RegisterPage.vue";
import findingDoc from "../components/findingDoc.vue";
import ProfilePatient from "../components/ProfilePatient.vue";
import ProfileDoctor from "../components/ProfileDoctor.vue";
import ProfileHosp from "../components/ProfileHosp.vue";
import ProfilePharmacy from "../components/ProfilePharmacy.vue";
import ProfileInsurance from "../components/ProfileInsurance.vue";
import paymentPage from "../components/paymentPage.vue";
import about from "../components/about.vue";
import findingHosp from "../components/findingHosp.vue";
import findingPharmacy from "../components/findingPharmacy.vue";
import findingInsurance from "../components/findingInsurance.vue";
import displayCatalog from "../components/displayCatalog.vue";
import displayFiles from "../components/displayFiles.vue";
import RegProfile from "../components/RegProfile.vue";
import adminApproval from "../components/adminApproval.vue";
import adminHomepage from "../components/adminHomepage.vue";
import adminAllusers from "../components/adminAllusers.vue";
import shareFiles from "../components/shareFiles.vue";
import store from "../store/index.js";
// Note to front end developers: When adding a new route here, make sure you also add the corresponding meta
// data for the page (make auth true if it must be accessilble only after being authenticated - logged in, else
// false)

const routes = [
  {
    path: "/Home",
    name: "HomePage",
    component: HomePage,
  },
  {
    path: "/shareFiles",
    name: "shareFiles",
    component: shareFiles,
  },
  {
    path: "/adminAllusers",
    name: "adminAllusers",
    component: adminAllusers,
    // meta: { auth: true },
    beforeEnter: (to, from, next) => {
      if(store.getters.getAdmin == "false") {
          next(false);
      } else {
          next();
      }
  }
  },
  {
    path: "/adminHomepage",
    name: "adminHomepage",
    component: adminHomepage,
    // meta: { auth: true },
    beforeEnter: (to, from, next) => {
      if(store.getters.getAdmin == "false") {
          next(false);
      } else {
          next();
      }
  }
  },
  {
    path: "/adminApproval",
    name: "adminApproval",
    component: adminApproval,
    // meta: { auth: true },
    beforeEnter: (to, from, next) => {
      if(store.getters.getAdmin == "false") {
          next(false);
      } else {
          next();
      }
  }
  },
  {
    path: "/displayCatalog",
    name: "displayCatalog",
    component: displayCatalog,
    meta: { auth: true },
  },
  {
    path: "/Regprofile",
    name: "RegProfile",
    component: RegProfile,
    meta: { auth: false },
  },
  {
    path: "/displayFiles",
    name: "displayFiles",
    component: displayFiles,
    meta: { auth: true },
  },
  {
    path: "/LoginPage",
    name: "LoginPage",
    component: LoginPage,
    meta: { auth: false },
  },

  {
    path: "/findingDoc",
    name: "findingDoc",
    component: findingDoc,
    meta: { auth: true },
  },
  {
    path: "/findingHosp",
    name: "findingHosp",
    component: findingHosp,
    meta: { auth: true },
  },
  {
    path: "/findingInsurance",
    name: "findingInsurance",
    component: findingInsurance,
    meta: { auth: true },
  },
  {
    path: "/findingPharmacy",
    name: "findingPharmacy",
    component: findingPharmacy,
    meta: { auth: true },
  },
  {
    path: "/ProfilePatient",
    name: "ProfilePatient",
    component: ProfilePatient,
    meta: { auth: true },
  },
  {
    path: "/ProfileDoctor",
    name: "ProfileDoctor",
    component: ProfileDoctor,
    meta: { auth: true },
  },
  {
    path: "/ProfileHosp",
    name: "ProfileHosp",
    component: ProfileHosp,
    meta: { auth: true },
  },
  {
    path: "/ProfilePharmacy",
    name: "ProfilePharmacy",
    component: ProfilePharmacy,
    meta: { auth: true },
  },
  {
    path: "/ProfileInsurance",
    name: "ProfileInsurance",
    component: ProfileInsurance,
    meta: { auth: true },
  },
  {
    path: "/",
    name: "RegisterPage",
    component: RegisterPage,
    meta: { auth: false },
  },
  {
    path: "/paymentPage",
    name: "paymentPage",
    component: paymentPage,
    meta: { auth: true },
  },
  {
    path: "/about",
    name: "about",
    component: about,
    meta: { auth: true },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// router.beforeEach(() => {
//   console.log(store.state.auth);
// });

export default router;
