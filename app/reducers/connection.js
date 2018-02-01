import { Actions } from 'react-native-router-flux';

const initialConnection = false;

export const DRONE_CONNECTED = 'DRONE_CONNECTED';
export const DRONE_DISCONNECTED = 'DRONE_DISCONNECTED';

const connected = () => ({ type: DRONE_CONNECTED })
const disconnected = () => ({ type: DRONE_DISCONNECTED })

export default (connection = initialConnection, action) => {
  switch (action.type) {
    case DRONE_CONNECTED:
      return true;
    case DRONE_DISCONNECTED:
      return false;
    default:
      return connection;
  }
};
