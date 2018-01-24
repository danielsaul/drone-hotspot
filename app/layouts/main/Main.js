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
import { Joystick, JoystickDemuxed, TouchEventDemuxer } from 'joystick-component-lib';

import MainHeader from '../../components/MainHeader'
import ConnectionStatus from '../../components/ConnectionStatus'
import SignalStatus from '../../components/SignalStatus'
import BatteryStatus from '../../components/BatteryStatus'
import AltitudeStatus from '../../components/AltitudeStatus'
import DistanceStatus from '../../components/DistanceStatus'
import SpeedStatus from '../../components/SpeedStatus'
import FlightButtons from '../../components/FlightButtons'

import styles from './styles';

const mapStateToProps = ({ location }) => ({ location });
const mapDispatchToProps = {};

const Demuxer = TouchEventDemuxer([JoystickDemuxed]);

const firstHandler = (xProp, yProp) => {
  console.log(xProp.dx);
}

const secondHandler = (xProp, yProp) => {
  console.log(`second joystick: ${xProp}, ${yProp}`);
}

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

  joystick(){
    return(
    <Demuxer style={{flex: 1}} childrenProps={[
            {
              neutralPointX: 100,
              neutralPointY: 100,
              length: 75,
              shape: 'circular',
              isSticky: true,
              onJoystickMove: secondHandler,
              draggableStyle: styles.draggableStyle,
              backgroundStyle: styles.backgroundStyle,
            } ]}/>)
  }

  render(){
    return (
      <Container>
        <MainHeader />

        <Content scrollEnabled={false}>

          <View style={{flex: 1}}>
            <MapView region={this.state.map_region} showsUserLocation={true} style={{ alignSelf: 'stretch', height: 250 }} />
          </View>

          <View style={styles.twocol}>
            <ConnectionStatus status={false} />
            <SignalStatus status={0} />
          </View>
          <View style={styles.twocol}>
            <AltitudeStatus status={0} />
            <BatteryStatus status={0} />
          </View>
          <View style={styles.twocol}>
            <DistanceStatus status={0} />
            <SpeedStatus status={0} />
          </View>

          <Segment>
          <Button first active style={styles.modeButton}>
            <Text style={styles.modeButtonTxt}>Manual</Text>
          </Button>
          <Button style={styles.modeButton}>
            <Text style={styles.modeButtonTxt}>Fly to Point</Text>
          </Button>
          <Button last style={styles.modeButton}>
            <Text style={styles.modeButtonTxt}>Autonomous</Text>
          </Button>
          </Segment>

          <View>
            <Joystick neutralPointX={175} neutralPointY={77} length={60} shape={'vertical'} isSticky={true} onDraggableMove={firstHandler} draggableStyle={styles.altitudeSliderInner} backgroundStyle={styles.altitudeSliderOuter} />
            <Text style={[styles.altitudeText, styles.labelText]}>Altitude</Text>
            <Joystick neutralPointX={280} neutralPointY={77} length={60} shape={'circular'} isSticky={true} onDraggableMove={firstHandler} draggableStyle={styles.directionSliderInner} backgroundStyle={styles.directionSliderOuter} />
            <Text style={[styles.moveText, styles.labelText]}>Move</Text>
            <Joystick neutralPointX={85} neutralPointY={77} length={50} shape={'horizontal'} isSticky={true} onDraggableMove={firstHandler} draggableStyle={styles.yawSliderInner} backgroundStyle={styles.yawSliderOuter} />
            <Text style={[styles.yawText, styles.labelText]}>Rotate</Text>
          </View>

        </Content>

        <Footer>
          <FlightButtons inFlight={true} onPress={{takeOff: null, land: null, return: null, abort: null}}/>
        </Footer>

      </Container>
    );
  }

}

export default connect(mapStateToProps, mapDispatchToProps)(Main);
