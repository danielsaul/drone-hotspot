import React from 'react';
import {
  Header,
  Container,
  Content,
  Icon,
  Text,
  Button,
} from 'native-base';
import { View } from 'react-native';
import { Actions } from 'react-native-router-flux';
import MainHeader from '../../components/MainHeader'

import styles from './styles';

export default() => (
  <Container>
    <MainHeader />
  </Container>
)
