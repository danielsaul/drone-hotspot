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
export const UPDATE_FLYTOPOINT = 'UPDATE_FLYTOPOINT';

const setmode = mode => ({ type: SET_MODE, mode: mode })
const updatemanual = manual => ({ type: UPDATE_MANUAL, manual })
const updateflytopoint = altitude => ({ type: UPDATE_FLYTOPOINT, flytopoint })

export default (control = initialControl, action) => {
  switch (action.type) {
    case SET_MODE:
      return {...control, mode: action.mode};
    case UPDATE_MANUAL:
      return {...control, manual: {...control.manual, ...action.manual}};
    case UPDATE_FLYTOPOINT:
      return {...control, flytopoint: {...control.flytopoint, ...action.flytopoint}};
    default:
      return control;
  }
};

export const modeChange = mode => dispatch => {
  dispatch(setmode(mode));
};

export const manualChange = change => dispatch => {
  dispatch(updatemanual(change));
};

export const flytopointChange = change => dispatch => {
  dispatch(updateflytopoint(change));
};
