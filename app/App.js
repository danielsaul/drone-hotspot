import React from 'react';
import { Alert, StyleSheet, Text, View, Image, Button } from 'react-native';
import io from 'socket.io-client';


export default class App extends React.Component {
  
  constructor(props) {
    super(props);
    this.state = {
      test: null,
    };

    this.onReceivedTest = this.onReceivedTest.bind(this);
    this.onSendTest = this.onSendTest.bind(this);

    this.socket = io.connect(`http://localhost:8080` , { transports: ['websocket'] });
    this.socket.on('test', this.onReceivedTest);
  }

  onReceivedTest(test) {
    this.setState((previousState) => {
      return {
        test: test,
      };
    });
  }

  onSendTest() {
    this.socket.emit('test_send', 'bla');
  }

  render() {
    
    return (
      <View style={styles.container}>
        <Text style={styles.text}>Drone Hotspot</Text>
        <Text>{this.state.test}</Text>
        <Button
          onPress={this.onSendTest}
          title="Test Btn"
          />
      </View>
    );

  }

}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#004066',
    alignItems: 'center',
    justifyContent: 'flex-start',
    flexDirection: 'column',
  },
  text: {
        color: 'white',
        fontSize: 30,
        padding: 20,
  }
});
