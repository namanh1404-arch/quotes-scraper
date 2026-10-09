import csv # thư viện ghi/đọc file csv
import requests # thư viện gửi yêu cầu HTTP lấy HTML về
from bs4 import BeautifulSoup # thư viện dào dữ liệu từ HTML

# 1. Gửi yêu cầu lấy nội dung trang web về
url = "http://quotes.toscrape.com/"

# response: chứa phản hồi từ server:
#   - status_code: 200 = ok. 404 = not_found. 403 = blocked.
#   - text: nội dung HTML (chuỗi string)
#   - headers: thông tin về response
response = requests.get(url)

# 2. Xử lý dữ liệu
# "html.parser": trình phân tích của Python
# BeautifulSoup(): nhận chuỗi HTML, biến thành object duyệt được
soup = BeautifulSoup(response.text, "html.parser")

# tìm các thẻ <div> có class="quote". 
# Kết quả = 1 list object BeautifulSoup đại diện cho các quote trên trang. 
# Dấu _ để tránh trùng với "class" - từ khóa Python
quotes = soup.find_all("div", class_="quote")

# with open(...) as file: mở file và tự động đóng khi xong
# "quotes.csv": Tên file đầu ra (sẽ nằm cùng thư mục với code).
# mode="w": Chế độ write (ghi). Mỗi lần chạy code sẽ ghi đè file cũ. 
# Nếu muốn thêm vào file cũ, dùng mode="a" (append). 
# newline="": Bắt buộc khi ghi CSV trên Windows để tránh lỗi xuống dòng kép.
# encoding='utf-8-sig': Mã hóa ký tự. Bắt buộc để hiển thị đúng tiếng Việt và ký tự đặc biệt
with open("quotes.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file) # Tạo object writer để ghi từng dòng vào file.

    # Ghi tiêu đề cột
    writer.writerow(["STT", "Author", "Quote"])

    for index, quote in enumerate(quotes, start=1): # Vừa lặp qua list quotes, vừa đếm số thứ tự bắt đầu từ 1.
        # Tìm thẻ <small class="author"> chứa tên tác giả.
        # .text: Lấy nội dung văn bản bên trong thẻ đó (bỏ hết HTML tags).
        author = quote.find("small", class_="author").text

        # Lấy nội dung câu trích dẫn
        text = quote.find("span", class_="text").text

        # Ghi dữ liệu vào file CSV
        writer.writerow([index, author, text])