# TravelPanda Connect

Official TravelPanda MCP integration and agent skills for travel in China.

This repository contains the plugin and its supporting resources. The hosted
TravelPanda service is separate. Connect with your TravelPanda account and
review the requested permissions and connection allowance in your browser.

## Install

In a compatible Codex host, add this Git repository as a plugin source:
https://github.com/yuri-cong/travelpanda-connect

Select the **TravelPanda** plugin from **TravelPanda Connect**, install it, and
complete the host's normal OAuth sign-in when connecting your account. Never
paste passwords, session cookies or access tokens into a chat. Host support
varies; see [TravelPanda](https://travelpanda.ai/agents/) for service information.

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
