const fs = require('fs');

const html = fs.readFileSync('C:/Users/ADMIN/Downloads/iee_government_portal (3).html', 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]);

const results = scripts.map((script, index) => {
  try {
    new Function(script);
    return { script: index + 1, ok: true, length: script.length };
  } catch (error) {
    return { script: index + 1, ok: false, error: error.message };
  }
});

console.log(JSON.stringify({ scriptCount: scripts.length, results }, null, 2));
if (results.some((result) => !result.ok)) {
  process.exit(1);
}
