import { ImagePickerIOS } from 'react-native';
import {launchCamera, launchImageLibrary} from 'react-native-image-picker';
import ImagePicker from 'react-native-image-crop-picker';
//launchImageLibrary(options?, callback)

// You can also use as a promise without 'callback':
//const result = await launchImageLibrary(options?);


const Home = () => {
    const handleClick = () => {
        //choose photo from library
        console.log('click');
        console.warn('choose photo');
        ImagePicker.openPicker({
            width: 300,
            height: 400,
            cropping: true
        }).then(image => {
            console.log(image);
            setImage(image.path);
        });

    }

    return (
        <div className = "button">
            <button onClick = {handleClick}>Click me</button>
        </div>
    )
}

//no clue what this is
export default Home;