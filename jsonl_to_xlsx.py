import json

try:
    import openpyxl
except ImportError:
    print("Thiếu thư viện. Chạy: pip install openpyxl")
    exit()

INPUT  = "E:/company_data.jsonl"
OUTPUT = "E:/masothue_nganh_2392.xlsx"

fields  = ["name", "intl_name", "mst", "address", "status", "rep", "phone", "email"]
headers = ["Company Name", "International Name", "Tax ID", "Address",
           "Status", "Legal Representative", "Phone", "Email"]

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "masothue_2392"
ws.append(headers)

# Làm header đậm
from openpyxl.styles import Font
for cell in ws[1]:
    cell.font = Font(bold=True)

count = 0
skipped = 0

with open(INPUT, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
            name = d.get("name", "")
            # Bỏ qua dòng lỗi (trang không load được)
            if not name or "can't be reached" in name.lower() or len(name) < 3:
                skipped += 1
                continue
            ws.append([d.get(k, "") for k in fields])
            count += 1
        except json.JSONDecodeError:
            skipped += 1

wb.save(OUTPUT)
print(f"XONG! {count} công ty → {OUTPUT}")
if skipped:
    print(f"(Bỏ qua {skipped} dòng lỗi)")
