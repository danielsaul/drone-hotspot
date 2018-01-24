import React from 'react';
import {
  Text,
  Button,
  Icon,
  Header,
  Title,
  Left,
  Right,
  Body
} from 'native-base';
import styles from './styles';
import { Image } from 'react-native';
export default (props) => (
  <Header style={styles.header} iosBarStyle='dark-content'>
    <Body>
      <Title style={styles.title}>DRONE HOTSPOT</Title>
  {/*<Image
        source={require('./logo.png')} style={styles.logo}
      />*/}
    </Body>
  </Header>
)
