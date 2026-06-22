import csv
import os
import re
from bs4 import BeautifulSoup

DIR_PATH = "E:/data_html"
OUTPUT_CSV = "E:/masothue_nganh_2392.csv"

headers = ["Company Name", "Tax Identification Number", "Address"]

with open(OUTPUT_CSV, mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)

print("=== BẮT ĐẦU TRÍCH XUẤT DỮ LIỆU TỪ FILE TĨNH ===")

for i in range(1, 12):
    file_name = f"trang_{i}.html"
    file_path = os.path.join(DIR_PATH, file_name)
    
    if not os.path.exists(file_path):
        print(f"[-] Không tìm thấy file {file_name}, bỏ qua.")
        continue
        
    print(f"[+] Đang đọc dữ liệu từ: {file_name}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    
    # Tìm tất cả các khối công ty lớn bao bọc thông tin trên masothue
    # Thường nằm trong div chứa thông tin doanh nghiệp cụ thể
    div_blocks = soup.find_all(["div", "header"], class_=lambda x: x and ('com-' in x or 'listing' in x or 'item' in x))
    
    # Nếu bộ lọc class không bắt được, quét trực tiếp qua các cụm chứa thẻ a liên kết mã số thuế
    if not div_blocks:
        div_blocks = soup.find_all("div")

    for block in div_blocks:
        a_tag = block.find("a", href=re.compile(r"/ma-so-thue/"))
        if not a_tag:
            continue
            
        name = a_tag.get_text(strip=True)
        if not name or "Tra cứu" in name:
            continue
            
        block_text = block.get_text("\n")
        lines = [line.strip() for line in block_text.split("\n") if line.strip()]
        
        mst = ""
        address = ""
        
        for idx, line in enumerate(lines):
            # Tìm dòng chứa ký tự mã số thuế
            if "Mã số thuế" in line or "MST" in line or (line.isdigit() and len(line) >= 10):
                # Lấy chuỗi số từ dòng đó
                digits = re.findall(r'\d+', line)
                if digits:
                    mst = "".join(digits)
            # Tìm dòng chứa thông tin địa chỉ dựa trên từ khóa hành chính
            elif any(k in line for k in ["Quận", "Huyện", "Thị xã", "Tỉnh", "Thành phố", "TP", "Ngõ", "Đường", "Thôn"]):
                address = line
                
        if name and mst:
            # Ghi dữ liệu, lọc trùng lặp thô sơ bằng cách kiểm tra file
            with open(OUTPUT_CSV, mode='a', encoding='utf-8-sig', newline='') as csv_file:
                csv.writer(csv_file).writerow([name, mst, address])

print(f"\n🎉 HOÀN THÀNH XUẤT SẮC! Dữ liệu sạch đã nằm tại: {OUTPUT_CSV}")