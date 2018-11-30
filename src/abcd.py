import requests
from bs4 import BeautifulSoup
import re
import os


def main():
    # 最新のやつを調べる
    url = "http://atcoder.jp/contest/archive?categories=5&mode=tmp"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    abc = soup.find("a", text=re.compile("AtCoder Beginner Contest"))
    latest = abc.string.split()[-1]
    # 作りたい場所
    path = ""
    with open("./src/latest.txt", "w+") as file:
        if len(file.read()) == 0 or int(file.read()) < latest:
            file.write(latest)
            # こっからディレクトリを作る
            # とりあえず今のパスでいいや
            createfolder(path, latest)


def createtestcase(count, path, foldername, course="abc"):
    problem = course+str(count).zfill(3)
    baseurl = "https://"+problem+".contest.atcoder.jp"
    problemsurl = baseurl+"/assignments"
    # 問題一覧ページから直接リンクを得る
    problemsreq = requests.get(problemsurl)
    problemsset = []
    if problemsreq.status_code == requests.codes.ok:
        problemsoup = BeautifulSoup(problemsreq.content, 'lxml')
        problemlinks = problemsoup.find_all("a", class_="linkwrapper")
        for p in problemlinks:
            target = baseurl+p.get("href")
            if target not in problemsset:
                problemsset.append(target)
        if len(problemsset) == 0:
            print("なんかおかしい")
            exit()
    for idx, p in enumerate(problemsset):
        print(p)
        r = requests.get(p)
        if r.status_code == requests.codes.ok:
            soup = BeautifulSoup(r.content, 'lxml')
            parts = soup.find_all("div", {"class": "part"})
            for p in parts:
                # 入力例って書いてあるh3がほしい
                if p.find("h3", text=re.compile("入力例")):
                    # その中のpreの中身がテストケース
                    testcase = p.find("pre")
                    if testcase.string:
                        source = testcase.string.rstrip().lstrip()
                        print(source)
                        with open(path+"/"+foldername+"/"+"abcdefghijklmn"[idx]+".txt", "w") as f:
                            f.write(source)
                        break  # 最初の一個だけでいい。全部欲しいときはbreakとればいいんじゃないかな


def createfolder(path, n):
    subfolders = ["testcase", "src"]
    for x in range(1, int(n)+1):
        numbering = path+"/"+str(x).zfill(3)
        if not os.path.exists(numbering):
            os.mkdir(numbering)
        for s in subfolders:
            if not os.path.exists(numbering+"/"+s):
                os.mkdir(numbering+"/"+s)
                if s == "testcase":
                    createtestcase(x, numbering, s)
                elif s == "src":
                    pass  # とくにやることなかったわ


if __name__ == '__main__':
    main()
