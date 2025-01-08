-- Add is_verified column to user table
ALTER TABLE "user" ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT FALSE;

-- Update existing users to have is_verified as true (optional)
UPDATE "user" SET is_verified = TRUE WHERE is_verified IS NULL; 