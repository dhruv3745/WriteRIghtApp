import * as React from 'react';
import {View, Text, TextInput, StyleSheet, SafeAreaView, TouchableOpacity, TouchableWithoutFeedback, Keyboard} from 'react-native';

export default function TextToStencil({navigation}) {



    
    const [value, onChangeText] = React.useState('');

    const buttonPressed = () => {
        //Add React Code to the button so that the value is sent to the 
        console.log(value);
        fetch("http://127.0.0.1:5000/process_frame", {
      method: 'POST',
      body: JSON.stringify({value}),
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(response => response.text()).then(data => {console.log(data)});

        navigation.navigate('Camera');

    }

    return(
        <TouchableWithoutFeedback onPress={Keyboard.dismiss} 
                          accessible={false}>
        <SafeAreaView style = {{margin: 10}}>
        
        <View style={{justifyContent: 'center'}}>
        <Text  style={{textAlign: 'center', fontSize: 30, fontWeight: 'bold', padding: 20}}>
        Text/Speech To Stencil! </Text>
        </View>
        <View
      style={{
        backgroundColor: 'white',
        borderColor: '#AAAAAA',
        borderWidth: 1,
        borderRadius: 5,
        marginTop: 10,
        minHeight: 50
      }}>
      
      <TextInput
        multiline
        numberOfLines={4}
        placeholder= "Enter Text to Convert here... "
        maxLength={400}
        onChangeText={text => onChangeText(text)}
        value={value}
        style={{padding: 7}}
      />
      </View>
      
      <View style={styles.createButtonSection}>
     <TouchableOpacity onPress={() => buttonPressed()} 
             style={styles.stencilCreateButton}>

      <View style={{
        backgroundColor: 'blue', borderRadius: 5, padding: 10}}>
             <Text style={styles.text}>
                Stencil Create Button
                
                </Text>

     
     </View>
             </TouchableOpacity>
     </View>

    </SafeAreaView>
    </TouchableWithoutFeedback>
    );
}

const styles = StyleSheet.create({
    createButtonSection: {
        width: '100%',
        height: '30%',
        justifyContent: 'center',
        alignItems: 'center',
     }, 
     stencilCreateButton: {
       backgroundColor: 'blue',
       color: 'white',
       borderRadius:5,
     },
     text: {
        color: 'white',
        fontWeight: 'bold',
        fontFamily: 'Arial',
        textSize: 30,
     }
})