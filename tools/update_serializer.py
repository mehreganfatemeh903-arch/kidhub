from pathlib import Path

p = Path("catalog/serializers.py")
s = p.read_text(encoding="utf-8")

old = '''class ParentLullabyRecordingSerializer(serializers.ModelSerializer):
    def validate_child(self, value):
'''

new = '''class ParentLullabyRecordingSerializer(serializers.ModelSerializer):
    MAX_AUDIO_SIZE = 10 * 1024 * 1024
    ALLOWED_AUDIO_EXTENSIONS = {".webm", ".ogg", ".mp3", ".wav", ".mp4", ".m4a"}
    ALLOWED_AUDIO_TYPES = {
        "audio/webm",
        "audio/ogg",
        "audio/mpeg",
        "audio/wav",
        "audio/x-wav",
        "audio/mp4",
        "audio/x-m4a",
        "audio/m4a",
    }

    def validate_audio_file(self, value):
        if value.size > self.MAX_AUDIO_SIZE:
            raise serializers.ValidationError(
                "حجم فایل صوتی نباید بیشتر از 10 مگابایت باشد."
            )

        extension = Path(value.name).suffix.lower()
        content_type = getattr(value, "content_type", "")

        if extension not in self.ALLOWED_AUDIO_EXTENSIONS:
            raise serializers.ValidationError(
                "فرمت فایل صوتی مجاز نیست."
            )

        if content_type and content_type not in self.ALLOWED_AUDIO_TYPES:
            raise serializers.ValidationError(
                "نوع فایل صوتی مجاز نیست."
            )

        return value

    def validate_child(self, value):
'''

if old not in s:
    raise SystemExit("TARGET NOT FOUND")

p.write_text(s.replace(old, new, 1), encoding="utf-8")
print("Serializer updated successfully.")
