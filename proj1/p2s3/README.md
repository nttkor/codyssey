## 반달곰 커피 홈페이지 (H2 헤더)

참조링크: https://반달곰 커피

문구: 오디오 출력 소스코드

```python
lang = request.args.get('lang', DEFAULT_LANG)
fp = BytesIO()
gTTS(text, "com", lang).write_to_fp(fp)
encoded_audio_data = base64.b64encode(fp.getvalue())
david.jpg 파일을 이미지로 삽입한다.
'''