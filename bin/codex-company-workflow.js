#!/usr/bin/env node
const { spawnSync } = require('node:child_process');
const path = require('node:path');

const rootDir = path.resolve(__dirname, '..');
const args = process.argv.slice(2);
const command = args[0];
const passthrough = args.slice(1);
const installSh = path.join(rootDir, 'scripts', 'install.sh');
const installPs1 = path.join(rootDir, 'scripts', 'install.ps1');

function printUsage() {
  console.log(`Usage:
  codex-company-workflow install-plugin [--lang zh|en] [--force]
  codex-company-workflow uninstall-plugin [--lang zh|en|--all]
  codex-company-workflow bootstrap-project <project-path> [--lang zh|en] [--force]
  codex-company-workflow deactivate-project <project-path> [--force]
  codex-company-workflow update-templates <project-path> [--lang zh|en] [--force]
  codex-company-workflow generate-index <project-path> [--lang zh|en] [--force]
  codex-company-workflow expert-preflight <project-path> [--lang zh|en]
  codex-company-workflow all <project-path> [--lang zh|en] [--force]
  codex-company-workflow verify [--lang zh|en]
`);
}

function run(commandName, commandArgs) {
  const result = spawnSync(commandName, commandArgs, { stdio: 'inherit' });
  if (result.error) {
    throw result.error;
  }
  process.exit(result.status ?? 0);
}

if (!command || command === '--help' || command === '-h' || command === 'help') {
  printUsage();
  process.exit(0);
}

if (process.platform === 'win32') {
  const shells = ['powershell', 'pwsh'];
  let lastError = null;
  for (const shell of shells) {
    const result = spawnSync(shell, ['-ExecutionPolicy', 'Bypass', '-File', installPs1, command, ...passthrough], {
      stdio: 'inherit',
    });
    if (!result.error) {
      process.exit(result.status ?? 0);
    }
    lastError = result.error;
  }
  throw lastError || new Error('Unable to find PowerShell');
}

run('bash', [installSh, command, ...passthrough]);
