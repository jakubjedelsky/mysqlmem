#!/usr/bin/env python
#
#   How much memory can my MySQL server eat?
#   Jakub Jedelsky <jakub.jedelsky@gmail.com>
#
#   Licensed under GPLv2+
#
#   It is based on maximum memory usage of mysql server:
#
#   Mysql_max_memory_usage =
#       Query_cache_size      +   Key_buffer_size         +
#       Myisam_sort_buffer_size   +   Innodb_buffer_pool_size     +
#       Innodb_log_buffer_size    +   Innodb_additional_mem_pool_size +
#       Max_connections       *
#       (
#           Sort_buffer_size        +   Read_buffer_size        +
#           Read_rnd_buffer_size    +   Join_buffer_size        +
#           Thread_stack
#       )
#
# Much more info about perfromance you cau get with mysqltuner:
#   http://mysqltuner.com/mysqltuner.pl
#
import os

MYSQL_CMD = "mysql -e 'show variables;'"

def get_variable(variable):
    return int(variables[variable])

def convert_bytes(bytes):
    bytes = float(bytes)
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2fT' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2fG' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2fM' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2fK' % kilobytes
    else:
        size = '%.2fb' % bytes
    return size

if __name__ == "__main__":
    v_temp = os.popen(MYSQL_CMD)

    variables = {}
    for line in v_temp.readlines():
        try:
            var = line.split(None, 1)[1]
        except IndexError:
            var =''
        variables[line.split()[0]] = var

    max_mem =   get_variable('query_cache_size') + get_variable('key_buffer_size') + \
                get_variable('myisam_sort_buffer_size') + get_variable('innodb_buffer_pool_size') + \
                get_variable('innodb_log_buffer_size') + get_variable('innodb_additional_mem_pool_size') + \
                get_variable('max_connections') * ( \
                    get_variable('sort_buffer_size') + get_variable('read_buffer_size') + \
                    get_variable('read_rnd_buffer_size') + get_variable('join_buffer_size') + \
                    get_variable('thread_stack') \
                )
    
    print convert_bytes(max_mem)
