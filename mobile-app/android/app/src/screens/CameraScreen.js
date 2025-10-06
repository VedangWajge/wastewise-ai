import React, { useState } from 'react';
import { View, Text, Button, Image, StyleSheet } from 'react-native';
import * as ImagePicker from 'expo-image-picker';

const CameraScreen = ({ navigation }) => {
  const [image, setImage] = useState(null);

  const takePicture = async () => {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') {
      alert('Camera permission required!');
      return;
    }

    const result = await ImagePicker.launchCameraAsync({
      allowsEditing: true,
      quality: 1,
    });

    if (!result.canceled) {
      const uri = result.assets[0].uri;
      setImage(uri);
      navigation.navigate('Classification', { imageUri: uri });
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.text}>Capture a photo of your waste item.</Text>
      <Button title="Open Camera" onPress={takePicture} />
      {image && <Image source={{ uri: image }} style={styles.preview} />}
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  text: { marginBottom: 20, fontSize: 16, textAlign: 'center' },
  preview: { width: 300, height: 300, marginTop: 20, borderRadius: 10 },
});

export default CameraScreen;
