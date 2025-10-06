import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const DashboardScreen = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Your Eco Dashboard</Text>
      <Text style={styles.stat}>Total Waste Classified: 120</Text>
      <Text style={styles.stat}>eWaste Segregated: 45</Text>
      <Text style={styles.stat}>Points Earned: 320 🌟</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', justifyContent: 'center', backgroundColor: '#e8f5e9' },
  title: { fontSize: 22, fontWeight: 'bold', marginBottom: 15, color: '#2d5a27' },
  stat: { fontSize: 16, marginVertical: 4 },
});

export default DashboardScreen;
