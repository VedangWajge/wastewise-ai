import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  Image,
  TouchableOpacity,
  ScrollView,
} from 'react-native';

const ClassificationScreen = ({ route, navigation }) => {
  const { result, imageUri } = route.params;

  const handleFindServices = () => {
    navigation.navigate('ServiceDiscovery', {
      wasteType: result.classification.waste_type,
    });
  };

  const handleNewClassification = () => {
    navigation.navigate('Camera');
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.imageContainer}>
        <Image source={{ uri: imageUri }} style={styles.image} />
      </View>

      <View style={styles.resultCard}>
        <Text style={styles.resultTitle}>Classification Result</Text>

        <View style={styles.resultItem}>
          <Text style={styles.label}>Waste Type:</Text>
          <Text style={styles.wasteType}>
            {result.classification.waste_type.toUpperCase()}
          </Text>
        </View>

        <View style={styles.resultItem}>
          <Text style={styles.label}>Confidence:</Text>
          <Text style={styles.confidence}>
            {(result.classification.confidence * 100).toFixed(1)}%
          </Text>
        </View>

        <View style={styles.recommendationsContainer}>
          <Text style={styles.sectionTitle}>Disposal Recommendations</Text>
          {result.classification.recommendations.map((rec, index) => (
            <Text key={index} style={styles.recommendation}>
              • {rec}
            </Text>
          ))}
        </View>

        <View style={styles.impactContainer}>
          <Text style={styles.sectionTitle}>Environmental Impact</Text>
          <Text style={styles.impact}>
            {result.classification.environmental_impact}
          </Text>
        </View>
      </View>

      <View style={styles.buttonContainer}>
        <TouchableOpacity
          style={styles.button}
          onPress={handleFindServices}
        >
          <Text style={styles.buttonText}>🚚 Find Disposal Services</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.button, styles.secondaryButton]}
          onPress={handleNewClassification}
        >
          <Text style={[styles.buttonText, styles.secondaryButtonText]}>
            📸 Classify Another Item
          </Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  imageContainer: {
    alignItems: 'center',
    padding: 20,
  },
  image: {
    width: 200,
    height: 200,
    borderRadius: 15,
    resizeMode: 'cover',
  },
  resultCard: {
    backgroundColor: '#fff',
    margin: 20,
    padding: 20,
    borderRadius: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  resultTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2d5a27',
    marginBottom: 15,
    textAlign: 'center',
  },
  resultItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
    paddingVertical: 5,
  },
  label: {
    fontSize: 16,
    color: '#666',
  },
  wasteType: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#4caf50',
  },
  confidence: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2d5a27',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2d5a27',
    marginTop: 20,
    marginBottom: 10,
  },
  recommendationsContainer: {
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
    paddingTop: 15,
  },
  recommendation: {
    fontSize: 14,
    color: '#666',
    marginBottom: 5,
    lineHeight: 20,
  },
  impactContainer: {
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
    paddingTop: 15,
  },
  impact: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  buttonContainer: {
    padding: 20,
    gap: 15,
  },
  button: {
    backgroundColor: '#4caf50',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  secondaryButton: {
    backgroundColor: 'transparent',
    borderWidth: 2,
    borderColor: '#4caf50',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  secondaryButtonText: {
    color: '#4caf50',
  },
});

export default ClassificationScreen;