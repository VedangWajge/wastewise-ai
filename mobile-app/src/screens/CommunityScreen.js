import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';

const CommunityScreen = ({ navigation }) => {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>🏢 Community Hub</Text>
        <Text style={styles.headerSubtitle}>
          Connect with your local community
        </Text>
      </View>

      <View style={styles.comingSoonCard}>
        <Text style={styles.comingSoonIcon}>🚧</Text>
        <Text style={styles.comingSoonTitle}>Coming Soon!</Text>
        <Text style={styles.comingSoonText}>
          Community features are under development. Soon you'll be able to:
        </Text>

        <View style={styles.featuresList}>
          <Text style={styles.featureItem}>🏘️ Join your neighborhood community</Text>
          <Text style={styles.featureItem}>📊 View community waste statistics</Text>
          <Text style={styles.featureItem}>🏆 Participate in recycling challenges</Text>
          <Text style={styles.featureItem}>📢 Get community announcements</Text>
          <Text style={styles.featureItem}>🤝 Connect with local environmental groups</Text>
          <Text style={styles.featureItem}>🌟 Earn community impact points</Text>
        </View>

        <TouchableOpacity style={styles.notifyButton}>
          <Text style={styles.notifyButtonText}>🔔 Notify Me When Ready</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.quickStatsCard}>
        <Text style={styles.quickStatsTitle}>Quick Community Stats</Text>
        <View style={styles.statsRow}>
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>2,847</Text>
            <Text style={styles.statLabel}>Items Classified</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>156</Text>
            <Text style={styles.statLabel}>Active Users</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>89%</Text>
            <Text style={styles.statLabel}>Recycling Rate</Text>
          </View>
        </View>
      </View>

      <View style={styles.tipCard}>
        <Text style={styles.tipTitle}>💡 Community Tip</Text>
        <Text style={styles.tipText}>
          Did you know? Communities that actively participate in waste classification
          see a 40% increase in proper recycling rates!
        </Text>
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
  comingSoonCard: {
    backgroundColor: '#fff',
    margin: 20,
    padding: 30,
    borderRadius: 15,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  comingSoonIcon: {
    fontSize: 48,
    marginBottom: 15,
  },
  comingSoonTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2d5a27',
    marginBottom: 10,
  },
  comingSoonText: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
    marginBottom: 20,
    lineHeight: 20,
  },
  featuresList: {
    width: '100%',
    marginBottom: 25,
  },
  featureItem: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
    paddingLeft: 10,
  },
  notifyButton: {
    backgroundColor: '#4caf50',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 25,
  },
  notifyButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  quickStatsCard: {
    backgroundColor: '#fff',
    marginHorizontal: 20,
    marginBottom: 20,
    padding: 20,
    borderRadius: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  quickStatsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2d5a27',
    marginBottom: 15,
    textAlign: 'center',
  },
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  statItem: {
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#4caf50',
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 5,
    textAlign: 'center',
  },
  tipCard: {
    backgroundColor: '#e8f5e8',
    marginHorizontal: 20,
    marginBottom: 30,
    padding: 20,
    borderRadius: 15,
    borderWidth: 1,
    borderColor: '#c8e6c8',
  },
  tipTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2d5a27',
    marginBottom: 10,
  },
  tipText: {
    fontSize: 14,
    color: '#2d5a27',
    lineHeight: 20,
  },
});

export default CommunityScreen;