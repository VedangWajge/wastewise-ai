import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TextInput,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
} from 'react-native';
import ApiService from '../services/ApiService';

const BookingScreen = ({ route, navigation }) => {
  const { service, wasteType } = route.params;
  const [formData, setFormData] = useState({
    quantity: '',
    pickup_address: '',
    phone_number: '',
    scheduled_date: '',
    special_instructions: '',
  });
  const [loading, setLoading] = useState(false);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const validateForm = () => {
    if (!formData.quantity.trim()) {
      Alert.alert('Error', 'Please enter the quantity');
      return false;
    }
    if (!formData.pickup_address.trim()) {
      Alert.alert('Error', 'Please enter pickup address');
      return false;
    }
    if (!formData.phone_number.trim()) {
      Alert.alert('Error', 'Please enter your phone number');
      return false;
    }
    if (!formData.scheduled_date.trim()) {
      Alert.alert('Error', 'Please enter preferred date');
      return false;
    }
    return true;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;

    setLoading(true);
    try {
      const bookingData = {
        service_provider_id: service.id,
        waste_type: wasteType,
        ...formData,
      };

      const response = await ApiService.createBooking(bookingData);

      Alert.alert(
        'Success',
        'Booking created successfully!',
        [
          {
            text: 'OK',
            onPress: () => navigation.navigate('Home')
          }
        ]
      );
    } catch (error) {
      Alert.alert('Error', 'Failed to create booking: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.serviceInfo}>
        <Text style={styles.serviceName}>{service.name}</Text>
        <Text style={styles.serviceType}>{service.type}</Text>
        <Text style={styles.wasteType}>Booking for: {wasteType.toUpperCase()} Waste</Text>
      </View>

      <View style={styles.form}>
        <Text style={styles.formTitle}>Booking Details</Text>

        <View style={styles.inputGroup}>
          <Text style={styles.label}>Quantity/Description *</Text>
          <TextInput
            style={styles.input}
            value={formData.quantity}
            onChangeText={(value) => handleInputChange('quantity', value)}
            placeholder="e.g. 2 bags, 10kg, 1 large item"
            multiline
          />
        </View>

        <View style={styles.inputGroup}>
          <Text style={styles.label}>Pickup Address *</Text>
          <TextInput
            style={[styles.input, styles.textArea]}
            value={formData.pickup_address}
            onChangeText={(value) => handleInputChange('pickup_address', value)}
            placeholder="Enter complete pickup address"
            multiline
            numberOfLines={3}
          />
        </View>

        <View style={styles.inputGroup}>
          <Text style={styles.label}>Phone Number *</Text>
          <TextInput
            style={styles.input}
            value={formData.phone_number}
            onChangeText={(value) => handleInputChange('phone_number', value)}
            placeholder="Your contact number"
            keyboardType="phone-pad"
          />
        </View>

        <View style={styles.inputGroup}>
          <Text style={styles.label}>Preferred Date *</Text>
          <TextInput
            style={styles.input}
            value={formData.scheduled_date}
            onChangeText={(value) => handleInputChange('scheduled_date', value)}
            placeholder="DD/MM/YYYY or Today/Tomorrow"
          />
        </View>

        <View style={styles.inputGroup}>
          <Text style={styles.label}>Special Instructions</Text>
          <TextInput
            style={[styles.input, styles.textArea]}
            value={formData.special_instructions}
            onChangeText={(value) => handleInputChange('special_instructions', value)}
            placeholder="Any special instructions for pickup"
            multiline
            numberOfLines={2}
          />
        </View>

        <TouchableOpacity
          style={styles.submitButton}
          onPress={handleSubmit}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.submitButtonText}>📅 Book Service</Text>
          )}
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  serviceInfo: {
    backgroundColor: '#fff',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  serviceName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2d5a27',
  },
  serviceType: {
    fontSize: 14,
    color: '#4caf50',
    marginTop: 5,
  },
  wasteType: {
    fontSize: 14,
    color: '#666',
    marginTop: 5,
    fontWeight: 'bold',
  },
  form: {
    backgroundColor: '#fff',
    margin: 20,
    padding: 20,
    borderRadius: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  formTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2d5a27',
    marginBottom: 20,
    textAlign: 'center',
  },
  inputGroup: {
    marginBottom: 20,
  },
  label: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    color: '#333',
    backgroundColor: '#fafafa',
  },
  textArea: {
    height: 80,
    textAlignVertical: 'top',
  },
  submitButton: {
    backgroundColor: '#4caf50',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    marginTop: 10,
  },
  submitButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default BookingScreen;