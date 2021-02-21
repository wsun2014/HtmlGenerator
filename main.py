# Generate the html file based on csv file provided

from os.path import isfile
import csv
from bs4 import BeautifulSoup


def get_courses(csv_file: str) -> [str]:
    if not isfile(csv_file):
        raise Exception(f"{csv_file} does not exist")
    courses = []
    with open(csv_file, 'r') as file:
        dict_reader = csv.DictReader(file)
        for course in dict_reader:
            soup = BeautifulSoup(course["嵌入代码"], 'lxml')
            iframe_tag = soup.find('iframe')
            url = iframe_tag['src']
            if not url.startswith("https:"):
                url = f"https:{url}&amp;high_quality=1&amp;danmaku=0"
            courses.append({"课程名称": course["课程名称"], "嵌入代码": url})
    return courses


def generate_html_file(html_file_path: str, html_dst_file_path: str, courses: []):
    content: str
    if not isfile(html_file_path):
        raise Exception(f"{html_file_path} does not exist")
    with open(html_file_path, 'r') as html_file:
        content = html_file.read()
    soup = BeautifulSoup(content, 'lxml')
    ul = soup.find("ul", {"id": "menu"})
    for course in courses:
        li = soup.new_tag("li", attrs={"onclick": "checklist(this);"})
        a = soup.new_tag("a", attrs={"href": course["嵌入代码"], "target": "aaa"})
        a.string = course["课程名称"]
        li.append(a)
        ul.append(li)
    with open(html_dst_file_path, 'w') as html_dst_file:
        html_dst_file.write(soup.prettify())


if __name__ == '__main__':
    courses = get_courses("/Users/weisun/Documents/workspace/HtmlListGenerator/孝就是道（曾仕强） - Sheet1.csv")
    generate_html_file("/Users/weisun/Documents/workspace/HtmlListGenerator/测试.html",
                       "/Users/weisun/Documents/workspace/HtmlListGenerator/result/test.html", courses)
