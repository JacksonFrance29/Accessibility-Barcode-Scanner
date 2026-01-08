# product_lookup.py
# Fetch product details from OpenFoodFacts. If nutrition is missing,
# optionally estimate typical values via OpenAI.

import json
import os
import ssl
import urllib.request
import urllib.parse
from typing import Optional, Dict, Any, List

from config import OPENFOODFACTS_BASE, OPENAI_API_KEY_ENV, OPENAI_MODEL


_ssl_ctx = ssl.create_default_context()
_ssl_ctx.check_hostname = False
_ssl_ctx.verify_mode = ssl.CERT_NONE

_FIELDS: List[str] = [
    "code",
    "product_name",
    "generic_name_en",
    "generic_name",
    "brands",
    "brand_owner",
    "categories",
    "categories_hierarchy",
    "categories_tags",
    "serving_size",
    "serving_size_prepared",
    "allergens",
    "allergens_tags",
    "ingredients_text",
    "ingredients_text_en",
    "nutriments",
]


def _build_off_url(barcode: str) -> str:
    qs = urllib.parse.urlencode({"fields": ",".join(_FIELDS)})
    return f"{OPENFOODFACTS_BASE}/{barcode}.json?{qs}"


def _http_get_json(url: str, timeout: float = 8.0) -> Optional[Dict[str, Any]]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ASU-Assistive-Scanner/1.1 (edu project)",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout, context=_ssl_ctx) as r:
        data = r.read().decode("utf-8", "ignore")
    try:
        return json.loads(data)
    except Exception:
        return None


def _normalize_off_product(p: Dict[str, Any]) -> Dict[str, Any]:
    name = p.get("product_name") or p.get("generic_name_en") or p.get("generic_name")
    brand = p.get("brands") or p.get("brand_owner")
    if not isinstance(p.get("nutriments"), dict):
        p["nutriments"] = {}
    p["name"] = name
    p["brand"] = brand
    return p


def _ai_client_or_none():
    key = os.getenv(OPENAI_API_KEY_ENV)
    if not key:
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=key)
    except Exception:
        return None


def _estimate_nutrition_with_ai(name: str | None, brand: str | None, cats: list[str]) -> Optional[Dict[str, Any]]:
    client = _ai_client_or_none()
    if not client:
        return None

    cats_text = ", ".join(c.replace("en:", "").replace("-", " ") for c in (cats or [])) or "unknown category"
    title = " ".join(x for x in [brand, name] if x) or "Unknown product"

    system = (
        "You are a careful nutrition assistant. When real facts are unavailable, you provide a "
        "reasonable, conservative estimate for typical products in the same category. "
        "Return strictly valid JSON with numeric values per 100 g (or 100 ml) when relevant. "
        "Do not include any text outside JSON."
    )
    user = f"""
    Estimate typical nutrition for:
    Title: {title}
    Category hints: {cats_text}

    Return JSON with keys:
    {{
      "serving_size": "string, e.g. '30 g'",
      "allergens": "string or empty",
      "ingredients_text_en": "string or empty",
      "nutriments": {{
        "energy-kcal_100g": number,
        "proteins_100g": number,
        "carbohydrates_100g": number,
        "sugars_100g": number,
        "fat_100g": number,
        "saturated-fat_100g": number,
        "fiber_100g": number,
        "sodium_100g": number
      }}
    }}
    """

    try:
        resp = client.responses.create(
            model=OPENAI_MODEL,
            input=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        raw = (resp.output_text or "").strip()
        obj = json.loads(raw)
        if not isinstance(obj, dict) or "nutriments" not in obj or not isinstance(obj["nutriments"], dict):
            return None
        return obj
    except Exception:
        return None


def _has_real_nutrition(p: Dict[str, Any]) -> bool:
    n = p.get("nutriments") or {}
    keys = [
        "energy-kcal_100g",
        "proteins_100g",
        "carbohydrates_100g",
        "sugars_100g",
        "fat_100g",
        "saturated-fat_100g",
        "fiber_100g",
        "sodium_100g",
    ]
    return any(k in n and n[k] not in (None, "", 0) for k in keys)


def lookup_product(barcode: str) -> Optional[Dict[str, Any]]:
    """Return a normalized product dict, possibly with estimated nutriments."""
    # 1) Try OpenFoodFacts
    try:
        data = _http_get_json(_build_off_url(barcode))
    except Exception:
        data = None

    product = (data or {}).get("product") or {}
    if product:
        product = _normalize_off_product(product)

    if product and _has_real_nutrition(product):
        product["estimated"] = False
        product["estimation_note"] = "Nutrition facts from OpenFoodFacts."
        return product

    if product and not _has_real_nutrition(product):
        est = _estimate_nutrition_with_ai(
            name=product.get("name"),
            brand=product.get("brand"),
            cats=product.get("categories_tags") or product.get("categories_hierarchy") or [],
        )
        if est:
            product.setdefault("nutriments", {})
            for k, v in (est.get("nutriments") or {}).items():
                product["nutriments"][k] = v
            if est.get("serving_size") and not product.get("serving_size"):
                product["serving_size"] = est["serving_size"]
            if est.get("allergens") and not product.get("allergens"):
                product["allergens"] = est["allergens"]
            if est.get("ingredients_text_en") and not product.get("ingredients_text_en"):
                product["ingredients_text_en"] = est["ingredients_text_en"]
            product["estimated"] = True
            product["estimation_note"] = "Nutrition values are estimated averages for this category."
            return product

        product["estimated"] = False
        product.setdefault("nutriments", {})
        product["estimation_note"] = "No nutrition facts found."
        return product

    # 2) No OFF record at all; optionally estimate a generic shell
    est = _estimate_nutrition_with_ai(name=None, brand=None, cats=[])
    if est:
        shell = {
            "code": barcode,
            "name": None,
            "brand": None,
            "categories_tags": [],
            "nutriments": est.get("nutriments") or {},
            "serving_size": est.get("serving_size"),
            "allergens": est.get("allergens"),
            "ingredients_text_en": est.get("ingredients_text_en"),
            "estimated": True,
            "estimation_note": "Estimated average nutrition due to missing product record.",
        }
        return shell

    # 3) Total failure
    return None
