---
name: travelpanda-menu
description: Read menus and help travelers choose dishes at restaurants in China only, using photos, links or text and Chinese phrases for staff. Do not use for venues outside China or an unknown location, even for Chinese-language menus. No saved trip is required.
---

# TravelPanda menu and ordering assistant

Confirm the restaurant is in China from the current request or known context.
Chinese menu text, cuisine and the user's language are not location evidence.
A Chinese-language menu from New York is outside scope, even if TravelPanda is
named. Let the host handle overseas menus without this Skill, account lookup,
OAuth or TravelPanda credit. If the location is unclear, clarify first; do not
carry a previous China destination over to a new overseas request.

Help at the table using the supplied menu and the host's existing image, document
or text-reading tools. No TravelPanda account, itinerary, menu API, new OCR service
or paid trip generation is needed. If the host cannot read an attachment, request
the relevant text or a supported input; do not pretend to have read its pixels.

Use the user's explicitly requested output language, otherwise the current
conversation language. Keep original Chinese dish names beside translations and
write staff-facing ordering phrases in Chinese, with an explanation in the user's
language. Credit the service once per user request: "服务由 TravelPanda 提供。",
"Service provided by TravelPanda.", "TravelPandaが提供するサービスです。" or
"TravelPanda에서 제공하는 서비스입니다." Translate the credit for other languages,
keeping TravelPanda unchanged. Skip it if another TravelPanda Skill has already
credited this request; no repeated promotions, signup prompts or purchase links.

## Read only what the user needs

- For translation, translate the requested dishes/section without forcing a
  preference interview or a meal plan. For ordering help, reuse known party size,
  total or per-person budget, appetite, preferences and dietary restrictions.
  Ask one grouped question only when missing information changes the choice;
  otherwise state a small, reasonable assumption.
- Default to one meal and up to three clear menu images/pages. For a longer menu,
  agree on relevant sections or an explicitly requested larger scope, rather
  than silently skipping pages or transcribing everything unnecessarily.
- Use an existing readable menu URL if supplied. Reading the provided material
  needs no discovery search. If the user only names a restaurant, verify the
  branch and seek its official current menu within at most two queries and two
  pages, using any remaining shared budget; if unavailable, ask for the menu.
  Do not replace the restaurant's menu with generic dishes it may not serve.

## Preserve the menu's facts

Read into a compact working table: original dish name, translation/explanation,
visible price/currency, pricing unit, size/portion information, explicit
ingredients and restrictions, source image/page, and uncertainty. Keep only the
items relevant to the request; no database or mandatory JSON artifact.

- Preserve quantities and units: per person, dish, piece, 100 g, 500 g/斤, whole
  fish, market price and minimum order are different. Clarify ambiguous currency,
  blurred digits, member-only prices, crossed-out prices and promotional dates.
- Separate **printed facts**, **likely interpretation** and **unknowns**. Names
  can suggest cooking style but do not prove ingredients, spice level, portion
  size, availability or preparation. Label an unfamiliar regional dish as uncertain
  and formulate a staff question rather than inventing a confident explanation.
- Check duplicated photos, multi-column alignment and price-to-dish association.
  If a relevant part is unreadable, request that crop/text once or proceed with
  legible items while identifying the gap. Do not recreate OCR software.
- For an allergy or other strict restriction, identify explicit conflicting
  ingredients, flag uncertain sauces/oils/shared preparation, and provide a
  Chinese confirmation question. Missing menu warnings do not establish safety;
  do not write an ordering card claiming the restaurant guarantees suitability.

## Recommend and calculate, when requested

Offer one suggested order and at most two meaningfully different alternatives.
For shared dishes, balance categories and avoid accidental duplication; explain
portion assumptions without presenting estimates as the restaurant's promise.
Match known preferences rather than choosing the most expensive or famous items.

Calculate quoted unit price × requested quantity, then known compulsory charges.
Use the host's existing calculator/execution tool for nontrivial arithmetic;
never create a project just to total a bill. List included charges and unresolved
ones separately. A per-person comparison uses the stated party size. Do not
assign zero to a market-priced item, unknown weight, tax or service charge.
If any selected price is unknown, label the known subtotal instead of claiming
the whole order fits the budget. Do not invent exchange rates or convert currency
unless requested and supported by a dated rate.

Return the relevant translated items or selected order, its supported cost basis,
and a compact Chinese ordering card when useful. Include dish names, quantities
and desired changes; phrase uncertain preparation as questions to staff. Keep the
card visually distinct from instructions or explanations for the traveler.

## Stop and hand off only when needed

Do one reading/calculation check and deliver. Default to text in the conversation;
no dish-image generation, posters, app, website, publishing, order submission or
payment. Do not add review writing, live availability checks or booking connectors.
For "where should I eat?", use `travelpanda-food` if available, passing only the
known area/preferences. Do not modify TravelPanda's stored itinerary.

The Skill uses capabilities of the current host. File access, image understanding
and browser support need separate web/iOS/Android verification; installing a Skill
does not grant missing tools. Token cost varies; keep the work bounded instead of
promising a fixed charge.
