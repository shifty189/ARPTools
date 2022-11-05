import unittest
import ARPTools

version = "0.01"
class TestSizeConverter(unittest.TestCase):
    def testNegative(self):
        expected = "Negative numbers are not supported: -50"
        actual = ARPTools.convert_size(-50)
        self.assertEqual(actual, expected)

    def testZero(self):
        actual = ARPTools.convert_size(0)
        self.assertEqual(actual, "0B")

    def testB(self):
        actual = ARPTools.convert_size(800)
        self.assertEqual(actual, "800.0 B")

    def testKB1(self):
        actual = ARPTools.convert_size(800000)
        self.assertEqual(actual, "781.25 KB")

    def testKB2(self):
        actual = ARPTools.convert_size(40000)
        self.assertEqual(actual, "39.06 KB")

    def testKB3(self):
        actual = ARPTools.convert_size(1048575)
        self.assertEqual(actual, "1024.0 KB")

    def testMB(self):
        actual = ARPTools.convert_size(1048576)
        self.assertEqual(actual, "1.0 MB")

    def testMB2(self):
        actual = ARPTools.convert_size(1024*7204)
        self.assertEqual(actual, "7.04 MB")

    def testGB(self):
        actual = ARPTools.convert_size(1073741824)
        self.assertEqual(actual, "1.0 GB")

    def testTB(self):
        actual = ARPTools.convert_size(10737418240008)
        self.assertEqual(actual, "9.77 TB")

    def testPB(self):
        actual = ARPTools.convert_size(107374182400083614)
        self.assertEqual(actual, "95.37 PB")


class TestVendorLookup(unittest.TestCase):
    def testVendorLookupBroadcast(self):
        actual = ARPTools.vendorLookup('ffffff')
        self.assertEqual(actual, 'Broadcast address')

    def testVendorLookupUnknown(self):
        actual = ARPTools.vendorLookup('aaaaa')
        self.assertEqual(actual, 'Unknown Vendor aa:aa:a')

    def testVendorLookupCisco(self):
        actual = ARPTools.vendorLookup('00000C')
        self.assertEqual(actual, 'Cisco')

    def testVendorLookupHyundai(self):
        actual = ARPTools.vendorLookup('00003B')
        self.assertEqual(actual, 'Hyundai')

    def testVendorLookupKyung(self):
        actual = ARPTools.vendorLookup('0005C1')
        expected = 'A-Kyung Motion, Inc.'
        self.assertEqual(actual, expected)

    def testVendorLookupVISION(self):
        actual = ARPTools.vendorLookup('0011A1')
        expected = 'VISION NETWARE CO.,LTD'
        self.assertEqual(actual, expected)



class TestStatusProcessNum(unittest.TestCase):
    def testStatusProcessNum(self):
        answer = False
        actual = ARPTools.systemStatus()
        if 'processNum' in actual: answer = True
        self.assertEqual(answer, True)

    def testStatusProcesses(self):
        answer = False
        actual = ARPTools.systemStatus()
        if 'processes' in actual: answer = True
        self.assertEqual(answer, True)


    def testStatus(self):
        answer = False
        actual = ARPTools.systemStatus()
        if 'CPUName' in actual: answer = True
        self.assertEqual(answer, True)



    def testStatusCPULoad(self):
        answer = False
        actual = ARPTools.systemStatus()
        if 'CPUload' in actual: answer = True
        self.assertEqual(answer, True)

    def testStatusDisks(self):
        answer = False
        actual = ARPTools.systemStatus()
        if 'disks' in actual: answer = True
        self.assertEqual(answer, True)

    def testStatusCpuRate(self):
        answer = False
        actual = ARPTools.systemStatus()
        if 'cpuRate' in actual: answer = True
        self.assertEqual(answer, True)

    def testStatusFreeRAM(self):
        answer = False
        actual = ARPTools.systemStatus()
        if 'freeRam' in actual: answer = True
        self.assertEqual(answer, True)

    def testStatusTotalRAM(self):
        answer = False
        actual = ARPTools.systemStatus()
        if 'totalRam' in actual: answer = True
        self.assertEqual(answer, True)


if __name__ == '__main__':
    unittest.main()
