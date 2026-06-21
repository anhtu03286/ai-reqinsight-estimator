from dataclasses import dataclass
import uuid


@dataclass
class DocumentParsedEvent:
    document_id: str
    project_id: str
    organization_id: str


@dataclass
class DocumentChunkedEvent:
    document_id: str
    project_id: str
    organization_id: str
    chunk_count: int


@dataclass
class AnalysisCompletedEvent:
    project_id: str
    organization_id: str
    result_count: int
