import sys
import uuid
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

sys.path.insert(0, str(Path(__file__).parent / "src"))

from integrity.blockchain import LocalHashchain
from integrity.hasher import merkle_root, sha256_hash
from pipeline.processor import process_batch, process_log_line
from storage.models import Base, NormalizedEvent, RawBatchPayload, RawEvent


def test_raw_event_text_and_normalized_copy_preserve_whitespace() -> None:
    raw_line = "  CEF:0|Cisco|ASA|9.1|106023|Denied|5|src=10.0.0.1 dst=8.8.8.8  \t"
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        event = process_log_line(raw_line, "test", uuid.uuid4(), session)
        session.flush()

        raw = session.get(RawEvent, uuid.UUID(event["ulpf_raw_event_id"]))
        normalized = session.get(NormalizedEvent, uuid.UUID(event["ulpf_event_id"]))

        assert raw is not None
        assert raw.raw_data == raw_line
        assert raw.sha256_hash == sha256_hash(raw_line)
        assert event["raw_data"] == raw_line
        assert normalized is not None
        assert normalized.ocsf_json["raw_data"] == raw_line

    engine.dispose()


def test_batch_payload_preserves_newlines_and_blank_lines(tmp_path: Path) -> None:
    raw_line = "  CEF:0|Cisco|ASA|9.1|106023|Denied|5|src=10.0.0.1 dst=8.8.8.8  \t"
    raw_payload = raw_line + "\r\n\r\n\t\n"
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        result = process_batch(
            raw_lines=raw_payload.splitlines(),
            source_file="test",
            session=session,
            blockchain=LocalHashchain(str(tmp_path / "chain.jsonl")),
            raw_payload=raw_payload,
        )
        session.flush()

        saved_payload = session.get(RawBatchPayload, uuid.UUID(result["batch_id"]))
        raw_events = session.query(RawEvent).filter_by(
            batch_id=uuid.UUID(result["batch_id"])
        ).all()

        assert saved_payload is not None
        assert saved_payload.raw_payload == raw_payload
        assert saved_payload.sha256_hash == sha256_hash(raw_payload)
        assert len(raw_events) == 1
        assert raw_events[0].raw_data == raw_line
        assert result["merkle_root"] == merkle_root([
            raw_events[0].sha256_hash,
            sha256_hash(raw_payload),
        ])

    engine.dispose()
