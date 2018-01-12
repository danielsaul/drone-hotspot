import watchLocationChannel from './location';
import { spawn, all } from 'redux-saga/effects';

const rootSaga = function * rootSaga() {
  yield all([
    spawn(watchLocationChannel),
  ]);
}

export default rootSaga;
