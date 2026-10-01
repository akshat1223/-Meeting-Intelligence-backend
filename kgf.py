from gtts import gTTS

# Meeting transcript content
transcript_text = """
Manager: Good morning everyone. We need to finalize the beta launch by 15 October.
Rahul: I can complete the payment API integration by 10 October.
Priya: I will prepare the QA test cases by 12 October.
Manager: Rahul, please also investigate the timeout issue reported by the mobile team.
Rahul: Sure, I will check the timeout issue tomorrow.
Priya: The product pricing is still not finalized.
Manager: Let's discuss pricing in the next meeting. For now, the beta launch date remains 15 October.
Rahul: I also need access to the payment gateway test account.
Manager: I will provide Rahul access to the test account today.
Priya: Once the QA cases are ready, I will share them with Rahul for integration testing.
Manager: Good. Let's review the remaining items in the next meeting.
"""

# Convert text to audio
tts = gTTS(text=transcript_text, lang='en', tld='co.uk')
tts.save("meeting_transcript.mp3")

print("Saved audio file as meeting_transcript.mp3")