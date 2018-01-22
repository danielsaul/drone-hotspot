import React from 'react';
import {
  Text,
  Icon,
} from 'native-base';
import { View } from 'react-native';

import styles from './styles';

export default (props) => (

  <View style={[styles.batterystatus_view,]}>
    <Icon name='ios-battery-dead' style={styles.batterystatus_icon} />
    <Text style={styles.batterystatus_txt}> Battery: {props.status}%
    </Text>
  </View>

)
