#!/usr/bin/env node

import fs from 'node:fs/promises';
import process from 'node:process';

function parseArgs(argv) {
  const args = {
    input: null,
  };

  for (let i = 2; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === '--input' && argv[i + 1]) {
      args.input = argv[i + 1];
      i += 1;
      continue;
    }
    if (token === '--help' || token === '-h') {
      args.help = true;
    }
  }

  return args;
}

function percentile(sortedValues, p) {
  if (sortedValues.length === 0) return null;
  if (sortedValues.length === 1) return sortedValues[0];
  const index = (sortedValues.length - 1) * p;
  const lower = Math.floor(index);
  const upper = Math.ceil(index);
  if (lower === upper) return sortedValues[lower];
  const weight = index - lower;
  return sortedValues[lower] * (1 - weight) + sortedValues[upper] * weight;
}

function summarize(values) {
  const numeric = values.filter((value) => Number.isFinite(value));
  if (numeric.length === 0) {
    return {
      count: 0,
      avg: null,
      min: null,
      p50: null,
      p95: null,
      max: null,
    };
  }

  const sorted = [...numeric].sort((a, b) => a - b);
  const sum = numeric.reduce((acc, value) => acc + value, 0);

  return {
    count: numeric.length,
    avg: Number((sum / numeric.length).toFixed(2)),
    min: sorted[0],
    p50: Number(percentile(sorted, 0.5).toFixed(2)),
    p95: Number(percentile(sorted, 0.95).toFixed(2)),
    max: sorted[sorted.length - 1],
  };
}

function printUsage() {
  console.log([
    'Usage:',
    '  node tools/metrics/summarize-metrics.mjs --input <report.json>',
    '',
    'Expected input shape:',
    '  { schemaVersion, generatedAt, runs: [{ renderTimeMs: [...], ... }] }',
  ].join('\n'));
}

const args = parseArgs(process.argv);
if (args.help || !args.input) {
  printUsage();
  process.exit(args.help ? 0 : 1);
}

const raw = await fs.readFile(args.input, 'utf8');
const report = JSON.parse(raw);
const output = {
  schemaVersion: 1,
  source: args.input,
  generatedAt: new Date().toISOString(),
  build: report.build ?? null,
  environment: report.environment ?? null,
  runs: [],
};

for (const run of report.runs ?? []) {
  output.runs.push({
    label: run.label ?? 'unnamed',
    samples: run.samples ?? null,
    renderTimeMs: summarize(run.renderTimeMs ?? []),
    encodeTimeMs: summarize(run.encodeTimeMs ?? []),
    networkLatencyMs: summarize(run.networkLatencyMs ?? []),
    frameDeliveryLatencyMs: summarize(run.frameDeliveryLatencyMs ?? []),
    inputToVisibleLatencyMs: summarize(run.inputToVisibleLatencyMs ?? []),
    notes: run.notes ?? null,
  });
}

process.stdout.write(`${JSON.stringify(output, null, 2)}\n`);
