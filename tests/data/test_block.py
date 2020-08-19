# -*- coding: utf-8 -*-

import base64

from icon.data.address import Address
from icon.data.block import Block
from icon.data.utils import hex_to_bytes, bytes_to_hex


class TestBlock(object):
    def test_from_dict_v0_5(self):
        version = "0.5"
        signature = "QotwNw1J7HufCDISyHSSMSPlomS07tM0fZzFfIWg8aRFW90zFfFfYrV1RnwwL1Bb0FEQ7tw4XIDfdNwq+pkHtgE="
        block_hash: bytes = hex_to_bytes(
            "c89185360aae47c3a3e633737414e3efce557af165ba976222dad1939e39aec0"
        )
        prev_block_hash: bytes = hex_to_bytes(
            "a7fdb4d8207f832a2dbb716c0a5d43cf6f52fc69f375b36a02979b0233b43921"
        )
        merkle_tree_root_hash: bytes = (
            hex_to_bytes(
                "49c072898557955cef50b2bc2e5a62e20ace4a49961624605a0994dbd62286c5"
            )
        )
        block_height: int = 17105728
        timestamp = 1586090680791618
        peer_id = Address.from_string("hx6f89b2c25c15f6294c79810221753131067ed3f8")
        next_leader = Address.from_string("hx6f89b2c25c15f6294c79810221753131067ed3f8")

        block_dict = {
            "version": version,
            "height": block_height,
            "signature": signature,
            "prev_block_hash": bytes_to_hex(prev_block_hash, prefix=""),
            "merkle_tree_root_hash": bytes_to_hex(merkle_tree_root_hash),
            "time_stamp": timestamp,
            "block_hash": bytes_to_hex(block_hash, prefix=""),
            "peer_id": str(peer_id),
            "next_leader": str(next_leader),
            "confirmed_transaction_list": [
                {
                    "version": "0x3",
                    "timestamp": "0x5a28a839c3242",
                    "dataType": "base",
                    "data": {
                        "prep": {
                            "irep": "0x92b17680aa306dedeb8",
                            "rrep": "0x22f",
                            "totalDelegation": "0xc0b93aca28aac6ffb961a6",
                            "value": "0x3f259eb7fcd16c91",
                        },
                        "result": {
                            "coveredByFee": "0x3612df8756e000",
                            "coveredByOverIssuedICX": "0x0",
                            "issue": "0x3eef8bd8757a8c91",
                        },
                    },
                    "txHash": "0x368bc1a545e5e2d4b600439f996bdc0ec949bd3755bf3f7b1c57a0a57b4af526",
                },
                {
                    "version": "0x3",
                    "from": "hx894644f1b9b7fa52866b1465ff06c44c3bc79c68",
                    "to": "cx1b97c1abfd001d5cd0b5a3f93f22cccfea77e34e",
                    "timestamp": "0x5a28a82997578",
                    "nid": "0x1",
                    "stepLimit": "0x2625a00",
                    "dataType": "call",
                    "value": "0x1bc16d674ec80000",
                    "data": {
                        "method": "bet_on_numbers",
                        "params": {
                            "numbers": "1,4,5,6,7,12,14,15,16,18,17,2,13,8,10,20,19,11",
                            "user_seed": "",
                        },
                    },
                    "signature": "2nx+dUL8MPBroB96I22UsK/+wsU4Nfiyn+k4RhH6E7N4FtvyQgeC4LYdxw1oI4pIX3n6OaLxLFJcH2gOZu/s8wA=",
                    "txHash": "0x926631ff8639daf7c6096081f2db13d9b1dbf5f46ffce209082c9fbb1e493a68",
                },
            ],
        }

        block = Block.from_dict(block_dict)
        assert block.version == version
        assert block_height == block_height
        assert block.block_hash == block_hash
        assert block.prev_block_hash == prev_block_hash
        assert block.timestamp == timestamp
        assert block.peer_id == peer_id
        assert block.next_leader == next_leader
        assert block.signature == base64.standard_b64decode(signature)
        assert block.merkle_tree_root_hash == merkle_tree_root_hash
