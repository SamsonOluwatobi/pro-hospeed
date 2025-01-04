"""initial migration

Revision ID: initial_migration
Revises: 
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create User table
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=64), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=128)),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('user_type', sa.String(length=20), nullable=False),
        sa.Column('specialization', sa.String(length=100), nullable=True),
        sa.Column('license_number', sa.String(length=50), nullable=True),
        sa.Column('clinic_address', sa.String(length=200), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    # Create Schedule table
    op.create_table('schedule',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('doctor_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('is_available', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['doctor_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create Appointment table
    op.create_table('appointment',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('doctor_id', sa.Integer(), nullable=False),
        sa.Column('patient_id', sa.Integer(), nullable=False),
        sa.Column('schedule_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(length=20), default='pending'),
        sa.Column('symptoms', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['doctor_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['patient_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['schedule_id'], ['schedule.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create Referral table
    op.create_table('referral',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('patient_id', sa.Integer(), nullable=False),
        sa.Column('referring_doctor_id', sa.Integer(), nullable=False),
        sa.Column('referred_doctor_id', sa.Integer(), nullable=False),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), default='pending'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['patient_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['referring_doctor_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['referred_doctor_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('referral')
    op.drop_table('appointment')
    op.drop_table('schedule')
    op.drop_table('user') 