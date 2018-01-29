import { combineReducers } from 'redux'

const rootReducer = combineReducers({
  connection: require('./connection').default,
  drone: require('./drone').default,
  control: require('./control').default,
  location: require('./location').default,
})

export default rootReducer;
