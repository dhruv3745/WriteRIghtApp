import * as React from 'react';
import { StyleSheet, Text, View, TouchableOpacity, Dimensions } from 'react-native';

const WIDTH = Dimensions.get('window').width;
const HEIGHT_MODAL = 150;

const WhatTypeStencil = () => {

    return(
        <TouchableOpacity
            disabled={true}
            style={styles.container}
        >
        <View style={styles.modal}>
            <View style={styles.textView}>
                <Text style={styles.text}> Stencil Type </Text>
                <Text style={styles.text}> How do you want to create a stencil?</Text>
            </View>

        </View>


        </TouchableOpacity>
    )
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        alignContent: 'center',
    },
    modal: {
        height: HEIGHT_MODAL,
        width: WIDTH - 80,
        paddingTop: 10,
        backgroundColor:'white',
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
    }
})