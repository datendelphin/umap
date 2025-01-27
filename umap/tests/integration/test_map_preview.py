import json
from urllib.parse import quote

import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.django_db

GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "name": "Niagara Falls",
            },
            "geometry": {
                "type": "Point",
                "coordinates": [-79.04, 43.08],
            },
        }
    ],
}
CSV = "name,latitude,longitude\nNiagara Falls,43.08,-79.04"


def test_map_preview(page, live_server, tilelayer):
    page.goto(f"{live_server.url}/map/")
    # Edit mode is not enabled
    edit_button = page.get_by_role("button", name="Edit")
    expect(edit_button).to_be_visible()


def test_map_preview_can_load_remote_geojson(page, live_server, tilelayer):
    def handle(route):
        route.fulfill(json=GEOJSON)

    # Intercept the route to the proxy
    page.route("*/**/ajax-proxy/**", handle)

    page.goto(f"{live_server.url}/map/?dataUrl=http://some.org/geo.json")
    markers = page.locator(".leaflet-marker-icon")
    expect(markers).to_have_count(1)


def test_map_preview_can_load_remote_csv(page, live_server, tilelayer):
    def handle(route):
        csv = """name,latitude,longitude\nNiagara Falls,43.08,-79.04"""
        route.fulfill(body=csv)

    # Intercept the route to the proxy
    page.route("*/**/ajax-proxy/**", handle)

    page.goto(f"{live_server.url}/map/?dataUrl=http://some.org/geo.csv&dataFormat=csv")
    markers = page.locator(".leaflet-marker-icon")
    expect(markers).to_have_count(1)


def test_map_preview_can_load_geojson_in_querystring(page, live_server, tilelayer):
    page.goto(f"{live_server.url}/map/?data={quote(json.dumps(GEOJSON))}")
    markers = page.locator(".leaflet-marker-icon")
    expect(markers).to_have_count(1)


def test_map_preview_can_load_csv_in_querystring(page, live_server, tilelayer):
    page.goto(f"{live_server.url}/map/?data={quote(CSV)}&dataFormat=csv")
    markers = page.locator(".leaflet-marker-icon")
    expect(markers).to_have_count(1)


def test_map_preview_can_change_styling_from_querystring(page, live_server, tilelayer):
    page.goto(f"{live_server.url}/map/?data={quote(json.dumps(GEOJSON))}&color=DarkRed")
    markers = page.locator(".leaflet-marker-icon .icon_container")
    expect(markers).to_have_count(1)
    expect(markers).to_have_css("background-color", "rgb(139, 0, 0)")
