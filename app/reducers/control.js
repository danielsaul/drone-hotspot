import { Actions } from 'react-native-router-flux';

const initialControl = {
  mode: "manual",
  manual: {
    move: {
      x: 0.0,
      y: 0.0
    },
    altitude: 0.0,
    yaw: 0.0,
  },
  flytopoint: {
    altitude: 1,
    location: null
  },
  autonomous: null,
};

export const SET_MODE = 'SET_MODE';
export const UPDATE_MANUAL = 'UPDATE_MANUAL';
export const UPDATE_FLYTOPOINT_ALT = 'UPDATE_FLYTOPOINT_ALT';
export const UPDATE_FLYTOPOINT_LOC = 'UPDATE_FLYTOPOINT_LOC';

const setmode = mode => ({ type: SET_MODE, mode: mode })
const updatemanual = manual => ({ type: UPDATE_MANUAL, manual })
const updateflytopointalt = altitude => ({ type: UPDATE_FLYTOPOINT_ALT, altitude })
const updateflytopointloc = location => ({ type: UPDATE_FLYTOPOINT_LOC, location })

export default (control = initialControl, action) => {
  switch (action.type) {
    case SET_MODE:
      return {...control, mode: action.mode};
    case UPDATE_MANUAL:
      return {...control, manual: action.manual};
    case UPDATE_FLYTOPOINT_ALT:
      return {...control, flytopoint: {...control.flytopoint, altitude: action.altitude}};
    case UPDATE_FLYTOPOINT_LOC:
      return {...control, flytopoint: {...control.flytopoint, location: action.location}};
    default:
      return control;
  }
};
