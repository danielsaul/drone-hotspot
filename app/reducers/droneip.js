import { Actions } from 'react-native-router-flux';
import { AsyncStorage } from 'react-native';

const initialDroneIP = "http://localhost:8080";

export const UPDATE_IP = 'UPDATE_IP';

export const updateip = ip => ({ type: UPDATE_IP, ip })

export default (droneip = initialDroneIP, action) => {
  switch (action.type) {
    case UPDATE_IP:
      return action.ip;
    default:
      return droneip;
  }
};
