import axios from 'axios'

const USER_API_URL = 'https://192.168.2.251:5000'

class UserDataService {

  uploadFile(files) {

    try {
      return axios.post(`${USER_API_URL}/uploadFile`, files);
    } catch (e) {
      console.log("error", e);
    }

  }
}

export default new UserDataService()