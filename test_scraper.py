import time
import csv # thư viện ghi/đọc file csv
import requests # thư viện gửi yêu cầu HTTP lấy HTML về
from bs4 import BeautifulSoup # thư viện dào dữ liệu từ HTML

url = "http://quotes.toscrape.com"
index = 1

"""with open(...) as file: mở file và tự động đóng khi xong
"quotes.csv": Tên file đầu ra (sẽ nằm cùng thư mục với code).
mode="w": Chế độ write (ghi). Mỗi lần chạy code sẽ ghi đè file cũ. 
Nếu muốn thêm vào file cũ, dùng mode="a" (append). 
newline="": Bắt buộc khi ghi CSV trên Windows để tránh lỗi xuống dòng kép.
encoding='utf-8-sig': Mã hóa ký tự. Bắt buộc để hiển thị đúng tiếng Việt và ký tự đặc biệt"""
with open("quotes.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file) # Tạo object writer để ghi từng dòng vào file.

    writer.writerow(["No.", "Author", "Quote"])

    while url:
        print(f"Đang cào: {url}")

        """response: chứa phản hồi từ server:
        - status_code: 200 = ok. 404 = not_found. 403 = blocked.
        - text: nội dung HTML (chuỗi string)
        - headers: thông tin về response"""
        response = requests.get(url)

        """"html.parser": trình phân tích của Python
        BeautifulSoup(): nhận chuỗi HTML, biến thành object duyệt được"""
        soup = BeautifulSoup(response.text, "html.parser")

        """tìm các thẻ <div> có class="quote". 
        Kết quả = 1 list object BeautifulSoup đại diện cho các quote trên trang. 
        Dấu _ để tránh trùng với "class" - từ khóa Python"""
        for quote in soup.find_all("div", class_="quote"):
            author = quote.find("small", class_="author").text # .text: Lấy nội dung văn bản bên trong thẻ đó (bỏ hết HTML tags).
            text = quote.find("span", class_="text").text
            writer.writerow([index, author, text])
            index += 1

        # Tìm nút next
        next_button = soup.find("li", class_="next")
        if next_button:
            url = "http://quotes.toscrape.com" + next_button.a["href"]
        else:
            url = None

        time.sleep(1)