import React from 'react';
import {
  Text,
  Icon,
} from 'native-base';
import { View } from 'react-native';

import styles from './styles';

export default (props) => (

  <View style={[styles.signalstatus_view,]}>
    <Icon name='ios-radio-outline' style={styles.signalstatus_icon} />
    <Text style={styles.signalstatus_txt}> 4G Signal: {props.status}
    </Text>
  </View>

)
