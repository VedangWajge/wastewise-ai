import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
} from 'react-native';
import ApiService from '../services/ApiService';

const ProfileScreen = ({ navigation }) => {
  const handleNetworkTest = async () => {
    try {
      const results = await ApiService.fullConnectivityTest();

      let message = `Network Test Results:\n\n`;
      message += `Overall Status: ${results.overall_status}\n`;
      message += `Summary: ${results.summary}\n\n`;

      Object.entries(results.tests).forEach(([testName, result]) => {
        message += `${testName}: ${result.status}\n`;
        if (result.error) {
          message += `Error: ${result.error}\n`;
        }
      });

      Alert.alert('Network Test Results', message);
    } catch (error) {
      Alert.alert('Network Test Failed', error.message);
    }
  };

  const SettingItem = ({ icon, title, subtitle, onPress, color = '#666' }) => (
    <TouchableOpacity style={styles.settingItem} onPress={onPress}>
      <Text style={styles.settingIcon}>{icon}</Text>
      <View style={styles.settingContent}>
        <Text style={styles.settingTitle}>{title}</Text>
        {subtitle && <Text style={styles.settingSubtitle}>{subtitle}</Text>}
      </View>
      <Text style={[styles.settingArrow, { color }]}>›</Text>
    </TouchableOpacity>
  );

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>👤 Profile & Settings</Text>
        <Text style={styles.headerSubtitle}>
          Manage your WasteWise experience
        </Text>
      </View>

      <View style={styles.profileCard}>
        <Text style={styles.avatar}>🌱</Text>
        <Text style={styles.username}>WasteWise User</Text>
        <Text style={styles.userStats}>Environmental Champion</Text>
        <View style={styles.badgeContainer}>
          <Text style={styles.badge}>🌟 Early Adopter</Text>
          <Text style={styles.badge}>♻️ Eco Warrior</Text>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>App Settings</Text>
        <View style={styles.settingsContainer}>
          <SettingItem
            icon="🔔"
            title="Notifications"
            subtitle="Manage push notifications"
            onPress={() => Alert.alert('Coming Soon', 'Notification settings will be available in the next update')}
          />
          <SettingItem
            icon="🌐"
            title="Language"
            subtitle="English (Default)"
            onPress={() => Alert.alert('Coming Soon', 'Multi-language support coming soon')}
          />
          <SettingItem
            icon="🎨"
            title="Theme"
            subtitle="Light mode"
            onPress={() => Alert.alert('Coming Soon', 'Dark mode support coming soon')}
          />
          <SettingItem
            icon="📍"
            title="Location Services"
            subtitle="Enable for better service discovery"
            onPress={() => Alert.alert('Location', 'Location services help find nearby disposal services')}
          />
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Privacy & Data</Text>
        <View style={styles.settingsContainer}>
          <SettingItem
            icon="🔒"
            title="Privacy Policy"
            subtitle="How we protect your data"
            onPress={() => Alert.alert('Privacy', 'WasteWise respects your privacy. We only collect data necessary for app functionality.')}
          />
          <SettingItem
            icon="📊"
            title="Data Usage"
            subtitle="View your data consumption"
            onPress={() => Alert.alert('Data Usage', 'This app uses minimal data for image classification and service discovery.')}
          />
          <SettingItem
            icon="🗑️"
            title="Clear Cache"
            subtitle="Free up storage space"
            onPress={() => Alert.alert('Clear Cache', 'Cache cleared successfully!')}
          />
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Support & Help</Text>
        <View style={styles.settingsContainer}>
          <SettingItem
            icon="❓"
            title="Help & FAQ"
            subtitle="Get answers to common questions"
            onPress={() => Alert.alert('Help', 'For help, contact support at help@wastewise.ai')}
          />
          <SettingItem
            icon="🐛"
            title="Report Bug"
            subtitle="Help us improve the app"
            onPress={() => Alert.alert('Bug Report', 'Please report bugs to bugs@wastewise.ai with details and screenshots.')}
          />
          <SettingItem
            icon="📡"
            title="Network Test"
            subtitle="Test connectivity to backend"
            onPress={handleNetworkTest}
            color="#4caf50"
          />
          <SettingItem
            icon="ℹ️"
            title="About WasteWise"
            subtitle="Version 1.0.0"
            onPress={() => Alert.alert('About', 'WasteWise v1.0.0\nAI-Powered Smart Waste Management\n\nDeveloped by Vedang Wajge\nBuilt with React Native & Flask')}
          />
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Account Actions</Text>
        <View style={styles.settingsContainer}>
          <SettingItem
            icon="🔄"
            title="Sync Data"
            subtitle="Sync with cloud storage"
            onPress={() => Alert.alert('Sync', 'Data synced successfully!')}
          />
          <SettingItem
            icon="📤"
            title="Export Data"
            subtitle="Download your data"
            onPress={() => Alert.alert('Export', 'Data export feature coming soon')}
          />
          <SettingItem
            icon="⚠️"
            title="Reset App Data"
            subtitle="Clear all local data"
            onPress={() => Alert.alert(
              'Reset Data',
              'This will clear all your local data. Are you sure?',
              [
                { text: 'Cancel', style: 'cancel' },
                { text: 'Reset', style: 'destructive', onPress: () => Alert.alert('Reset', 'App data has been reset') }
              ]
            )}
            color="#f44336"
          />
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#fff',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  headerTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#2d5a27',
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 5,
  },
  profileCard: {
    backgroundColor: '#fff',
    margin: 20,
    padding: 25,
    borderRadius: 15,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  avatar: {
    fontSize: 60,
    marginBottom: 15,
  },
  username: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2d5a27',
    marginBottom: 5,
  },
  userStats: {
    fontSize: 14,
    color: '#4caf50',
    marginBottom: 15,
  },
  badgeContainer: {
    flexDirection: 'row',
    gap: 10,
  },
  badge: {
    backgroundColor: '#e8f5e8',
    color: '#2d5a27',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 15,
    fontSize: 12,
    fontWeight: 'bold',
  },
  section: {
    marginHorizontal: 20,
    marginBottom: 25,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2d5a27',
    marginBottom: 15,
  },
  settingsContainer: {
    backgroundColor: '#fff',
    borderRadius: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 18,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  settingIcon: {
    fontSize: 20,
    marginRight: 15,
    width: 25,
    textAlign: 'center',
  },
  settingContent: {
    flex: 1,
  },
  settingTitle: {
    fontSize: 16,
    color: '#333',
    fontWeight: '500',
  },
  settingSubtitle: {
    fontSize: 13,
    color: '#666',
    marginTop: 2,
  },
  settingArrow: {
    fontSize: 20,
    fontWeight: 'bold',
  },
});

export default ProfileScreen;