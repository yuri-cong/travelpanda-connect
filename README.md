# TravelPanda Connect

Official TravelPanda MCP integration and agent skills for travel in China.

This repository contains the plugin and its supporting resources. The hosted
TravelPanda service is separate. Connect with your TravelPanda account and
review the requested permissions and connection allowance in your browser.

## Ask your AI to help you connect

Copy this message into your AI assistant:

> Please read the official guide at https://github.com/yuri-cong/travelpanda-connect and help me install or connect TravelPanda using the setup method this AI assistant supports. Guide me through signing in and let me know when the connection is ready. If you need me to do anything, walk me through it step by step.

中文：把下面这段话复制给你正在使用的 AI 助手：

> 请阅读 https://github.com/yuri-cong/travelpanda-connect 的官方说明，按照当前 AI 助手支持的方式，帮我安装或连接 TravelPanda，并引导我完成登录。连接完成后，请告诉我可以开始使用了。需要我操作时，请一步一步告诉我怎么做。

Complete sign-in and review access on the TravelPanda page in your browser.
You do not need to send your password to the assistant or create a GitHub account.

### Do I need to set anything up myself?

Some assistants can install connections for you; others guide you through
their settings. Send the message above to your assistant and follow its
instructions. You complete sign-in and review access in your browser.
See [TravelPanda](https://travelpanda.ai/agents/) for service information.

### Prefer to set up Codex yourself?

In a Codex version that supports plugins, run these two lines:

```bash
codex plugin marketplace add https://github.com/yuri-cong/travelpanda-connect
codex plugin add travelpanda@travelpanda-connect
```

Then follow the sign-in prompt in your assistant. Once connected, tell your
assistant what you would like to do. If you already installed TravelPanda, use the
existing connection instead of adding another one.

<details>
<summary>For assistants helping with setup</summary>

- Read the connection instructions before changing settings. Use the current
  host's supported installation flow and preserve unrelated connections.
- The hosted MCP address is `https://api-sg.travelpanda.ai/agent/mcp`.
  Account access currently requires a registered OAuth client; dynamic client
  registration is not enabled. A remote MCP address alone is not a complete
  setup for an unregistered host. Do not reuse Codex's client identity in
  another assistant or invent a compatible plugin format.
- If this host cannot install or connect, explain that briefly and offer the
  Codex option above. Do not claim setup succeeded just because files were
  downloaded.
- Use the host's normal browser sign-in. The user completes login and reviews
  permissions and the connection allowance. Never ask for passwords, session
  cookies or access tokens in the conversation.
- After authorization, confirm the connection using the host's connection status
  or a minimal read-only account check, then let the user know it is ready.
  A new account does not need any saved trips. Do not list trips or start planning
  unless the user asks. Installing the plugin does not authorize a paid trip request.

</details>

## Capabilities

- Read, create and preview changes to saved China itineraries. Generation uses
  Bamboo; review the quoted usage and confirm before starting.
- Create Chinese directions and taxi cards, including image export where the
  host supports it.
- Find restaurants and interpret menus using the host's research tools.
- Build walking, cycling or driving roadbooks from an existing China itinerary.
  Routing and map tiles use OpenStreetMap services and their usage policies.

Public transport and mixed-mode routing, bookings and payments are not supported.
Interactive maps require a host that runs the page scripts and loads map
dependencies. A successfully generated PNG does not guarantee an interactive
preview in every host. Python 3 is needed to run the roadbook builder locally.

## Development and checks

This is a generated distribution repository. Changes are reviewed upstream and
exported as an explicit set of files, without the application's commit history.
Run `node --test tests/plugin.test.mjs` to check the distributed plugin structure.
Report issues here without including account data, credentials or private trips.

Plugin source: MIT; the hosted service has separate
[terms](https://account.travelpanda.ai/terms-of-service) and
[privacy information](https://travelpanda.ai/agents/#privacy).
Contact: support@travelpanda.ai.
