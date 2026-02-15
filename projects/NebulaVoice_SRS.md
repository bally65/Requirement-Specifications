# SRS: NebulaVoice - AI Speech-to-Text Engine

## 1. Overview
NebulaVoice is a lightweight, professional-grade speech-to-text (STT) web application designed for high-accuracy transcription of laboratory notes, meetings, and interviews.

## 2. Target Features
- **Engine Selection**: Support for local `Faster-Whisper` (Privacy-first) and `Groq/OpenAI` (Speed-first).
- **Real-time Recording**: Direct browser-based audio capture.
- **Batch Processing**: Upload multiple .wav/mp3 files and get bulk transcriptions.
- **Smart Formatting**: Use LLM (Gemini) to post-process text (punctuation, speaker diarization, summary).
- **Export Formats**: TXT, SRT (for video), and Markdown.

## 3. Technology Stack
- **Backend**: Python (FastAPI / Flask).
- **Frontend**: HTML5, Tailwind CSS, JavaScript (MediaRecorder API).
- **Inference**: Faster-Whisper (Local) or API-based.
- **Styling**: Minimalist "Laboratory Blue" (consistent with Spectral Analysis tool).

## 4. Implementation Plan
- Phase 1: Basic CLI tool for local transcription.
- Phase 2: Web UI for recording and file upload.
- Phase 3: Integration with Project Records Hub for automatic daily log transcription.

---
*Maintained by Antigravity Agent • 2026-02-13*
