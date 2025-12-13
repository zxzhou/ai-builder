/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Enable standalone output for Docker deployment
  output: 'standalone',
  // Ensure environment variables are available at runtime
  env: {
    AI_BUILDER_TOKEN: process.env.AI_BUILDER_TOKEN,
  },
}

module.exports = nextConfig

