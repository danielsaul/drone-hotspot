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
import { View, Picker, Image, AlertIOS } from 'react-native';
import { connect } from 'react-redux';
import { Actions } from 'react-native-router-flux';
import { MapView } from 'expo';

import MainHeader from '../../components/MainHeader'
import ConnectionStatus from '../../components/ConnectionStatus'
import SignalStatus from '../../components/SignalStatus'
import BatteryStatus from '../../components/BatteryStatus'
import AltitudeStatus from '../../components/AltitudeStatus'
import DistanceStatus from '../../components/DistanceStatus'
import SpeedStatus from '../../components/SpeedStatus'
import FlightButtons from '../../components/FlightButtons'
import ManualMode from '../../components/ManualMode'
import FlyToPointMode from '../../components/FlyToPointMode'

import { setmode, updatemanual, updateflytopoint } from '../../reducers/control'
import { updateip } from '../../reducers/droneip'

import styles from './styles';

const mapStateToProps = s => ({ connection: s.connection, droneip: s.droneip, drone: s.drone, control: { mode: s.control.mode, flytopoint: s.control.flytopoint } });
const mapDispatchToProps = dispatch => ({
  modeChange: mode => {
    dispatch(setmode(mode))
  },
  manualChange: manual => {
    dispatch(updatemanual(manual))
  },
  flytopointChange: flytopoint => {
    dispatch(updateflytopoint(flytopoint))
  },
  buttonPress: type => () => {
    dispatch({type})
  },
  ipChange: ip => {
    dispatch(updateip(ip))
  }
});

class Main extends Component{
  constructor(){
    super();
    this.state = {};
    this.prevJoystick = {x: 0.0, y: 0.0}

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

  getDroneIP = () => {
    AlertIOS.prompt(
      'Drone Connection',
      'Enter IP address and port of drone:',
      [
        {
          text: 'Cancel',
          style: 'cancel',
        },
        {
          text: 'OK',
          onPress: this.props.ipChange,
        },
      ],
      'plain-text',
      this.props.droneip,
      'url'
    );
  }

  joystickHandler = (str, len) => (e) => {
    let x = Math.round( (e.dx/len) * 1e2 ) / 1e2;
    let y = Math.round( (-e.dy/len) * 1e2 ) / 1e2;
    
    if (str == "release") {
      this.props.manualChange({move: {x: 0.0, y: 0.0}, altitude: 0.0, yaw: 0.0});
      return;
    }

    if (Math.abs(this.prevJoystick.x - x) >= 0.1 || Math.abs(this.prevJoystick.y - y) >= 0.1) {
      switch (str) {
        case "move":
          this.props.manualChange({move: {x, y}, altitude: 0.0, yaw: 0.0});
          break;
        case "altitude":
          let altitude = y;
          this.props.manualChange({move: {x: 0.0, y: 0.0}, altitude, yaw: 0.0});
          break;
        case "yaw":
          let yaw = x;
          this.props.manualChange({yaw});
          this.props.manualChange({move: {x: 0.0, y: 0.0}, altitude: 0.0, yaw});
          break;
      }
      
      this.prevJoystick = {x, y}
    }

  }

  segmentChange = (x) => (e) => {
    if (x != this.props.control.mode) {
      this.props.modeChange({mode: x});
    }
  }

  regionChange = (map_region) => {
    this.setState({ map_region });
  }

  mapPress = (e) => {
    let location = e.nativeEvent.coordinate;
    if (this.props.control.mode == "flytopoint") {
      this.props.flytopointChange({location});
    }
  }

  markerToFlyTo = () => (
    <MapView.Marker
      draggable
      coordinate={this.props.control.flytopoint.location}
      onDragEnd={this.mapPress}
      title='Location to fly to'
    />
  )

  lineToFlyTo = () => (
    <MapView.Polyline
		coordinates={[
      this.props.control.flytopoint.location,
			this.props.drone.location
		]}
		strokeColor="#777" 
		strokeWidth={2}
    lineDashPattern={[5,3]}
	  />
  )

  markerDrone = () => (
    <MapView.Marker
      coordinate={this.props.drone.location}
      title='Drone Location'
    >
      <Image
        source={require('./mapicon9.png')}
        style={{width: 70, height: 70}}
      />
    </MapView.Marker>
  )

  altitudePicker = (x) => {
    this.props.flytopointChange({altitude: x});
  }

  render(){
    return (
      <Container>
        <MainHeader btn={this.getDroneIP} />

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
              {this.props.control.mode == "flytopoint" && this.props.control.flytopoint.location != null ? this.markerToFlyTo() : null}
              {this.props.control.mode == "flytopoint" && this.props.control.flytopoint.location != null ? this.lineToFlyTo() : null}
              {this.markerDrone()}
            </MapView>
          </View>

          <View style={styles.twocol}>
            <ConnectionStatus status={this.props.connection} />
            <SignalStatus status={this.props.drone.signal} />
          </View>
          <View style={styles.twocol}>
            <AltitudeStatus status={this.props.drone.altitude} />
            <BatteryStatus status={this.props.drone.battery} />
          </View>
          <View style={styles.twocol}>
            <DistanceStatus status={this.props.drone.distance} />
            <SpeedStatus status={this.props.drone.speed} />
          </View>

          <Segment>
            <Button first active={this.props.control.mode == "manual"} style={styles.modeButton} onPress={this.segmentChange("manual")}>
              <Text style={styles.modeButtonTxt}>Manual</Text>
            </Button>
            <Button  active={this.props.control.mode == "flytopoint"} style={styles.modeButton} onPress={this.segmentChange("flytopoint")}>
              <Text style={styles.modeButtonTxt}>Fly to Point</Text>
            </Button>
            <Button last active={this.props.control.mode == "autonomous"} style={styles.modeButton} onPress={this.segmentChange("autonomous")}>
              <Text style={styles.modeButtonTxt}>Autonomous</Text>
            </Button>
          </Segment>

          {this.props.control.mode == "manual" ? <ManualMode handler={this.joystickHandler} /> : null } 
          {this.props.control.mode == "flytopoint" ?
              <FlyToPointMode
                min={1}
                max={100}
                coords={this.props.control.flytopoint.location}
                altitudeValue={this.props.control.flytopoint.altitude}
                altitudePickerChange={this.altitudePicker}
              />
          : null } 

        </Content>

        <Footer>
          <FlightButtons
            disabled={!this.props.connection}
            inFlight={this.props.drone.status == "flying"}
            onPress={{
              takeOff: this.props.buttonPress('BTN_TAKEOFF'),
              land: this.props.buttonPress('BTN_LAND'),
              return: this.props.buttonPress('BTN_RETURN'),
              abort: this.props.buttonPress('BTN_ABORT')
            }}
          />
        </Footer>

      </Container>
    );
  }

}

export default connect(mapStateToProps, mapDispatchToProps)(Main);
