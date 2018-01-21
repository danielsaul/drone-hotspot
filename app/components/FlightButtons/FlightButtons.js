import React from 'react';
import {
  Footer,
  Button,
  Text,
  Icon,
} from 'native-base';
import { View } from 'react-native';

import styles from './styles';

export default (props) => (

  <View style={styles.flightbuttons_view}>

    <Button full primary style={styles.takeoff}>
      <Icon name='md-arrow-up' style={styles.flightbuttons_icon} />
      <Text style={styles.flightbuttons_txt}>
        Take Off
      </Text>
    </Button>


    <Button full primary style={styles.land}>
      <Icon name='md-arrow-down' style={styles.flightbuttons_icon} />
      <Text style={styles.flightbuttons_txt}>
        Land
      </Text>
    </Button>

    <Button full warning style={styles.return}>
      <Icon name='md-undo' style={styles.flightbuttons_icon} />
      <Text style={styles.flightbuttons_txt}>
        Return
      </Text>
    </Button>

    <Button full danger style={styles.abort}>
      <Icon name='md-close-circle' style={styles.flightbuttons_icon} />
    </Button>



  </View>

)
