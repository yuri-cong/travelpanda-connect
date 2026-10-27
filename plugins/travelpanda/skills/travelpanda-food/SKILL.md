---
name: travelpanda-food
description: Find restaurants, compare branches or assess customer reviews for travel in China only. Do not use for venues outside China or an unknown location. No saved itinerary is needed; use travelpanda-menu for menus at venues in China.
---

# TravelPanda restaurant assistant

Use only for venues in China, based on the current request or known location
context. Chinese cuisine, Chinese text and the user's nationality do not establish
location. A Chinese restaurant in New York is outside scope, even if TravelPanda
is named. Let the host handle overseas requests without this Skill, account
lookup, OAuth or TravelPanda credit. If the location is unclear, clarify first;
do not assume China from an earlier trip when the user changes destinations.

Help the user decide where to eat or whether a specific restaurant suits them.
Use the host's existing search/browser or supplied links, text and screenshots.
TravelPanda has no restaurant, review or availability MCP API. A saved trip,
account connection and precise GPS location are not prerequisites. Never call
paid trip generation, read an account or install a service for this workflow.

Use the explicitly requested output language, otherwise the current conversation
language. Keep the restaurant's Chinese name and branch/address alongside any
translated explanation so the user can find it locally. Identify the service
once per user request with a short localized credit, such as "服务由 TravelPanda
提供。" or "Service provided by TravelPanda." If another TravelPanda Skill has
already done so in this request, do not repeat it. No promotional paragraph,
signup requirement or purchase link; do not imply TravelPanda verified the venue
in person or supplies the underlying review platform's data.

## Choose only the relevant mode

- **Find food:** reuse the known city/area or landmark, meal time, party size,
  budget and preferences. Ask one grouped question only for missing information
  that would materially change the choice; an area is sufficient. If the user
  is undecided, suggest two suitable meal types before researching venues.
- **Compare named places:** resolve the supplied branches, then compare them.
  Do not run a new discovery search or add candidates unless requested or all
  supplied choices are unsuitable.
- **Read reviews:** for "is this place worth it?", recurring complaints or a
  review-based comparison, read [review assessment](references/reviews.md).
  A normal shortlist needs only a brief, supported reputation note; do not load
  this reference or launch deep review research by default.

## Resolve facts, then make the choice

1. Search only missing facts. Use the Chinese branch name plus city/area to avoid
   combining namesakes, moved premises or different chain branches. Deduplicate
   by branch and address, not just translated name. Prefer the business's current
   page for contact details, menu and hours; customer comments are opinions.
2. Keep a compact record: Chinese name/branch, city/address, source URL, check
   date, known price basis/currency, hours and their source, user-fit reasons,
   relevant concerns and unknowns. Retain original publication dates when shown;
   today's retrieval does not make an old review or menu current. Use a small
   table or existing host context, not a new database or mandatory file.
3. Separate per-person estimates, a quoted dish/set price and a verified meal
   total. Do not silently turn one into another. State conflicting facts briefly
   and prefer newer branch-specific evidence where it actually resolves them.
4. Prioritize the user's explicit constraints, then practical fit: cuisine,
   price, solo/group seating evidence, convenient area and suitable meal hours.
   Explain the tradeoff instead of inventing a composite numerical score. A high
   rating does not override a known mismatch; missing evidence is not a bad review.
5. Return up to three choices with branch/address, why it fits, supported cost
   basis, the important caveat and source. Name one best fit and a fallback when
   the evidence supports both. For a single-venue question, give a direct verdict
   with the main reasons instead of forcing a multi-restaurant table.

Hours do not prove a kitchen is serving, seats are available or a queue is short.
Say when these are unverified. An address does not establish exact walking time;
use a sourced distance/time or describe the area without inventing precision.
Dietary suitability needs ingredient/preparation evidence or staff confirmation.
Search snippets can identify leads but cannot prove current prices or live status.

## Bounded work and handoff

- Default shared ceiling for discovery, comparison and review work: two search
  batches, four queries, six opened pages, five candidates and three recommendations.
  Stop earlier once the decision has adequate support. Reuse facts across modes;
  switching to reviews does not reset the budget. A user-requested wider study
  can set a larger scope explicitly; do not silently omit requested venues.
- Read only relevant page sections, not whole review histories. No mass scraping,
  login bypass, background polling, agent fan-out, new integrations or frameworks.
  If access fails, provide the supported subset and name the missing evidence.
  Without search, use supplied material and disclose that it was not live-checked.
- For a supplied menu or a dish-selection question, use `travelpanda-menu` when
  available and pass only the chosen branch and known party/budget/preferences.
  For an explicitly requested map, use `travelpanda-roadbook` and verify WGS84
  coordinates separately. These handoffs share the current research budget.
- Keep recommendations in the conversation unless the user requests a file.
  No automatic maps, posters, collection website, itinerary changes, reminder,
  review-writing workflow, booking, availability integration or public posting.
  An availability request may receive a verified official contact/booking link,
  with a clear statement that this version has not checked live seats.

This is a local plugin candidate. Skill discovery and search/browser access vary
by host; desktop success does not establish independent web, iOS or Android support.
