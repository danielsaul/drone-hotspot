import { combineReducers } from 'redux'

const rootReducer = combineReducers({
  data: require('./data').default,
  location: require('./location').default,
})

export default rootReducer;
