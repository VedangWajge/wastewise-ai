import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Dimensions,
  Alert,
  PermissionsAndroid,
  Platform,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import LinearGradient from 'react-native-linear-gradient';
import Geolocation from 'react-native-geolocation-service';
import ApiService from '../services/ApiService';

const { width, height } = Dimensions.get('window');

const HomeScreen = ({ navigation }) => {
  const [location, setLocation] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    requestLocationPermission();
    fetchDashboardStats();
  }, []);

  const requestLocationPermission = async () => {
    if (Platform.OS === 'android') {
      try {
        const granted = await PermissionsAndroid.request(
          PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
          {
            title: 'Location Access Required',
            message: 'WasteWise needs access to your location to find nearby services',
            buttonNeutral: 'Ask Me Later',
            buttonNegative: 'Cancel',
            buttonPositive: 'OK',
          },
        );

        if (granted === PermissionsAndroid.RESULTS.GRANTED) {
          getCurrentLocation();
        }
      } catch (err) {
        console.warn(err);
      }
    } else {
      getCurrentLocation();
    }
  };

  const getCurrentLocation = () => {
    Geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        const locationData = { latitude, longitude };
        setLocation(locationData);
        ApiService.updateUserLocation(locationData);
      },
      (error) => {
        console.log('Location error:', error);
        Alert.alert(
          'Location Error',
          'Unable to get your location. You can still use the app without location services.',
        );
      },
      { enableHighAccuracy: true, timeout: 15000, maximumAge: 10000 }
    );
  };

  const fetchDashboardStats = async () => {
    try {
      const response = await ApiService.getStatistics();
      setStats(response);
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCameraPress = () => {
    navigation.navigate('Camera');
  };

  const handleQuickAction = (wasteType) => {
    navigation.navigate('ServiceDiscovery', { wasteType });
  };

  const getWasteTypeIcon = (type) => {
    const icons = {
      plastic: '♻️',
      organic: '🌱',
      paper: '📄',
      glass: '🗞️',
      metal: '🔧',
    };
    return icons[type] || '🗑️';
  };

  const quickActions = [
    { type: 'plastic', label: 'Plastic', color: '#2196f3' },
    { type: 'organic', label: 'Organic', color: '#4caf50' },
    { type: 'paper', label: 'Paper', color: '#ff9800' },
    { type: 'glass', label: 'Glass', color: '#00bcd4' },
    { type: 'metal', label: 'Metal', color: '#607d8b' },
  ];

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      {/* Header Section */}
      <LinearGradient
        colors={['#4caf50', '#2d5a27']}
        style={styles.headerSection}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}>
        <Text style={styles.welcomeText}>Welcome to WasteWise</Text>
        <Text style={styles.subtitleText}>AI-Powered Smart Waste Classification</Text>

        {location && (
          <View style={styles.locationBadge}>
            <Icon name="location-on" size={16} color="#fff" />
            <Text style={styles.locationText}>Location Enabled</Text>
          </View>
        )}
      </LinearGradient>

      {/* Main Action Button */}
      <View style={styles.mainActionSection}>
        <TouchableOpacity style={styles.cameraButton} onPress={handleCameraPress}>
          <LinearGradient
            colors={['#66bb6a', '#4caf50']}
            style={styles.cameraButtonGradient}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}>
            <Icon name="camera-alt" size={40} color="#fff" />
            <Text style={styles.cameraButtonText}>Classify Waste</Text>
            <Text style={styles.cameraButtonSubtext}>Take a photo or upload image</Text>
          </LinearGradient>
        </TouchableOpacity>
      </View>

      {/* Quick Stats */}
      {stats && (
        <View style={styles.statsSection}>
          <Text style={styles.sectionTitle}>📊 Your Impact</Text>
          <View style={styles.statsRow}>
            <View style={styles.statCard}>
              <Text style={styles.statNumber}>{stats.total_classifications}</Text>
              <Text style={styles.statLabel}>Classifications</Text>
            </View>
            <View style={styles.statCard}>
              <Text style={styles.statNumber}>{stats.recycling_rate}%</Text>
              <Text style={styles.statLabel}>Recycling Rate</Text>
            </View>
          </View>

          <View style={styles.impactCard}>
            <Text style={styles.impactTitle}>🌍 Environmental Impact</Text>
            <View style={styles.impactRow}>
              <View style={styles.impactItem}>
                <Text style={styles.impactValue}>{stats.environmental_impact?.co2_saved}</Text>
                <Text style={styles.impactLabel}>CO₂ Saved</Text>
              </View>
              <View style={styles.impactItem}>
                <Text style={styles.impactValue}>{stats.environmental_impact?.water_saved}</Text>
                <Text style={styles.impactLabel}>Water Saved</Text>
              </View>
              <View style={styles.impactItem}>
                <Text style={styles.impactValue}>{stats.environmental_impact?.energy_saved}</Text>
                <Text style={styles.impactLabel}>Energy Saved</Text>
              </View>
            </View>
          </View>
        </View>
      )}

      {/* Quick Actions */}
      <View style={styles.quickActionsSection}>
        <Text style={styles.sectionTitle}>🚀 Quick Actions</Text>
        <Text style={styles.sectionSubtitle}>Find services by waste type</Text>

        <View style={styles.quickActionsGrid}>
          {quickActions.map((action) => (
            <TouchableOpacity
              key={action.type}
              style={[styles.quickActionCard, { borderColor: action.color }]}
              onPress={() => handleQuickAction(action.type)}>
              <Text style={styles.quickActionIcon}>
                {getWasteTypeIcon(action.type)}
              </Text>
              <Text style={styles.quickActionLabel}>{action.label}</Text>
              <View style={[styles.quickActionBadge, { backgroundColor: action.color }]}>
                <Icon name="search" size={16} color="#fff" />
              </View>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      {/* Recent Activity */}
      <View style={styles.recentSection}>
        <Text style={styles.sectionTitle}>📋 How It Works</Text>
        <View style={styles.stepsContainer}>
          <View style={styles.stepItem}>
            <View style={styles.stepNumber}>
              <Text style={styles.stepNumberText}>1</Text>
            </View>
            <View style={styles.stepContent}>
              <Text style={styles.stepTitle}>Capture or Upload</Text>
              <Text style={styles.stepDescription}>Take a photo of your waste item</Text>
            </View>
          </View>

          <View style={styles.stepItem}>
            <View style={styles.stepNumber}>
              <Text style={styles.stepNumberText}>2</Text>
            </View>
            <View style={styles.stepContent}>
              <Text style={styles.stepTitle}>AI Classification</Text>
              <Text style={styles.stepDescription}>Our AI identifies the waste type</Text>
            </View>
          </View>

          <View style={styles.stepItem}>
            <View style={styles.stepNumber}>
              <Text style={styles.stepNumberText}>3</Text>
            </View>
            <View style={styles.stepContent}>
              <Text style={styles.stepTitle}>Find Services</Text>
              <Text style={styles.stepDescription}>Get connected to nearby disposal services</Text>
            </View>
          </View>

          <View style={styles.stepItem}>
            <View style={styles.stepNumber}>
              <Text style={styles.stepNumberText}>4</Text>
            </View>
            <View style={styles.stepContent}>
              <Text style={styles.stepTitle}>Book & Track</Text>
              <Text style={styles.stepDescription}>Schedule pickup and track your impact</Text>
            </View>
          </View>
        </View>
      </View>

      {/* Footer padding */}
      <View style={styles.footerPadding} />
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f7fa',
  },
  headerSection: {
    paddingHorizontal: 20,
    paddingVertical: 30,
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
  },
  welcomeText: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
    marginBottom: 8,
  },
  subtitleText: {
    fontSize: 16,
    color: '#e8f5e8',
    textAlign: 'center',
    marginBottom: 15,
  },
  locationBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
    alignSelf: 'center',
  },
  locationText: {
    color: '#fff',
    fontSize: 14,
    marginLeft: 6,
    fontWeight: '500',
  },
  mainActionSection: {
    paddingHorizontal: 20,
    paddingVertical: 30,
    alignItems: 'center',
  },
  cameraButton: {
    width: width * 0.8,
    height: 120,
    borderRadius: 20,
    elevation: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
  },
  cameraButtonGradient: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 20,
  },
  cameraButtonText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 8,
  },
  cameraButtonSubtext: {
    fontSize: 14,
    color: '#e8f5e8',
    marginTop: 4,
  },
  sectionTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#2d5a27',
    marginBottom: 8,
  },
  sectionSubtitle: {
    fontSize: 16,
    color: '#666',
    marginBottom: 20,
  },
  statsSection: {
    paddingHorizontal: 20,
    paddingVertical: 20,
  },
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 16,
    marginHorizontal: 5,
    alignItems: 'center',
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  statNumber: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#4caf50',
  },
  statLabel: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  impactCard: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 16,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  impactTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2d5a27',
    marginBottom: 15,
    textAlign: 'center',
  },
  impactRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  impactItem: {
    alignItems: 'center',
  },
  impactValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#4caf50',
  },
  impactLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
    textAlign: 'center',
  },
  quickActionsSection: {
    paddingHorizontal: 20,
    paddingVertical: 20,
  },
  quickActionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  quickActionCard: {
    width: (width - 60) / 2,
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 16,
    marginBottom: 15,
    alignItems: 'center',
    position: 'relative',
    borderWidth: 2,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  quickActionIcon: {
    fontSize: 32,
    marginBottom: 8,
  },
  quickActionLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  quickActionBadge: {
    position: 'absolute',
    top: 15,
    right: 15,
    width: 30,
    height: 30,
    borderRadius: 15,
    justifyContent: 'center',
    alignItems: 'center',
  },
  recentSection: {
    paddingHorizontal: 20,
    paddingVertical: 20,
  },
  stepsContainer: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 20,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  stepItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  stepNumber: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#4caf50',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 15,
  },
  stepNumberText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  stepContent: {
    flex: 1,
  },
  stepTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  stepDescription: {
    fontSize: 14,
    color: '#666',
  },
  footerPadding: {
    height: 80,
  },
});

export default HomeScreen;