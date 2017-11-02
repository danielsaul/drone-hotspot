import React from 'react';
import { StyleSheet, Text, View, Image } from 'react-native';
import io from 'socket.io-client';


export default class App extends React.Component {
  
constructor(props) {
    super(props);
    this.state = {
      test: null
    };

    this.onReceivedTest = this.onReceivedTest.bind(this);

    this.socket = io(`http://localhost:8080` , { transports: ['websocket'] });
    this.socket.on('test', this.onReceivedTest);
  }

  onReceivedTest(test) {
    this.setState((previousState) => {
      return {
        test: test,
      };
    });
  }

  render() {
    
    return (
      <View style={styles.container}>
        <Text style={styles.text}>Drone Hotspot</Text>
        <Text>{this.state.test}</Text>
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
