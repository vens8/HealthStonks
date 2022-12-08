import { createStore } from 'vuex'

export default createStore({
    state: {
        
        currentUser: [],
        adminlog: "false",
    },
    mutations: {
        UPDATE_USER(state, payload) {
            state.currentUser = payload
        },
        UPDATE_ADMIN(state, payload) {
            state.adminlog = payload
        }
    },
    actions: {
        updateUser(context, payload) {
            
            context.commit('UPDATE_USER', payload)
        },
        updateAdmin(context,payload){
            context.commit('UPDATE_ADMIN', payload)
        }
    },
    getters: {
        getUser: function (state) {
            return state.currentUser
        },
        getAdmin: function (state) {
            return state.adminlog
        }
    }
})