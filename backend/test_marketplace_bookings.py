"""
Test script to debug marketplace bookings issue
"""
import sqlite3
import os

def check_marketplace_bookings():
    """Check if marketplace bookings exist in database"""

    # Find the database file
    db_path = 'wastewise.db'

    if not os.path.exists(db_path):
        print(f"[ERROR] Database file not found: {db_path}")
        return

    print(f"[OK] Database file found: {db_path}")
    print("\n" + "=" * 60)
    print("MARKETPLACE BOOKINGS DIAGNOSTIC")
    print("=" * 60)

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Check if table exists
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='marketplace_bookings'
        """)
        table_exists = cursor.fetchone()

        if not table_exists:
            print("\n[ERROR] marketplace_bookings table does not exist!")
            print("Run the app first to create tables")
            return

        print("\n[OK] marketplace_bookings table exists")

        # Get total bookings count
        cursor.execute("SELECT COUNT(*) as total FROM marketplace_bookings")
        total = cursor.fetchone()['total']
        print(f"\nTotal bookings in database: {total}")

        if total == 0:
            print("\n[INFO] No bookings found in database")
            print("This is why the frontend shows 'No bookings found'")
            print("\nTo create test bookings:")
            print("1. Go to Marketplace → Browse Listings")
            print("2. Click on a listing and book it")
            print("3. Or create a listing and have someone book it")
        else:
            print(f"\n[OK] Found {total} bookings")

            # Show all bookings
            cursor.execute("""
                SELECT b.id, b.buyer_id, b.seller_id, b.status,
                       b.payment_status, b.created_at,
                       l.title as listing_title,
                       l.waste_type
                FROM marketplace_bookings b
                LEFT JOIN marketplace_listings l ON b.listing_id = l.id
                ORDER BY b.created_at DESC
            """)

            bookings = cursor.fetchall()

            print("\n" + "-" * 60)
            print("BOOKINGS LIST:")
            print("-" * 60)

            for booking in bookings:
                print(f"\nBooking ID: {booking['id']}")
                print(f"  Listing: {booking['listing_title']}")
                print(f"  Waste Type: {booking['waste_type']}")
                print(f"  Buyer ID: {booking['buyer_id']}")
                print(f"  Seller ID: {booking['seller_id']}")
                print(f"  Status: {booking['status']}")
                print(f"  Payment: {booking['payment_status']}")
                print(f"  Created: {booking['created_at']}")

        # Check marketplace listings
        cursor.execute("SELECT COUNT(*) as total FROM marketplace_listings")
        listings_total = cursor.fetchone()['total']
        print(f"\n" + "-" * 60)
        print(f"Total marketplace listings: {listings_total}")

        if listings_total == 0:
            print("\n[INFO] No listings found")
            print("Create listings first before bookings can be made")
        else:
            cursor.execute("""
                SELECT id, title, waste_type, status, seller_id
                FROM marketplace_listings
                LIMIT 5
            """)
            listings = cursor.fetchall()
            print("\nSample Listings:")
            for listing in listings:
                print(f"  - {listing['title']} ({listing['waste_type']}) - {listing['status']}")

        # Check users
        cursor.execute("SELECT COUNT(*) as total FROM users")
        users_total = cursor.fetchone()['total']
        print(f"\nTotal users: {users_total}")

        conn.close()

        print("\n" + "=" * 60)
        print("DIAGNOSTIC COMPLETE")
        print("=" * 60)

    except Exception as e:
        print(f"\n[ERROR] Database error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_marketplace_bookings()
