"""
python-wechaty-plugin-contrib - https://github.com/wechaty/python-wechaty-plugin-contrib

Authors:    Jingjing WU (吴京京) <https://github.com/wj-Mcat>

2020-now @ Copyright wj-Mcat

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from dataclasses import (
    dataclass,
    field
)
from enum import Enum
from typing import Optional, List

from wechaty import (
    WechatyPluginOptions
)


class GithubContentType(Enum):
    JSON = 0,
    WWM_FORM_URLENCODED = 1


@dataclass
class GithubHookItem:
    """plugin can hook many gitlab projects, so the GitlabHookItem can specific
    the project
    """
    project_id: str

    room_topic: Optional[str] = None
    room_id: Optional[str] = None

    contact_name: Optional[str] = None
    contact_id: Optional[str] = None

    content_type: Optional[GithubContentType] = GithubContentType.JSON
    secret_token: Optional[str] = None


@dataclass
class GithubWebhookOptions(WechatyPluginOptions):
    listen_port: Optional[int] = 5101
    hook_items: List[GithubHookItem] = field(default_factory=list)
