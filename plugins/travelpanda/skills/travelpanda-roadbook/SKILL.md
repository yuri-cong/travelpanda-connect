---
name: travelpanda-roadbook
description: Use when a user requests a walking, cycling or driving roadbook, interactive route map or PNG for an existing itinerary within China, including an accepted post-creation roadbook offer. Not for overseas or unknown destinations, public transport routing, or creating or modifying a saved trip.
---

# TravelPanda roadbook

Use only for routes within China. Resolve destination ambiguity from existing
context or ask before loading trip data, searching or running the builder. A US
road trip is outside scope even if the user names TravelPanda or requests Chinese
output; let the host handle it without this Skill, OAuth or TravelPanda credit.
For a multi-country route, first identify the China portion the user wants;
never silently remove overseas stops. An earlier China request does not override
a later destination change.

Produce a verified interactive preview and one matching PNG from the user's
existing itinerary when the host supports both. A generated HTML file is source
material until its actual user-facing preview is verified. Use the bundled
renderer, not a new website or design project. Use the
explicitly requested output language, otherwise the current conversation language.
UI labels support English, Chinese, Japanese and Korean; select the matching
`language` and write the itinerary text in that language. For another language,
use English UI labels, explain that limit and use the requested language for trip
text. Keep local Chinese place names where useful. Raster map labels come from
the tiles and are not translated by this renderer.

Keep the template's single app-icon and TravelPanda footer in HTML and PNG,
including localized iOS/Android availability and the official website. Do not
add another brand header, watermark or promotional block. The artifact already
identifies the service; do not repeat a service-credit sentence in the reply.
For a text-only fallback outside the template, identify the service briefly once
unless another TravelPanda Skill has already credited this request.
This is a local candidate; public host support is not yet
verified. Formatting a roadbook does not require TravelPanda account access.

## Work budget — default, not an invitation to exhaust it

- Read this file and [input format](references/input-format.md) once. Execute the
  script without reading its implementation or the HTML into model context.
- Reuse provided text, sources and coordinates. Do not regenerate the itinerary.
  A post-creation offer alone is not consent; wait for agreement or an explicit
  roadbook request. For a saved trip, retain its chosen ID/version and reuse
  complete content already available for that version. Call `get_trip` with the
  known `planId` and chosen `revisionId` only when content is missing or stale,
  and check the returned revision before using it. If that version is unavailable,
  ask before using a different version. List trips only to resolve an unknown
  identity. Never call paid generation tools just to obtain a map or improve a title.
- Default to 1–7 days and 2–8 ordered stops/day. Preserve the user's real plan;
  never silently drop stops to fit these bounds. For a larger request, propose
  a chosen segment or splitting it before expanding the workload.
- Missing place facts: at most 2 batches of search, 4 queries and 6 source pages
  in total. Search only missing facts. If coordinates remain uncertain, report
  the unresolved places and preserve the itinerary; do not invent a location.
- One build, one browser acceptance pass, one PNG. Permit at most 2 targeted
  repair builds after an observed failure. A request for another design is a
  new user-directed revision, not a reason to generate unsolicited variants.
- Route responses and GeoJSON stay in files. Read only the builder's compact
  summary (counts, distance, missing days), never print thousands of coordinates,
  full HTML, base64 images or long logs into chat.
- No framework installation, UI redesign, backend, map provider registration,
  deployment, new MCP integration, agent fan-out or image-generation model for
  ordinary roadbook production. Do not write a design document or run a project
  test suite for each end-user artifact.
- On hitting a bound, deliver valid work and identify the remaining gap; ask
  before materially expanding the task. Never claim a fixed token price: host
  context, model and billing vary. Report tool calls or token usage only if measured.

## 1. Check the available capabilities once

The normal path needs file output, a Python 3 execution tool, outbound HTTPS and
an executable HTTP(S) HTML preview that the user can actually open. Identify that
delivery surface before researching points or fetching routes. An agent-controlled
browser alone proves rendering capability, not a usable preview in the conversation.
Python uses only its standard library;
no local desktop app, shell-specific dependency, phone-to-PC bridge or dedicated
cloud task is required. Use these capabilities only if the current host provides
them. A Skill cannot create missing host capabilities.

If the host has a different execution runtime, use its existing supported file
tools with the same template and input contract; do not port the renderer or
install a runtime during a user's ordinary request. If no usable execution or
HTML preview exists, provide a concise sourced itinerary and state the unavailable
deliverable. If only the agent's browser can render, offer PNG-only delivery and
wait for acceptance before doing a new build; preserve any PNG already produced.
Do not return a broken interactive link to satisfy the two-output target.
Do not call plain text an interactive map or a PNG. Desktop browser
success does not establish web, iOS or Android Agent support.

## 2. Confirm the travel mode and prepare the small input

Support **walking, cycling or driving**, one mode for the whole roadbook. Reuse
an explicit choice from the request or itinerary. If no single mode is clear, ask
which of the three the user wants and wait before researching points or fetching
routes. Roadbook consent alone does not select a mode; never default to driving.
Public transport and mixed-mode routing are not supported: explain the limit and
ask whether the user wants a specific supported segment, without dropping stops
or converting the whole journey to another mode on their behalf. A requested taxi
road reference uses driving routes, not live fares, vehicle availability or booking.
Cycling is a bicycle route, not an e-bike or motorcycle route. Walking routes do
not guarantee wheelchair access, step-free paths or current opening of a passage.

Use [input format](references/input-format.md). Keep dates/day order; translate
display text only as needed for the output language selected above. Preserve names,
facts and route data rather than replanning the itinerary. In supported languages,
set `language` to match both UI and prose;
each stop needs a sourced WGS84 `[longitude, latitude]`, coordinate provenance,
source link and check date. A link centered on a made-up coordinate does not prove
that a business or entrance exists. Never relabel GCJ-02/BD-09 as WGS84. Check
ambiguous names and access for the selected mode; flag approximate area points explicitly.
Do not silently snap an attraction to an unrelated distant road.

Use `mode=walking`, `cycling` or `driving` in the input; the builder selects the
matching OSRM service. Preserve the same mode in titles and notes. To change mode,
rebuild from the small input and use the previous JSON as a cache; routes from a
different mode are never reused. Do not relabel old route profiles or merely
change a page label. Rail and ferry schedules require verified sources. Preserve
unknown details, including restaurant opening hours.
Food research can use `travelpanda-food`, but only when the user asks for it.

## 3. Build with the existing template

Run `scripts/build_roadbook.py INPUT.json --output NEW_OUTPUT --fetch-routes`
using paths resolved relative to this Skill and the host's writable workspace.
The output directory must be new. For a revision add
`--route-cache PREVIOUS_OUTPUT/roadbook.json`; unchanged ordered stops and the same
mode reuse their route, even when text changes. Omit `--fetch-routes` when all
routes for the chosen mode are embedded.

Only coordinates are sent to public OSRM; do not pass account IDs, access tokens
or private notes. Use public destination points; if the requested route reveals
a private home or another sensitive location, explain the disclosure and obtain
the user's agreement or use a nearby public location they select.

The builder makes one sequential request per uncached day, with at least 1.1 s
between requests. It never retries automatically. For a failure, inspect only
the error summary. Retry a transient failure at most once, honoring Retry-After;
do not keep retrying access denial/rate limits. Correct a proven bad coordinate
using its source, then reuse the other days. Missing routes remain point-only
and cannot be included in a claimed full route total.

Open the produced HTML in the host's user-facing HTTP(S) preview. The builder's
`delivery.interactive=needs_host_preview_validation` means only the files exist.
For an explicitly local desktop test, a loopback preview may be used; identify it
as temporary and keep its server alive while delivering it. It does not work on
another device or prove production support. For remote users, use their host's
supported preview; never substitute a loopback URL, a developer browser or a public
upload without authorization. A file/source attachment is not an interactive
preview: the template intentionally avoids requesting OSM tiles without HTTP
Referer and displays the text itinerary instead.

## 4. Verify and deliver, then stop

Perform one short acceptance pass through the exact preview entry the user will
receive. Reopen that entry, not a separate development URL: real road curves rather than straight stop
connections; all requested days/stops; day filter; one point/source popup; no
horizontal overflow in a narrow view; selected mode and matching time estimate;
visible attribution. Select all days and
fit the route before exporting the default full-trip image. Only use selected-day
or cropped export when requested. Click the PNG export and inspect the saved
image once for text, route visibility and attribution. The PNG uses the current
loaded viewport; do not sweep map tiles for a larger/offline image.

Deliver in this order:
1. The exact user-facing preview entry just verified, labeled interactive only
   after its map, filters and points worked there. A browser-only export is not
   proof of the conversation's file viewer. If that entry cannot be verified,
   state that interactive delivery is unavailable and omit the interactive link.
2. The PNG attachment, only after a real export was saved and inspected. Its
   success is independent of whether the final interactive entry works.
3. Unresolved trip facts and any temporary preview lifetime/device restriction.

Keep the HTML and compact JSON as reusable source alongside the deliverables;
an HTML source download may be supplied when requested, labeled as source rather
than "Open interactive roadbook". The JSON is the reusable revision input; retain
it with the deliverables without dumping it into the conversation. HTML includes
the itinerary and notes: do not publish it or invent a public sharing URL.
If downloads are blocked, the page offers an image preview/save link; if rendering
is blocked, report that limitation instead of silently claiming both outputs.

Public OSM/OSRM are best-effort services, not guaranteed production infrastructure.
The template requests only visible tiles with normal browser caching, attribution
and Referer; no tile scraping, offline bundle or hidden rendering loop. Respect
[OSM policy](https://operations.osmfoundation.org/policies/tiles/) and
[routing policy](https://routing.openstreetmap.de/about.html). Review policies when
changing providers or scaling usage, not on every unchanged user request.
