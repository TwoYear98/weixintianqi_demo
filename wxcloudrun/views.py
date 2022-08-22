import time
from flask import render_template, request, abort
from run import app
# from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
# from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import xmltodict


@app.route("/api/get_message", methods=['POST', 'GET'])
def get_message():
    """
    :return: 返回消息
    """
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    if request.method == 'GET':
        return "Success"
    elif request.method == 'POST':
        # 表示微信服务器转发消息到本地服务器
        xml_str = request.data
        xml_dict = xmltodict.parse(xml_str)
        xml_dict1 = xml_dict.get('xml')
        # print(xml_dict1)
        # 提取消息类型
        msg_type = xml_dict1.get('MsgType')

        # print(msg_type)
        if msg_type == 'text':
            # 这是文本消息
            # 构造返回值，由为微信服务器回复消息
            # 重点：以下参数值一个不能少，一个字母不能错，大小写不能错，键名必须完全一样
            resp_dict = {
                "xml": {
                    'ToUserName': xml_dict1.get('FromUserName'),
                    'FromUserName': xml_dict1.get('ToUserName'),
                    'CreateTime': int(time.time()),
                    'MsgType': 'text',
                    'Content': xml_dict1.get('Content'),
                }
            }
            # print(resp_dict)
        else:
            resp_dict = {
                "xml": {
                    'ToUserName': xml_dict1.get('FromUserName'),
                    'FromUserName': xml_dict1.get('ToUserName'),
                    'CreateTime': int(time.time()),
                    'MsgType': 'text',
                    'Content': "我们收到您的消息，谢谢您"
                }
            }
            # 将字典转为xml字符串
        resp_xml_str = xmltodict.unparse(resp_dict)
        print(resp_xml_str)
        # # 返回消息字符串
        return resp_xml_str
