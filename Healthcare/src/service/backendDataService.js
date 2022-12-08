import axios from "axios";

const USER_API_URL = "https://192.168.2.251:5000/api/v1"; // Add our VM IP address here!

class UserDataService {
  sendOTP(email) {
    console.log("sda");
    return axios.post(`${USER_API_URL}/email`, email);
  }

  verify(data) {
    return axios.post(`${USER_API_URL}/verifyOtp`, data);
  }
  retrieveAllUsers() {
    return axios.get(`${USER_API_URL}/users`);
  }

  verifyUserFile(id) {
    return axios.post(`${USER_API_URL}/users/verifyUserFile`, id);
  }

  approveUser(id) {
    return axios.post(`${USER_API_URL}/users/approveUser`, id);
  }

  denyUser(id) {
    return axios.post(`${USER_API_URL}/users/denyUser`, id);
  }

  retrieveUser(id) {
    return axios.post(`${USER_API_URL}/users/login`, id);
  }

  fetchUser(id) {
    return axios.post(`${USER_API_URL}/users/fetch`, id);
  }

  deleteUser(id) {
    return axios.delete(`${USER_API_URL}/users/${id}`);
  }

  updateUser(id) {
    return axios.put(`${USER_API_URL}/users/update`, id);
  }

  registerUser(id) {
    return axios.post(`${USER_API_URL}/users/register`, id);
  }

  createUser(user) {
    return axios.post(`${USER_API_URL}/users`, user);
  }

  retrieveUnverifiedUsers() {
    return axios.get(`${USER_API_URL}/unverifiedUsers`);
  }

  retrieveVerifiedUsers() {
    return axios.get(`${USER_API_URL}/verifiedUsers`);
  }

  verifyUser(data) {
    return axios.post(`${USER_API_URL}/verifyOtp`, data);
  }
}

export default new UserDataService();
