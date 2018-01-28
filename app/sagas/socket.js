import io from 'socket.io-client';
import { eventChannel, delay } from 'redux-saga';
import { takeEvery, take, put, call, race, fork } from 'redux-saga/effects';

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
  /*while (true) {
    continue; 
  }*/
};

// Saga
const listenServerSaga = function* () {
  try {
    
    console.log("saga");
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

  } catch (error) {
    console.log(error);
  }
};

export default listenServerSaga;
