import { watchLocationChannel } from './sagas/location';

export default function * rootSaga() {
  yield [
    spawn(watchLocationChannel),
  ];
}
