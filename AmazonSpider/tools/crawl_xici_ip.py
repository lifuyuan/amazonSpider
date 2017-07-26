import requests
from scrapy.selector import Selector
import psycopg2
import logging

conn = psycopg2.connect(database="amazon_spider", user="fuyuan", password="fuyuan", host="127.0.0.1", port="5432")
cursor = conn.cursor()


def crawl_ips():
    # 爬取西刺的免费ip代理
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }
    http_proxy = "http://110.73.13.153:8123"
    proxyDict = {"http": http_proxy}

    for i in range(2000):
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers, proxies=proxyDict)
        selector = Selector(text=re.text)
        all_trs = selector.css("#ip_list tr")
        ip_lists = []
        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract_first()
            if speed_str:
                speed = float(speed_str.split("秒")[0])
            all_texts = tr.css("td::text").extract()
            ip = all_texts[0]
            port = all_texts[1]
            proxy_type = all_texts[5]
            ip_lists.append((ip, port, proxy_type, speed))
        for ip_info in ip_lists:
            if ip_info[2] == "HTTP" or ip_info[2] == "HTTPS":
                cursor.execute(
                    "insert into proxy_ips(ip, port, speed, proxy_type) values ('{0}', '{1}', {2}, '{3}')".format(
                        ip_info[0], ip_info[1], ip_info[3], ip_info[2]
                    )
                )
                conn.commit()
    cursor.close()
    conn.close()


class GetIP(object):
    def judge_ip(self, ip, port, proxy_type):
        # 判断ip是否可用
        http_url = "http://www.baidu.com"
        proxy_url = "{0}://{1}:{2}".format(proxy_type, ip, port)
        try:
            proxy_dict = {
                "{0}".format(proxy_type.lower()): proxy_url
            }
            re = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            print("invalid")
            self.delete_ip(ip)
            return False
        else:
            code = re.status_code
            if code >= 200 and code < 300:
                print("effective ip")
                return True
            else:
                print("invalid")
                self.delete_ip(ip)
                return False

    def delete_ip(self, ip):
        delete_sql = """
            delete from proxy_ips where ip = '{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def get_random_ip(self):
        sql = """
            select ip, port, proxy_type from proxy_ips order by random() limit 1
        """
        cursor.execute(sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            proxy_type = ip_info[2]
            print(ip)
            judge_re = self.judge_ip(ip, port, proxy_type)
            if judge_re:
                return "{0}://{1}:{2}".format(proxy_type, ip, port)
            else:
                return self.get_random_ip()


if __name__ == "__main__":
    get_ip = GetIP()
    get_ip.get_random_ip()
