import assert from 'node:assert/strict';
import {test} from 'node:test';
import {readFile, stat} from 'node:fs/promises';

const root = new URL('../', import.meta.url);
const json = async path => JSON.parse(await readFile(new URL(path, root), 'utf8'));

test('marketplace resolves the distributed plugin and its declared resources', async () => {
  const marketplace = await json('.agents/plugins/marketplace.json');
  assert.equal(marketplace.name, 'travelpanda-connect');
  assert.equal(marketplace.plugins.length, 1);
  const source = marketplace.plugins[0].source;
  assert.equal(source.source, 'local');
  assert.equal(source.path, './plugins/travelpanda');
  const manifest = await json('plugins/travelpanda/.codex-plugin/plugin.json');
  assert.equal(manifest.name, 'travelpanda');
  assert.match(manifest.version, /^\d+\.\d+\.\d+$/);
  for (const path of [manifest.mcpServers, manifest.interface.logo, manifest.interface.composerIcon,
    manifest.extensions['com.openai'].onboardingSkill]) {
    assert((await stat(new URL(`plugins/travelpanda/${path}`, root))).isFile());
  }
  for (const skill of ['travelpanda', 'travelpanda-food', 'travelpanda-menu', 'travelpanda-roadbook']) {
    const text = await readFile(new URL(`plugins/travelpanda/skills/${skill}/SKILL.md`, root), 'utf8');
    assert(text.startsWith('---\n'));
    assert(text.includes(`name: ${skill}`));
  }
});

test('connection uses the hosted service and requests no embedded credentials', async () => {
  const config = await json('plugins/travelpanda/.mcp.json');
  assert.deepEqual(Object.keys(config.mcpServers), ['travelpanda_plugin']);
  const server = config.mcpServers.travelpanda_plugin;
  assert.equal(server.url, 'https://api-sg.travelpanda.ai/agent/mcp');
  assert(!server.headers && !server.env && !server.command);
  assert.equal(server.extensions['com.openai'].auth.client.tokenEndpointAuthMethod, 'none');
  assert.equal(server.oauth.clientId, 'travelpanda-codex');
});
