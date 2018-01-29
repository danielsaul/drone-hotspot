import io from 'socket.io-client';
import { eventChannel, delay } from 'redux-saga';
import { takeEvery, take, put, call, race, fork, select, actionChannel } from 'redux-saga/effects';

import { DRONE_CONNECTED, DRONE_DISCONNECTED } from '../reducers/connection';
import { UPDATE_DRONE } from '../reducers/drone';


const socketServerURL = 'http://localhost:8080';


// Connection functions (connect, disconnect, reconnect)
let socket;
const connect = () => {
  socket = io(socketServerURL, {transports: ['websocket']});
  return new Promise((resolve) => {
    socket.on('connect', () => {
      resolve(socket);
    });
  });
};

const disconnect = () => {
  socket = io(socketServerURL, {transports: ['websocket']});
  return new Promise((resolve) => {
    socket.on('disconnect', () => {
      resolve(socket);
    });
  });
};

const reconnect = () => {
  socket = io(socketServerURL, {transports: ['websocket']});
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
    yield call(disconnect);
    yield put({type: DRONE_DISCONNECTED});
  }
};
const listenConnectSaga = function* () {
  while (true) {
    yield call(reconnect);
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
    };
  }
};

const sendAbort = function* (socket, action) {
  socket.emit('action', 'abort');
};

// Saga
const listenServerSaga = function* () {
  try {
    // Try to connect
    const {timeout} = yield race({
      connected: call(connect),
      timeout: delay(2000),
    });
    if (timeout) {
      yield put({type: DRONE_DISCONNECTED});
    }

    const socket = yield call(connect);

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
