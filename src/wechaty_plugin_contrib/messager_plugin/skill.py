"""
Python Plugin repo - https://github.com/wechaty/python-wechaty-plugin-contrib

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
from typing import List, Union
from enum import Enum
import jieba.posseg as pseg

TokenType = str


class Token:
    """token is the unit word group in sentence and store the metadata of
    the tokens

    the defination of token_type is :
    标签	含义	标签	含义	标签	含义	标签	含义
    n	普通名词	f	方位名词	s	处所名词	nw	作品名
    nz	其他专名	v	普通动词	vd	动副词	vn	名动词
    a	形容词	ad	副形词	an	名形词	d	副词
    m	数量词	q	量词	r	代词	p	介词
    c	连词	u	助词	xc	其他虚词	w	标点符号
    PER	人名	LOC	地名	ORG	机构名	TIME	时间
    """

    def __init__(self, words: str, type: str):
        self.words = words
        self.type = type


class Skill:
    """this is the base interface for messager plugin"""

    def get_template(self) -> Union[List[TokenType], List[List[TokenType]]]:
        """get all of the token type"""
        return ['n', 'f', 'an']

    def suit_this_skill(self, text: str, friend_names: List[str]) -> bool:
        """check if it's suit for template extract"""
        words = pseg.lcut
        import jieba
        jieba.set_dictionary

