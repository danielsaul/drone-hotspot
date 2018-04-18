import React from 'react';
import { Text } from 'native-base';
import { View, Picker } from 'react-native';
const Item = Picker.Item;

import styles from './styles';

options = (x,y) => {
  var options = [];
  for (var i = x; i <= y; i++) {
    options.push(<Item label={i+" m"} key={i} value={i} />);
  }
  return options;
};

export default (props) => (

  <View style={{justifyContent: 'center', flexDirection: 'row'}}>

    <View style={styles.halfview}>
      <Text style={[styles.centered, styles.padded]}>Select radius:</Text>
      <Picker
        onValueChange={props.radiusPickerChange}
        selectedValue={props.radiusValue}
        style={{height: 100, width: '100%',}}
        itemStyle={{fontSize: 15, height: 90,}}
      >
        {options(props.min, props.max)}
      </Picker>
    </View>

    <View style={styles.halfview}>
      <Text style={[styles.centered, styles.padded]}>Select altitude:</Text>
      <Picker
        onValueChange={props.altitudePickerChange}
        selectedValue={props.altitudeValue}
        style={{height: 100, width: '100%',}}
        itemStyle={{fontSize: 15, height: 90,}}
      >
        {options(props.min, props.max)}
      </Picker>
    </View>

  </View>

)
