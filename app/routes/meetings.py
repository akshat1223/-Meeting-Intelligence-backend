import os
import uuid
from datetime import datetime

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.config import settings
from app.database.mongodb import get_database
from app.services.transcription import transcribe_audio
from app.services.meeting_analyzer import analyze_meeting
from app.services.meeting_query import answer_metting_question
from app.models.meeting import MeetingQueryRequest


router = APIRouter(prefix="/api/meetings")


@router.post("/upload")
async def upload_meeting(file: UploadFile = File(...)):

    if not file.filename.endswith((".mp3", ".wav")):
        raise HTTPException(
            400,
            "Only MP3 and WAV files are allowed"
        )

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    meeting_id = str(uuid.uuid4())

    file_path = os.path.join(
        settings.UPLOAD_DIR,
        meeting_id + os.path.splitext(file.filename)[1]
    )

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Speech to text
    transcript = await transcribe_audio(file_path)

    # AI analysis
    analysis = await analyze_meeting(transcript)

    # Save to MongoDB
    db = get_database()

    await db.meetings.insert_one({
        "meeting_id": meeting_id,
        "filename": file.filename,
        "transcript": transcript,
        "analysis": analysis.model_dump(),
        "created_at": datetime.now()
    })

    return {
        "message": "Meeting processed successfully",
        "meeting_id": meeting_id
    }


@router.get("")
async def get_meetings():

    db = get_database()

    meetings = []

    async for meeting in db.meetings.find(
        {},
        {"_id": 0}
    ):
        meetings.append(meeting)

    return meetings


@router.get("/{meeting_id}")
async def get_meeting(meeting_id: str):

    db = get_database()

    meeting = await db.meetings.find_one(
        {"meeting_id": meeting_id},
        {"_id": 0}
    )

    if not meeting:
        raise HTTPException(
            404,
            "Meeting not found"
        )

    return meeting


@router.post("/{meeting_id}/query")
async def query_meeting(
    meeting_id: str,
    data: MeetingQueryRequest
):

    db = get_database()

    meeting = await db.meetings.find_one(
        {"meeting_id": meeting_id},
        {"_id": 0}
    )

    if not meeting:
        raise HTTPException(
            404,
            "Meeting not found"
        )

    answer = await answer_metting_question(
        data.question,
        meeting["transcript"],
        meeting["analysis"]
    )

    return {
        "answer": answer
    }