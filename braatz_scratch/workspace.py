col = 'admin'.encode('utf-8')
col = col.decode('utf-8')
print(col)
if '"' in col:
    col = col.replace('"', '\\\\"')
if "'" in col:
    col = col.replace("'", "\\\\'")
col = col.encode('utf-8')
print(col)