import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  Alert,
  TouchableOpacity,
} from 'react-native';
import ApiService from '../services/ApiService';

const DashboardScreen = ({ navigation }) => {
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStatistics();
  }, []);

  const loadStatistics = async () => {
    try {
      setLoading(true);
      const stats = await ApiService.getStatistics();
      setStatistics(stats);
    } catch (error) {
      Alert.alert('Error', 'Failed to load statistics: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ title, value, icon, color = '#4caf50' }) => (
    <View style={[styles.statCard, { borderLeftColor: color }]}>
      <Text style={styles.statIcon}>{icon}</Text>
      <View style={styles.statContent}>
        <Text style={styles.statValue}>{value}</Text>
        <Text style={styles.statTitle}>{title}</Text>
      </View>
    </View>
  );

  const CategoryCard = ({ category, count, percentage, color }) => (
    <View style={styles.categoryCard}>
      <View style={styles.categoryHeader}>
        <Text style={styles.categoryName}>{category}</Text>
        <Text style={[styles.categoryCount, { color }]}>{count}</Text>
      </View>
      <View style={styles.progressBar}>
        <View
          style={[
            styles.progressFill,
            { width: `${percentage}%`, backgroundColor: color }
          ]}
        />
      </View>
      <Text style={styles.categoryPercentage}>{percentage}%</Text>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#4caf50" />
        <Text style={styles.loadingText}>Loading dashboard...</Text>
      </View>
    );
  }

  if (!statistics) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>Failed to load statistics</Text>
        <TouchableOpacity style={styles.retryButton} onPress={loadStatistics}>
          <Text style={styles.retryText}>🔄 Retry</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>📊 My Impact Dashboard</Text>
        <Text style={styles.headerSubtitle}>
          Track your environmental contributions
        </Text>
      </View>

      <View style={styles.statsGrid}>
        <StatCard
          title="Items Classified"
          value={statistics.total_classifications}
          icon="🔍"
          color="#4caf50"
        />
        <StatCard
          title="CO₂ Saved"
          value={`${statistics.environmental_impact.co2_saved}kg`}
          icon="🌍"
          color="#2196f3"
        />
        <StatCard
          title="Water Saved"
          value={`${statistics.environmental_impact.water_saved}L`}
          icon="💧"
          color="#00bcd4"
        />
        <StatCard
          title="Energy Saved"
          value={`${statistics.environmental_impact.energy_saved}kWh`}
          icon="⚡"
          color="#ff9800"
        />
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Waste Categories</Text>
        <View style={styles.categoriesContainer}>
          {Object.entries(statistics.waste_breakdown).map(([category, data]) => (
            <CategoryCard
              key={category}
              category={category.charAt(0).toUpperCase() + category.slice(1)}
              count={data.count}
              percentage={data.percentage}
              color={getCategoryColor(category)}
            />
          ))}
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Recent Activity</Text>
        <View style={styles.activityContainer}>
          <Text style={styles.activityText}>
            🎯 Most classified: {statistics.most_common_waste_type}
          </Text>
          <Text style={styles.activityText}>
            📈 Average confidence: {(statistics.average_confidence * 100).toFixed(1)}%
          </Text>
          <Text style={styles.activityText}>
            🗓️ Last classification: {statistics.last_classification_date}
          </Text>
        </View>
      </View>

      <View style={styles.impactSection}>
        <Text style={styles.sectionTitle}>Environmental Impact</Text>
        <View style={styles.impactCard}>
          <Text style={styles.impactText}>
            Your waste classification efforts have helped save the equivalent of:
          </Text>
          <View style={styles.impactItems}>
            <Text style={styles.impactItem}>
              🌳 {statistics.environmental_impact.trees_equivalent} trees planted
            </Text>
            <Text style={styles.impactItem}>
              🚗 {statistics.environmental_impact.car_emissions_avoided} km of car emissions avoided
            </Text>
            <Text style={styles.impactItem}>
              💡 {statistics.environmental_impact.light_bulb_hours} hours of LED light bulb usage
            </Text>
          </View>
        </View>
      </View>
    </ScrollView>
  );
};

const getCategoryColor = (category) => {
  const colors = {
    plastic: '#f44336',
    organic: '#4caf50',
    paper: '#ff9800',
    glass: '#2196f3',
    metal: '#9c27b0',
  };
  return colors[category] || '#666';
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
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  errorText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 20,
  },
  retryButton: {
    backgroundColor: '#4caf50',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
  },
  retryText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
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
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: 15,
    justifyContent: 'space-between',
  },
  statCard: {
    backgroundColor: '#fff',
    width: '48%',
    padding: 15,
    borderRadius: 15,
    marginBottom: 15,
    flexDirection: 'row',
    alignItems: 'center',
    borderLeftWidth: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  statIcon: {
    fontSize: 24,
    marginRight: 12,
  },
  statContent: {
    flex: 1,
  },
  statValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2d5a27',
  },
  statTitle: {
    fontSize: 12,
    color: '#666',
    marginTop: 2,
  },
  section: {
    margin: 15,
    marginTop: 0,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2d5a27',
    marginBottom: 15,
  },
  categoriesContainer: {
    backgroundColor: '#fff',
    borderRadius: 15,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  categoryCard: {
    marginBottom: 15,
  },
  categoryHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  categoryName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  categoryCount: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  progressBar: {
    height: 6,
    backgroundColor: '#e0e0e0',
    borderRadius: 3,
    marginBottom: 5,
  },
  progressFill: {
    height: 6,
    borderRadius: 3,
  },
  categoryPercentage: {
    fontSize: 12,
    color: '#666',
    textAlign: 'right',
  },
  activityContainer: {
    backgroundColor: '#fff',
    borderRadius: 15,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  activityText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 10,
    lineHeight: 20,
  },
  impactSection: {
    margin: 15,
    marginTop: 0,
    marginBottom: 30,
  },
  impactCard: {
    backgroundColor: '#e8f5e8',
    borderRadius: 15,
    padding: 20,
    borderWidth: 1,
    borderColor: '#c8e6c8',
  },
  impactText: {
    fontSize: 14,
    color: '#2d5a27',
    marginBottom: 15,
    lineHeight: 20,
  },
  impactItems: {
    paddingLeft: 10,
  },
  impactItem: {
    fontSize: 14,
    color: '#2d5a27',
    marginBottom: 8,
    lineHeight: 20,
  },
});

export default DashboardScreen;