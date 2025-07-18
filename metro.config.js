const { getDefaultConfig } = require('expo/metro-config');
const { execSync } = require('child_process');

function getGitCommitHash() {
  try {
    return execSync('git rev-parse HEAD', { encoding: 'utf8' }).trim();
  } catch (error) {
    console.warn('Could not get git commit hash:', error.message);
    return 'unknown';
  }
}

/** @type {import('expo/metro-config').MetroConfig} */
const config = getDefaultConfig(__dirname);

// Add wasm asset support
config.resolver.assetExts.push('wasm');

// Add build-time constants via environment variables that Metro will pick up
process.env.EXPO_PUBLIC_COMMIT_HASH = getGitCommitHash();
process.env.EXPO_PUBLIC_BUILD_DATE = new Date().toISOString();

console.log(`📦 Metro: Injected git commit ${process.env.EXPO_PUBLIC_COMMIT_HASH.slice(0, 7)}`);

// Add COEP and COOP headers to support SharedArrayBuffer
config.server.enhanceMiddleware = (middleware) => {
  return (req, res, next) => {
    res.setHeader('Cross-Origin-Embedder-Policy', 'credentialless');
    res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
    middleware(req, res, next);
  };
};

module.exports = config;
