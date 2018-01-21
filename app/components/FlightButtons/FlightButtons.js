import React from 'react';
import {
  Footer,
  Button,
  Text,
  Icon,
} from 'native-base';
import { View } from 'react-native';

import styles from './styles';

const TakeOffBtn = (props) => (
  
  <Button disabled={props.disabled} full iconLeft
    style={[styles.takeoff, props.disabled && styles.disabled]} onPress={props.onPress}>
    <Icon name='md-arrow-up' style={styles.flightbuttons_icon} />
    <Text style={styles.flightbuttons_txt}>
      Take Off
    </Text>
  </Button>

)

const InFlightBtns = (props) => (
  
  <View style={styles.flightbuttons_view}>
  <Button disabled={props.disabled} full iconLeft
    style={[styles.land, props.disabled && styles.disabled]} onPress={props.onPress.land}>
    <Icon name='md-arrow-down' style={styles.flightbuttons_icon} />
    <Text style={styles.flightbuttons_txt}>
      Land
    </Text>
  </Button>

  <Button disabled={props.disabled} full iconLeft
    style={[styles.return, props.disabled && styles.disabled]} onPress={props.onPress.return}>
    <Icon name='md-undo' style={styles.flightbuttons_icon} />
    <Text style={styles.flightbuttons_txt}>
      Return
    </Text>
  </Button>

  <Button disabled={props.disabled} full danger
    style={[styles.abort, props.disabled && styles.disabled]} onPress={props.onPress.abort}>
    <Icon name='md-close-circle' style={styles.flightbuttons_icon} />
  </Button>
  </View>

)

export default (props) => (

  <View style={styles.flightbuttons_view}>

    { props.inFlight ? <InFlightBtns disabled={props.disabled} onPress={props.onPress} /> : <TakeOffBtn disabled={props.disabled} onPress={props.onPress.takeOff} /> }

  </View>

)
