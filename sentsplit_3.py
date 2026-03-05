# coding=utf-8

import re

def split_sentence(
    text: str, 
    min_length: int = 16, 
    max_length: int = 256, 
    return_loc: bool = False
):
    # 当前字符位置
    cur = 0
    # 最大回溯长度
    maxMove = max_length - min_length
    # 段落划分
    regions = text.split('\n')

    locs, sents = [], []
    for region in regions:
        n = len(region)
        if not region.strip():
            cur += n
            cur += 1
            continue

        # 标点符号切分
        #region = re.sub('([。！？!?;；])([^”’])', r'\1\n\2', region)
        #region = re.sub('([。！？!?;；][”’])(.)', r'\1\n\2', region)
        region = re.sub('([。！？!?;；]+[”’]*)(.)', r'\1\n\2', region)
        region = region.split('\n')

        start, end = 0, len(region)
        if end == 1 and n > max_length and region[0][-1] != '。':
            # 汉字 + "."
            region = re.sub('([\u4e00-\u9fa5][.])(.)', r'\1\n\2', region[0])
            region = region.split('\n')
            end = len(region)
        
        # 短句合并 长句细分
        before = len(sents)
        while start < end:
            sent = region[start]
            if len(sent) >= min_length and len(sent) <= max_length:
                locs.append(cur)
                sents.append(sent)
                cur += len(sent)
                start += 1
                continue
            
            while len(sent) < min_length and start < end - 1:
                start += 1
                sent  += region[start]
            if len(sent) <= max_length:
                locs.append(cur)
                sents.append(sent)
                cur += len(sent)
                start += 1
                continue
            
            # 最大长度回溯切分
            while len(sent) > max_length:
                move = 1
                while move < maxMove:
                    if sent[max_length - move] in [',', '，', '\t']:
                        break
                    move += 1
                if move == maxMove:
                    move = 1
                    while move < maxMove:
                        if sent[max_length - move] in ['、', ' ']:
                            break
                        move += 1
                if move == maxMove:
                    locs.append(cur)
                    sents.append(sent[:max_length])
                    sent = sent[max_length:]
                    cur += max_length
                else:
                    split = max_length - move + 1
                    locs.append(cur)
                    sents.append(sent[: split])
                    sent = sent[split: ]
                    cur += split

            if len(sent) < min_length:
                sents[-1] += sent
            else:
                locs.append(cur)
                sents.append(sent)
            cur += len(sent)
            start += 1

        after = len(sents)
        if after - before > 1 and len(sents[-1]) < min_length:
            sents[-2] += sents[-1]
            locs.pop()
            sents.pop()
        cur += 1

    return (sents, locs) if return_loc else sents

