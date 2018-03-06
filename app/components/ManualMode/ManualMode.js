import React from 'react';
import { Text } from 'native-base';
import { View } from 'react-native';

import { Joystick } from 'joystick-component-lib';

import styles from './styles';

export default (props) => (
    <View>

      <Joystick
        neutralPointX={175}
        neutralPointY={77}
        length={60}
        shape={'vertical'}
        isSticky={true}
        onDraggableMove={props.handler("altitude", 60)}
        onDraggableRelease={props.handler("release", 60)}
        draggableStyle={styles.altitudeSliderInner}
        backgroundStyle={styles.altitudeSliderOuter}
      />
      <Text style={[styles.altitudeText, styles.labelText]}>Altitude</Text>

      <Joystick
        neutralPointX={280}
        neutralPointY={77}
        length={60}
        shape={'circular'}
        isSticky={true}
        onDraggableMove={props.handler("move", 60)}
        onDraggableRelease={props.handler("release", 60)}
        draggableStyle={styles.directionSliderInner}
        backgroundStyle={styles.directionSliderOuter}
      />
      <Text style={[styles.moveText, styles.labelText]}>Move</Text>

      <Joystick
        neutralPointX={85}
        neutralPointY={77}
        length={50}
        shape={'horizontal'}
        isSticky={true}
        onDraggableMove={props.handler("yaw", 50)}
        onDraggableRelease={props.handler("release", 60)}
        draggableStyle={styles.yawSliderInner}
        backgroundStyle={styles.yawSliderOuter}
      />
      <Text style={[styles.yawText, styles.labelText]}>Rotate</Text>

    </View>
 
)
