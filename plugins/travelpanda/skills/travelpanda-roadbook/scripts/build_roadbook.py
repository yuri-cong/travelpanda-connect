"""Build a roadbook with the Python standard library; never fetch map tiles."""
import argparse
import base64
from datetime import datetime, timezone
from html import escape
import json
import math
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ROUTERS = {
    "walking": "https://routing.openstreetmap.de/routed-foot/route/v1/foot/",
    "cycling": "https://routing.openstreetmap.de/routed-bike/route/v1/bike/",
    "driving": "https://routing.openstreetmap.de/routed-car/route/v1/driving/",
}
USER_AGENT = "TravelPandaRoadbook/0.1 (+https://travelpanda.ai; support@travelpanda.ai)"


class RoutingUnavailable(ValueError):
    """Stop the batch when the provider denies or limits access."""


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value, label, limit=300):
    require(isinstance(value, str) and 0 < len(value.strip()) <= limit,
            f"{label}: expected nonempty text, max {limit} characters")


def number(value):
    return type(value) in (int, float) and math.isfinite(value)


def coordinate(value):
    return (isinstance(value, list) and len(value) == 2 and
            all(number(v) for v in value) and
            -180 <= value[0] <= 180 and -85 <= value[1] <= 85)


def source_url(value):
    text(value, "source URL", 1000)
    parsed = urlsplit(value)
    require(parsed.scheme == "https" and parsed.hostname and
            not parsed.username and not parsed.password, "Sources require credential-free HTTPS URLs")


def valid_route(route, coordinates, mode):
    require(isinstance(route, dict), "Route must be an object")
    require(route.get("inputCoordinates") == coordinates, "Cached route does not match this day's stops")
    require(route.get("profile") == mode, "Route profile does not match the selected travel mode")
    source_url(route.get("source"))
    text(route.get("retrievedAt"), "route.retrievedAt", 80)
    geometry = route.get("geometry", {})
    require(isinstance(geometry, dict), "Geometry must be an object")
    points = geometry.get("coordinates", [])
    require(geometry.get("type") == "LineString" and isinstance(points, list) and
            2 <= len(points) <= 150000 and all(coordinate(p) for p in points), "Invalid road geometry")
    for key in ("distance", "duration"):
        require(number(route.get(key)) and route[key] >= 0, f"Invalid route {key}")
    snaps = route.get("snaps", [])
    require(isinstance(snaps, list) and len(snaps) == len(coordinates) and all(
        isinstance(s, dict) and coordinate(s.get("location")) and number(s.get("distance")) and 0 <= s["distance"] <= 200
        for s in snaps), "Missing or excessive road snapping (maximum 200 m)")


def validate(data):
    require(isinstance(data, dict), "Expected a JSON object")
    require(data.get("coordinateSystem") == "WGS84", "Coordinates must be sourced as WGS84, not GCJ-02/BD-09")
    require(data.get("mode") in tuple(ROUTERS), "Choose a travel mode: walking, cycling or driving")
    require(data.get("language") in ("zh-CN", "en", "ja", "ko"), "Supported languages: zh-CN, en, ja, ko")
    text(data.get("title"), "title", 90)
    text(data.get("subtitle"), "subtitle", 250)
    days = data.get("days")
    require(isinstance(days, list) and 1 <= len(days) <= 7, "Use 1-7 days per roadbook")
    for day in days:
        require(isinstance(day, dict), "Day must be an object")
        text(day.get("title"), "day.title", 90)
        text(day.get("note"), "day.note", 350)
        stops = day.get("stops")
        require(isinstance(stops, list) and 2 <= len(stops) <= 8, "Use 2-8 ordered stops per day")
        for stop in stops:
            require(isinstance(stop, dict), "Stop must be an object")
            text(stop.get("name"), "stop.name", 90)
            text(stop.get("note"), "stop.note", 250)
            text(stop.get("coordinateNote"), "stop.coordinateNote", 180)
            text(stop.get("checkedAt"), "stop.checkedAt", 40)
            require(coordinate(stop.get("coordinates")), "Stop coordinates must be [longitude, latitude]")
            source_url(stop.get("source"))
        coordinates = [s["coordinates"] for s in stops]
        if day.get("route"):
            valid_route(day["route"], coordinates, data["mode"])
    return data


def route_day(day, mode):
    require(mode in tuple(ROUTERS), "Choose a travel mode: walking, cycling or driving")
    coordinates = [stop["coordinates"] for stop in day["stops"]]
    path = ";".join(",".join(f"{n:.6f}" for n in point) for point in coordinates)
    query = "?overview=full&geometries=geojson&steps=false&radiuses=" + ";".join(["200"] * len(coordinates))
    # Each transport mode needs its own prepared graph, not just a different URL profile label.
    request = Request(ROUTERS[mode] + path + query, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=25) as response:
            raw = response.read(8_000_001)
            require(len(raw) <= 8_000_000, "Route response too large")
            result = json.loads(raw)
    except HTTPError as error:
        detail = error.read(1000).decode("utf-8", errors="replace")
        if error.code in (401, 403, 429):
            raise RoutingUnavailable(
                f"OSRM HTTP {error.code}; batch stopped. Retry-After: {error.headers.get('Retry-After', 'unspecified')}"
            ) from error
        raise ValueError(f"OSRM HTTP {error.code}: {detail}") from error
    require(result.get("code") == "Ok" and result.get("routes"), f"OSRM: {result.get('code', 'invalid response')}")
    first = result["routes"][0]
    route = {
        "inputCoordinates": coordinates, "profile": mode,
        "source": "https://routing.openstreetmap.de/about.html",
        "retrievedAt": datetime.now(timezone.utc).isoformat(),
        "geometry": first["geometry"], "distance": first["distance"], "duration": first["duration"],
        "snaps": [{"location": p["location"], "distance": p["distance"]} for p in result["waypoints"]],
    }
    valid_route(route, coordinates, mode)
    return route


def render(data):
    validate(data)
    template = (Path(__file__).resolve().parent.parent / "assets" / "roadbook.html").read_text(encoding="utf-8")
    # JSON data must not be able to close its inert script element.
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    payload = payload.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    require(template.count("__ROADBOOK_DATA__") == 1, "Missing/duplicate template data slot")
    # Hosts may disable scripts. Preserve readable text without exposing unescaped input.
    notice = {
        "zh-CN": "此预览无法运行交互地图。以下为行程文字版；请使用对话中的交互预览入口或 PNG 图片。",
        "en": "This preview cannot run the interactive map. Read the itinerary below, or use the conversation's interactive preview or PNG.",
        "ja": "このプレビューでは地図を操作できません。以下の旅程、会話内の地図プレビュー、またはPNGをご利用ください。",
        "ko": "이 미리보기에서는 지도를 실행할 수 없습니다. 아래 일정 또는 대화의 지도 미리보기나 PNG를 이용하세요.",
    }[data["language"]]
    fallback = f'<section class="text-fallback"><h1>{escape(data["title"])}</h1><p>{escape(data["subtitle"])}</p><p>{notice}</p>'
    for day in data["days"]:
        fallback += f'<article><h2>{escape(day["title"])}</h2><p>{escape(day["note"])}</p><ol>'
        for stop in day["stops"]:
            fallback += (f'<li><strong>{escape(stop["name"])}</strong><p>{escape(stop["note"])}</p>'
                         f'<small>{escape(stop["coordinateNote"])} · {escape(stop["checkedAt"])}</small>'
                         f'<a href="{escape(stop["source"], quote=True)}" target="_blank" rel="noopener">{escape(stop["source"])}</a></li>')
        fallback += '</ol></article>'
    fallback += '</section>'
    platform = {"zh-CN": "支持 iOS 与 Android", "en": "Available on iOS & Android",
                "ja": "iOS・Android 対応", "ko": "iOS 및 Android 지원"}[data["language"]]
    icon = (Path(__file__).resolve().parents[3] / "assets" / "icon.png").read_bytes()
    icon_url = "data:image/png;base64," + base64.b64encode(icon).decode("ascii")
    require(template.count("__ROADBOOK_FALLBACK__") == 1, "Missing/duplicate fallback slot")
    require(template.count("__BRAND_ICON__") == 1 and template.count("__BRAND_PLATFORM__") == 1,
            "Missing/duplicate brand slot")
    return (template.replace("__BRAND_ICON__", icon_url, 1).replace("__BRAND_PLATFORM__", escape(platform), 1)
            .replace("__ROADBOOK_DATA__", payload, 1).replace("__ROADBOOK_FALLBACK__", fallback, 1)
            .replace('<html lang="en">', f'<html lang="{data["language"]}">', 1)
            .replace('<title>TravelPanda Roadbook</title>', f'<title>{escape(data["title"])} | TravelPanda</title>', 1))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True, help="New output directory (never overwrite)")
    parser.add_argument("--fetch-routes", action="store_true", help="Send only coordinates to public OSRM; reuse existing routes")
    parser.add_argument("--route-cache", type=Path, help="Previous roadbook.json; reuse the same mode and ordered coordinates")
    args = parser.parse_args()
    require(args.input.stat().st_size <= 15_000_000, "Input too large")
    data = validate(json.loads(args.input.read_text(encoding="utf-8")))
    require(not args.output.exists(), "Output directory already exists; choose a new version")
    if args.route_cache:
        require(args.route_cache.stat().st_size <= 15_000_000, "Cache too large")
        previous = validate(json.loads(args.route_cache.read_text(encoding="utf-8")))
        for day in data["days"]:
            coordinates = [s["coordinates"] for s in day["stops"]]
            for old in previous["days"]:
                cached = old.get("route", {})
                if (not day.get("route") and cached.get("profile") == data["mode"] and
                        cached.get("inputCoordinates") == coordinates):
                    day["route"] = old["route"]
                    day.pop("routeError", None)
    requests = 0
    if args.fetch_routes:
        for day in data["days"]:
            if day.get("route"):
                continue
            if requests:
                time.sleep(1.1)
            requests += 1
            try:
                day["route"] = route_day(day, data["mode"])
                day.pop("routeError", None)
            except RoutingUnavailable as error:
                for pending in data["days"]:
                    if not pending.get("route"):
                        pending["routeError"] = str(error)
                break
            except (ValueError, KeyError, TypeError, HTTPError, URLError, TimeoutError) as error:
                # A failed day remains an explicit point-only day; never invent a road.
                day["routeError"] = str(error)[:200]
    html = render(data)
    args.output.mkdir(parents=True)
    (args.output / "roadbook.json").write_text(json.dumps(data, ensure_ascii=False, allow_nan=False), encoding="utf-8")
    (args.output / "roadbook.html").write_text(html, encoding="utf-8")
    summary = {
        "html": str(args.output / "roadbook.html"), "data": str(args.output / "roadbook.json"),
        "mode": data["mode"], "days": len(data["days"]), "requests": requests,
        "delivery": {"interactive": "needs_host_preview_validation", "png": "not_exported"},
        "routedDays": sum(bool(d.get("route")) for d in data["days"]),
        "routes": [{"day": d["title"], "km": round(d["route"]["distance"] / 1000, 1),
                    "points": len(d["route"]["geometry"]["coordinates"])}
                   for d in data["days"] if d.get("route")],
        "missing": [{"day": d["title"], "reason": d.get("routeError", "No route supplied")}
                    for d in data["days"] if not d.get("route")],
    }
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, TypeError, KeyError) as error:
        raise SystemExit(f"Roadbook: {error}") from error
