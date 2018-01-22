import React from 'react';
import {
  Text,
  Icon,
} from 'native-base';
import { View } from 'react-native';

import styles from './styles';

export default (props) => (

  <View style={[styles.altitudestatus_view,]}>
    <Icon name='ios-trending-up' style={styles.altitudestatus_icon} />
    <Text style={styles.altitudestatus_txt}> Altitude: {props.status}m
    </Text>
  </View>

)
