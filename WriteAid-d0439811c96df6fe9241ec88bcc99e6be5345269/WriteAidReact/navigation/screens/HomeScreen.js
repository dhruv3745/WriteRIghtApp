import { useState, useEffect } from 'react';
import * as React from 'react';
import {View, Text, SafeAreaView, TouchableOpacity, Modal, Dimensions, StyleSheet, Image} from 'react-native';
//import {WhatTypeStencil} from '../Components/WhatTypeStencil';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function HomeScreen({navigation}) {


  const [isModalVisible, setIsModalVisible] = useState(false);

  const ChangeModalVisible = (bool) => {
    setIsModalVisible(bool);
  }

  

const WhatTypeStencil = (props) => {

  closeModal = (bool) => {
    props.ChangeModalVisible(bool);
  }

    return(
        <TouchableOpacity
            disabled={true}
            style={styles.container}
        >
        <View style={styles.modal}>
            <View style={styles.textView}>
                <Text style={[styles.text, {fontSize:20}]}> Stencil Type </Text>
                <Text style={[styles.text, {fontWeight:'normal', paddingTop: 20}]}> How do you want to create a stencil?</Text>
            </View>

            <View style={styles.buttonsView}>
              <TouchableOpacity style={ styles.touchableOpacity}
              onPress={() => [closeModal(false), navigation.navigate('UploadImage')]}
              >
                <Text style={ [styles.text, {color: 'blue'}]}>
                  Upload Image
                </Text>
              </TouchableOpacity>
              <TouchableOpacity 
              style={ styles.touchableOpacity}
              onPress={() => [closeModal(false), navigation.navigate('TextToStencil')]}
              >
                <Text style={ [styles.text, {color: 'blue'}]}>
                  Enter Text/Speak
                </Text>
              </TouchableOpacity>
            </View>

        </View>
        

        </TouchableOpacity>
    )
}
// let welcomeMessage;

// const getName = async() => {
//   welcomeMessage = await AsyncStorage.getItem('Name');
//   //console.log(welcomeMessage);
//   //console.log(welcomeMessage);
//   //welcomeMessage;
//   return (welcomeMessage)
// };
// getName();

// // getName().then((value) => {
// //   welcomeMessage = value;
// //   //console.log(welcomeMessage + ' logged');
// // });
// // console.log(JSON.parse(welcomeMessage) + " logged");
// console.log(welcomeMessage + " logged");

const [welcomeMessage, setWelcomeMessage] = useState('');

  useEffect(() => {
    const getName = async () => {
      const message = await AsyncStorage.getItem('Name');
      setWelcomeMessage("Welcome " + message);
      console.log("in welcome, setting name");
    };

    getName();
  }, []);

  const stencilWithText = () => {
    console.log(" stencilWithSpeech");
    navigation.navigate('TextToStencil');
  };

  const stencilWithImage = () => {
    console.log(" stencilWithSpeech");
    navigation.navigate('TextToStencil');
  };


  return (
    <SafeAreaView style={{ margin: 10, flex:1, flexDirection: 'column'}}>
  <View style={{ paddingTop: 30, flex:1, flexDirection: 'column'}}>
    <View style={{ textAlign: 'right', padding: 12, margin: 1}}>
      <Text style={styles.welcome}>{welcomeMessage}</Text>
    </View>
    <View style={styles.buttonHolders}>
      <View style={{
        flex: 1,
        height: 150,
        marginHorizontal: 5,
      }}>
        <TouchableOpacity
          style={styles.touchableOpacity}
          onPress={() => stencilWithText()}>
          <Text style={styles.ButtonText}>New Stencil with Text/Speech</Text>
          <Text style={styles.ButtonPlus}>+</Text>
        </TouchableOpacity>
      </View>
      <View style={{
        flex: 1,
        height: 150,
        marginHorizontal: 5,
      }}>
        <TouchableOpacity
          style={styles.touchableOpacity}
          onPress={() => stencilWithImage()}>
          <Text style={styles.ButtonText}>New Stencil with Image</Text>
          <Text style={styles.ButtonPlus}>+</Text>
        </TouchableOpacity>
      </View>
    </View>
  </View>
</SafeAreaView>
    // <SafeAreaView
    //   style={{margin: 10}}>
    //   <View style = {{paddingTop: 30}}>
    //   <View style = {{textAlign: 'right'}}>
    //   <Text style = {styles.welcome}> {welcomeMessage}</Text>
    //   </View>
    //   <View StyleSheet = {styles.buttonHolders}>
    // <View style ={{
    // flex: 1,
    // height: 50,
    // marginHorizontal: 5,}}>
    //   <TouchableOpacity 
    //     style={{ backgroundColor: '#00A89D', padding: 10, borderRadius: 15, height:'60%' }}
    //     onPress={() => consoloe.log("stencil with speech")}>
    //     <Text style={{ color: '#fff', fontFamily:'Verdana', fontSize: 20 }}>New Stencil with Text/Speech</Text>
    //     <Text style={{ color: '#fff', fontFamily:'Verdana', fontSize: 40, fontWeight:'bold' }}>+</Text>
    //   </TouchableOpacity>
    // </View>
    // <View style ={{
    // flex: 1,
    // height: 50,
    // marginHorizontal: 5,}}>
    //   <TouchableOpacity
    //     style={{ backgroundColor: '#00A89D', padding: 10, borderRadius: 15, height:'60%'}}
    //     onPress={() => console.log("stencil with image")}>
    //     <Text style={{ color: '#fff', fontFamily:'Verdana', fontSize: 20 }}>New Stencil with Image</Text>
    //     <Text style={{ color: '#fff', fontFamily:'Verdana', fontSize: 40, fontWeight:'bold' }}>+</Text>
    //   </TouchableOpacity>
    //   </View>
    //   </View>
      /* <Modal 
        transparent={true}
        animationType='fade'
        visible={isModalVisible}
        nRequestClose={() => ChangeModalVisible(false)}
      >
        <WhatTypeStencil
          ChangeModalVisible={ChangeModalVisible}
        />

      </Modal> */
      
  );
}

const styles = StyleSheet.create({
  welcome: {
    fontSize: 60, paddingBottom: 25, fontWeight: 'bold', paddingBottom: 10
  
  },
  container: {
      flex: 1,
      alignItems: 'center',
      justifyContent: 'center',
  },
  modal: {
      height: 150,
      width: Dimensions.get('window').width - 80,
      paddingTop: 10,
      backgroundColor:'#A8A8A8',
      borderRadius: 10,
  },
  textView: {
      flex: 1,
      alignItems: 'center',
  },
  text: {
      margin:5,
      fontSize:16,
      fontWeight:'bold'
  },
  buttonsView: {
    width:'100%',
    flexDirection: 'row',
  },
  buttonHolders: {
    paddingTop: 15,
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'top',
    paddingHorizontal: 10,
  },
  touchableOpacity: {
    backgroundColor: '#00A89D',
            padding: 10,
            borderRadius: 15,
            flex: 1,
            justifyContent: 'center',
            alignItems: 'center',
  },
  ButtonText: { color: '#fff', fontFamily: 'Verdana', fontSize: 20, textAlign: 'center'},
  ButtonPlus: 
    { color: '#fff', fontFamily: 'Verdana', fontSize: 40, fontWeight: 'bold', textAlign: 'center' }
  ,
})

