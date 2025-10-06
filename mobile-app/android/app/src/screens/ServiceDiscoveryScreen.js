import React from 'react';
import { View, Text, Button, StyleSheet, FlatList } from 'react-native';

const services = [
  { id: '1', name: 'EcoCollect Center', distance: '1.2 km' },
  { id: '2', name: 'GreenBin Recycler', distance: '2.5 km' },
  { id: '3', name: 'Smart eWaste Drop', distance: '3.8 km' },
];

const ServiceDiscoveryScreen = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Nearby Recycling Centers</Text>
      <FlatList
        data={services}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.name}>{item.name}</Text>
            <Text>{item.distance} away</Text>
            <Button title="Book Pickup" onPress={() => navigation.navigate('Booking', { name: item.name })} />
          </View>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#f1f8e9' },
  title: { fontSize: 20, fontWeight: 'bold', color: '#2d5a27', marginBottom: 10 },
  card: { backgroundColor: '#fff', padding: 15, marginVertical: 8, borderRadius: 10, elevation: 3 },
  name: { fontSize: 16, fontWeight: 'bold' },
});

export default ServiceDiscoveryScreen;
