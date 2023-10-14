#!/usr/bin/env python3
import itertools
import typing
import unicodedata
from collections import defaultdict
from urllib.parse import urlparse
from warnings import warn

warn("We have moved from M$ GitHub to https://codeberg.org/KOLANICH-libs/emojiNorm.py , read why on https://codeberg.org/KOLANICH/Fuck-GuanTEEnomo .")

import icu
import more_itertools

__all__ = ("sequenceStrIntoEmoji", "sequenceIntoEmoji", "isSingleGrapheme", "graphemeCount", "normalizeEmoji")


countryBase = 0x1F1E6
countryEnd = countryBase + 26
countryCharRange = range(countryBase, countryEnd)
zwjCode = 0x200D
zwj = chr(zwjCode)
emojiPresSelCode = 0xFE0F  # forces emoji repr
emojiPresSel = chr(emojiPresSelCode)
keycapEncloserCode = 0x20E3
keycapEncloser = chr(keycapEncloserCode)
skinToneRange = range(0x1F3FB, 0x1F400)
hairStyleRange = range(0x1F9B0, 0x1F9B4)
familyCode = 0x1F46A
familyComponentsRange = range(0x1F466, familyCode)
genderfulMinorRange = range(0x1F466, 0x1F468)
genderfulAdultRange = range(0x1F468, familyCode)
genderlessBabyCode = 0x1F476
genderlessAdultCode = 0x1F9D1
genderlessMinorCode = 0x1F9D2
genderlessElderlyCode = 0x1F9D3
genderDeityIndicatorsSet = set("♀♂")


def _normalizeUnicode(s: str) -> str:
	return unicodedata.normalize("NFC", s)


def uciEnumIntoPythonEnum(cls):
	d = {k: getattr(cls, k) for k in dir(cls) if k[0] != "_"}
	return IntEnum(cls.__name__, d)


shit = {icu.UCharCategory.LOWERCASE_LETTER, icu.UCharCategory.UPPERCASE_LETTER, icu.UCharCategory.DECIMAL_DIGIT_NUMBER}


def _hbp(c: typing.Union[str, int], p: icu.UProperty) -> bool:
	"""Checks if a char has binary property. A simple wrapper to remind me how to deal with it"""
	if len(c):
		c = c[0]

	if isinstance(c, str):
		c = ord(c)
	return icu.Char.hasBinaryProperty(c, p)


def isHairStyle(s: str) -> bool:
	return ord(s) in hairStyleRange


def isSkinTone(s: str) -> bool:
	return ord(s) in skinToneRange


def isGenderDeity(s: str) -> bool:
	return s in genderDeityIndicatorsSet


def isGenderPerson(s: str) -> bool:
	return ord(s) in genderfulAdultRange


_diversityModalities = {
	"hair": isHairStyle,
	"skin": isSkinTone,
	"genderDeity": isGenderDeity,
}
_diversityModalitiesPerson = {
	"genderPerson": isGenderPerson,
}

ExtractedDiversityModalityT = typing.Iterable[str]
ExtractedDiversity = typing.Dict[str, ExtractedDiversityModalityT]


def _replaceDiversityModality(c: str, extracted: ExtractedDiversityModalityT, replacementsIter, modalityChecker) -> str:
	if modalityChecker(c):
		extracted.append(c)
		try:
			return next(replacementsIter)
		except StopIteration:
			return c
	return c


def _replaceDiversityIter(_diversityModalities, s: str, extracted: ExtractedDiversity, **kwargs: ExtractedDiversity) -> typing.Iterable[str]:
	modalities = [(k, (iter(v) if v is not None else iter(())), _diversityModalities[k]) for k, v in kwargs.items()]

	for i, c in enumerate(s):
		for modalityName, replacementsIter, modalityChecker in modalities:
			c = _replaceDiversityModality(c, extracted[modalityName], replacementsIter, modalityChecker)
			if c is None:
				break

		if c is None:
			continue

		yield c


def _replaceDiversity(_diversityModalities, s: str, **kwargs) -> typing.Tuple[str, ExtractedDiversity]:
	extracted = defaultdict(list)

	return normalizeEmoji("".join(_replaceDiversityIter(_diversityModalities, s, extracted, **kwargs))), {k: tuple(v) for k, v in extracted.items() if v}


def replaceDiversity(s: str, hair: typing.Iterable[str] = (), skin: typing.Iterable[str] = (), genderDeity: typing.Iterable[str] = ()) -> typing.Tuple[str, ExtractedDiversity]:
	"""Replaces diversity modalities within a sequence. Note: not all modalities are reforged (man-woman modality using man-woman chars is untouched), for example there is no sequencies of families made of genderless characters, instead distinct emoji are used, it is overhead to check for this special case in this function.
	P.S: *ists are the ones who overestimate the significance of such factors."""

	return _replaceDiversity(_diversityModalities, s, hair=hair, skin=skin, genderDeity=genderDeity)


def stripDiversity(s: str, hair: bool = True, skin: bool = True, genderDeity: bool = True) -> typing.Tuple[str, ExtractedDiversity]:
	alwaysNone = itertools.repeat(None)
	return replaceDiversity(s, alwaysNone if hair else (), alwaysNone if skin else (), alwaysNone if genderDeity else ())


def replaceDiversityPerson(s: str, genderPerson=()) -> typing.Tuple[str, ExtractedDiversity]:
	"""Replaces diversity modalities within a sequence."""

	return _replaceDiversity(_diversityModalitiesPerson, s, genderPerson=genderPerson)


def stripDiversityPerson(s: str) -> typing.Tuple[str, ExtractedDiversity]:
	return replaceDiversityPerson(s, itertools.repeat("🧑"))


def splitGraphemes(s: str) -> typing.Iterator[str]:
	"""Splits a string into distinct graphemes"""

	us = icu.UnicodeString(s)
	it = icu.BreakIterator.createCharacterInstance(icu.Locale.getUS())
	it.setText(us)

	for slc in more_itertools.windowed(itertools.chain([None], it), 2):
		yield str(us[slice(*slc)])


def _addPresSelForGrapheme(el: str) -> typing.Iterable[str]:
	yield el
	if not _hbp(el, icu.UProperty.EMOJI_PRESENTATION) and not _hbp(el, icu.UProperty.DEFAULT_IGNORABLE_CODE_POINT):
		yield emojiPresSel


def _addPresSel(s: str) -> typing.Iterable[str]:
	for el in splitGraphemes(s):
		# Because Presentation selector must be before U+20E3 (Combining Enclosing Keycap)
		if el[-1] == keycapEncloser:
			yield from _addPresSelForGrapheme(el[:-1])
			yield el[-1]
		else:
			yield from _addPresSelForGrapheme(el)


def addPresSel(s: str) -> str:
	return "".join(_addPresSel(s))


def mergeZWJWhereNeeded(s: str) -> str:
	"""Adds missing zero-width joiners"""

	return zwj.join(splitGraphemes(s))


def _removeBrokenTrailingZWJ(s: str):
	"""Removes zero-width joiners in the end of graphemes that take no effect because of the next char being incomposable to the one preceeding the joiner."""

	for el in splitGraphemes(s):
		if el[-1] == zwj:
			el = el[:-1]
		yield el


def removeBrokenTrailingZWJ(s: str) -> str:
	return "".join(_removeBrokenTrailingZWJ(s))


removeBrokenTrailingZWJ.__doc__ = _removeBrokenTrailingZWJ.__doc__


def normalizeEmoji(s: str) -> str:
	"""Normalizes an emoji string"""

	s = _normalizeUnicode(s)
	s = s.replace(zwj, "").replace(emojiPresSel, "")
	s = mergeZWJWhereNeeded(s)
	s = removeBrokenTrailingZWJ(s)
	s = addPresSel(s)
	s = _normalizeUnicode(s)
	return s


def graphemeCount(s: str) -> int:
	"""Gets count of graphemes in an emoji string"""
	return len(tuple(splitGraphemes(s)))


def isSingleGrapheme(s: str) -> bool:
	"""If a string is made of a single grapheme, returns True"""
	return graphemeCount(s) == 1


def sequenceIntoEmoji(seq: typing.Iterable[str]) -> str:
	"""Converts sequences of integers used in Unicode specs into an emoji string"""

	v = "".join(chr(el) for el in seq)
	v = normalizeEmoji(v)
	assert isSingleGrapheme(v)
	return v


def sequenceStrIntoEmoji(seqStr: str) -> str:
	"""Parses sequences of integers used in Unicode specs and converts them into an emoji string"""

	v = sequenceIntoEmoji(int(el, 16) for el in seqStr.split("-"))
	return v
