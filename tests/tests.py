#!/usr/bin/env python3
import sys
from pathlib import Path
import unittest
import itertools, re

sys.path.insert(0, str(Path(__file__).parent.parent))

from collections import OrderedDict

dict = OrderedDict

import emojiNorm
from emojiNorm import normalizeEmoji, graphemeCount


class Tests(unittest.TestCase):
	TEST_MATRIX = {
		'šØš¦': 'šØš¦',
		'šØ\u200dš¦': 'šØš¦',
		'\u200dšØš¦': 'šØš¦',
		'šØ\ufe0fš¦': 'šØš¦',
		'\u200dš“\u200dā': 'š“\u200dā',
		'š“\u200dā\u200d': 'š“\u200dā',
		'š“\u200dā\u200d\u200d': 'š“\u200dā',
		'š“\u200d\u200dā\u200d': 'š“\u200dā',
		'\ufe0fš“\ufe0fā': 'š“\u200dā',
		'š“\ufe0fā\ufe0f': 'š“\u200dā',
		'š“\ufe0fā\ufe0f\ufe0f': 'š“\u200dā',
		'š“\ufe0f\ufe0fā\ufe0f': 'š“\u200dā',
		'š“ā': 'š“\u200dā',
		'ā': 'ā\ufe0f',
		"3\ufe0fā£": "3\ufe0fā£",
		"š©šæ\u200dā¤\ufe0f\ufe0f\u200dšØš»": "š©šæ\u200dā¤\ufe0f\ufe0f\u200dšØš»",
		"š©šæ\u200dā¤\ufe0f\\u200dšØš»": "š©šæ\u200dā¤\ufe0f\ufe0f\u200dšØš»",
		"š©šæ\u200dā¤\\u200dšØš»": "š©šæ\u200dā¤\ufe0f\ufe0f\u200dšØš»",
		"š©šæ\u200dā¤šØš»": "š©šæ\u200dā¤\ufe0f\ufe0f\u200dšØš»",
		"š©šæā¤šØš»": "š©šæ\u200dā¤\ufe0f\ufe0f\u200dšØš»",
	}

	def testNormalize(self):
		for i, (challenge, etalon) in enumerate(self.__class__.TEST_MATRIX.items()):
			with self.subTest(i=i, challenge=repr(challenge), etalon=repr(etalon)):
				response = normalizeEmoji(challenge)
				with self.subTest("normalization"):
					self.assertEqual(repr(response), repr(etalon))
					self.assertEqual(graphemeCount(response), 1)

if __name__ == "__main__":
	unittest.main()
