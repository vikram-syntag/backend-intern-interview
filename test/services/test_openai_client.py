# Testing the OpenAI client

# Path: test/services/test_openai_client.py

from app.services.openai_client import OpenAIClient, OpenAIModel
import pytest
import openai
from unittest.mock import Mock

@pytest.fixture
def openai_client():
    return OpenAIClient(api_key="fake_key")

@pytest.fixture
def openai_client_mock():
    openai.api_key = "fake_key"
    openai_client = OpenAIClient(api_key="fake_key")
    openai_client.single_response = Mock()
    openai_client.single_response_stream = Mock()
    openai_client.server_and_user_message_response = Mock()
    openai_client.conversation_response = Mock()
    openai_client.server_and_user_message_response_stream = Mock()
    openai_client.conversation_response_stream = Mock()
    return openai_client

def test_openai_client_init(openai_client):
    assert openai_client.api_key == "fake_key"
    assert openai_client.model == OpenAIModel.GPT_3_5
    assert openai_client.temperature == 0.7
    assert openai_client.max_tokens == 250
    
def test_openai_client_single_response(openai_client_mock):
    openai_client_mock.single_response("test")
    openai_client_mock.single_response.assert_called_once_with("test")
    
def test_openai_client_single_response_stream(openai_client_mock):
    openai_client_mock.single_response_stream("test")
    openai_client_mock.single_response_stream.assert_called_once_with("test")
    
def test_openai_client_server_and_user_message_response(openai_client_mock):
    openai_client_mock.server_and_user_message_response("server", "user")
    openai_client_mock.server_and_user_message_response.assert_called_once_with("server", "user")
    
def test_openai_client_conversation_response(openai_client_mock):
    messages = [{"role": "system", "content": "server"}, {"role": "user", "content": "user"}]
    openai_client_mock.conversation_response(messages)
    openai_client_mock.conversation_response.assert_called_once_with(messages)
    
def test_openai_client_server_and_user_message_response_stream(openai_client_mock):
    openai_client_mock.server_and_user_message_response_stream("server", "user")
    openai_client_mock.server_and_user_message_response_stream.assert_called_once_with("server", "user")    
    
def test_openai_client_conversation_response_stream(openai_client_mock):
    messages = [{"role": "system", "content": "server"}, {"role": "user", "content": "user"}]
    openai_client_mock.conversation_response_stream(messages)
    openai_client_mock.conversation_response_stream.assert_called_once_with(messages)