import pytest

from src.lib.autoreplyer import AutoReplyer, StatusCode


replyer = AutoReplyer("config.yml")

@pytest.mark.asyncio
async def test_read_config():
    assert replyer._read_config("config.yml")["wait"] == 5


@pytest.mark.asyncio
async def test_sign_in():
    status = await replyer._sign_in()
    assert status == StatusCode.NowConnected.value


@pytest.mark.asyncio
async def test_send_message_by_id():
    await replyer._sign_in()
    status = await replyer._send_message_by_id("me", message="TEST")
    assert status == StatusCode.Success.value