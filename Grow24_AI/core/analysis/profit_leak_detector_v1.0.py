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
    profit_file = os.path.join(json_dir, 'true_profit_per_asin.json')
    
    profits = load_json(profit_file)
    if not profits or not isinstance(profits, list):
        logging.error("Could not load true_profit_per_asin.json or it's not a list.")
        return
        
    bleeding_products = []
    total_loss = 0.0
    
    for item in profits:
        if item.get('state') == 'ENABLED':
            # Identify bleeding conditions
            true_profit = item.get('true_profit', 0)
            ad_spend = item.get('ad_spend_7d', 0)
            orders = item.get('orders_7d', 0)
            current_acr = item.get('current_acr', 0)
            
            is_bleeding = False
            reason = ""
            if true_profit < 0 and ad_spend > 0:
                is_bleeding = True
                reason = "Negative true profit while spending on ads"
            elif ad_spend > 0 and orders == 0:
                is_bleeding = True
                reason = "Spending on ads but 0 orders in 7 days"
            elif isinstance(current_acr, (int, float)) and current_acr > 120.0:
                is_bleeding = True
                reason = f"ACR is extremely high ({current_acr}%)"
                
            if is_bleeding:
                # Estimate a daily loss based on 7 days ad profit or true profit
                daily_loss = abs(true_profit) if true_profit < 0 else 0
                if daily_loss == 0 and ad_spend > 0:
                    daily_loss = ad_spend / 7.0
                    
                total_loss += daily_loss
                bleeding_products.append({
                    'asin': item.get('asin'),
                    'sku': item.get('sku'),
                    'reason': reason,
                    'true_profit': true_profit,
                    'ad_spend_7d': ad_spend,
                    'orders_7d': orders,
                    'est_daily_loss': round(daily_loss, 2)
                })
                
    # Sort by highest loss
    bleeding_products.sort(key=lambda x: x['est_daily_loss'], reverse=True)
    
    report = {
        'version': '1.0',
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_bleeding_products': len(bleeding_products),
            'total_est_daily_loss': round(total_loss, 2),
        },
        'top_offenders': bleeding_products[:5],
        'all_bleeding_products': bleeding_products
    }
    
    # Centralized output directory
    output_dir = os.path.join(project_root, 'Grow24_AI', 'data', 'analysis_results')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, 'profit_leak_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
        
    # Also save a copy in the report folder for reference
    report_json_output = os.path.join(json_dir, 'profit_leak_report.json')
    with open(report_json_output, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
        
    logging.info(f"🚨 PROFIT LEAK REPORT")
    logging.info(f"━━━━━━━━━━━━━━━━━━━━")
    logging.info(f"Total Products Bleeding Money: {len(bleeding_products)}")
    logging.info(f"Total Estimated Daily Loss: Rs.{total_loss:.2f}")
    if bleeding_products:
        logging.info("Top 5 Worst Offenders:")
        for off in bleeding_products[:5]:
            logging.info(f" - {off['sku']} (ASIN: {off['asin']}) : Loss Rs.{off['est_daily_loss']:.2f}/day | Reason: {off['reason']}")
    logging.info(f"Recommended Action: PAUSE ads on these {len(bleeding_products)} products immediately.")
    logging.info(f"Report saved to {output_path}")

if __name__ == '__main__':
    main()
