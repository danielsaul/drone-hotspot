import { eventChannel } from 'redux-saga';
import { takeEvery, put, call } from 'redux-saga/effects';

import { UPDATE_LOCATION } from '../reducers/location';

const GET_POSITION_OPTIONS = {
  enableHighAccuracy: true,
  timeout: 1000,
  maximumAge: 100,
}

export function locationChannel () {
  return eventChannel((emit) => {

    const onError = (error) => emit({ error: error.message })
    const onSuccess = (position) => emit({
      latitude: position.coords.latitude,
      longitude: position.coords.longitude,
      error: null
    })
    let timer = setInterval(() => {navigator.geolocation.getCurrentPosition(onSuccess, onError, GET_POSITION_OPTIONS)}, 1000)
    return () => {}

  })
}

function * locationUpdate (location) {

  yield put({ type: UPDATE_LOCATION, location })

}

const watchLocationChannel = function * watchLocationChannel () {

  const channel = yield call(locationChannel)
  yield takeEvery(channel, locationUpdate)

}

export default watchLocationChannel;
