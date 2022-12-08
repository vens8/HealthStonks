import { IS_USER_AUTHENTICATE_GETTER } from "@/store/storeConstants";

export default {
    [IS_USER_AUTHENTICATE_GETTER](state) {
        return !!state.token;
    },
}