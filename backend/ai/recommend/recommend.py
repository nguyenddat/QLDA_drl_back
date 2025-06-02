from models.user_subcriteria import User_SubCriteria
from models.subcriteria import SubCriteria
from database.init_db import get_db
from ai.recommend.services import get_event

difficulty_order = [12, 9, 11, 23]

db = next(get_db())
criteria_dict = {
    criteria.id: criteria for criteria in db.query(SubCriteria).filter(SubCriteria.id.in_(difficulty_order)).all()
}
db.close()

def recommend(db, user_id: int):
    user_subcriterias = db.query(User_SubCriteria).join(
        SubCriteria, SubCriteria.id == User_SubCriteria.subcriteria_id
    ).filter(
        User_SubCriteria.user_id == user_id,
        SubCriteria.required_evidence.is_(True)
    )

    user_sub_dict = {usc.subcriteria_id: usc for usc in user_subcriterias}
    message_parts = []

    for sub_id in difficulty_order:
        usc = user_sub_dict.get(sub_id)
        sub = criteria_dict.get(sub_id)

        if usc and usc.current_score < usc.max_score:
            remaining = usc.max_score - usc.current_score

            if sub_id == 11:
                message_parts.append(
                    f"- **{sub.description}**: Bạn nên tham gia các hoạt động công tác xã hội như hiến máu, ủng hộ người nghèo. "
                    f"Bạn cũng có thể quyên góp qua ứng dụng ngân hàng online và chụp lại biên nhận để nộp minh chứng."
                )

            elif sub_id == 12:
                message_parts.append(
                    f"- **{sub.description}**: Bạn hiện có {usc.current_score} điểm. "
                    f"Cần thêm {remaining} bài đăng tích cực về Học viện/Khoa trên mạng xã hội. "
                    f"Hãy đăng bài kèm hashtag và chụp ảnh làm minh chứng."
                )

            elif sub_id == 23:
                message_parts.append(
                    f"- **{sub.description}**: Hãy tham gia các cuộc thi học thuật, nghiên cứu khoa học hoặc hoạt động rèn luyện cấp Học viện để có cơ hội đạt điểm tối đa."
                )

            elif sub_id == 9:
                events = get_event.get_future_events_this_week(db)
                if events:
                    events_list = "\n  + " + "\n  + ".join(events)
                    message_parts.append(
                        f"- **{sub.description}**: Có các sự kiện nghề nghiệp trong tuần này mà bạn có thể tham gia:{events_list}. "
                        f"Nhớ chụp ảnh check-in hoặc giấy chứng nhận làm minh chứng."
                    )
                else:
                    message_parts.append(
                        f"- **{sub.description}**: Hiện tại chưa có sự kiện nào trong tuần này, vui lòng kiểm tra lại sau."
                    )

    if not message_parts:
        return {
            "message": "Tất cả tiêu chí đã đạt tối đa điểm hoặc không cần gợi ý thêm."
        }

    # Ghép toàn bộ message thành một đoạn
    final_message = "Dưới đây là các gợi ý để bạn cải thiện điểm rèn luyện:\n\n" + "\n\n".join(message_parts)

    return {
        "message": final_message
    }

