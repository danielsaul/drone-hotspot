import React, { Component } from 'react';
import { AppRegistry, View } from 'react-native';
import { Provider, connect } from 'react-redux';
import { Font, AppLoading } from 'expo';
import store from './store';
import Router from './routes';
import io from 'socket.io-client';


export default class App extends Component {
  
  constructor() {
    super();
    this.state = {
      isReady: false,
    };

    //this.onReceivedTest = this.onReceivedTest.bind(this);
    //this.onSendTest = this.onSendTest.bind(this);
    //this.socket = io.connect(`http://localhost:8080` , { transports: ['websocket'] });
    //this.socket.on('test', this.onReceivedTest);
  }

  async componentWillMount() {
    await Font.loadAsync({
      'Roboto': require('native-base/Fonts/Roboto.ttf'),
      'Roboto_medium': require('native-base/Fonts/Roboto_medium.ttf'),
      'Ionicons': require('native-base/Fonts/Ionicons.ttf'),
    });
    this.setState({isReady: true});
  }


  render() {
    if(!this.state.isReady){
      return <AppLoading />;
    }
    return (
      <Provider store={store}>
        <Router />
      </Provider>
    );
  }

}

