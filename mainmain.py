import requests

from bs4 import BeautifulSoup

dollar_uah = 'https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&aqs=chrome..69i57j0l7.2783j1j7&sourceid=chrome&ie=UTF-8'
euro_uah = 'https://www.google.com/search?sxsrf=ALeKk01ersKax97WhzSU5_lIFv8bw-ZKFA%3A1594031922272&ei=Mv8CX5WFEOKkrgTX9ap4&q=%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&oq=%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&gs_lcp=CgZwc3ktYWIQAzIKCAAQywEQRhCCAjIFCAAQywEyBQgAEMsBMgIIADIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBggAEAcQHjIFCAAQywE6CAgAEAcQChAeOggIABAIEAcQHjoKCAAQBxAKEB4QKjoECAAQDToJCAAQDRBGEIICULHvAViIhAJgoIYCaANwAHgAgAFoiAG9BpIBAzcuMpgBAKABAaoBB2d3cy13aXo&sclient=psy-ab&ved=0ahUKEwiV5vLTt7jqAhVikosKHde6Cg8Q4dUDCAw&uact=5'
pound_uah = 'https://www.google.com/search?sxsrf=ALeKk01MdsjHZtnRCKn9PFvMcRRjo89zhA%3A1594032012963&ei=jP8CX_WJOpW43AOK5q74Dw&q=%D1%84%D1%83%D0%BD%D1%82+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&oq=%D1%84%D1%83%D0%BD%D1%82+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&gs_lcp=CgZwc3ktYWIQAzIKCAAQsQMQRhCCAjIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeOgQIIxAnOgQIABBDOgUIABCDAToFCAAQsQM6AggAOgkIIxAnEEYQggJQmStYkD9ggkBoAHAAeACAAYABiAGwCZIBAzkuNJgBAKABAaoBB2d3cy13aXq4AQI&sclient=psy-ab&ved=0ahUKEwj1_5H_t7jqAhUVHHcKHQqzC_8Q4dUDCAw&uact=5'
bitcoin_uah = 'https://www.google.com/search?sxsrf=ALeKk02JazDsagUc6USf3TjjpzTPoWR4nQ%3A1594032021843&ei=lf8CX5KHM--JrwSZromoBg&q=%D0%B1%D0%B8%D1%82%D0%BA%D0%BE%D0%B8%D0%BD+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&oq=%D0%B1%D0%B8%D1%82%D0%BA%D0%BE%D0%B8%D0%BD+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&gs_lcp=CgZwc3ktYWIQAzIKCAAQywEQRhCCAjIFCAAQywEyBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeOgQIIxAnOgcIIxAnEIsDOgUIABCDAToFCAAQsQM6AggAOgcIIxDqAhAnOgoIIxDqAhAnEIsDOgQIABBDOgcIABCxAxBDOgoIABCxAxBGEIICUOLtAliglQNgiZcDaAJwAHgAgAGeAYgB_QySAQQxNC40mAEAoAEBqgEHZ3dzLXdperABCrgBAg&sclient=psy-ab&ved=0ahUKEwjSpbCDuLjqAhXvxIsKHRlXAmUQ4dUDCAw&uact=5'
rubl_uah = 'https://www.google.com/search?sxsrf=ALeKk02PRhiOpv4IqSkEhMl_xvZ1lF4bmw%3A1594127354384&ei=-nMEX6_3FvLlrgSH1Iz4CQ&q=%D1%80%D1%83%D0%B1%D0%BB%D1%8C+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&oq=%D1%80%D1%83%D0%B1%D0%BB%D1%8C+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&gs_lcp=CgZwc3ktYWIQAzIKCAAQywEQRhCCAjIFCAAQywEyBQgAEMsBMgUIABDLATICCAAyBQgAEMsBMgUIABDLATIFCAAQywEyAggAMgUIABDLAToECCMQJzoECAAQQzoFCAAQsQM6CAgAELEDEIMBOgYIIxAnEBM6BwgAELEDEEM6CQgjECcQRhCCAlD6TFiVYWD9YmgAcAB4AIABd4gB0QmSAQQxMi4ymAEAoAEBqgEHZ3dzLXdpeg&sclient=psy-ab&ved=0ahUKEwiv3LyVm7vqAhXysosKHQcqA58Q4dUDCAw&uact=5'
frank_uah = 'https://www.google.com/search?sxsrf=ALeKk01yY8fPzIsd7ikSs3iW8xmGd3xefQ%3A1594128540554&ei=nHgEX9qlIcenrgSj-ZiYCQ&q=%D1%84%D1%80%D0%B0%D0%BD%D0%BA%D0%B8+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B0%D0%BC&oq=%D1%84%D1%80%D0%B0%D0%BD%D0%BA%D0%B8+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B0%D0%BC&gs_lcp=CgZwc3ktYWIQAzIECCMQJzIFCAAQywEyBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeOgQIABBDOggIABCxAxCDAToFCAAQsQM6AggAOgcIABAKEMsBUIIaWNgqYLkraABwAHgAgAFziAGVCZIBBDEyLjKYAQCgAQGqAQdnd3Mtd2l6&sclient=psy-ab&ved=0ahUKEwja44rLn7vqAhXHk4sKHaM8BpMQ4dUDCAw&uact=5'
canadadollar_uah = 'https://www.google.com/search?sxsrf=ALeKk02BtnxGtKGB9eFVOYevCk9zB-oKBw%3A1594128547152&ei=o3gEX-jmCNWk3AP496CICQ&q=%D0%BA%D0%B0%D0%BD%D0%B0%D0%B4%D1%81%D0%BA%D0%B8%D0%B9+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80&oq=rfyflcrbq+ljkfh&gs_lcp=CgZwc3ktYWIQARgAMg4IABAKEMsBECoQRhCCAjoECCMQJzoFCAAQsQM6CAgAELEDEIMBOgIIADoGCAAQChAqOgQIABAKOgsIABAKEAEQywEQKjoJCAAQChABEMsBOhAIABAKEAEQywEQKhBGEIICOgYIABAWEB5Q78IKWNHVCmD44wpoAHAAeACAAV-IAdsJkgECMTWYAQCgAQGqAQdnd3Mtd2l6&sclient=psy-ab'
ausdollar_uah = 'https://www.google.com/search?sxsrf=ALeKk02wbVuN_Q3zO_2DbabYEV9Juih7kw%3A1594128724512&ei=VHkEX6voHsP1qwG2-r-wBg&q=%D0%B0%D0%B2%D1%81%D1%82%D1%80%D0%B0%D0%BB%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D0%B9+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80&oq=%D0%B0%D0%B2%D1%81%D1%82%D1%80&gs_lcp=CgZwc3ktYWIQARgBMgQIIxAnMgQIABBDMgUIABDLATIFCAAQywEyBQgAELEDMgUIABCxAzIFCAAQywEyBAgAEEMyBQgAEMsBMgUIABDLAToGCCMQJxATOggIABCxAxCDAToCCAA6BggAEAoQQzoHCCMQ6gIQJzoHCAAQsQMQQ1CurQlYlMcJYLPTCWgCcAB4AIABcogB9gSSAQM1LjKYAQCgAQGqAQdnd3Mtd2l6sAEK&sclient=psy-ab'
yen_uah = 'https://www.google.com/search?sxsrf=ALeKk01uuVKS5bV9KqzMKOj8_fWLN003yw%3A1594128883529&ei=83kEX7juH8borgThgqXIBw&q=%D1%8F%D0%BF%D0%BE%D0%BD%D1%81%D0%BA%D0%B0%D1%8F+%D0%B8%D0%B5%D0%BD%D0%B0&oq=%D1%8F%D0%BF%D0%BE%D0%BD%D1%81&gs_lcp=CgZwc3ktYWIQARgAMgkIABBDEEYQggIyBQgAEMsBMgUIABDLATIFCAAQywEyBAgAEEMyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLAToECCMQJzoFCAAQsQM6AggAOgYIABAKECo6BAgAEAo6BwgjEOoCECc6BwgAELEDEEM6CAgAELEDEIMBOgoIABCxAxCDARBDUKn-BljSkgdglp0HaANwAHgAgAFyiAGoBZIBAzcuMZgBAKABAaoBB2d3cy13aXqwAQo&sclient=psy-ab'
israel_uah = 'https://www.google.com/search?sxsrf=ALeKk0131faM-35wLKal-gYy_668ZQXh-w%3A1594129003024&ei=a3oEX_B_6OOuBLqqsJAK&q=%D1%88%D0%B5%D0%BA%D0%B5%D0%BB%D0%B8+%D0%B2+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D1%8B&oq=itrtkb&gs_lcp=CgZwc3ktYWIQARgBMgsIABAKEAEQywEQKjIECAAQCjIECAAQCjIECAAQCjIECAAQCjIECAAQCjIECAAQCjIJCAAQChABEMsBMgQIABAKMgQIABAKOgYIIxAnEBM6BAgjECc6BQgAELEDOgIIADoICAAQsQMQgwE6BggAEAoQKjoECAAQHjoGCAAQChAeULrSB1jk2QdgoOUHaABwAHgAgAFviAGKBJIBAzUuMZgBAKABAaoBB2d3cy13aXo&sclient=psy-ab'
ether_uah = 'https://www.google.com/search?sxsrf=ALeKk00wZtweVL3A0QfJaZEEmLWso-uscg%3A1594129547210&ei=i3wEX8a4DMqMrwS7uqSoCw&q=%D1%8D%D1%84%D0%B8%D1%80+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&oq=%D1%8D%D1%84%D0%B8%D1%80+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&gs_lcp=CgZwc3ktYWIQAzIKCAAQywEQRhCCAjoECAAQRzoFCAAQywE6BggAEBYQHjoICAAQFhAKEB5QlTtYiURgiEVoAHABeACAAWOIAagFkgEBOJgBAKABAaoBB2d3cy13aXo&sclient=psy-ab&ved=0ahUKEwiGqoyro7vqAhVKxosKHTsdCbUQ4dUDCAw&uact=5'
litecoin_uah = 'https://www.google.com/search?sxsrf=ALeKk01PwbJ2oDnNkff6GtRiQBu3SYX8EA%3A1594129978420&ei=On4EX7SSGaOAk74P88uZwAU&q=%D0%BB%D0%B0%D0%B9%D1%82%D0%BA%D0%BE%D0%B8%D0%BD+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&oq=%D0%BB%D0%B0%D0%B9%D1%82%D0%BA%D0%BE%D0%B8%D0%BD+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&gs_lcp=CgZwc3ktYWIQAzIJCCMQJxBGEIICMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeOgQIIxAnOgIIADoFCAAQsQM6CAgAELEDEIMBOgQIABBDOgUIABDLAVDbE1inN2CJOGgBcAB4AIABW4gB9wqSAQIxOJgBAKABAaoBB2d3cy13aXo&sclient=psy-ab&ved=0ahUKEwi0l9v4pLvqAhUjwMQBHfNlBlgQ4dUDCAw&uact=5'
zlotiy_uah = 'https://www.google.com/search?q=1+%D0%B7%D0%BB%D0%BE%D1%82%D0%B8%D0%B9+%D0%B2+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B0%D1%85&oq=1+%D0%B7%D0%BB%D0%BE%D1%82%D0%B8%D0%B9+%D0%B2+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B0%D1%85&aqs=chrome..69i57j0l7.9007j1j7&sourceid=chrome&ie=UTF-8'

bitcoin_dollar = 'https://www.google.com/search?rlz=1C1CHBF_enUA768UA768&sxsrf=ALeKk015oZTErxYirgBF7grEnOxq6gKbYA%3A1594325323134&ei=S3kHX8vtB-HMrgTdj7fwBA&q=%D0%B1%D0%B8%D1%82%D0%BA%D0%BE%D0%B8%D0%BD+%D0%B2+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0%D1%85&oq=%D0%B1%D0%B8%D1%82%D0%BA%D0%BE%D0%B8%D0%BD+%D0%B2+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0%D1%85&gs_lcp=CgZwc3ktYWIQAzIKCAAQxAIQRhCCAjICCAAyAggAMgIIADICCAAyBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeOgcIABBHELADOgUIABCxAzoKCAAQsQMQRhCCAjoFCAAQywFQhx1YqytgmS5oAXAAeACAAZ0BiAGzCJIBAzYuNJgBAKABAaoBB2d3cy13aXo&sclient=psy-ab&ved=0ahUKEwiLv6rU_MDqAhVhposKHd3HDU4Q4dUDCAw&uact=5'
ether_dollar = 'https://www.google.com/search?rlz=1C1CHBF_enUA768UA768&sxsrf=ALeKk02JnvNRSBsG1kdk2lexsHY168G8oQ%3A1594325342477&ei=XnkHX5zUHOPIrgSEpLP4Ag&q=%D1%8D%D1%84%D0%B8%D1%80+%D0%B2+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0%D1%85&oq=%D1%8D%D1%84%D0%B8%D1%80+%D0%B2+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0%D1%85&gs_lcp=CgZwc3ktYWIQAzIECAAQQzIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIICAAQBxAFEB4yCAgAEAcQBRAeMggIABAHEAUQHlD21wNYkf8DYKGKBGgAcAB4AIABkwKIAYkGkgEFMi4zLjGYAQCgAQGqAQdnd3Mtd2l6&sclient=psy-ab&ved=0ahUKEwic-8bd_MDqAhVjpIsKHQTSDC8Q4dUDCAw&uact=5'
litecoin_dollar = 'https://www.google.com/search?rlz=1C1CHBF_enUA768UA768&sxsrf=ALeKk01zfMKg02jqtVgwl0YEaTBly-9wcQ%3A1594325410178&ei=onkHX7atCsGxrgTMvJTQAw&q=%D0%BB%D0%B0%D0%B9%D1%82%D0%BA%D0%BE%D0%B8%D0%BD+%D0%B2+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0%D1%85&oq=%D0%BB%D0%B0%D0%B9%D1%82%D0%BA%D0%BE%D0%B8%D0%BD+%D0%B2+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0%D1%85&gs_lcp=CgZwc3ktYWIQAzIJCAAQQxBGEIICMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjoECCMQJzoFCAAQsQM6CAgAELEDEIMBOgcIIxDqAhAnOgIIADoECAAQQzoKCAAQsQMQgwEQQzoHCAAQsQMQQzoHCAAQFBCHAjoMCAAQFBCHAhBGEIICOggIABAWEAoQHlD7kwRYsdUEYJLYBGgBcAB4AIAB0AOIAf4YkgEKMS4xNy4xLjAuMZgBAKABAaoBB2d3cy13aXqwAQo&sclient=psy-ab&ved=0ahUKEwi2huv9_MDqAhXBmIsKHUweBToQ4dUDCAw&uact=5'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
full_page_dollar = requests.get(dollar_uah, headers=headers)
full_page_euro = requests.get(euro_uah, headers=headers)
full_page_pound = requests.get(pound_uah, headers=headers)
full_page_bitcoin = requests.get(bitcoin_uah, headers=headers)
full_page_rubl = requests.get(rubl_uah, headers=headers)
full_page_frank = requests.get(frank_uah, headers=headers)
full_page_canadadollar = requests.get(canadadollar_uah, headers=headers)
full_page_ausdollar = requests.get(ausdollar_uah, headers=headers)
full_page_yen = requests.get(yen_uah, headers=headers)
full_page_israel = requests.get(israel_uah, headers=headers)
full_page_ether = requests.get(ether_uah, headers=headers)
full_page_litecoin = requests.get(litecoin_uah, headers=headers)
#full_page_zlotiy = requests.get(zlotiy_uah, headers=headers)

full_page_bitcoin_dollar = requests.get(bitcoin_dollar, headers=headers)
full_page_ether_dollar = requests.get(ether_dollar, headers=headers)
full_page_litecoin_dollar = requests.get(litecoin_dollar, headers=headers)

soup_dollar = BeautifulSoup(full_page_dollar.content, 'html.parser')
soup_euro = BeautifulSoup(full_page_euro.content, 'html.parser')
soup_pound = BeautifulSoup(full_page_pound.content, 'html.parser')
soup_bitcoin = BeautifulSoup(full_page_bitcoin.content, 'html.parser')
soup_rubl = BeautifulSoup(full_page_rubl.content, 'html.parser')
soup_frank = BeautifulSoup(full_page_frank.content, 'html.parser')
soup_canadadollar = BeautifulSoup(full_page_canadadollar.content, 'html.parser')
soup_ausdollar = BeautifulSoup(full_page_ausdollar.content, 'html.parser')
soup_yen = BeautifulSoup(full_page_yen.content, 'html.parser')
soup_israel = BeautifulSoup(full_page_israel.content, 'html.parser')
soup_ether = BeautifulSoup(full_page_ether.content, 'html.parser')
soup_litecoin = BeautifulSoup(full_page_litecoin.content, 'html.parser')
#soup_zlotiy = BeautifulSoup(full_page_zlotiy, 'html.parser')

soup_bitcoin_dollar = BeautifulSoup(full_page_bitcoin_dollar.content, 'html.parser')
soup_ether_dollar = BeautifulSoup(full_page_ether_dollar.content, 'html.parser')
soup_litecoin_dollar = BeautifulSoup(full_page_litecoin_dollar.content, 'html.parser')

convert_dollar = soup_dollar.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_euro = soup_euro.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_pound = soup_pound.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_bitcoin = soup_bitcoin.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_rubl = soup_rubl.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_frank = soup_frank.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_canadadollar = soup_canadadollar.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_ausdollar = soup_ausdollar.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_yen = soup_yen.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_israel = soup_israel.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_ether = soup_ether.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_litecoin = soup_litecoin.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
#convert_zlotiy = soup_zlotiy.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})

convert_bitcoin_dollar = soup_bitcoin_dollar.findAll("span",
                                                     {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_ether_dollar = soup_ether_dollar.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
convert_litecoin_dollar = soup_litecoin_dollar.findAll("span",
                                                       {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})

print('GET STARTED')

'''print('1 йен = ',convert_yen[0].text, 'гривнам')
print('1 rfyflf ljkkfh =', convert_canadadollar[0].text, 'гривнам')'''
