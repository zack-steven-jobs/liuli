# encoding=utf-8
import os
import sys
import simplejson
import MySQLdb


class MySQLdbWrapper:

    conn = None

    def connect(self):
        self.conn = MySQLdb.connect('localhost', 'root', 'P@55word', 'market')
        self.conn.set_character_set('utf8')

    def cursor(self):
        try:
            if not self.conn:
                self.connect()
            return self.conn.cursor()
        except MySQLdb.OperationalError:
            self.connect()
            return self.conn.cursor()

_db = MySQLdbWrapper()

cate_map_dic = {"442": "系统安全",
                "435": "系统安全",
                "441": "系统安全",
                "手机安全": "系统安全",
                "系统工具": "系统安全",
                "安全杀毒": "系统安全",
                "11556": "主题桌面",
                "311": "主题桌面",
                "407": "主题桌面",
                "408": "主题桌面",
                "409": "主题桌面",
                "410": "主题桌面",
                "453": "主题桌面",
                "454": "主题桌面",
                "455": "主题桌面",
                "456": "主题桌面",
                "457": "主题桌面",
                "458": "主题桌面",
                "459": "主题桌面",
                "460": "主题桌面",
                "461": "主题桌面",
                "462": "主题桌面",
                "463": "主题桌面",
                "464": "主题桌面",
                "465": "主题桌面",
                "466": "主题桌面",
                "467": "主题桌面",
                "468": "主题桌面",
                "469": "主题桌面",
                "470": "主题桌面",
                "471": "主题桌面",
                "472": "主题桌面",
                "473": "主题桌面",
                "474": "主题桌面",
                "主题桌面": "主题桌面",
                "美化.壁纸": "主题桌面",
                "壁纸主题铃声": "主题桌面",
                "主题插件": "主题桌面",
                "动态壁纸": "主题桌面",
                "主题壁纸": "主题桌面",
                "438": "聊天通讯",
                "479": "聊天通讯",
                "通信聊天": "聊天通讯",
                "通讯.聊天": "聊天通讯",
                "社交通讯": "聊天通讯",
                "通话通讯": "聊天通讯",
                "通话增强": "聊天通讯",
                "即时通讯": "聊天通讯",
                "短信增强": "聊天通讯",
                "0": "生活实用",
                "494": "生活实用",
                "404": "生活实用",
                "405": "生活实用",
                "406": "生活实用",
                "442": "生活实用",
                "445": "生活实用",
                "447": "生活实用",
                "449": "生活实用",
                "450": "生活实用",
                "451": "生活实用",
                "452": "生活实用",
                "411": "生活实用",
                "412": "生活实用",
                "413": "生活实用",
                "437": "生活实用",
                "443": "生活实用",
                "480": "生活实用",
                "481": "生活实用",
                "482": "生活实用",
                "483": "生活实用",
                "484": "生活实用",
                "485": "生活实用",
                "486": "生活实用",
                "综合服务": "生活实用",
                "创意休闲": "生活实用",
                "其他": "生活实用",
                "DIY作品": "生活实用",
                "必备软件": "生活实用",
                "便捷生活": "生活实用",
                "辅助工具": "生活实用",
                "休闲娱乐": "生活实用",
                "436": "影音阅读",
                "544": "影音阅读",
                "545": "影音阅读",
                "10035": "影音阅读",
                "10036": "影音阅读",
                "10037": "影音阅读",
                "530": "影音阅读",
                "531": "影音阅读",
                "495": "影音阅读",
                "125": "影音阅读",
                "478": "影音阅读",
                "544": "影音阅读",
                "电子图书": "影音阅读",
                "音乐音频": "影音阅读",
                "视频播放": "影音阅读",
                "影音.图像": "影音阅读",
                "阅读.图书": "影音阅读",
                "漫画电子书": "影音阅读",
                "影音播放": "影音阅读",
                "图书阅读": "影音阅读",
                "音乐视频": "影音阅读",
                "图书动漫": "影音阅读",
                "444": "学习办公",
                "办公学习": "学习办公",
                "办公.财经": "学习办公",
                "资讯.词典": "学习办公",
                "办公理财": "学习办公",
                "学习办公": "学习办公",
                "教育学习": "学习办公",
                "商务办公": "学习办公",
                "医疗保健": "学习办公",
                "437": "网络社区",
                "440": "网络社区",
                "475": "网络社区",
                "476": "网络社区",
                "477": "网络社区",
                "497": "网络社区",
                "498": "网络社区",
                "499": "网络社区",
                "社交网络": "网络社区",
                "网络.社区": "网络社区",
                "社交网络": "网络社区",
                "社交微博": "网络社区",
                "445": "出行导航",
                "489": "出行导航",
                "490": "出行导航",
                "气象交通": "出行导航",
                "旅行.地图": "出行导航",
                "地图导航": "出行导航",
                "天气时间": "出行导航",
                "出行地图": "出行导航",
                "446": "购物理财",
                "448": "购物理财",
                "487": "购物理财",
                "488": "购物理财",
                "493": "购物理财",
                "金融理财": "购物理财",
                "购物支付": "购物理财",
                "生活.购物": "购物理财",
                "生活购物旅行": "购物理财",
                "网购支付": "购物理财",
                "购物理财": "购物理财",
                "434": "输入浏览",
                "浏览器": "输入浏览",
                "输入法": "输入浏览",
                "输入法.系统工具": "输入浏览",
                "网络浏览": "输入浏览",
                "439": "摄影美化",
                "摄影美化": "摄影美化",
                "影音拍摄": "摄影美化",
                "拍摄美化": "摄影美化",
                "摄影图像": "摄影美化",
                "443": "新闻资讯",
                "新闻阅读": "新闻资讯",
                "新闻资讯": "新闻资讯",
                "14346": "窗口小部件",
                "431": "益智休闲",
                "432": "益智休闲",
                "492": "益智休闲",
                "益智休闲": "益智休闲",
                "必备游戏": "益智休闲",
                "益智": "新闻资讯",
                "420": "角色冒险",
                "421": "角色冒险",
                "422": "角色冒险",
                "角色扮演": "角色冒险",
                "冒险闯关": "角色冒险",
                "423": "动作格斗",
                "425": "动作格斗",
                "426": "动作格斗",
                "427": "动作格斗",
                "动作射击": "动作格斗",
                "动作冒险": "动作格斗",
                "格斗对战": "动作格斗",
                "街机模拟": "动作格斗",
                "对战格斗": "动作格斗",
                "动作游戏": "动作格斗",
                "433": "策略经营",
                "419": "策略经营",
                "策略经营": "策略经营",
                "策略塔防": "策略经营",
                "模拟经营": "策略经营",
                "策略": "策略经营",
                "428": "体育竞技",
                "429": "体育竞技",
                "体育竞速": "体育竞技",
                "赛车竞速": "体育竞技",
                "体育运动": "体育竞技",
                "赛车游戏": "体育竞技",
                "424": "飞行射击",
                "竞技飞行": "飞行射击",
                "射击飞行": "飞行射击",
                "飞行射击": "飞行射击",
                "射击": "飞行射击",
                "430": "桌游棋牌",
                "557": "桌游棋牌",
                "558": "桌游棋牌",
                "益智棋牌": "桌游棋牌",
                "棋牌休闲": "桌游棋牌",
                "棋牌桌游": "桌游棋牌",
                "策略棋牌": "桌游棋牌",
                "421": "模拟养成",
                "模拟游戏": "模拟养成",
                "经营养成": "模拟养成",
                "虚拟养成": "模拟养成",
                "养成经营": "模拟养成",
                "网络游戏": "网络游戏",
                "手机网游": "网络游戏",
                "559": "音乐其他",
                "音乐游戏": "音乐其他",
                "其他游戏": "音乐其他",
                "532": "书籍",
                "533": "书籍",
                "534": "书籍",
                "535": "书籍",
                "536": "书籍",
                "537": "书籍",
                "538": "书籍",
                "539": "书籍",
                "540": "书籍",
                "541": "书籍",
                "542": "书籍",
                "543": "书籍",
                "491": "书籍",
                "546": "漫画",
                "547": "漫画",
                "548": "漫画",
                "549": "漫画",
                "550": "漫画",
                "551": "漫画",
                "552": "漫画",
                "553": "漫画",
                "554": "漫画",
                "555": "漫画",
                "556": "漫画",
                "12095": "有声阅读",
                "12096": "有声阅读",
                "14376": "资料",
                "10992": "笑话",
                "414": "音乐",
                "511": "音乐",
                "496": "音乐",
                "500": "音乐",
                "501": "音乐",
                "502": "音乐",
                "503": "音乐",
                "504": "音乐",
                "505": "音乐",
                "506": "音乐",
                "507": "音乐",
                "508": "音乐",
                "509": "音乐",
                "510": "音乐",
                "511": "音乐",
                "512": "视频",
                "513": "视频",
                "514": "视频",
                "515": "视频",
                "516": "视频",
                "517": "视频",
                "518": "视频",
                "519": "视频",
                "520": "视频",
                "521": "视频",
                "522": "视频",
                "523": "视频",
                "524": "视频",
                "525": "视频",
                "526": "视频",
                "527": "视频",
                "528": "视频",
                "529": "视频",
                }


def start_refresh():
    while True:
        apks = get_apks()
        if not apks:
            return
        report_list = []
        for apk in apks:
            try:
                if not apk[1]:
                    cate = '其他'
                else:
                    cate = cate_map_dic.get(apk[1].strip(), '生活实用')
                report_list.append((apk[0], cate))
            except Exception as e:
                print file
                print e
        report_status(report_list)


def report_status(list):
    for l in list:
        try:
            cursor = _db.cursor()
            sql = "UPDATE final_app set is_refresh=1, category = %s where id = %s"
            cursor.execute(sql, (l[1], l[0]))
            cursor.connection.commit()
        except MySQLdb.Error as e:
            print e
        finally:
            cursor.close()


def get_apks():
    try:
        cursor = _db.cursor()
        sql = "SELECT id,category from final_app where is_refresh is null limit 100"
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except MySQLdb.Error as e:
        print e
    finally:
        cursor.close()

if __name__ == "__main__":
    start_refresh()
