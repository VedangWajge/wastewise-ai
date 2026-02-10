"""
Pricing utility for waste valuation
Calculates estimated prices based on waste type, quantity, and market rates
"""

from datetime import datetime

class WastePricing:
    """
    Handles pricing calculations for different waste types
    Supports both collection service pricing and marketplace waste valuation
    """

    # Base rates per kg for different waste types (in INR)
    MARKET_RATES = {
        'plastic': {
            'PET bottles': 15,
            'HDPE': 12,
            'PVC': 8,
            'LDPE': 10,
            'PP': 14,
            'PS': 6,
            'mixed': 10
        },
        'paper': {
            'newspaper': 8,
            'cardboard': 6,
            'office paper': 10,
            'magazines': 7,
            'mixed': 7
        },
        'metal': {
            'aluminum': 80,
            'steel': 25,
            'copper': 400,
            'brass': 250,
            'iron': 20,
            'mixed': 30
        },
        'glass': {
            'clear': 2,
            'colored': 1.5,
            'mixed': 2
        },
        'e-waste': {
            'mobile phones': 50,
            'laptops': 200,
            'batteries': 30,
            'circuit boards': 100,
            'cables': 15,
            'mixed': 40
        },
        'organic': {
            'compost': 0,  # Usually free for composting
            'garden waste': 0,
            'food waste': 0
        }
    }

    # Service provider collection charges (per kg)
    COLLECTION_CHARGES = {
        'plastic': 5,
        'paper': 4,
        'metal': 8,
        'glass': 6,
        'e-waste': 15,
        'organic': 3
    }

    # Minimum booking amounts
    MIN_BOOKING_AMOUNT = 50  # INR

    # Base pickup charge
    BASE_PICKUP_CHARGE = 30  # INR

    @classmethod
    def calculate_waste_value(cls, waste_type, quantity_kg, subtype='mixed'):
        """
        Calculate the market value of waste

        Args:
            waste_type: Type of waste (plastic, paper, metal, etc.)
            quantity_kg: Quantity in kilograms
            subtype: Subtype of waste (e.g., 'PET bottles', 'newspaper')

        Returns:
            dict: {
                'waste_type': str,
                'quantity_kg': float,
                'subtype': str,
                'rate_per_kg': float,
                'total_value': float,
                'currency': 'INR'
            }
        """
        waste_type = waste_type.lower()
        quantity_kg = float(quantity_kg)

        # Get rate for waste type and subtype
        if waste_type in cls.MARKET_RATES:
            rates = cls.MARKET_RATES[waste_type]
            rate_per_kg = rates.get(subtype, rates.get('mixed', 0))
        else:
            rate_per_kg = 0

        total_value = rate_per_kg * quantity_kg

        return {
            'waste_type': waste_type,
            'quantity_kg': quantity_kg,
            'subtype': subtype,
            'rate_per_kg': rate_per_kg,
            'total_value': round(total_value, 2),
            'currency': 'INR'
        }

    @classmethod
    def calculate_collection_cost(cls, waste_type, quantity_kg, distance_km=0):
        """
        Calculate the cost for waste collection service

        Args:
            waste_type: Type of waste
            quantity_kg: Quantity in kilograms
            distance_km: Distance to collection point

        Returns:
            dict: {
                'waste_type': str,
                'quantity_kg': float,
                'base_charge': float,
                'collection_charge_per_kg': float,
                'collection_charge': float,
                'distance_charge': float,
                'subtotal': float,
                'tax': float (18% GST),
                'total_cost': float,
                'currency': 'INR'
            }
        """
        waste_type = waste_type.lower()
        quantity_kg = float(quantity_kg)
        distance_km = float(distance_km)

        # Get collection charge per kg
        charge_per_kg = cls.COLLECTION_CHARGES.get(waste_type, 5)

        # Calculate charges
        base_charge = cls.BASE_PICKUP_CHARGE
        collection_charge = charge_per_kg * quantity_kg

        # Distance charge: ₹2 per km beyond 5km
        distance_charge = max(0, (distance_km - 5) * 2) if distance_km > 0 else 0

        subtotal = base_charge + collection_charge + distance_charge

        # Apply minimum booking amount
        if subtotal < cls.MIN_BOOKING_AMOUNT:
            subtotal = cls.MIN_BOOKING_AMOUNT

        # Calculate 18% GST
        tax = subtotal * 0.18
        total_cost = subtotal + tax

        return {
            'waste_type': waste_type,
            'quantity_kg': quantity_kg,
            'base_charge': base_charge,
            'collection_charge_per_kg': charge_per_kg,
            'collection_charge': round(collection_charge, 2),
            'distance_km': distance_km,
            'distance_charge': round(distance_charge, 2),
            'subtotal': round(subtotal, 2),
            'tax': round(tax, 2),
            'tax_percentage': 18,
            'total_cost': round(total_cost, 2),
            'currency': 'INR'
        }

    @classmethod
    def calculate_net_transaction(cls, waste_type, quantity_kg, subtype='mixed', distance_km=0):
        """
        Calculate net value for user (waste value - collection cost)
        Useful for marketplace listings where users can see potential earnings

        Args:
            waste_type: Type of waste
            quantity_kg: Quantity in kilograms
            subtype: Subtype of waste
            distance_km: Distance to collection point

        Returns:
            dict: {
                'waste_value': dict,
                'collection_cost': dict,
                'net_amount': float (positive = user earns, negative = user pays),
                'transaction_type': 'earning' | 'payment',
                'currency': 'INR'
            }
        """
        waste_value = cls.calculate_waste_value(waste_type, quantity_kg, subtype)
        collection_cost = cls.calculate_collection_cost(waste_type, quantity_kg, distance_km)

        net_amount = waste_value['total_value'] - collection_cost['total_cost']

        return {
            'waste_value': waste_value,
            'collection_cost': collection_cost,
            'net_amount': round(net_amount, 2),
            'transaction_type': 'earning' if net_amount > 0 else 'payment',
            'currency': 'INR',
            'summary': {
                'waste_type': waste_type,
                'quantity_kg': quantity_kg,
                'subtype': subtype,
                'you_earn' if net_amount > 0 else 'you_pay': abs(round(net_amount, 2))
            }
        }

    @classmethod
    def get_price_breakdown(cls, waste_items, distance_km=0):
        """
        Calculate pricing for multiple waste items

        Args:
            waste_items: List of dicts with {waste_type, quantity_kg, subtype}
            distance_km: Distance to collection point

        Returns:
            dict: Detailed breakdown of all items
        """
        items = []
        total_waste_value = 0
        total_collection_cost = 0

        for item in waste_items:
            waste_type = item.get('waste_type')
            quantity_kg = item.get('quantity_kg', 0)
            subtype = item.get('subtype', 'mixed')

            waste_value = cls.calculate_waste_value(waste_type, quantity_kg, subtype)
            collection_cost = cls.calculate_collection_cost(waste_type, quantity_kg, 0)  # Distance applied once

            items.append({
                'waste_type': waste_type,
                'quantity_kg': quantity_kg,
                'subtype': subtype,
                'waste_value': waste_value['total_value'],
                'collection_charge': collection_cost['collection_charge']
            })

            total_waste_value += waste_value['total_value']
            total_collection_cost += collection_cost['collection_charge']

        # Add distance charge once
        distance_charge = max(0, (distance_km - 5) * 2) if distance_km > 0 else 0

        subtotal = cls.BASE_PICKUP_CHARGE + total_collection_cost + distance_charge

        # Apply minimum
        if subtotal < cls.MIN_BOOKING_AMOUNT:
            subtotal = cls.MIN_BOOKING_AMOUNT

        tax = subtotal * 0.18
        total_cost = subtotal + tax
        net_amount = total_waste_value - total_cost

        return {
            'items': items,
            'total_waste_value': round(total_waste_value, 2),
            'base_charge': cls.BASE_PICKUP_CHARGE,
            'total_collection_charge': round(total_collection_cost, 2),
            'distance_km': distance_km,
            'distance_charge': round(distance_charge, 2),
            'subtotal': round(subtotal, 2),
            'tax': round(tax, 2),
            'tax_percentage': 18,
            'total_cost': round(total_cost, 2),
            'net_amount': round(net_amount, 2),
            'transaction_type': 'earning' if net_amount > 0 else 'payment',
            'currency': 'INR'
        }

    @classmethod
    def get_waste_subtypes(cls, waste_type):
        """
        Get available subtypes for a waste type

        Args:
            waste_type: Type of waste

        Returns:
            list: Available subtypes with their rates
        """
        waste_type = waste_type.lower()
        if waste_type in cls.MARKET_RATES:
            rates = cls.MARKET_RATES[waste_type]
            return [
                {
                    'subtype': subtype,
                    'rate_per_kg': rate,
                    'currency': 'INR'
                }
                for subtype, rate in rates.items()
            ]
        return []
