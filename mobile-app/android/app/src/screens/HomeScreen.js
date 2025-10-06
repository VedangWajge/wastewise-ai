import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

const HomeScreen = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>♻️ Welcome to WasteWise</Text>
      <Text style={styles.subtitle}>AI-based Smart Waste Segregation System</Text>

      <Button title="📸 Capture Waste" onPress={() => navigation.navigate('Camera')} />
      <Button title="🚚 Find Services" onPress={() => navigation.navigate('ServiceDiscovery')} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#e8f5e9', padding: 20 },
  title: { fontSize: 24, fontWeight: 'bold', color: '#2d5a27', marginBottom: 10 },
  subtitle: { fontSize: 16, color: '#4caf50', marginBottom: 20, textAlign: 'center' },
});

export default HomeScreen;
