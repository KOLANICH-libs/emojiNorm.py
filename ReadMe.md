emojiNorm.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
============
~~[wheel (GHA via `nightly.link`)](https://nightly.link/KOLANICH-libs/emojiNorm.py/workflows/CI/master/emojiNorm-0.CI-py3-none-any.whl)~~
~~[![GitHub Actions](https://github.com/KOLANICH-libs/emojiNorm.py/workflows/CI/badge.svg)](https://github.com/KOLANICH-libs/emojiNorm.py/actions/)~~
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH-libs/emojiNorm.py.svg)](https://libraries.io/github/KOLANICH-libs/emojiNorm.py)
[![Code style: antiflash](https://img.shields.io/badge/code%20style-antiflash-FFF.svg)](https://codeberg.org/KOLANICH-tools/antiflash.py)

**We have moved to https://codeberg.org/KOLANICH-libs/emojiNorm.py, grab new versions there.**

Under the disguise of "better security" Micro$oft-owned GitHub has [discriminated users of 1FA passwords](https://github.blog/2023-03-09-raising-the-bar-for-software-security-github-2fa-begins-march-13/) while having commercial interest in success and wide adoption of [FIDO 1FA specifications](https://fidoalliance.org/specifications/download/) and [Windows Hello implementation](https://support.microsoft.com/en-us/windows/passkeys-in-windows-301c8944-5ea2-452b-9886-97e4d2ef4422) which [it promotes as a replacement for passwords](https://github.blog/2023-07-12-introducing-passwordless-authentication-on-github-com/). It will result in dire consequencies and is competely inacceptable, [read why](https://codeberg.org/KOLANICH/Fuck-GuanTEEnomo).

If you don't want to participate in harming yourself, it is recommended to follow the lead and migrate somewhere away of GitHub and Micro$oft. Here is [the list of alternatives and rationales to do it](https://github.com/orgs/community/discussions/49869). If they delete the discussion, there are certain well-known places where you can get a copy of it. [Read why you should also leave GitHub](https://codeberg.org/KOLANICH/Fuck-GuanTEEnomo).

---

A library to normalize Unicode emoji sequencies. **Currently broken for some cases, needs more fixing and testing. Use with care.**

## Usage

### `normalizeEmoji`

Does emoji normalization
* remove redundant zero-width-joiners;
* add missing zero-width joiners;
* add emoji presentation selectors where they are needed.

```python
normalizeEmoji('☑') # ☑️
```

**Issues**:
* some compound emoji (i.e. `"👩🏿\u200d❤\ufe0f\ufe0f\u200d👨🏻"`) contain a sequence of 2 presentation selectors right after each other (`\ufe0f\ufe0f`). This function breaks those emoji since it first strips all emoji presentation selectors, and then generates them from scratch. It seems that for those emoji the only way is to remember that they are constructed this way. Currently I'm not sure how to handle them, so they are broken.

### `graphemeCount`

Counts graphemes. Emoji must contain of 1.

```python
o = '🚴️♂'
print(graphemeCount(o))  # 2
r = normalizeEmoji(o)
print(r, graphemeCount(r))  # 🚴‍♂️ 1
```

### `stripDiversity`

Strips skin tone, hair style modifiers and gender (not all, only deity-based (Venus/Mars)) zwj seqs.

```python
print(*stripDiversity("👩🏻‍❤︎️‍👨🏿"))  # 👩‍❤︎‍👨 {'skin': ('🏻', '🏿')}
print(*stripDiversity("👩🏻‍🦰"))  # 👩 {'hair': ('🦰',), 'skin': ('🏻',)}
print(*stripDiversity("🚵‍♂️"))  # 🚵 {'genderDeity': ('♂',)}
```

### `stripDiversityPerson`

Replaces `man`/`woman` code points with `person` ones.

```python
print(*stripDiversityPerson("👨‍🚒"))  # 🧑‍🚒 {'genderPerson': ('👨',)} (male firefighter to just firefighter)
```
