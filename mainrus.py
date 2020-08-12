import requests

from bs4 import BeautifulSoup

dollar_rub = 'https://www.google.com/search?sxsrf=ALeKk03bRcEWy3b3B4qTMDyH4dzMYeojVg%3A1594719903379&ei=n34NX-jhFsjKrgSLjbi4Ag&q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIKCAAQywEQRhCCAjIFCAAQywEyBQgAEMsBMgUIABDLATIECAAQQzIFCAAQywEyAggAMgUIABDLATIFCAAQywEyAggAOgQIIxAnOgoIABCxAxCDARBDOgkIIxAnEEYQggI6BwgAELEDEEM6CAgAELEDEIMBOgUIABCxA1DUGljyNGD2PGgAcAB4AYAB_wGIAfkNkgEGMTkuMC4xmAEAoAEBqgEHZ3dzLXdpeg&sclient=psy-ab&ved=0ahUKEwiore3KuszqAhVIpYsKHYsGDicQ4dUDCAw&uact=5'
euro_rub = 'https://www.google.com/search?sxsrf=ALeKk00zxeGzK4CO7SKSC05LMeqAfkRs9A%3A1594719912195&ei=qH4NX-vHC6KqrgTQ566gBQ&q=%D0%BA%D1%83%D1%80%D1%81+%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIKCAAQywEQRhCCAjIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLAToECAAQRzoGCAAQBxAeOgQIABANULejA1iPpwNg_qkDaABwAXgAgAFjiAHgApIBATSYAQCgAQGqAQdnd3Mtd2l6&sclient=psy-ab&ved=0ahUKEwjru4fPuszqAhUilYsKHdCzC1QQ4dUDCAw&uact=5'
pound_rub = 'https://www.google.com/search?sxsrf=ALeKk022TjUrZ7kvF7qV4imwXSck-M4Jyg%3A1594719967501&ei=334NX8qIHtDIrgSDs7igDw&q=%D0%BA%D1%83%D1%80%D1%81+%D1%84%D1%83%D0%BD%D1%82%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%BA%D1%83%D1%80%D1%81+%D1%84%D1%83%D0%BD%D1%82%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIFCAAQywEyBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB46BAgAEEc6BAgAEA1QnZMBWKaYAWDNmQFoAHABeACAAVSIAZQDkgEBNZgBAKABAaoBB2d3cy13aXo&sclient=psy-ab&ved=0ahUKEwiK9LbpuszqAhVQpIsKHYMZDvQQ4dUDCAw&uact=5'
bitcoin_rub = 'https://www.google.com/search?sxsrf=ALeKk03v35ojikhr8oZjcA3q0BHKtjLELw%3A1594719988128&ei=9H4NX5KtB9DIrgSDs7igDw&q=%D0%BA%D1%83%D1%80%D1%81+%D0%B1%D0%B8%D1%82%D0%BA%D0%BE%D0%B8%D0%BD%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B1%D0%B8%D1%82%D0%BA%D0%BE%D0%B8%D0%BD%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIKCAAQywEQRhCCAjIFCAAQywEyBggAEAcQHjIFCAAQywEyBggAEAcQHjIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBOgQIABBHOggIABAHEB4QEzoECAAQEzoECAAQDVDh5wFYoe8BYIrxAWgAcAF4AIABa4gB0QWSAQM3LjGYAQCgAQGqAQdnd3Mtd2l6&sclient=psy-ab&ved=0ahUKEwiS96HzuszqAhVQpIsKHYMZDvQQ4dUDCAw&uact=5'
grivna_rub = 'https://www.google.com/search?sxsrf=ALeKk03TKoCCC8rkGW_rCnoN9YEK2KLLDQ%3A1594720946349&ei=soINX4_jFObmrgSc65zgDw&q=%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIKCAAQywEQRhCCAjIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLAToECCMQJzoECAAQQzoICAAQsQMQgwE6BQgAELEDOgIIADoECAAQCjoHCAAQsQMQQzoJCCMQJxBGEIICUJa1AVjK0wFgmtUBaAFwAHgAgAFniAHuCZIBBDE0LjGYAQCgAQGqAQdnd3Mtd2l6&sclient=psy-ab&ved=0ahUKEwiPhJe8vszqAhVms4sKHZw1B_wQ4dUDCAw&uact=5'
frank_rub = 'https://www.google.com/search?sxsrf=ALeKk01cEN7N9RpxLlFQdtytQgwXVGY-Yw%3A1594720019847&ei=E38NX92YM-GMrgT6tYgw&q=%D0%BA%D1%83%D1%80%D1%81+%D1%84%D1%80%D0%B0%D0%BD%D0%BA%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%BA%D1%83%D1%80%D1%81+%D1%84%D1%80%D0%B0%D0%BD%D0%BA%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIFCAAQywEyBggAEAcQHjIGCAAQBxAeMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLAToECAAQRzoICAAQBxAeEBNQ-YQJWLmKCWCiiwloAHABeACAAV-IAfwDkgEBNpgBAKABAaoBB2d3cy13aXo&sclient=psy-ab&ved=0ahUKEwid7rGCu8zqAhVhhosKHfoaAgYQ4dUDCAw&uact=5'
canadadollar_rub = 'https://www.google.com/search?sxsrf=ALeKk00SZXc_JQ9s3Pj1-ElwNIFVasvGRw%3A1594720169637&ei=qX8NX5vEJseyrgTX0pH4AQ&q=%D0%BA%D1%83%D1%80%D1%81+%D0%BA%D0%B0%D0%BD%D0%B0%D0%B4%D1%81%D0%BA%D0%BE%D0%B3%D0%BE+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%BA%D0%B0%D0%BD%D0%B0%D0%B4%D1%81%D0%BA%D0%BE%D0%B3%D0%BE+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIGCAAQBxAeMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBOgQIABBHOggIABAHEB4QEzoKCAAQBxAKEB4QEzoICAAQBxAKEB46BAgAEA1Q9ZABWP2jAWCHpQFoAHABeAKAAaUEiAHsE5IBDDE0LjEuMS4wLjEuMZgBAKABAaoBB2d3cy13aXo&sclient=psy-ab&ved=0ahUKEwjbvOjJu8zqAhVHmYsKHVdpBB8Q4dUDCAw&uact=5'
ausdollar_rub = 'https://www.google.com/search?sxsrf=ALeKk02ntIQXM6wDTw1KL9hGm5uLmdYvhg%3A1594720191599&ei=v38NX5qVJPGnrgTTy6u4AQ&q=%D0%BA%D1%83%D1%80%D1%81+%D0%B0%D0%B2%D1%81%D1%82%D1%80%D0%B0%D0%BB%D0%B8%D0%B9%D1%81%D0%BA%D0%BE%D0%B3%D0%BE+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B0%D0%B2%D1%81%D1%82%D1%80%D0%B0%D0%BB%D0%B8%D0%B9%D1%81%D0%BA%D0%BE%D0%B3%D0%BE+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgQIABAeMgQIABAeMgYIABAIEB4yBggAEAgQHjIGCAAQCBAeOgQIABBHOgYIABAHEB46CAgAEAcQChAeOggIABAIEAcQHjoICAAQBxAeEBM6CggAEAcQChAeEBM6CggAEAgQBxAeEBM6BAgAEBM6DQgAEAcQHhATEEYQggJQp4EBWLaRAWD3kwFoAHABeACAAWuIAc8JkgEEMTMuMZgBAKABAaoBB2d3cy13aXo&sclient=psy-ab&ved=0ahUKEwja8KTUu8zqAhXxk4sKHdPlChcQ4dUDCAw&uact=5'
yen_rub = 'https://www.google.com/search?sxsrf=ALeKk02335-Qdwm3s3M4sboWKQNhRsRRWw%3A1594720211428&ei=038NX4LMGa-QrgTdlZ_4DQ&q=%D0%BA%D1%83%D1%80%D1%81+%D0%B9%D0%B5%D0%BD%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B9%D0%B5%D0%BD%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIFCAAQywEyBQgAEMsBMgQIABAeMgYIABAIEB4yBggAEAgQHjIICAAQCBAKEB4yBggAEAgQHjIGCAAQCBAeMgYIABAIEB46BAgAEEc6BggAEAcQHjoICAAQBxAKEB46BAgAEA06CggAEAgQDRAKEB46CAgAEAgQDRAeOggIABAHEB4QE1CZvwJYg9ICYMrTAmgBcAF4AIABbYgBqwWSAQM3LjGYAQCgAQGqAQdnd3Mtd2l6&sclient=psy-ab&ved=0ahUKEwjCgd_du8zqAhUviIsKHd3KB98Q4dUDCAw&uact=5'
israel_rub = 'https://www.google.com/search?sxsrf=ALeKk00CwfbLojivesXjk9f2_jyvyaGQVQ%3A1594722894306&ei=TooNX9unEr2GwPAPhNGOmAE&q=%D1%88%D0%B5%D0%BA%D0%B5%D0%BB%D1%8C+%D0%B2+%D1%80%D1%83%D0%B1%D0%BB%D1%8F%D1%85&oq=%D1%88%D0%B5%D0%BA%D0%B5%D0%BB%D1%8C+%D0%B2+%D1%80%D1%83%D0%B1%D0%BB%D1%8F%D1%85&gs_lcp=CgZwc3ktYWIQAzIKCAAQywEQRhCCAjIFCAAQywEyBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeOgQIIxAnOgIIAFC7IVjrKWDJL2gAcAB4AIABX4gBjwaSAQE5mAEAoAEBqgEHZ3dzLXdpeg&sclient=psy-ab&ved=0ahUKEwjbhoXdxczqAhU9AxAIHYSoAxMQ4dUDCAw&uact=5'
ether_rub = 'https://www.google.com/search?sxsrf=ALeKk00DKZceBbue1r8LXlcpYSafJ2qVrg%3A1594720293657&ei=JYANX57gJ-TErgTXsqNo&q=%D0%BA%D1%83%D1%80%D1%81+%D1%8D%D1%84%D0%B8%D1%80%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%BA%D1%83%D1%80%D1%81+%D1%8D%D1%84%D0%B8%D1%80%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIFCAAQywEyBQgAEMsBMgUIABDLATIECAAQHjIGCAAQBxAeMgQIABAeMgIIADoECCMQJzoICAAQBxAKEB46BAgAEA1Q-pACWIGWAmCplwJoAHAAeACAAV-IAfgDkgEBNpgBAKABAaoBB2d3cy13aXo&sclient=psy-ab&ved=0ahUKEwjehvqEvMzqAhVkoosKHVfZCA0Q4dUDCAw&uact=5'
litecoin_rub = 'https://www.google.com/search?sxsrf=ALeKk02kkPteXQZpbP8_RxykgEhDBUB-hA%3A1594720330356&ei=SoANX8anFZbergTRp6qIDw&q=%D0%BA%D1%83%D1%80%D1%81+%D0%BB%D0%B0%D0%B9%D1%82%D0%BA%D0%BE%D0%B8%D0%BD%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%BB%D0%B0%D0%B9%D1%82%D0%BA%D0%BE%D0%B8%D0%BD%D0%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=CgZwc3ktYWIQAzIFCAAQywEyBQgAEMsBMgQIABAeOgQIABBHOggIABAHEB4QEzoGCAAQBxAeOgQIABANOgoIABAIEAcQChAeOgYIABANEB46CAgAEA0QBRAeOggIABAIEA0QHjoECAAQE1DqpAFYwa4BYMqvAWgAcAF4AIABogGIAfQGkgEDNi4zmAEAoAEBqgEHZ3dzLXdpeg&sclient=psy-ab&ved=0ahUKEwjG9LmWvMzqAhUWr4sKHdGTCvEQ4dUDCAw&uact=5'

bitcoin_euro = 'https://www.google.com/search?sxsrf=ALeKk02uwkaBlheGAAMWT4mcuLegNvehxw%3A1594723250232&ei=sosNX97aDcWXmwWQpLOgAg&q=%D0%B1%D0%B8%D1%82%D0%BA%D0%BE%D0%B8%D0%BD+%D0%BA+%D0%B5%D0%B2%D1%80%D0%BE&oq=%D0%B1%D0%B8%D1%82%D0%BA%D0%BE%D0%B8%D0%BD+%D0%BA+%D0%B5%D0%B2%D1%80%D0%BE&gs_lcp=CgZwc3ktYWIQAzIKCAAQywEQRhCCAjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeOggIABCxAxCDAToCCAA6BAgjECc6BAgAEEM6BwgAELEDEEM6BQgAELEDOgkIIxAnEEYQggI6BQgAEMsBOggIABAWEAoQHlDU6Y4BWOuMjwFgvZKPAWgDcAB4AIABZYgB9wmSAQQxNC4xmAEAoAEBqgEHZ3dzLXdpeg&sclient=psy-ab&ved=0ahUKEwje--CGx8zqAhXFy6YKHRDSDCQQ4dUDCAw&uact=5'
ether_euro = 'https://www.google.com/search?sxsrf=ALeKk00RJnMStKrD3_h-SzdEedXY0xtcww%3A1594725596174&ei=3JQNX82UCqaEk74P94Og4Ak&q=%D1%8D%D1%84%D0%B8%D1%80+%D0%BA+%D0%B2%D0%B5%D0%B2%D1%80%D0%BE&oq=%D1%8D%D1%84%D0%B8%D1%80+%D0%BA+%D0%B2%D0%B5%D0%B2%D1%80%D0%BE&gs_lcp=CgZwc3ktYWIQAzIECAAQDToECCMQJzoFCAAQsQM6AggAOggIABCxAxCDAToJCCMQJxBGEIICOgQIABBDOgcIABCxAxBDOgUIABDLAToGCAAQFhAeOgcIIRAKEKABUKXIAVjE3AFgpd8BaABwAHgAgAF8iAHaCJIBAzguNJgBAKABAaoBB2d3cy13aXo&sclient=psy-ab&ved=0ahUKEwjN8rHlz8zqAhUmwsQBHfcBCJwQ4dUDCAw&uact=5'
litecoin_euro = 'https://www.google.com/search?sxsrf=ALeKk01XXVMDzwOvd-z6tlFVt9_hE5iW2Q%3A1594725625473&ei=-ZQNX6HAHLuJk74PyP2P8AU&q=%D0%BB%D0%B0%D0%B9%D1%82%D0%BA%D0%BE%D0%B8%D0%BD+%D0%BA+%D0%B5%D0%B2%D1%80%D0%BE&oq=%D0%BB%D0%B0%D0%B9%D1%82%D0%BA%D0%BE%D0%B8%D0%BD+%D0%BA+%D0%B5%D0%B2%D1%80%D0%BE&gs_lcp=CgZwc3ktYWIQAzIICCEQFhAdEB4yCAghEBYQHRAeMggIIRAWEB0QHjIICCEQFhAdEB4yCAghEBYQHRAeMggIIRAWEB0QHjIICCEQFhAdEB4yCAghEBYQHRAeMggIIRAWEB0QHjIICCEQFhAdEB46BAgjECc6AggAOggIABCxAxCDAToFCAAQsQM6CggAELEDEIMBEEM6CQgjECcQRhCCAjoECAAQQzoFCAAQywE6BggAEBYQHjoICAAQFhAKEB46BQghEKABOgcIIRAKEKABUI-yAVjgwAFgjcIBaABwAHgAgAGAAYgBwwqSAQQxMi4zmAEAoAEBqgEHZ3dzLXdpeg&sclient=psy-ab&ved=0ahUKEwjhoK7zz8zqAhW7xMQBHcj-A14Q4dUDCAw&uact=5'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
full_page_rus_dollar = requests.get(dollar_rub, headers=headers)
full_page_rus_euro = requests.get(euro_rub, headers=headers)
full_page_rus_pound = requests.get(pound_rub, headers=headers)
full_page_rus_bitcoin = requests.get(bitcoin_rub, headers=headers)
full_page_rus_grivna = requests.get(grivna_rub, headers=headers)
full_page_rus_frank = requests.get(frank_rub, headers=headers)
full_page_rus_canadadollar = requests.get(canadadollar_rub, headers=headers)
full_page_rus_ausdollar = requests.get(ausdollar_rub, headers=headers)
full_page_rus_yen = requests.get(yen_rub, headers=headers)
full_page_rus_israel = requests.get(israel_rub, headers=headers)
full_page_rus_ether = requests.get(ether_rub, headers=headers)
full_page_rus_litecoin = requests.get(litecoin_rub, headers=headers)

full_page_euro_bitcoin = requests.get(bitcoin_euro, headers=headers)
full_page_ether_euro = requests.get(ether_euro, headers=headers)
full_page_litecoin_euro = requests.get(litecoin_euro, headers=headers)

soup_dollar_rub = BeautifulSoup(full_page_rus_dollar.content, 'html.parser')
soup_euro_rub = BeautifulSoup(full_page_rus_euro.content, 'html.parser')
soup_pound_rub = BeautifulSoup(full_page_rus_pound.content, 'html.parser')
soup_bitcoin_rub = BeautifulSoup(full_page_rus_bitcoin.content, 'html.parser')
soup_grivna_rub = BeautifulSoup(full_page_rus_grivna.content, 'html.parser')
soup_frank_rub = BeautifulSoup(full_page_rus_frank.content, 'html.parser')
soup_canadadollar_rub = BeautifulSoup(full_page_rus_canadadollar.content, 'html.parser')
soup_ausdollar_rub = BeautifulSoup(full_page_rus_ausdollar.content, 'html.parser')
soup_yen_rub = BeautifulSoup(full_page_rus_yen.content, 'html.parser')
soup_israel_rub = BeautifulSoup(full_page_rus_israel.content, 'html.parser')
soup_ether_rub = BeautifulSoup(full_page_rus_ether.content, 'html.parser')
soup_litecoin_rub = BeautifulSoup(full_page_rus_litecoin.content, 'html.parser')

soup_bitcoin_euro = BeautifulSoup(full_page_euro_bitcoin.content, 'html.parser')
soup_ether_euro = BeautifulSoup(full_page_ether_euro.content, 'html.parser')
soup_litecoin_euro = BeautifulSoup(full_page_litecoin_euro.content, 'html.parser')

convert_rus_dollar = soup_dollar_rub.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_rus_euro = soup_euro_rub.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_rus_pound = soup_pound_rub.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_rus_bitcoin = soup_bitcoin_rub.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_rus_grivna = soup_grivna_rub.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_rus_frank = soup_frank_rub.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_rus_canadadollar = soup_canadadollar_rub.findAll("span",
                                                         {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_rus_ausdollar = soup_ausdollar_rub.findAll("span",
                                                   {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_rus_yen = soup_yen_rub.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_rus_israel = soup_israel_rub.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_rus_ether = soup_ether_rub.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_rus_litecoin = soup_litecoin_rub.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})

convert_bitcoin_euro = soup_bitcoin_euro.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_ether_euro = soup_ether_euro.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_litecoin_euro = soup_litecoin_euro.findAll("span",
                                                   {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})

print(convert_rus_yen[0].text)
print(convert_rus_israel[0].text)
print(convert_rus_frank[0].text)
print(convert_rus_dollar[0].text)

