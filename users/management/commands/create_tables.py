from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Create users tables manually'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Check if custom_user table exists
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.tables 
                WHERE table_name = 'custom_user'
            """)
            table_exists = cursor.fetchone()[0]
            
            if not table_exists:
                # Create the tables by running the migration SQL
                cursor.execute("""
                    CREATE TABLE custom_user (
                        id BIGSERIAL PRIMARY KEY,
                        password VARCHAR(128) NOT NULL,
                        last_login TIMESTAMP,
                        is_superuser BOOLEAN NOT NULL,
                        username VARCHAR(150) UNIQUE NOT NULL,
                        first_name VARCHAR(150),
                        last_name VARCHAR(150),
                        email VARCHAR(254),
                        is_staff BOOLEAN NOT NULL,
                        is_active BOOLEAN NOT NULL,
                        date_joined TIMESTAMP NOT NULL,
                        phone_number VARCHAR(20),
                        address TEXT,
                        date_of_birth DATE,
                        is_customer BOOLEAN NOT NULL DEFAULT TRUE,
                        is_staff_member BOOLEAN NOT NULL DEFAULT FALSE,
                        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                        updated_at TIMESTAMP NOT NULL DEFAULT NOW()
                    )
                """)
                
                # Create other tables
                cursor.execute("""
                    CREATE TABLE registration (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        user_id BIGINT UNIQUE NOT NULL REFERENCES custom_user(id) ON DELETE CASCADE,
                        status VARCHAR(20) NOT NULL DEFAULT 'pending',
                        registration_type VARCHAR(20) NOT NULL DEFAULT 'customer',
                        confirmation_token VARCHAR(100) UNIQUE,
                        is_email_verified BOOLEAN NOT NULL DEFAULT FALSE,
                        registration_date TIMESTAMP NOT NULL DEFAULT NOW(),
                        confirmed_date TIMESTAMP,
                        notes TEXT
                    )
                """)
                
                cursor.execute("""
                    CREATE TABLE email_verification (
                        id BIGSERIAL PRIMARY KEY,
                        user_id BIGINT NOT NULL REFERENCES custom_user(id) ON DELETE CASCADE,
                        token VARCHAR(100) UNIQUE NOT NULL,
                        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                        expires_at TIMESTAMP NOT NULL,
                        is_used BOOLEAN NOT NULL DEFAULT FALSE
                    )
                """)
                
                cursor.execute("""
                    CREATE TABLE password_reset (
                        id BIGSERIAL PRIMARY KEY,
                        user_id BIGINT NOT NULL REFERENCES custom_user(id) ON DELETE CASCADE,
                        token VARCHAR(100) UNIQUE NOT NULL,
                        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                        expires_at TIMESTAMP NOT NULL,
                        is_used BOOLEAN NOT NULL DEFAULT FALSE
                    )
                """)
                
                cursor.execute("""
                    CREATE TABLE user_profile (
                        id BIGSERIAL PRIMARY KEY,
                        user_id BIGINT UNIQUE NOT NULL REFERENCES custom_user(id) ON DELETE CASCADE,
                        profile_picture VARCHAR(100),
                        gender VARCHAR(1),
                        bio VARCHAR(500),
                        website VARCHAR(200),
                        social_media_links JSONB DEFAULT '{}',
                        preferences JSONB DEFAULT '{}',
                        notification_settings JSONB DEFAULT '{}',
                        last_login_ip INET,
                        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                        updated_at TIMESTAMP NOT NULL DEFAULT NOW()
                    )
                """)
                
                self.stdout.write(
                    self.style.SUCCESS('Successfully created all users tables')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('Tables already exist')
                )
