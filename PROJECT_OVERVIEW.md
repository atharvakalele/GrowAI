# Grow24 AI — Project Overview

## 🌟 What is this Project?
**Grow24 AI** (formerly GoAmrita) is an advanced, automated business management system designed specifically for Amazon Sellers (specifically targeting the Amazon India marketplace). 

Think of it as an **"AI-Freelancer"** or a **"Virtual Business Manager"** that works 24/7. It doesn't just show you data; it actively manages your store, fixes errors, optimizes prices, and handles complex Amazon operations without human intervention.

---

## 🛑 The Problem We Are Solving
Running a large Amazon business manually is incredibly hard. Sellers face several "pain points":
1.  **Complexity:** Handling Amazon's technical APIs (SP-API and Ads API) is difficult and prone to mistakes (like using the wrong geographic region).
2.  **Time-Consuming:** Tasks like checking stock, adjusting prices to win the "Buy Box," and creating FBA shipments take hours every day.
3.  **Hidden Costs:** Calculating "True Profit" is hard when you factor in ads, returns, and Amazon fees.
4.  **Reaction vs. Action:** Most tools just tell you there is a problem. You still have to log in and fix it manually.

---

## 🎯 The Goal
The goal of Grow24 AI is to **Automate everything.** 
The project follows a simple but powerful philosophy: **"Automate business > Everything else."** 
Every module is built with two parts:
1.  **Get Data:** Use APIs to see what's happening.
2.  **Take Action:** Automatically fix the problem (e.g., lower a price, restock an item, or fix a broken listing).

---

## 🛠️ Features (In Simple Language)
The project is divided into several smart "modules":

### 1. 📊 Smart Data & Profit
*   **Data Import:** Automatically pulls your latest sales and ad data from Amazon every morning.
*   **True Profit Calculator:** Tells you exactly how much money you *actually* made after all costs.

### 2. 🕵️ continuous Monitoring (The "Watchmen")
*   **Buy Box Monitor:** Checks if you own the "Buy Box" (the 'Add to Cart' button). If you lose it, it alerts you or fixes your price.
*   **Stock Monitor:** Watches your inventory. It knows when you are running low and tells you exactly what to restock.
*   **Listing Health:** Checks if your product pages are broken or if Amazon has suppressed them.

### 3. ⚡ Automated Actions (The "Doers")
*   **Price Optimizer:** Automatically adjusts your prices every 30 minutes to stay competitive and profitable.
*   **FBA Manager:** Handles the complex 15-step process of sending stock to Amazon warehouses (FBA) automatically.
*   **Auto-Ads Creator:** Automatically creates and manages advertising campaigns for your best-performing products.

### 4. 📈 Reporting & Control
*   **Central Dashboard:** A single page where you can see all your business health stats and toggle features ON or OFF.
*   **Daily Emails:** Sends a summary of your ads and listing health directly to your inbox every morning.

---

## 💻 Tech Stack
The project uses modern, reliable tools to ensure stability:
*   **Language:** Python (The core engine).
*   **Database:** SQLite (Used for lightning-fast, local data storage).
*   **APIs:** 
    *   **Amazon SP-API:** To talk to the Seller side (Inventory, Orders, Pricing).
    *   **Amazon Ads API:** To manage advertising campaigns.
*   **Region:** Configured for Amazon India (operating via the Europe region endpoints).
*   **Control Layer:** A central `config_features.json` file that acts as the "Brain" to schedule and run all these tasks.

---

## 🚀 Summary
Grow24 AI is not just a dashboard; it is an **autonomous engine** built to scale an Amazon business by removing human error and manual labor. It lives by the rule: **If it can be automated, it should be.**
