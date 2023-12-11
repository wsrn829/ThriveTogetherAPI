from fastapi import APIRouter, Depends, Response
from typing import List

from ..models import PeerConnection, Peer, PeerConnections

from ..queries.peers import PeerConnectionQueries, PeerQueries
from authenticator import authenticator

router = APIRouter()


@router.post(
    "/api/connections/create",
    tags=["Peers"],
    response_model=PeerConnection,
)
def create_connection(
    peer_connection: PeerConnection,
    response: Response,
    queries: PeerConnectionQueries = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
):
    record = queries.create_connection(peer_connection)
    if record is None:
        response.status_code = 404
        return []

    peer_connection = PeerConnection(
        sender=record["sender"],
        recipient=record["recipient"],
        status=record["status"],
        has_messaged=record["has_messaged"],
        sender_name=record["sender_name"],
        recipient_name=record["recipient_name"],
    )

    return peer_connection


@router.get("/api/peers/{user_id}", tags=["Peers"], response_model=List[Peer])
def get_peers(
    user_id: int,
    response: Response,
    queries: PeerQueries = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
):
    records = queries.get_peers(user_id)
    if records is None:
        response.status_code = 404
        return []

    peers = []
    for record in records:
        peer = Peer(
            user_id=record["user_id"],
            peer_id=record["peer_id"],
            peer_name=record["peer_name"],
            profile_link=record["profile_link"],
            tags_id=record["tags_id"],
            profile_image=record["profile_image"],
            status=record["status"],
        )
        peers.append(peer)
    return peers


# This function is to show the other user request to be a peer for the login\
# user.
# The login user could check how many people want to be a peer for\
# he/she
# peer_connection table status would have 3 type: pending, approve, reject,\
# all type will show in peer pending function
@router.get(
    "/api/peer_connections/{user_id}",
    tags=["Peers"],
    response_model=PeerConnections,
)
async def get_peerConnection(
    user_id: int,
    response: Response,
    queries: PeerConnectionQueries = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
):
    result = {}
    records = queries.get_peer_connection(user_id)
    if records is None:
        response.status_code = 404
        return []
    result["peerConnections"] = records
    return result


# this method is for operate peer request. when the user approve or reject \
# the peer request update
# This method will update peer_connection table status column, it will change \
# to accept or reject
@router.post(
    "/api/peerRequest/operate/{user_id}/{sendRequest_id}/{status}",
    tags=["Peers"],
    response_model=PeerConnection,
)
async def update_peerConnection(
    user_id: int,
    sendRequest_id: int,
    status: str,
    response: Response,
    queries: PeerQueries = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
):
    records = queries.update_peer_connections(status, user_id, sendRequest_id)
    return records


# If the user approve the request, this method will also insert the data \
# into peer table
# Peer table is the such like friends list, it will show the status \
# equal 0 peer.
# peer table status 0: activate 1 and other meaning delete or deactivate
@router.post("/api/peerAdd", tags=["Peers"], response_model=Peer)
async def insert_peer(
    info: Peer,
    response: Response,
    queries: PeerQueries = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
):
    records = queries.insert_peer(info)
    return records
