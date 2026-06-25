/**
 * Global API Keys Loader for Node.js
 * Usage: require('/home/aditya/.config/global-apikeys/load_keys.js')
 * Or:   import '/home/aditya/.config/global-apikeys/load_keys.js'
 */
const fs = require('fs');
const path = require('path');
const KEYS_FILE = path.join(process.env.HOME, '.config/global-apikeys/keys.env');
try {
  const content = fs.readFileSync(KEYS_FILE, 'utf8');
  content.split('\n').forEach(line => {
    line = line.trim();
    if (!line || line.startsWith('#') || !line.includes('=')) return;
    const [key, ...rest] = line.split('=');
    const val = rest.join('=').trim().replace(/^["']|["']$/g, '');
    if (val && !process.env[key.trim()]) process.env[key.trim()] = val;
  });
} catch(e) { console.warn('[global-keys] Could not load keys:', e.message); }
module.exports = process.env;
