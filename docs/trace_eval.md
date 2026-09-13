# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Hà Thị Mỹ Linh 
> **Mã Sinh Viên / Mã Học viên:** 2A202602619  
> **Chủ đề Lựa chọn:** *Trợ lý Quản lý Thư viện & Tài liệu:* Tra cứu vị trí sách, tình trạng mượn/trả và gia hạn tài liệu.

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 4/ 5 | Bài toán có yêu cầu chia nhỏ nhiều bước suy luận nối tiếp nhau không? |Agent phải thực hiện chuỗi bước: xác định tài liệu → tra cứu cơ sở dữ liệu → kiểm tra vị trí/trạng thái → kiểm tra thông tin người mượn → xác định điều kiện gia hạn → thực hiện gia hạn nếu đủ điều kiện → phản hồi kết quả. Tuy nhiên, một số yêu cầu đơn giản như “sách này ở đâu?” chỉ cần vài bước.
| **2. Tool Interaction** | 5/ 5 | Hệ thống có cần kết nối với MCP Server / Cơ sở dữ liệu bên ngoài không? |Đây là điểm mạnh nhất của bài toán. Agent cần tương tác với MCP Server/API hoặc cơ sở dữ liệu thư viện để tra cứu catalogue, vị trí kệ, tình trạng mượn/trả, hạn trả và thực hiện thao tác gia hạn. Các hành động này không nên được mô phỏng hoàn toàn bằng LLM.
| **3. Dynamic Decision** | 5/ 5 | Bước tiếp theo có phụ thuộc vào kết quả quan sát bước trước không? |Bước tiếp theo phụ thuộc trực tiếp vào kết quả quan sát. Ví dụ: nếu tài liệu đang có người mượn → kiểm tra hạn trả; nếu tài liệu thuộc diện không được gia hạn → từ chối; nếu đã quá số lần gia hạn → thông báo không thể gia hạn; nếu đủ điều kiện → thực hiện gia hạn và cập nhật hệ thống.
| **4. Long Horizon Goal** | 4/ 5 | Hệ thống có phải giữ mục tiêu xuyên suốt qua nhiều lượt xử lý không? |Agent có thể phải duy trì mục tiêu qua nhiều thao tác và nhiều lượt trao đổi, đặc biệt với các yêu cầu như “tìm tất cả tài liệu tôi đang mượn và gia hạn những tài liệu đủ điều kiện”. Tuy nhiên, phần lớn tác vụ thư viện vẫn có phạm vi tương đối ngắn, nên chưa đạt mức 5.
| **TỔNG ĐIỂM AGENTIC FIT** | **18/ 20** | *Nếu tổng điểm > 12/20: Bài toán rất phù hợp triển khai Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "Tôi muốn gia hạn cuốn sách BK2026001 đang mượn. Hãy kiểm tra tình trạng mượn và điều kiện gia hạn trước, nếu đủ điều kiện thì thực hiện gia hạn cho tôi.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "document_query",
    "arguments": {
      "document_id": "BK2026001"
    },
    "observation": {
      "status": "SUCCESS",
      "document_id": "BK2026001",
      "data": {
        "title": "Introduction to Artificial Intelligence",
        "author": "Stuart Russell & Peter Norvig",
        "location": "Thư viện tầng 2 - Kệ AI-03",
        "status": "BORROWED",
        "borrowed_by": "SV2026001",
        "borrow_date": "01/09/2026",
        "due_date": "20/09/2026",
        "renewal_count": 1,
        "max_renewals": 2
      }
    },
    "latency_ms": 1314.31
  },
  {
    "step": 2,
    "query": "Tôi muốn gia hạn cuốn sách BK2026001 đang mượn. Hãy kiểm tra tình trạng mượn và điều kiện gia hạn trước, nếu đủ điều kiện thì thực hiện gia hạn cho tôi.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "renew_document",
    "arguments": {
      "document_id": "BK2026001",
      "student_id": "SV2026001"
    },
    "observation": {
      "status": "SUCCESS",
      "student_id": "SV2026001",
      "document_id": "BK2026001",
      "title": "Introduction to Artificial Intelligence",
      "renewal_count": 2,
      "max_renewals": 2,
      "due_date": "20/09/2026",
      "message": "Gia hạn thành công tài liệu 'Introduction to Artificial Intelligence' cho sinh viên SV2026001."
    },
    "latency_ms": 1682.28
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [ x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 6 lượt.
- **Kết quả đẩy Repo nộp bài:** [ x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
