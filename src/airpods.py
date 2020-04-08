import json
import asyncio,threading

from bleak import discover

class Airpods:
    def isFlipped(self, data):
        return format((int(""+data[10], 16)+(0x10)), 'b')[3] == '0'

    def parseValues(self, result, flipped):
        if result['model'] == 'e':
            result['model'] = "pro"
        else:
            result['model'] = "other"

        result['left'] = int(result['left'], 16) * 10
        result['right'] = int(result['right'], 16) * 10
        result['case'] = int(result['case'], 16) * 10

        if result['left'] > 100:
            result['left'] = -1

        if result['right'] > 100:
            result['right'] = -1

        if result['case'] > 100:
            result['case'] = -1

        chargeStatus = int(result['charging_case'], 16)
        if flipped:
            result['charging_left'] = (chargeStatus & 0b00000001) != 0
            result['charging_right'] = (chargeStatus & 0b00000010) != 0
        else:
            result['charging_left'] = (chargeStatus & 0b00000001) != 0
            result['charging_right'] = (chargeStatus & 0b00000010) != 0
        result['charging_case'] = (chargeStatus & 0b00000100) != 0

        return result

    async def run(self):
        result = self.EmptyResult()
        devices = await discover()

        for d in devices:
            try:
                if not 76 in d.metadata['manufacturer_data']:
                    continue
                if not len(d.metadata['manufacturer_data'][76]) == 27:
                    continue

                if result['status'] == 1 and result['rssi'] > d.rssi:
                    continue

                result['rssi'] = d.rssi
                result['addr'] = d.address
                
                hexData = d.metadata['manufacturer_data'][76].hex()
                flipped = self.isFlipped(hexData)
                if flipped:
                    result['left'] = "" + hexData[12]
                    result['right'] = "" + hexData[13]
                else:
                    result['left'] = "" + hexData[13]
                    result['right'] = "" + hexData[12]
                result['case'] = "" + hexData[15]
                result['charging_case'] = "" + hexData[14]
                result['charging_left'] = "" + hexData[14]
                result['charging_right'] = "" + hexData[14]
                result['model'] = "" + hexData[7]
                result['status'] = 1

                result = self.parseValues(result, flipped)

            except Exception as ex:
                result = self.EmptyResult()
                result["error"] = str(ex)

        return result

    def GetData(self):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.run())

    def GetDataJsonString(self):
        data = self.GetData()
        return json.dumps(data)

    def EmptyResult(self):
        result = {}
        result["status"] = 0
        result['left'] = -1
        result['right'] = -1
        result['case'] = -1
        result['charging_case'] = False
        result['charging_left'] = False
        result['charging_right'] = False
        result["error"] = ""
        result["rssi"] = -670
        result["addr"] = ""
        result['model'] = ""
        return result


if __name__ == '__main__':
    a = Airpods()
    while True:
        print(a.GetDataJsonString())
        print("---------------")
