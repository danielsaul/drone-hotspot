import { eventChannel } from 'redux-saga';
import { takeEvery, put, call } from 'redux-saga/effects';

import { UPDATE_LOCATION } from '../reducers/location';

const WATCH_POSITION_OPTIONS = {
  enableHighAccuracy: true,
  timeout: 20000,
  maximumAge: 1000,
  distanceFilter: 10
}

export function locationChannel () {
  return eventChannel((emit) => {
    
    const onError = (error) => emit({ error: error.message })
    const onSuccess = (position) => emit({
      latitude: position.coords.latitude,
      longitude: position.coords.longitude,
      error: null
    })
    const watch = navigator.geolocation.watchPosition(onSuccess, onError, WATCH_POSITION_OPTIONS)
    return () => navigator.geolocation.clearWatch(watch)

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
