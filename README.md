# sentence-splitter

Split Chinese text and English text into sentences.

## Installation

```shell
pip install git+https://github.com/zejunwang1/sentence-splitter
```

## Usage

***split_text_into_sentences***: Split Chinese text into sentences.

```python
def split_text_into_sentences(
    text: str,
    fast: bool=True,
    merge_and_split: bool=False,
    return_loc: bool = False,
    min_length: int = 16,
    max_length: int = 256
)
```

- `text`: Text to be split into individual sentences.

- `fast`: Whether to enable fast mode.

- `merge_and_split`: Whether to merge short sentences and split long sentences.

- `return_loc`: Whether to return the character position of the sentence in the original text string.

- `min_length`: Minimum sentence length within a paragraph. When the length of a sentence is less than min_length, the short sentences in the paragraph are merged. Sentences in different paragraphs are not merged.

- `max_length`: Maximum sentence length within a paragraph. When the length of a sentence is greater than max_length, the long sentence is further segmented based on punctuation marks.

```python
from sentence_splitter import split_text_into_sentences
text = "春节假期结束，许多人踏上了归途，奔向自己的工作岗位，告别时刻，总是满满的不舍和牵挂，即将返程，后备箱里必然塞的满满的，有各种家乡的特产，有妈妈亲手制作的各种吃食，也就又开启了“后备箱大赛”，前两天我看到一段视频，在浙江嘉兴，一位女子返程时，后备箱被塞的满满的，还有四只妈妈养的鸭子，由于车内空间有限，放不下，只好将鸭子挂在车尾，以免过多占用后备箱空间。\n\n返程时，每个人的后备箱里都塞满了家乡的味道和父母的牵挂，父母把最好的东西给儿女带上，这是家乡的味道，更是一种情感的寄托，是一份沉垫垫的来自父母的爱。使我们在离家的路上能感受到父母的爱和牵挂，挂在车尾的鸭子，显示出浓浓的母爱和期盼，写满了满满的爱和牵挂。我们一定要铭记这份爱意，把家人时刻放在心里。今年返程时，你的后备箱里都装了些啥呢？"
sents, locs = split_text_into_sentences(
    text, merge_and_split=True, return_loc=True, min_length=16, max_length=256
)
for sent, loc in zip(sents, locs):
    assert text[loc] == sent[0]
    print("{}\t{}".format(loc, sent))
```

```context
0	春节假期结束，许多人踏上了归途，奔向自己的工作岗位，告别时刻，总是满满的不舍和牵挂，即将返程，后备箱里必然塞的满满的，有各种家乡的特产，有妈妈亲手制作的各种吃食，也就又开启了“后备箱大赛”，前两天我看到一段视频，在浙江嘉兴，一位女子返程时，后备箱被塞的满满的，还有四只妈妈养的鸭子，由于车内空间有限，放不下，只好将鸭子挂在车尾，以免过多占用后备箱空间。
178	返程时，每个人的后备箱里都塞满了家乡的味道和父母的牵挂，父母把最好的东西给儿女带上，这是家乡的味道，更是一种情感的寄托，是一份沉垫垫的来自父母的爱。
252	使我们在离家的路上能感受到父母的爱和牵挂，挂在车尾的鸭子，显示出浓浓的母爱和期盼，写满了满满的爱和牵挂。
304	我们一定要铭记这份爱意，把家人时刻放在心里。
326	今年返程时，你的后备箱里都装了些啥呢？
```

***split_en_text_into_sentences***: Split English text into sentences.

```python
def split_en_text_into_sentences(
    text: str,
    split_long: bool=False,
    return_loc: bool = False,
    max_length: int = 1024
)
```

- `text`: Text to be split into individual sentences.

- `split_long`: Whether to split long sentences.

- `return_loc`: Whether to return the character position of the sentence in the original text string.

- `max_length`: Maximum sentence length within a paragraph. When the length of a sentence is greater than max_length, the long sentence is further segmented based on punctuation marks.

```python
from sentence_splitter import split_en_text_into_sentences
text = "What budgeting strategies should I use to save money each month? There are several budgeting strategies that can help you save money each month. Here are a few:\n\n1. Create a budget: Start by tracking your expenses and creating a budget that includes all of your monthly bills and expenses, such as rent/mortgage, utilities, groceries, transportation, entertainment, and savings. This will help you see where your money is going and where you can cut back.\n\n2. Use cash: Try using cash instead of credit cards or debit cards for your daily expenses. This will help you stay within your budget and prevent overspending.\n\n3. Set financial goals: Set specific financial goals, such as paying off debt, saving for a down payment on a house or car, or building an emergency fund. Having a goal in mind can help you stay motivated to save money.\n\n4. Cut back on unnecessary expenses: Look for areas where you can cut back on expenses, such as eating out less, canceling subscriptions you don't use, or finding cheaper alternatives for your daily expenses.\n\n5. Automate savings: Set up automatic transfers from your checking account to your savings account each month. This will help you save money without even thinking about it.\n\nRemember, saving money takes time and effort, but with a little discipline and planning, you can achieve your financial goals."
sents, locs = split_en_text_into_sentences(
    text, split_long=False, return_loc=True
)
for sent, loc in zip(sents, locs):
    assert text[loc] == sent[0]
    print("{}\t{}".format(loc, sent))
```

```context
0	What budgeting strategies should I use to save money each month?
65	There are several budgeting strategies that can help you save money each month.
145	Here are a few:
162	1. Create a budget: Start by tracking your expenses and creating a budget that includes all of your monthly bills and expenses, such as rent/mortgage, utilities, groceries, transportation, entertainment, and savings.
379	This will help you see where your money is going and where you can cut back.
457	2. Use cash: Try using cash instead of credit cards or debit cards for your daily expenses.
549	This will help you stay within your budget and prevent overspending.
619	3. Set financial goals: Set specific financial goals, such as paying off debt, saving for a down payment on a house or car, or building an emergency fund.
774	Having a goal in mind can help you stay motivated to save money.
840	4. Cut back on unnecessary expenses: Look for areas where you can cut back on expenses, such as eating out less, canceling subscriptions you don't use, or finding cheaper alternatives for your daily expenses.
1050	5. Automate savings: Set up automatic transfers from your checking account to your savings account each month.
1161	This will help you save money without even thinking about it.
1224	Remember, saving money takes time and effort, but with a little discipline and planning, you can achieve your financial goals.
```

## Reference

English sentence segmentation implementation is based on scripts developed by Philipp Koehn and Josh Schroeder.

https://github.com/mediacloud/sentence-splitter


