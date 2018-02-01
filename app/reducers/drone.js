import { Actions } from 'react-native-router-flux';

// Drone Status
// offline | waiting | flying to location | hovering | returning | landing | error

const initialDrone = {
  status: "offline",
  location: {latitude: 0.0, longitude: 0.0},
  altitude: 0.0,
  distance: 0.0,
  speed: 0.0,
  battery: 0,
  signal: 0
};

export const UPDATE_DRONE = 'UPDATE_DRONE';

const update = drone => ({ type: UPDATE_DRONE, drone })

export default (drone = initialDrone, action) => {
  switch (action.type) {
    case UPDATE_DRONE:
      return action.drone;
    default:
      return drone;
  }
};
