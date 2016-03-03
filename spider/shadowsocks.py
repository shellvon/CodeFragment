# encoding=utf-8
# author:shellvon

import re
import random
import urllib2
import subprocess


def getShadowSocksParam():
    url = 'http://www.ishadowsocks.com/'
    data = urllib2.urlopen(url, timeout=30).read()
    regex = r'(?P<group>A|B|C)服务器地址:(?P<name>[^<]+)</h4>\n\s*<h4>端口:(?P<port>\d+)</h4>\n\s*<h4>\w密码:(?P<password>[^<]+)</h4>\n\s*<h4>加密方式:(?P<method>[^<]+)</h4>\n\s*<h4>状态:<font color="green">正常</font></h4>'
    return [dict(map(lambda (k, v):(k, v.upper()), m.groupdict().iteritems())) for m in re.finditer(regex, data)]


def runSSLocal(kwargs):
    cmd = 'sslocal -s {name} -p {port} -l 443 -k {password} -m {method} -d start'.format(
        **kwargs)
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,  universal_newlines=True)
    stderr = p.stderr.read()
    if stderr:
        pid_regex = 'already started at pid (?P<pid>\d+)'
        m = re.search(pid_regex, stderr)
        if m:
            print 'it already run, restart it..'
            pid = m.group('pid')
            kill_cmd = 'kill -9 %s' % pid
            subprocess.Popen(kill_cmd.split())
            runSSLocal(kwargs)
        else:
            print stderr
    else:
        print p.stdout.read()


def main():
    lst = getShadowSocksParam()
    choice = random.choice(lst)
    print 'run sslocal use config =>', choice
    runSSLocal(choice)

if __name__ == '__main__':
    main()
