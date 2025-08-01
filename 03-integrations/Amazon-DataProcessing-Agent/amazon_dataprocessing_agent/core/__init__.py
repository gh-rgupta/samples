# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Core functionality for the DataProcessing Agent."""

from amazon_dataprocessing_agent.core.agent_manager import MCPAgentManager
from core.strands_bedrock_agent import StrandsBedrockAgent
from amazon_dataprocessing_agent.core.chat_history_manager import \
    ChatHistoryManager
from amazon_dataprocessing_agent.core.session_state import SessionState
from amazon_dataprocessing_agent.core.streaming_handler import StreamingHandler

__all__ = [
    "MCPAgentManager",
    "SessionState",
    "StrandsBedrockAgent",
    "StreamingHandler",
    "ChatHistoryManager",
]
