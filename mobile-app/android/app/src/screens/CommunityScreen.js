import React from 'react';
import { View, Text, StyleSheet, FlatList } from 'react-native';

const posts = [
  { id: '1', user: 'Anita', text: 'Started composting kitchen waste! 🌿' },
  { id: '2', user: 'Rahul', text: 'Donated old laptop to recycler ♻️' },
  { id: '3', user: 'Priya', text: 'Organized eWaste drive in society!' },
];

const CommunityScreen = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Community Feed</Text>
      <FlatList
        data={posts}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={styles.post}>
            <Text style={styles.user}>{item.user}</Text>
            <Text>{item.text}</Text>
          </View>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#f9fbe7' },
  title: { fontSize: 20, fontWeight: 'bold', color: '#2d5a27', marginBottom: 10 },
  post: { backgroundColor: '#fff', padding: 15, borderRadius: 10, marginVertical: 8, elevation: 2 },
  user: { fontWeight: 'bold', color: '#4caf50' },
});

export default CommunityScreen;
