import React from 'react';
import {
  Text,
  Icon,
} from 'native-base';
import { View } from 'react-native';

import styles from './styles';

export default (props) => (

  <View style={[styles.speedstatus_view,]}>
    <Icon name='ios-speedometer-outline' style={styles.speedstatus_icon} />
    <Text style={styles.speedstatus_txt}> Speed: {props.status}
    </Text>
  </View>

)
