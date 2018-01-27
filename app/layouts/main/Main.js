import React, { Component } from 'react';
import {
  Header,
  Footer,
  Container,
  Content,
  Icon,
  Text,
  Button,
  Segment,
  Form,
} from 'native-base';
const Item = Picker.Item;
import { View, Picker, Image } from 'react-native';
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

class Main extends Component{
  constructor(){
    super();
    this.state = {
      segmentMode: 0,
    };

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

  joysticks = () => {
    return (
    <View>
      <Joystick neutralPointX={175} neutralPointY={77} length={60} shape={'vertical'} isSticky={true} onDraggableMove={this.joystickHandler("altitude")} draggableStyle={styles.altitudeSliderInner} backgroundStyle={styles.altitudeSliderOuter} />
      <Text style={[styles.altitudeText, styles.labelText]}>Altitude</Text>
      <Joystick neutralPointX={280} neutralPointY={77} length={60} shape={'circular'} isSticky={true} onDraggableMove={this.joystickHandler("move")} draggableStyle={styles.directionSliderInner} backgroundStyle={styles.directionSliderOuter} />
      <Text style={[styles.moveText, styles.labelText]}>Move</Text>
      <Joystick neutralPointX={85} neutralPointY={77} length={50} shape={'horizontal'} isSticky={true} onDraggableMove={this.joystickHandler("yaw")} draggableStyle={styles.yawSliderInner} backgroundStyle={styles.yawSliderOuter} />
      <Text style={[styles.yawText, styles.labelText]}>Rotate</Text>
    </View>
    )
  }

  joystickHandler = (x) => (e) => {
  }

  flyToPoint = () => {
    var options = [];
    for (var i = 1; i < 20; i++) {
      options.push(<Item label={i+" m"} key={i} value={i} />);
    } 
    return (
      <View style={{justifyContent: 'center'}}>
        <Text style={[styles.centered2, {paddingTop: 5}]}>Choose a location to fly to on the map above.</Text>
        <Text style={[styles.centered2, styles.labelText, {paddingBottom: 5}]}>
          {'flyToCoords' in this.state ? this.state.flyToCoords.latitude.toFixed(6) + ', ' + this.state.flyToCoords.longitude.toFixed(6) : 'No location selected' }
        </Text>
        <Text style={[styles.centered]}>Select altitude to fly to below:</Text>
        <Picker
          onValueChange={this.altitudePicker}
          selectedValue={this.state.flyToAltitude}
          style={{height: 100,}}
          itemStyle={{fontSize: 15, height: 90,}}
        >
          {options}
        </Picker>
      </View>
    )
  }

  segmentChange = (x) => (e) => {
    if (x != this.state.segmentMode) {
      this.setState({segmentMode: x});
    }
  }

  regionChange = (map_region) => {
    this.setState({ map_region });
  }

  mapPress = (e) => {
    flyToCoords = e.nativeEvent.coordinate;
    if (this.state.segmentMode == 1) {
      this.setState({flyToCoords});
    }
  }

  markerToFlyTo = () => (
    <MapView.Marker
      draggable
      coordinate={this.state.flyToCoords}
      onDragEnd={this.mapPress}
      title='Location to fly to'
    />
  )

  lineFlyTo = () => (
    <MapView.Polyline
		coordinates={[
			this.state.flyToCoords,
			{ latitude: 51.35, longitude: -0.228 }
		]}
		strokeColor="#777" // fallback for when `strokeColors` is not supported by the map-provider
		strokeWidth={2}
    lineDashPattern={[5,3]}
	  />
  )

  markerDrone = () => (
    <MapView.Marker
      coordinate={{latitude: 51.35, longitude: -0.228}}
      title='Drone Location'
    >
      <Image
        source={require('./mapicon9.png')}
        style={{width: 70, height: 70}}
      />
    </MapView.Marker>
  )

  altitudePicker = (flyToAltitude) => {
    this.setState({flyToAltitude});
  }

  render(){
    return (
      <Container>
        <MainHeader />

        <Content scrollEnabled={false}>

          <View style={{flex: 1}}>
            <MapView
              region={this.state.map_region}
              onRegionChange={this.regionChange}
              onPress={this.mapPress}
              showsUserLocation={true}
              showsMyLocationButton={true}
              style={{ alignSelf: 'stretch', height: 250 }}
            >
              {this.state.segmentMode == 1 && 'flyToCoords' in this.state ? this.markerToFlyTo() : null}
              {this.state.segmentMode == 1 && 'flyToCoords' in this.state ? this.lineFlyTo() : null}
              {this.markerDrone()}
            </MapView>
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
            <Button first active={this.state.segmentMode == 0} style={styles.modeButton} onPress={this.segmentChange(0)}>
              <Text style={styles.modeButtonTxt}>Manual</Text>
            </Button>
            <Button  active={this.state.segmentMode == 1} style={styles.modeButton} onPress={this.segmentChange(1)}>
              <Text style={styles.modeButtonTxt}>Fly to Point</Text>
            </Button>
            <Button last active={this.state.segmentMode == 2} style={styles.modeButton} onPress={this.segmentChange(2)}>
              <Text style={styles.modeButtonTxt}>Autonomous</Text>
            </Button>
          </Segment>

          {this.state.segmentMode == 0 ? this.joysticks() : null } 
          {this.state.segmentMode == 1 ? this.flyToPoint() : null } 

        </Content>

        <Footer>
          <FlightButtons inFlight={true} onPress={{takeOff: null, land: null, return: null, abort: null}}/>
        </Footer>

      </Container>
    );
  }

}

export default connect(mapStateToProps, mapDispatchToProps)(Main);
