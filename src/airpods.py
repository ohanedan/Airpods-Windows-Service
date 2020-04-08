import json
import asyncio,threading

from bleak import discover

class Airpods:
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
                
                print(hexData) #TODO: PARSE hexData

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
        result["error"] = ""
        result["rssi"] = -670
        result["addr"] = ""
        return result


if __name__ == '__main__':
    a = Airpods()
    print(a.GetDataJsonString())
