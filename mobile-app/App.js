/**
 * WasteWise Mobile App
 * AI-Powered Smart Waste Segregation System
 */

import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { StatusBar, StyleSheet } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';

// Screens
import HomeScreen from './src/screens/HomeScreen';
import CameraScreen from './src/screens/CameraScreen';
import ClassificationScreen from './src/screens/ClassificationScreen';
import ServiceDiscoveryScreen from './src/screens/ServiceDiscoveryScreen';
import BookingScreen from './src/screens/BookingScreen';
import DashboardScreen from './src/screens/DashboardScreen';
import CommunityScreen from './src/screens/CommunityScreen';
import ProfileScreen from './src/screens/ProfileScreen';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

const HomeStack = () => {
  return (
    <Stack.Navigator
      initialRouteName="Home"
      screenOptions={{
        headerStyle: {
          backgroundColor: '#2d5a27',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      }}>
      <Stack.Screen
        name="Home"
        component={HomeScreen}
        options={{
          title: '🌱 WasteWise',
          headerStyle: {
            backgroundColor: '#4caf50',
          },
        }}
      />
      <Stack.Screen
        name="Camera"
        component={CameraScreen}
        options={{ title: '📸 Capture Waste' }}
      />
      <Stack.Screen
        name="Classification"
        component={ClassificationScreen}
        options={{ title: '🔍 Classification Results' }}
      />
      <Stack.Screen
        name="ServiceDiscovery"
        component={ServiceDiscoveryScreen}
        options={{ title: '🚚 Find Services' }}
      />
      <Stack.Screen
        name="Booking"
        component={BookingScreen}
        options={{ title: '📅 Book Service' }}
      />
    </Stack.Navigator>
  );
};

const MainTabs = () => {
  return (
    <Tab.Navigator
      initialRouteName="HomeStack"
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;

          if (route.name === 'HomeStack') {
            iconName = 'camera-alt';
          } else if (route.name === 'Dashboard') {
            iconName = 'dashboard';
          } else if (route.name === 'Community') {
            iconName = 'apartment';
          } else if (route.name === 'Profile') {
            iconName = 'person';
          }

          return <Icon name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#4caf50',
        tabBarInactiveTintColor: 'gray',
        tabBarStyle: {
          backgroundColor: '#fff',
          borderTopWidth: 1,
          borderTopColor: '#e0e0e0',
          paddingVertical: 5,
          height: 60,
        },
        tabBarLabelStyle: {
          fontSize: 12,
          fontWeight: '600',
        },
        headerShown: false,
      })}>
      <Tab.Screen
        name="HomeStack"
        component={HomeStack}
        options={{ tabBarLabel: 'Classify' }}
      />
      <Tab.Screen
        name="Dashboard"
        component={DashboardScreen}
        options={{ tabBarLabel: 'Dashboard' }}
      />
      <Tab.Screen
        name="Community"
        component={CommunityScreen}
        options={{ tabBarLabel: 'Community' }}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{ tabBarLabel: 'Profile' }}
      />
    </Tab.Navigator>
  );
};

const App = () => {
  return (
    <NavigationContainer>
      <StatusBar
        barStyle="light-content"
        backgroundColor="#2d5a27"
        translucent={false}
      />
      <MainTabs />
    </NavigationContainer>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
});

export default App;