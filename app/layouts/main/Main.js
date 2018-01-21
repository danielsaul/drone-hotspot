import React, { Component } from 'react';
import {
  Header,
  Footer,
  Container,
  Content,
  Icon,
  Text,
  Button,
  Segment
} from 'native-base';
import { View } from 'react-native';
import { connect } from 'react-redux';
import { Actions } from 'react-native-router-flux';
import { MapView } from 'expo';

import MainHeader from '../../components/MainHeader'
import ConnectionStatus from '../../components/ConnectionStatus'
import SignalStatus from '../../components/SignalStatus'
import FlightButtons from '../../components/FlightButtons'

import styles from './styles';

const mapStateToProps = ({ location }) => ({ location });
const mapDispatchToProps = {};

class Main extends Component{
  constructor(){
    super();
    this.state = {};

    navigator.geolocation.getCurrentPosition(
      (position) => {
        map_region = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          latitudeDelta: 0.001,
          longitudeDelta: 0.001,
        }
        this.setState({map_region})
      }
    )

  }

  render(){
    return (
      <Container>
        <MainHeader />
        <Content>
          <View style={{flex: 1}}>
            <MapView region={this.state.map_region} showsUserLocation={true} style={{ alignSelf: 'stretch', height: 250 }} />
          </View>

          <ConnectionStatus status={false} />
          <SignalStatus status={0} />

          <Segment>
          <Button first active>
            <Text>Fly to Point</Text>
          </Button>
          <Button last>
            <Text>Autonomous</Text>
          </Button>
          </Segment>

        </Content>
        <Footer>
          <FlightButtons inFlight={true} onPress={{takeOff: null, land: null, return: null, abort: null}}/>
        </Footer>
      </Container>
    );
  }

}

export default connect(mapStateToProps, mapDispatchToProps)(Main);
