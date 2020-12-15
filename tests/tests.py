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
		'🇨🇦': '🇨🇦',
		'🇨\u200d🇦': '🇨🇦',
		'\u200d🇨🇦': '🇨🇦',
		'🇨\ufe0f🇦': '🇨🇦',
		'\u200d🚴\u200d♂': '🚴\u200d♂',
		'🚴\u200d♂\u200d': '🚴\u200d♂',
		'🚴\u200d♂\u200d\u200d': '🚴\u200d♂',
		'🚴\u200d\u200d♂\u200d': '🚴\u200d♂',
		'\ufe0f🚴\ufe0f♂': '🚴\u200d♂',
		'🚴\ufe0f♂\ufe0f': '🚴\u200d♂',
		'🚴\ufe0f♂\ufe0f\ufe0f': '🚴\u200d♂',
		'🚴\ufe0f\ufe0f♂\ufe0f': '🚴\u200d♂',
		'🚴♂': '🚴\u200d♂',
		'☑': '☑\ufe0f',
		"3\ufe0f⃣": "3\ufe0f⃣",
		"👩🏿\u200d❤\ufe0f\ufe0f\u200d👨🏻": "👩🏿\u200d❤\ufe0f\ufe0f\u200d👨🏻",
		"👩🏿\u200d❤\ufe0f\\u200d👨🏻": "👩🏿\u200d❤\ufe0f\ufe0f\u200d👨🏻",
		"👩🏿\u200d❤\\u200d👨🏻": "👩🏿\u200d❤\ufe0f\ufe0f\u200d👨🏻",
		"👩🏿\u200d❤👨🏻": "👩🏿\u200d❤\ufe0f\ufe0f\u200d👨🏻",
		"👩🏿❤👨🏻": "👩🏿\u200d❤\ufe0f\ufe0f\u200d👨🏻",
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
