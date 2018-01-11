import React, { Component } from 'react';
import {
  Header,
  Container,
  Content,
  Icon,
  Text,
  Button,
} from 'native-base';
import { View } from 'react-native';
import { connect } from 'react-redux';
import { Actions } from 'react-native-router-flux';
import MainHeader from '../../components/MainHeader'
import { MapView } from 'expo';

import styles from './styles';

const mapStateToProps = ({ location }) => ({ location });
const mapDispatchToProps = {};

class Main extends Component{
 

  render(){
    return (
      <Container>
        <MainHeader />
        <Content>
          <View style={{flex: 1}}>
            <MapView showsUserLocation={true} style={{ alignSelf: 'stretch', height: 300 }} />
          </View>
          <View style={{flex: 1}}>
            <Text>{this.props.location.latitude}</Text>
          </View>
        </Content>
      </Container>
    );
  }

}

export default connect(mapStateToProps, mapDispatchToProps)(Main);
