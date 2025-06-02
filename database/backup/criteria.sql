-- Tiêu chí 1
INSERT INTO criteria (name, min_score, max_score) VALUES
('Đánh giá về ý thức tham gia học tập', 0, 20) RETURNING id;

-- Giả sử ID của tiêu chí trên là 1
INSERT INTO subcriteria (parent_criteria_id, name, min_score, max_score, required_evidence, editable) VALUES
(1, 'Ý thức và thái độ trong học tập', 0, 3, false, true),
(1, 'Kết quả học tập trong kỳ học', 0, 10, false, true),
(1, 'Ý thức chấp hành tốt nội quy về các kỳ thi', -4, 4, false, true),
(1, 'Ý thức và thái độ tham gia các hoạt động ngoại khóa, nghiên cứu, chuyên môn, CLB', 0, 2, false, true),
(1, 'Tinh thần vượt khó, phấn đấu trong học tập', 0, 1, false, true);

-- Tiêu chí 2
INSERT INTO criteria (name, min_score, max_score) VALUES
('Đánh giá về ý thức chấp hành nội quy, quy chế, quy định trong Học viện', 0, 25) RETURNING id;

-- Giả sử ID là 2
INSERT INTO subcriteria (parent_criteria_id, name, min_score, max_score, required_evidence, editable) VALUES
(2, 'Thực hiện nghiêm túc các nội quy, quy chế của Học viện', 0, 15, false, true),
(2, 'Thực hiện quy định về nội trú, ngoại trú', -5, 0, false, true),
(2, 'Tham gia đầy đủ các buổi họp lớp/sinh hoạt đoàn thể', 0, 5, false, true),
(2, 'Tham gia hội thảo việc làm, định hướng nghề nghiệp', 0, 5, false, true);

-- Tiêu chí 3
INSERT INTO criteria (name, min_score, max_score) VALUES
('Đánh giá về ý thức và kết quả tham gia hoạt động chính trị - xã hội, văn hóa, thể thao, phòng chống tệ nạn', 0, 20) RETURNING id;

-- ID giả sử là 3
INSERT INTO subcriteria (parent_criteria_id, name, min_score, max_score, required_evidence, editable) VALUES
(3, 'Tham gia đầy đủ các hoạt động chính trị, xã hội, văn hóa, thể thao,...', 0, 10, false, false),
(3, 'Tham gia công tác xã hội như hiến máu, ủng hộ người nghèo,...', 0, 4, true, false),
(3, 'Tuyên truyền tích cực hình ảnh Học viện/Khoa trên MXH', 0, 3, true, false),
(3, 'Tích cực phòng chống tội phạm, tệ nạn, báo cáo hành vi sai phạm', 0, 3, false, false),
(3, 'Đưa thông tin sai lệch, bình luận tiêu cực về Học viện/Khoa', -10, 0, false, false);

-- Tiêu chí 4
INSERT INTO criteria (name, min_score, max_score) VALUES
('Đánh giá ý thức công dân trong quan hệ cộng đồng', 0, 25) RETURNING id;

-- ID giả sử là 4
INSERT INTO subcriteria (parent_criteria_id, name, min_score, max_score, required_evidence, editable) VALUES
(4, 'Chấp hành chủ trương, pháp luật của Nhà nước, Học viện, địa phương', 0, 8, false, true),
(4, 'Tuyên truyền chủ trương, vệ sinh môi trường, ý thức cộng đồng', 0, 5, false, true),
(4, 'Quan hệ đúng mực với giảng viên, cán bộ Học viện', 0, 5, false, true),
(4, 'Quan hệ tốt với bạn bè, tinh thần giúp đỡ lẫn nhau', 0, 5, false, true),
(4, 'Được biểu dương trong hoạt động công dân cộng đồng', 0, 2, false, false),
(4, 'Vi phạm an ninh, trật tự, ATGT', -5, 0, false, false);

-- Tiêu chí 5
INSERT INTO criteria (name, min_score, max_score) VALUES
('Đánh giá về ý thức và kết quả tham gia phụ trách lớp, đoàn thể và thành tích học tập, rèn luyện', 0, 10) RETURNING id;

-- ID giả sử là 5
INSERT INTO subcriteria (parent_criteria_id, name, min_score, max_score, required_evidence, editable) VALUES
(5, 'Sinh viên được Học viện phân công làm lớp trưởng, lớp phó; bí thư, phó bí thư chi đoàn, BCH đoàn Học viện/khoa; BCH Hội sinh viên Học viện/khoa; chủ nhiệm, phó chủ nhiệm các các Câu lạc bộ, đội nhóm trực thuộc Học viện/khoa được tập thể sinh viên và đơn vị quản lý ghi nhận hoàn thành nhiệm vụ.', 0, 4, false, false),
(5, 'Thành viên tham gia các Câu lạc bộ, đội nhóm trực thuộc Học viện /khoa được tập thể sinh viên và đơn vị quản lý ghi nhận hoàn thành tốt nhiệm vụ; sinh viên tham gia tổ chức các chương trình, là cộng tác viên tham gia tích cực vào các hoạt động chung cấp Học viện, khoa.', 0, 3, false, false),
(5, 'Sinh viên đạt thành tích đặc biệt trong học tập, rèn luyện', 0, 3, true, false);