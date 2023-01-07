import os
import json
import time
import bech32
from binascii import hexlify
from fastapi import APIRouter
from subprocess import check_output

home = os.path.expanduser("~")
router = APIRouter()


@router.get("/api/nostr/note")
def get_note(
    note_id: str = "d9bd9c124d1920f7bb01de6737bfb2d5e2db4826a6059235c55a7ba66e4d2a07",
):
    note_id = note_id.strip()
    if note_id.startswith("note1"):
        hrp, data = bech32.bech32_decode(note_id)
        bts = bech32.convertbits(data, 5, 8)
        note_id = hexlify(bytes(bts))[:-2].decode("utf8")
    print(note_id)
    out = check_output(
        [
            f"{home}/.nvm/versions/node/v16.14.2/bin/node",
            f"{home}/dev/nostr-js/test/query.js",
            note_id,
        ]
    )
    return json.loads(out)
