import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

const ProfileScreen = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>My Profile</Text>
      <Text>Name: Shreya Sawant</Text>
      <Text>Email: sawantshreya647@gmail.com</Text>
      <Text>Member Since: 2024</Text>
      <Button title="Logout" onPress={() => alert('Logged out successfully!')} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', justifyContent: 'center', backgroundColor: '#f1f8e9' },
  title: { fontSize: 22, fontWeight: 'bold', marginBottom: 15, color: '#2d5a27' },
});

export default ProfileScreen;
