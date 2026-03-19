#!/usr/bin/env node

import process from 'node:process';
import { setTimeout as sleep } from 'node:timers/promises';
import WebSocket from 'ws';

function parseArgs(argv) {
  const args = {
    url: null,
    count: 20,
    burstSize: 5,
    intervalMs: 250,
    timeoutMs: 5000,
    text: 'burst-input',
  };

  for (let i = 2; i < argv.length; i += 1) {
    const token = argv[i];
    const next = argv[i + 1];
    if (token === '--url' && next) {
      args.url = next;
      i += 1;
      continue;
    }
    if (token === '--count' && next) {
      args.count = Number(next);
      i += 1;
      continue;
    }
    if (token === '--burst-size' && next) {
      args.burstSize = Number(next);
      i += 1;
      continue;
    }
    if (token === '--interval-ms' && next) {
      args.intervalMs = Number(next);
      i += 1;
      continue;
    }
    if (token === '--timeout-ms' && next) {
      args.timeoutMs = Number(next);
      i += 1;
      continue;
    }
    if (token === '--text' && next) {
      args.text = next;
      i += 1;
      continue;
    }
    if (token === '--help' || token === '-h') {
      args.help = true;
    }
  }

  return args;
}

function printUsage() {
  console.log([
    'Usage:',
    '  node tools/control-burst-input.mjs --url ws://localhost:8080/ws [--count 20] [--burst-size 5]',
    '',
    'Options:',
    '  --text <value>       Payload text sent with each message',
    '  --interval-ms <n>    Pause between bursts',
    '  --timeout-ms <n>     Close the test if no ack arrives within the timeout',
  ].join('\n'));
}

const args = parseArgs(process.argv);
if (args.help || !args.url) {
  printUsage();
  process.exit(args.help ? 0 : 1);
}

const state = {
  sent: 0,
  acked: 0,
  samples: [],
};

const pending = new Map();
let closed = false;
let sendsDone = false;

const ws = new WebSocket(args.url);

function finish(code, message) {
  if (closed) return;
  closed = true;
  if (message) {
    console.log(message);
  }
  const missing = pending.size;
  const avg = state.samples.length
    ? state.samples.reduce((acc, value) => acc + value, 0) / state.samples.length
    : null;
  const sorted = [...state.samples].sort((a, b) => a - b);
  const p95 = sorted.length
    ? sorted[Math.min(sorted.length - 1, Math.ceil(sorted.length * 0.95) - 1)]
    : null;
  console.log(JSON.stringify({
    url: args.url,
    sent: state.sent,
    acked: state.acked,
    missing,
    avgAckLatencyMs: avg == null ? null : Number(avg.toFixed(2)),
    p95AckLatencyMs: p95,
  }, null, 2));
  ws.close();
  process.exit(code);
}

ws.on('open', async () => {
  for (let burst = 0; burst < args.count; burst += 1) {
    for (let i = 0; i < args.burstSize; i += 1) {
      const id = `${Date.now()}-${burst}-${i}`;
      const sentAt = Date.now();
      pending.set(id, sentAt);
      state.sent += 1;
      ws.send(JSON.stringify({
        type: 'control-input',
        id,
        text: args.text,
        sequence: state.sent,
        sentAt,
      }));
    }
    if (burst < args.count - 1) {
      await sleep(args.intervalMs);
    }
  }

  sendsDone = true;
  const deadline = Date.now() + args.timeoutMs;
  while (Date.now() < deadline) {
    if (pending.size === 0) {
      finish(0, 'Burst test finished.');
      return;
    }
    await sleep(50);
  }

  finish(2, 'Burst test timed out waiting for acknowledgements.');
});

ws.on('message', (data) => {
  let payload;
  try {
    payload = JSON.parse(data.toString());
  } catch {
    return;
  }

  const id = payload.id ?? payload.sequence ?? payload.ackId;
  if (!id || !pending.has(String(id))) {
    return;
  }

  const sentAt = pending.get(String(id));
  pending.delete(String(id));
  const latency = Date.now() - sentAt;
  state.acked += 1;
  state.samples.push(latency);
});

ws.on('error', (error) => {
  finish(1, `Websocket error: ${error.message}`);
});

ws.on('close', () => {
  if (!closed) {
    const code = sendsDone && pending.size === 0 ? 0 : 2;
    finish(code, 'Websocket closed.');
  }
});

process.on('SIGINT', () => finish(130, 'Interrupted.'));
