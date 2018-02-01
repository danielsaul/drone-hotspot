import watchLocationChannel from './location';
import listenServerSaga from './socket';
import { spawn, all } from 'redux-saga/effects';

const rootSaga = function * rootSaga() {
  yield all([
    spawn(watchLocationChannel),
    spawn(listenServerSaga),
  ]);
}

export default rootSaga;
