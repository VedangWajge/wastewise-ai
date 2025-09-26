import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
  Image,
  ActivityIndicator,
} from 'react-native';
import { launchImageLibrary, launchCamera } from 'react-native-image-picker';
import ApiService from '../services/ApiService';

const CameraScreen = ({ navigation }) => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const showImagePicker = () => {
    const options = {
      mediaType: 'photo',
      includeBase64: false,
      maxHeight: 2000,
      maxWidth: 2000,
    };

    Alert.alert(
      'Select Image',
      'Choose how you want to add an image',
      [
        { text: 'Camera', onPress: () => openCamera(options) },
        { text: 'Gallery', onPress: () => openGallery(options) },
        { text: 'Cancel', style: 'cancel' },
      ]
    );
  };

  const openCamera = (options) => {
    launchCamera(options, handleImageResponse);
  };

  const openGallery = (options) => {
    launchImageLibrary(options, handleImageResponse);
  };

  const handleImageResponse = (response) => {
    if (response.didCancel) {
      return;
    }

    if (response.errorMessage) {
      Alert.alert('Error', response.errorMessage);
      return;
    }

    const imageUri = response.assets[0].uri;
    setSelectedImage(imageUri);
  };

  const classifyImage = async () => {
    if (!selectedImage) {
      Alert.alert('Error', 'Please select an image first');
      return;
    }

    setLoading(true);
    try {
      const result = await ApiService.classifyWaste(selectedImage);
      navigation.navigate('Classification', { result, imageUri: selectedImage });
    } catch (error) {
      Alert.alert('Error', 'Failed to classify image: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.imageContainer}>
        {selectedImage ? (
          <Image source={{ uri: selectedImage }} style={styles.image} />
        ) : (
          <View style={styles.placeholder}>
            <Text style={styles.placeholderText}>📸</Text>
            <Text style={styles.placeholderSubtext}>No image selected</Text>
          </View>
        )}
      </View>

      <View style={styles.buttonContainer}>
        <TouchableOpacity
          style={styles.button}
          onPress={showImagePicker}
          disabled={loading}
        >
          <Text style={styles.buttonText}>
            {selectedImage ? '📷 Change Image' : '📷 Select Image'}
          </Text>
        </TouchableOpacity>

        {selectedImage && (
          <TouchableOpacity
            style={[styles.button, styles.classifyButton]}
            onPress={classifyImage}
            disabled={loading}
          >
            {loading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.buttonText}>🔍 Classify Waste</Text>
            )}
          </TouchableOpacity>
        )}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 20,
  },
  imageContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 30,
  },
  image: {
    width: 300,
    height: 300,
    borderRadius: 15,
    resizeMode: 'cover',
  },
  placeholder: {
    width: 300,
    height: 300,
    backgroundColor: '#e0e0e0',
    borderRadius: 15,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#ccc',
    borderStyle: 'dashed',
  },
  placeholderText: {
    fontSize: 60,
    marginBottom: 10,
  },
  placeholderSubtext: {
    fontSize: 16,
    color: '#666',
  },
  buttonContainer: {
    gap: 15,
  },
  button: {
    backgroundColor: '#4caf50',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  classifyButton: {
    backgroundColor: '#2d5a27',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default CameraScreen;