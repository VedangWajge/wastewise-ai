import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
} from 'react-native';
import ApiService from '../services/ApiService';

const ServiceDiscoveryScreen = ({ route, navigation }) => {
  const { wasteType } = route.params;
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadServices();
  }, []);

  const loadServices = async () => {
    try {
      setLoading(true);
      const response = await ApiService.findNearbyServices(wasteType);
      setServices(response.services);
    } catch (error) {
      Alert.alert('Error', 'Failed to load services: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleServiceSelect = (service) => {
    navigation.navigate('Booking', { service, wasteType });
  };

  const renderServiceItem = ({ item }) => (
    <TouchableOpacity
      style={styles.serviceCard}
      onPress={() => handleServiceSelect(item)}
    >
      <View style={styles.serviceHeader}>
        <Text style={styles.serviceName}>{item.name}</Text>
        <Text style={styles.serviceType}>{item.type}</Text>
      </View>

      <Text style={styles.serviceAddress}>{item.address}</Text>

      <View style={styles.serviceDetails}>
        <Text style={styles.detailItem}>📞 {item.phone}</Text>
        <Text style={styles.detailItem}>📧 {item.email}</Text>
      </View>

      <View style={styles.serviceFooter}>
        <Text style={styles.distance}>{item.distance}</Text>
        <Text style={styles.rating}>⭐ {item.rating}/5</Text>
      </View>

      <View style={styles.servicesOffered}>
        <Text style={styles.servicesTitle}>Services:</Text>
        {item.services_offered.map((service, index) => (
          <Text key={index} style={styles.serviceOffered}>
            • {service}
          </Text>
        ))}
      </View>
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#4caf50" />
        <Text style={styles.loadingText}>Finding services for {wasteType}...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>
          Services for {wasteType.toUpperCase()} Waste
        </Text>
        <Text style={styles.headerSubtitle}>
          Found {services.length} service providers
        </Text>
      </View>

      <FlatList
        data={services}
        keyExtractor={(item) => item.id}
        renderItem={renderServiceItem}
        contentContainerStyle={styles.listContainer}
        showsVerticalScrollIndicator={false}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#666',
  },
  header: {
    backgroundColor: '#fff',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2d5a27',
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 5,
  },
  listContainer: {
    padding: 15,
  },
  serviceCard: {
    backgroundColor: '#fff',
    marginBottom: 15,
    padding: 20,
    borderRadius: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  serviceHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 10,
  },
  serviceName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2d5a27',
    flex: 1,
  },
  serviceType: {
    fontSize: 12,
    color: '#4caf50',
    backgroundColor: '#e8f5e8',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 5,
    fontWeight: 'bold',
  },
  serviceAddress: {
    fontSize: 14,
    color: '#666',
    marginBottom: 15,
  },
  serviceDetails: {
    marginBottom: 15,
  },
  detailItem: {
    fontSize: 13,
    color: '#666',
    marginBottom: 5,
  },
  serviceFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  distance: {
    fontSize: 14,
    color: '#666',
    fontWeight: 'bold',
  },
  rating: {
    fontSize: 14,
    color: '#ff9800',
    fontWeight: 'bold',
  },
  servicesOffered: {
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
    paddingTop: 15,
  },
  servicesTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#2d5a27',
    marginBottom: 5,
  },
  serviceOffered: {
    fontSize: 13,
    color: '#666',
    marginBottom: 2,
  },
});

export default ServiceDiscoveryScreen;