import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

OPENWEATHERMAP_CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"


def dashboard(request: HttpRequest) -> HttpResponse:
    default_city = getattr(settings, "OPENWEATHERMAP_DEFAULT_CITY", "Berlin") or "Berlin"
    default_units = getattr(settings, "OPENWEATHERMAP_DEFAULT_UNITS", "metric") or "metric"
    return render(
        request,
        "weather/dashboard.html",
        {"default_city": default_city, "default_units": default_units},
    )


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        "Weather app is connected. Visit / for the dashboard or call /weather/?city=Berlin",
        content_type="text/plain",
    )


def current_weather(request: HttpRequest) -> JsonResponse:
    api_key = getattr(settings, "OPENWEATHERMAP_API_KEY", "")
    if not api_key:
        return JsonResponse(
            {"error": "Missing OPENWEATHERMAP_API_KEY in Django settings."},
            status=500,
        )

    city = request.GET.get("city") or getattr(settings, "OPENWEATHERMAP_DEFAULT_CITY", "")
    if not city:
        return JsonResponse(
            {"error": "Missing required query parameter: city"},
            status=400,
        )

    units = request.GET.get("units") or getattr(
        settings, "OPENWEATHERMAP_DEFAULT_UNITS", "metric"
    )

    url = f"{OPENWEATHERMAP_CURRENT_URL}?{urlencode({'q': city, 'appid': api_key, 'units': units})}"
    req = Request(url, headers={"Accept": "application/json"})

    try:
        with urlopen(req, timeout=10) as resp:
            data: dict[str, Any] = json.load(resp)
    except HTTPError as e:
        details: Any = None
        try:
            raw = e.read().decode("utf-8", errors="ignore")
            details = json.loads(raw) if raw else None
        except Exception:
            details = None
        return JsonResponse(
            {
                "error": "OpenWeatherMap request failed",
                "status": getattr(e, "code", None),
                "details": details,
            },
            status=502,
        )
    except URLError as e:
        return JsonResponse(
            {"error": "Unable to reach OpenWeatherMap", "details": str(e)},
            status=502,
        )

    weather_list = data.get("weather") or []
    weather0 = weather_list[0] if isinstance(weather_list, list) and weather_list else {}

    result: dict[str, Any] = {
        "city": data.get("name"),
        "country": (data.get("sys") or {}).get("country"),
        "lat": (data.get("coord") or {}).get("lat"),
        "lon": (data.get("coord") or {}).get("lon"),
        "units": units,
        "temperature": (data.get("main") or {}).get("temp"),
        "feels_like": (data.get("main") or {}).get("feels_like"),
        "humidity": (data.get("main") or {}).get("humidity"),
        "pressure": (data.get("main") or {}).get("pressure"),
        "description": weather0.get("description"),
        "wind_speed": (data.get("wind") or {}).get("speed"),
        "timestamp": data.get("dt"),
    }

    if request.GET.get("raw") in {"1", "true", "yes"}:
        result["raw"] = data

    return JsonResponse(result)
