import os
import pytest
import respx

from pyfcm import FCMNotification, errors
from pyfcm.baseapi import BaseAPI, FCMResult


@pytest.fixture(scope="module")
def push_service():
    api_key = os.getenv("FCM_TEST_API_KEY", None)
    assert (
        api_key
    ), "Please set the environment variables for testing according to CONTRIBUTING.rst"

    return FCMNotification(api_key=api_key)


@pytest.mark.asyncio
async def test_push_service_without_credentials():
    try:
        FCMNotification()
        assert False, "Should raise AuthenticationError without credentials"
    except errors.AuthenticationError:
        pass


@pytest.mark.asyncio
async def test_notify_single_device(push_service: FCMNotification, respx_mock):
    respx_mock.post(BaseAPI.FCM_END_POINT) % dict(json={"success": 1})  # type: ignore
    response = await push_service.notify(
        registration_id="Test", message_body="Test", message_title="Test"
    )

    assert isinstance(response, FCMResult)
    assert response.success == 1


@pytest.mark.asyncio
async def test_single_device_data_message(push_service: FCMNotification, respx_mock):
    respx_mock.post(BaseAPI.FCM_END_POINT) % dict(json={"success": 1})  # type: ignore
    try:
        await push_service.notify(data_message={"test": "Test"})
        assert False, "Should raise InvalidDataError without registration id"
    except errors.InvalidDataError:
        pass

    response = await push_service.notify(
        registration_id="Test", data_message={"test": "Test"}
    )

    assert isinstance(response, FCMResult)
    assert response.success == 1


@pytest.mark.asyncio
async def test_notify_multiple_devices(push_service: FCMNotification, respx_mock):
    respx_mock.post(BaseAPI.FCM_END_POINT) % dict(json={"success": 1, "failure": 1})  # type: ignore
    response = await push_service.notify(
        registration_ids=["Test", "Test2"],
        message_body="Test",
        message_title="Test",
    )
    assert isinstance(response, FCMResult)
    assert response.failure == 1
    assert response.success == 1


@pytest.mark.asyncio
async def test_multiple_devices_data_message(push_service: FCMNotification, respx_mock):
    respx_mock.post(BaseAPI.FCM_END_POINT) % dict(json={"success": 1, "failure": 1})  # type: ignore
    try:
        await push_service.notify(data_message={"test": "Test"})
        assert False, "Should raise InvalidDataError without registration ids"
    except errors.InvalidDataError:
        pass

    response = await push_service.notify(
        registration_ids=["Test", "Test2"], data_message={"test": "Test"}
    )
    assert isinstance(response, FCMResult)
    assert response.failure == 1
    assert response.success == 1


@pytest.mark.asyncio
async def test_notify_topic_subscribers(push_service: FCMNotification, respx_mock):
    respx_mock.post(BaseAPI.FCM_END_POINT) % dict(json={"success": 1})  # type: ignore
    response = await push_service.notify_topic_subscribers(
        topic_name="test", message_body="Test", message_title="Test", dry_run=True
    )

    assert response.success == 1


@pytest.mark.asyncio
async def test_notify_with_args(push_service: FCMNotification, respx_mock):
    respx_mock.post(BaseAPI.FCM_END_POINT) % dict(json={"hi": "ok"})
    await push_service.notify(
        registration_id="Test",
        message_body="Test",
        message_title="Test",
        message_icon="Test",
        sound="Test",
        collapse_key="Test",
        delay_while_idle=False,
        time_to_live=100,
        restricted_package_name="Test",
        low_priority=False,
        data_message={"test": "test"},
        click_action="Test",
        badge="Test",
        color="Test",
        tag="Test",
        body_loc_key="Test",
        body_loc_args=["Test"],
        title_loc_key="Test",
        title_loc_args=["Test"],
        content_available=None,
        android_channel_id="Test",
        timeout=5,
        extra_notification_kwargs={},
        extra_kwargs={},
    )
