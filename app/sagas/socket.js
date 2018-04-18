import io from 'socket.io-client';
import { AsyncStorage } from 'react-native';
import { eventChannel, delay } from 'redux-saga';
import { takeEvery, take, put, call, race, fork, select, actionChannel } from 'redux-saga/effects';

import { DRONE_CONNECTED, DRONE_DISCONNECTED } from '../reducers/connection';
import { UPDATE_DRONE } from '../reducers/drone';


export const getIP = state => state.droneip;

// Connection functions (connect, disconnect, reconnect)
let socket;
const connect = url => {
  socket = io(url, {transports: ['websocket']});
  return new Promise((resolve) => {
    socket.on('connect', () => {
      resolve(socket);
    });
  });
};

const disconnect = url => {
  socket = io(url, {transports: ['websocket']});
  return new Promise((resolve) => {
    socket.on('disconnect', () => {
      resolve(socket);
    });
  });
};

const reconnect = url => {
  socket = io(url, {transports: ['websocket']});
  return new Promise((resolve) => {
    socket.on('reconnect', () => {
      resolve(socket);
    });
  });
};

// Channel for subscribing to events
const socketChannel = socket => eventChannel((emit) => {
  
  const handler = (data) => {
    emit(data);
  };
  socket.on('updateDroneStatus', handler);

  return () => {
    socket.off('updateDroneStatus', handler);
  };
});

// monitor connection status
const listenDisconnectSaga = function* () {
  while (true) {
    const url = yield select(getIP);
    yield call(disconnect, url);
    yield put({type: DRONE_DISCONNECTED});
  }
};
const listenConnectSaga = function* () {
  while (true) {
    const url = yield select(getIP);
    yield call(reconnect, url);
    yield put({type: DRONE_CONNECTED});
  }
};

// listen
const listen = function* (socket) {
  const channel = yield call(socketChannel, socket);
  while (true) {
    const drone = yield take(channel);
    yield put({type: UPDATE_DRONE, drone});
  }
};

export const getState = state => ({...state.control, location: state.location});

// send
const send = function* (socket) {
  const chan = yield actionChannel('*');
  while (true) {
    action = yield take(chan);
    switch (action.type){
      case 'DRONE_CONNECTED':
        const state = yield select(getState)
        socket.emit('update_all', state);
        break;
      case 'BTN_TAKEOFF':
        socket.emit('action', 'takeoff');
        break;
      case 'BTN_LAND':
        socket.emit('action', 'land');
        break;
      case 'BTN_RETURN':
        socket.emit('action', 'return');
        break;
      case 'UPDATE_LOCATION':
        socket.emit('update_location', action.location);
        break;
      case 'SET_MODE':
        socket.emit('set_mode', action.mode);
        break;
      case 'UPDATE_MANUAL':
        socket.emit('update_manual', action.manual);
        break;
      case 'UPDATE_FLYTOPOINT':
        socket.emit('update_flytopoint', action.flytopoint);
        break;
      case 'UPDATE_AUTONOMOUS':
        socket.emit('update_autonomous', action.autonomous);
        break;
    };
  }
};

const sendAbort = function* (socket, action) {
  socket.emit('action', 'abort');
};

const monitorDroneIP = function* (action) {
  yield AsyncStorage.setItem('@AppLocalStorage:drone_ip', action.ip);
};

// Saga
const listenServerSaga = function* () {
  try {
    
    // Get IP address / URL from storage
    const ip = yield AsyncStorage.getItem('@AppLocalStorage:drone_ip');
    if (ip != null){
      yield put({type: 'UPDATE_IP', ip});
    }

    // Monitor changes to IP
    yield takeEvery('UPDATE_IP', monitorDroneIP);

    // Try to connect
    while (true) {
      const url = yield select(getIP);
      const {socket, timeout} = yield race({
        socket: call(connect, url),
        timeout: delay(2000),
      });
      if (timeout) {
        yield put({type: DRONE_DISCONNECTED});
      }else{
        break;
      }
    }
    
    // Monitor connection
    yield fork(listenDisconnectSaga);
    yield fork(listenConnectSaga);

    // Listen and Send 
    yield fork(listen, socket);
    yield fork(send, socket);
    yield takeEvery('BTN_ABORT', sendAbort, socket);

    yield put({type: DRONE_CONNECTED});

  } catch (error) {
    console.log(error);
  }
};

export default listenServerSaga;
