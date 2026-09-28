#!/usr/bin/env node
/**
 * Bundle + minify src/js/experience.js (imports breeds.js) → docs/js/experience.js
 */
const esbuild = require('esbuild');
const path = require('path');
const fs = require('fs');

const root = path.join(__dirname, '..');
const entry = path.join(root, 'src', 'js', 'experience.js');
const outDir = path.join(root, 'docs', 'js');
const outfile = path.join(outDir, 'experience.js');

async function build() {
  if (!fs.existsSync(entry)) {
    console.error('missing', entry);
    process.exit(1);
  }
  fs.mkdirSync(outDir, { recursive: true });
  await esbuild.build({
    entryPoints: [entry],
    outfile,
    bundle: true,
    minify: true,
    target: ['es2018'],
    format: 'iife',
    legalComments: 'none',
    logLevel: 'silent',
  });
  const kb = (fs.statSync(outfile).size / 1024).toFixed(1);
  console.log('bundled experience.js → docs/js/experience.js (' + kb + ' KB)');
}

build().catch((err) => {
  console.error(err);
  process.exit(1);
});
