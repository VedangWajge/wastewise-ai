import React, { useEffect, useState } from 'react';
import { View, Text, Image, Button, StyleSheet, ActivityIndicator } from 'react-native';
import { classifyWaste } from '../services/classifier';

const ClassificationScreen = ({ route, navigation }) => {
  const { imageUri } = route.params;
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const classify = async () => {
      const prediction = await classifyWaste(imageUri);
      setResult(prediction);
      setLoading(false);
    };
    classify();
  }, []);

  if (loading) {
    return <ActivityIndicator size="large" color="#4caf50" style={{ flex: 1 }} />;
  }

  return (
    <View style={styles.container}>
      <Image source={{ uri: imageUri }} style={styles.image} />
      <Text style={styles.title}>Classification Result</Text>
      <Text style={styles.result}>Category: {result.category}</Text>
      <Text>Confidence: {(result.confidence * 100).toFixed(1)}%</Text>
      <Button title="Find Services" onPress={() => navigation.navigate('ServiceDiscovery')} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', padding: 20 },
  image: { width: 300, height: 300, borderRadius: 10, marginVertical: 20 },
  title: { fontSize: 22, fontWeight: 'bold', color: '#2d5a27' },
  result: { fontSize: 18, marginVertical: 10, color: '#4caf50' },
});

export default ClassificationScreen;
