

class cn_com_smartdevices_bracelet_r:
    def d(self):
        pass

    def a(self, alias):
        pass

    def c(self, intv):
        pass


class com_xiaomi_hm_bleservice_a_b:
    def d(self, data):
        pass


# NOTE: this is not tested
def setUserInfo(self, info):
    cn_com_smartdevices_bracelet_r.d()

    data = bytearray(0x14)

    data[0] = info.uid & 0xff
    data[1] = (info.uid >> 8) & 0xff
    data[2] = (info.uid >> 0x10) & 0xff
    data[3] = (info.uid >> 0x18) & 0xff
    data[4] = info.gender
    data[5] = info.age
    data[6] = info.height
    data[7] = info.weight
    data[8] = info.type

    cn_com_smartdevices_bracelet_r.a(info.alias)

    v0 = 1
    if len(info.alias) > 10:
        v0 = 0

    cn_com_smartdevices_bracelet_r.c(v0)

    for i in range(0, len(info.alias)):
        data[i + 9] = info.alias[i]

    device = self.getDevice()
    addr = device.getAddress()

    b = com_xiaomi_hm_bleservice_a_b.d(data[:19])
    b = b ^ int(addr[-2:], 16)
    b = b & 0xff
    data[19] = b

    retval = self.write(self.m_CharUserInfo, data)
    return retval
