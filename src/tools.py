"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Trợ lý Quản lý Thư viện & Tài liệu
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS
# ==============================================================================

TOOLS_SCHEMA = [

    # --------------------------------------------------------------------------
    # TOOL 1: Tra cứu thông tin và vị trí tài liệu
    # --------------------------------------------------------------------------
    {
        "name": "document_query",
        "description": "Tra cứu thông tin tài liệu trong thư viện bằng mã tài liệu, bao gồm tên tài liệu, tác giả, vị trí và tình trạng mượn/trả.",
        "parameters": {
            "type": "object",
            "properties": {
                "document_id": {
                    "type": "string",
                    "description": "Mã tài liệu cần tra cứu (ví dụ: 'BK2026001')"
                }
            },
            "required": ["document_id"]
        }
    },

    # --------------------------------------------------------------------------
    # TOOL 2: Kiểm tra tài liệu người dùng đang mượn
    # --------------------------------------------------------------------------
    {
        "name": "borrow_query",
        "description": "Tra cứu thông tin các tài liệu mà sinh viên đang mượn, bao gồm ngày mượn, hạn trả và số lần đã gia hạn.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên cần tra cứu (ví dụ: 'SV2026001')"
                }
            },
            "required": ["student_id"]
        }
    },

    # --------------------------------------------------------------------------
    # TOOL 3: Gia hạn tài liệu
    # --------------------------------------------------------------------------
    {
        "name": "renew_document",
        "description": "Gia hạn thời gian mượn tài liệu cho sinh viên nếu tài liệu đủ điều kiện gia hạn.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên đang mượn tài liệu"
                },
                "document_id": {
                    "type": "string",
                    "description": "Mã tài liệu cần gia hạn (ví dụ: 'BK2026001')"
                }
            },
            "required": ["student_id", "document_id"]
        }
    }
]


# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU THƯ VIỆN
# ==============================================================================

MOCK_DOCUMENT_DATABASE = {

    "BK2026001": {
        "title": "Introduction to Artificial Intelligence",
        "author": "Stuart Russell & Peter Norvig",
        "location": "Thư viện tầng 2 - Kệ AI-03",
        "status": "BORROWED",
        "borrowed_by": "SV2026001",
        "borrow_date": "01/09/2026",
        "due_date": "20/09/2026",
        "renewal_count": 0,
        "max_renewals": 2
    },

    "BK2026002": {
        "title": "Python Programming",
        "author": "Mark Lutz",
        "location": "Thư viện tầng 1 - Kệ CS-05",
        "status": "AVAILABLE",
        "borrowed_by": None,
        "borrow_date": None,
        "due_date": None,
        "renewal_count": 0,
        "max_renewals": 2
    },

    "BK2026003": {
        "title": "Database System Concepts",
        "author": "Abraham Silberschatz",
        "location": "Thư viện tầng 2 - Kệ DB-02",
        "status": "BORROWED",
        "borrowed_by": "SV2026002",
        "borrow_date": "05/09/2026",
        "due_date": "15/09/2026",
        "renewal_count": 2,
        "max_renewals": 2
    }
}


# ==============================================================================
# 3. DỮ LIỆU SINH VIÊN
# ==============================================================================

MOCK_STUDENT_DATABASE = {

    "SV2026001": {
        "full_name": "Nguyễn Văn An",
        "email": "an.nv@vinuni.edu.vn"
    },

    "SV2026002": {
        "full_name": "Trần Thị Bình",
        "email": "binh.tt@vinuni.edu.vn"
    }
}


# ==============================================================================
# 4. TOOL: TRA CỨU TÀI LIỆU
# ==============================================================================

def execute_document_query(document_id: str) -> str:
    """Tra cứu thông tin và vị trí tài liệu."""

    document_id = document_id.strip().upper()

    document = MOCK_DOCUMENT_DATABASE.get(document_id)

    if document:
        return json.dumps({
            "status": "SUCCESS",
            "document_id": document_id,
            "data": document
        }, ensure_ascii=False)

    return json.dumps({
        "status": "NOT_FOUND",
        "message": f"Không tìm thấy tài liệu có mã '{document_id}'."
    }, ensure_ascii=False)


# ==============================================================================
# 5. TOOL: TRA CỨU TÀI LIỆU ĐANG MƯỢN
# ==============================================================================

def execute_borrow_query(student_id: str) -> str:
    """Tra cứu các tài liệu sinh viên đang mượn."""

    student_id = student_id.strip().upper()

    if student_id not in MOCK_STUDENT_DATABASE:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy sinh viên có mã '{student_id}'."
        }, ensure_ascii=False)

    borrowed_documents = []

    for document_id, document in MOCK_DOCUMENT_DATABASE.items():

        if document["borrowed_by"] == student_id:
            borrowed_documents.append({
                "document_id": document_id,
                "title": document["title"],
                "borrow_date": document["borrow_date"],
                "due_date": document["due_date"],
                "renewal_count": document["renewal_count"],
                "max_renewals": document["max_renewals"]
            })

    return json.dumps({
        "status": "SUCCESS",
        "student_id": student_id,
        "data": borrowed_documents
    }, ensure_ascii=False)


# ==============================================================================
# 6. TOOL: GIA HẠN TÀI LIỆU
# ==============================================================================

def execute_renew_document(
    student_id: str,
    document_id: str
) -> str:
    """Gia hạn tài liệu nếu đủ điều kiện."""

    student_id = student_id.strip().upper()
    document_id = document_id.strip().upper()

    # Kiểm tra sinh viên
    if student_id not in MOCK_STUDENT_DATABASE:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy sinh viên có mã '{student_id}'."
        }, ensure_ascii=False)

    # Kiểm tra tài liệu
    document = MOCK_DOCUMENT_DATABASE.get(document_id)

    if not document:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy tài liệu có mã '{document_id}'."
        }, ensure_ascii=False)

    # Kiểm tra người đang mượn
    if document["borrowed_by"] != student_id:
        return json.dumps({
            "status": "REJECTED",
            "reason": "NOT_BORROWED_BY_STUDENT",
            "message": "Sinh viên không phải người đang mượn tài liệu này."
        }, ensure_ascii=False)

    # Kiểm tra trạng thái
    if document["status"] != "BORROWED":
        return json.dumps({
            "status": "REJECTED",
            "reason": "DOCUMENT_NOT_BORROWED",
            "message": "Tài liệu hiện không ở trạng thái đang được mượn."
        }, ensure_ascii=False)

    # Kiểm tra số lần gia hạn
    if document["renewal_count"] >= document["max_renewals"]:
        return json.dumps({
            "status": "REJECTED",
            "reason": "MAX_RENEWAL_REACHED",
            "message": "Tài liệu đã đạt số lần gia hạn tối đa."
        }, ensure_ascii=False)

    # Thực hiện gia hạn
    document["renewal_count"] += 1

    return json.dumps({
        "status": "SUCCESS",
        "student_id": student_id,
        "document_id": document_id,
        "title": document["title"],
        "renewal_count": document["renewal_count"],
        "max_renewals": document["max_renewals"],
        "due_date": document["due_date"],
        "message": (
            f"Gia hạn thành công tài liệu '{document['title']}' "
            f"cho sinh viên {student_id}."
        )
    }, ensure_ascii=False)


# ==============================================================================
# 7. TOOL ROUTER
# ==============================================================================

TOOL_ROUTER = {
    "document_query": execute_document_query,
    "borrow_query": execute_borrow_query,
    "renew_document": execute_renew_document
}


def dispatch_tool_call(
    tool_name: str,
    arguments: Dict[str, Any]
) -> str:
    """Hàm trung chuyển thực thi Tool."""

    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)

        except Exception as e:
            return json.dumps({
                "status": "EXECUTION_ERROR",
                "error": str(e)
            }, ensure_ascii=False)

    return json.dumps({
        "status": "UNKNOWN_TOOL",
        "error": f"Tool '{tool_name}' không tồn tại!"
    }, ensure_ascii=False)