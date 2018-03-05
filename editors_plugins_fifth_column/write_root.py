try:
    f = open("/stub.file", "wb")
    f.close()
except IOError as e:
    pass
