# Airpods Windows Service

A Windows Service for reading Airpods Battery and some other informations.
Using this service, you can get your Airpods data as JSON over the named pipe.

## Requirements
- Windows 10, version 16299 (Fall Creators Update) or greater
- Bluetooth 4.0+

## Installation for End Users
soon

## Installation for Developers
1. Download/clone project
2. Run "build.bat". Executable file will automatically create in build folder.
2. In build folder, Run "airpods-windows-service.exe install" in cmd as Administrator or simply click "register-service.bat"
3. Run Service on Windows Services

or

1. Download/clone project
2. In src folder, Run "python3 service.py install" in cmd as Administrator
3. Run Service on Windows Services or simply run "python3 service.py start" as Administrator in same folder.
4. You can test the service without installing it with the command "python3 service.py debug".

## Usage
While the service is running, it will automatically send JSON data over the named pipe.
You can read pipe which named **airpods-windows-service** for reaching data.
The data looks like the following. You can use this JSON data in any application you create.

```
{
   "status" : 0, //IF AIRPODS FOUND IT RETURNS 1
   "error" : "", //IF ANY ERROR OCCURED, IT IS HERE
   "rssi" : -670, //RECEIVED SIGNAL STRENGTH INDICATIOR
   "addr" : "", //MAC ADDRESS FROM WHICH DATA IS TAKEN
   "left" : -1, //LEFT BATTERY LEVEL (0-100) (-1 is unknown)
   "right" : -1, //RIGHT BATTERY LEVEL (0-100) (-1 is unknown)
   "case" : -1, //CASE BATTERY LEVEL (0-100) (-1 is unknown)
   "model" : "", //"pro" or "other"
   "charging_case" : false, //IS CASE CHARGING (false = no or unknown)
   "charging_right" : false, //IS RIGHT CHARGING (false = no or unknown)
   "charging_left" : false //IS LEFT CHARGING (false = no or unknown)
}
```

## Referances
- [tzY15368](https://github.com/tzY15368)/**[WinPods](https://github.com/tzY15368/WinPods)**
- [adolfintel](https://github.com/adolfintel)/**[OpenPods](https://github.com/adolfintel/OpenPods)**
- [HaroldMills](https://github.com/HaroldMills)/**[Python-Windows-Service-Example](https://github.com/HaroldMills/Python-Windows-Service-Example)**

## Copyright and License
**Airpods Windows Service** is licensed under the GNU General Public License v3.0.
