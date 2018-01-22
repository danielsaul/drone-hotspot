import React from 'react';
import {
  Text,
  Icon,
} from 'native-base';
import { View } from 'react-native';

import styles from './styles';

export default (props) => (

  <View style={[styles.distancestatus_view,]}>
    <Icon name='ios-map-outline' style={styles.distancestatus_icon} />
    <Text style={styles.distancestatus_txt}> Distance: {props.status}m
    </Text>
  </View>

)
