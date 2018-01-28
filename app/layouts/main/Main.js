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

import MainHeader from '../../components/MainHeader'
import ConnectionStatus from '../../components/ConnectionStatus'
import SignalStatus from '../../components/SignalStatus'
import BatteryStatus from '../../components/BatteryStatus'
import AltitudeStatus from '../../components/AltitudeStatus'
import DistanceStatus from '../../components/DistanceStatus'
import SpeedStatus from '../../components/SpeedStatus'
import FlightButtons from '../../components/FlightButtons'
import ManualMode from '../../components/ManualMode'

import styles from './styles';

const mapStateToProps = ({ location, connection, drone }) => ({ location, connection, drone });
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

          {this.state.segmentMode == 0 ? <ManualMode handler={this.joystickHandler} /> : null } 
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
