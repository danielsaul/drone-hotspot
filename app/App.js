import React from 'react';
import { StyleSheet, Text, View, Image } from 'react-native';

export default class App extends React.Component {
  render() {
    
    return (
      <View style={styles.container}>
        <Text style={styles.text}>Drone Hotspot</Text>
        <Text>Yay</Text>
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
