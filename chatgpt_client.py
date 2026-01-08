# chatgpt_client.py
# Turn product data (including nutriments) into a speech string.
# Focus on serving size, calories, protein, and sugar.

import os
from config import OPENAI_API_KEY_ENV, OPENAI_MODEL


def get_openai_client():
    key = os.getenv(OPENAI_API_KEY_ENV)
    if not key:
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=key)
    except Exception:
        return None


def generate_product_speech(barcode: str, product_info: dict | None) -> str:
    """
    Generate a short, speech-friendly summary focused on serving size,
    calories, protein, and sugar.
    """
    def first_nonempty(*xs):
        for x in xs:
            if isinstance(x, str) and x.strip():
                return x.strip()
        return None

    if product_info is None:
        return f"I scanned barcode {barcode}. I couldn't identify the product."

    name = first_nonempty(
        product_info.get("name"),
        product_info.get("product_name"),
        product_info.get("generic_name_en"),
        product_info.get("generic_name"),
    )
    brand = first_nonempty(
        product_info.get("brand"),
        product_info.get("brands"),
    )

    nutr = product_info.get("nutriments") or {}
    serving = first_nonempty(
        product_info.get("serving_size"),
        product_info.get("serving_size_prepared"),
    )

    # Only the key nutrients we care about
    kcal = nutr.get("energy-kcal_100g") or nutr.get("energy-kcal_serving") or nutr.get("energy-kcal")
    protein = nutr.get("proteins_100g") or nutr.get("proteins_serving")
    sugars = nutr.get("sugars_100g") or nutr.get("sugars_serving")

    estimated = bool(product_info.get("estimated"))
    est_note = product_info.get("estimation_note") or ""

    base_line = "You are assisting a blind shopper."
    prompt = f"""
    {base_line}
    Provide a short, factual spoken summary using ONLY these fields:
    - Serving size (say it once)
    - Calories
    - Protein
    - Sugar

    If a value is missing, skip it silently. Do NOT invent numbers.
    If estimated values are indicated, begin with: "Estimated values."

    Format example:
    "<Brand> <Name>. Serving size <serving>. Calories <value>. Protein <value>. Sugar <value>."

    Product data:
    Barcode: {barcode}
    Brand: {brand or "unknown"}
    Name: {name or "unknown"}
    Serving size: {serving or "unknown"}
    Calories: {kcal or "unknown"}
    Protein: {protein or "unknown"}
    Sugar: {sugars or "unknown"}
    Estimation note: {est_note}
    """

    try:
        client = get_openai_client()
        if client:
            resp = client.responses.create(model=OPENAI_MODEL, input=prompt)
            txt = (resp.output_text or "").strip()
            if txt:
                return txt
    except Exception:
        pass

    # Deterministic local fallback (no AI)
    title = " ".join(x for x in [brand, name] if x) or "Product"
    parts = []
    if estimated:
        parts.append("Estimated values.")
    parts.append(f"{title}.")
    if serving:
        parts.append(f"Serving size {serving}.")
    if kcal is not None:
        try:
            parts.append(f"Calories {int(round(float(kcal)))}.")
        except Exception:
            pass
    if protein is not None:
        parts.append(f"Protein {protein} grams.")
    if sugars is not None:
        parts.append(f"Sugar {sugars} grams.")
    return " ".join(parts) or "Product details unavailable."
