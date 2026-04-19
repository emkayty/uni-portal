import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  transpilePackages: ['@university/ui', '@university/api-client'],
};

export default nextConfig;