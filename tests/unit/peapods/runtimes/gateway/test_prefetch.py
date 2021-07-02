import threading
import time

import pytest

from jina.helper import ArgNamespace, random_identity
from jina.parsers import set_gateway_parser
from jina.peapods.runtimes.gateway.prefetch import PrefetchCaller
from jina.proto import jina_pb2


class ZmqletMock:
    def __init__(self, wait_for_receive: threading.Event):
        self.wait_for_receive = wait_for_receive
        self.receive_value = None

    async def send_message(self, message):
        return message

    async def recv_message(self, **kwargs):
        self.wait_for_receive.wait()
        self.wait_for_receive.clear()
        recv = self.receive_value
        self.receive_value = None
        return recv


def _generate_request(client_id):
    req = jina_pb2.RequestProto()
    req.request_id = random_identity()
    d = req.data.docs.add()
    d.tags['client_id'] = client_id
    return req


@pytest.mark.asyncio
async def test_concurrent_requests():
    wait_for_receive = threading.Event()
    mock = ZmqletMock(wait_for_receive)
    subject = PrefetchCaller(
        ArgNamespace.kwargs2namespace({}, set_gateway_parser()), mock
    )

    req1 = _generate_request(1)
    req2 = _generate_request(2)

    async def send_message(req):
        responses = []
        async for item in subject.Call(iter([req])):
            responses.append(item)
        return responses

    async def trigger_receive(req):
        time.sleep(0.1)
        mock.receive_value = req
        wait_for_receive.set()

    response_client_1 = send_message(req1)
    response_client_2 = send_message(req2)

    await trigger_receive(req2)
    response_client_1 = await response_client_1

    await trigger_receive(req1)
    response_client_2 = await response_client_2

    assert response_client_1[0] == req1
    assert response_client_2[0] == req2
