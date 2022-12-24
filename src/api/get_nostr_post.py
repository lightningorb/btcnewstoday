# from functools import lru_cache
# from nostr.event import Event, EventKind
# from nostr.filter import Filter, Filters
# from nostr.message_type import ClientMessageType
# from nostr.relay_manager import RelayManager
# from nostr.key import PrivateKey, PublicKey

# import ssl
# import json
# import time
# import os


# def get_post(sender_publickey: str, note_id: str):
#     pk = PublicKey(bytes.fromhex(sender_publickey))
#     relay_manager = RelayManager()
#     for r in [
#         "wss://nostr-pub.wellorder.net",
#         "wss://relay.damus.io",
#         "wss://nostr1.starbackr.me",
#         "wss://nostr.formigator.eu",
#         "wss://wizards.wormrobot.org",
#     ]:
#         relay_manager.add_relay(r)
#     relay_manager.open_connections(
#         {"cert_reqs": ssl.CERT_NONE}
#     )  # NOTE: This disables ssl certificate verification
#     time.sleep(3)  # allow the connections to open

#     filters = Filters(
#         [
#             Filter(
#                 ids=[note_id],
#                 authors=[pk.hex()],
#                 kinds=[EventKind.TEXT_NOTE],
#             )
#         ]
#     )
#     subscription_id = os.urandom(4).hex()
#     relay_manager.add_subscription(subscription_id, filters)

#     request = [ClientMessageType.REQUEST, subscription_id]
#     request.extend(filters.to_json_array())
#     message = json.dumps(request)

#     relay_manager.publish_message(message)

#     while True:
#         while relay_manager.message_pool.has_events():
#             event_msg = relay_manager.message_pool.get_event()
#             t = event_msg.event.content
#             relay_manager.close_connections()
#             return t
#         else:
#             time.sleep(0.1)
