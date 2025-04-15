#!/usr/bin/env python
# coding=utf-8
import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, current_dir)
target_domain = os.environ.get('TARGET_DOMAIN', None)
domain_dir = None
if current_dir != '' and target_domain:
    os.chdir(current_dir)
    candidate_dir = os.path.join(current_dir, 'target_domains', target_domain)
    if os.path.exists(candidate_dir):
        domain_dir = candidate_dir
        sys.path.insert(0, domain_dir)

from zmirror.zmirror import app as application, infoprint, errprint

if domain_dir:
    infoprint("Registered domain path: " + domain_dir)

__author__ = 'Aploium <i@z.codes>'


def main():
    from zmirror.zmirror import my_host_port, built_in_server_host, \
        built_in_server_debug, built_in_server_extra_params, \
        errprint

    if my_host_port is None:
        my_host_port = int(os.environ.get('WEB_PORT', os.environ.get('PORT', '8000')))
    try:
        application.run(
            port=my_host_port,

            threaded="processes" not in built_in_server_extra_params,

            # built_in_server_host='0.0.0.0'
            # built_in_server_debug=False

            debug=built_in_server_debug,  # 默认是开启debug模式的
            # 默认只允许本机访问, 如果你希望让外网访问, 请根据上面的注释修改配置文件
            host=built_in_server_host,

            **built_in_server_extra_params  # extra params
        )
    except OSError as e:
        if e.errno in (98, 10013):  # Address already in use, 98 for linux, 10013 for win
            errprint("Port {port} was occupied by other program, please close it.\n"
                     "You can see which process is using your port by the following command:\n"
                     "    Linux: netstat -apn |grep \":{port}\"\n"
                     "    Windows: netstat -ano |find \":{port}\"\n\n"
                     "Or change zmirror\'s port: change(add, if not exist) the `my_host_port` setting in `config.py`\n"
                     "eg: my_host_port=81".format(port=my_host_port))
            exit()
        else:
            raise


try:
    import domain_handler
except Exception as e:
    infoprint("There is no special domain handler registered for this domain:", target_domain)
    errprint("Exception message:", e)
else:
    application.register_blueprint(domain_handler.page)
    infoprint("A domain handler is registered for this domain:", target_domain)

if __name__ == '__main__':
    main()
