import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import path from 'node:path';
import { test } from 'node:test';

const root = path.resolve(import.meta.dirname, '..');

function read(relativePath) {
  return readFileSync(path.join(root, relativePath), 'utf8');
}

function walkFiles(dir) {
  const absDir = path.join(root, dir);
  if (!existsSync(absDir)) return [];
  return readdirSync(absDir).flatMap((entry) => {
    const abs = path.join(absDir, entry);
    const rel = path.relative(root, abs);
    return statSync(abs).isDirectory() ? walkFiles(rel) : [rel];
  });
}

test('static site exposes the required public routes and navigation', () => {
  const routes = [
    ['site/index.html', 'AI Deployment & Readiness Advisor'],
    ['site/services/index.html', 'Services'],
    ['site/demo/index.html', 'Voice Demo'],
    ['site/contact/index.html', 'Contact'],
    ['site/case-studies/ask-capitano/index.html', 'Ask-Capitano']
  ];

  for (const [route, expectedText] of routes) {
    assert.equal(existsSync(path.join(root, route)), true, `${route} should exist`);
    const html = read(route);
    assert.match(html, new RegExp(expectedText), `${route} should mention ${expectedText}`);
    assert.match(html, /href="[^"]*services\/"/, `${route} should link to services`);
    assert.match(html, /href="[^"]*demo\/"/, `${route} should link to demo`);
    assert.match(html, /href="[^"]*contact\/"/, `${route} should link to contact`);
  }
});

test('site assets include a shared stylesheet and interaction script', () => {
  assert.equal(existsSync(path.join(root, 'site/assets/styles.css')), true);
  assert.equal(existsSync(path.join(root, 'site/assets/site.js')), true);
  const css = read('site/assets/styles.css');
  assert.match(css, /--color-ink:/);
  assert.match(css, /@media \(max-width: 760px\)/);
});

test('Hugging Face Space demo is documented and syntactically valid', () => {
  const required = [
    'spaces/voice-demo/app.py',
    'spaces/voice-demo/requirements.txt',
    'spaces/voice-demo/README.md',
    'spaces/voice-demo/.env.example'
  ];

  for (const file of required) {
    assert.equal(existsSync(path.join(root, file)), true, `${file} should exist`);
  }

  const app = read('spaces/voice-demo/app.py');
  assert.match(app, /ELEVENLABS_API_KEY/);
  assert.match(app, /gradio/);

  execFileSync('python3', ['-m', 'py_compile', path.join(root, 'spaces/voice-demo/app.py')]);
});

test('deployment docs and GitHub Pages workflow exist', () => {
  const required = [
    'README.md',
    'docs/deploy-github-pages.md',
    'docs/deploy-huggingface-space.md',
    '.github/workflows/pages.yml'
  ];

  for (const file of required) {
    assert.equal(existsSync(path.join(root, file)), true, `${file} should exist`);
  }

  assert.match(read('README.md'), /Ask-Capitano/);
  assert.match(read('docs/deploy-github-pages.md'), /GitHub Pages/);
  assert.match(read('docs/deploy-huggingface-space.md'), /Hugging Face/);
});

test('public files avoid old brand name and hard-coded secrets', () => {
  const oldBrand = ['Ask', 'Spark'].join(' ');
  const files = [
    ...walkFiles('site'),
    ...walkFiles('spaces'),
    ...walkFiles('docs'),
    'README.md',
    '.github/workflows/pages.yml'
  ].filter((file) => existsSync(path.join(root, file)));

  for (const file of files) {
    const body = read(file);
    assert.equal(body.toLowerCase().includes(oldBrand.toLowerCase()), false, `${file} should use Ask-Capitano branding`);
    assert.doesNotMatch(body, /sk-[A-Za-z0-9_-]{20,}/, `${file} should not contain OpenAI-style secrets`);
    assert.doesNotMatch(body, /xi-api-key\s*[:=]\s*["'][A-Za-z0-9_-]+/i, `${file} should not contain ElevenLabs secrets`);
  }
});

test('demo page ships a working in-browser voice demo (no key required)', () => {
  assert.equal(existsSync(path.join(root, 'site/assets/demo.js')), true, 'demo.js should exist');

  const demo = read('site/demo/index.html');
  assert.match(demo, /data-tts/, 'demo page should mount the in-browser demo');
  assert.match(demo, /assets\/demo\.js/, 'demo page should load demo.js');
  assert.match(demo, /id="tts-(speak|lang|voice|text)"/, 'demo page should expose the TTS controls');

  const js = read('site/assets/demo.js');
  assert.match(js, /speechSynthesis/, 'demo.js should use the Web Speech API');
  assert.match(js, /SpeechSynthesisUtterance/, 'demo.js should build an utterance');
  // The free in-browser path must never depend on a key or network secret.
  assert.doesNotMatch(js, /api[_-]?key/i, 'in-browser demo must not reference an API key');
});
