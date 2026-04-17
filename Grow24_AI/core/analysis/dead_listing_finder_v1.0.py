import os
import json
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def get_latest_report_dir(base_dir):
    folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
    if not folders: return None
    folders.sort(key=lambda x: os.path.getmtime(os.path.join(base_dir, x)), reverse=True)
    return os.path.join(base_dir, folders[0])

def load_json(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading {filepath}: {e}")
    return None

def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    report_base = os.path.join(project_root, 'ClaudeCode', 'Report')
    
    if not os.path.exists(report_base):
        logging.error("Report base directory does not exist.")
        return
        
    latest_report_dir = get_latest_report_dir(report_base)
    
    if not latest_report_dir:
        logging.error("No report directory found.")
        return
        
    json_dir = os.path.join(latest_report_dir, 'Json')
    
    bb_file = os.path.join(json_dir, 'buy_box_status.json')
    stock_file = os.path.join(json_dir, 'stock_status.json')
    profit_file = os.path.join(json_dir, 'true_profit_per_asin.json')
    
    bb_data = load_json(bb_file) or []
    stock_data = load_json(stock_file) or {}
    profit_data = load_json(profit_file) or []
    
    # Map data by ASIN
    buybox_map = {item.get('asin'): item for item in bb_data if item.get('asin')}
    
    # Stock map: Map ASINs to stock count
    stock_map = {}
    for st in stock_data.get('zero_stock', []):
        stock_map[st.get('asin')] = 0
    for st in stock_data.get('low_stock', []):
        stock_map[st.get('asin')] = st.get('total_stock', 1)
        
    profit_map = {item.get('asin'): item for item in profit_data if item.get('asin')}
    
    dead_listings = []
    fixable_listings = []
    at_risk_listings = []
    
    # Collect all unique ASINs
    all_asins = set(buybox_map.keys()).union(stock_map.keys()).union(profit_map.keys())
    
    for asin in all_asins:
        bb_info = buybox_map.get(asin, {})
        has_bb = bb_info.get('buy_box_status') == 'WON'
        no_bb = bb_info.get('buy_box_status') in ('NO_BUYBOX', 'LOST')
        
        # If it's not explicitly in the zero stock list, we assume it has stock 
        # (or check if it was specifically registered with 0)
        has_stock = stock_map.get(asin, -1) != 0
        
        prof_info = profit_map.get(asin, {})
        has_sales = prof_info.get('orders_7d', 0) > 0 or prof_info.get('sales_7d', 0) > 0
        
        # Determine SKU
        sku = bb_info.get('sku') or prof_info.get('sku') or 'Unknown'
        
        if no_bb and not has_stock and not has_sales:
            dead_listings.append({'asin': asin, 'sku': sku})
        elif no_bb and has_stock:
            fixable_listings.append({
                'asin': asin, 
                'sku': sku, 
                'reason': bb_info.get('reason', 'Listing may be suppressed')
            })
        elif has_bb and not has_stock:
            at_risk_listings.append({'asin': asin, 'sku': sku})
            
    # Compile the final report
    report = {
        'version': '1.0',
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'dead': len(dead_listings),
            'fixable': len(fixable_listings),
            'at_risk': len(at_risk_listings)
        },
        'dead_listings': dead_listings,
        'fixable_listings': fixable_listings,
        'at_risk_listings': at_risk_listings
    }
    
    # Centralized output directory
    output_dir = os.path.join(project_root, 'Grow24_AI', 'data', 'analysis_results')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, 'dead_listing_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
        
    # Also save a copy in the report folder for reference
    report_json_output = os.path.join(json_dir, 'dead_listing_report.json')
    with open(report_json_output, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
        
    # Output to console
    logging.info("💀 DEAD LISTING REPORT")
    logging.info("━━━━━━━━━━━━━━━━━━━━━")
    logging.info(f"☠️ Truly Dead (ignore): {len(dead_listings)} listings")
    logging.info(f"🔧 Fixable (act now):   {len(fixable_listings)} listings  ← PRIORITY")
    logging.info(f"⚠️ At Risk (restock):   {len(at_risk_listings)} listings")
    
    if fixable_listings:
        logging.info("")
        logging.info("🔧 TOP FIXABLE LISTINGS (they have stock but no Buy Box):")
        for fix in fixable_listings[:5]:
            logging.info(f" {fix['sku']} ({fix['asin']}) — Reason: {fix['reason']}")
            
    logging.info(f"Report saved to {output_path}")

if __name__ == '__main__':
    main()
