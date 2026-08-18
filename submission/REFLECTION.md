# Reflection — Lakehouse Anti-Pattern

Trong năm Lakehouse Anti-Patterns, rủi ro lớn nhất của team mình là **Small-Files Problem**. Pipeline observability nhận dữ liệu theo streaming hoặc nhiều micro-batch; nếu mỗi batch ghi một file Parquet nhỏ, số file và chi phí metadata tăng nhanh. Truy vấn phải mở nhiều file, làm latency và chi phí đọc tăng, trong khi việc partition quá chi tiết còn làm tình hình nghiêm trọng hơn.

Giải pháp là chọn kích thước micro-batch hợp lý, tránh partition theo các cột có độ phân biệt cao, và đặt lịch compaction/OPTIMIZE sau ingest. Với dữ liệu cần truy vấn theo khóa, kết hợp clustering hoặc Z-ORDER sau compaction. Team cũng cần monitor numFiles, kích thước file trung bình, thời gian truy vấn và tỷ lệ file bị prune; đặt alert khi các ngưỡng vượt mức. Mỗi job phải idempotent để retry không tạo thêm file rác hoặc bản ghi trùng.
