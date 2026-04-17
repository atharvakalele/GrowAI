#!/usr/bin/env python3
"""
GoAmrita - True Profit Calculator v1.0 (MVP)
=============================================
Author: Msir + Claude
Date: 13 April 2026

Calculates TRUE profit per ASIN after ALL costs.
Foundation for all optimization decisions.

MVP Approach:
  Sale Price    -> Calculated from actual sales data (sales7d / orders7d)
                   If no orders -> SP-API Catalog fetch (Phase 0.2)
                   If still none -> config default
  Product Cost  -> 3-Level: Product > Category > Account default
  Amazon Fee    -> Rs.165 + 6% of sale price (configurable)
  Shipping      -> Rs.80 flat (configurable)

  If no sale price available at all -> flat Rs.180/order default

Usage:
    python true_profit_calculator_v1.0.py
    python true_profit_calculator_v1.0.py --export excel
"""

import json
import os
import sys
from datetime import datetime

# ============================================
# CONFIGURATION (all configurable!)
# ============================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))

TODAY = datetime.now().strftime("%d %B %Y")
# Find latest report folder
REPORT_BASE = os.path.join(SCRIPT_DIR, "..", "Report")
if os.path.exists(REPORT_BASE):
    report_folders = [f for f in os.listdir(REPORT_BASE) if os.path.isdir(os.path.join(REPORT_BASE, f))]
    report_folders.sort(key=lambda x: os.path.getmtime(os.path.join(REPORT_BASE, x)), reverse=True)
    LATEST_REPORT = report_folders[0] if report_folders else TODAY
else:
    LATEST_REPORT = TODAY
REPORT_DIR = os.path.join(SCRIPT_DIR, "..", "Report", LATEST_REPORT)
JSON_DIR = os.path.join(REPORT_DIR, "Json")
CONFIG_FILE = os.path.join(PROJECT_DIR, "config_true_profit.json")

# Default config (created on first run if not exists)
DEFAULT_CONFIG = {
    "version": "1.0",
    "last_updated": "",

    # 3-Level Product Cost (Account > Category > Product)
    "account_default": {
        "product_cost": 150,
        "description": "Default product cost for ALL ASINs if not specified at category/product level"
    },
    "category_costs": {
        "Sea Salt": 250,
        "Capsules": 100,
        "Powder": 80,
        "Oil": 120,
        "Combo": 200
    },
    "product_costs": {
        # ASIN: cost  (overrides category and account)
        # "B0FBWXQ9JL": 280
    },

    # ASIN to Category mapping
    "asin_category": {
        # "B0FBWXQ9JL": "Sea Salt"
    },

    # Amazon Fee Structure (configurable)
    "amazon_fees": {
        "fixed_fee": 165,
        "percentage_fee": 6.0,
        "description": "Total Amazon fee = Rs.165 + 6% of sale price"
    },

    # Shipping (configurable)
    "shipping": {
        "default": 80,
        "description": "Flat shipping cost per order. Update per product later."
    },

    # Return Rate
    "return_rate": {
        "default_percent": 5.0,
        "description": "Average return rate. Cost of return = return_rate% of sale_price"
    },

    # Fallback if no sale price found at all
    "fallback_order_value": 180,

    # Target Profit Settings
    "target_profit_retention": 60,
    "description_target": "Keep 60% of true profit after ads. Ads can eat max 40%.",

    # GST (future - not in MVP)
    "gst_rate": 0
}


def load_or_create_config():
    """Load config, create default if not exists"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        print(f"  Config loaded: {CONFIG_FILE}")
        return config
    else:
        DEFAULT_CONFIG["last_updated"] = datetime.now().isoformat()
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
        print(f"  Config created (first run): {CONFIG_FILE}")
        print(f"  >> Edit this file to set product costs, categories, fees!")
        return DEFAULT_CONFIG


def get_product_cost(asin, config):
    """3-Level lookup: Product > Category > Account default"""
    # Level 1: Product-specific
    if asin in config.get("product_costs", {}):
        return config["product_costs"][asin], "product"

    # Level 2: Category-specific
    category = config.get("asin_category", {}).get(asin, "")
    if category and category in config.get("category_costs", {}):
        return config["category_costs"][category], f"category:{category}"

    # Level 3: Account default
    return config["account_default"]["product_cost"], "account_default"


def calculate_true_profit(sale_price, product_cost, config):
    """Calculate true profit after ALL costs"""
    fees = config["amazon_fees"]
    shipping = config["shipping"]["default"]
    return_rate = config["return_rate"]["default_percent"] / 100

    referral_fee = fees.get("referral_fee_pct", fees.get("percentage_fee", 3.0)) / 100 * sale_price
    closing_fee = fees.get("closing_fee", fees.get("fixed_fee", 5))
    amazon_fee = referral_fee + closing_fee
    return_cost = return_rate * sale_price

    true_profit = sale_price - product_cost - amazon_fee - shipping - return_cost
    true_profit_pct = (true_profit / sale_price * 100) if sale_price > 0 else 0

    # Max ad spend per sale (target: keep X% of profit)
    target_retention = config.get("target_profit_retention", 60) / 100
    max_ad_spend = true_profit * (1 - target_retention) if true_profit > 0 else 0

    # Break-even: max ad spend where profit = 0
    break_even_ad = true_profit if true_profit > 0 else 0
    break_even_acr = 100  # 100% of true profit = break even

    # Target ACR
    target_acr = (1 - target_retention) * 100  # e.g. 40% if retention=60%

    return {
        "sale_price": round(sale_price, 2),
        "product_cost": round(product_cost, 2),
        "amazon_fee": round(amazon_fee, 2),
        "shipping": shipping,
        "return_cost": round(return_cost, 2),
        "true_profit": round(true_profit, 2),
        "true_profit_pct": round(true_profit_pct, 1),
        "max_ad_spend_per_sale": round(max_ad_spend, 2),
        "break_even_ad_spend": round(break_even_ad, 2),
        "target_acr": target_acr,
        "profitable_for_ads": true_profit > 0
    }


def load_asin_data():
    """Load ASIN data from imported JSON files"""
    asins = {}

    # 1. Get ASIN list from product ads
    ads_file = os.path.join(JSON_DIR, "sp_product_ads_list.json")
    if os.path.exists(ads_file):
        with open(ads_file, "r", encoding="utf-8") as f:
            ads = json.load(f)
        for a in ads:
            asin = a.get("asin", "")
            if asin and asin not in asins:
                asins[asin] = {
                    "sku": a.get("sku", ""),
                    "state": a.get("state", ""),
                    "sales": 0, "orders": 0, "cost": 0,
                    "clicks": 0, "impressions": 0,
                    "avg_sale_price": 0
                }

    # 2. Get performance data from advertised product report
    prod_file = os.path.join(JSON_DIR, "sp_advertisedproduct_daily.json")
    if os.path.exists(prod_file):
        with open(prod_file, "r", encoding="utf-8") as f:
            prod = json.load(f)
        for r in prod:
            asin = r.get("advertisedAsin", "")
            if asin not in asins:
                asins[asin] = {
                    "sku": r.get("advertisedSku", ""),
                    "state": "UNKNOWN",
                    "sales": 0, "orders": 0, "cost": 0,
                    "clicks": 0, "impressions": 0,
                    "avg_sale_price": 0
                }
            asins[asin]["sales"] += float(r.get("sales7d", 0))
            asins[asin]["orders"] += int(r.get("purchases7d", 0))
            asins[asin]["cost"] += float(r.get("cost", 0))
            asins[asin]["clicks"] += int(r.get("clicks", 0))
            asins[asin]["impressions"] += int(r.get("impressions", 0))
            if not asins[asin]["sku"]:
                asins[asin]["sku"] = r.get("advertisedSku", "")

    # 3. Calculate avg sale price per ASIN (from actual sales — BEST source, includes MOQ)
    for asin, d in asins.items():
        if d["orders"] > 0:
            d["avg_sale_price"] = d["sales"] / d["orders"]

    # 4. Fallback: Load API prices for ASINs without orders
    pricing_file = os.path.join(JSON_DIR, "sp_pricing_data.json")
    if os.path.exists(pricing_file):
        with open(pricing_file, "r", encoding="utf-8") as f:
            api_prices = json.load(f)
        api_enriched = 0
        for asin, d in asins.items():
            if d["avg_sale_price"] == 0 and asin in api_prices:
                api_price = api_prices[asin].get("your_price", 0)
                if api_price > 0:
                    d["avg_sale_price"] = api_price
                    d["price_source"] = "api"
                    api_enriched += 1
        print(f"  API price fallback applied: {api_enriched} ASINs")

    return asins


def main():
    print("=" * 70)
    print("  GoAmrita - True Profit Calculator v1.0 (MVP)")
    print(f"  Date: {TODAY}")
    print("=" * 70)

    # Load config
    print("\n[1/4] Loading configuration...")
    config = load_or_create_config()

    # Load ASIN data
    print("\n[2/4] Loading ASIN data from imported reports...")
    asins = load_asin_data()
    print(f"  Found {len(asins)} unique ASINs")

    with_price = sum(1 for a in asins.values() if a["avg_sale_price"] > 0)
    without_price = len(asins) - with_price
    print(f"  With sale price (from orders): {with_price}")
    print(f"  Without price (using fallback): {without_price}")

    # Calculate true profit for each ASIN
    print("\n[3/4] Calculating True Profit per ASIN...")
    results = []
    skipped_no_price = []

    for asin, data in asins.items():
        # Sale price: actual sales > API price > SKIP (no fallback!)
        if data["avg_sale_price"] > 0:
            sale_price = data["avg_sale_price"]
            price_source = "actual_sales"
        elif data.get("price_source") == "api" and data["avg_sale_price"] > 0:
            sale_price = data["avg_sale_price"]
            price_source = "api"
        else:
            # NO PRICE = SKIP — don't use ₹180 fallback (wrong decisions!)
            skipped_no_price.append({
                "asin": asin,
                "sku": data.get("sku", "")[:30],
                "status": "No Price Available - Excluded from Optimization",
                "ai_reason": "Price not available from sales data or API. Listing may be suppressed, inactive, or draft. No ads will run until price verified. Check Seller Central.",
                "profitable_for_ads": False,
            })
            continue

        price_source = "actual_sales" if data["avg_sale_price"] == sale_price and data.get("price_source") != "api" else "api"

        # Product cost: 3-level lookup
        product_cost, cost_source = get_product_cost(asin, config)

        # Calculate
        profit = calculate_true_profit(sale_price, product_cost, config)

        # Ad metrics
        ad_spend_per_sale = (data["cost"] / data["orders"]) if data["orders"] > 0 else 0
        current_acr = (ad_spend_per_sale / profit["true_profit"] * 100) if profit["true_profit"] > 0 and data["orders"] > 0 else (999 if data["cost"] > 0 else 0)

        results.append({
            "asin": asin,
            "sku": data["sku"][:30],
            "state": data["state"],
            "sale_price": round(sale_price),
            "price_source": price_source,
            "product_cost": product_cost,
            "cost_source": cost_source,
            "amazon_fee": profit["amazon_fee"],
            "shipping": profit["shipping"],
            "return_cost": profit["return_cost"],
            "true_profit": profit["true_profit"],
            "true_profit_pct": profit["true_profit_pct"],
            "profitable_for_ads": profit["profitable_for_ads"],
            "max_ad_spend": profit["max_ad_spend_per_sale"],
            "break_even_ad": profit["break_even_ad_spend"],
            "target_acr": profit["target_acr"],
            "orders_7d": data["orders"],
            "sales_7d": round(data["sales"]),
            "ad_spend_7d": round(data["cost"]),
            "ad_spend_per_sale": round(ad_spend_per_sale),
            "current_acr": round(current_acr, 1) if current_acr < 999 else "N/A",
            "ad_profit_7d": round(data["sales"] - data["cost"]) if data["orders"] > 0 else round(-data["cost"]),
            "impressions": data["impressions"],
            "clicks": data["clicks"],
        })

    # Sort: worst (negative profit) first, then by true profit
    results.sort(key=lambda x: x["true_profit"])

    # Display
    print(f"\n[4/4] Results:")
    print("=" * 130)
    print(f"{'ASIN':<14} {'SKU':<22} {'Price':>7} {'Cost':>6} {'Fee':>6} {'Ship':>5} {'TrueProfit':>10} {'TP%':>5} {'MaxAd':>7} {'Orders':>6} {'AdSpend':>8} {'ACR':>7} {'Ads OK?'}")
    print("-" * 130)

    profitable_count = 0
    unprofitable_count = 0
    total_true_profit = 0
    total_ad_profit = 0

    for r in results:
        flag = "YES" if r["profitable_for_ads"] else "NO!"
        acr_str = f"{r['current_acr']}%" if r['current_acr'] != "N/A" else "N/A"

        if r["true_profit"] > 0:
            profitable_count += 1
        else:
            unprofitable_count += 1
        total_true_profit += r["true_profit"] * max(r["orders_7d"], 1)
        total_ad_profit += r["ad_profit_7d"]

        print(f"{r['asin']:<14} {r['sku']:<22} {r['sale_price']:>7} {r['product_cost']:>6} {r['amazon_fee']:>6.0f} {r['shipping']:>5} {r['true_profit']:>10.0f} {r['true_profit_pct']:>5.1f}% {r['max_ad_spend']:>7.0f} {r['orders_7d']:>6} {r['ad_spend_7d']:>8} {acr_str:>7} {flag}")

    print("=" * 130)
    print(f"\nSUMMARY:")
    print(f"  Total ASINs: {len(results)}")
    pct_profitable = (profitable_count/len(results)*100) if len(results) > 0 else 0
    pct_unprofitable = (unprofitable_count/len(results)*100) if len(results) > 0 else 0
    print(f"  Profitable for ads: {profitable_count} ({pct_profitable:.0f}%)")
    print(f"  NOT profitable for ads: {unprofitable_count} ({pct_unprofitable:.0f}%)")
    print(f"  No Price Available - Excluded from Optimization: {len(skipped_no_price)} (excluded from calculations)")
    print(f"  Total Ad P&L (7 days): Rs.{total_ad_profit:,.0f}")
    print(f"\n  Config: Amazon Fee = {config['amazon_fees'].get('referral_fee_pct', 3)}% referral + Rs.{config['amazon_fees'].get('closing_fee', 5)} closing")
    print(f"  Config: Shipping = Rs.{config['shipping']['default']}")
    print(f"  Config: Default Product Cost = Rs.{config['account_default']['product_cost']}")
    print(f"  Config: Target Profit Retention = {config.get('target_profit_retention', 60)}%")

    # Save results
    output_json = os.path.join(JSON_DIR, "true_profit_per_asin.json")
    os.makedirs(JSON_DIR, exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n  Saved: {output_json}")

    # Save config path reminder
    print(f"\n  >> To customize product costs, edit: {CONFIG_FILE}")
    print(f"  >> Add ASIN-specific: product_costs -> 'B0XXXX': 250")
    print(f"  >> Add category: category_costs -> 'Sea Salt': 280")
    print(f"  >> Map ASIN to category: asin_category -> 'B0XXXX': 'Sea Salt'")

    return 0


if __name__ == "__main__":
    sys.exit(main())
