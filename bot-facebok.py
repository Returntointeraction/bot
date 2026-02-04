from flask import Flask, request
import requests

app = Flask(__name__)

# ضع البيانات الخاصة بك هنا
ACCESS_TOKEN = 'TOKEN_الذي_نسخته_من_المستكشف'
VERIFY_TOKEN = 'momeen_bot_123' # كلمة سر من اختيارك للربط

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # التحقق من الرابط عند الربط لأول مرة
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "خطأ في التحقق", 403

    # استقبال التعليق والرد عليه
    data = request.json
    if data.get('object') == 'page':
        for entry in data['entry']:
            for change in entry['changes']:
                if change['value'].get('item') == 'comment' and change['value'].get('verb') == 'add':
                    comment_id = change['value']['comment_id']
                    # إرسال الرد
                    url = f"https://graph.facebook.com/v19.0/{comment_id}/comments"
                    requests.post(url, data={'message': 'أهلاً بك! شكراً لتعليقك.', 'access_token': ACCESS_TOKEN})
    return "OK", 200

if __name__ == '__main__':
    app.run(port=5000)