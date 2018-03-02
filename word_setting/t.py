# coding=utf-8

from flask import Flask, make_response, request


app = Flask(__name__)


@app.route("/set_cookie")
def set_cookie():
    """设置cookie"""
    #先创建响应对象
    resp = make_response("set cookie OK")
    # 通过max_age控制cookie有效期, 单位:秒
    resp.set_cookie("wancheng2", "python2", max_age=30)
    return resp


@app.route("/get_cookie")
def get_cookie():
    """获取cookie"""
    cookie = request.cookies.get("wancheng2")
    return "cookie wancheng2=%s" % cookie


@app.route("/delete_cookie")
def delete_cookie():
    """删除cookie"""
    resp = make_response("delete cookie ok")
    resp.delete_cookie("wancheng2")
    return resp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
