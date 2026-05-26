"""
generate_dataset.py

Generates a clean 1000+ row training dataset with realistic
expense descriptions and correct categories.

Run once: python3 ml/generate_dataset.py
It creates: backend/data/classifier_training.csv
"""

import pandas as pd
import random
import os

random.seed(42)

# ── Templates per category ──────────────────────────────────────────────────
# Each entry is a template. {var} gets replaced with a random word from its list.
# This gives us huge variety from a small set of templates.

TEMPLATES = {

    "food": {
        "templates": [
            "{app} food delivery", "{app} order {meal}",
            "{meal} restaurant", "lunch {place}",
            "dinner {place}", "breakfast {place}",
            "grocery {store}", "bought {grocery}",
            "{meal} takeaway", "canteen {meal}",
            "mess fee payment", "tiffin service",
            "{meal} street food", "chai snacks",
            "ordered {meal} online",
        ],
        "vars": {
            "app":     ["zomato","swiggy","uber eats","dunzo"],
            "meal":    ["biryani","pizza","burger","pasta","dosa","idli","noodles",
                        "chicken","sandwich","salad","sushi","tacos","roti","rice"],
            "place":   ["cafe","restaurant","hotel","canteen","dhaba","food court"],
            "store":   ["supermarket","bigbasket","blinkit","zepto","dmart","reliance fresh"],
            "grocery": ["vegetables","fruits","milk eggs bread","rice dal","cooking oil",
                        "snacks biscuits","paneer","meat fish"],
        }
    },

    "transport": {
        "templates": [
            "{app} cab ride", "{app} bike taxi",
            "metro card recharge", "bus pass {period}",
            "auto rickshaw fare", "{fuel} refill pump",
            "train ticket {route}", "flight ticket booking",
            "toll plaza charges", "parking fee",
            "bike servicing {place}", "vehicle {service}",
            "cab to {dest}", "local bus commute",
            "monthly {pass} pass",
        ],
        "vars": {
            "app":     ["uber","ola","rapido","indrive","meru"],
            "fuel":    ["petrol","diesel","cng"],
            "period":  ["monthly","weekly","quarterly"],
            "route":   ["booking","irctc","station"],
            "place":   ["workshop","garage","service center"],
            "service": ["service","repair","oil change","tyre change"],
            "dest":    ["airport","office","college","station","home"],
            "pass":    ["metro","bus","transit"],
        }
    },

    "entertainment": {
        "templates": [
            "{app} subscription {period}",
            "movie ticket {place}",
            "{game} gaming purchase",
            "concert {event} ticket",
            "{app} premium plan",
            "bowling alley game",
            "escape room booking",
            "amusement park entry",
            "comedy show ticket",
            "sports match ticket",
            "theme park entry",
            "laser tag arena",
            "karaoke night out",
            "club entry fee",
            "online game {game}",
        ],
        "vars": {
            "app":    ["netflix","amazon prime","hotstar","spotify","youtube",
                       "zee5","sonyliv","apple tv","discord","twitch"],
            "period": ["monthly","annual","yearly"],
            "place":  ["pvr","inox","cinepolis","multiplex"],
            "game":   ["steam","playstation","xbox","mobile","pc"],
            "event":  ["live","music","stand up","dj"],
        }
    },

    "shopping": {
        "templates": [
            "{app} online shopping",
            "{item} purchase {app}",
            "bought {item} online",
            "{store} shopping haul",
            "{item} {store}",
            "sale shopping {item}",
            "ordered {item} {app}",
            "{item} delivery {app}",
        ],
        "vars": {
            "app":   ["amazon","flipkart","myntra","ajio","meesho","nykaa","snapdeal"],
            "item":  ["clothes","shoes","bags","accessories","home decor","electronics",
                      "gadgets","books","toys","gifts","watches","sunglasses"],
            "store": ["mall","outlet","store","market"],
        }
    },

    "technology": {
        "templates": [
            "{item} purchase {store}",
            "bought {item}",
            "{item} upgrade",
            "{store} tech purchase",
            "{item} repair service",
            "software {sub} subscription",
            "{item} accessories",
            "new {item} order",
        ],
        "vars": {
            "item":  ["laptop","phone","iphone","smartphone","tablet","ipad",
                      "earphones","airpods","keyboard","mouse","monitor",
                      "hard disk","pen drive","charger","cable","router"],
            "store": ["apple store","samsung","croma","reliance digital","amazon"],
            "sub":   ["adobe","microsoft office","antivirus","cloud storage"],
        }
    },

    "health": {
        "templates": [
            "{place} doctor consultation",
            "pharmacy {medicine}",
            "bought {medicine}",
            "{test} medical test",
            "hospital {visit}",
            "health insurance premium",
            "{place} dentist visit",
            "eye checkup {place}",
            "physiotherapy session",
            "blood test {lab}",
        ],
        "vars": {
            "place":    ["clinic","hospital","apollo","fortis","care"],
            "medicine": ["medicines","tablets","vitamins","supplements","syrup"],
            "test":     ["blood","urine","xray","mri","ecg","thyroid"],
            "visit":    ["consultation","checkup","followup","emergency"],
            "lab":      ["lab","diagnostic center","pathology"],
        }
    },

    "education": {
        "templates": [
            "{place} course fee",
            "{app} subscription learning",
            "bought {item} college",
            "{place} tuition fee",
            "exam registration fee",
            "{item} study material",
            "semester {place} fee",
            "workshop training fee",
            "{app} certificate course",
            "coaching class {subject}",
        ],
        "vars": {
            "place":   ["college","university","school","institute","coaching"],
            "app":     ["udemy","coursera","skillshare","linkedin learning","unacademy"],
            "item":    ["books","notebooks","stationery","pen drive","calculator"],
            "subject": ["math","science","english","coding","data science","design"],
        }
    },

    "utilities": {
        "templates": [
            "{bill} bill payment",
            "paid {bill} bill",
            "{provider} recharge",
            "monthly {bill} charge",
            "{bill} dues payment",
            "prepaid {bill} recharge",
        ],
        "vars": {
            "bill":     ["electricity","water","wifi","broadband","internet",
                         "gas cylinder","lpg","dth","cable tv","mobile postpaid"],
            "provider": ["jio","airtel","bsnl","vodafone","act","hathway","tata sky"],
        }
    },

    "travel": {
        "templates": [
            "flight ticket {dest}",
            "hotel stay {dest}",
            "{dest} trip travel",
            "train booking {dest}",
            "bus ticket {dest}",
            "travel insurance",
            "visa fee {dest}",
            "holiday package {dest}",
            "airbnb stay {dest}",
            "cab {dest} outstation",
        ],
        "vars": {
            "dest": ["mumbai","delhi","goa","bangalore","hyderabad","kerala",
                     "manali","shimla","dubai","bangkok","singapore","london"],
        }
    },

}

# ── Generate rows ────────────────────────────────────────────────────────────

def fill_template(template, var_map):
    result = template
    for key, options in var_map.items():
        placeholder = "{" + key + "}"
        if placeholder in result:
            result = result.replace(placeholder, random.choice(options))
    return result

rows = []
SAMPLES_PER_CATEGORY = 130   # ~130 × 9 categories = ~1170 total

for category, data in TEMPLATES.items():
    templates = data["templates"]
    var_map   = data["vars"]
    seen = set()

    attempts = 0
    while len([r for r in rows if r["category"] == category]) < SAMPLES_PER_CATEGORY:
        t = random.choice(templates)
        desc = fill_template(t, var_map)
        desc = desc.strip().lower()

        if desc not in seen:
            seen.add(desc)
            rows.append({"description": desc, "category": category})

        attempts += 1
        if attempts > 10000:
            break

random.shuffle(rows)
df = pd.DataFrame(rows)

# Save
out_path = os.path.join(os.path.dirname(__file__), "../data/classifier_training.csv")
df.to_csv(out_path, index=False)

print(f"Generated {len(df)} rows")
print(f"Category counts:")
print(df["category"].value_counts())
print(f"\nSample rows:")
print(df.head(10).to_string(index=False))
print(f"\nSaved to: {out_path}")