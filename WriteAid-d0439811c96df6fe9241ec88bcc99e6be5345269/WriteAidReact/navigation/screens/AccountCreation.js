import * as React from 'react';
import { useState } from 'react';
import {View, Text, TextInput, StyleSheet, TouchableOpacity} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { SafeAreaView } from 'react-native-safe-area-context';



export default function AccountCreation({navigation}) {

    
    //let hasAccount = false;
    
    
    

    const createAccount = () => {
        console.log("accountCreated: " + nameInput);
        setData(nameInput).then(navigation.navigate('mainApplication'));
        //const value = await AsyncStorage.getItem('Name');
        //console.log(value);
        
    }

    const setData = async (value) => {
        if (value) {
          AsyncStorage.setItem('Name', value);
        } else {
          alert('Please Enter a Name First');
        }
      };
    

    const [nameInput, setTextInputValue] = useState('');
    const [getValue, setGetValue] = useState('');
    

    return(
        <View  style={{flex: 1, alignItems: 'center', justifyContent: 'center', backgroundColor :'beige'}}>
        <View style={{flex: 1, alignItems: 'center', justifyContent: 'center', paddingBottom: 20}}>
        <Text style={{fontSize: 60, paddingBottom: 25, fontWeight: 'bold', paddingBottom: 10}}>
          Welcome!
        </Text>
        <Text style={{fontSize: 20}}>
          Please Enter your Name:
        </Text>
        <TextInput
          placeholder="Name"
           value={nameInput}
           onChangeText={(data) => setTextInputValue(data)}
           maxLength = {20}
        //   underlineColorAndroid="transparent"
          style={styles.input}
        />
        <TouchableOpacity 
        style={{ backgroundColor: '#5377f5', padding: 10, borderRadius: 15, width:'50%',  alignItems:'center', justifyContent: 'center' }}
        onPress={() => createAccount()}>
        <Text> Create Account </Text>
      </TouchableOpacity>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    input: {
      align :'center',
      height: 40,
      margin: 12,
      minWidth: 100,
      borderWidth: 1,
      padding: 10,
      borderRadius:10,
    },
  });