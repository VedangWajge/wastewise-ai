import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

const BookingScreen = ({ route, navigation }) => {
  const { name } = route.params || {};

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Book a Pickup</Text>
      <Text style={styles.text}>Service Provider: {name || 'Not Selected'}</Text>
      <Text style={styles.text}>Pickup Date: Tomorrow 10:00 AM</Text>
      <Button title="Confirm Booking" onPress={() => alert('Pickup Confirmed ✅')} />
      <Button title="Back to Dashboard" onPress={() => navigation.navigate('Dashboard')} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  title: { fontSize: 20, fontWeight: 'bold', color: '#2d5a27', marginBottom: 10 },
  text: { fontSize: 16, marginBottom: 5 },
});

export default BookingScreen;
