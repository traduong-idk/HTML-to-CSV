import json
import csv

INPUT  = "E:/company_data.jsonl"
OUTPUT = "E:/masothue_nganh_2392.csv"

headers = ["Company Name (VN)", "International Name", "Tax ID", "Address", "Representative", "Phone"]
fields  = ["name", "intl_name", "mst", "address", "rep", "phone"]

with open(OUTPUT, "w", encoding="utf-8-sig", newline="") as f:
    csv.writer(f).writerow(headers)

count  = 0
errors = 0

with open(INPUT, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
            with open(OUTPUT, "a", encoding="utf-8-sig", newline="") as cf:
                csv.writer(cf).writerow([d.get(k, "") for k in fields])
            count += 1
        except json.JSONDecodeError:
            errors += 1

print(f"XONG! {count} công ty → {OUTPUT}")
if errors:
    print(f"(Bỏ qua {errors} dòng lỗi JSON)")
