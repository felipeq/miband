# -*- mode: python; coding: utf-8 -*-


# NOTE: this class is for debugging purposes (it seems)
class cn_com_smartdevices_bracelet_r:
    @classmethod
    def d(cls):
        pass

    @classmethod
    def a(self, alias):
        pass

    @classmethod
    def c(self, intv):
        pass


class com_xiaomi_hm_bleservice_a_b(object):
    @classmethod
    def d(cls, data):
        """ This is the Dallas CRC8 algorithm """

        crc = 0
        for i in range(0, len(data)):
            crc = crc ^ (data[i] & 0xff)

            for j in range(8):
                if crc & 0x01:
                    crc = (crc >> 1) ^ 0x8c
                else:
                    crc >>= 1

        return crc


class com_xiaomi_hm_bleservice_profile_IMiLiProfile_UserInfo(object):
    CLEAR_DATA = 0x1
    NORMAL = 0x0
    RETAIN_DATA = 0x2
    SAMPLE = None

    @classmethod
    def clinit(cls):
        uid = 0xa2867cf
        gender = 0x0
        age = 0x17
        height = -0x58
        weight = 0x32
        alias = bytearray("anri.okita")

        cls.SAMPLE = cls(uid, gender, age, height, weight, alias, type)

    def __init__(self, uid, gender, age, height, weight, alias, type=0):
        self.uid = uid
        self.gender = gender  # 0 : female, !0 : male
        self.age = age        # years
        self.height = height  # cms
        self.weight = weight  # kg
        self.alias = alias
        self.type = type


class com_xiaomi_hm_bleservice_profile_MiLiProfile:
    def getDevice(self):
        raise NotImplementedError

    def write(self, char, data):
        raise NotImplementedError

    # NOTE: this is not tested!
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


### Some testing code, just remove it! ##########################################
def test_last_byte(byteseq, mac_last_byte):
    data = map(lambda x: int(x, 16), byteseq.split(":"))
    expected = data[-1]

    got = com_xiaomi_hm_bleservice_a_b.d(data[:-1])
    got = (got ^ mac_last_byte) & 0xff

    assert expected == got, "Not equal :(, {} != {}".format(got, expected)
    print "OK!"


if __name__ == '__main__':
    test_last_byte("2c:78:91:5c:01:2c:ae:5d:01:31:35:35:33:30:33:37:33:35:36:0f", 0xda)
    test_last_byte("7e:de:4e:5c:01:1e:bd:4e:00:31:35:34:38:36:37:32:36:33:38:f3", 0xda)
    test_last_byte("22:81:64:5c:01:18:b7:37:00:31:35:35:30:30:39:30:35:33:30:52", 0x68)
