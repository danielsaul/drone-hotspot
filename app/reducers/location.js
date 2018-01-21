import { Actions } from 'react-native-router-flux';

const initialLocation = { latitude: 0.0, longitude: 0.0 }

export const UPDATE_LOCATION = 'UPDATE_LOCATION';

const update = location => ({ type: UPDATE_LOCATION, location })

export default (location = initialLocation, action) => {
  switch (action.type) {
    case UPDATE_LOCATION:
      return action.location;
    default:
      return location;
  }
  return data;
};
