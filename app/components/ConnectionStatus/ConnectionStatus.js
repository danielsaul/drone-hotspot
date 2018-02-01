import React from 'react';
import {
  Text,
  Icon,
} from 'native-base';
import { View } from 'react-native';

import styles from './styles';

export default (props) => (

  <View style={[styles.connectionstatus_view, props.status && styles.background_green]}>
    <Icon name='ios-plane' style={styles.connectionstatus_icon} />
    <Text style={styles.connectionstatus_txt}>
      {props.status ? ' Drone Connected' : ' Drone Disconnected'}
    </Text>
  </View>

)
