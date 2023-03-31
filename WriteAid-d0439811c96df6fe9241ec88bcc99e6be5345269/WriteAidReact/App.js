//import * as React from 'react';
import React, {useEffect, useState} from 'react';
import MainContainer from './navigation/MainContainer';
import { NavigationContainer } from '@react-navigation/native'
import {createNativeStackNavigator} from '@react-navigation/native-stack';
import AccountCreation from './navigation/screens/AccountCreation';
import AsyncStorage from '@react-native-async-storage/async-storage';


function App() {
  AsyncStorage.clear();

  const [initialRouteName, setInitialRouteName] = useState('MainContainer');

  useEffect(() => {
    async function checkItem() {
      try {
        const value = await AsyncStorage.getItem('Name');
        if (value !== null) {
          setInitialRouteName('AccountCreation');
          console.log('found');
        } else {
          console.log(value);
        }
      } catch (error) {
        console.log(error.message);
      }
    }
    checkItem();
  }, []);
  
  console.log("App start");

  const Stack = createNativeStackNavigator();


    return (
      <NavigationContainer>
      <Stack.Navigator 
      
      initialRouteName={initialRouteName}
      screenOptions={{
            headerShown: false
          }}>
        <Stack.Screen name={'mainApplication'} component={MainContainer}/>
        <Stack.Screen name = {'AccountCheck'} component = {AccountCreation}/>
      </Stack.Navigator>
      </NavigationContainer>
    );
  // return(
  //   <MainContainer/>
  // );

        }
export default App;