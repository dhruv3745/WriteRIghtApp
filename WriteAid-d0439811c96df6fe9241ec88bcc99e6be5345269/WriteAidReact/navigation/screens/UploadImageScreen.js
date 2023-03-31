import { useState, useEffect } from 'react';
import * as React from 'react';
import {View, Text, Image, Button} from 'react-native';
import ImagePicker from 'react-native-image-picker';
import * as MediaLibrary from 'expo-media-library';

export default function UploadImageScreen({navigation}) {

    /*const [hasMediaLibraryPermission, setHasMediaLibraryPermission] = useState();

    useEffect(() => {
        (async () => {
          const mediaLibraryPermission = await MediaLibrary.requestPermissionsAsync();
          setHasMediaLibraryPermission(mediaLibraryPermission.status === "granted");
        })();
      }, []);
            

  const state = {
    photo: null,
  };

  const handleChoosePhoto = () => {
    const options = {
      noData: true,
    }
    ImagePicker.launchImageLibrary(options, response => {
        if (response.uri) {
          state = { photo: response }
        }
      })
  };

  

  
    const { photo } = state;
    return (
      <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
        {photo && (
          <Image
            source={{ uri: photo.uri }}
            style={{ width: 300, height: 300 }}
          />
        )}
        <Button title="Choose Photo" onPress={ async () => {
  let _image = await ImagePicker.launchImageLibraryAsync()
}
} />
      </View>
    );
  
*/

const [image, setImage] = useState(null);

  const selectImage = () => {
    const options = {
      title: 'Select Image',
      storageOptions: {
        skipBackup: true,
        path: 'images',
      },
    };

    ImagePicker.showImagePicker(options, (response) => {
      if (response.didCancel) {
        console.log('User cancelled image picker');
      } else if (response.error) {
        console.log('ImagePicker Error: ', response.error);
      } else if (response.customButton) {
        console.log('User tapped custom button: ', response.customButton);
      } else {
        setImage(response);
      }
    });
  };

  const uploadImage = () => {
    const data = new FormData();
    data.append('file', {
      name: image.fileName,
      type: image.type,
      uri:
        Platform.OS === 'android'
          ? image.uri
          : image.uri.replace('file://', ''),
    });

    fetch('YOUR_UPLOAD_URL', {
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      body: data,
    })
      .then((response) => response.json())
      .then((response) => {
        Alert.alert('Image Uploaded');
      })
      .catch((error) => {
        console.error(error);
      });
  };

  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Button title="Select Image" onPress={selectImage} />
      {image && (
        <View>
          <Image
            source={{ uri: image.uri }}
            style={{ width: 200, height: 200 }}
          />
          <Button title="Upload Image" onPress={uploadImage} />
        </View>
      )}
    </View>
  );
      
}
