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
  autonomous: {
    altitude: 1,
    radius: 5,
  },
};

export const SET_MODE = 'SET_MODE';
export const UPDATE_MANUAL = 'UPDATE_MANUAL';
export const UPDATE_FLYTOPOINT = 'UPDATE_FLYTOPOINT';
export const UPDATE_AUTONOMOUS = 'UPDATE_AUTONOMOUS';

export const setmode = mode => ({ type: SET_MODE, mode })
export const updatemanual = manual => ({ type: UPDATE_MANUAL, manual })
export const updateflytopoint = flytopoint => ({ type: UPDATE_FLYTOPOINT, flytopoint })
export const updateautonomous = autonomous => ({ type: UPDATE_AUTONOMOUS, autonomous })

export default (control = initialControl, action) => {
  switch (action.type) {
    case SET_MODE:
      return {...control, ...action.mode};
    case UPDATE_MANUAL:
      return {...control, manual: {...control.manual, ...action.manual}};
    case UPDATE_FLYTOPOINT:
      return {...control, flytopoint: {...control.flytopoint, ...action.flytopoint}};
    case UPDATE_AUTONOMOUS:
      return {...control, autonomous: {...control.autonomous, ...action.autonomous}};
    default:
      return control;
  }
};


