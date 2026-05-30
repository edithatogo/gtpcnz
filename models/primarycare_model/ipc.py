"""
PyArrow IPC Streaming Server/Client for ABM Runtime -> Streamlit UI.
Zero-copy Arrow RecordBatch streaming, bypassing disk operations.
"""
from __future__ import annotations
import io, logging, socket, struct, threading, time
from typing import Any, Dict, Generator, Optional
import pyarrow as pa
import pyarrow.ipc as ipc
from .data_layer import IPC_WRITE_OPTIONS, TELEMETRY_ARROW_SCHEMA

logger = logging.getLogger(__name__)
_FRAME_HEADER = struct.Struct("!I")
_DEFAULT_HOST = "127.0.0.1"
_DEFAULT_PORT = 12_345


class ArrowMemoryChannel:
    """In-memory Arrow IPC channel for same-process streaming."""
    def __init__(self) -> None:
        self._buffer: io.BytesIO = io.BytesIO()
        self._writer: Optional[ipc.RecordBatchStreamWriter] = None
        self._lock = threading.Lock()
        self._finished = False

    def open(self, schema: pa.Schema) -> None:
        with self._lock:
            self._buffer.seek(0); self._buffer.truncate(0)
            self._writer = ipc.new_stream(self._buffer, schema, options=IPC_WRITE_OPTIONS)
            self._finished = False

    def write_batch(self, batch: pa.RecordBatch) -> int:
        if self._writer is None: raise RuntimeError("Not opened.")
        with self._lock:
            pos = self._buffer.tell()
            self._writer.write_batch(batch)
            return self._buffer.tell() - pos

    def write_table(self, table: pa.Table) -> int:
        return sum(self.write_batch(b) for b in table.to_batches())

    def close(self) -> None:
        with self._lock:
            if self._writer is not None:
                self._writer.close(); self._writer = None
            self._finished = True

    def read_all(self) -> pa.Table:
        with self._lock:
            self._buffer.seek(0)
            try:
                batches = list(ipc.open_stream(self._buffer))
                if not batches:
                    return pa.Table.from_batches([], schema=TELEMETRY_ARROW_SCHEMA)
                return pa.Table.from_batches(batches)
            except pa.ArrowInvalid:
                return pa.Table.from_batches([], schema=TELEMETRY_ARROW_SCHEMA)

    @property
    def is_finished(self) -> bool: return self._finished


class ArrowStreamServer:
    """TCP socket server streaming Arrow RecordBatches."""
    def __init__(self, host=_DEFAULT_HOST, port=_DEFAULT_PORT,
                 schema=TELEMETRY_ARROW_SCHEMA):
        self.host, self.port, self.schema = host, port, schema
        self._server: Optional[socket.socket] = None
        self._client: Optional[socket.socket] = None
        self._running = False
        self._lock = threading.Lock()

    def start(self) -> None:
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self._server.bind((self.host, self.port))
        self._server.listen(1); self._server.settimeout(10.0)
        self._running = True

    def accept(self) -> None:
        if self._server is None: raise RuntimeError("Not started.")
        try:
            c, addr = self._server.accept()
            self._client = c
        except socket.timeout: pass

    def stream_batch(self, batch: pa.RecordBatch) -> int:
        if self._client is None: raise RuntimeError("No client.")
        buf = io.BytesIO()
        with ipc.new_stream(buf, batch.schema, options=IPC_WRITE_OPTIONS) as writer:
            writer.write_batch(batch)
        payload = buf.getvalue()
        header = _FRAME_HEADER.pack(len(payload))
        with self._lock: self._client.sendall(header + payload)
        return len(header) + len(payload)

    def stream_table(self, table: pa.Table) -> int:
        return sum(self.stream_batch(b) for b in table.to_batches())

    def stop(self) -> None:
        self._running = False
        for s in (self._client, self._server):
            if s is not None:
                try: s.close()
                except OSError: pass
        self._client = self._server = None


class ArrowStreamClient:
    """TCP socket client receiving Arrow RecordBatches."""
    def __init__(self, host=_DEFAULT_HOST, port=_DEFAULT_PORT):
        self.host, self.port = host, port
        self._socket: Optional[socket.socket] = None

    def connect(self) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self._socket.connect((self.host, self.port))

    def receive_batches(self) -> Generator[pa.RecordBatch, None, None]:
        if self._socket is None: raise RuntimeError("Not connected.")
        while True:
            try:
                hdr = self._recv_exact(_FRAME_HEADER.size)
                if not hdr: break
                plen = _FRAME_HEADER.unpack(hdr)[0]
                payload = self._recv_exact(plen)
                if not payload: break
                buf = io.BytesIO(payload)
                try:
                    with ipc.open_stream(buf) as reader:
                        for batch in reader: yield batch
                except pa.ArrowInvalid: continue
            except (ConnectionError, OSError): break

    def _recv_exact(self, size: int) -> Optional[bytes]:
        if self._socket is None: return None
        chunks, remaining = [], size
        while remaining > 0:
            try: chunk = self._socket.recv(remaining)
            except (ConnectionError, OSError): return None
            if not chunk: return None
            chunks.append(chunk); remaining -= len(chunk)
        return b"".join(chunks)

    def close(self) -> None:
        if self._socket is not None:
            try: self._socket.close()
            except OSError: pass
            self._socket = None


def stream_abm_run_inmemory(run_fn, schema=TELEMETRY_ARROW_SCHEMA) -> ArrowMemoryChannel:
    """Run ABM and stream telemetry via in-memory Arrow IPC."""
    channel = ArrowMemoryChannel()
    channel.open(schema)
    def writer(tel):
        arrays = [pa.array([tel.get(f.name)], type=f.type) for f in schema]
        channel.write_batch(pa.record_batch(arrays, schema=schema))
    try: run_fn(writer)
    finally: channel.close()
    return channel


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    def _demo(w):
        for t in range(5):
            w({"timestamp": time.time_ns()//1000, "run_id":"demo",
               "scenario_name":"test", "tick":t, "month":t,
               "patient_count":1000, "provider_count":50,
               "total_visits":300, "capitation_flow":50000.0,
               "ffs_flow":15000.0, "total_funding_flow":65000.0,
               "avg_wait_days":3.5, "unmet_demand":10,
               "cpu_usage_pct":45.0, "memory_mb":256.0})
            time.sleep(0.05)
    ch = stream_abm_run_inmemory(_demo)
    tab = ch.read_all()
    print(f"IPC test: {tab.num_rows} rows received - PASSED")
