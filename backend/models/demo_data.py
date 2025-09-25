import random
from datetime import datetime, timedelta
import uuid

class DemoDataGenerator:
    def __init__(self):
        self.service_providers = self._generate_service_providers()
        self.communities = self._generate_communities()
        self.bookings = self._generate_bookings()
        self.notifications = self._generate_notifications()

    def _generate_service_providers(self):
        providers = [
            {
                'id': 'sp_001',
                'name': 'Green Earth NGO',
                'type': 'NGO',
                'speciality': ['paper', 'organic'],
                'location': {'lat': 19.0760, 'lng': 72.8777, 'address': 'Bandra West, Mumbai'},
                'contact': {'phone': '+91-98765-43210', 'email': 'contact@greenearth.org'},
                'rating': 4.8,
                'operating_hours': '9:00 AM - 6:00 PM',
                'capacity': '500 kg/day',
                'verified': True,
                'description': 'Leading environmental NGO focusing on paper and organic waste recycling'
            },
            {
                'id': 'sp_002',
                'name': 'TechCycle E-Waste Center',
                'type': 'E-Waste',
                'speciality': ['metal', 'glass'],
                'location': {'lat': 19.1136, 'lng': 72.8697, 'address': 'Andheri East, Mumbai'},
                'contact': {'phone': '+91-98765-43211', 'email': 'info@techcycle.com'},
                'rating': 4.6,
                'operating_hours': '10:00 AM - 7:00 PM',
                'capacity': '200 devices/day',
                'verified': True,
                'description': 'Professional e-waste recycling with data security guarantee'
            },
            {
                'id': 'sp_003',
                'name': 'Mumbai Compost Hub',
                'type': 'Composting',
                'speciality': ['organic'],
                'location': {'lat': 19.0176, 'lng': 72.8562, 'address': 'Worli, Mumbai'},
                'contact': {'phone': '+91-98765-43212', 'email': 'hello@compostHub.in'},
                'rating': 4.9,
                'operating_hours': '8:00 AM - 8:00 PM',
                'capacity': '1000 kg/day',
                'verified': True,
                'description': 'Converting organic waste into high-quality fertilizer'
            },
            {
                'id': 'sp_004',
                'name': 'RecyclePlus Industries',
                'type': 'Recycling',
                'speciality': ['plastic', 'paper', 'glass'],
                'location': {'lat': 19.0728, 'lng': 72.8826, 'address': 'Lower Parel, Mumbai'},
                'contact': {'phone': '+91-98765-43213', 'email': 'operations@recycleplus.co.in'},
                'rating': 4.5,
                'operating_hours': '9:00 AM - 6:00 PM',
                'capacity': '2000 kg/day',
                'verified': True,
                'description': 'Industrial-scale recycling with innovative processing methods'
            },
            {
                'id': 'sp_005',
                'name': 'Organic Fertilizers Co.',
                'type': 'Fertilizer',
                'speciality': ['organic'],
                'location': {'lat': 19.0330, 'lng': 72.8397, 'address': 'Tardeo, Mumbai'},
                'contact': {'phone': '+91-98765-43214', 'email': 'procurement@organicfert.com'},
                'rating': 4.7,
                'operating_hours': '7:00 AM - 5:00 PM',
                'capacity': '800 kg/day',
                'verified': True,
                'description': 'Premium organic fertilizer production from kitchen waste'
            }
        ]
        return providers

    def _generate_communities(self):
        communities = [
            {
                'id': 'comm_001',
                'name': 'Sunshine Apartments',
                'type': 'Residential Complex',
                'location': {'lat': 19.0896, 'lng': 72.8656, 'address': 'Juhu, Mumbai'},
                'total_units': 120,
                'active_users': 89,
                'admin_contact': {'name': 'Rajesh Sharma', 'phone': '+91-98765-11111'},
                'waste_generation': {'daily_avg': '450 kg', 'monthly_total': '13,500 kg'},
                'sustainability_score': 85,
                'preferred_services': ['sp_001', 'sp_003'],
                'achievements': ['Water Warrior', 'Green Champion', 'Waste Reducer']
            },
            {
                'id': 'comm_002',
                'name': 'Tech Park Business Center',
                'type': 'Commercial Complex',
                'location': {'lat': 19.1197, 'lng': 72.9081, 'address': 'Powai, Mumbai'},
                'total_units': 45,
                'active_users': 234,
                'admin_contact': {'name': 'Priya Patel', 'phone': '+91-98765-22222'},
                'waste_generation': {'daily_avg': '890 kg', 'monthly_total': '26,700 kg'},
                'sustainability_score': 92,
                'preferred_services': ['sp_002', 'sp_004'],
                'achievements': ['E-Waste Expert', 'Carbon Neutral', 'Innovation Leader']
            },
            {
                'id': 'comm_003',
                'name': 'Green Valley Society',
                'type': 'Gated Community',
                'location': {'lat': 19.0522, 'lng': 72.8311, 'address': 'Breach Candy, Mumbai'},
                'total_units': 200,
                'active_users': 145,
                'admin_contact': {'name': 'Anita Desai', 'phone': '+91-98765-33333'},
                'waste_generation': {'daily_avg': '650 kg', 'monthly_total': '19,500 kg'},
                'sustainability_score': 78,
                'preferred_services': ['sp_001', 'sp_005'],
                'achievements': ['Composting King', 'Green Society Award']
            }
        ]
        return communities

    def _generate_bookings(self):
        bookings = []
        statuses = ['Scheduled', 'In Progress', 'Completed', 'Cancelled']
        waste_types = ['plastic', 'organic', 'paper', 'glass', 'metal']

        for i in range(50):
            booking_date = datetime.now() - timedelta(days=random.randint(0, 30))
            bookings.append({
                'id': f'book_{i+1:03d}',
                'user_id': f'user_{random.randint(1, 100):03d}',
                'community_id': random.choice([c['id'] for c in self.communities]),
                'service_provider_id': random.choice([sp['id'] for sp in self.service_providers]),
                'waste_type': random.choice(waste_types),
                'quantity': f"{random.randint(5, 100)} kg",
                'status': random.choice(statuses),
                'created_at': booking_date.isoformat(),
                'scheduled_date': (booking_date + timedelta(days=random.randint(1, 7))).isoformat(),
                'pickup_address': random.choice([c['location']['address'] for c in self.communities]),
                'special_instructions': 'Handle with care' if random.random() > 0.7 else '',
                'estimated_cost': random.randint(50, 500),
                'rating': random.randint(4, 5) if random.random() > 0.3 else None
            })

        return bookings

    def _generate_notifications(self):
        notifications = [
            {
                'id': 'notif_001',
                'title': '♻️ Pickup Scheduled',
                'message': 'Your organic waste pickup is scheduled for tomorrow at 10:00 AM',
                'type': 'pickup_scheduled',
                'timestamp': (datetime.now() - timedelta(hours=2)).isoformat(),
                'read': False,
                'action_url': '/bookings/book_001'
            },
            {
                'id': 'notif_002',
                'title': '🏆 Achievement Unlocked!',
                'message': 'Congratulations! You have earned the "Green Champion" badge',
                'type': 'achievement',
                'timestamp': (datetime.now() - timedelta(days=1)).isoformat(),
                'read': False,
                'action_url': '/profile/achievements'
            },
            {
                'id': 'notif_003',
                'title': '📊 Weekly Impact Report',
                'message': 'This week you helped save 15kg CO₂ and 45 liters of water!',
                'type': 'impact_report',
                'timestamp': (datetime.now() - timedelta(days=2)).isoformat(),
                'read': True,
                'action_url': '/dashboard/impact'
            },
            {
                'id': 'notif_004',
                'title': '🚛 Pickup Completed',
                'message': 'Your plastic waste has been successfully collected by RecyclePlus Industries',
                'type': 'pickup_completed',
                'timestamp': (datetime.now() - timedelta(days=3)).isoformat(),
                'read': True,
                'action_url': '/bookings/book_045'
            }
        ]
        return notifications

    def get_nearby_services(self, waste_type, location=None):
        """Simulate finding nearby service providers based on waste type"""
        suitable_providers = [
            sp for sp in self.service_providers
            if waste_type in sp['speciality'] or sp['type'] == 'Recycling'
        ]

        # Simulate distance calculation and sorting
        for provider in suitable_providers:
            provider['distance'] = f"{random.uniform(0.5, 10.0):.1f} km"
            provider['estimated_time'] = f"{random.randint(15, 60)} min"
            provider['available_slots'] = [
                'Today 2:00 PM - 4:00 PM',
                'Tomorrow 10:00 AM - 12:00 PM',
                'Tomorrow 3:00 PM - 5:00 PM'
            ]

        return sorted(suitable_providers, key=lambda x: float(x['distance'].split()[0]))

    def get_community_stats(self, community_id):
        """Generate community-specific statistics"""
        community = next((c for c in self.communities if c['id'] == community_id), None)
        if not community:
            return None

        return {
            'community': community,
            'monthly_stats': {
                'total_classifications': random.randint(800, 1500),
                'waste_breakdown': {
                    'organic': random.randint(200, 400),
                    'plastic': random.randint(150, 300),
                    'paper': random.randint(100, 250),
                    'glass': random.randint(50, 150),
                    'metal': random.randint(30, 100)
                },
                'services_used': len([b for b in self.bookings if b['community_id'] == community_id]),
                'cost_savings': random.randint(5000, 15000),
                'environmental_impact': {
                    'co2_saved': f"{random.randint(100, 500)} kg",
                    'water_saved': f"{random.randint(1000, 5000)} liters",
                    'energy_saved': f"{random.randint(200, 800)} kWh"
                }
            },
            'leaderboard': [
                {'unit': f'A-{i+1}', 'user': f'Resident {i+1}', 'points': random.randint(800, 1200)}
                for i in range(10)
            ]
        }

    def simulate_booking_process(self, booking_data):
        """Simulate the booking creation and tracking process"""
        booking_id = f"book_{len(self.bookings)+1:03d}"

        new_booking = {
            'id': booking_id,
            'user_id': booking_data.get('user_id', 'demo_user'),
            'service_provider_id': booking_data['service_provider_id'],
            'waste_type': booking_data['waste_type'],
            'quantity': booking_data['quantity'],
            'pickup_address': booking_data['pickup_address'],
            'status': 'Scheduled',
            'created_at': datetime.now().isoformat(),
            'scheduled_date': booking_data['scheduled_date'],
            'estimated_cost': random.randint(50, 300),
            'tracking_steps': [
                {'step': 'Booking Confirmed', 'status': 'completed', 'time': datetime.now().isoformat()},
                {'step': 'Service Provider Notified', 'status': 'completed', 'time': (datetime.now() + timedelta(minutes=5)).isoformat()},
                {'step': 'Pickup Scheduled', 'status': 'in_progress', 'time': None},
                {'step': 'Waste Collected', 'status': 'pending', 'time': None},
                {'step': 'Processing Complete', 'status': 'pending', 'time': None}
            ]
        }

        self.bookings.append(new_booking)
        return new_booking

# Global instance for the demo
demo_data = DemoDataGenerator()