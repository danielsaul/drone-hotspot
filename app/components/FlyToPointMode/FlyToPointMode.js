import React from 'react';
import { Text } from 'native-base';
import { View, Picker } from 'react-native';
const Item = Picker.Item;
import { Joystick } from 'joystick-component-lib';

import styles from './styles';

options = (x,y) => {
  var options = [];
  for (var i = x; i <= y; i++) {
    options.push(<Item label={i+" m"} key={i} value={i} />);
  }
  return options;
};

export default (props) => (

  <View style={{justifyContent: 'center'}}>

    <Text style={[styles.centered, {paddingTop: 5}]}>Choose a location to fly to on the map above.</Text>
    <Text style={[styles.centered, styles.labelText, {paddingBottom: 5}]}>
      {props.coords != null ? props.coords.latitude.toFixed(6) + ', ' + props.coords.longitude.toFixed(6) : 'No location selected' }
    </Text>

    <Text style={[styles.centered, styles.padded]}>Select altitude to fly to below:</Text>
    <Picker
      onValueChange={props.altitudePickerChange}
      selectedValue={props.altitudeValue}
      style={{height: 100,}}
      itemStyle={{fontSize: 15, height: 90,}}
    >
      {options(props.min, props.max)}
    </Picker>

  </View>

)
