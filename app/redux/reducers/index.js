import { combineReducers } from 'redux'

const rootReducer = combineReducers({
  data: require('./data').default,
  //posts: require('./posts').default,
})

export default rootReducer;
