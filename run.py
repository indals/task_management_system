# run.py
import os
from app import create_app, db
from app.urls import register_routes

# Set environment variables for Flask CLI
os.environ['FLASK_APP'] = 'run.py'
os.environ['FLASK_ENV'] = 'development'

# Create the app with default config
app = create_app('development')

# Register routes
register_routes(app)

# This is needed for Flask CLI commands like 'flask db init'
# Flask CLI will use this app instance
if __name__ == '__main__':
    app.run(debug=True)




# # Drop all tables (if you don't mind losing data)
# flask --app "run:create_app('development')" db drop

# # Initialize migrations
# flask --app "run:create_app('development')" db init

# # Create migration
# flask --app "run:create_app('development')" db migrate -m "initial migration"

# # Apply migration
# flask --app "run:create_app('development')" db upgrade

# # Import data
# python import_data.py



# -- Add missing columns to user table
# ALTER TABLE "user" ADD COLUMN IF NOT EXISTS avatar_url VARCHAR(500);
# ALTER TABLE "user" ADD COLUMN IF NOT EXISTS bio TEXT;  
# ALTER TABLE "user" ADD COLUMN IF NOT EXISTS skills TEXT;
# ALTER TABLE "user" ADD COLUMN IF NOT EXISTS github_username VARCHAR(100);
# ALTER TABLE "user" ADD COLUMN IF NOT EXISTS linkedin_url VARCHAR(500);
# ALTER TABLE "user" ADD COLUMN IF NOT EXISTS phone VARCHAR(20);
# ALTER TABLE "user" ADD COLUMN IF NOT EXISTS timezone VARCHAR(50) DEFAULT 'UTC';
# ALTER TABLE "user" ADD COLUMN IF NOT EXISTS daily_work_hours FLOAT DEFAULT 8.0;
# ALTER TABLE "user" ADD COLUMN IF NOT EXISTS hourly_rate FLOAT;
# ALTER TABLE "user" ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
# ALTER TABLE "user" ADD COLUMN IF NOT EXISTS last_login TIMESTAMP;

# -- Create ENUM types for new tables
# DO $$ BEGIN
#     CREATE TYPE sprintstatus AS ENUM ('PLANNED', 'ACTIVE', 'COMPLETED', 'CANCELLED');
# EXCEPTION
#     WHEN duplicate_object THEN null;
# END $$;

# DO $$ BEGIN
#     CREATE TYPE estimationunit AS ENUM ('HOURS', 'DAYS', 'STORY_POINTS');
# EXCEPTION
#     WHEN duplicate_object THEN null;
# END $$;

# -- Create sprint table
# CREATE TABLE IF NOT EXISTS sprint (
#     id SERIAL PRIMARY KEY,
#     name VARCHAR(200) NOT NULL,
#     description TEXT,
#     status sprintstatus NOT NULL DEFAULT 'PLANNED',
#     project_id INTEGER NOT NULL REFERENCES project(id) ON DELETE CASCADE,
#     start_date TIMESTAMP NOT NULL,
#     end_date TIMESTAMP NOT NULL,
#     goal TEXT,
#     capacity_hours FLOAT,
#     velocity_points INTEGER,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

# -- Create project_members table  
# CREATE TABLE IF NOT EXISTS project_members (
#     id SERIAL PRIMARY KEY,
#     project_id INTEGER NOT NULL REFERENCES project(id) ON DELETE CASCADE,
#     user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
#     role VARCHAR(100),
#     can_create_tasks BOOLEAN DEFAULT TRUE,
#     can_edit_tasks BOOLEAN DEFAULT TRUE,
#     can_delete_tasks BOOLEAN DEFAULT FALSE,
#     can_manage_sprints BOOLEAN DEFAULT FALSE,
#     can_manage_members BOOLEAN DEFAULT FALSE,
#     joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     UNIQUE(project_id, user_id)
# );

# -- Create task_attachments table
# CREATE TABLE IF NOT EXISTS task_attachments (
#     id SERIAL PRIMARY KEY,
#     task_id INTEGER NOT NULL REFERENCES task(id) ON DELETE CASCADE,
#     uploaded_by_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
#     filename VARCHAR(255) NOT NULL,
#     original_filename VARCHAR(255) NOT NULL,
#     file_path VARCHAR(500) NOT NULL,
#     file_size INTEGER,
#     mime_type VARCHAR(100),
#     uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

# -- Create time_logs table
# CREATE TABLE IF NOT EXISTS time_logs (
#     id SERIAL PRIMARY KEY,
#     task_id INTEGER NOT NULL REFERENCES task(id) ON DELETE CASCADE,  
#     user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
#     hours FLOAT NOT NULL,
#     description TEXT,
#     work_date DATE NOT NULL DEFAULT CURRENT_DATE,
#     logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

# -- Add sprint_id to task table if not exists
# ALTER TABLE task ADD COLUMN IF NOT EXISTS sprint_id INTEGER REFERENCES sprint(id) ON DELETE SET NULL;

# -- Add missing columns to task table if needed
# ALTER TABLE task ADD COLUMN IF NOT EXISTS estimation_unit estimationunit DEFAULT 'HOURS';

# -- Update existing users to have default values
# UPDATE "user" SET 
#     timezone = 'UTC' WHERE timezone IS NULL,
#     daily_work_hours = 8.0 WHERE daily_work_hours IS NULL,
#     is_active = true WHERE is_active IS NULL;