import io from 'socket.io-client';
import { eventChannel, delay } from 'redux-saga';
import { takeEvery, take, put, call, race, fork, actionChannel } from 'redux-saga/effects';

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
    const payload = yield take(channel);
    yield put({type: UPDATE_DRONE, payload});
  }
};

// send
const send = function* (socket) {
  const chan = yield actionChannel('*');
  while (true) {
    action = yield take(chan);
    switch (action.type){
      case 'BTN_TAKEOFF':
        console.log('takeoff');
        break;
      case 'BTN_LAND':
        console.log('land');
        break;
      case 'BTN_RETURN':
        console.log('return');
        break;
      case 'UPDATE_LOCATION':
        console.log('location');
        break;
      case 'SET_MODE':
        console.log('mode');
        break;
      case 'UPDATE_MANUAL':
        console.log('manual');
        break;
      case 'UPDATE_FLYTOPOINT':
        console.log('flytopoint');
        break;
    };
  }
};

const sendAbort = function* (socket, action) {
  console.log('abort');
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

    yield put({type: DRONE_CONNECTED});

    // Listen and Send 
    yield fork(listen, socket);
    yield fork(send, socket);
    yield takeEvery('BTN_ABORT', sendAbort, socket);

  } catch (error) {
    console.log(error);
  }
};

export default listenServerSaga;
